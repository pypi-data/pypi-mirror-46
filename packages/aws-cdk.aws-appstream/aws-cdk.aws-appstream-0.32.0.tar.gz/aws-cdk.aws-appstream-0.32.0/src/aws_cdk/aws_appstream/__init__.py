import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-appstream", "0.32.0", __name__, "aws-appstream@0.32.0.jsii.tgz")
class CfnDirectoryConfig(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig"):
    """A CloudFormation ``AWS::AppStream::DirectoryConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
    cloudformationResource:
        AWS::AppStream::DirectoryConfig
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, directory_name: str, organizational_unit_distinguished_names: typing.List[str], service_account_credentials: typing.Union["ServiceAccountCredentialsProperty", aws_cdk.cdk.Token]) -> None:
        """Create a new ``AWS::AppStream::DirectoryConfig``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            directoryName: ``AWS::AppStream::DirectoryConfig.DirectoryName``.
            organizationalUnitDistinguishedNames: ``AWS::AppStream::DirectoryConfig.OrganizationalUnitDistinguishedNames``.
            serviceAccountCredentials: ``AWS::AppStream::DirectoryConfig.ServiceAccountCredentials``.
        """
        props: CfnDirectoryConfigProps = {"directoryName": directory_name, "organizationalUnitDistinguishedNames": organizational_unit_distinguished_names, "serviceAccountCredentials": service_account_credentials}

        jsii.create(CfnDirectoryConfig, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnDirectoryConfigProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfig.ServiceAccountCredentialsProperty", jsii_struct_bases=[])
    class ServiceAccountCredentialsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html
        """
        accountName: str
        """``CfnDirectoryConfig.ServiceAccountCredentialsProperty.AccountName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountname
        """

        accountPassword: str
        """``CfnDirectoryConfig.ServiceAccountCredentialsProperty.AccountPassword``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-directoryconfig-serviceaccountcredentials.html#cfn-appstream-directoryconfig-serviceaccountcredentials-accountpassword
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnDirectoryConfigProps", jsii_struct_bases=[])
class CfnDirectoryConfigProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::AppStream::DirectoryConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html
    """
    directoryName: str
    """``AWS::AppStream::DirectoryConfig.DirectoryName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-directoryname
    """

    organizationalUnitDistinguishedNames: typing.List[str]
    """``AWS::AppStream::DirectoryConfig.OrganizationalUnitDistinguishedNames``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-organizationalunitdistinguishednames
    """

    serviceAccountCredentials: typing.Union["CfnDirectoryConfig.ServiceAccountCredentialsProperty", aws_cdk.cdk.Token]
    """``AWS::AppStream::DirectoryConfig.ServiceAccountCredentials``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-directoryconfig.html#cfn-appstream-directoryconfig-serviceaccountcredentials
    """

class CfnFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnFleet"):
    """A CloudFormation ``AWS::AppStream::Fleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
    cloudformationResource:
        AWS::AppStream::Fleet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, compute_capacity: typing.Union[aws_cdk.cdk.Token, "ComputeCapacityProperty"], instance_type: str, description: typing.Optional[str]=None, disconnect_timeout_in_seconds: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, display_name: typing.Optional[str]=None, domain_join_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["DomainJoinInfoProperty"]]]=None, enable_default_internet_access: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, fleet_type: typing.Optional[str]=None, image_arn: typing.Optional[str]=None, image_name: typing.Optional[str]=None, max_user_duration_in_seconds: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["VpcConfigProperty"]]]=None) -> None:
        """Create a new ``AWS::AppStream::Fleet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            computeCapacity: ``AWS::AppStream::Fleet.ComputeCapacity``.
            instanceType: ``AWS::AppStream::Fleet.InstanceType``.
            description: ``AWS::AppStream::Fleet.Description``.
            disconnectTimeoutInSeconds: ``AWS::AppStream::Fleet.DisconnectTimeoutInSeconds``.
            displayName: ``AWS::AppStream::Fleet.DisplayName``.
            domainJoinInfo: ``AWS::AppStream::Fleet.DomainJoinInfo``.
            enableDefaultInternetAccess: ``AWS::AppStream::Fleet.EnableDefaultInternetAccess``.
            fleetType: ``AWS::AppStream::Fleet.FleetType``.
            imageArn: ``AWS::AppStream::Fleet.ImageArn``.
            imageName: ``AWS::AppStream::Fleet.ImageName``.
            maxUserDurationInSeconds: ``AWS::AppStream::Fleet.MaxUserDurationInSeconds``.
            name: ``AWS::AppStream::Fleet.Name``.
            tags: ``AWS::AppStream::Fleet.Tags``.
            vpcConfig: ``AWS::AppStream::Fleet.VpcConfig``.
        """
        props: CfnFleetProps = {"computeCapacity": compute_capacity, "instanceType": instance_type}

        if description is not None:
            props["description"] = description

        if disconnect_timeout_in_seconds is not None:
            props["disconnectTimeoutInSeconds"] = disconnect_timeout_in_seconds

        if display_name is not None:
            props["displayName"] = display_name

        if domain_join_info is not None:
            props["domainJoinInfo"] = domain_join_info

        if enable_default_internet_access is not None:
            props["enableDefaultInternetAccess"] = enable_default_internet_access

        if fleet_type is not None:
            props["fleetType"] = fleet_type

        if image_arn is not None:
            props["imageArn"] = image_arn

        if image_name is not None:
            props["imageName"] = image_name

        if max_user_duration_in_seconds is not None:
            props["maxUserDurationInSeconds"] = max_user_duration_in_seconds

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

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
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFleetProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleet.ComputeCapacityProperty", jsii_struct_bases=[])
    class ComputeCapacityProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html
        """
        desiredInstances: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnFleet.ComputeCapacityProperty.DesiredInstances``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-computecapacity.html#cfn-appstream-fleet-computecapacity-desiredinstances
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleet.DomainJoinInfoProperty", jsii_struct_bases=[])
    class DomainJoinInfoProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html
        """
        directoryName: str
        """``CfnFleet.DomainJoinInfoProperty.DirectoryName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-directoryname
        """

        organizationalUnitDistinguishedName: str
        """``CfnFleet.DomainJoinInfoProperty.OrganizationalUnitDistinguishedName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-domainjoininfo.html#cfn-appstream-fleet-domainjoininfo-organizationalunitdistinguishedname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleet.VpcConfigProperty", jsii_struct_bases=[])
    class VpcConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html
        """
        securityGroupIds: typing.List[str]
        """``CfnFleet.VpcConfigProperty.SecurityGroupIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-securitygroupids
        """

        subnetIds: typing.List[str]
        """``CfnFleet.VpcConfigProperty.SubnetIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-fleet-vpcconfig.html#cfn-appstream-fleet-vpcconfig-subnetids
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnFleetProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::AppStream::Fleet.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-description
    """
    disconnectTimeoutInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AppStream::Fleet.DisconnectTimeoutInSeconds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-disconnecttimeoutinseconds
    """
    displayName: str
    """``AWS::AppStream::Fleet.DisplayName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-displayname
    """
    domainJoinInfo: typing.Union[aws_cdk.cdk.Token, "CfnFleet.DomainJoinInfoProperty"]
    """``AWS::AppStream::Fleet.DomainJoinInfo``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-domainjoininfo
    """
    enableDefaultInternetAccess: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AppStream::Fleet.EnableDefaultInternetAccess``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-enabledefaultinternetaccess
    """
    fleetType: str
    """``AWS::AppStream::Fleet.FleetType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-fleettype
    """
    imageArn: str
    """``AWS::AppStream::Fleet.ImageArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagearn
    """
    imageName: str
    """``AWS::AppStream::Fleet.ImageName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-imagename
    """
    maxUserDurationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AppStream::Fleet.MaxUserDurationInSeconds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-maxuserdurationinseconds
    """
    name: str
    """``AWS::AppStream::Fleet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-name
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::AppStream::Fleet.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-tags
    """
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnFleet.VpcConfigProperty"]
    """``AWS::AppStream::Fleet.VpcConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-vpcconfig
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnFleetProps", jsii_struct_bases=[_CfnFleetProps])
class CfnFleetProps(_CfnFleetProps):
    """Properties for defining a ``AWS::AppStream::Fleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html
    """
    computeCapacity: typing.Union[aws_cdk.cdk.Token, "CfnFleet.ComputeCapacityProperty"]
    """``AWS::AppStream::Fleet.ComputeCapacity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-computecapacity
    """

    instanceType: str
    """``AWS::AppStream::Fleet.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-fleet.html#cfn-appstream-fleet-instancetype
    """

class CfnImageBuilder(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder"):
    """A CloudFormation ``AWS::AppStream::ImageBuilder``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
    cloudformationResource:
        AWS::AppStream::ImageBuilder
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: str, appstream_agent_version: typing.Optional[str]=None, description: typing.Optional[str]=None, display_name: typing.Optional[str]=None, domain_join_info: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["DomainJoinInfoProperty"]]]=None, enable_default_internet_access: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, image_arn: typing.Optional[str]=None, image_name: typing.Optional[str]=None, name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["VpcConfigProperty"]]]=None) -> None:
        """Create a new ``AWS::AppStream::ImageBuilder``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            instanceType: ``AWS::AppStream::ImageBuilder.InstanceType``.
            appstreamAgentVersion: ``AWS::AppStream::ImageBuilder.AppstreamAgentVersion``.
            description: ``AWS::AppStream::ImageBuilder.Description``.
            displayName: ``AWS::AppStream::ImageBuilder.DisplayName``.
            domainJoinInfo: ``AWS::AppStream::ImageBuilder.DomainJoinInfo``.
            enableDefaultInternetAccess: ``AWS::AppStream::ImageBuilder.EnableDefaultInternetAccess``.
            imageArn: ``AWS::AppStream::ImageBuilder.ImageArn``.
            imageName: ``AWS::AppStream::ImageBuilder.ImageName``.
            name: ``AWS::AppStream::ImageBuilder.Name``.
            tags: ``AWS::AppStream::ImageBuilder.Tags``.
            vpcConfig: ``AWS::AppStream::ImageBuilder.VpcConfig``.
        """
        props: CfnImageBuilderProps = {"instanceType": instance_type}

        if appstream_agent_version is not None:
            props["appstreamAgentVersion"] = appstream_agent_version

        if description is not None:
            props["description"] = description

        if display_name is not None:
            props["displayName"] = display_name

        if domain_join_info is not None:
            props["domainJoinInfo"] = domain_join_info

        if enable_default_internet_access is not None:
            props["enableDefaultInternetAccess"] = enable_default_internet_access

        if image_arn is not None:
            props["imageArn"] = image_arn

        if image_name is not None:
            props["imageName"] = image_name

        if name is not None:
            props["name"] = name

        if tags is not None:
            props["tags"] = tags

        if vpc_config is not None:
            props["vpcConfig"] = vpc_config

        jsii.create(CfnImageBuilder, self, [scope, id, props])

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
    @jsii.member(jsii_name="imageBuilderStreamingUrl")
    def image_builder_streaming_url(self) -> str:
        """
        cloudformationAttribute:
            StreamingUrl
        """
        return jsii.get(self, "imageBuilderStreamingUrl")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnImageBuilderProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.DomainJoinInfoProperty", jsii_struct_bases=[])
    class DomainJoinInfoProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html
        """
        directoryName: str
        """``CfnImageBuilder.DomainJoinInfoProperty.DirectoryName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-directoryname
        """

        organizationalUnitDistinguishedName: str
        """``CfnImageBuilder.DomainJoinInfoProperty.OrganizationalUnitDistinguishedName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-domainjoininfo.html#cfn-appstream-imagebuilder-domainjoininfo-organizationalunitdistinguishedname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnImageBuilder.VpcConfigProperty", jsii_struct_bases=[])
    class VpcConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html
        """
        securityGroupIds: typing.List[str]
        """``CfnImageBuilder.VpcConfigProperty.SecurityGroupIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-securitygroupids
        """

        subnetIds: typing.List[str]
        """``CfnImageBuilder.VpcConfigProperty.SubnetIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-imagebuilder-vpcconfig.html#cfn-appstream-imagebuilder-vpcconfig-subnetids
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnImageBuilderProps(jsii.compat.TypedDict, total=False):
    appstreamAgentVersion: str
    """``AWS::AppStream::ImageBuilder.AppstreamAgentVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-appstreamagentversion
    """
    description: str
    """``AWS::AppStream::ImageBuilder.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-description
    """
    displayName: str
    """``AWS::AppStream::ImageBuilder.DisplayName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-displayname
    """
    domainJoinInfo: typing.Union[aws_cdk.cdk.Token, "CfnImageBuilder.DomainJoinInfoProperty"]
    """``AWS::AppStream::ImageBuilder.DomainJoinInfo``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-domainjoininfo
    """
    enableDefaultInternetAccess: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AppStream::ImageBuilder.EnableDefaultInternetAccess``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-enabledefaultinternetaccess
    """
    imageArn: str
    """``AWS::AppStream::ImageBuilder.ImageArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagearn
    """
    imageName: str
    """``AWS::AppStream::ImageBuilder.ImageName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-imagename
    """
    name: str
    """``AWS::AppStream::ImageBuilder.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-name
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::AppStream::ImageBuilder.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-tags
    """
    vpcConfig: typing.Union[aws_cdk.cdk.Token, "CfnImageBuilder.VpcConfigProperty"]
    """``AWS::AppStream::ImageBuilder.VpcConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-vpcconfig
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnImageBuilderProps", jsii_struct_bases=[_CfnImageBuilderProps])
class CfnImageBuilderProps(_CfnImageBuilderProps):
    """Properties for defining a ``AWS::AppStream::ImageBuilder``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html
    """
    instanceType: str
    """``AWS::AppStream::ImageBuilder.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-imagebuilder.html#cfn-appstream-imagebuilder-instancetype
    """

