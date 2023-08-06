# -*- coding: utf-8 -*-
import click
import ipaddress
import json
import random
import subprocess
import tempfile
import git
import shutil
import os
import yaml

from spell.cli.exceptions import (
    api_client_exception_handler,
    ExitException,
)
from spell.cli.utils import HiddenOption, is_installed
from spell.cli.utils.kube_cluster_templates import (
    eks_cluster_aws_auth_string,
    generate_eks_cluster_autoscaler_yaml,
    generate_eks_cluster_secret_yaml,
    generate_gke_cluster_rbac_yaml,
    generate_cluster_ambassador_yaml,
    cluster_statsd_sink_yaml,
)


INGRESS_PORTS = [22, 2376, 9999]  # SSH, Docker Daemon, and Jupyter respectively


@click.group(name="cluster", short_help="Manage external clusters",
             help="Manage external clusters on Spell",
             hidden=True)
@click.pass_context
def cluster(ctx):
    pass


@cluster.command(name="init",
                 short_help="Sets up an AWS VPC as a Spell cluster", hidden=True)
@click.pass_context
@click.option("-n", "--name", "name", required=True, prompt="Enter a display name for this cluster within Spell",
              help="This will be used by Spell for you to identify the cluster")
@click.option("-p", "--profile", "profile", required=True, default=u"default",
              prompt="Enter the name of the AWS profile you would like to use",
              help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
                   "You will be prompted to confirm the Key and Region are correct before continuing. "
                   "This key will be used to create all the resources necessary for Spell to manage machines "
                   "in your external VPC. It must have permissions to create these resources.")
def create(ctx, name, profile):
    """
    This command sets an AWS VPC of your choosing as an external Spell cluster.
    This will let your organization run runs in that VPC, so your data never leaves
    your VPC. You set an S3 bucket of your choosing for all run outputs to be written to.
    After this cluster is set up you will be able to select the types and number of machines
    you would like Spell to create in this cluster.

    NOTE: This command uses your AWS credentials, found in ~/.aws/credentials to create the necessary
    AWS resources for Spell to access and manage those machines. Your AWS credentials will
    need permission to setup these resources.
    """

    # Verify the owner is the admin of an org
    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        owner_details = spell_client.get_owner_details()
        if owner_details.type == "user":
            raise ExitException("Only organizations can create clusters, use `spell owner` "
                                "to switch current owner to an organization ".format(ctx.obj["owner"]))
        if owner_details.requestor_role not in ("admin", "manager"):
            raise ExitException(
                "You must be a Manager or Admin with current org {} to proceed".format(ctx.obj["owner"]))

    try:
        import boto3
        from botocore.exceptions import BotoCoreError
    except ImportError:
        click.echo("Please pip install boto3 and rerun this command")
        return

    # Setup clients with the provided profile
    try:
        session = boto3.session.Session(profile_name=profile)
        s3 = session.resource("s3")
        ec2 = session.resource("ec2")
        iam = session.resource("iam")
    except BotoCoreError as e:
        click.echo("Failed to set profile {} with error: {}".format(profile, e))
        return
    click.echo("""This command will help you
    - Setup an S3 bucket to store your run outputs in
    - Setup a VPC which Spell will spin up workers in to run your jobs
    - Ensure subnets in the VPC in multiple availability zones
    - Upload spell-worker public to list of available keys in your account
    - Setup a Security Group providing Spell SSH and Docker access to workers
    - Setup an IAM role allowing Spell to spin up and down machines and access the S3 bucket""")
    if not click.confirm(
        "All of this will be done with your AWS profile '{}' which has "
        "Access Key ID '{}' and region '{}' - continue?".format(
            profile,
            session.get_credentials().access_key,
            session.region_name)):
        return

    bucket_name = get_bucket_name(ctx, s3, session.region_name)
    if bucket_name is None:
        return

    vpc = get_vpc(ec2, name)
    if vpc is None:
        return

    ensure_key_pair(ec2)

    security_group = get_security_group(ec2, vpc)
    if security_group is None:
        return

    role_arn, external_id, read_policy = get_role_arn(iam, bucket_name)
    if role_arn is None:
        return

    with api_client_exception_handler():
        spell_client.create_aws_cluster(name, role_arn, external_id, read_policy, security_group.id, bucket_name,
                                        vpc.id, [s.id for s in vpc.subnets.all()], session.region_name)
    echo_delimiter()
    click.echo("Your cluster {} is initialized! Head over to the web console to create machine types "
               "to execute your runs on.".format(name))


@cluster.command(name="gke-init", short_help="Sets up a GKE cluster to host model servers",
                 hidden=True)
@click.pass_context
@click.option("-c", "--cluster", "cluster_id", required=True, type=int,
              help="The spell cluster id that you would like to configure this "
                   "model serving GKE cluster to work with.")
@click.option("--auth-api-url", cls=HiddenOption, type=str,
              help="URL of the spell API server used by Ambassador for authentication. "
                   "This must be externally accessible")
@click.option("--gcp-project-name", type=str,
              help="Name of the GCP project to create the GKE cluster in")
@click.option("--gke-cluster-name", type=str, default="spell-model-serving",
              help="Name of the newly created GKE cluster")
@click.option("--nodes-min", type=int, default=1,
              help="Minimum number of nodes in the model serving cluster (default 1)")
@click.option("--nodes-max", type=int, default=2,
              help="Minimum number of nodes in the model serving cluster (default 2)")
@click.option("--node-disk-size", type=int, default=50,
              help="Size of disks on each node in GB (default 50GB)")
