import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-elasticsearch", "0.32.0", __name__, "aws-elasticsearch@0.32.0.jsii.tgz")
class CfnDomain(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain"):
    """A CloudFormation ``AWS::Elasticsearch::Domain``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
    cloudformationResource:
        AWS::Elasticsearch::Domain
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, access_policies: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, advanced_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.Mapping[str,str]]]]=None, domain_name: typing.Optional[str]=None, ebs_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["EBSOptionsProperty"]]]=None, elasticsearch_cluster_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ElasticsearchClusterConfigProperty"]]]=None, elasticsearch_version: typing.Optional[str]=None, encryption_at_rest_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["EncryptionAtRestOptionsProperty"]]]=None, node_to_node_encryption_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["NodeToNodeEncryptionOptionsProperty"]]]=None, snapshot_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SnapshotOptionsProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["VPCOptionsProperty"]]]=None) -> None:
        """Create a new ``AWS::Elasticsearch::Domain``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            accessPolicies: ``AWS::Elasticsearch::Domain.AccessPolicies``.
            advancedOptions: ``AWS::Elasticsearch::Domain.AdvancedOptions``.
            domainName: ``AWS::Elasticsearch::Domain.DomainName``.
            ebsOptions: ``AWS::Elasticsearch::Domain.EBSOptions``.
            elasticsearchClusterConfig: ``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.
            elasticsearchVersion: ``AWS::Elasticsearch::Domain.ElasticsearchVersion``.
            encryptionAtRestOptions: ``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.
            nodeToNodeEncryptionOptions: ``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.
            snapshotOptions: ``AWS::Elasticsearch::Domain.SnapshotOptions``.
            tags: ``AWS::Elasticsearch::Domain.Tags``.
            vpcOptions: ``AWS::Elasticsearch::Domain.VPCOptions``.
        """
        props: CfnDomainProps = {}

        if access_policies is not None:
            props["accessPolicies"] = access_policies

        if advanced_options is not None:
            props["advancedOptions"] = advanced_options

        if domain_name is not None:
            props["domainName"] = domain_name

        if ebs_options is not None:
            props["ebsOptions"] = ebs_options

        if elasticsearch_cluster_config is not None:
            props["elasticsearchClusterConfig"] = elasticsearch_cluster_config

        if elasticsearch_version is not None:
            props["elasticsearchVersion"] = elasticsearch_version

        if encryption_at_rest_options is not None:
            props["encryptionAtRestOptions"] = encryption_at_rest_options

        if node_to_node_encryption_options is not None:
            props["nodeToNodeEncryptionOptions"] = node_to_node_encryption_options

        if snapshot_options is not None:
            props["snapshotOptions"] = snapshot_options

        if tags is not None:
            props["tags"] = tags

        if vpc_options is not None:
            props["vpcOptions"] = vpc_options

        jsii.create(CfnDomain, self, [scope, id, props])

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(self, properties: typing.Any) -> typing.Mapping[str,typing.Any]:
        """
        Arguments:
            properties: -
        """
        return jsii.invoke(self, "renderProperties", [properties])

    @classproperty
    @jsii.member(jsii_name="resourceTypeName")
    def RESOURCE_TYPE_NAME(cls) -> str:
        """The CloudFormation resource type name for this resource class."""
        return jsii.sget(cls, "resourceTypeName")

    @property
    @jsii.member(jsii_name="domainArn")
    def domain_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "domainArn")

    @property
    @jsii.member(jsii_name="domainEndpoint")
    def domain_endpoint(self) -> str:
        """
        cloudformationAttribute:
            DomainEndpoint
        """
        return jsii.get(self, "domainEndpoint")

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        return jsii.get(self, "domainName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDomainProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.EBSOptionsProperty", jsii_struct_bases=[])
    class EBSOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html
        """
        ebsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDomain.EBSOptionsProperty.EBSEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-ebsenabled
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDomain.EBSOptionsProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-iops
        """

        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDomain.EBSOptionsProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumesize
        """

        volumeType: str
        """``CfnDomain.EBSOptionsProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-ebsoptions.html#cfn-elasticsearch-domain-ebsoptions-volumetype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.ElasticsearchClusterConfigProperty", jsii_struct_bases=[])
    class ElasticsearchClusterConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html
        """
        dedicatedMasterCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastercount
        """

        dedicatedMasterEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmasterenabled
        """

        dedicatedMasterType: str
        """``CfnDomain.ElasticsearchClusterConfigProperty.DedicatedMasterType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-dedicatedmastertype
        """

        instanceCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDomain.ElasticsearchClusterConfigProperty.InstanceCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instancecount
        """

        instanceType: str
        """``CfnDomain.ElasticsearchClusterConfigProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-instnacetype
        """

        zoneAwarenessEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDomain.ElasticsearchClusterConfigProperty.ZoneAwarenessEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-elasticsearchclusterconfig.html#cfn-elasticsearch-domain-elasticseachclusterconfig-zoneawarenessenabled
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.EncryptionAtRestOptionsProperty", jsii_struct_bases=[])
    class EncryptionAtRestOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDomain.EncryptionAtRestOptionsProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-enabled
        """

        kmsKeyId: str
        """``CfnDomain.EncryptionAtRestOptionsProperty.KmsKeyId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-encryptionatrestoptions.html#cfn-elasticsearch-domain-encryptionatrestoptions-kmskeyid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.NodeToNodeEncryptionOptionsProperty", jsii_struct_bases=[])
    class NodeToNodeEncryptionOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDomain.NodeToNodeEncryptionOptionsProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-nodetonodeencryptionoptions.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions-enabled
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.SnapshotOptionsProperty", jsii_struct_bases=[])
    class SnapshotOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html
        """
        automatedSnapshotStartHour: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDomain.SnapshotOptionsProperty.AutomatedSnapshotStartHour``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-snapshotoptions.html#cfn-elasticsearch-domain-snapshotoptions-automatedsnapshotstarthour
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomain.VPCOptionsProperty", jsii_struct_bases=[])
    class VPCOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html
        """
        securityGroupIds: typing.List[str]
        """``CfnDomain.VPCOptionsProperty.SecurityGroupIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-securitygroupids
        """

        subnetIds: typing.List[str]
        """``CfnDomain.VPCOptionsProperty.SubnetIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-elasticsearch-domain-vpcoptions.html#cfn-elasticsearch-domain-vpcoptions-subnetids
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-elasticsearch.CfnDomainProps", jsii_struct_bases=[])
class CfnDomainProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::Elasticsearch::Domain``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html
    """
    accessPolicies: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::Elasticsearch::Domain.AccessPolicies``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-accesspolicies
    """

    advancedOptions: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    """``AWS::Elasticsearch::Domain.AdvancedOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-advancedoptions
    """

    domainName: str
    """``AWS::Elasticsearch::Domain.DomainName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-domainname
    """

    ebsOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.EBSOptionsProperty"]
    """``AWS::Elasticsearch::Domain.EBSOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-ebsoptions
    """

    elasticsearchClusterConfig: typing.Union[aws_cdk.cdk.Token, "CfnDomain.ElasticsearchClusterConfigProperty"]
    """``AWS::Elasticsearch::Domain.ElasticsearchClusterConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchclusterconfig
    """

    elasticsearchVersion: str
    """``AWS::Elasticsearch::Domain.ElasticsearchVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-elasticsearchversion
    """

    encryptionAtRestOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.EncryptionAtRestOptionsProperty"]
    """``AWS::Elasticsearch::Domain.EncryptionAtRestOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-encryptionatrestoptions
    """

    nodeToNodeEncryptionOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.NodeToNodeEncryptionOptionsProperty"]
    """``AWS::Elasticsearch::Domain.NodeToNodeEncryptionOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-nodetonodeencryptionoptions
    """

    snapshotOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.SnapshotOptionsProperty"]
    """``AWS::Elasticsearch::Domain.SnapshotOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-snapshotoptions
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::Elasticsearch::Domain.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-tags
    """

    vpcOptions: typing.Union[aws_cdk.cdk.Token, "CfnDomain.VPCOptionsProperty"]
    """``AWS::Elasticsearch::Domain.VPCOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-elasticsearch-domain.html#cfn-elasticsearch-domain-vpcoptions
    """

__all__ = ["CfnDomain", "CfnDomainProps", "__jsii_assembly__"]

publication.publish()