class CfnStack(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnStack"):
    """A CloudFormation ``AWS::AppStream::Stack``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
    cloudformationResource:
        AWS::AppStream::Stack
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ApplicationSettingsProperty"]]]=None, attributes_to_delete: typing.Optional[typing.List[str]]=None, delete_storage_connectors: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, description: typing.Optional[str]=None, display_name: typing.Optional[str]=None, feedback_url: typing.Optional[str]=None, name: typing.Optional[str]=None, redirect_url: typing.Optional[str]=None, storage_connectors: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "StorageConnectorProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, user_settings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "UserSettingProperty"]]]]]=None) -> None:
        """Create a new ``AWS::AppStream::Stack``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationSettings: ``AWS::AppStream::Stack.ApplicationSettings``.
            attributesToDelete: ``AWS::AppStream::Stack.AttributesToDelete``.
            deleteStorageConnectors: ``AWS::AppStream::Stack.DeleteStorageConnectors``.
            description: ``AWS::AppStream::Stack.Description``.
            displayName: ``AWS::AppStream::Stack.DisplayName``.
            feedbackUrl: ``AWS::AppStream::Stack.FeedbackURL``.
            name: ``AWS::AppStream::Stack.Name``.
            redirectUrl: ``AWS::AppStream::Stack.RedirectURL``.
            storageConnectors: ``AWS::AppStream::Stack.StorageConnectors``.
            tags: ``AWS::AppStream::Stack.Tags``.
            userSettings: ``AWS::AppStream::Stack.UserSettings``.
        """
        props: CfnStackProps = {}

        if application_settings is not None:
            props["applicationSettings"] = application_settings

        if attributes_to_delete is not None:
            props["attributesToDelete"] = attributes_to_delete

        if delete_storage_connectors is not None:
            props["deleteStorageConnectors"] = delete_storage_connectors

        if description is not None:
            props["description"] = description

        if display_name is not None:
            props["displayName"] = display_name

        if feedback_url is not None:
            props["feedbackUrl"] = feedback_url

        if name is not None:
            props["name"] = name

        if redirect_url is not None:
            props["redirectUrl"] = redirect_url

        if storage_connectors is not None:
            props["storageConnectors"] = storage_connectors

        if tags is not None:
            props["tags"] = tags

        if user_settings is not None:
            props["userSettings"] = user_settings

        jsii.create(CfnStack, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnStackProps":
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

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ApplicationSettingsProperty(jsii.compat.TypedDict, total=False):
        settingsGroup: str
        """``CfnStack.ApplicationSettingsProperty.SettingsGroup``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-settingsgroup
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStack.ApplicationSettingsProperty", jsii_struct_bases=[_ApplicationSettingsProperty])
    class ApplicationSettingsProperty(_ApplicationSettingsProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnStack.ApplicationSettingsProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-applicationsettings.html#cfn-appstream-stack-applicationsettings-enabled
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StorageConnectorProperty(jsii.compat.TypedDict, total=False):
        domains: typing.List[str]
        """``CfnStack.StorageConnectorProperty.Domains``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-domains
        """
        resourceIdentifier: str
        """``CfnStack.StorageConnectorProperty.ResourceIdentifier``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-resourceidentifier
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStack.StorageConnectorProperty", jsii_struct_bases=[_StorageConnectorProperty])
    class StorageConnectorProperty(_StorageConnectorProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html
        """
        connectorType: str
        """``CfnStack.StorageConnectorProperty.ConnectorType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-storageconnector.html#cfn-appstream-stack-storageconnector-connectortype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStack.UserSettingProperty", jsii_struct_bases=[])
    class UserSettingProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html
        """
        action: str
        """``CfnStack.UserSettingProperty.Action``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-action
        """

        permission: str
        """``CfnStack.UserSettingProperty.Permission``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-appstream-stack-usersetting.html#cfn-appstream-stack-usersetting-permission
        """


class CfnStackFleetAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociation"):
    """A CloudFormation ``AWS::AppStream::StackFleetAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
    cloudformationResource:
        AWS::AppStream::StackFleetAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, fleet_name: str, stack_name: str) -> None:
        """Create a new ``AWS::AppStream::StackFleetAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            fleetName: ``AWS::AppStream::StackFleetAssociation.FleetName``.
            stackName: ``AWS::AppStream::StackFleetAssociation.StackName``.
        """
        props: CfnStackFleetAssociationProps = {"fleetName": fleet_name, "stackName": stack_name}

        jsii.create(CfnStackFleetAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnStackFleetAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStackFleetAssociationProps", jsii_struct_bases=[])
class CfnStackFleetAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::AppStream::StackFleetAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html
    """
    fleetName: str
    """``AWS::AppStream::StackFleetAssociation.FleetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-fleetname
    """

    stackName: str
    """``AWS::AppStream::StackFleetAssociation.StackName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackfleetassociation.html#cfn-appstream-stackfleetassociation-stackname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStackProps", jsii_struct_bases=[])
class CfnStackProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::AppStream::Stack``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html
    """
    applicationSettings: typing.Union[aws_cdk.cdk.Token, "CfnStack.ApplicationSettingsProperty"]
    """``AWS::AppStream::Stack.ApplicationSettings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-applicationsettings
    """

    attributesToDelete: typing.List[str]
    """``AWS::AppStream::Stack.AttributesToDelete``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-attributestodelete
    """

    deleteStorageConnectors: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AppStream::Stack.DeleteStorageConnectors``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-deletestorageconnectors
    """

    description: str
    """``AWS::AppStream::Stack.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-description
    """

    displayName: str
    """``AWS::AppStream::Stack.DisplayName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-displayname
    """

    feedbackUrl: str
    """``AWS::AppStream::Stack.FeedbackURL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-feedbackurl
    """

    name: str
    """``AWS::AppStream::Stack.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-name
    """

    redirectUrl: str
    """``AWS::AppStream::Stack.RedirectURL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-redirecturl
    """

    storageConnectors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.StorageConnectorProperty"]]]
    """``AWS::AppStream::Stack.StorageConnectors``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-storageconnectors
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::AppStream::Stack.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-tags
    """

    userSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnStack.UserSettingProperty"]]]
    """``AWS::AppStream::Stack.UserSettings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stack.html#cfn-appstream-stack-usersettings
    """

class CfnStackUserAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociation"):
    """A CloudFormation ``AWS::AppStream::StackUserAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
    cloudformationResource:
        AWS::AppStream::StackUserAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication_type: str, stack_name: str, user_name: str, send_email_notification: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::AppStream::StackUserAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            authenticationType: ``AWS::AppStream::StackUserAssociation.AuthenticationType``.
            stackName: ``AWS::AppStream::StackUserAssociation.StackName``.
            userName: ``AWS::AppStream::StackUserAssociation.UserName``.
            sendEmailNotification: ``AWS::AppStream::StackUserAssociation.SendEmailNotification``.
        """
        props: CfnStackUserAssociationProps = {"authenticationType": authentication_type, "stackName": stack_name, "userName": user_name}

        if send_email_notification is not None:
            props["sendEmailNotification"] = send_email_notification

        jsii.create(CfnStackUserAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnStackUserAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnStackUserAssociationProps(jsii.compat.TypedDict, total=False):
    sendEmailNotification: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AppStream::StackUserAssociation.SendEmailNotification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-sendemailnotification
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnStackUserAssociationProps", jsii_struct_bases=[_CfnStackUserAssociationProps])
class CfnStackUserAssociationProps(_CfnStackUserAssociationProps):
    """Properties for defining a ``AWS::AppStream::StackUserAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html
    """
    authenticationType: str
    """``AWS::AppStream::StackUserAssociation.AuthenticationType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-authenticationtype
    """

    stackName: str
    """``AWS::AppStream::StackUserAssociation.StackName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-stackname
    """

    userName: str
    """``AWS::AppStream::StackUserAssociation.UserName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-stackuserassociation.html#cfn-appstream-stackuserassociation-username
    """

class CfnUser(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-appstream.CfnUser"):
    """A CloudFormation ``AWS::AppStream::User``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
    cloudformationResource:
        AWS::AppStream::User
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authentication_type: str, user_name: str, first_name: typing.Optional[str]=None, last_name: typing.Optional[str]=None, message_action: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AppStream::User``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            authenticationType: ``AWS::AppStream::User.AuthenticationType``.
            userName: ``AWS::AppStream::User.UserName``.
            firstName: ``AWS::AppStream::User.FirstName``.
            lastName: ``AWS::AppStream::User.LastName``.
            messageAction: ``AWS::AppStream::User.MessageAction``.
        """
        props: CfnUserProps = {"authenticationType": authentication_type, "userName": user_name}

        if first_name is not None:
            props["firstName"] = first_name

        if last_name is not None:
            props["lastName"] = last_name

        if message_action is not None:
            props["messageAction"] = message_action

        jsii.create(CfnUser, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnUserProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnUserProps(jsii.compat.TypedDict, total=False):
    firstName: str
    """``AWS::AppStream::User.FirstName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-firstname
    """
    lastName: str
    """``AWS::AppStream::User.LastName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-lastname
    """
    messageAction: str
    """``AWS::AppStream::User.MessageAction``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-messageaction
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-appstream.CfnUserProps", jsii_struct_bases=[_CfnUserProps])
class CfnUserProps(_CfnUserProps):
    """Properties for defining a ``AWS::AppStream::User``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html
    """
    authenticationType: str
    """``AWS::AppStream::User.AuthenticationType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-authenticationtype
    """

    userName: str
    """``AWS::AppStream::User.UserName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-appstream-user.html#cfn-appstream-user-username
    """

__all__ = ["CfnDirectoryConfig", "CfnDirectoryConfigProps", "CfnFleet", "CfnFleetProps", "CfnImageBuilder", "CfnImageBuilderProps", "CfnStack", "CfnStackFleetAssociation", "CfnStackFleetAssociationProps", "CfnStackProps", "CfnStackUserAssociation", "CfnStackUserAssociationProps", "CfnUser", "CfnUserProps", "__jsii_assembly__"]

publication.publish()