def gke_init(ctx, cluster_id, auth_api_url, gcp_project_name, gke_cluster_name,
             nodes_min, nodes_max, node_disk_size):
    """
    Configure an existing GKE cluster for model serving using your current
    `gcloud` credentials. You need to have both `kubectl` and `gcloud` installed.
    This command will install the necessary deployments and services to host
    model servers.
    """

    try:
        import kubernetes.client
        import kubernetes.config
    except ImportError:
        raise ExitException("kubernetes (for Python) is required. "
                            "Please `pip install kubernetes` and rerun this command")

    if not is_installed("gcloud"):
        raise ExitException("`gcloud` is required, please install it before proceeding")
    if not is_installed("kubectl"):
        raise ExitException("`kubectl` is required, please install it before proceeding")

    # Verify valid cluster_id
    spell_client = ctx.obj["client"]
    cluster = get_cluster(spell_client, ctx.obj["owner"], cluster_id)
    role_creds_gcp = cluster["role_credentials"]["gcp"]

    response = click.prompt("Create a GKE cluster for model serving? "
                            "You may skip this step if you have previously run it.",
                            type=click.Choice(["create", "skip"])).strip()
    if response == "create":
        create_gke_cluster(gke_cluster_name, gcp_project_name, role_creds_gcp["service_account_id"],
                           nodes_min, nodes_max, node_disk_size)

    elif response == "skip":
        click.echo("Skipping GKE cluster creation, existing contexts are:")
        subprocess.check_call(("kubectl", "config", "get-contexts"))
        kube_ctx = subprocess.check_output(("kubectl", "config", "current-context")).decode('utf-8').strip()
        correct_kube_ctx = click.confirm("Is context '{}' the GKE cluster to use for model serving?".format(kube_ctx))
        if not correct_kube_ctx:
            raise ExitException("Set context to correct GKE cluster with `kubectl config use-context`")

    # Create "serving" namespace
    # TODO(Benno): this doesn't work with GKE on the second run... Seems `gcloud` auth fails?!
    create_serving_namespace(kubernetes.config, kubernetes.client)

    # Give Spell permissions to the cluster (via RBAC)
    echo_delimiter()
    click.echo("Giving Spell RBAC permissions to GKE cluster...")
    try:
        rbac_yaml = generate_gke_cluster_rbac_yaml(role_creds_gcp["service_account_id"])
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(rbac_yaml)
            f.flush()
            subprocess.check_call(("kubectl", "apply", "--namespace", "serving", "--filename", f.name))
        click.echo("RBAC permissions granted!")
    except Exception as e:
        click.echo("ERROR: Giving Spell RBAC permissions failed. Error was: {}".format(e), err=True)

    # Add Ambassador
    echo_delimiter()
    click.echo("Setting up Ambassador...")
    try:
        ambassador_yaml = generate_cluster_ambassador_yaml(auth_api_url, cloud="gke")
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(ambassador_yaml)
            f.flush()
            subprocess.check_call(("kubectl", "apply", "--namespace", "serving", "--filename", f.name))
        click.echo("Ambassador set up!")
    except Exception as e:
        click.echo("ERROR: Setting up Ambassador failed. Error was: {}".format(e), err=True)

    # Add StatsD
    add_statsd()

    # Upload config to Spell API
    echo_delimiter()
    click.echo("Uploading config to Spell...")
    try:
        with tempfile.NamedTemporaryFile(mode="r", suffix=".yaml") as f:
            cmd = ("gcloud", "container", "clusters", "get-credentials", gke_cluster_name,
                   "--zone", "us-west2-a",
                   "--project", gcp_project_name)
            env = os.environ.copy()
            env["KUBECONFIG"] = f.name
            p = subprocess.Popen(cmd, env=env)
            p.communicate()
            if p.returncode != 0:
                raise Exception("gcloud command had exit code {}".format(p.returncode))
            parsed_yaml = yaml.load(f)

        # update kubeconfig to use the custom `gcp-svc` auth-provider
        if "users" not in parsed_yaml or \
           len(parsed_yaml["users"]) != 1 or \
           "user" not in parsed_yaml["users"][0] or \
           "auth-provider" not in parsed_yaml["users"][0]["user"]:
            raise Exception("Unexpected kubeconfig yaml generated from gcloud command")
        parsed_yaml["users"][0]["user"]["auth-provider"] = {
            "name": "gcp-svc",
            "config": {"service-acct": "%s"}
        }
        yaml_str = yaml.dump(parsed_yaml)

        with api_client_exception_handler():
            spell_client.set_kube_config(cluster_id, yaml_str)
        click.echo("Config successfully uploaded to Spell!")
    except Exception as e:
        click.echo("ERROR: Uploading config to Spell failed. Error was: {}".format(e), err=True)

    echo_delimiter()
    click.echo("Cluster setup complete!")


@cluster.command(name="eks-init", short_help="Sets up an EKS cluster to host model servers",
                 hidden=True)
@click.pass_context
@click.option("-p", "--profile", "aws_profile", required=True, default="default",
              prompt="Enter the name of the AWS profile you would like to use",
              help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
                   "You will be prompted to confirm the Key and Region are correct before continuing. "
                   "This key will be used to create all the resources necessary to host a cluster for model "
                   "serving. It must have permissions to create these resources.")
@click.option("-c", "--cluster", "cluster_id", required=True, type=int,
              help="The cluster id that you would like to configure this model serving cluster to work with.")
@click.option("--vpc-private-subnets", multiple=True,
              help="Specify if you want to use an existing VPC for your model server cluster. Use this option "
                   "in conjunction with --vpc-public-subnets to specify all the subnets for your cluster. The VPC will "
                   "be inferred from these subnets. Note that this command will not create any routing tables or other "
                   "resources, such as internet/NAT gateways. It will, however, create dedicated security groups for "
                   "use within cluster.\n\n"
                   "If you'd like a new VPC dedicated to this cluster, leave this and --vpc-public-subnets blank.")
@click.option("--vpc-public-subnets", multiple=True,
              help="Specify if you want to use an existing VPC for your model server cluster. Use this option "
                   "in conjunction with --vpc-private-subnets to specify all the subnets for your cluster. The "
                   "VPC will be inferred from these subnets. Note that this command will not create any routing "
                   "tables or other resources, such as internet/NAT gateways. It will, however, create dedicated "
                   "security groups for use within cluster.\n\n"
                   "If you'd like a new VPC dedicated to this cluster, leave this and --vpc-public-subnets blank.")
@click.option("--node-private-networking", is_flag=True,
              help="Specify if you prefer to isolate the nodes of your cluster from the public internet")
@click.option("--nodes-min", type=int, default=1,
              help="Minimum number of nodes in the model serving cluster (default 1)")
@click.option("--nodes-max", type=int, default=2,
              help="Minimum number of nodes in the model serving cluster (default 2)")
@click.option("--node-volume-size", type=int, default=50,
              help="Size of disks on each node in GB (default 50GB)")
@click.option("--auth-api-url", cls=HiddenOption, type=str,
              help="URL of the spell API server used by Ambassador for authentication. "
                   "This must be externally accessible")
@click.option("--eks-cluster-name", cls=HiddenOption, type=str, default="spell-model-serving",
              help="Name of the newly created EKS cluster")
