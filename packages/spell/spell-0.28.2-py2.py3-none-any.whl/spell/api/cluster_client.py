from spell.api import base_client
from spell.api.utils import url_path_join

CLUSTER_RESOURCE_URL = "clusters"


class ClusterClient(base_client.BaseClient):

    def get_cluster(self, cluster_id):
        """Get info for a cluster given a cluster_id.

        Keyword arguments:
        cluster_id -- the id of the cluster
        """
        r = self.request("get", url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_id))
        self.check_and_raise(r)
        return self.get_json(r)["cluster"]

    def create_aws_cluster(self, name, role_arn, external_id, read_policy, security_group_id, s3_bucket,
                           vpc_id, subnets, region):
        """Construct a cluster to map to a users aws cluster.

        Keyword arguments:
        name -- a display name for the cluster
        role_arn -- the aws arn of a role granting Spell necessary permissions to manage the cluster
        external_id -- needed to assume the role
        read_policy -- name of the s3 read policy associated with the IAM role
        security_group_id -- security group in the VPC with SSH and Docker port access to workers
        s3_bucket - a bucket to store run outputs in
        vpc_id - the id of vpc to setup this cluster in
        subnets - all subnets which Spell will attempt to launch machines in
            (due to aws capacity constraints more is preferable)
        region - the aws region of this vpc
        """
        payload = {
            "cluster_name": name,
            "role_arn": role_arn,
            "external_id": external_id,
            "read_policy": read_policy,
            "security_group_id": security_group_id,
            "s3_bucket": s3_bucket,
            "vpc_id": vpc_id,
            "subnets": subnets,
            "region": region,
        }
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner)
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)

    def set_kube_config(self, cluster_id, kube_config):
        """Submit a model-server kubeconfig to be stored as the
        active model-server cluster for the current org.

        Keyword arguments:
        cluster_id -- the id of the cluster to update
        ms_kube_config -- a string containing a yaml kubeconfig
        """
        payload = {"kube_config": kube_config}
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_id, "kube_config")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)

    def add_bucket(self, bucket_name, cluster_id, provider):
        """Add a bucket to SpellFS using the permissions of the specified cluster

        Keyword arguments:
        bucket_name -- the name of the bucket
        cluster_id -- the id of the cluster
        provider -- storage provider for bucket ("s3", "gs", etc.)
        """
        payload = {"bucket": bucket_name, "provider": provider}
        endpoint = url_path_join(CLUSTER_RESOURCE_URL, self.owner, cluster_id, "bucket")
        r = self.request("put", endpoint, payload=payload)
        self.check_and_raise(r)
