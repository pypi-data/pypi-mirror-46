import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-gamelift", "0.32.0", __name__, "aws-gamelift@0.32.0.jsii.tgz")
class CfnAlias(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-gamelift.CfnAlias"):
    """A CloudFormation ``AWS::GameLift::Alias``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html
    cloudformationResource:
        AWS::GameLift::Alias
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, routing_strategy: typing.Union["RoutingStrategyProperty", aws_cdk.cdk.Token], description: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GameLift::Alias``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::GameLift::Alias.Name``.
            routingStrategy: ``AWS::GameLift::Alias.RoutingStrategy``.
            description: ``AWS::GameLift::Alias.Description``.
        """
        props: CfnAliasProps = {"name": name, "routingStrategy": routing_strategy}

        if description is not None:
            props["description"] = description

        jsii.create(CfnAlias, self, [scope, id, props])

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
    @jsii.member(jsii_name="aliasId")
    def alias_id(self) -> str:
        return jsii.get(self, "aliasId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAliasProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RoutingStrategyProperty(jsii.compat.TypedDict, total=False):
        fleetId: str
        """``CfnAlias.RoutingStrategyProperty.FleetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-fleetid
        """
        message: str
        """``CfnAlias.RoutingStrategyProperty.Message``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-message
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnAlias.RoutingStrategyProperty", jsii_struct_bases=[_RoutingStrategyProperty])
    class RoutingStrategyProperty(_RoutingStrategyProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html
        """
        type: str
        """``CfnAlias.RoutingStrategyProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-alias-routingstrategy.html#cfn-gamelift-alias-routingstrategy-type
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnAliasProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::GameLift::Alias.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-description
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnAliasProps", jsii_struct_bases=[_CfnAliasProps])
class CfnAliasProps(_CfnAliasProps):
    """Properties for defining a ``AWS::GameLift::Alias``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html
    """
    name: str
    """``AWS::GameLift::Alias.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-name
    """

    routingStrategy: typing.Union["CfnAlias.RoutingStrategyProperty", aws_cdk.cdk.Token]
    """``AWS::GameLift::Alias.RoutingStrategy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-alias.html#cfn-gamelift-alias-routingstrategy
    """

class CfnBuild(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-gamelift.CfnBuild"):
    """A CloudFormation ``AWS::GameLift::Build``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html
    cloudformationResource:
        AWS::GameLift::Build
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: typing.Optional[str]=None, storage_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["S3LocationProperty"]]]=None, version: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GameLift::Build``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::GameLift::Build.Name``.
            storageLocation: ``AWS::GameLift::Build.StorageLocation``.
            version: ``AWS::GameLift::Build.Version``.
        """
        props: CfnBuildProps = {}

        if name is not None:
            props["name"] = name

        if storage_location is not None:
            props["storageLocation"] = storage_location

        if version is not None:
            props["version"] = version

        jsii.create(CfnBuild, self, [scope, id, props])

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
    @jsii.member(jsii_name="buildId")
    def build_id(self) -> str:
        return jsii.get(self, "buildId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBuildProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnBuild.S3LocationProperty", jsii_struct_bases=[])
    class S3LocationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html
        """
        bucket: str
        """``CfnBuild.S3LocationProperty.Bucket``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storage-bucket
        """

        key: str
        """``CfnBuild.S3LocationProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storage-key
        """

        roleArn: str
        """``CfnBuild.S3LocationProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-build-storagelocation.html#cfn-gamelift-build-storage-rolearn
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnBuildProps", jsii_struct_bases=[])
class CfnBuildProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::GameLift::Build``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html
    """
    name: str
    """``AWS::GameLift::Build.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-name
    """

    storageLocation: typing.Union[aws_cdk.cdk.Token, "CfnBuild.S3LocationProperty"]
    """``AWS::GameLift::Build.StorageLocation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-storagelocation
    """

    version: str
    """``AWS::GameLift::Build.Version``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-build.html#cfn-gamelift-build-version
    """

class CfnFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-gamelift.CfnFleet"):
    """A CloudFormation ``AWS::GameLift::Fleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html
    cloudformationResource:
        AWS::GameLift::Fleet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, build_id: str, desired_ec2_instances: typing.Union[jsii.Number, aws_cdk.cdk.Token], ec2_instance_type: str, name: str, server_launch_path: str, description: typing.Optional[str]=None, ec2_inbound_permissions: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "IpPermissionProperty"]]]]]=None, log_paths: typing.Optional[typing.List[str]]=None, max_size: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, min_size: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, server_launch_parameters: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::GameLift::Fleet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            buildId: ``AWS::GameLift::Fleet.BuildId``.
            desiredEc2Instances: ``AWS::GameLift::Fleet.DesiredEC2Instances``.
            ec2InstanceType: ``AWS::GameLift::Fleet.EC2InstanceType``.
            name: ``AWS::GameLift::Fleet.Name``.
            serverLaunchPath: ``AWS::GameLift::Fleet.ServerLaunchPath``.
            description: ``AWS::GameLift::Fleet.Description``.
            ec2InboundPermissions: ``AWS::GameLift::Fleet.EC2InboundPermissions``.
            logPaths: ``AWS::GameLift::Fleet.LogPaths``.
            maxSize: ``AWS::GameLift::Fleet.MaxSize``.
            minSize: ``AWS::GameLift::Fleet.MinSize``.
            serverLaunchParameters: ``AWS::GameLift::Fleet.ServerLaunchParameters``.
        """
        props: CfnFleetProps = {"buildId": build_id, "desiredEc2Instances": desired_ec2_instances, "ec2InstanceType": ec2_instance_type, "name": name, "serverLaunchPath": server_launch_path}

        if description is not None:
            props["description"] = description

        if ec2_inbound_permissions is not None:
            props["ec2InboundPermissions"] = ec2_inbound_permissions

        if log_paths is not None:
            props["logPaths"] = log_paths

        if max_size is not None:
            props["maxSize"] = max_size

        if min_size is not None:
            props["minSize"] = min_size

        if server_launch_parameters is not None:
            props["serverLaunchParameters"] = server_launch_parameters

        jsii.create(CfnFleet, self, [scope, id, props])

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
    @jsii.member(jsii_name="fleetId")
    def fleet_id(self) -> str:
        return jsii.get(self, "fleetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFleetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnFleet.IpPermissionProperty", jsii_struct_bases=[])
    class IpPermissionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html
        """
        fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnFleet.IpPermissionProperty.FromPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-fromport
        """

        ipRange: str
        """``CfnFleet.IpPermissionProperty.IpRange``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-iprange
        """

        protocol: str
        """``CfnFleet.IpPermissionProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-protocol
        """

        toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnFleet.IpPermissionProperty.ToPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-gamelift-fleet-ec2inboundpermission.html#cfn-gamelift-fleet-ec2inboundpermissions-toport
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnFleetProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::GameLift::Fleet.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-description
    """
    ec2InboundPermissions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFleet.IpPermissionProperty"]]]
    """``AWS::GameLift::Fleet.EC2InboundPermissions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2inboundpermissions
    """
    logPaths: typing.List[str]
    """``AWS::GameLift::Fleet.LogPaths``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-logpaths
    """
    maxSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::GameLift::Fleet.MaxSize``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-maxsize
    """
    minSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::GameLift::Fleet.MinSize``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-minsize
    """
    serverLaunchParameters: str
    """``AWS::GameLift::Fleet.ServerLaunchParameters``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchparameters
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-gamelift.CfnFleetProps", jsii_struct_bases=[_CfnFleetProps])
class CfnFleetProps(_CfnFleetProps):
    """Properties for defining a ``AWS::GameLift::Fleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html
    """
    buildId: str
    """``AWS::GameLift::Fleet.BuildId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-buildid
    """

    desiredEc2Instances: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::GameLift::Fleet.DesiredEC2Instances``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-desiredec2instances
    """

    ec2InstanceType: str
    """``AWS::GameLift::Fleet.EC2InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-ec2instancetype
    """

    name: str
    """``AWS::GameLift::Fleet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-name
    """

    serverLaunchPath: str
    """``AWS::GameLift::Fleet.ServerLaunchPath``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-gamelift-fleet.html#cfn-gamelift-fleet-serverlaunchpath
    """

__all__ = ["CfnAlias", "CfnAliasProps", "CfnBuild", "CfnBuildProps", "CfnFleet", "CfnFleetProps", "__jsii_assembly__"]

publication.publish()