def eks_init(ctx, aws_profile, cluster_id,
             vpc_private_subnets, vpc_public_subnets, node_private_networking,
             nodes_min, nodes_max, node_volume_size, auth_api_url, eks_cluster_name):
    """
    Create a new EKS cluster for model serving using your current
    AWS credentials. Your profile must have privileges to EC2, EKS, IAM, and
    CloudFormation. You need to have both `kubectl` and `eksctl` installed.
    This command will walk you through the process and allows users to specify
    networking and security options.

    NOTE: This can take a very long time (15-20 minutes), so make sure you are on a
    computer with a stable Internet connection and power before beginning.
    """

    # default auth_api_url to --api-url if it's not overriden by --auth-api-url
    auth_api_url = auth_api_url or ctx.obj["client_args"]["base_url"]

    try:
        import boto3
        from botocore.exceptions import BotoCoreError
        import kubernetes.client
        import kubernetes.config
    except ImportError:
        raise ExitException("boto3 and kubernetes are both required. "
                            "Please `pip install boto3 kubernetes` and rerun this command")

    if not is_installed("aws-iam-authenticator"):
        raise ExitException("`aws-iam-authenticator` is required, please install it before proceeding")
    if not is_installed("eksctl"):
        raise ExitException("`eksctl` is required, please install it before proceeding https://eksctl.io/")
    if not is_installed("kubectl"):
        raise ExitException("`kubectl` is required, please install it before proceeding")

    # Verify valid cluster_id
    spell_client = ctx.obj["client"]
    cluster = get_cluster(spell_client, ctx.obj["owner"], cluster_id)

    # Setup clients with the provided profile
    try:
        session = boto3.session.Session(profile_name=aws_profile)
        autoscaling = session.client("autoscaling")
        iam = session.resource("iam")
    except BotoCoreError as e:
        raise ExitException("Failed to set profile {} with error: {}".format(aws_profile, e))
    click.confirm("Profile '{}' has Access Key ID '{}' and region '{}' - continue?".format(
        aws_profile, session.get_credentials().access_key, session.region_name),
        default=True, abort=True)

    response = click.prompt("Create an EKS cluster for model serving? "
                            "You may skip this step if you have previously run it.",
                            type=click.Choice(["create", "skip"])).strip()
    if response == "create":
        create_eks_cluster(aws_profile, eks_cluster_name, session, vpc_private_subnets, vpc_public_subnets,
                           node_private_networking, nodes_min, nodes_max, node_volume_size)
    elif response == "skip":
        click.echo("Skipping EKS cluster creation, existing contexts are:")
        subprocess.check_call(("kubectl", "config", "get-contexts"))
        kube_ctx = subprocess.check_output(("kubectl", "config", "current-context")).decode('utf-8').strip()
        correct_kube_ctx = click.confirm("Is context '{}' the EKS cluster to use for model serving?".format(kube_ctx))
        if not correct_kube_ctx:
            raise ExitException("Set context to correct EKS cluster with `kubectl config use-context`")

    # Set up ClusterAutoscaling
    echo_delimiter()
    click.echo("Setting up Cluster Autoscaling...")
    try:
        asgs = [asg for asg in autoscaling.describe_auto_scaling_groups()["AutoScalingGroups"]
                if asg["AutoScalingGroupName"].startswith("eksctl-{}-nodegroup".format(eks_cluster_name))]
        if len(asgs) == 0 or len(asgs) > 1:
            raise ExitException("Failed to find AutoScalingGroup for cluster. Contact support@spell.run for assistance")
        ca_yaml = generate_eks_cluster_autoscaler_yaml(nodes_min, nodes_max, asgs[0]["AutoScalingGroupName"])
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(ca_yaml)
            f.flush()
            subprocess.check_call(("kubectl", "apply", "--filename", f.name))
        click.echo("Cluster Autoscaling set up!")
    except Exception as e:
        click.echo("ERROR: Cluster Autoscaling failed to set up. Error was: {}".format(e), err=True)

    # Set up metrics-server
    echo_delimiter()
    click.echo("Setting up metrics-server for HPA...")
    tmp_dir = tempfile.mkdtemp()
    try:
        git.Git(tmp_dir).clone("https://github.com/kubernetes-incubator/metrics-server")
        subprocess.check_call(
            ("kubectl", "apply", "--filename", os.path.join(tmp_dir, "metrics-server", "deploy", "1.8+"))
        )
        click.echo("metrics-server set up!")
    except Exception as e:
        click.echo("ERROR: metrics-server failed to set up. Error was: {}".format(e), err=True)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        tmp_dir = None

    # Create "serving" namespace
    create_serving_namespace(kubernetes.config, kubernetes.client)

    # Give Spell permissions to the cluster
    echo_delimiter()
    click.echo("Giving Spell permissions to the cluster...")
    try:
        kube_api = kubernetes.client.CoreV1Api()
        conf_map = kube_api.read_namespaced_config_map("aws-auth", "kube-system", exact=True, export=True)
        if "arn:aws:iam::002219003547:role/nodes.prod.spell" in conf_map.data["mapRoles"]:
            click.echo("Spell permissions already in the cluster! Skipping.")
        else:
            conf_map.data["mapRoles"] += eks_cluster_aws_auth_string
            kube_api.replace_namespaced_config_map("aws-auth", "kube-system", conf_map)
            click.echo("Spell permissions granted!")
    except Exception as e:
        click.echo("ERROR: Giving Spell permissions to the cluster failed. Error was: {}".format(e), err=True)

    # Add Ambassador
    echo_delimiter()
    click.echo("Setting up Ambassador...")
    try:
        ambassador_yaml = generate_cluster_ambassador_yaml(auth_api_url)
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(ambassador_yaml)
            f.flush()
            subprocess.check_call(("kubectl", "apply", "--namespace", "serving", "--filename", f.name))
        click.echo("Ambassador set up!")
    except Exception as e:
        click.echo("ERROR: Setting up Ambassador failed. Error was: {}".format(e), err=True)

    # Create SpellReadS3 IAM User
    echo_delimiter()
    policy_name = cluster["role_credentials"]["aws"]["read_policy"]
    suffix = policy_name.split("-")[-1]  # Get the ID suffix off the policy name
    user_name = "SpellReadS3User-{}".format(suffix)
    click.echo("Creating and configuring {} IAM user...".format(user_name))
    try:
        existing_users = [u for u in iam.users.all() if user_name == u.name]
        if len(existing_users) > 0:
            user = existing_users[0]
            click.echo("Existing {} user found".format(user_name))
        else:
            user = iam.create_user(UserName=user_name)
            click.echo("New {} user created".format(user_name))
        if len([p for p in user.attached_policies.all() if p.policy_name == policy_name]) == 0:
            matching_policies = [p for p in iam.policies.all() if p.policy_name == policy_name]
            if len(matching_policies) != 1:
                raise ExitException("Found unexpected number of policies named "
                                    "'{}': {}".format(policy_name, len(matching_policies)))
            s3_read_policy = matching_policies[0]
            user.attach_policy(PolicyArn=s3_read_policy.arn)
            click.echo("Policy {} attached to user".format(policy_name))
        for existing_access_key in user.access_keys.all():
            existing_access_key.delete()
        access_key = user.create_access_key_pair()
        iam_access_key, iam_secret_key = access_key.access_key_id, access_key.secret_access_key
        click.echo("{} user new access key pair created".format(user_name))
    except Exception as e:
        raise ExitException("Unable to create and attach IAM policies. Error: {}".format(e))

    # Create secrets on cluster with SpellReadS3 IAM user
    echo_delimiter()
    click.echo("Setting secrets on the cluster...")
    try:
        secret_yaml = generate_eks_cluster_secret_yaml(iam_access_key, iam_secret_key)
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(secret_yaml)
            f.flush()
            subprocess.check_call(("kubectl", "apply", "--filename", f.name))
        click.echo("Cluster Secrets set up!")
    except Exception as e:
        raise ExitException("Unable to apply secrets to cluster. Error: {}".format(e))

    # Add StatsD
    add_statsd()

    # Upload config to Spell API
    echo_delimiter()
    click.echo("Uploading config to Spell...")
    try:
        with tempfile.NamedTemporaryFile(mode="r", suffix=".yaml") as f:
            cmd = ("eksctl", "utils", "write-kubeconfig",
                   "--profile", aws_profile,
                   "--name", eks_cluster_name,
                   "--kubeconfig", f.name)
            subprocess.check_call(cmd)
            config_yaml = f.read()
        with api_client_exception_handler():
            spell_client.set_kube_config(cluster_id, config_yaml)
        click.echo("Config successfully uploaded to Spell!")
    except Exception as e:
        click.echo("ERROR: Uploading config to Spell failed. Error was: {}".format(e), err=True)

    echo_delimiter()
    click.echo("Cluster setup complete!")


