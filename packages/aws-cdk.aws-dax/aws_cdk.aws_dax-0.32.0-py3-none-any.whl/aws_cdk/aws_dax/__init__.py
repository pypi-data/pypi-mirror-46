import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-dax", "0.32.0", __name__, "aws-dax@0.32.0.jsii.tgz")
class CfnCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dax.CfnCluster"):
    """A CloudFormation ``AWS::DAX::Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
    cloudformationResource:
        AWS::DAX::Cluster
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, iam_role_arn: str, node_type: str, replication_factor: typing.Union[jsii.Number, aws_cdk.cdk.Token], availability_zones: typing.Optional[typing.List[str]]=None, cluster_name: typing.Optional[str]=None, description: typing.Optional[str]=None, notification_topic_arn: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, sse_specification: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SSESpecificationProperty"]]]=None, subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.Mapping[typing.Any, typing.Any]]=None) -> None:
        """Create a new ``AWS::DAX::Cluster``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            iamRoleArn: ``AWS::DAX::Cluster.IAMRoleARN``.
            nodeType: ``AWS::DAX::Cluster.NodeType``.
            replicationFactor: ``AWS::DAX::Cluster.ReplicationFactor``.
            availabilityZones: ``AWS::DAX::Cluster.AvailabilityZones``.
            clusterName: ``AWS::DAX::Cluster.ClusterName``.
            description: ``AWS::DAX::Cluster.Description``.
            notificationTopicArn: ``AWS::DAX::Cluster.NotificationTopicARN``.
            parameterGroupName: ``AWS::DAX::Cluster.ParameterGroupName``.
            preferredMaintenanceWindow: ``AWS::DAX::Cluster.PreferredMaintenanceWindow``.
            securityGroupIds: ``AWS::DAX::Cluster.SecurityGroupIds``.
            sseSpecification: ``AWS::DAX::Cluster.SSESpecification``.
            subnetGroupName: ``AWS::DAX::Cluster.SubnetGroupName``.
            tags: ``AWS::DAX::Cluster.Tags``.
        """
        props: CfnClusterProps = {"iamRoleArn": iam_role_arn, "nodeType": node_type, "replicationFactor": replication_factor}

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if cluster_name is not None:
            props["clusterName"] = cluster_name

        if description is not None:
            props["description"] = description

        if notification_topic_arn is not None:
            props["notificationTopicArn"] = notification_topic_arn

        if parameter_group_name is not None:
            props["parameterGroupName"] = parameter_group_name

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if sse_specification is not None:
            props["sseSpecification"] = sse_specification

        if subnet_group_name is not None:
            props["subnetGroupName"] = subnet_group_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="clusterArn")
    def cluster_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "clusterArn")

    @property
    @jsii.member(jsii_name="clusterDiscoveryEndpoint")
    def cluster_discovery_endpoint(self) -> str:
        """
        cloudformationAttribute:
            ClusterDiscoveryEndpoint
        """
        return jsii.get(self, "clusterDiscoveryEndpoint")

    @property
    @jsii.member(jsii_name="clusterName")
    def cluster_name(self) -> str:
        return jsii.get(self, "clusterName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnClusterProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnCluster.SSESpecificationProperty", jsii_struct_bases=[])
    class SSESpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html
        """
        sseEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnCluster.SSESpecificationProperty.SSEEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-dax-cluster-ssespecification.html#cfn-dax-cluster-ssespecification-sseenabled
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnClusterProps(jsii.compat.TypedDict, total=False):
    availabilityZones: typing.List[str]
    """``AWS::DAX::Cluster.AvailabilityZones``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-availabilityzones
    """
    clusterName: str
    """``AWS::DAX::Cluster.ClusterName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-clustername
    """
    description: str
    """``AWS::DAX::Cluster.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-description
    """
    notificationTopicArn: str
    """``AWS::DAX::Cluster.NotificationTopicARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-notificationtopicarn
    """
    parameterGroupName: str
    """``AWS::DAX::Cluster.ParameterGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-parametergroupname
    """
    preferredMaintenanceWindow: str
    """``AWS::DAX::Cluster.PreferredMaintenanceWindow``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-preferredmaintenancewindow
    """
    securityGroupIds: typing.List[str]
    """``AWS::DAX::Cluster.SecurityGroupIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-securitygroupids
    """
    sseSpecification: typing.Union[aws_cdk.cdk.Token, "CfnCluster.SSESpecificationProperty"]
    """``AWS::DAX::Cluster.SSESpecification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-ssespecification
    """
    subnetGroupName: str
    """``AWS::DAX::Cluster.SubnetGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-subnetgroupname
    """
    tags: typing.Mapping[typing.Any, typing.Any]
    """``AWS::DAX::Cluster.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnClusterProps", jsii_struct_bases=[_CfnClusterProps])
class CfnClusterProps(_CfnClusterProps):
    """Properties for defining a ``AWS::DAX::Cluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html
    """
    iamRoleArn: str
    """``AWS::DAX::Cluster.IAMRoleARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-iamrolearn
    """

    nodeType: str
    """``AWS::DAX::Cluster.NodeType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-nodetype
    """

    replicationFactor: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::DAX::Cluster.ReplicationFactor``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-cluster.html#cfn-dax-cluster-replicationfactor
    """

class CfnParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dax.CfnParameterGroup"):
    """A CloudFormation ``AWS::DAX::ParameterGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
    cloudformationResource:
        AWS::DAX::ParameterGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, parameter_group_name: typing.Optional[str]=None, parameter_name_values: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::DAX::ParameterGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            description: ``AWS::DAX::ParameterGroup.Description``.
            parameterGroupName: ``AWS::DAX::ParameterGroup.ParameterGroupName``.
            parameterNameValues: ``AWS::DAX::ParameterGroup.ParameterNameValues``.
        """
        props: CfnParameterGroupProps = {}

        if description is not None:
            props["description"] = description

        if parameter_group_name is not None:
            props["parameterGroupName"] = parameter_group_name

        if parameter_name_values is not None:
            props["parameterNameValues"] = parameter_name_values

        jsii.create(CfnParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="parameterGroupArn")
    def parameter_group_arn(self) -> str:
        return jsii.get(self, "parameterGroupArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnParameterGroupProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnParameterGroupProps", jsii_struct_bases=[])
class CfnParameterGroupProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::DAX::ParameterGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html
    """
    description: str
    """``AWS::DAX::ParameterGroup.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-description
    """

    parameterGroupName: str
    """``AWS::DAX::ParameterGroup.ParameterGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parametergroupname
    """

    parameterNameValues: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::DAX::ParameterGroup.ParameterNameValues``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-parametergroup.html#cfn-dax-parametergroup-parameternamevalues
    """

class CfnSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-dax.CfnSubnetGroup"):
    """A CloudFormation ``AWS::DAX::SubnetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
    cloudformationResource:
        AWS::DAX::SubnetGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subnet_ids: typing.List[str], description: typing.Optional[str]=None, subnet_group_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::DAX::SubnetGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            subnetIds: ``AWS::DAX::SubnetGroup.SubnetIds``.
            description: ``AWS::DAX::SubnetGroup.Description``.
            subnetGroupName: ``AWS::DAX::SubnetGroup.SubnetGroupName``.
        """
        props: CfnSubnetGroupProps = {"subnetIds": subnet_ids}

        if description is not None:
            props["description"] = description

        if subnet_group_name is not None:
            props["subnetGroupName"] = subnet_group_name

        jsii.create(CfnSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetGroupArn")
    def subnet_group_arn(self) -> str:
        return jsii.get(self, "subnetGroupArn")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSubnetGroupProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::DAX::SubnetGroup.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-description
    """
    subnetGroupName: str
    """``AWS::DAX::SubnetGroup.SubnetGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetgroupname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-dax.CfnSubnetGroupProps", jsii_struct_bases=[_CfnSubnetGroupProps])
class CfnSubnetGroupProps(_CfnSubnetGroupProps):
    """Properties for defining a ``AWS::DAX::SubnetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html
    """
    subnetIds: typing.List[str]
    """``AWS::DAX::SubnetGroup.SubnetIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-dax-subnetgroup.html#cfn-dax-subnetgroup-subnetids
    """

__all__ = ["CfnCluster", "CfnClusterProps", "CfnParameterGroup", "CfnParameterGroupProps", "CfnSubnetGroup", "CfnSubnetGroupProps", "__jsii_assembly__"]

publication.publish()