def get_cluster(spell_client, owner, cluster_id):
    """
    Verify valid cluster_id for current owner, and return that cluster
    """
    with api_client_exception_handler():
        owner_details = spell_client.get_owner_details()
        if owner_details.type != "organization":
            raise ExitException("Only organizations can create clusters, use `spell owner` "
                                "to switch current owner to an organization ")
        if owner_details.requestor_role not in ("admin", "manager"):
            raise ExitException(
                "You must be a Manager or Admin with current org {} to proceed".format(owner))
        return spell_client.get_cluster(cluster_id)  # This will throw if the cluster id is invalid


def create_serving_namespace(kconfig, kclient):
    echo_delimiter()
    click.echo("Creating 'serving' namespace...")
    try:
        kconfig.load_kube_config()
        kube_api = kclient.CoreV1Api()
        if len([i for i in kube_api.list_namespace().items if i.metadata.name == 'serving']) > 0:
            click.echo("'serving' namespace already exists!")
        else:
            kube_api.create_namespace(
                kclient.V1Namespace(metadata=kclient.V1ObjectMeta(name="serving")))
            click.echo("'serving' namespace created!")
        subprocess.check_call(("kubectl", "config", "set-context", "--current", "--namespace=serving"))
    except Exception as e:
        raise ExitException("ERROR: Creating 'serving' namespace failed. Error was: {}".format(e))


def add_statsd():
    echo_delimiter()
    click.echo("Setting up StatsD...")
    try:
        with tempfile.NamedTemporaryFile(suffix=".yaml", mode="w+") as f:
            f.write(cluster_statsd_sink_yaml)
            f.flush()
            subprocess.check_call(("kubectl", "apply", "--namespace", "serving", "--filename", f.name))
        click.echo("StatsD set up!")
    except Exception as e:
        click.echo("ERROR: Setting up StatsD failed. Error was: {}".format(e), err=True)


def create_gke_cluster(cluster_name, gcp_project_name, service_account_id, nodes_min, nodes_max, node_disk_size):
    """Create the GKE cluster with `gcloud`"""

    try:
        cmd = ["gcloud", "config", "list", "compute/zone", "--format", "value(compute.zone)"]
        backplane_zone = subprocess.check_output(cmd).decode('utf-8').strip()
        backplane_zone = click.prompt("Enter the compute zone for your GKE cluster backplane",
                                      default=backplane_zone).strip()

        additional_node_zones = click.prompt("Enter the additional compute zones for your GKE cluster nodes "
                                             "(comma separated). The backplane zone is already included. "
                                             "Nodes will be in the same zone as the backplane by default, but "
                                             "you can optionally add any additional zones here. Note that each "
                                             "zone specified will always have a minimum of {} nodes".format(nodes_min),
                                             default="").strip().split(",")

        cmd = [
            "gcloud", "container", "clusters", "create", cluster_name,
            "--project", gcp_project_name,
            "--zone", backplane_zone,
            "--node-locations", ",".join([backplane_zone] + additional_node_zones),
            "--addons=HorizontalPodAutoscaling",
            "--enable-autoscaling",
            "--num-nodes", "1", "--min-nodes", str(nodes_min), "--max-nodes", str(nodes_max),
            "--service-account", service_account_id,
            "--disk-size", str(node_disk_size),
            "--no-enable-cloud-logging",
            "--no-enable-cloud-monitoring",
            "--labels=spell=model_serving",
            "--no-enable-basic-auth",
        ]
        click.echo("Creating the cluster. This can take a while...")
        subprocess.check_call(cmd)
        click.echo("Cluster created!")

        click.echo("Giving current gcloud user cluster-admin...")
        cmd = ["gcloud", "config", "list", "account", "--format", "value(core.account)"]
        gcloud_user = subprocess.check_output(cmd).decode('utf-8').strip()
        cmd = [
            "kubectl", "create", "clusterrolebinding", "cluster-admin-binding",
            "--clusterrole", "cluster-admin",
            "--user", gcloud_user,
        ]
        subprocess.check_call(cmd)
        click.echo("Current gcloud user {} granted cluster-admin".format(gcloud_user))

    except subprocess.CalledProcessError:
        raise ExitException("Failed to run `gcloud`. Make sure it's installed correctly and "
                            "your inputs are valid. Error details are above in the `gcloud` output.")


def create_eks_cluster(aws_profile, cluster_name, session,
                       vpc_private_subnets, vpc_public_subnets, node_private_networking,
                       nodes_min, nodes_max, node_volume_size):
    """Create the EKS cluster with eksctl"""

    cmd = [
        "eksctl", "create", "cluster",
        "--profile", aws_profile,
        "--name", cluster_name,
        "--region", session.region_name,
        "--version", "1.11",
        "--nodegroup-name", "ng",
        "--node-type", "m5.large",
        "--nodes-min", str(nodes_min),
        "--nodes-max", str(nodes_max),
        "--node-volume-size", str(node_volume_size),
        "--asg-access",
    ]
    if vpc_private_subnets:
        cmd.append("--vpc-private-subnets={}".format(",".join(vpc_private_subnets)))
    if vpc_public_subnets:
        cmd.append("--vpc-public-subnets={}".format(",".join(vpc_public_subnets)))
    if node_private_networking:
        cmd.append("--node-private-networking")

    try:
        click.echo("Creating the cluster. This can take a while...")
        subprocess.check_call(cmd)
        click.echo("Cluster created!")
    except subprocess.CalledProcessError:
        raise ExitException("Failed to run `eksctl`. Make sure it's installed correctly and "
                            "your inputs are valid. Error details are above in the `eksctl` output.")


def echo_delimiter():
    click.echo("---------------------------------------------")


def get_bucket_name(ctx, s3, region):
    from botocore.exceptions import BotoCoreError, ClientError

    echo_delimiter()
    response = click.prompt("We recommend an empty S3 Bucket for Spell outputs would "
                            "you like to make a new bucket or use an existing",
                            type=click.Choice(["new", 'existing', 'quit'])).strip()
    if response == "quit":
        return None

    if response == "new":
        owner_name = ctx.obj["owner"]
        bucket_name = click.prompt(
            "Please enter a name for the S3 Bucket Spell will create for run outputs",
            default=u"spell-{}".format(owner_name.lower())).strip()
        if not bucket_name.islower():
            click.echo("AWS does not support capital letter in the bucket name")
            return get_bucket_name(ctx, s3, region)
        if "_" in bucket_name:
            click.echo("AWS does not allow underscores in bucket name")
            return get_bucket_name(ctx, s3, region)

        try:
            if region == "us-east-1":
                s3.create_bucket(Bucket=bucket_name, ACL="private")
            else:
                s3.create_bucket(Bucket=bucket_name,
                                 ACL="private",
                                 CreateBucketConfiguration={"LocationConstraint": region})
        except ClientError as e:
            raise ExitException("Unable to create bucket. AWS error: {}".format(e))
        click.echo("Created your new bucket {}!".format(bucket_name))
        return bucket_name

    bucket_name = click.prompt("Enter the bucket name", type=str).strip()
    try:
        if bucket_name not in [b.name for b in s3.buckets.all()]:
            click.echo("Can't find bucket {}".format(bucket_name))
            return get_bucket_name(ctx, s3, region)
    except BotoCoreError as e:
        click.echo("Unable to check if this is a valid bucket name due to error: {}".format(e))
        return get_bucket_name(ctx, s3, region)
    return bucket_name


def get_vpc(ec2, cluster_name):
    from botocore.exceptions import BotoCoreError, ClientError

    echo_delimiter()
    response = click.prompt("Would you like to make a new VPC or use an existing one",
                            type=click.Choice(["new", "existing", "quit"])).strip()
    if response == "quit":
        return None

    if response == "existing":
        vpc_id = click.prompt("Enter the VPC ID", type=str).strip()
        vpc = ec2.Vpc(vpc_id)
        try:
            vpc.load()
            if len(list(vpc.subnets.all())) == 0:
                click.echo("VPC {} has no subnets. Subnets are required to launch instances. "
                           "Please select a VPC with subnets or create a new one and we will "
                           "populate it with subnets.".format(vpc_id))
                return get_vpc(ec2, cluster_name)
        except ClientError:
            click.echo("Unable to find VPC {}".format(vpc_id))
            return get_vpc(ec2, cluster_name)
        return vpc

    cidr = click.prompt("Enter a CIDR for your new VPC or feel free to use the default",
                        default=u"10.0.0.0/16").strip()
    try:
        vpc = ec2.create_vpc(CidrBlock=cidr)
        vpc.wait_until_available()
        vpc.create_tags(Tags=[{"Key": "Name", "Value": "Spell-{}".format(cluster_name)}])
    except BotoCoreError as e:
        raise ExitException("Unable to create VPC. AWS error: {}".format(e))
    click.echo("Created a new VPC with ID {}!".format(vpc.id))

    # Create subnets
    zones = [z[u'ZoneName'] for z in ec2.meta.client.describe_availability_zones()[u'AvailabilityZones']]
    zones = zones[:8]  # Max at 8 since we use 3 bits of the cidr range for subnets
    cidr_generator = ipaddress.ip_network(cidr).subnets(3)
    subnets = []
    for zone in zones:
        subnet_cidr = str(next(cidr_generator))
        try:
            subnet = vpc.create_subnet(AvailabilityZone=zone, CidrBlock=subnet_cidr)
            # By default give instances launched in this subnet a public ip
            resp = subnet.meta.client.modify_subnet_attribute(SubnetId=subnet.id, MapPublicIpOnLaunch={"Value": True})
            if resp[u'ResponseMetadata'][u'HTTPStatusCode'] != 200:
                click.echo("WARNING: Unable to set subnet {} to launch instances with "
                           "public ip address. This is required for Spell.".format(subnet.id))
            subnets.append(subnet.id)
            click.echo("Created a new subnet {} in your new VPC in availability-zone {} "
                       "and a CIDR of {}".format(subnet.id, zone, subnet_cidr))
        except BotoCoreError as e:
            click.echo(e)
    if len(subnets) == 0:
        raise ExitException("Unable to make any subnets in your new VPC. Contact Spell for support")

    # Create internet gateway
    gateway = ec2.create_internet_gateway()
    resp = vpc.attach_internet_gateway(InternetGatewayId=gateway.id)
    if resp[u'ResponseMetadata'][u'HTTPStatusCode'] != 200:
        raise ExitException("Failed to attach internet gateway {} to vpc".format(gateway.id))
    route_tables = list(vpc.route_tables.all())
    if len(route_tables) == 0:
        raise ExitException("No route table found on VPC, unable to set route for internet gateway")
    route_table = route_tables[0]
    route_table.create_route(DestinationCidrBlock=u'0.0.0.0/0', GatewayId=gateway.id)
    click.echo("Created internet gateway {} for new VPC".format(gateway.id))

    return vpc


def ensure_key_pair(ec2):
    key_name = "spell-worker"
    if key_name not in [k[u"KeyName"] for k in ec2.meta.client.describe_key_pairs()[u"KeyPairs"]]:
        ec2.import_key_pair(KeyName=key_name, PublicKeyMaterial=u"ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAACAQC"
                            u"2cMD2wG/nQYAGfOpx/1L6M1TeBRSc0XOPgiO+GLlu5B644rtqNItKTWMSt4sIUh+1JYorbNeSnBy"
                            u"t5OTFkUAgV6ATUKQnqMwNHBOMBk1gGN9BOj3BGYcDI7iZ9tW1w3X2i6Z+GhfjBFX4oHfgV8rN2aW"
                            u"NxaSRhBp+SoIy+nJdmRB2owLbhdCctjuGOiW8ir9YgPufu2GjVHS/rWmeFPsbzrH5vMe2UsdzBsh"
                            u"MEJG7gVmMV1RQeeWyWsItIV05sejRTSc4LUMJ98l2Y6CdB9E35g/yPaqfDHnufxdG0om6RKxEXU7"
                            u"7FqGoXeAfpmHHV6EVnQLapGE44ysGQ0wGV0TOvkL4D5IVivTFtuG6WSespjSirxsSvcgOgLrllce"
                            u"IpfE0ZV51bwxeSBrk+/7HUZebFlA7ymKGju/XwyHBkmLWTz+VXz6TIMsGNotAph58wOCZ5aGvrvS"
                            u"rJgdMUc+lKsVH052DNdfilAUscp0tqyZkjap5tLQnTb8K6N6f7g9ZAKPOi4lTh+UocFX6Oe2es8O"
                            u"3A1QU7dOGodSfJW0POblFujrAFzcwNxmBlN8M61FHTMo3aHrFXGBygj/oYBHKHjbjEw0cQXFtFbD"
                            u"QcfGMQCONgDBV1aepzK5+mrflu55KipuodKIqKjQqv2NlC6g3vrlyogQMaFwEihSE2YMOUAVK+w==")
        click.echo("Uploaded the {} public key to your aws keys.".format(key_name))
    else:
        click.echo("Found an existing {} public key".format(key_name))


def get_security_group(ec2, vpc):
    from botocore.exceptions import BotoCoreError

    # Check for existing Spell-Ingress group otherwise create one
    try:
        existing = [x for x in vpc.security_groups.all() if x.group_name == "Spell-Ingress"]
    except BotoCoreError:
        raise ExitException("Unable to query for existing security groups")

    if len(existing) > 1:
        raise ExitException("Found multiple Spell-Ingress security groups for vpc {}".format(vpc.id))
    if len(existing) > 0:
        security_group = existing[0]
        # Check that both port 22 and 2376 have rules
        existing_ports = [dict.get(p, "ToPort") for p in security_group.ip_permissions]
        for port in INGRESS_PORTS:
            if port not in existing_ports:
                raise ExitException(
                    "Found Spell-Ingress security group but it doesn't have ingress rules for port {}".format(port))
        click.echo("Found existing Spell-Ingress security group {}".format(security_group.id))
        return security_group

    try:
        security_group = vpc.create_security_group(
            GroupName="Spell-Ingress",
            Description="Allows the Spell API SSH and Docker access to worker machines",
        )
        for port in INGRESS_PORTS:
            security_group.authorize_ingress(CidrIp="0.0.0.0/0", FromPort=port, ToPort=port, IpProtocol="tcp")
        security_group.authorize_ingress(IpPermissions=[{
            'IpProtocol': '-1',
            'FromPort': 0,
            'ToPort': 65355,
            'UserIdGroupPairs': [{'GroupId': security_group.id, 'VpcId': security_group.vpc_id}],
        }])
        click.echo("Successfully created security group {}".format(security_group.id))
        return security_group
    except BotoCoreError as e:
        raise ExitException("Unable to create new security group in VPC. AWS error: {}".format(e))


# Returns a tuple of
# role_arn: the full ARN of the IAM role
# external_id: the external_id required to assume this role
# read_policy: the name of the s3 policy that allows read access to selected buckets
def get_role_arn(iam, bucket_name):
    from botocore.exceptions import ClientError

    echo_delimiter()
    response = click.prompt("Would you like to make a new IAM Role or use an existing one?\n We recommend making "
                            "a new one. If you do use an existing one it must grant all the permissions Spell "
                            "requires to manage machines and access S3.",
                            type=click.Choice(["new", "existing", "quit"])).strip()
    if response == "quit":
        return None, None

    if response == "existing":
        role_name = click.prompt("Please enter the Role Name").strip()
        external_id = click.prompt(
            "Please enter the External ID for this Role (or 'back' to make a new IAM Role instead)").strip()
        if external_id == "back":
            return get_role_arn(iam, bucket_name)
        try:
            role = iam.Role(role_name)
            role_arn = role.arn
            attached_policies = role.attached_policies.all()
            read_policies = [p for p in attached_policies if p.policy_name.startswith("SpellReadS3")]
            if len(read_policies) != 1:
                click.echo("Role {} has {} policies s3 reader policies. "
                           "Needs to have exactly 1".format(role_arn, len(read_policies)))
                return get_role_arn(iam, bucket_name)
            read_policy = read_policies[0].name
            click.echo("Found role {} with arn {} and read policy {}".format(role_name, role_arn, read_policy))
            return role_arn, external_id, read_policy
        except ClientError:
            click.echo("Can't find role with name {}".format(role_name))
            return get_role_arn(iam, bucket_name)

    read_buckets = click.prompt("Please list all buckets you would like Spell to be able to read from "
                                "(comma separated).\nIf you would like Spell to have read only access to "
                                "any bucket type 'all'",
                                default="")

    write_bucket_arn = "arn:aws:s3:::{}".format(bucket_name)
    write_bucket_objects_arn = "arn:aws:s3:::{}/*".format(bucket_name)

    read_bucket_arns = [write_bucket_arn, write_bucket_objects_arn]
    if read_buckets == "all":
        read_bucket_arns = "*"
    else:
        for bucket in read_buckets.split(","):
            bucket = bucket.strip()
            if len(bucket) > 0:
                read_bucket_arns.append("arn:aws:s3:::{}".format(bucket))
                read_bucket_arns.append("arn:aws:s3:::{}/*".format(bucket))

    suffix = str(random.randint(10**6, 10**7))
    read_policy = "SpellReadS3-{}".format(suffix)
    policies = {
        "SpellEC2-{}".format(suffix): [
            {
                "Sid": "EC2",
                "Effect": "Allow",
                "Action": [
                    "s3:GetAccountPublicAccessBlock",
                    "ec2:*",
                    "s3:HeadBucket"
                ],
                "Resource": "*"
            },
            {
                "Sid": "DenyTerminate",
                "Effect": "Deny",
                "Action": [
                    "ec2:TerminateInstances",
                    "ec2:StopInstances"
                ],
                "Resource": "*",
                "Condition": {
                    "StringNotEquals": {
                        "ec2:ResourceTag/spell-machine": "true"
                    }
                }
            }
        ],
        read_policy: {
            "Sid": "ReadS3",
            "Effect": "Allow",
            "Action": [
                "s3:ListBucketByTags",
                "s3:GetLifecycleConfiguration",
                "s3:GetBucketTagging",
                "s3:GetInventoryConfiguration",
                "s3:GetObjectVersionTagging",
                "s3:ListBucketVersions",
                "s3:GetBucketLogging",
                "s3:ListBucket",
                "s3:GetAccelerateConfiguration",
                "s3:GetBucketPolicy",
                "s3:GetObjectVersionTorrent",
                "s3:GetObjectAcl",
                "s3:GetEncryptionConfiguration",
                "s3:GetBucketRequestPayment",
                "s3:GetObjectVersionAcl",
                "s3:GetObjectTagging",
                "s3:GetMetricsConfiguration",
                "s3:GetBucketPublicAccessBlock",
                "s3:GetBucketPolicyStatus",
                "s3:ListBucketMultipartUploads",
                "s3:GetBucketWebsite",
                "s3:GetBucketVersioning",
                "s3:GetBucketAcl",
                "s3:GetBucketNotification",
                "s3:GetReplicationConfiguration",
                "s3:ListMultipartUploadParts",
                "s3:GetObject",
                "s3:GetObjectTorrent",
                "s3:GetBucketCORS",
                "s3:GetAnalyticsConfiguration",
                "s3:GetObjectVersionForReplication",
                "s3:GetBucketLocation",
                "s3:GetObjectVersion"
            ],
            "Resource": read_bucket_arns
        },
        "SpellWriteS3-{}".format(suffix): {
            "Sid": "WriteS3",
            "Effect": "Allow",
            "Action": [
                "s3:PutAnalyticsConfiguration",
                "s3:PutAccelerateConfiguration",
                "s3:DeleteObjectVersion",
                "s3:ReplicateTags",
                "s3:RestoreObject",
                "s3:ReplicateObject",
                "s3:PutEncryptionConfiguration",
                "s3:DeleteBucketWebsite",
                "s3:AbortMultipartUpload",
                "s3:PutBucketTagging",
                "s3:PutLifecycleConfiguration",
                "s3:PutObjectTagging",
                "s3:DeleteObject",
                "s3:PutBucketVersioning",
                "s3:DeleteObjectTagging",
                "s3:PutMetricsConfiguration",
                "s3:PutReplicationConfiguration",
                "s3:PutObjectVersionTagging",
                "s3:DeleteObjectVersionTagging",
                "s3:PutBucketCORS",
                "s3:PutInventoryConfiguration",
                "s3:PutObject",
                "s3:PutBucketNotification",
                "s3:PutBucketWebsite",
                "s3:PutBucketRequestPayment",
                "s3:PutBucketLogging",
                "s3:ReplicateDelete"
            ],
            "Resource": [write_bucket_arn, write_bucket_objects_arn]
        }
    }

    spell_aws_arn = "arn:aws:iam::002219003547:root"
    external_id = str(random.randint(10**8, 10**9))
    assume_role_policy = json.dumps({
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": spell_aws_arn
                },
                "Action": "sts:AssumeRole",
                "Condition": {
                    "StringEquals": {
                        "sts:ExternalId": external_id
                    }
                }
            }
        ]
    })

    try:
        role_name = "SpellAccess-{}".format(suffix)
        role = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=assume_role_policy,
            Description="Grants Spell EC2 and S3 access")
    except ClientError as e:
        raise ExitException("Unable to create new IAM role. AWS error: {}".format(e))

    try:
        for name, statement in policies.items():
            iam_policy = iam.create_policy(
                PolicyName=name,
                PolicyDocument=json.dumps({"Version": "2012-10-17", "Statement": statement}))
            role.attach_policy(PolicyArn=iam_policy.arn)
    except ClientError as e:
        raise ExitException("Unable to create and attach IAM policies. AWS error: {}".format(e))

    click.echo("Successfully created IAM role {}".format(role_name))
    return role.arn, external_id, read_policy


@cluster.command(name="add-bucket",
                 short_help="Adds a cloud storage bucket to SpellFS", hidden=True)
@click.pass_context
@click.option("-p", "--profile", "profile", required=True, default=u"default",
              prompt="Enter the name of the AWS profile you would like to use",
              help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
                   "You will be prompted to confirm the Key and Region are correct before continuing. "
                   "This key will be used to adjust IAM permissions of the role associated with the cluster "
                   "that the bucket is being added to.")
@click.option("--bucket", "bucket_name", help="Name of bucket")
# TODO(peter): Take in cluster name instead of cluster ID once we have a list clusters endpoint
@click.option("--cluster-id", type=int, default=1, help="ID of cluster to add bucket permissions to, defaults to 1")
def add_bucket(ctx, profile, bucket_name, cluster_id):
    """
    This command adds a cloud storage bucket to SpellFS, which enables interaction with the bucket objects
    via ls, cp, and mounts. It will also add bucket read permissions to the AWS role associated with the
    cluster.

    NOTE: This command uses your AWS credentials, found in ~/.aws/credentials to create the necessary
    AWS resources for Spell to access the remote storage bucket. Your AWS credentials will
    need permission to setup these resources.
    """
    try:
        import boto3
        import botocore
        from botocore.exceptions import BotoCoreError
    except ImportError:
        click.echo("Please pip install boto3 and rerun this command")
        return

    try:
        session = boto3.session.Session(profile_name=profile)
    except BotoCoreError as e:
        click.echo("Failed to set profile {} with error: {}".format(profile, e))
        return

    # Retrieve Spell cluster
    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        cluster = spell_client.get_cluster(cluster_id)

    click.echo("""This command will
    - List your buckets to generate an options menu of buckets that can be added to Spell
    - Add list and read permissions for that bucket to the IAM role associated with the cluster""")
    if not click.confirm(
        "All of this will be done with your AWS profile '{}' which has "
        "Access Key ID '{}' and region '{}' - continue?".format(
            profile,
            session.get_credentials().access_key,
            session.region_name)):
        return

    # Set up clients with the provided profile
    try:
        s3 = session.resource("s3")
        iam = session.resource("iam")
    except BotoCoreError as e:
        click.echo("Failed to get clients with profile {}: {}".format(profile, e))
        return

    # Get all buckets
    all_buckets = [bucket.name for bucket in s3.buckets.all()]

    # Prompt for bucket name
    if bucket_name is None:
        bucket_names = [bucket.name for bucket in s3.buckets.all()]
        for bucket in bucket_names:
            click.echo("- {}".format(bucket))
        bucket_name = click.prompt("Please choose a bucket")

    # Check if bucket is public if the bucket name is not one of the returned
    bucket_is_public = False
    if bucket_name not in all_buckets:
        # Set up an anonymous client
        anon_s3 = session.resource("s3", config=botocore.client.Config(signature_version=botocore.UNSIGNED))
        try:
            list(anon_s3.Bucket(bucket_name).objects.limit(count=1))
        except botocore.exceptions.ClientError:
            click.echo("Bucket {} is not accessible".format(bucket_name))
            return
        bucket_is_public = True

    # Skip IAM role management logic if bucket is public
    if bucket_is_public:
        click.echo("Bucket {} is public, no IAM updates required.".format(bucket_name))
        with api_client_exception_handler():
            spell_client.add_bucket(bucket_name, cluster_id, "s3")
        click.echo("Bucket {} has been added to cluster {}!".format(bucket_name, cluster_id))
        return

    # Add bucket read permissions to policy
    policy_name = cluster["role_credentials"]["aws"]["read_policy"]
    policies = [p for p in iam.policies.all() if p.policy_name == policy_name]
    if len(policies) != 1:
        click.echo("Found {} policies with name {}".format(len(policies), policy_name))
        return
    policy = policies[0]
    print(policy_name, policy)
    current_policy_version = policy.default_version
    policy_document = current_policy_version.document
    read_resources = policy_document["Statement"]["Resource"]
    bucket_arn = "arn:aws:s3:::{}".format(bucket_name)
    if read_resources != "*" and bucket_arn not in read_resources:
        policy_document["Statement"]["Resource"] += [bucket_arn, bucket_arn+"/*"]
        click.echo("Creating new version of policy {} with read access to {}...".format(policy.arn, bucket_name))
        new_version = policy.create_version(PolicyDocument=json.dumps(policy_document), SetAsDefault=True)
        click.echo("Created new version {} of policy {}.".format(new_version.arn, policy.arn))
        click.echo("Pruning old version {} of policy {}...".format(current_policy_version.arn, policy.arn))
        current_policy_version.delete()
    else:
        click.echo("Policy {} has permissions to access {}".format(policy.arn, bucket_arn))

    # Register new bucket to cluster in API
    with api_client_exception_handler():
        spell_client.add_bucket(bucket_name, cluster_id, "s3")
    click.echo("Bucket {} has been added to cluster {}!".format(bucket_name, cluster_id))


@cluster.command(name="update",
                 short_help="Makes sure your Spell cluster is fully up to date and able to support the latest features",
                 hidden=True)
@click.pass_context
@click.option("-p", "--profile", "profile", required=True, default=u"default",
              prompt="Enter the name of the AWS profile you would like to use",
              help="This AWS profile will be used to get your Access Key ID and Secret as well as your Region. "
                   "You will be prompted to confirm the Key and Region are correct before continuing. "
                   "This key will be used to set up any new Security Group Ingress required by Spell")
# TODO(ian): Take in cluster name instead of cluster ID once we have a list clusters endpoint
@click.option("--cluster-id", type=int, default=1, help="ID of cluster to update, defaults to 1")
def update(ctx, profile, cluster_id):
    """
    This command idempotently makes sure that any updates needed since you ran cluster init are available.

    NOTE: This command uses your AWS credentials, found in ~/.aws/credentials to create the necessary
    AWS resources for Spell to access the remote storage bucket. Your AWS credentials will
    need permission to setup these resources.
    """
    try:
        import boto3
        from botocore.exceptions import BotoCoreError, ClientError
    except ImportError:
        click.echo("Please pip install boto3 and rerun this command")
        return

    try:
        session = boto3.session.Session(profile_name=profile)
    except BotoCoreError as e:
        click.echo("Failed to set profile {} with error: {}".format(profile, e))
        return

    # Retrieve Spell cluster
    spell_client = ctx.obj["client"]
    with api_client_exception_handler():
        cluster = spell_client.get_cluster(cluster_id)

    click.echo("""This command will
    - Update your security group ingress rules""")
    if not click.confirm(
        "This will be done with your AWS profile '{}' which has "
        "Access Key ID '{}' and region '{}' - continue?".format(
            profile,
            session.get_credentials().access_key,
            session.region_name)):
        return

    # Set up clients with the provided profile
    try:
        ec2 = session.resource("ec2")
    except BotoCoreError as e:
        click.echo("Failed to get clients with profile {}: {}".format(profile, e))
        return

    id = cluster["networking"]["aws"]["security_group_id"]
    security_group = ec2.SecurityGroup(id)
    for port in INGRESS_PORTS:
        try:
            security_group.authorize_ingress(CidrIp="0.0.0.0/0", FromPort=port, ToPort=port, IpProtocol="tcp")
        except ClientError as e:
            if "InvalidPermission.Duplicate" not in e.message:
                click.echo(e.message)
                return
    try:
        security_group.authorize_ingress(IpPermissions=[{
            'IpProtocol': '-1',
            'FromPort': 0,
            'ToPort': 65355,
            'UserIdGroupPairs': [{'GroupId': security_group.id, 'VpcId': security_group.vpc_id}],
        }])
    except ClientError as e:
        if "InvalidPermission.Duplicate" not in e.message:
            click.echo(e.message)
            return

    click.echo("Successfully updated cluster {}".format(cluster["name"]))
