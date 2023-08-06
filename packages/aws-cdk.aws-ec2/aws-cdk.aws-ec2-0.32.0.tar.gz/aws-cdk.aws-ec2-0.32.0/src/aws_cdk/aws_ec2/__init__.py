import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ec2", "0.32.0", __name__, "aws-ec2@0.32.0.jsii.tgz")
@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxEdition")
class AmazonLinuxEdition(enum.Enum):
    """Amazon Linux edition."""
    Standard = "Standard"
    """Standard edition."""
    Minimal = "Minimal"
    """Minimal edition."""

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxGeneration")
class AmazonLinuxGeneration(enum.Enum):
    """What generation of Amazon Linux to use."""
    AmazonLinux = "AmazonLinux"
    """Amazon Linux."""
    AmazonLinux2 = "AmazonLinux2"
    """Amazon Linux 2."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxImageProps", jsii_struct_bases=[])
class AmazonLinuxImageProps(jsii.compat.TypedDict, total=False):
    """Amazon Linux image properties."""
    edition: "AmazonLinuxEdition"
    """What edition of Amazon Linux to use.

    Default:
        Standard
    """

    generation: "AmazonLinuxGeneration"
    """What generation of Amazon Linux to use.

    Default:
        AmazonLinux
    """

    storage: "AmazonLinuxStorage"
    """What storage backed image to use.

    Default:
        GeneralPurpose
    """

    virtualization: "AmazonLinuxVirt"
    """Virtualization type.

    Default:
        HVM
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxStorage")
class AmazonLinuxStorage(enum.Enum):
    EBS = "EBS"
    """EBS-backed storage."""
    GeneralPurpose = "GeneralPurpose"
    """General Purpose-based storage (recommended)."""

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.AmazonLinuxVirt")
class AmazonLinuxVirt(enum.Enum):
    """Virtualization type for Amazon Linux."""
    HVM = "HVM"
    """HVM virtualization (recommended)."""
    PV = "PV"
    """PV virtualization."""

class CfnCustomerGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnCustomerGateway"):
    """A CloudFormation ``AWS::EC2::CustomerGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html
    cloudformationResource:
        AWS::EC2::CustomerGateway
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, bgp_asn: typing.Union[jsii.Number, aws_cdk.cdk.Token], ip_address: str, type: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::CustomerGateway``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            bgpAsn: ``AWS::EC2::CustomerGateway.BgpAsn``.
            ipAddress: ``AWS::EC2::CustomerGateway.IpAddress``.
            type: ``AWS::EC2::CustomerGateway.Type``.
            tags: ``AWS::EC2::CustomerGateway.Tags``.
        """
        props: CfnCustomerGatewayProps = {"bgpAsn": bgp_asn, "ipAddress": ip_address, "type": type}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnCustomerGateway, self, [scope, id, props])

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
    @jsii.member(jsii_name="customerGatewayName")
    def customer_gateway_name(self) -> str:
        return jsii.get(self, "customerGatewayName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCustomerGatewayProps":
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
class _CfnCustomerGatewayProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::CustomerGateway.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html#cfn-ec2-customergateway-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnCustomerGatewayProps", jsii_struct_bases=[_CfnCustomerGatewayProps])
class CfnCustomerGatewayProps(_CfnCustomerGatewayProps):
    """Properties for defining a ``AWS::EC2::CustomerGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html
    """
    bgpAsn: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::CustomerGateway.BgpAsn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html#cfn-ec2-customergateway-bgpasn
    """

    ipAddress: str
    """``AWS::EC2::CustomerGateway.IpAddress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html#cfn-ec2-customergateway-ipaddress
    """

    type: str
    """``AWS::EC2::CustomerGateway.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-customer-gateway.html#cfn-ec2-customergateway-type
    """

class CfnDHCPOptions(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnDHCPOptions"):
    """A CloudFormation ``AWS::EC2::DHCPOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html
    cloudformationResource:
        AWS::EC2::DHCPOptions
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain_name: typing.Optional[str]=None, domain_name_servers: typing.Optional[typing.List[str]]=None, netbios_name_servers: typing.Optional[typing.List[str]]=None, netbios_node_type: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, ntp_servers: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::DHCPOptions``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            domainName: ``AWS::EC2::DHCPOptions.DomainName``.
            domainNameServers: ``AWS::EC2::DHCPOptions.DomainNameServers``.
            netbiosNameServers: ``AWS::EC2::DHCPOptions.NetbiosNameServers``.
            netbiosNodeType: ``AWS::EC2::DHCPOptions.NetbiosNodeType``.
            ntpServers: ``AWS::EC2::DHCPOptions.NtpServers``.
            tags: ``AWS::EC2::DHCPOptions.Tags``.
        """
        props: CfnDHCPOptionsProps = {}

        if domain_name is not None:
            props["domainName"] = domain_name

        if domain_name_servers is not None:
            props["domainNameServers"] = domain_name_servers

        if netbios_name_servers is not None:
            props["netbiosNameServers"] = netbios_name_servers

        if netbios_node_type is not None:
            props["netbiosNodeType"] = netbios_node_type

        if ntp_servers is not None:
            props["ntpServers"] = ntp_servers

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDHCPOptions, self, [scope, id, props])

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
    @jsii.member(jsii_name="dhcpOptionsName")
    def dhcp_options_name(self) -> str:
        return jsii.get(self, "dhcpOptionsName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDHCPOptionsProps":
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


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnDHCPOptionsProps", jsii_struct_bases=[])
class CfnDHCPOptionsProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::DHCPOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html
    """
    domainName: str
    """``AWS::EC2::DHCPOptions.DomainName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html#cfn-ec2-dhcpoptions-domainname
    """

    domainNameServers: typing.List[str]
    """``AWS::EC2::DHCPOptions.DomainNameServers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html#cfn-ec2-dhcpoptions-domainnameservers
    """

    netbiosNameServers: typing.List[str]
    """``AWS::EC2::DHCPOptions.NetbiosNameServers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html#cfn-ec2-dhcpoptions-netbiosnameservers
    """

    netbiosNodeType: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::DHCPOptions.NetbiosNodeType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html#cfn-ec2-dhcpoptions-netbiosnodetype
    """

    ntpServers: typing.List[str]
    """``AWS::EC2::DHCPOptions.NtpServers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html#cfn-ec2-dhcpoptions-ntpservers
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::DHCPOptions.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-dhcp-options.html#cfn-ec2-dhcpoptions-tags
    """

class CfnEC2Fleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet"):
    """A CloudFormation ``AWS::EC2::EC2Fleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html
    cloudformationResource:
        AWS::EC2::EC2Fleet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, launch_template_configs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "FleetLaunchTemplateConfigRequestProperty"]]], target_capacity_specification: typing.Union[aws_cdk.cdk.Token, "TargetCapacitySpecificationRequestProperty"], excess_capacity_termination_policy: typing.Optional[str]=None, on_demand_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["OnDemandOptionsRequestProperty"]]]=None, replace_unhealthy_instances: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, spot_options: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SpotOptionsRequestProperty"]]]=None, tag_specifications: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "TagSpecificationProperty"]]]]]=None, terminate_instances_with_expiration: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, type: typing.Optional[str]=None, valid_from: typing.Optional[str]=None, valid_until: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::EC2Fleet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            launchTemplateConfigs: ``AWS::EC2::EC2Fleet.LaunchTemplateConfigs``.
            targetCapacitySpecification: ``AWS::EC2::EC2Fleet.TargetCapacitySpecification``.
            excessCapacityTerminationPolicy: ``AWS::EC2::EC2Fleet.ExcessCapacityTerminationPolicy``.
            onDemandOptions: ``AWS::EC2::EC2Fleet.OnDemandOptions``.
            replaceUnhealthyInstances: ``AWS::EC2::EC2Fleet.ReplaceUnhealthyInstances``.
            spotOptions: ``AWS::EC2::EC2Fleet.SpotOptions``.
            tagSpecifications: ``AWS::EC2::EC2Fleet.TagSpecifications``.
            terminateInstancesWithExpiration: ``AWS::EC2::EC2Fleet.TerminateInstancesWithExpiration``.
            type: ``AWS::EC2::EC2Fleet.Type``.
            validFrom: ``AWS::EC2::EC2Fleet.ValidFrom``.
            validUntil: ``AWS::EC2::EC2Fleet.ValidUntil``.
        """
        props: CfnEC2FleetProps = {"launchTemplateConfigs": launch_template_configs, "targetCapacitySpecification": target_capacity_specification}

        if excess_capacity_termination_policy is not None:
            props["excessCapacityTerminationPolicy"] = excess_capacity_termination_policy

        if on_demand_options is not None:
            props["onDemandOptions"] = on_demand_options

        if replace_unhealthy_instances is not None:
            props["replaceUnhealthyInstances"] = replace_unhealthy_instances

        if spot_options is not None:
            props["spotOptions"] = spot_options

        if tag_specifications is not None:
            props["tagSpecifications"] = tag_specifications

        if terminate_instances_with_expiration is not None:
            props["terminateInstancesWithExpiration"] = terminate_instances_with_expiration

        if type is not None:
            props["type"] = type

        if valid_from is not None:
            props["validFrom"] = valid_from

        if valid_until is not None:
            props["validUntil"] = valid_until

        jsii.create(CfnEC2Fleet, self, [scope, id, props])

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
    @jsii.member(jsii_name="ec2FleetId")
    def ec2_fleet_id(self) -> str:
        return jsii.get(self, "ec2FleetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEC2FleetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.FleetLaunchTemplateConfigRequestProperty", jsii_struct_bases=[])
    class FleetLaunchTemplateConfigRequestProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateconfigrequest.html
        """
        launchTemplateSpecification: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty"]
        """``CfnEC2Fleet.FleetLaunchTemplateConfigRequestProperty.LaunchTemplateSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateconfigrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateconfigrequest-launchtemplatespecification
        """

        overrides: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty"]]]
        """``CfnEC2Fleet.FleetLaunchTemplateConfigRequestProperty.Overrides``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateconfigrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateconfigrequest-overrides
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty", jsii_struct_bases=[])
    class FleetLaunchTemplateOverridesRequestProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html
        """
        availabilityZone: str
        """``CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty.AvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest-availabilityzone
        """

        instanceType: str
        """``CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest-instancetype
        """

        maxPrice: str
        """``CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty.MaxPrice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest-maxprice
        """

        priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty.Priority``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest-priority
        """

        subnetId: str
        """``CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest-subnetid
        """

        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnEC2Fleet.FleetLaunchTemplateOverridesRequestProperty.WeightedCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplateoverridesrequest-weightedcapacity
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty", jsii_struct_bases=[])
    class FleetLaunchTemplateSpecificationRequestProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest.html
        """
        launchTemplateId: str
        """``CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty.LaunchTemplateId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest-launchtemplateid
        """

        launchTemplateName: str
        """``CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty.LaunchTemplateName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest-launchtemplatename
        """

        version: str
        """``CfnEC2Fleet.FleetLaunchTemplateSpecificationRequestProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest.html#cfn-ec2-ec2fleet-fleetlaunchtemplatespecificationrequest-version
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.OnDemandOptionsRequestProperty", jsii_struct_bases=[])
    class OnDemandOptionsRequestProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-ondemandoptionsrequest.html
        """
        allocationStrategy: str
        """``CfnEC2Fleet.OnDemandOptionsRequestProperty.AllocationStrategy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-ondemandoptionsrequest.html#cfn-ec2-ec2fleet-ondemandoptionsrequest-allocationstrategy
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.SpotOptionsRequestProperty", jsii_struct_bases=[])
    class SpotOptionsRequestProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-spotoptionsrequest.html
        """
        allocationStrategy: str
        """``CfnEC2Fleet.SpotOptionsRequestProperty.AllocationStrategy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-spotoptionsrequest.html#cfn-ec2-ec2fleet-spotoptionsrequest-allocationstrategy
        """

        instanceInterruptionBehavior: str
        """``CfnEC2Fleet.SpotOptionsRequestProperty.InstanceInterruptionBehavior``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-spotoptionsrequest.html#cfn-ec2-ec2fleet-spotoptionsrequest-instanceinterruptionbehavior
        """

        instancePoolsToUseCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnEC2Fleet.SpotOptionsRequestProperty.InstancePoolsToUseCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-spotoptionsrequest.html#cfn-ec2-ec2fleet-spotoptionsrequest-instancepoolstousecount
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.TagRequestProperty", jsii_struct_bases=[])
    class TagRequestProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-tagrequest.html
        """
        key: str
        """``CfnEC2Fleet.TagRequestProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-tagrequest.html#cfn-ec2-ec2fleet-tagrequest-key
        """

        value: str
        """``CfnEC2Fleet.TagRequestProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-tagrequest.html#cfn-ec2-ec2fleet-tagrequest-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.TagSpecificationProperty", jsii_struct_bases=[])
    class TagSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-tagspecification.html
        """
        resourceType: str
        """``CfnEC2Fleet.TagSpecificationProperty.ResourceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-tagspecification.html#cfn-ec2-ec2fleet-tagspecification-resourcetype
        """

        tags: typing.List["CfnEC2Fleet.TagRequestProperty"]
        """``CfnEC2Fleet.TagSpecificationProperty.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-tagspecification.html#cfn-ec2-ec2fleet-tagspecification-tags
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TargetCapacitySpecificationRequestProperty(jsii.compat.TypedDict, total=False):
        defaultTargetCapacityType: str
        """``CfnEC2Fleet.TargetCapacitySpecificationRequestProperty.DefaultTargetCapacityType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-targetcapacityspecificationrequest.html#cfn-ec2-ec2fleet-targetcapacityspecificationrequest-defaulttargetcapacitytype
        """
        onDemandTargetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnEC2Fleet.TargetCapacitySpecificationRequestProperty.OnDemandTargetCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-targetcapacityspecificationrequest.html#cfn-ec2-ec2fleet-targetcapacityspecificationrequest-ondemandtargetcapacity
        """
        spotTargetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnEC2Fleet.TargetCapacitySpecificationRequestProperty.SpotTargetCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-targetcapacityspecificationrequest.html#cfn-ec2-ec2fleet-targetcapacityspecificationrequest-spottargetcapacity
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2Fleet.TargetCapacitySpecificationRequestProperty", jsii_struct_bases=[_TargetCapacitySpecificationRequestProperty])
    class TargetCapacitySpecificationRequestProperty(_TargetCapacitySpecificationRequestProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-targetcapacityspecificationrequest.html
        """
        totalTargetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnEC2Fleet.TargetCapacitySpecificationRequestProperty.TotalTargetCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ec2fleet-targetcapacityspecificationrequest.html#cfn-ec2-ec2fleet-targetcapacityspecificationrequest-totaltargetcapacity
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnEC2FleetProps(jsii.compat.TypedDict, total=False):
    excessCapacityTerminationPolicy: str
    """``AWS::EC2::EC2Fleet.ExcessCapacityTerminationPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-excesscapacityterminationpolicy
    """
    onDemandOptions: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.OnDemandOptionsRequestProperty"]
    """``AWS::EC2::EC2Fleet.OnDemandOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-ondemandoptions
    """
    replaceUnhealthyInstances: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::EC2Fleet.ReplaceUnhealthyInstances``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-replaceunhealthyinstances
    """
    spotOptions: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.SpotOptionsRequestProperty"]
    """``AWS::EC2::EC2Fleet.SpotOptions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-spotoptions
    """
    tagSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.TagSpecificationProperty"]]]
    """``AWS::EC2::EC2Fleet.TagSpecifications``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-tagspecifications
    """
    terminateInstancesWithExpiration: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::EC2Fleet.TerminateInstancesWithExpiration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-terminateinstanceswithexpiration
    """
    type: str
    """``AWS::EC2::EC2Fleet.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-type
    """
    validFrom: str
    """``AWS::EC2::EC2Fleet.ValidFrom``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-validfrom
    """
    validUntil: str
    """``AWS::EC2::EC2Fleet.ValidUntil``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-validuntil
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEC2FleetProps", jsii_struct_bases=[_CfnEC2FleetProps])
class CfnEC2FleetProps(_CfnEC2FleetProps):
    """Properties for defining a ``AWS::EC2::EC2Fleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html
    """
    launchTemplateConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.FleetLaunchTemplateConfigRequestProperty"]]]
    """``AWS::EC2::EC2Fleet.LaunchTemplateConfigs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-launchtemplateconfigs
    """

    targetCapacitySpecification: typing.Union[aws_cdk.cdk.Token, "CfnEC2Fleet.TargetCapacitySpecificationRequestProperty"]
    """``AWS::EC2::EC2Fleet.TargetCapacitySpecification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-ec2fleet.html#cfn-ec2-ec2fleet-targetcapacityspecification
    """

class CfnEIP(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEIP"):
    """A CloudFormation ``AWS::EC2::EIP``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html
    cloudformationResource:
        AWS::EC2::EIP
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, domain: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, public_ipv4_pool: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::EIP``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            domain: ``AWS::EC2::EIP.Domain``.
            instanceId: ``AWS::EC2::EIP.InstanceId``.
            publicIpv4Pool: ``AWS::EC2::EIP.PublicIpv4Pool``.
        """
        props: CfnEIPProps = {}

        if domain is not None:
            props["domain"] = domain

        if instance_id is not None:
            props["instanceId"] = instance_id

        if public_ipv4_pool is not None:
            props["publicIpv4Pool"] = public_ipv4_pool

        jsii.create(CfnEIP, self, [scope, id, props])

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
    @jsii.member(jsii_name="eipAllocationId")
    def eip_allocation_id(self) -> str:
        """
        cloudformationAttribute:
            AllocationId
        """
        return jsii.get(self, "eipAllocationId")

    @property
    @jsii.member(jsii_name="eipIp")
    def eip_ip(self) -> str:
        return jsii.get(self, "eipIp")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEIPProps":
        return jsii.get(self, "propertyOverrides")


class CfnEIPAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEIPAssociation"):
    """A CloudFormation ``AWS::EC2::EIPAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html
    cloudformationResource:
        AWS::EC2::EIPAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allocation_id: typing.Optional[str]=None, eip: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, network_interface_id: typing.Optional[str]=None, private_ip_address: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::EIPAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            allocationId: ``AWS::EC2::EIPAssociation.AllocationId``.
            eip: ``AWS::EC2::EIPAssociation.EIP``.
            instanceId: ``AWS::EC2::EIPAssociation.InstanceId``.
            networkInterfaceId: ``AWS::EC2::EIPAssociation.NetworkInterfaceId``.
            privateIpAddress: ``AWS::EC2::EIPAssociation.PrivateIpAddress``.
        """
        props: CfnEIPAssociationProps = {}

        if allocation_id is not None:
            props["allocationId"] = allocation_id

        if eip is not None:
            props["eip"] = eip

        if instance_id is not None:
            props["instanceId"] = instance_id

        if network_interface_id is not None:
            props["networkInterfaceId"] = network_interface_id

        if private_ip_address is not None:
            props["privateIpAddress"] = private_ip_address

        jsii.create(CfnEIPAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="eipAssociationName")
    def eip_association_name(self) -> str:
        return jsii.get(self, "eipAssociationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEIPAssociationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEIPAssociationProps", jsii_struct_bases=[])
class CfnEIPAssociationProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::EIPAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html
    """
    allocationId: str
    """``AWS::EC2::EIPAssociation.AllocationId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html#cfn-ec2-eipassociation-allocationid
    """

    eip: str
    """``AWS::EC2::EIPAssociation.EIP``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html#cfn-ec2-eipassociation-eip
    """

    instanceId: str
    """``AWS::EC2::EIPAssociation.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html#cfn-ec2-eipassociation-instanceid
    """

    networkInterfaceId: str
    """``AWS::EC2::EIPAssociation.NetworkInterfaceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html#cfn-ec2-eipassociation-networkinterfaceid
    """

    privateIpAddress: str
    """``AWS::EC2::EIPAssociation.PrivateIpAddress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip-association.html#cfn-ec2-eipassociation-PrivateIpAddress
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEIPProps", jsii_struct_bases=[])
class CfnEIPProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::EIP``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html
    """
    domain: str
    """``AWS::EC2::EIP.Domain``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html#cfn-ec2-eip-domain
    """

    instanceId: str
    """``AWS::EC2::EIP.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html#cfn-ec2-eip-instanceid
    """

    publicIpv4Pool: str
    """``AWS::EC2::EIP.PublicIpv4Pool``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-eip.html#cfn-ec2-eip-publicipv4pool
    """

class CfnEgressOnlyInternetGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnEgressOnlyInternetGateway"):
    """A CloudFormation ``AWS::EC2::EgressOnlyInternetGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-egressonlyinternetgateway.html
    cloudformationResource:
        AWS::EC2::EgressOnlyInternetGateway
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str) -> None:
        """Create a new ``AWS::EC2::EgressOnlyInternetGateway``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            vpcId: ``AWS::EC2::EgressOnlyInternetGateway.VpcId``.
        """
        props: CfnEgressOnlyInternetGatewayProps = {"vpcId": vpc_id}

        jsii.create(CfnEgressOnlyInternetGateway, self, [scope, id, props])

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
    @jsii.member(jsii_name="egressOnlyInternetGatewayId")
    def egress_only_internet_gateway_id(self) -> str:
        return jsii.get(self, "egressOnlyInternetGatewayId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEgressOnlyInternetGatewayProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnEgressOnlyInternetGatewayProps", jsii_struct_bases=[])
class CfnEgressOnlyInternetGatewayProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::EgressOnlyInternetGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-egressonlyinternetgateway.html
    """
    vpcId: str
    """``AWS::EC2::EgressOnlyInternetGateway.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-egressonlyinternetgateway.html#cfn-ec2-egressonlyinternetgateway-vpcid
    """

class CfnFlowLog(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnFlowLog"):
    """A CloudFormation ``AWS::EC2::FlowLog``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html
    cloudformationResource:
        AWS::EC2::FlowLog
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_id: str, resource_type: str, traffic_type: str, deliver_logs_permission_arn: typing.Optional[str]=None, log_destination: typing.Optional[str]=None, log_destination_type: typing.Optional[str]=None, log_group_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::FlowLog``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            resourceId: ``AWS::EC2::FlowLog.ResourceId``.
            resourceType: ``AWS::EC2::FlowLog.ResourceType``.
            trafficType: ``AWS::EC2::FlowLog.TrafficType``.
            deliverLogsPermissionArn: ``AWS::EC2::FlowLog.DeliverLogsPermissionArn``.
            logDestination: ``AWS::EC2::FlowLog.LogDestination``.
            logDestinationType: ``AWS::EC2::FlowLog.LogDestinationType``.
            logGroupName: ``AWS::EC2::FlowLog.LogGroupName``.
        """
        props: CfnFlowLogProps = {"resourceId": resource_id, "resourceType": resource_type, "trafficType": traffic_type}

        if deliver_logs_permission_arn is not None:
            props["deliverLogsPermissionArn"] = deliver_logs_permission_arn

        if log_destination is not None:
            props["logDestination"] = log_destination

        if log_destination_type is not None:
            props["logDestinationType"] = log_destination_type

        if log_group_name is not None:
            props["logGroupName"] = log_group_name

        jsii.create(CfnFlowLog, self, [scope, id, props])

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
    @jsii.member(jsii_name="flowLogId")
    def flow_log_id(self) -> str:
        return jsii.get(self, "flowLogId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFlowLogProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnFlowLogProps(jsii.compat.TypedDict, total=False):
    deliverLogsPermissionArn: str
    """``AWS::EC2::FlowLog.DeliverLogsPermissionArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-deliverlogspermissionarn
    """
    logDestination: str
    """``AWS::EC2::FlowLog.LogDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestination
    """
    logDestinationType: str
    """``AWS::EC2::FlowLog.LogDestinationType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-logdestinationtype
    """
    logGroupName: str
    """``AWS::EC2::FlowLog.LogGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-loggroupname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnFlowLogProps", jsii_struct_bases=[_CfnFlowLogProps])
class CfnFlowLogProps(_CfnFlowLogProps):
    """Properties for defining a ``AWS::EC2::FlowLog``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html
    """
    resourceId: str
    """``AWS::EC2::FlowLog.ResourceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-resourceid
    """

    resourceType: str
    """``AWS::EC2::FlowLog.ResourceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-resourcetype
    """

    trafficType: str
    """``AWS::EC2::FlowLog.TrafficType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-flowlog.html#cfn-ec2-flowlog-traffictype
    """

class CfnHost(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnHost"):
    """A CloudFormation ``AWS::EC2::Host``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html
    cloudformationResource:
        AWS::EC2::Host
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, instance_type: str, auto_placement: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::Host``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            availabilityZone: ``AWS::EC2::Host.AvailabilityZone``.
            instanceType: ``AWS::EC2::Host.InstanceType``.
            autoPlacement: ``AWS::EC2::Host.AutoPlacement``.
        """
        props: CfnHostProps = {"availabilityZone": availability_zone, "instanceType": instance_type}

        if auto_placement is not None:
            props["autoPlacement"] = auto_placement

        jsii.create(CfnHost, self, [scope, id, props])

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
    @jsii.member(jsii_name="hostId")
    def host_id(self) -> str:
        return jsii.get(self, "hostId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHostProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnHostProps(jsii.compat.TypedDict, total=False):
    autoPlacement: str
    """``AWS::EC2::Host.AutoPlacement``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html#cfn-ec2-host-autoplacement
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnHostProps", jsii_struct_bases=[_CfnHostProps])
class CfnHostProps(_CfnHostProps):
    """Properties for defining a ``AWS::EC2::Host``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html
    """
    availabilityZone: str
    """``AWS::EC2::Host.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html#cfn-ec2-host-availabilityzone
    """

    instanceType: str
    """``AWS::EC2::Host.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-host.html#cfn-ec2-host-instancetype
    """

class CfnInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnInstance"):
    """A CloudFormation ``AWS::EC2::Instance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html
    cloudformationResource:
        AWS::EC2::Instance
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, additional_info: typing.Optional[str]=None, affinity: typing.Optional[str]=None, availability_zone: typing.Optional[str]=None, block_device_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "BlockDeviceMappingProperty"]]]]]=None, credit_specification: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["CreditSpecificationProperty"]]]=None, disable_api_termination: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, ebs_optimized: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, elastic_gpu_specifications: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticGpuSpecificationProperty"]]]]]=None, elastic_inference_accelerators: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticInferenceAcceleratorProperty"]]]]]=None, host_id: typing.Optional[str]=None, iam_instance_profile: typing.Optional[str]=None, image_id: typing.Optional[str]=None, instance_initiated_shutdown_behavior: typing.Optional[str]=None, instance_type: typing.Optional[str]=None, ipv6_address_count: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, ipv6_addresses: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "InstanceIpv6AddressProperty"]]]]]=None, kernel_id: typing.Optional[str]=None, key_name: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["LaunchTemplateSpecificationProperty"]]]=None, license_specifications: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "LicenseSpecificationProperty"]]]]]=None, monitoring: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, network_interfaces: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "NetworkInterfaceProperty"]]]]]=None, placement_group_name: typing.Optional[str]=None, private_ip_address: typing.Optional[str]=None, ramdisk_id: typing.Optional[str]=None, security_group_ids: typing.Optional[typing.List[str]]=None, security_groups: typing.Optional[typing.List[str]]=None, source_dest_check: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, ssm_associations: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "SsmAssociationProperty"]]]]]=None, subnet_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, tenancy: typing.Optional[str]=None, user_data: typing.Optional[str]=None, volumes: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "VolumeProperty"]]]]]=None) -> None:
        """Create a new ``AWS::EC2::Instance``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            additionalInfo: ``AWS::EC2::Instance.AdditionalInfo``.
            affinity: ``AWS::EC2::Instance.Affinity``.
            availabilityZone: ``AWS::EC2::Instance.AvailabilityZone``.
            blockDeviceMappings: ``AWS::EC2::Instance.BlockDeviceMappings``.
            creditSpecification: ``AWS::EC2::Instance.CreditSpecification``.
            disableApiTermination: ``AWS::EC2::Instance.DisableApiTermination``.
            ebsOptimized: ``AWS::EC2::Instance.EbsOptimized``.
            elasticGpuSpecifications: ``AWS::EC2::Instance.ElasticGpuSpecifications``.
            elasticInferenceAccelerators: ``AWS::EC2::Instance.ElasticInferenceAccelerators``.
            hostId: ``AWS::EC2::Instance.HostId``.
            iamInstanceProfile: ``AWS::EC2::Instance.IamInstanceProfile``.
            imageId: ``AWS::EC2::Instance.ImageId``.
            instanceInitiatedShutdownBehavior: ``AWS::EC2::Instance.InstanceInitiatedShutdownBehavior``.
            instanceType: ``AWS::EC2::Instance.InstanceType``.
            ipv6AddressCount: ``AWS::EC2::Instance.Ipv6AddressCount``.
            ipv6Addresses: ``AWS::EC2::Instance.Ipv6Addresses``.
            kernelId: ``AWS::EC2::Instance.KernelId``.
            keyName: ``AWS::EC2::Instance.KeyName``.
            launchTemplate: ``AWS::EC2::Instance.LaunchTemplate``.
            licenseSpecifications: ``AWS::EC2::Instance.LicenseSpecifications``.
            monitoring: ``AWS::EC2::Instance.Monitoring``.
            networkInterfaces: ``AWS::EC2::Instance.NetworkInterfaces``.
            placementGroupName: ``AWS::EC2::Instance.PlacementGroupName``.
            privateIpAddress: ``AWS::EC2::Instance.PrivateIpAddress``.
            ramdiskId: ``AWS::EC2::Instance.RamdiskId``.
            securityGroupIds: ``AWS::EC2::Instance.SecurityGroupIds``.
            securityGroups: ``AWS::EC2::Instance.SecurityGroups``.
            sourceDestCheck: ``AWS::EC2::Instance.SourceDestCheck``.
            ssmAssociations: ``AWS::EC2::Instance.SsmAssociations``.
            subnetId: ``AWS::EC2::Instance.SubnetId``.
            tags: ``AWS::EC2::Instance.Tags``.
            tenancy: ``AWS::EC2::Instance.Tenancy``.
            userData: ``AWS::EC2::Instance.UserData``.
            volumes: ``AWS::EC2::Instance.Volumes``.
        """
        props: CfnInstanceProps = {}

        if additional_info is not None:
            props["additionalInfo"] = additional_info

        if affinity is not None:
            props["affinity"] = affinity

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if credit_specification is not None:
            props["creditSpecification"] = credit_specification

        if disable_api_termination is not None:
            props["disableApiTermination"] = disable_api_termination

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if elastic_gpu_specifications is not None:
            props["elasticGpuSpecifications"] = elastic_gpu_specifications

        if elastic_inference_accelerators is not None:
            props["elasticInferenceAccelerators"] = elastic_inference_accelerators

        if host_id is not None:
            props["hostId"] = host_id

        if iam_instance_profile is not None:
            props["iamInstanceProfile"] = iam_instance_profile

        if image_id is not None:
            props["imageId"] = image_id

        if instance_initiated_shutdown_behavior is not None:
            props["instanceInitiatedShutdownBehavior"] = instance_initiated_shutdown_behavior

        if instance_type is not None:
            props["instanceType"] = instance_type

        if ipv6_address_count is not None:
            props["ipv6AddressCount"] = ipv6_address_count

        if ipv6_addresses is not None:
            props["ipv6Addresses"] = ipv6_addresses

        if kernel_id is not None:
            props["kernelId"] = kernel_id

        if key_name is not None:
            props["keyName"] = key_name

        if launch_template is not None:
            props["launchTemplate"] = launch_template

        if license_specifications is not None:
            props["licenseSpecifications"] = license_specifications

        if monitoring is not None:
            props["monitoring"] = monitoring

        if network_interfaces is not None:
            props["networkInterfaces"] = network_interfaces

        if placement_group_name is not None:
            props["placementGroupName"] = placement_group_name

        if private_ip_address is not None:
            props["privateIpAddress"] = private_ip_address

        if ramdisk_id is not None:
            props["ramdiskId"] = ramdisk_id

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if source_dest_check is not None:
            props["sourceDestCheck"] = source_dest_check

        if ssm_associations is not None:
            props["ssmAssociations"] = ssm_associations

        if subnet_id is not None:
            props["subnetId"] = subnet_id

        if tags is not None:
            props["tags"] = tags

        if tenancy is not None:
            props["tenancy"] = tenancy

        if user_data is not None:
            props["userData"] = user_data

        if volumes is not None:
            props["volumes"] = volumes

        jsii.create(CfnInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="instanceAvailabilityZone")
    def instance_availability_zone(self) -> str:
        """
        cloudformationAttribute:
            AvailabilityZone
        """
        return jsii.get(self, "instanceAvailabilityZone")

    @property
    @jsii.member(jsii_name="instanceId")
    def instance_id(self) -> str:
        return jsii.get(self, "instanceId")

    @property
    @jsii.member(jsii_name="instancePrivateDnsName")
    def instance_private_dns_name(self) -> str:
        """
        cloudformationAttribute:
            PrivateDnsName
        """
        return jsii.get(self, "instancePrivateDnsName")

    @property
    @jsii.member(jsii_name="instancePrivateIp")
    def instance_private_ip(self) -> str:
        """
        cloudformationAttribute:
            PrivateIp
        """
        return jsii.get(self, "instancePrivateIp")

    @property
    @jsii.member(jsii_name="instancePublicDnsName")
    def instance_public_dns_name(self) -> str:
        """
        cloudformationAttribute:
            PublicDnsName
        """
        return jsii.get(self, "instancePublicDnsName")

    @property
    @jsii.member(jsii_name="instancePublicIp")
    def instance_public_ip(self) -> str:
        """
        cloudformationAttribute:
            PublicIp
        """
        return jsii.get(self, "instancePublicIp")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInstanceProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.AssociationParameterProperty", jsii_struct_bases=[])
    class AssociationParameterProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-ssmassociations-associationparameters.html
        """
        key: str
        """``CfnInstance.AssociationParameterProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-ssmassociations-associationparameters.html#cfn-ec2-instance-ssmassociations-associationparameters-key
        """

        value: typing.List[str]
        """``CfnInstance.AssociationParameterProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-ssmassociations-associationparameters.html#cfn-ec2-instance-ssmassociations-associationparameters-value
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnInstance.EbsProperty"]
        """``CfnInstance.BlockDeviceMappingProperty.Ebs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-mapping.html#cfn-ec2-blockdev-mapping-ebs
        """
        noDevice: typing.Union[aws_cdk.cdk.Token, "CfnInstance.NoDeviceProperty"]
        """``CfnInstance.BlockDeviceMappingProperty.NoDevice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-mapping.html#cfn-ec2-blockdev-mapping-nodevice
        """
        virtualName: str
        """``CfnInstance.BlockDeviceMappingProperty.VirtualName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-mapping.html#cfn-ec2-blockdev-mapping-virtualname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.BlockDeviceMappingProperty", jsii_struct_bases=[_BlockDeviceMappingProperty])
    class BlockDeviceMappingProperty(_BlockDeviceMappingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-mapping.html
        """
        deviceName: str
        """``CfnInstance.BlockDeviceMappingProperty.DeviceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-mapping.html#cfn-ec2-blockdev-mapping-devicename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.CreditSpecificationProperty", jsii_struct_bases=[])
    class CreditSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-creditspecification.html
        """
        cpuCredits: str
        """``CfnInstance.CreditSpecificationProperty.CPUCredits``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-creditspecification.html#cfn-ec2-instance-creditspecification-cpucredits
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.EbsProperty", jsii_struct_bases=[])
    class EbsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnInstance.EbsProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html#cfn-ec2-blockdev-template-deleteontermination
        """

        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnInstance.EbsProperty.Encrypted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html#cfn-ec2-blockdev-template-encrypted
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnInstance.EbsProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html#cfn-ec2-blockdev-template-iops
        """

        snapshotId: str
        """``CfnInstance.EbsProperty.SnapshotId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html#cfn-ec2-blockdev-template-snapshotid
        """

        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnInstance.EbsProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html#cfn-ec2-blockdev-template-volumesize
        """

        volumeType: str
        """``CfnInstance.EbsProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-blockdev-template.html#cfn-ec2-blockdev-template-volumetype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.ElasticGpuSpecificationProperty", jsii_struct_bases=[])
    class ElasticGpuSpecificationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-elasticgpuspecification.html
        """
        type: str
        """``CfnInstance.ElasticGpuSpecificationProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-elasticgpuspecification.html#cfn-ec2-instance-elasticgpuspecification-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.ElasticInferenceAcceleratorProperty", jsii_struct_bases=[])
    class ElasticInferenceAcceleratorProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-elasticinferenceaccelerator.html
        """
        type: str
        """``CfnInstance.ElasticInferenceAcceleratorProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-elasticinferenceaccelerator.html#cfn-ec2-instance-elasticinferenceaccelerator-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.InstanceIpv6AddressProperty", jsii_struct_bases=[])
    class InstanceIpv6AddressProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-instanceipv6address.html
        """
        ipv6Address: str
        """``CfnInstance.InstanceIpv6AddressProperty.Ipv6Address``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-instanceipv6address.html#cfn-ec2-instance-instanceipv6address-ipv6address
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        """``CfnInstance.LaunchTemplateSpecificationProperty.LaunchTemplateId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-launchtemplatespecification.html#cfn-ec2-instance-launchtemplatespecification-launchtemplateid
        """
        launchTemplateName: str
        """``CfnInstance.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-launchtemplatespecification.html#cfn-ec2-instance-launchtemplatespecification-launchtemplatename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.LaunchTemplateSpecificationProperty", jsii_struct_bases=[_LaunchTemplateSpecificationProperty])
    class LaunchTemplateSpecificationProperty(_LaunchTemplateSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-launchtemplatespecification.html
        """
        version: str
        """``CfnInstance.LaunchTemplateSpecificationProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-launchtemplatespecification.html#cfn-ec2-instance-launchtemplatespecification-version
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.LicenseSpecificationProperty", jsii_struct_bases=[])
    class LicenseSpecificationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-licensespecification.html
        """
        licenseConfigurationArn: str
        """``CfnInstance.LicenseSpecificationProperty.LicenseConfigurationArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-licensespecification.html#cfn-ec2-instance-licensespecification-licenseconfigurationarn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _NetworkInterfaceProperty(jsii.compat.TypedDict, total=False):
        associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnInstance.NetworkInterfaceProperty.AssociatePublicIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-associatepubip
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnInstance.NetworkInterfaceProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-delete
        """
        description: str
        """``CfnInstance.NetworkInterfaceProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-description
        """
        groupSet: typing.List[str]
        """``CfnInstance.NetworkInterfaceProperty.GroupSet``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-groupset
        """
        ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnInstance.NetworkInterfaceProperty.Ipv6AddressCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#cfn-ec2-instance-networkinterface-ipv6addresscount
        """
        ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.InstanceIpv6AddressProperty"]]]
        """``CfnInstance.NetworkInterfaceProperty.Ipv6Addresses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#cfn-ec2-instance-networkinterface-ipv6addresses
        """
        networkInterfaceId: str
        """``CfnInstance.NetworkInterfaceProperty.NetworkInterfaceId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-network-iface
        """
        privateIpAddress: str
        """``CfnInstance.NetworkInterfaceProperty.PrivateIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-privateipaddress
        """
        privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.PrivateIpAddressSpecificationProperty"]]]
        """``CfnInstance.NetworkInterfaceProperty.PrivateIpAddresses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-privateipaddresses
        """
        secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnInstance.NetworkInterfaceProperty.SecondaryPrivateIpAddressCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-secondprivateip
        """
        subnetId: str
        """``CfnInstance.NetworkInterfaceProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-subnetid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.NetworkInterfaceProperty", jsii_struct_bases=[_NetworkInterfaceProperty])
    class NetworkInterfaceProperty(_NetworkInterfaceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html
        """
        deviceIndex: str
        """``CfnInstance.NetworkInterfaceProperty.DeviceIndex``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-iface-embedded.html#aws-properties-ec2-network-iface-embedded-deviceindex
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.NoDeviceProperty", jsii_struct_bases=[])
    class NoDeviceProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-nodevice.html
        """
        pass

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.PrivateIpAddressSpecificationProperty", jsii_struct_bases=[])
    class PrivateIpAddressSpecificationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-interface-privateipspec.html
        """
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnInstance.PrivateIpAddressSpecificationProperty.Primary``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-interface-privateipspec.html#cfn-ec2-networkinterface-privateipspecification-primary
        """

        privateIpAddress: str
        """``CfnInstance.PrivateIpAddressSpecificationProperty.PrivateIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-interface-privateipspec.html#cfn-ec2-networkinterface-privateipspecification-privateipaddress
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SsmAssociationProperty(jsii.compat.TypedDict, total=False):
        associationParameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.AssociationParameterProperty"]]]
        """``CfnInstance.SsmAssociationProperty.AssociationParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-ssmassociations.html#cfn-ec2-instance-ssmassociations-associationparameters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.SsmAssociationProperty", jsii_struct_bases=[_SsmAssociationProperty])
    class SsmAssociationProperty(_SsmAssociationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-ssmassociations.html
        """
        documentName: str
        """``CfnInstance.SsmAssociationProperty.DocumentName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance-ssmassociations.html#cfn-ec2-instance-ssmassociations-documentname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstance.VolumeProperty", jsii_struct_bases=[])
    class VolumeProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-mount-point.html
        """
        device: str
        """``CfnInstance.VolumeProperty.Device``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-mount-point.html#cfn-ec2-mountpoint-device
        """

        volumeId: str
        """``CfnInstance.VolumeProperty.VolumeId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-mount-point.html#cfn-ec2-mountpoint-volumeid
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInstanceProps", jsii_struct_bases=[])
class CfnInstanceProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::Instance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html
    """
    additionalInfo: str
    """``AWS::EC2::Instance.AdditionalInfo``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-additionalinfo
    """

    affinity: str
    """``AWS::EC2::Instance.Affinity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-affinity
    """

    availabilityZone: str
    """``AWS::EC2::Instance.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-availabilityzone
    """

    blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.BlockDeviceMappingProperty"]]]
    """``AWS::EC2::Instance.BlockDeviceMappings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-blockdevicemappings
    """

    creditSpecification: typing.Union[aws_cdk.cdk.Token, "CfnInstance.CreditSpecificationProperty"]
    """``AWS::EC2::Instance.CreditSpecification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-creditspecification
    """

    disableApiTermination: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Instance.DisableApiTermination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-disableapitermination
    """

    ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Instance.EbsOptimized``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-ebsoptimized
    """

    elasticGpuSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.ElasticGpuSpecificationProperty"]]]
    """``AWS::EC2::Instance.ElasticGpuSpecifications``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-elasticgpuspecifications
    """

    elasticInferenceAccelerators: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.ElasticInferenceAcceleratorProperty"]]]
    """``AWS::EC2::Instance.ElasticInferenceAccelerators``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-elasticinferenceaccelerators
    """

    hostId: str
    """``AWS::EC2::Instance.HostId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-hostid
    """

    iamInstanceProfile: str
    """``AWS::EC2::Instance.IamInstanceProfile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-iaminstanceprofile
    """

    imageId: str
    """``AWS::EC2::Instance.ImageId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-imageid
    """

    instanceInitiatedShutdownBehavior: str
    """``AWS::EC2::Instance.InstanceInitiatedShutdownBehavior``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-instanceinitiatedshutdownbehavior
    """

    instanceType: str
    """``AWS::EC2::Instance.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-instancetype
    """

    ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::Instance.Ipv6AddressCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-ipv6addresscount
    """

    ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.InstanceIpv6AddressProperty"]]]
    """``AWS::EC2::Instance.Ipv6Addresses``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-ipv6addresses
    """

    kernelId: str
    """``AWS::EC2::Instance.KernelId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-kernelid
    """

    keyName: str
    """``AWS::EC2::Instance.KeyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-keyname
    """

    launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnInstance.LaunchTemplateSpecificationProperty"]
    """``AWS::EC2::Instance.LaunchTemplate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-launchtemplate
    """

    licenseSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.LicenseSpecificationProperty"]]]
    """``AWS::EC2::Instance.LicenseSpecifications``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-licensespecifications
    """

    monitoring: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Instance.Monitoring``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-monitoring
    """

    networkInterfaces: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.NetworkInterfaceProperty"]]]
    """``AWS::EC2::Instance.NetworkInterfaces``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-networkinterfaces
    """

    placementGroupName: str
    """``AWS::EC2::Instance.PlacementGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-placementgroupname
    """

    privateIpAddress: str
    """``AWS::EC2::Instance.PrivateIpAddress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-privateipaddress
    """

    ramdiskId: str
    """``AWS::EC2::Instance.RamdiskId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-ramdiskid
    """

    securityGroupIds: typing.List[str]
    """``AWS::EC2::Instance.SecurityGroupIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-securitygroupids
    """

    securityGroups: typing.List[str]
    """``AWS::EC2::Instance.SecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-securitygroups
    """

    sourceDestCheck: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Instance.SourceDestCheck``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-sourcedestcheck
    """

    ssmAssociations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.SsmAssociationProperty"]]]
    """``AWS::EC2::Instance.SsmAssociations``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-ssmassociations
    """

    subnetId: str
    """``AWS::EC2::Instance.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-subnetid
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::Instance.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-tags
    """

    tenancy: str
    """``AWS::EC2::Instance.Tenancy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-tenancy
    """

    userData: str
    """``AWS::EC2::Instance.UserData``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-userdata
    """

    volumes: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnInstance.VolumeProperty"]]]
    """``AWS::EC2::Instance.Volumes``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-instance.html#cfn-ec2-instance-volumes
    """

class CfnInternetGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnInternetGateway"):
    """A CloudFormation ``AWS::EC2::InternetGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html
    cloudformationResource:
        AWS::EC2::InternetGateway
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::InternetGateway``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            tags: ``AWS::EC2::InternetGateway.Tags``.
        """
        props: CfnInternetGatewayProps = {}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnInternetGateway, self, [scope, id, props])

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
    @jsii.member(jsii_name="internetGatewayName")
    def internet_gateway_name(self) -> str:
        return jsii.get(self, "internetGatewayName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnInternetGatewayProps":
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


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnInternetGatewayProps", jsii_struct_bases=[])
class CfnInternetGatewayProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::InternetGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::InternetGateway.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-internetgateway.html#cfn-ec2-internetgateway-tags
    """

class CfnLaunchTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate"):
    """A CloudFormation ``AWS::EC2::LaunchTemplate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html
    cloudformationResource:
        AWS::EC2::LaunchTemplate
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, launch_template_data: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["LaunchTemplateDataProperty"]]]=None, launch_template_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::LaunchTemplate``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            launchTemplateData: ``AWS::EC2::LaunchTemplate.LaunchTemplateData``.
            launchTemplateName: ``AWS::EC2::LaunchTemplate.LaunchTemplateName``.
        """
        props: CfnLaunchTemplateProps = {}

        if launch_template_data is not None:
            props["launchTemplateData"] = launch_template_data

        if launch_template_name is not None:
            props["launchTemplateName"] = launch_template_name

        jsii.create(CfnLaunchTemplate, self, [scope, id, props])

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
    @jsii.member(jsii_name="launchTemplateDefaultVersionNumber")
    def launch_template_default_version_number(self) -> str:
        """
        cloudformationAttribute:
            DefaultVersionNumber
        """
        return jsii.get(self, "launchTemplateDefaultVersionNumber")

    @property
    @jsii.member(jsii_name="launchTemplateId")
    def launch_template_id(self) -> str:
        return jsii.get(self, "launchTemplateId")

    @property
    @jsii.member(jsii_name="launchTemplateLatestVersionNumber")
    def launch_template_latest_version_number(self) -> str:
        """
        cloudformationAttribute:
            LatestVersionNumber
        """
        return jsii.get(self, "launchTemplateLatestVersionNumber")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchTemplateProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.BlockDeviceMappingProperty", jsii_struct_bases=[])
    class BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping.html
        """
        deviceName: str
        """``CfnLaunchTemplate.BlockDeviceMappingProperty.DeviceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping.html#cfn-ec2-launchtemplate-blockdevicemapping-devicename
        """

        ebs: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.EbsProperty"]
        """``CfnLaunchTemplate.BlockDeviceMappingProperty.Ebs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs
        """

        noDevice: str
        """``CfnLaunchTemplate.BlockDeviceMappingProperty.NoDevice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping.html#cfn-ec2-launchtemplate-blockdevicemapping-nodevice
        """

        virtualName: str
        """``CfnLaunchTemplate.BlockDeviceMappingProperty.VirtualName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping.html#cfn-ec2-launchtemplate-blockdevicemapping-virtualname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CapacityReservationSpecificationProperty", jsii_struct_bases=[])
    class CapacityReservationSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-capacityreservationspecification.html
        """
        capacityReservationPreference: str
        """``CfnLaunchTemplate.CapacityReservationSpecificationProperty.CapacityReservationPreference``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-capacityreservationspecification.html#cfn-ec2-launchtemplate-launchtemplatedata-capacityreservationspecification-capacityreservationpreference
        """

        capacityReservationTarget: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CapacityReservationTargetProperty"]
        """``CfnLaunchTemplate.CapacityReservationSpecificationProperty.CapacityReservationTarget``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-capacityreservationspecification.html#cfn-ec2-launchtemplate-launchtemplatedata-capacityreservationspecification-capacityreservationtarget
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CapacityReservationTargetProperty", jsii_struct_bases=[])
    class CapacityReservationTargetProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-capacityreservationtarget.html
        """
        capacityReservationId: str
        """``CfnLaunchTemplate.CapacityReservationTargetProperty.CapacityReservationId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-capacityreservationtarget.html#cfn-ec2-launchtemplate-capacityreservationtarget-capacityreservationid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CpuOptionsProperty", jsii_struct_bases=[])
    class CpuOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-cpuoptions.html
        """
        coreCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.CpuOptionsProperty.CoreCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-cpuoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-cpuoptions-corecount
        """

        threadsPerCore: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.CpuOptionsProperty.ThreadsPerCore``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-cpuoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-cpuoptions-threadspercore
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.CreditSpecificationProperty", jsii_struct_bases=[])
    class CreditSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-creditspecification.html
        """
        cpuCredits: str
        """``CfnLaunchTemplate.CreditSpecificationProperty.CpuCredits``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-creditspecification.html#cfn-ec2-launchtemplate-launchtemplatedata-creditspecification-cpucredits
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.EbsProperty", jsii_struct_bases=[])
    class EbsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.EbsProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-deleteontermination
        """

        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.EbsProperty.Encrypted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-encrypted
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.EbsProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-iops
        """

        kmsKeyId: str
        """``CfnLaunchTemplate.EbsProperty.KmsKeyId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-kmskeyid
        """

        snapshotId: str
        """``CfnLaunchTemplate.EbsProperty.SnapshotId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-snapshotid
        """

        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.EbsProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-volumesize
        """

        volumeType: str
        """``CfnLaunchTemplate.EbsProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-blockdevicemapping-ebs.html#cfn-ec2-launchtemplate-blockdevicemapping-ebs-volumetype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.ElasticGpuSpecificationProperty", jsii_struct_bases=[])
    class ElasticGpuSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-elasticgpuspecification.html
        """
        type: str
        """``CfnLaunchTemplate.ElasticGpuSpecificationProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-elasticgpuspecification.html#cfn-ec2-launchtemplate-elasticgpuspecification-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.HibernationOptionsProperty", jsii_struct_bases=[])
    class HibernationOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-hibernationoptions.html
        """
        configured: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.HibernationOptionsProperty.Configured``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-hibernationoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-hibernationoptions-configured
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.IamInstanceProfileProperty", jsii_struct_bases=[])
    class IamInstanceProfileProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-iaminstanceprofile.html
        """
        arn: str
        """``CfnLaunchTemplate.IamInstanceProfileProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-iaminstanceprofile.html#cfn-ec2-launchtemplate-launchtemplatedata-iaminstanceprofile-arn
        """

        name: str
        """``CfnLaunchTemplate.IamInstanceProfileProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-iaminstanceprofile.html#cfn-ec2-launchtemplate-launchtemplatedata-iaminstanceprofile-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.InstanceMarketOptionsProperty", jsii_struct_bases=[])
    class InstanceMarketOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions.html
        """
        marketType: str
        """``CfnLaunchTemplate.InstanceMarketOptionsProperty.MarketType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-markettype
        """

        spotOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.SpotOptionsProperty"]
        """``CfnLaunchTemplate.InstanceMarketOptionsProperty.SpotOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.Ipv6AddProperty", jsii_struct_bases=[])
    class Ipv6AddProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-ipv6add.html
        """
        ipv6Address: str
        """``CfnLaunchTemplate.Ipv6AddProperty.Ipv6Address``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-ipv6add.html#cfn-ec2-launchtemplate-ipv6add-ipv6address
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.LaunchTemplateDataProperty", jsii_struct_bases=[])
    class LaunchTemplateDataProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html
        """
        blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.BlockDeviceMappingProperty"]]]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.BlockDeviceMappings``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-blockdevicemappings
        """

        capacityReservationSpecification: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CapacityReservationSpecificationProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.CapacityReservationSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-capacityreservationspecification
        """

        cpuOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CpuOptionsProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.CpuOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-cpuoptions
        """

        creditSpecification: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.CreditSpecificationProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.CreditSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-creditspecification
        """

        disableApiTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.DisableApiTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-disableapitermination
        """

        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.EbsOptimized``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-ebsoptimized
        """

        elasticGpuSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.ElasticGpuSpecificationProperty"]]]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.ElasticGpuSpecifications``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-elasticgpuspecifications
        """

        elasticInferenceAccelerators: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.LaunchTemplateElasticInferenceAcceleratorProperty"]]]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.ElasticInferenceAccelerators``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-elasticinferenceaccelerators
        """

        hibernationOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.HibernationOptionsProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.HibernationOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-hibernationoptions
        """

        iamInstanceProfile: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.IamInstanceProfileProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.IamInstanceProfile``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-iaminstanceprofile
        """

        imageId: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.ImageId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-imageid
        """

        instanceInitiatedShutdownBehavior: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.InstanceInitiatedShutdownBehavior``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-instanceinitiatedshutdownbehavior
        """

        instanceMarketOptions: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.InstanceMarketOptionsProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.InstanceMarketOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-instancemarketoptions
        """

        instanceType: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-instancetype
        """

        kernelId: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.KernelId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-kernelid
        """

        keyName: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.KeyName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-keyname
        """

        licenseSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.LicenseSpecificationProperty"]]]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.LicenseSpecifications``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-licensespecifications
        """

        monitoring: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.MonitoringProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.Monitoring``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-monitoring
        """

        networkInterfaces: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.NetworkInterfaceProperty"]]]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.NetworkInterfaces``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-networkinterfaces
        """

        placement: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.PlacementProperty"]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.Placement``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-placement
        """

        ramDiskId: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.RamDiskId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-ramdiskid
        """

        securityGroupIds: typing.List[str]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.SecurityGroupIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-securitygroupids
        """

        securityGroups: typing.List[str]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.SecurityGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-securitygroups
        """

        tagSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.TagSpecificationProperty"]]]
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.TagSpecifications``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-tagspecifications
        """

        userData: str
        """``CfnLaunchTemplate.LaunchTemplateDataProperty.UserData``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata.html#cfn-ec2-launchtemplate-launchtemplatedata-userdata
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.LaunchTemplateElasticInferenceAcceleratorProperty", jsii_struct_bases=[])
    class LaunchTemplateElasticInferenceAcceleratorProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplateelasticinferenceaccelerator.html
        """
        type: str
        """``CfnLaunchTemplate.LaunchTemplateElasticInferenceAcceleratorProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplateelasticinferenceaccelerator.html#cfn-ec2-launchtemplate-launchtemplateelasticinferenceaccelerator-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.LicenseSpecificationProperty", jsii_struct_bases=[])
    class LicenseSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-licensespecification.html
        """
        licenseConfigurationArn: str
        """``CfnLaunchTemplate.LicenseSpecificationProperty.LicenseConfigurationArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-licensespecification.html#cfn-ec2-launchtemplate-licensespecification-licenseconfigurationarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.MonitoringProperty", jsii_struct_bases=[])
    class MonitoringProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-monitoring.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.MonitoringProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-monitoring.html#cfn-ec2-launchtemplate-launchtemplatedata-monitoring-enabled
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.NetworkInterfaceProperty", jsii_struct_bases=[])
    class NetworkInterfaceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html
        """
        associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.AssociatePublicIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-associatepublicipaddress
        """

        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-deleteontermination
        """

        description: str
        """``CfnLaunchTemplate.NetworkInterfaceProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-description
        """

        deviceIndex: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.DeviceIndex``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-deviceindex
        """

        groups: typing.List[str]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.Groups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-groups
        """

        ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.Ipv6AddressCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-ipv6addresscount
        """

        ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.Ipv6AddProperty"]]]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.Ipv6Addresses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-ipv6addresses
        """

        networkInterfaceId: str
        """``CfnLaunchTemplate.NetworkInterfaceProperty.NetworkInterfaceId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-networkinterfaceid
        """

        privateIpAddress: str
        """``CfnLaunchTemplate.NetworkInterfaceProperty.PrivateIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-privateipaddress
        """

        privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.PrivateIpAddProperty"]]]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.PrivateIpAddresses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-privateipaddresses
        """

        secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.NetworkInterfaceProperty.SecondaryPrivateIpAddressCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-secondaryprivateipaddresscount
        """

        subnetId: str
        """``CfnLaunchTemplate.NetworkInterfaceProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-networkinterface.html#cfn-ec2-launchtemplate-networkinterface-subnetid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.PlacementProperty", jsii_struct_bases=[])
    class PlacementProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-placement.html
        """
        affinity: str
        """``CfnLaunchTemplate.PlacementProperty.Affinity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-placement.html#cfn-ec2-launchtemplate-launchtemplatedata-placement-affinity
        """

        availabilityZone: str
        """``CfnLaunchTemplate.PlacementProperty.AvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-placement.html#cfn-ec2-launchtemplate-launchtemplatedata-placement-availabilityzone
        """

        groupName: str
        """``CfnLaunchTemplate.PlacementProperty.GroupName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-placement.html#cfn-ec2-launchtemplate-launchtemplatedata-placement-groupname
        """

        hostId: str
        """``CfnLaunchTemplate.PlacementProperty.HostId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-placement.html#cfn-ec2-launchtemplate-launchtemplatedata-placement-hostid
        """

        tenancy: str
        """``CfnLaunchTemplate.PlacementProperty.Tenancy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-placement.html#cfn-ec2-launchtemplate-launchtemplatedata-placement-tenancy
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.PrivateIpAddProperty", jsii_struct_bases=[])
    class PrivateIpAddProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-privateipadd.html
        """
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchTemplate.PrivateIpAddProperty.Primary``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-privateipadd.html#cfn-ec2-launchtemplate-privateipadd-primary
        """

        privateIpAddress: str
        """``CfnLaunchTemplate.PrivateIpAddProperty.PrivateIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-privateipadd.html#cfn-ec2-launchtemplate-privateipadd-privateipaddress
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.SpotOptionsProperty", jsii_struct_bases=[])
    class SpotOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions.html
        """
        instanceInterruptionBehavior: str
        """``CfnLaunchTemplate.SpotOptionsProperty.InstanceInterruptionBehavior``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions-instanceinterruptionbehavior
        """

        maxPrice: str
        """``CfnLaunchTemplate.SpotOptionsProperty.MaxPrice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions-maxprice
        """

        spotInstanceType: str
        """``CfnLaunchTemplate.SpotOptionsProperty.SpotInstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions.html#cfn-ec2-launchtemplate-launchtemplatedata-instancemarketoptions-spotoptions-spotinstancetype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplate.TagSpecificationProperty", jsii_struct_bases=[])
    class TagSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-tagspecification.html
        """
        resourceType: str
        """``CfnLaunchTemplate.TagSpecificationProperty.ResourceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-tagspecification.html#cfn-ec2-launchtemplate-tagspecification-resourcetype
        """

        tags: typing.List[aws_cdk.cdk.CfnTag]
        """``CfnLaunchTemplate.TagSpecificationProperty.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-launchtemplate-tagspecification.html#cfn-ec2-launchtemplate-tagspecification-tags
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnLaunchTemplateProps", jsii_struct_bases=[])
class CfnLaunchTemplateProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::LaunchTemplate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html
    """
    launchTemplateData: typing.Union[aws_cdk.cdk.Token, "CfnLaunchTemplate.LaunchTemplateDataProperty"]
    """``AWS::EC2::LaunchTemplate.LaunchTemplateData``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html#cfn-ec2-launchtemplate-launchtemplatedata
    """

    launchTemplateName: str
    """``AWS::EC2::LaunchTemplate.LaunchTemplateName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-launchtemplate.html#cfn-ec2-launchtemplate-launchtemplatename
    """

class CfnNatGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNatGateway"):
    """A CloudFormation ``AWS::EC2::NatGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html
    cloudformationResource:
        AWS::EC2::NatGateway
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, allocation_id: str, subnet_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::NatGateway``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            allocationId: ``AWS::EC2::NatGateway.AllocationId``.
            subnetId: ``AWS::EC2::NatGateway.SubnetId``.
            tags: ``AWS::EC2::NatGateway.Tags``.
        """
        props: CfnNatGatewayProps = {"allocationId": allocation_id, "subnetId": subnet_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnNatGateway, self, [scope, id, props])

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
    @jsii.member(jsii_name="natGatewayId")
    def nat_gateway_id(self) -> str:
        return jsii.get(self, "natGatewayId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNatGatewayProps":
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
class _CfnNatGatewayProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::NatGateway.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html#cfn-ec2-natgateway-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNatGatewayProps", jsii_struct_bases=[_CfnNatGatewayProps])
class CfnNatGatewayProps(_CfnNatGatewayProps):
    """Properties for defining a ``AWS::EC2::NatGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html
    """
    allocationId: str
    """``AWS::EC2::NatGateway.AllocationId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html#cfn-ec2-natgateway-allocationid
    """

    subnetId: str
    """``AWS::EC2::NatGateway.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-natgateway.html#cfn-ec2-natgateway-subnetid
    """

class CfnNetworkAcl(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkAcl"):
    """A CloudFormation ``AWS::EC2::NetworkAcl``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl.html
    cloudformationResource:
        AWS::EC2::NetworkAcl
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::NetworkAcl``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            vpcId: ``AWS::EC2::NetworkAcl.VpcId``.
            tags: ``AWS::EC2::NetworkAcl.Tags``.
        """
        props: CfnNetworkAclProps = {"vpcId": vpc_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnNetworkAcl, self, [scope, id, props])

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
    @jsii.member(jsii_name="networkAclName")
    def network_acl_name(self) -> str:
        return jsii.get(self, "networkAclName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkAclProps":
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


class CfnNetworkAclEntry(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntry"):
    """A CloudFormation ``AWS::EC2::NetworkAclEntry``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html
    cloudformationResource:
        AWS::EC2::NetworkAclEntry
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_acl_id: str, protocol: typing.Union[jsii.Number, aws_cdk.cdk.Token], rule_action: str, rule_number: typing.Union[jsii.Number, aws_cdk.cdk.Token], cidr_block: typing.Optional[str]=None, egress: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, icmp: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["IcmpProperty"]]]=None, ipv6_cidr_block: typing.Optional[str]=None, port_range: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["PortRangeProperty"]]]=None) -> None:
        """Create a new ``AWS::EC2::NetworkAclEntry``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            networkAclId: ``AWS::EC2::NetworkAclEntry.NetworkAclId``.
            protocol: ``AWS::EC2::NetworkAclEntry.Protocol``.
            ruleAction: ``AWS::EC2::NetworkAclEntry.RuleAction``.
            ruleNumber: ``AWS::EC2::NetworkAclEntry.RuleNumber``.
            cidrBlock: ``AWS::EC2::NetworkAclEntry.CidrBlock``.
            egress: ``AWS::EC2::NetworkAclEntry.Egress``.
            icmp: ``AWS::EC2::NetworkAclEntry.Icmp``.
            ipv6CidrBlock: ``AWS::EC2::NetworkAclEntry.Ipv6CidrBlock``.
            portRange: ``AWS::EC2::NetworkAclEntry.PortRange``.
        """
        props: CfnNetworkAclEntryProps = {"networkAclId": network_acl_id, "protocol": protocol, "ruleAction": rule_action, "ruleNumber": rule_number}

        if cidr_block is not None:
            props["cidrBlock"] = cidr_block

        if egress is not None:
            props["egress"] = egress

        if icmp is not None:
            props["icmp"] = icmp

        if ipv6_cidr_block is not None:
            props["ipv6CidrBlock"] = ipv6_cidr_block

        if port_range is not None:
            props["portRange"] = port_range

        jsii.create(CfnNetworkAclEntry, self, [scope, id, props])

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
    @jsii.member(jsii_name="networkAclEntryName")
    def network_acl_entry_name(self) -> str:
        return jsii.get(self, "networkAclEntryName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkAclEntryProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntry.IcmpProperty", jsii_struct_bases=[])
    class IcmpProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkaclentry-icmp.html
        """
        code: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnNetworkAclEntry.IcmpProperty.Code``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkaclentry-icmp.html#cfn-ec2-networkaclentry-icmp-code
        """

        type: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnNetworkAclEntry.IcmpProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkaclentry-icmp.html#cfn-ec2-networkaclentry-icmp-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntry.PortRangeProperty", jsii_struct_bases=[])
    class PortRangeProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkaclentry-portrange.html
        """
        from_: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnNetworkAclEntry.PortRangeProperty.From``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkaclentry-portrange.html#cfn-ec2-networkaclentry-portrange-from
        """

        to: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnNetworkAclEntry.PortRangeProperty.To``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkaclentry-portrange.html#cfn-ec2-networkaclentry-portrange-to
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnNetworkAclEntryProps(jsii.compat.TypedDict, total=False):
    cidrBlock: str
    """``AWS::EC2::NetworkAclEntry.CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-cidrblock
    """
    egress: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkAclEntry.Egress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-egress
    """
    icmp: typing.Union[aws_cdk.cdk.Token, "CfnNetworkAclEntry.IcmpProperty"]
    """``AWS::EC2::NetworkAclEntry.Icmp``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-icmp
    """
    ipv6CidrBlock: str
    """``AWS::EC2::NetworkAclEntry.Ipv6CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-ipv6cidrblock
    """
    portRange: typing.Union[aws_cdk.cdk.Token, "CfnNetworkAclEntry.PortRangeProperty"]
    """``AWS::EC2::NetworkAclEntry.PortRange``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-portrange
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclEntryProps", jsii_struct_bases=[_CfnNetworkAclEntryProps])
class CfnNetworkAclEntryProps(_CfnNetworkAclEntryProps):
    """Properties for defining a ``AWS::EC2::NetworkAclEntry``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html
    """
    networkAclId: str
    """``AWS::EC2::NetworkAclEntry.NetworkAclId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-networkaclid
    """

    protocol: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkAclEntry.Protocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-protocol
    """

    ruleAction: str
    """``AWS::EC2::NetworkAclEntry.RuleAction``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-ruleaction
    """

    ruleNumber: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkAclEntry.RuleNumber``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl-entry.html#cfn-ec2-networkaclentry-rulenumber
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnNetworkAclProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::NetworkAcl.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl.html#cfn-ec2-networkacl-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkAclProps", jsii_struct_bases=[_CfnNetworkAclProps])
class CfnNetworkAclProps(_CfnNetworkAclProps):
    """Properties for defining a ``AWS::EC2::NetworkAcl``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl.html
    """
    vpcId: str
    """``AWS::EC2::NetworkAcl.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-acl.html#cfn-ec2-networkacl-vpcid
    """

class CfnNetworkInterface(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterface"):
    """A CloudFormation ``AWS::EC2::NetworkInterface``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html
    cloudformationResource:
        AWS::EC2::NetworkInterface
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subnet_id: str, description: typing.Optional[str]=None, group_set: typing.Optional[typing.List[str]]=None, interface_type: typing.Optional[str]=None, ipv6_address_count: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, ipv6_addresses: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["InstanceIpv6AddressProperty"]]]=None, private_ip_address: typing.Optional[str]=None, private_ip_addresses: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "PrivateIpAddressSpecificationProperty"]]]]]=None, secondary_private_ip_address_count: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, source_dest_check: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::NetworkInterface``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            subnetId: ``AWS::EC2::NetworkInterface.SubnetId``.
            description: ``AWS::EC2::NetworkInterface.Description``.
            groupSet: ``AWS::EC2::NetworkInterface.GroupSet``.
            interfaceType: ``AWS::EC2::NetworkInterface.InterfaceType``.
            ipv6AddressCount: ``AWS::EC2::NetworkInterface.Ipv6AddressCount``.
            ipv6Addresses: ``AWS::EC2::NetworkInterface.Ipv6Addresses``.
            privateIpAddress: ``AWS::EC2::NetworkInterface.PrivateIpAddress``.
            privateIpAddresses: ``AWS::EC2::NetworkInterface.PrivateIpAddresses``.
            secondaryPrivateIpAddressCount: ``AWS::EC2::NetworkInterface.SecondaryPrivateIpAddressCount``.
            sourceDestCheck: ``AWS::EC2::NetworkInterface.SourceDestCheck``.
            tags: ``AWS::EC2::NetworkInterface.Tags``.
        """
        props: CfnNetworkInterfaceProps = {"subnetId": subnet_id}

        if description is not None:
            props["description"] = description

        if group_set is not None:
            props["groupSet"] = group_set

        if interface_type is not None:
            props["interfaceType"] = interface_type

        if ipv6_address_count is not None:
            props["ipv6AddressCount"] = ipv6_address_count

        if ipv6_addresses is not None:
            props["ipv6Addresses"] = ipv6_addresses

        if private_ip_address is not None:
            props["privateIpAddress"] = private_ip_address

        if private_ip_addresses is not None:
            props["privateIpAddresses"] = private_ip_addresses

        if secondary_private_ip_address_count is not None:
            props["secondaryPrivateIpAddressCount"] = secondary_private_ip_address_count

        if source_dest_check is not None:
            props["sourceDestCheck"] = source_dest_check

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnNetworkInterface, self, [scope, id, props])

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
    @jsii.member(jsii_name="networkInterfaceName")
    def network_interface_name(self) -> str:
        return jsii.get(self, "networkInterfaceName")

    @property
    @jsii.member(jsii_name="networkInterfacePrimaryPrivateIpAddress")
    def network_interface_primary_private_ip_address(self) -> str:
        """
        cloudformationAttribute:
            PrimaryPrivateIpAddress
        """
        return jsii.get(self, "networkInterfacePrimaryPrivateIpAddress")

    @property
    @jsii.member(jsii_name="networkInterfaceSecondaryPrivateIpAddresses")
    def network_interface_secondary_private_ip_addresses(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            SecondaryPrivateIpAddresses
        """
        return jsii.get(self, "networkInterfaceSecondaryPrivateIpAddresses")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkInterfaceProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterface.InstanceIpv6AddressProperty", jsii_struct_bases=[])
    class InstanceIpv6AddressProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkinterface-instanceipv6address.html
        """
        ipv6Address: str
        """``CfnNetworkInterface.InstanceIpv6AddressProperty.Ipv6Address``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-networkinterface-instanceipv6address.html#cfn-ec2-networkinterface-instanceipv6address-ipv6address
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterface.PrivateIpAddressSpecificationProperty", jsii_struct_bases=[])
    class PrivateIpAddressSpecificationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-interface-privateipspec.html
        """
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnNetworkInterface.PrivateIpAddressSpecificationProperty.Primary``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-interface-privateipspec.html#cfn-ec2-networkinterface-privateipspecification-primary
        """

        privateIpAddress: str
        """``CfnNetworkInterface.PrivateIpAddressSpecificationProperty.PrivateIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-network-interface-privateipspec.html#cfn-ec2-networkinterface-privateipspecification-privateipaddress
        """


class CfnNetworkInterfaceAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfaceAttachment"):
    """A CloudFormation ``AWS::EC2::NetworkInterfaceAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html
    cloudformationResource:
        AWS::EC2::NetworkInterfaceAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, device_index: str, instance_id: str, network_interface_id: str, delete_on_termination: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::EC2::NetworkInterfaceAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            deviceIndex: ``AWS::EC2::NetworkInterfaceAttachment.DeviceIndex``.
            instanceId: ``AWS::EC2::NetworkInterfaceAttachment.InstanceId``.
            networkInterfaceId: ``AWS::EC2::NetworkInterfaceAttachment.NetworkInterfaceId``.
            deleteOnTermination: ``AWS::EC2::NetworkInterfaceAttachment.DeleteOnTermination``.
        """
        props: CfnNetworkInterfaceAttachmentProps = {"deviceIndex": device_index, "instanceId": instance_id, "networkInterfaceId": network_interface_id}

        if delete_on_termination is not None:
            props["deleteOnTermination"] = delete_on_termination

        jsii.create(CfnNetworkInterfaceAttachment, self, [scope, id, props])

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
    @jsii.member(jsii_name="networkInterfaceAttachmentName")
    def network_interface_attachment_name(self) -> str:
        return jsii.get(self, "networkInterfaceAttachmentName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkInterfaceAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnNetworkInterfaceAttachmentProps(jsii.compat.TypedDict, total=False):
    deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkInterfaceAttachment.DeleteOnTermination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html#cfn-ec2-network-interface-attachment-deleteonterm
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfaceAttachmentProps", jsii_struct_bases=[_CfnNetworkInterfaceAttachmentProps])
class CfnNetworkInterfaceAttachmentProps(_CfnNetworkInterfaceAttachmentProps):
    """Properties for defining a ``AWS::EC2::NetworkInterfaceAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html
    """
    deviceIndex: str
    """``AWS::EC2::NetworkInterfaceAttachment.DeviceIndex``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html#cfn-ec2-network-interface-attachment-deviceindex
    """

    instanceId: str
    """``AWS::EC2::NetworkInterfaceAttachment.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html#cfn-ec2-network-interface-attachment-instanceid
    """

    networkInterfaceId: str
    """``AWS::EC2::NetworkInterfaceAttachment.NetworkInterfaceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface-attachment.html#cfn-ec2-network-interface-attachment-networkinterfaceid
    """

class CfnNetworkInterfacePermission(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfacePermission"):
    """A CloudFormation ``AWS::EC2::NetworkInterfacePermission``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html
    cloudformationResource:
        AWS::EC2::NetworkInterfacePermission
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, aws_account_id: str, network_interface_id: str, permission: str) -> None:
        """Create a new ``AWS::EC2::NetworkInterfacePermission``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            awsAccountId: ``AWS::EC2::NetworkInterfacePermission.AwsAccountId``.
            networkInterfaceId: ``AWS::EC2::NetworkInterfacePermission.NetworkInterfaceId``.
            permission: ``AWS::EC2::NetworkInterfacePermission.Permission``.
        """
        props: CfnNetworkInterfacePermissionProps = {"awsAccountId": aws_account_id, "networkInterfaceId": network_interface_id, "permission": permission}

        jsii.create(CfnNetworkInterfacePermission, self, [scope, id, props])

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
    @jsii.member(jsii_name="networkInterfacePermissionId")
    def network_interface_permission_id(self) -> str:
        return jsii.get(self, "networkInterfacePermissionId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnNetworkInterfacePermissionProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfacePermissionProps", jsii_struct_bases=[])
class CfnNetworkInterfacePermissionProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::NetworkInterfacePermission``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html
    """
    awsAccountId: str
    """``AWS::EC2::NetworkInterfacePermission.AwsAccountId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html#cfn-ec2-networkinterfacepermission-awsaccountid
    """

    networkInterfaceId: str
    """``AWS::EC2::NetworkInterfacePermission.NetworkInterfaceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html#cfn-ec2-networkinterfacepermission-networkinterfaceid
    """

    permission: str
    """``AWS::EC2::NetworkInterfacePermission.Permission``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-networkinterfacepermission.html#cfn-ec2-networkinterfacepermission-permission
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnNetworkInterfaceProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::EC2::NetworkInterface.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-description
    """
    groupSet: typing.List[str]
    """``AWS::EC2::NetworkInterface.GroupSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-groupset
    """
    interfaceType: str
    """``AWS::EC2::NetworkInterface.InterfaceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-ec2-networkinterface-interfacetype
    """
    ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkInterface.Ipv6AddressCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-ec2-networkinterface-ipv6addresscount
    """
    ipv6Addresses: typing.Union[aws_cdk.cdk.Token, "CfnNetworkInterface.InstanceIpv6AddressProperty"]
    """``AWS::EC2::NetworkInterface.Ipv6Addresses``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-ec2-networkinterface-ipv6addresses
    """
    privateIpAddress: str
    """``AWS::EC2::NetworkInterface.PrivateIpAddress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-privateipaddress
    """
    privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnNetworkInterface.PrivateIpAddressSpecificationProperty"]]]
    """``AWS::EC2::NetworkInterface.PrivateIpAddresses``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-privateipaddresses
    """
    secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkInterface.SecondaryPrivateIpAddressCount``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-secondaryprivateipcount
    """
    sourceDestCheck: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::NetworkInterface.SourceDestCheck``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-sourcedestcheck
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::NetworkInterface.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnNetworkInterfaceProps", jsii_struct_bases=[_CfnNetworkInterfaceProps])
class CfnNetworkInterfaceProps(_CfnNetworkInterfaceProps):
    """Properties for defining a ``AWS::EC2::NetworkInterface``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html
    """
    subnetId: str
    """``AWS::EC2::NetworkInterface.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-network-interface.html#cfn-awsec2networkinterface-subnetid
    """

class CfnPlacementGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnPlacementGroup"):
    """A CloudFormation ``AWS::EC2::PlacementGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-placementgroup.html
    cloudformationResource:
        AWS::EC2::PlacementGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, strategy: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::PlacementGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            strategy: ``AWS::EC2::PlacementGroup.Strategy``.
        """
        props: CfnPlacementGroupProps = {}

        if strategy is not None:
            props["strategy"] = strategy

        jsii.create(CfnPlacementGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="placementGroupName")
    def placement_group_name(self) -> str:
        return jsii.get(self, "placementGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPlacementGroupProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnPlacementGroupProps", jsii_struct_bases=[])
class CfnPlacementGroupProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::PlacementGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-placementgroup.html
    """
    strategy: str
    """``AWS::EC2::PlacementGroup.Strategy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-placementgroup.html#cfn-ec2-placementgroup-strategy
    """

class CfnRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnRoute"):
    """A CloudFormation ``AWS::EC2::Route``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html
    cloudformationResource:
        AWS::EC2::Route
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, route_table_id: str, destination_cidr_block: typing.Optional[str]=None, destination_ipv6_cidr_block: typing.Optional[str]=None, egress_only_internet_gateway_id: typing.Optional[str]=None, gateway_id: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, nat_gateway_id: typing.Optional[str]=None, network_interface_id: typing.Optional[str]=None, vpc_peering_connection_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::Route``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            routeTableId: ``AWS::EC2::Route.RouteTableId``.
            destinationCidrBlock: ``AWS::EC2::Route.DestinationCidrBlock``.
            destinationIpv6CidrBlock: ``AWS::EC2::Route.DestinationIpv6CidrBlock``.
            egressOnlyInternetGatewayId: ``AWS::EC2::Route.EgressOnlyInternetGatewayId``.
            gatewayId: ``AWS::EC2::Route.GatewayId``.
            instanceId: ``AWS::EC2::Route.InstanceId``.
            natGatewayId: ``AWS::EC2::Route.NatGatewayId``.
            networkInterfaceId: ``AWS::EC2::Route.NetworkInterfaceId``.
            vpcPeeringConnectionId: ``AWS::EC2::Route.VpcPeeringConnectionId``.
        """
        props: CfnRouteProps = {"routeTableId": route_table_id}

        if destination_cidr_block is not None:
            props["destinationCidrBlock"] = destination_cidr_block

        if destination_ipv6_cidr_block is not None:
            props["destinationIpv6CidrBlock"] = destination_ipv6_cidr_block

        if egress_only_internet_gateway_id is not None:
            props["egressOnlyInternetGatewayId"] = egress_only_internet_gateway_id

        if gateway_id is not None:
            props["gatewayId"] = gateway_id

        if instance_id is not None:
            props["instanceId"] = instance_id

        if nat_gateway_id is not None:
            props["natGatewayId"] = nat_gateway_id

        if network_interface_id is not None:
            props["networkInterfaceId"] = network_interface_id

        if vpc_peering_connection_id is not None:
            props["vpcPeeringConnectionId"] = vpc_peering_connection_id

        jsii.create(CfnRoute, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeName")
    def route_name(self) -> str:
        return jsii.get(self, "routeName")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRouteProps(jsii.compat.TypedDict, total=False):
    destinationCidrBlock: str
    """``AWS::EC2::Route.DestinationCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-destinationcidrblock
    """
    destinationIpv6CidrBlock: str
    """``AWS::EC2::Route.DestinationIpv6CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-destinationipv6cidrblock
    """
    egressOnlyInternetGatewayId: str
    """``AWS::EC2::Route.EgressOnlyInternetGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-egressonlyinternetgatewayid
    """
    gatewayId: str
    """``AWS::EC2::Route.GatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-gatewayid
    """
    instanceId: str
    """``AWS::EC2::Route.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-instanceid
    """
    natGatewayId: str
    """``AWS::EC2::Route.NatGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-natgatewayid
    """
    networkInterfaceId: str
    """``AWS::EC2::Route.NetworkInterfaceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-networkinterfaceid
    """
    vpcPeeringConnectionId: str
    """``AWS::EC2::Route.VpcPeeringConnectionId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-vpcpeeringconnectionid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnRouteProps", jsii_struct_bases=[_CfnRouteProps])
class CfnRouteProps(_CfnRouteProps):
    """Properties for defining a ``AWS::EC2::Route``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html
    """
    routeTableId: str
    """``AWS::EC2::Route.RouteTableId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route.html#cfn-ec2-route-routetableid
    """

class CfnRouteTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnRouteTable"):
    """A CloudFormation ``AWS::EC2::RouteTable``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html
    cloudformationResource:
        AWS::EC2::RouteTable
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::RouteTable``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            vpcId: ``AWS::EC2::RouteTable.VpcId``.
            tags: ``AWS::EC2::RouteTable.Tags``.
        """
        props: CfnRouteTableProps = {"vpcId": vpc_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnRouteTable, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRouteTableProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> str:
        return jsii.get(self, "routeTableId")

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
class _CfnRouteTableProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::RouteTable.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html#cfn-ec2-routetable-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnRouteTableProps", jsii_struct_bases=[_CfnRouteTableProps])
class CfnRouteTableProps(_CfnRouteTableProps):
    """Properties for defining a ``AWS::EC2::RouteTable``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html
    """
    vpcId: str
    """``AWS::EC2::RouteTable.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-route-table.html#cfn-ec2-routetable-vpcid
    """

class CfnSecurityGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroup"):
    """A CloudFormation ``AWS::EC2::SecurityGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html
    cloudformationResource:
        AWS::EC2::SecurityGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_description: str, group_name: typing.Optional[str]=None, security_group_egress: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "EgressProperty"]]]]]=None, security_group_ingress: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "IngressProperty"]]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::SecurityGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            groupDescription: ``AWS::EC2::SecurityGroup.GroupDescription``.
            groupName: ``AWS::EC2::SecurityGroup.GroupName``.
            securityGroupEgress: ``AWS::EC2::SecurityGroup.SecurityGroupEgress``.
            securityGroupIngress: ``AWS::EC2::SecurityGroup.SecurityGroupIngress``.
            tags: ``AWS::EC2::SecurityGroup.Tags``.
            vpcId: ``AWS::EC2::SecurityGroup.VpcId``.
        """
        props: CfnSecurityGroupProps = {"groupDescription": group_description}

        if group_name is not None:
            props["groupName"] = group_name

        if security_group_egress is not None:
            props["securityGroupEgress"] = security_group_egress

        if security_group_ingress is not None:
            props["securityGroupIngress"] = security_group_ingress

        if tags is not None:
            props["tags"] = tags

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(CfnSecurityGroup, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSecurityGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """
        cloudformationAttribute:
            GroupId
        """
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> str:
        return jsii.get(self, "securityGroupName")

    @property
    @jsii.member(jsii_name="securityGroupVpcId")
    def security_group_vpc_id(self) -> str:
        """
        cloudformationAttribute:
            VpcId
        """
        return jsii.get(self, "securityGroupVpcId")

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
    class _EgressProperty(jsii.compat.TypedDict, total=False):
        cidrIp: str
        """``CfnSecurityGroup.EgressProperty.CidrIp``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-cidrip
        """
        cidrIpv6: str
        """``CfnSecurityGroup.EgressProperty.CidrIpv6``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-cidripv6
        """
        description: str
        """``CfnSecurityGroup.EgressProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-description
        """
        destinationPrefixListId: str
        """``CfnSecurityGroup.EgressProperty.DestinationPrefixListId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-destinationprefixlistid
        """
        destinationSecurityGroupId: str
        """``CfnSecurityGroup.EgressProperty.DestinationSecurityGroupId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-destsecgroupid
        """
        fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSecurityGroup.EgressProperty.FromPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-fromport
        """
        toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSecurityGroup.EgressProperty.ToPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-toport
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroup.EgressProperty", jsii_struct_bases=[_EgressProperty])
    class EgressProperty(_EgressProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html
        """
        ipProtocol: str
        """``CfnSecurityGroup.EgressProperty.IpProtocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-ipprotocol
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _IngressProperty(jsii.compat.TypedDict, total=False):
        cidrIp: str
        """``CfnSecurityGroup.IngressProperty.CidrIp``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-cidrip
        """
        cidrIpv6: str
        """``CfnSecurityGroup.IngressProperty.CidrIpv6``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-cidripv6
        """
        description: str
        """``CfnSecurityGroup.IngressProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-description
        """
        fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSecurityGroup.IngressProperty.FromPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-fromport
        """
        sourcePrefixListId: str
        """``CfnSecurityGroup.IngressProperty.SourcePrefixListId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-securitygroup-ingress-sourceprefixlistid
        """
        sourceSecurityGroupId: str
        """``CfnSecurityGroup.IngressProperty.SourceSecurityGroupId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-sourcesecuritygroupid
        """
        sourceSecurityGroupName: str
        """``CfnSecurityGroup.IngressProperty.SourceSecurityGroupName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-sourcesecuritygroupname
        """
        sourceSecurityGroupOwnerId: str
        """``CfnSecurityGroup.IngressProperty.SourceSecurityGroupOwnerId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-sourcesecuritygroupownerid
        """
        toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSecurityGroup.IngressProperty.ToPort``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-toport
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroup.IngressProperty", jsii_struct_bases=[_IngressProperty])
    class IngressProperty(_IngressProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html
        """
        ipProtocol: str
        """``CfnSecurityGroup.IngressProperty.IpProtocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-rule.html#cfn-ec2-security-group-rule-ipprotocol
        """


class CfnSecurityGroupEgress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupEgress"):
    """A CloudFormation ``AWS::EC2::SecurityGroupEgress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html
    cloudformationResource:
        AWS::EC2::SecurityGroupEgress
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, group_id: str, ip_protocol: str, cidr_ip: typing.Optional[str]=None, cidr_ipv6: typing.Optional[str]=None, description: typing.Optional[str]=None, destination_prefix_list_id: typing.Optional[str]=None, destination_security_group_id: typing.Optional[str]=None, from_port: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, to_port: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::EC2::SecurityGroupEgress``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            groupId: ``AWS::EC2::SecurityGroupEgress.GroupId``.
            ipProtocol: ``AWS::EC2::SecurityGroupEgress.IpProtocol``.
            cidrIp: ``AWS::EC2::SecurityGroupEgress.CidrIp``.
            cidrIpv6: ``AWS::EC2::SecurityGroupEgress.CidrIpv6``.
            description: ``AWS::EC2::SecurityGroupEgress.Description``.
            destinationPrefixListId: ``AWS::EC2::SecurityGroupEgress.DestinationPrefixListId``.
            destinationSecurityGroupId: ``AWS::EC2::SecurityGroupEgress.DestinationSecurityGroupId``.
            fromPort: ``AWS::EC2::SecurityGroupEgress.FromPort``.
            toPort: ``AWS::EC2::SecurityGroupEgress.ToPort``.
        """
        props: CfnSecurityGroupEgressProps = {"groupId": group_id, "ipProtocol": ip_protocol}

        if cidr_ip is not None:
            props["cidrIp"] = cidr_ip

        if cidr_ipv6 is not None:
            props["cidrIpv6"] = cidr_ipv6

        if description is not None:
            props["description"] = description

        if destination_prefix_list_id is not None:
            props["destinationPrefixListId"] = destination_prefix_list_id

        if destination_security_group_id is not None:
            props["destinationSecurityGroupId"] = destination_security_group_id

        if from_port is not None:
            props["fromPort"] = from_port

        if to_port is not None:
            props["toPort"] = to_port

        jsii.create(CfnSecurityGroupEgress, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSecurityGroupEgressProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityGroupEgressId")
    def security_group_egress_id(self) -> str:
        return jsii.get(self, "securityGroupEgressId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSecurityGroupEgressProps(jsii.compat.TypedDict, total=False):
    cidrIp: str
    """``AWS::EC2::SecurityGroupEgress.CidrIp``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-cidrip
    """
    cidrIpv6: str
    """``AWS::EC2::SecurityGroupEgress.CidrIpv6``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-cidripv6
    """
    description: str
    """``AWS::EC2::SecurityGroupEgress.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-description
    """
    destinationPrefixListId: str
    """``AWS::EC2::SecurityGroupEgress.DestinationPrefixListId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-destinationprefixlistid
    """
    destinationSecurityGroupId: str
    """``AWS::EC2::SecurityGroupEgress.DestinationSecurityGroupId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-destinationsecuritygroupid
    """
    fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::SecurityGroupEgress.FromPort``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-fromport
    """
    toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::SecurityGroupEgress.ToPort``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-toport
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupEgressProps", jsii_struct_bases=[_CfnSecurityGroupEgressProps])
class CfnSecurityGroupEgressProps(_CfnSecurityGroupEgressProps):
    """Properties for defining a ``AWS::EC2::SecurityGroupEgress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html
    """
    groupId: str
    """``AWS::EC2::SecurityGroupEgress.GroupId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-groupid
    """

    ipProtocol: str
    """``AWS::EC2::SecurityGroupEgress.IpProtocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-security-group-egress.html#cfn-ec2-securitygroupegress-ipprotocol
    """

class CfnSecurityGroupIngress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupIngress"):
    """A CloudFormation ``AWS::EC2::SecurityGroupIngress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html
    cloudformationResource:
        AWS::EC2::SecurityGroupIngress
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ip_protocol: str, cidr_ip: typing.Optional[str]=None, cidr_ipv6: typing.Optional[str]=None, description: typing.Optional[str]=None, from_port: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, group_id: typing.Optional[str]=None, group_name: typing.Optional[str]=None, source_prefix_list_id: typing.Optional[str]=None, source_security_group_id: typing.Optional[str]=None, source_security_group_name: typing.Optional[str]=None, source_security_group_owner_id: typing.Optional[str]=None, to_port: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::EC2::SecurityGroupIngress``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            ipProtocol: ``AWS::EC2::SecurityGroupIngress.IpProtocol``.
            cidrIp: ``AWS::EC2::SecurityGroupIngress.CidrIp``.
            cidrIpv6: ``AWS::EC2::SecurityGroupIngress.CidrIpv6``.
            description: ``AWS::EC2::SecurityGroupIngress.Description``.
            fromPort: ``AWS::EC2::SecurityGroupIngress.FromPort``.
            groupId: ``AWS::EC2::SecurityGroupIngress.GroupId``.
            groupName: ``AWS::EC2::SecurityGroupIngress.GroupName``.
            sourcePrefixListId: ``AWS::EC2::SecurityGroupIngress.SourcePrefixListId``.
            sourceSecurityGroupId: ``AWS::EC2::SecurityGroupIngress.SourceSecurityGroupId``.
            sourceSecurityGroupName: ``AWS::EC2::SecurityGroupIngress.SourceSecurityGroupName``.
            sourceSecurityGroupOwnerId: ``AWS::EC2::SecurityGroupIngress.SourceSecurityGroupOwnerId``.
            toPort: ``AWS::EC2::SecurityGroupIngress.ToPort``.
        """
        props: CfnSecurityGroupIngressProps = {"ipProtocol": ip_protocol}

        if cidr_ip is not None:
            props["cidrIp"] = cidr_ip

        if cidr_ipv6 is not None:
            props["cidrIpv6"] = cidr_ipv6

        if description is not None:
            props["description"] = description

        if from_port is not None:
            props["fromPort"] = from_port

        if group_id is not None:
            props["groupId"] = group_id

        if group_name is not None:
            props["groupName"] = group_name

        if source_prefix_list_id is not None:
            props["sourcePrefixListId"] = source_prefix_list_id

        if source_security_group_id is not None:
            props["sourceSecurityGroupId"] = source_security_group_id

        if source_security_group_name is not None:
            props["sourceSecurityGroupName"] = source_security_group_name

        if source_security_group_owner_id is not None:
            props["sourceSecurityGroupOwnerId"] = source_security_group_owner_id

        if to_port is not None:
            props["toPort"] = to_port

        jsii.create(CfnSecurityGroupIngress, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSecurityGroupIngressProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="securityGroupIngressId")
    def security_group_ingress_id(self) -> str:
        return jsii.get(self, "securityGroupIngressId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSecurityGroupIngressProps(jsii.compat.TypedDict, total=False):
    cidrIp: str
    """``AWS::EC2::SecurityGroupIngress.CidrIp``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-cidrip
    """
    cidrIpv6: str
    """``AWS::EC2::SecurityGroupIngress.CidrIpv6``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-cidripv6
    """
    description: str
    """``AWS::EC2::SecurityGroupIngress.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-description
    """
    fromPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::SecurityGroupIngress.FromPort``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-fromport
    """
    groupId: str
    """``AWS::EC2::SecurityGroupIngress.GroupId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-groupid
    """
    groupName: str
    """``AWS::EC2::SecurityGroupIngress.GroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-groupname
    """
    sourcePrefixListId: str
    """``AWS::EC2::SecurityGroupIngress.SourcePrefixListId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-securitygroupingress-sourceprefixlistid
    """
    sourceSecurityGroupId: str
    """``AWS::EC2::SecurityGroupIngress.SourceSecurityGroupId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-sourcesecuritygroupid
    """
    sourceSecurityGroupName: str
    """``AWS::EC2::SecurityGroupIngress.SourceSecurityGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-sourcesecuritygroupname
    """
    sourceSecurityGroupOwnerId: str
    """``AWS::EC2::SecurityGroupIngress.SourceSecurityGroupOwnerId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-sourcesecuritygroupownerid
    """
    toPort: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::SecurityGroupIngress.ToPort``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-toport
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupIngressProps", jsii_struct_bases=[_CfnSecurityGroupIngressProps])
class CfnSecurityGroupIngressProps(_CfnSecurityGroupIngressProps):
    """Properties for defining a ``AWS::EC2::SecurityGroupIngress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html
    """
    ipProtocol: str
    """``AWS::EC2::SecurityGroupIngress.IpProtocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group-ingress.html#cfn-ec2-security-group-ingress-ipprotocol
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSecurityGroupProps(jsii.compat.TypedDict, total=False):
    groupName: str
    """``AWS::EC2::SecurityGroup.GroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html#cfn-ec2-securitygroup-groupname
    """
    securityGroupEgress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSecurityGroup.EgressProperty"]]]
    """``AWS::EC2::SecurityGroup.SecurityGroupEgress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html#cfn-ec2-securitygroup-securitygroupegress
    """
    securityGroupIngress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSecurityGroup.IngressProperty"]]]
    """``AWS::EC2::SecurityGroup.SecurityGroupIngress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html#cfn-ec2-securitygroup-securitygroupingress
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::SecurityGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html#cfn-ec2-securitygroup-tags
    """
    vpcId: str
    """``AWS::EC2::SecurityGroup.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html#cfn-ec2-securitygroup-vpcid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSecurityGroupProps", jsii_struct_bases=[_CfnSecurityGroupProps])
class CfnSecurityGroupProps(_CfnSecurityGroupProps):
    """Properties for defining a ``AWS::EC2::SecurityGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html
    """
    groupDescription: str
    """``AWS::EC2::SecurityGroup.GroupDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-security-group.html#cfn-ec2-securitygroup-groupdescription
    """

class CfnSpotFleet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet"):
    """A CloudFormation ``AWS::EC2::SpotFleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-spotfleet.html
    cloudformationResource:
        AWS::EC2::SpotFleet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, spot_fleet_request_config_data: typing.Union[aws_cdk.cdk.Token, "SpotFleetRequestConfigDataProperty"]) -> None:
        """Create a new ``AWS::EC2::SpotFleet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            spotFleetRequestConfigData: ``AWS::EC2::SpotFleet.SpotFleetRequestConfigData``.
        """
        props: CfnSpotFleetProps = {"spotFleetRequestConfigData": spot_fleet_request_config_data}

        jsii.create(CfnSpotFleet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSpotFleetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="spotFleetName")
    def spot_fleet_name(self) -> str:
        return jsii.get(self, "spotFleetName")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.EbsBlockDeviceProperty"]
        """``CfnSpotFleet.BlockDeviceMappingProperty.Ebs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings.html#cfn-ec2-spotfleet-blockdevicemapping-ebs
        """
        noDevice: str
        """``CfnSpotFleet.BlockDeviceMappingProperty.NoDevice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings.html#cfn-ec2-spotfleet-blockdevicemapping-nodevice
        """
        virtualName: str
        """``CfnSpotFleet.BlockDeviceMappingProperty.VirtualName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings.html#cfn-ec2-spotfleet-blockdevicemapping-virtualname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.BlockDeviceMappingProperty", jsii_struct_bases=[_BlockDeviceMappingProperty])
    class BlockDeviceMappingProperty(_BlockDeviceMappingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings.html
        """
        deviceName: str
        """``CfnSpotFleet.BlockDeviceMappingProperty.DeviceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings.html#cfn-ec2-spotfleet-blockdevicemapping-devicename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.ClassicLoadBalancerProperty", jsii_struct_bases=[])
    class ClassicLoadBalancerProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-classicloadbalancer.html
        """
        name: str
        """``CfnSpotFleet.ClassicLoadBalancerProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-classicloadbalancer.html#cfn-ec2-spotfleet-classicloadbalancer-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.ClassicLoadBalancersConfigProperty", jsii_struct_bases=[])
    class ClassicLoadBalancersConfigProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-classicloadbalancersconfig.html
        """
        classicLoadBalancers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.ClassicLoadBalancerProperty"]]]
        """``CfnSpotFleet.ClassicLoadBalancersConfigProperty.ClassicLoadBalancers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-classicloadbalancersconfig.html#cfn-ec2-spotfleet-classicloadbalancersconfig-classicloadbalancers
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.EbsBlockDeviceProperty", jsii_struct_bases=[])
    class EbsBlockDeviceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.EbsBlockDeviceProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html#cfn-ec2-spotfleet-ebsblockdevice-deleteontermination
        """

        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.EbsBlockDeviceProperty.Encrypted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html#cfn-ec2-spotfleet-ebsblockdevice-encrypted
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.EbsBlockDeviceProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html#cfn-ec2-spotfleet-ebsblockdevice-iops
        """

        snapshotId: str
        """``CfnSpotFleet.EbsBlockDeviceProperty.SnapshotId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html#cfn-ec2-spotfleet-ebsblockdevice-snapshotid
        """

        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.EbsBlockDeviceProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html#cfn-ec2-spotfleet-ebsblockdevice-volumesize
        """

        volumeType: str
        """``CfnSpotFleet.EbsBlockDeviceProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-blockdevicemappings-ebs.html#cfn-ec2-spotfleet-ebsblockdevice-volumetype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FleetLaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        """``CfnSpotFleet.FleetLaunchTemplateSpecificationProperty.LaunchTemplateId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-fleetlaunchtemplatespecification.html#cfn-ec2-spotfleet-fleetlaunchtemplatespecification-launchtemplateid
        """
        launchTemplateName: str
        """``CfnSpotFleet.FleetLaunchTemplateSpecificationProperty.LaunchTemplateName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-fleetlaunchtemplatespecification.html#cfn-ec2-spotfleet-fleetlaunchtemplatespecification-launchtemplatename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.FleetLaunchTemplateSpecificationProperty", jsii_struct_bases=[_FleetLaunchTemplateSpecificationProperty])
    class FleetLaunchTemplateSpecificationProperty(_FleetLaunchTemplateSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-fleetlaunchtemplatespecification.html
        """
        version: str
        """``CfnSpotFleet.FleetLaunchTemplateSpecificationProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-fleetlaunchtemplatespecification.html#cfn-ec2-spotfleet-fleetlaunchtemplatespecification-version
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.GroupIdentifierProperty", jsii_struct_bases=[])
    class GroupIdentifierProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-securitygroups.html
        """
        groupId: str
        """``CfnSpotFleet.GroupIdentifierProperty.GroupId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-securitygroups.html#cfn-ec2-spotfleet-groupidentifier-groupid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.IamInstanceProfileSpecificationProperty", jsii_struct_bases=[])
    class IamInstanceProfileSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-iaminstanceprofile.html
        """
        arn: str
        """``CfnSpotFleet.IamInstanceProfileSpecificationProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-iaminstanceprofile.html#cfn-ec2-spotfleet-iaminstanceprofilespecification-arn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.InstanceIpv6AddressProperty", jsii_struct_bases=[])
    class InstanceIpv6AddressProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-instanceipv6address.html
        """
        ipv6Address: str
        """``CfnSpotFleet.InstanceIpv6AddressProperty.Ipv6Address``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-instanceipv6address.html#cfn-ec2-spotfleet-instanceipv6address-ipv6address
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty", jsii_struct_bases=[])
    class InstanceNetworkInterfaceSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html
        """
        associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.AssociatePublicIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-associatepublicipaddress
        """

        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-deleteontermination
        """

        description: str
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-description
        """

        deviceIndex: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.DeviceIndex``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-deviceindex
        """

        groups: typing.List[str]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.Groups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-groups
        """

        ipv6AddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.Ipv6AddressCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-ipv6addresscount
        """

        ipv6Addresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.InstanceIpv6AddressProperty"]]]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.Ipv6Addresses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-ipv6addresses
        """

        networkInterfaceId: str
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.NetworkInterfaceId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-networkinterfaceid
        """

        privateIpAddresses: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.PrivateIpAddressSpecificationProperty"]]]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.PrivateIpAddresses``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-privateipaddresses
        """

        secondaryPrivateIpAddressCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.SecondaryPrivateIpAddressCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-secondaryprivateipaddresscount
        """

        subnetId: str
        """``CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces.html#cfn-ec2-spotfleet-instancenetworkinterfacespecification-subnetid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.LaunchTemplateConfigProperty", jsii_struct_bases=[])
    class LaunchTemplateConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateconfig.html
        """
        launchTemplateSpecification: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.FleetLaunchTemplateSpecificationProperty"]
        """``CfnSpotFleet.LaunchTemplateConfigProperty.LaunchTemplateSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateconfig.html#cfn-ec2-spotfleet-launchtemplateconfig-launchtemplatespecification
        """

        overrides: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.LaunchTemplateOverridesProperty"]]]
        """``CfnSpotFleet.LaunchTemplateConfigProperty.Overrides``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateconfig.html#cfn-ec2-spotfleet-launchtemplateconfig-overrides
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.LaunchTemplateOverridesProperty", jsii_struct_bases=[])
    class LaunchTemplateOverridesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateoverrides.html
        """
        availabilityZone: str
        """``CfnSpotFleet.LaunchTemplateOverridesProperty.AvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateoverrides.html#cfn-ec2-spotfleet-launchtemplateoverrides-availabilityzone
        """

        instanceType: str
        """``CfnSpotFleet.LaunchTemplateOverridesProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateoverrides.html#cfn-ec2-spotfleet-launchtemplateoverrides-instancetype
        """

        spotPrice: str
        """``CfnSpotFleet.LaunchTemplateOverridesProperty.SpotPrice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateoverrides.html#cfn-ec2-spotfleet-launchtemplateoverrides-spotprice
        """

        subnetId: str
        """``CfnSpotFleet.LaunchTemplateOverridesProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateoverrides.html#cfn-ec2-spotfleet-launchtemplateoverrides-subnetid
        """

        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.LaunchTemplateOverridesProperty.WeightedCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-launchtemplateoverrides.html#cfn-ec2-spotfleet-launchtemplateoverrides-weightedcapacity
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.LoadBalancersConfigProperty", jsii_struct_bases=[])
    class LoadBalancersConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-loadbalancersconfig.html
        """
        classicLoadBalancersConfig: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.ClassicLoadBalancersConfigProperty"]
        """``CfnSpotFleet.LoadBalancersConfigProperty.ClassicLoadBalancersConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-loadbalancersconfig.html#cfn-ec2-spotfleet-loadbalancersconfig-classicloadbalancersconfig
        """

        targetGroupsConfig: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.TargetGroupsConfigProperty"]
        """``CfnSpotFleet.LoadBalancersConfigProperty.TargetGroupsConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-loadbalancersconfig.html#cfn-ec2-spotfleet-loadbalancersconfig-targetgroupsconfig
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _PrivateIpAddressSpecificationProperty(jsii.compat.TypedDict, total=False):
        primary: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.PrivateIpAddressSpecificationProperty.Primary``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces-privateipaddresses.html#cfn-ec2-spotfleet-privateipaddressspecification-primary
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.PrivateIpAddressSpecificationProperty", jsii_struct_bases=[_PrivateIpAddressSpecificationProperty])
    class PrivateIpAddressSpecificationProperty(_PrivateIpAddressSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces-privateipaddresses.html
        """
        privateIpAddress: str
        """``CfnSpotFleet.PrivateIpAddressSpecificationProperty.PrivateIpAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-networkinterfaces-privateipaddresses.html#cfn-ec2-spotfleet-privateipaddressspecification-privateipaddress
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SpotFleetLaunchSpecificationProperty(jsii.compat.TypedDict, total=False):
        blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.BlockDeviceMappingProperty"]]]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.BlockDeviceMappings``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-blockdevicemappings
        """
        ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.EbsOptimized``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-ebsoptimized
        """
        iamInstanceProfile: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.IamInstanceProfileSpecificationProperty"]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.IamInstanceProfile``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-iaminstanceprofile
        """
        kernelId: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.KernelId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-kernelid
        """
        keyName: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.KeyName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-keyname
        """
        monitoring: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetMonitoringProperty"]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.Monitoring``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-monitoring
        """
        networkInterfaces: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.InstanceNetworkInterfaceSpecificationProperty"]]]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.NetworkInterfaces``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-networkinterfaces
        """
        placement: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotPlacementProperty"]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.Placement``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-placement
        """
        ramdiskId: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.RamdiskId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-ramdiskid
        """
        securityGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.GroupIdentifierProperty"]]]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.SecurityGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-securitygroups
        """
        spotPrice: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.SpotPrice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-spotprice
        """
        subnetId: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.SubnetId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-subnetid
        """
        tagSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetTagSpecificationProperty"]]]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.TagSpecifications``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-tagspecifications
        """
        userData: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.UserData``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-userdata
        """
        weightedCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.WeightedCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-weightedcapacity
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetLaunchSpecificationProperty", jsii_struct_bases=[_SpotFleetLaunchSpecificationProperty])
    class SpotFleetLaunchSpecificationProperty(_SpotFleetLaunchSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html
        """
        imageId: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.ImageId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-imageid
        """

        instanceType: str
        """``CfnSpotFleet.SpotFleetLaunchSpecificationProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications.html#cfn-ec2-spotfleet-spotfleetlaunchspecification-instancetype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetMonitoringProperty", jsii_struct_bases=[])
    class SpotFleetMonitoringProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-monitoring.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.SpotFleetMonitoringProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-monitoring.html#cfn-ec2-spotfleet-spotfleetmonitoring-enabled
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SpotFleetRequestConfigDataProperty(jsii.compat.TypedDict, total=False):
        allocationStrategy: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.AllocationStrategy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-allocationstrategy
        """
        excessCapacityTerminationPolicy: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.ExcessCapacityTerminationPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-excesscapacityterminationpolicy
        """
        instanceInterruptionBehavior: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.InstanceInterruptionBehavior``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-instanceinterruptionbehavior
        """
        launchSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetLaunchSpecificationProperty"]]]
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.LaunchSpecifications``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications
        """
        launchTemplateConfigs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.LaunchTemplateConfigProperty"]]]
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.LaunchTemplateConfigs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-launchtemplateconfigs
        """
        loadBalancersConfig: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.LoadBalancersConfigProperty"]
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.LoadBalancersConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-loadbalancersconfig
        """
        replaceUnhealthyInstances: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.ReplaceUnhealthyInstances``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-replaceunhealthyinstances
        """
        spotPrice: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.SpotPrice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-spotprice
        """
        terminateInstancesWithExpiration: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.TerminateInstancesWithExpiration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-terminateinstanceswithexpiration
        """
        type: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-type
        """
        validFrom: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.ValidFrom``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-validfrom
        """
        validUntil: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.ValidUntil``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-validuntil
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetRequestConfigDataProperty", jsii_struct_bases=[_SpotFleetRequestConfigDataProperty])
    class SpotFleetRequestConfigDataProperty(_SpotFleetRequestConfigDataProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html
        """
        iamFleetRole: str
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.IamFleetRole``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-iamfleetrole
        """

        targetCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSpotFleet.SpotFleetRequestConfigDataProperty.TargetCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata-targetcapacity
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotFleetTagSpecificationProperty", jsii_struct_bases=[])
    class SpotFleetTagSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-tagspecifications.html
        """
        resourceType: str
        """``CfnSpotFleet.SpotFleetTagSpecificationProperty.ResourceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-tagspecifications.html#cfn-ec2-spotfleet-spotfleettagspecification-resourcetype
        """

        tags: typing.List[aws_cdk.cdk.CfnTag]
        """``CfnSpotFleet.SpotFleetTagSpecificationProperty.Tags``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-tagspecifications.html#cfn-ec2-spotfleet-tags
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.SpotPlacementProperty", jsii_struct_bases=[])
    class SpotPlacementProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-placement.html
        """
        availabilityZone: str
        """``CfnSpotFleet.SpotPlacementProperty.AvailabilityZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-placement.html#cfn-ec2-spotfleet-spotplacement-availabilityzone
        """

        groupName: str
        """``CfnSpotFleet.SpotPlacementProperty.GroupName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-placement.html#cfn-ec2-spotfleet-spotplacement-groupname
        """

        tenancy: str
        """``CfnSpotFleet.SpotPlacementProperty.Tenancy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-spotfleetrequestconfigdata-launchspecifications-placement.html#cfn-ec2-spotfleet-spotplacement-tenancy
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.TargetGroupProperty", jsii_struct_bases=[])
    class TargetGroupProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-targetgroup.html
        """
        arn: str
        """``CfnSpotFleet.TargetGroupProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-targetgroup.html#cfn-ec2-spotfleet-targetgroup-arn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleet.TargetGroupsConfigProperty", jsii_struct_bases=[])
    class TargetGroupsConfigProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-targetgroupsconfig.html
        """
        targetGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.TargetGroupProperty"]]]
        """``CfnSpotFleet.TargetGroupsConfigProperty.TargetGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-spotfleet-targetgroupsconfig.html#cfn-ec2-spotfleet-targetgroupsconfig-targetgroups
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSpotFleetProps", jsii_struct_bases=[])
class CfnSpotFleetProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::SpotFleet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-spotfleet.html
    """
    spotFleetRequestConfigData: typing.Union[aws_cdk.cdk.Token, "CfnSpotFleet.SpotFleetRequestConfigDataProperty"]
    """``AWS::EC2::SpotFleet.SpotFleetRequestConfigData``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-spotfleet.html#cfn-ec2-spotfleet-spotfleetrequestconfigdata
    """

class CfnSubnet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnet"):
    """A CloudFormation ``AWS::EC2::Subnet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    cloudformationResource:
        AWS::EC2::Subnet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cidr_block: str, vpc_id: str, assign_ipv6_address_on_creation: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, availability_zone: typing.Optional[str]=None, ipv6_cidr_block: typing.Optional[str]=None, map_public_ip_on_launch: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::Subnet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            cidrBlock: ``AWS::EC2::Subnet.CidrBlock``.
            vpcId: ``AWS::EC2::Subnet.VpcId``.
            assignIpv6AddressOnCreation: ``AWS::EC2::Subnet.AssignIpv6AddressOnCreation``.
            availabilityZone: ``AWS::EC2::Subnet.AvailabilityZone``.
            ipv6CidrBlock: ``AWS::EC2::Subnet.Ipv6CidrBlock``.
            mapPublicIpOnLaunch: ``AWS::EC2::Subnet.MapPublicIpOnLaunch``.
            tags: ``AWS::EC2::Subnet.Tags``.
        """
        props: CfnSubnetProps = {"cidrBlock": cidr_block, "vpcId": vpc_id}

        if assign_ipv6_address_on_creation is not None:
            props["assignIpv6AddressOnCreation"] = assign_ipv6_address_on_creation

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if ipv6_cidr_block is not None:
            props["ipv6CidrBlock"] = ipv6_cidr_block

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnSubnet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSubnetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetAvailabilityZone")
    def subnet_availability_zone(self) -> str:
        """
        cloudformationAttribute:
            AvailabilityZone
        """
        return jsii.get(self, "subnetAvailabilityZone")

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        return jsii.get(self, "subnetId")

    @property
    @jsii.member(jsii_name="subnetIpv6CidrBlocks")
    def subnet_ipv6_cidr_blocks(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            Ipv6CidrBlocks
        """
        return jsii.get(self, "subnetIpv6CidrBlocks")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationId")
    def subnet_network_acl_association_id(self) -> str:
        """
        cloudformationAttribute:
            NetworkAclAssociationId
        """
        return jsii.get(self, "subnetNetworkAclAssociationId")

    @property
    @jsii.member(jsii_name="subnetVpcId")
    def subnet_vpc_id(self) -> str:
        """
        cloudformationAttribute:
            VpcId
        """
        return jsii.get(self, "subnetVpcId")

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


class CfnSubnetCidrBlock(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnetCidrBlock"):
    """A CloudFormation ``AWS::EC2::SubnetCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnetcidrblock.html
    cloudformationResource:
        AWS::EC2::SubnetCidrBlock
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ipv6_cidr_block: str, subnet_id: str) -> None:
        """Create a new ``AWS::EC2::SubnetCidrBlock``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            ipv6CidrBlock: ``AWS::EC2::SubnetCidrBlock.Ipv6CidrBlock``.
            subnetId: ``AWS::EC2::SubnetCidrBlock.SubnetId``.
        """
        props: CfnSubnetCidrBlockProps = {"ipv6CidrBlock": ipv6_cidr_block, "subnetId": subnet_id}

        jsii.create(CfnSubnetCidrBlock, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSubnetCidrBlockProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetCidrBlockId")
    def subnet_cidr_block_id(self) -> str:
        return jsii.get(self, "subnetCidrBlockId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetCidrBlockProps", jsii_struct_bases=[])
class CfnSubnetCidrBlockProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::SubnetCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnetcidrblock.html
    """
    ipv6CidrBlock: str
    """``AWS::EC2::SubnetCidrBlock.Ipv6CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnetcidrblock.html#cfn-ec2-subnetcidrblock-ipv6cidrblock
    """

    subnetId: str
    """``AWS::EC2::SubnetCidrBlock.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnetcidrblock.html#cfn-ec2-subnetcidrblock-subnetid
    """

class CfnSubnetNetworkAclAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnetNetworkAclAssociation"):
    """A CloudFormation ``AWS::EC2::SubnetNetworkAclAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-network-acl-assoc.html
    cloudformationResource:
        AWS::EC2::SubnetNetworkAclAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_acl_id: str, subnet_id: str) -> None:
        """Create a new ``AWS::EC2::SubnetNetworkAclAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            networkAclId: ``AWS::EC2::SubnetNetworkAclAssociation.NetworkAclId``.
            subnetId: ``AWS::EC2::SubnetNetworkAclAssociation.SubnetId``.
        """
        props: CfnSubnetNetworkAclAssociationProps = {"networkAclId": network_acl_id, "subnetId": subnet_id}

        jsii.create(CfnSubnetNetworkAclAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSubnetNetworkAclAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationAssociationId")
    def subnet_network_acl_association_association_id(self) -> str:
        """
        cloudformationAttribute:
            AssociationId
        """
        return jsii.get(self, "subnetNetworkAclAssociationAssociationId")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationName")
    def subnet_network_acl_association_name(self) -> str:
        return jsii.get(self, "subnetNetworkAclAssociationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetNetworkAclAssociationProps", jsii_struct_bases=[])
class CfnSubnetNetworkAclAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::SubnetNetworkAclAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-network-acl-assoc.html
    """
    networkAclId: str
    """``AWS::EC2::SubnetNetworkAclAssociation.NetworkAclId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-network-acl-assoc.html#cfn-ec2-subnetnetworkaclassociation-networkaclid
    """

    subnetId: str
    """``AWS::EC2::SubnetNetworkAclAssociation.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-network-acl-assoc.html#cfn-ec2-subnetnetworkaclassociation-associationid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSubnetProps(jsii.compat.TypedDict, total=False):
    assignIpv6AddressOnCreation: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Subnet.AssignIpv6AddressOnCreation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-assignipv6addressoncreation
    """
    availabilityZone: str
    """``AWS::EC2::Subnet.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-availabilityzone
    """
    ipv6CidrBlock: str
    """``AWS::EC2::Subnet.Ipv6CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-ipv6cidrblock
    """
    mapPublicIpOnLaunch: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Subnet.MapPublicIpOnLaunch``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-mappubliciponlaunch
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::Subnet.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetProps", jsii_struct_bases=[_CfnSubnetProps])
class CfnSubnetProps(_CfnSubnetProps):
    """Properties for defining a ``AWS::EC2::Subnet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html
    """
    cidrBlock: str
    """``AWS::EC2::Subnet.CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-ec2-subnet-cidrblock
    """

    vpcId: str
    """``AWS::EC2::Subnet.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet.html#cfn-awsec2subnet-prop-vpcid
    """

class CfnSubnetRouteTableAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnSubnetRouteTableAssociation"):
    """A CloudFormation ``AWS::EC2::SubnetRouteTableAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html
    cloudformationResource:
        AWS::EC2::SubnetRouteTableAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, route_table_id: str, subnet_id: str) -> None:
        """Create a new ``AWS::EC2::SubnetRouteTableAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            routeTableId: ``AWS::EC2::SubnetRouteTableAssociation.RouteTableId``.
            subnetId: ``AWS::EC2::SubnetRouteTableAssociation.SubnetId``.
        """
        props: CfnSubnetRouteTableAssociationProps = {"routeTableId": route_table_id, "subnetId": subnet_id}

        jsii.create(CfnSubnetRouteTableAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSubnetRouteTableAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subnetRouteTableAssociationName")
    def subnet_route_table_association_name(self) -> str:
        return jsii.get(self, "subnetRouteTableAssociationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnSubnetRouteTableAssociationProps", jsii_struct_bases=[])
class CfnSubnetRouteTableAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::SubnetRouteTableAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html
    """
    routeTableId: str
    """``AWS::EC2::SubnetRouteTableAssociation.RouteTableId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html#cfn-ec2-subnetroutetableassociation-routetableid
    """

    subnetId: str
    """``AWS::EC2::SubnetRouteTableAssociation.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-subnet-route-table-assoc.html#cfn-ec2-subnetroutetableassociation-subnetid
    """

class CfnTransitGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGateway"):
    """A CloudFormation ``AWS::EC2::TransitGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html
    cloudformationResource:
        AWS::EC2::TransitGateway
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, amazon_side_asn: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, auto_accept_shared_attachments: typing.Optional[str]=None, default_route_table_association: typing.Optional[str]=None, default_route_table_propagation: typing.Optional[str]=None, description: typing.Optional[str]=None, dns_support: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpn_ecmp_support: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::TransitGateway``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            amazonSideAsn: ``AWS::EC2::TransitGateway.AmazonSideAsn``.
            autoAcceptSharedAttachments: ``AWS::EC2::TransitGateway.AutoAcceptSharedAttachments``.
            defaultRouteTableAssociation: ``AWS::EC2::TransitGateway.DefaultRouteTableAssociation``.
            defaultRouteTablePropagation: ``AWS::EC2::TransitGateway.DefaultRouteTablePropagation``.
            description: ``AWS::EC2::TransitGateway.Description``.
            dnsSupport: ``AWS::EC2::TransitGateway.DnsSupport``.
            tags: ``AWS::EC2::TransitGateway.Tags``.
            vpnEcmpSupport: ``AWS::EC2::TransitGateway.VpnEcmpSupport``.
        """
        props: CfnTransitGatewayProps = {}

        if amazon_side_asn is not None:
            props["amazonSideAsn"] = amazon_side_asn

        if auto_accept_shared_attachments is not None:
            props["autoAcceptSharedAttachments"] = auto_accept_shared_attachments

        if default_route_table_association is not None:
            props["defaultRouteTableAssociation"] = default_route_table_association

        if default_route_table_propagation is not None:
            props["defaultRouteTablePropagation"] = default_route_table_propagation

        if description is not None:
            props["description"] = description

        if dns_support is not None:
            props["dnsSupport"] = dns_support

        if tags is not None:
            props["tags"] = tags

        if vpn_ecmp_support is not None:
            props["vpnEcmpSupport"] = vpn_ecmp_support

        jsii.create(CfnTransitGateway, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTransitGatewayProps":
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

    @property
    @jsii.member(jsii_name="transitGatewayId")
    def transit_gateway_id(self) -> str:
        return jsii.get(self, "transitGatewayId")


class CfnTransitGatewayAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayAttachment"):
    """A CloudFormation ``AWS::EC2::TransitGatewayAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayattachment.html
    cloudformationResource:
        AWS::EC2::TransitGatewayAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, subnet_ids: typing.List[str], transit_gateway_id: str, vpc_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::TransitGatewayAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            subnetIds: ``AWS::EC2::TransitGatewayAttachment.SubnetIds``.
            transitGatewayId: ``AWS::EC2::TransitGatewayAttachment.TransitGatewayId``.
            vpcId: ``AWS::EC2::TransitGatewayAttachment.VpcId``.
            tags: ``AWS::EC2::TransitGatewayAttachment.Tags``.
        """
        props: CfnTransitGatewayAttachmentProps = {"subnetIds": subnet_ids, "transitGatewayId": transit_gateway_id, "vpcId": vpc_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnTransitGatewayAttachment, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTransitGatewayAttachmentProps":
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

    @property
    @jsii.member(jsii_name="transitGatewayAttachmentId")
    def transit_gateway_attachment_id(self) -> str:
        return jsii.get(self, "transitGatewayAttachmentId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnTransitGatewayAttachmentProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::TransitGatewayAttachment.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayattachment.html#cfn-ec2-transitgatewayattachment-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayAttachmentProps", jsii_struct_bases=[_CfnTransitGatewayAttachmentProps])
class CfnTransitGatewayAttachmentProps(_CfnTransitGatewayAttachmentProps):
    """Properties for defining a ``AWS::EC2::TransitGatewayAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayattachment.html
    """
    subnetIds: typing.List[str]
    """``AWS::EC2::TransitGatewayAttachment.SubnetIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayattachment.html#cfn-ec2-transitgatewayattachment-subnetids
    """

    transitGatewayId: str
    """``AWS::EC2::TransitGatewayAttachment.TransitGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayattachment.html#cfn-ec2-transitgatewayattachment-transitgatewayid
    """

    vpcId: str
    """``AWS::EC2::TransitGatewayAttachment.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayattachment.html#cfn-ec2-transitgatewayattachment-vpcid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayProps", jsii_struct_bases=[])
class CfnTransitGatewayProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EC2::TransitGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html
    """
    amazonSideAsn: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::TransitGateway.AmazonSideAsn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-amazonsideasn
    """

    autoAcceptSharedAttachments: str
    """``AWS::EC2::TransitGateway.AutoAcceptSharedAttachments``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-autoacceptsharedattachments
    """

    defaultRouteTableAssociation: str
    """``AWS::EC2::TransitGateway.DefaultRouteTableAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-defaultroutetableassociation
    """

    defaultRouteTablePropagation: str
    """``AWS::EC2::TransitGateway.DefaultRouteTablePropagation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-defaultroutetablepropagation
    """

    description: str
    """``AWS::EC2::TransitGateway.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-description
    """

    dnsSupport: str
    """``AWS::EC2::TransitGateway.DnsSupport``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-dnssupport
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::TransitGateway.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-tags
    """

    vpnEcmpSupport: str
    """``AWS::EC2::TransitGateway.VpnEcmpSupport``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgateway.html#cfn-ec2-transitgateway-vpnecmpsupport
    """

class CfnTransitGatewayRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRoute"):
    """A CloudFormation ``AWS::EC2::TransitGatewayRoute``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroute.html
    cloudformationResource:
        AWS::EC2::TransitGatewayRoute
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_route_table_id: str, blackhole: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, destination_cidr_block: typing.Optional[str]=None, transit_gateway_attachment_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::TransitGatewayRoute``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            transitGatewayRouteTableId: ``AWS::EC2::TransitGatewayRoute.TransitGatewayRouteTableId``.
            blackhole: ``AWS::EC2::TransitGatewayRoute.Blackhole``.
            destinationCidrBlock: ``AWS::EC2::TransitGatewayRoute.DestinationCidrBlock``.
            transitGatewayAttachmentId: ``AWS::EC2::TransitGatewayRoute.TransitGatewayAttachmentId``.
        """
        props: CfnTransitGatewayRouteProps = {"transitGatewayRouteTableId": transit_gateway_route_table_id}

        if blackhole is not None:
            props["blackhole"] = blackhole

        if destination_cidr_block is not None:
            props["destinationCidrBlock"] = destination_cidr_block

        if transit_gateway_attachment_id is not None:
            props["transitGatewayAttachmentId"] = transit_gateway_attachment_id

        jsii.create(CfnTransitGatewayRoute, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTransitGatewayRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="transitGatewayRouteId")
    def transit_gateway_route_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnTransitGatewayRouteProps(jsii.compat.TypedDict, total=False):
    blackhole: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::TransitGatewayRoute.Blackhole``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroute.html#cfn-ec2-transitgatewayroute-blackhole
    """
    destinationCidrBlock: str
    """``AWS::EC2::TransitGatewayRoute.DestinationCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroute.html#cfn-ec2-transitgatewayroute-destinationcidrblock
    """
    transitGatewayAttachmentId: str
    """``AWS::EC2::TransitGatewayRoute.TransitGatewayAttachmentId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroute.html#cfn-ec2-transitgatewayroute-transitgatewayattachmentid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteProps", jsii_struct_bases=[_CfnTransitGatewayRouteProps])
class CfnTransitGatewayRouteProps(_CfnTransitGatewayRouteProps):
    """Properties for defining a ``AWS::EC2::TransitGatewayRoute``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroute.html
    """
    transitGatewayRouteTableId: str
    """``AWS::EC2::TransitGatewayRoute.TransitGatewayRouteTableId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroute.html#cfn-ec2-transitgatewayroute-transitgatewayroutetableid
    """

class CfnTransitGatewayRouteTable(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTable"):
    """A CloudFormation ``AWS::EC2::TransitGatewayRouteTable``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html
    cloudformationResource:
        AWS::EC2::TransitGatewayRouteTable
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_id: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::TransitGatewayRouteTable``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            transitGatewayId: ``AWS::EC2::TransitGatewayRouteTable.TransitGatewayId``.
            tags: ``AWS::EC2::TransitGatewayRouteTable.Tags``.
        """
        props: CfnTransitGatewayRouteTableProps = {"transitGatewayId": transit_gateway_id}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnTransitGatewayRouteTable, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTransitGatewayRouteTableProps":
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

    @property
    @jsii.member(jsii_name="transitGatewayRouteTableId")
    def transit_gateway_route_table_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteTableId")


class CfnTransitGatewayRouteTableAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTableAssociation"):
    """A CloudFormation ``AWS::EC2::TransitGatewayRouteTableAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetableassociation.html
    cloudformationResource:
        AWS::EC2::TransitGatewayRouteTableAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_attachment_id: str, transit_gateway_route_table_id: str) -> None:
        """Create a new ``AWS::EC2::TransitGatewayRouteTableAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            transitGatewayAttachmentId: ``AWS::EC2::TransitGatewayRouteTableAssociation.TransitGatewayAttachmentId``.
            transitGatewayRouteTableId: ``AWS::EC2::TransitGatewayRouteTableAssociation.TransitGatewayRouteTableId``.
        """
        props: CfnTransitGatewayRouteTableAssociationProps = {"transitGatewayAttachmentId": transit_gateway_attachment_id, "transitGatewayRouteTableId": transit_gateway_route_table_id}

        jsii.create(CfnTransitGatewayRouteTableAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTransitGatewayRouteTableAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="transitGatewayRouteTableAssociationId")
    def transit_gateway_route_table_association_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteTableAssociationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTableAssociationProps", jsii_struct_bases=[])
class CfnTransitGatewayRouteTableAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::TransitGatewayRouteTableAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetableassociation.html
    """
    transitGatewayAttachmentId: str
    """``AWS::EC2::TransitGatewayRouteTableAssociation.TransitGatewayAttachmentId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetableassociation.html#cfn-ec2-transitgatewayroutetableassociation-transitgatewayattachmentid
    """

    transitGatewayRouteTableId: str
    """``AWS::EC2::TransitGatewayRouteTableAssociation.TransitGatewayRouteTableId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetableassociation.html#cfn-ec2-transitgatewayroutetableassociation-transitgatewayroutetableid
    """

class CfnTransitGatewayRouteTablePropagation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTablePropagation"):
    """A CloudFormation ``AWS::EC2::TransitGatewayRouteTablePropagation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetablepropagation.html
    cloudformationResource:
        AWS::EC2::TransitGatewayRouteTablePropagation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, transit_gateway_attachment_id: str, transit_gateway_route_table_id: str) -> None:
        """Create a new ``AWS::EC2::TransitGatewayRouteTablePropagation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            transitGatewayAttachmentId: ``AWS::EC2::TransitGatewayRouteTablePropagation.TransitGatewayAttachmentId``.
            transitGatewayRouteTableId: ``AWS::EC2::TransitGatewayRouteTablePropagation.TransitGatewayRouteTableId``.
        """
        props: CfnTransitGatewayRouteTablePropagationProps = {"transitGatewayAttachmentId": transit_gateway_attachment_id, "transitGatewayRouteTableId": transit_gateway_route_table_id}

        jsii.create(CfnTransitGatewayRouteTablePropagation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTransitGatewayRouteTablePropagationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="transitGatewayRouteTablePropagationId")
    def transit_gateway_route_table_propagation_id(self) -> str:
        return jsii.get(self, "transitGatewayRouteTablePropagationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTablePropagationProps", jsii_struct_bases=[])
class CfnTransitGatewayRouteTablePropagationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::TransitGatewayRouteTablePropagation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetablepropagation.html
    """
    transitGatewayAttachmentId: str
    """``AWS::EC2::TransitGatewayRouteTablePropagation.TransitGatewayAttachmentId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetablepropagation.html#cfn-ec2-transitgatewayroutetablepropagation-transitgatewayattachmentid
    """

    transitGatewayRouteTableId: str
    """``AWS::EC2::TransitGatewayRouteTablePropagation.TransitGatewayRouteTableId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetablepropagation.html#cfn-ec2-transitgatewayroutetablepropagation-transitgatewayroutetableid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnTransitGatewayRouteTableProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::TransitGatewayRouteTable.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html#cfn-ec2-transitgatewayroutetable-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnTransitGatewayRouteTableProps", jsii_struct_bases=[_CfnTransitGatewayRouteTableProps])
class CfnTransitGatewayRouteTableProps(_CfnTransitGatewayRouteTableProps):
    """Properties for defining a ``AWS::EC2::TransitGatewayRouteTable``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html
    """
    transitGatewayId: str
    """``AWS::EC2::TransitGatewayRouteTable.TransitGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-transitgatewayroutetable.html#cfn-ec2-transitgatewayroutetable-transitgatewayid
    """

class CfnVPC(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPC"):
    """A CloudFormation ``AWS::EC2::VPC``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html
    cloudformationResource:
        AWS::EC2::VPC
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cidr_block: str, enable_dns_hostnames: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, enable_dns_support: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, instance_tenancy: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::VPC``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            cidrBlock: ``AWS::EC2::VPC.CidrBlock``.
            enableDnsHostnames: ``AWS::EC2::VPC.EnableDnsHostnames``.
            enableDnsSupport: ``AWS::EC2::VPC.EnableDnsSupport``.
            instanceTenancy: ``AWS::EC2::VPC.InstanceTenancy``.
            tags: ``AWS::EC2::VPC.Tags``.
        """
        props: CfnVPCProps = {"cidrBlock": cidr_block}

        if enable_dns_hostnames is not None:
            props["enableDnsHostnames"] = enable_dns_hostnames

        if enable_dns_support is not None:
            props["enableDnsSupport"] = enable_dns_support

        if instance_tenancy is not None:
            props["instanceTenancy"] = instance_tenancy

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVPC, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCProps":
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

    @property
    @jsii.member(jsii_name="vpcCidrBlock")
    def vpc_cidr_block(self) -> str:
        """
        cloudformationAttribute:
            CidrBlock
        """
        return jsii.get(self, "vpcCidrBlock")

    @property
    @jsii.member(jsii_name="vpcCidrBlockAssociations")
    def vpc_cidr_block_associations(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            CidrBlockAssociations
        """
        return jsii.get(self, "vpcCidrBlockAssociations")

    @property
    @jsii.member(jsii_name="vpcDefaultNetworkAcl")
    def vpc_default_network_acl(self) -> str:
        """
        cloudformationAttribute:
            DefaultNetworkAcl
        """
        return jsii.get(self, "vpcDefaultNetworkAcl")

    @property
    @jsii.member(jsii_name="vpcDefaultSecurityGroup")
    def vpc_default_security_group(self) -> str:
        """
        cloudformationAttribute:
            DefaultSecurityGroup
        """
        return jsii.get(self, "vpcDefaultSecurityGroup")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpcIpv6CidrBlocks")
    def vpc_ipv6_cidr_blocks(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            Ipv6CidrBlocks
        """
        return jsii.get(self, "vpcIpv6CidrBlocks")


class CfnVPCCidrBlock(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCCidrBlock"):
    """A CloudFormation ``AWS::EC2::VPCCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html
    cloudformationResource:
        AWS::EC2::VPCCidrBlock
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, amazon_provided_ipv6_cidr_block: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, cidr_block: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::VPCCidrBlock``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            vpcId: ``AWS::EC2::VPCCidrBlock.VpcId``.
            amazonProvidedIpv6CidrBlock: ``AWS::EC2::VPCCidrBlock.AmazonProvidedIpv6CidrBlock``.
            cidrBlock: ``AWS::EC2::VPCCidrBlock.CidrBlock``.
        """
        props: CfnVPCCidrBlockProps = {"vpcId": vpc_id}

        if amazon_provided_ipv6_cidr_block is not None:
            props["amazonProvidedIpv6CidrBlock"] = amazon_provided_ipv6_cidr_block

        if cidr_block is not None:
            props["cidrBlock"] = cidr_block

        jsii.create(CfnVPCCidrBlock, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCCidrBlockProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcCidrBlockId")
    def vpc_cidr_block_id(self) -> str:
        return jsii.get(self, "vpcCidrBlockId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCCidrBlockProps(jsii.compat.TypedDict, total=False):
    amazonProvidedIpv6CidrBlock: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::VPCCidrBlock.AmazonProvidedIpv6CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html#cfn-ec2-vpccidrblock-amazonprovidedipv6cidrblock
    """
    cidrBlock: str
    """``AWS::EC2::VPCCidrBlock.CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html#cfn-ec2-vpccidrblock-cidrblock
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCCidrBlockProps", jsii_struct_bases=[_CfnVPCCidrBlockProps])
class CfnVPCCidrBlockProps(_CfnVPCCidrBlockProps):
    """Properties for defining a ``AWS::EC2::VPCCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html
    """
    vpcId: str
    """``AWS::EC2::VPCCidrBlock.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpccidrblock.html#cfn-ec2-vpccidrblock-vpcid
    """

class CfnVPCDHCPOptionsAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCDHCPOptionsAssociation"):
    """A CloudFormation ``AWS::EC2::VPCDHCPOptionsAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html
    cloudformationResource:
        AWS::EC2::VPCDHCPOptionsAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dhcp_options_id: str, vpc_id: str) -> None:
        """Create a new ``AWS::EC2::VPCDHCPOptionsAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            dhcpOptionsId: ``AWS::EC2::VPCDHCPOptionsAssociation.DhcpOptionsId``.
            vpcId: ``AWS::EC2::VPCDHCPOptionsAssociation.VpcId``.
        """
        props: CfnVPCDHCPOptionsAssociationProps = {"dhcpOptionsId": dhcp_options_id, "vpcId": vpc_id}

        jsii.create(CfnVPCDHCPOptionsAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCDHCPOptionsAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcdhcpOptionsAssociationName")
    def vpcdhcp_options_association_name(self) -> str:
        return jsii.get(self, "vpcdhcpOptionsAssociationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCDHCPOptionsAssociationProps", jsii_struct_bases=[])
class CfnVPCDHCPOptionsAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::VPCDHCPOptionsAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html
    """
    dhcpOptionsId: str
    """``AWS::EC2::VPCDHCPOptionsAssociation.DhcpOptionsId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html#cfn-ec2-vpcdhcpoptionsassociation-dhcpoptionsid
    """

    vpcId: str
    """``AWS::EC2::VPCDHCPOptionsAssociation.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-dhcp-options-assoc.html#cfn-ec2-vpcdhcpoptionsassociation-vpcid
    """

class CfnVPCEndpoint(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpoint"):
    """A CloudFormation ``AWS::EC2::VPCEndpoint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html
    cloudformationResource:
        AWS::EC2::VPCEndpoint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service_name: str, vpc_id: str, policy_document: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, private_dns_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, route_table_ids: typing.Optional[typing.List[str]]=None, security_group_ids: typing.Optional[typing.List[str]]=None, subnet_ids: typing.Optional[typing.List[str]]=None, vpc_endpoint_type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::VPCEndpoint``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            serviceName: ``AWS::EC2::VPCEndpoint.ServiceName``.
            vpcId: ``AWS::EC2::VPCEndpoint.VpcId``.
            policyDocument: ``AWS::EC2::VPCEndpoint.PolicyDocument``.
            privateDnsEnabled: ``AWS::EC2::VPCEndpoint.PrivateDnsEnabled``.
            routeTableIds: ``AWS::EC2::VPCEndpoint.RouteTableIds``.
            securityGroupIds: ``AWS::EC2::VPCEndpoint.SecurityGroupIds``.
            subnetIds: ``AWS::EC2::VPCEndpoint.SubnetIds``.
            vpcEndpointType: ``AWS::EC2::VPCEndpoint.VpcEndpointType``.
        """
        props: CfnVPCEndpointProps = {"serviceName": service_name, "vpcId": vpc_id}

        if policy_document is not None:
            props["policyDocument"] = policy_document

        if private_dns_enabled is not None:
            props["privateDnsEnabled"] = private_dns_enabled

        if route_table_ids is not None:
            props["routeTableIds"] = route_table_ids

        if security_group_ids is not None:
            props["securityGroupIds"] = security_group_ids

        if subnet_ids is not None:
            props["subnetIds"] = subnet_ids

        if vpc_endpoint_type is not None:
            props["vpcEndpointType"] = vpc_endpoint_type

        jsii.create(CfnVPCEndpoint, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCEndpointProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcEndpointCreationTimestamp")
    def vpc_endpoint_creation_timestamp(self) -> str:
        """
        cloudformationAttribute:
            CreationTimestamp
        """
        return jsii.get(self, "vpcEndpointCreationTimestamp")

    @property
    @jsii.member(jsii_name="vpcEndpointDnsEntries")
    def vpc_endpoint_dns_entries(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            DnsEntries
        """
        return jsii.get(self, "vpcEndpointDnsEntries")

    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        return jsii.get(self, "vpcEndpointId")

    @property
    @jsii.member(jsii_name="vpcEndpointNetworkInterfaceIds")
    def vpc_endpoint_network_interface_ids(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            NetworkInterfaceIds
        """
        return jsii.get(self, "vpcEndpointNetworkInterfaceIds")


class CfnVPCEndpointConnectionNotification(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointConnectionNotification"):
    """A CloudFormation ``AWS::EC2::VPCEndpointConnectionNotification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointconnectionnotification.html
    cloudformationResource:
        AWS::EC2::VPCEndpointConnectionNotification
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, connection_events: typing.List[str], connection_notification_arn: str, service_id: typing.Optional[str]=None, vpc_endpoint_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::VPCEndpointConnectionNotification``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            connectionEvents: ``AWS::EC2::VPCEndpointConnectionNotification.ConnectionEvents``.
            connectionNotificationArn: ``AWS::EC2::VPCEndpointConnectionNotification.ConnectionNotificationArn``.
            serviceId: ``AWS::EC2::VPCEndpointConnectionNotification.ServiceId``.
            vpcEndpointId: ``AWS::EC2::VPCEndpointConnectionNotification.VPCEndpointId``.
        """
        props: CfnVPCEndpointConnectionNotificationProps = {"connectionEvents": connection_events, "connectionNotificationArn": connection_notification_arn}

        if service_id is not None:
            props["serviceId"] = service_id

        if vpc_endpoint_id is not None:
            props["vpcEndpointId"] = vpc_endpoint_id

        jsii.create(CfnVPCEndpointConnectionNotification, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCEndpointConnectionNotificationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCEndpointConnectionNotificationProps(jsii.compat.TypedDict, total=False):
    serviceId: str
    """``AWS::EC2::VPCEndpointConnectionNotification.ServiceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointconnectionnotification.html#cfn-ec2-vpcendpointconnectionnotification-serviceid
    """
    vpcEndpointId: str
    """``AWS::EC2::VPCEndpointConnectionNotification.VPCEndpointId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointconnectionnotification.html#cfn-ec2-vpcendpointconnectionnotification-vpcendpointid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointConnectionNotificationProps", jsii_struct_bases=[_CfnVPCEndpointConnectionNotificationProps])
class CfnVPCEndpointConnectionNotificationProps(_CfnVPCEndpointConnectionNotificationProps):
    """Properties for defining a ``AWS::EC2::VPCEndpointConnectionNotification``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointconnectionnotification.html
    """
    connectionEvents: typing.List[str]
    """``AWS::EC2::VPCEndpointConnectionNotification.ConnectionEvents``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointconnectionnotification.html#cfn-ec2-vpcendpointconnectionnotification-connectionevents
    """

    connectionNotificationArn: str
    """``AWS::EC2::VPCEndpointConnectionNotification.ConnectionNotificationArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointconnectionnotification.html#cfn-ec2-vpcendpointconnectionnotification-connectionnotificationarn
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCEndpointProps(jsii.compat.TypedDict, total=False):
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::EC2::VPCEndpoint.PolicyDocument``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-policydocument
    """
    privateDnsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::VPCEndpoint.PrivateDnsEnabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-privatednsenabled
    """
    routeTableIds: typing.List[str]
    """``AWS::EC2::VPCEndpoint.RouteTableIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-routetableids
    """
    securityGroupIds: typing.List[str]
    """``AWS::EC2::VPCEndpoint.SecurityGroupIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-securitygroupids
    """
    subnetIds: typing.List[str]
    """``AWS::EC2::VPCEndpoint.SubnetIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-subnetids
    """
    vpcEndpointType: str
    """``AWS::EC2::VPCEndpoint.VpcEndpointType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-vpcendpointtype
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointProps", jsii_struct_bases=[_CfnVPCEndpointProps])
class CfnVPCEndpointProps(_CfnVPCEndpointProps):
    """Properties for defining a ``AWS::EC2::VPCEndpoint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html
    """
    serviceName: str
    """``AWS::EC2::VPCEndpoint.ServiceName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-servicename
    """

    vpcId: str
    """``AWS::EC2::VPCEndpoint.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpoint.html#cfn-ec2-vpcendpoint-vpcid
    """

class CfnVPCEndpointService(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointService"):
    """A CloudFormation ``AWS::EC2::VPCEndpointService``.

    See:
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservice.html
    cloudformationResource:
        AWS::EC2::VPCEndpointService
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, network_load_balancer_arns: typing.List[str], acceptance_required: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::EC2::VPCEndpointService``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            networkLoadBalancerArns: ``AWS::EC2::VPCEndpointService.NetworkLoadBalancerArns``.
            acceptanceRequired: ``AWS::EC2::VPCEndpointService.AcceptanceRequired``.
        """
        props: CfnVPCEndpointServiceProps = {"networkLoadBalancerArns": network_load_balancer_arns}

        if acceptance_required is not None:
            props["acceptanceRequired"] = acceptance_required

        jsii.create(CfnVPCEndpointService, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCEndpointServiceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcEndpointServiceId")
    def vpc_endpoint_service_id(self) -> str:
        return jsii.get(self, "vpcEndpointServiceId")


class CfnVPCEndpointServicePermissions(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointServicePermissions"):
    """A CloudFormation ``AWS::EC2::VPCEndpointServicePermissions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservicepermissions.html
    cloudformationResource:
        AWS::EC2::VPCEndpointServicePermissions
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, service_id: str, allowed_principals: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::EC2::VPCEndpointServicePermissions``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            serviceId: ``AWS::EC2::VPCEndpointServicePermissions.ServiceId``.
            allowedPrincipals: ``AWS::EC2::VPCEndpointServicePermissions.AllowedPrincipals``.
        """
        props: CfnVPCEndpointServicePermissionsProps = {"serviceId": service_id}

        if allowed_principals is not None:
            props["allowedPrincipals"] = allowed_principals

        jsii.create(CfnVPCEndpointServicePermissions, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCEndpointServicePermissionsProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCEndpointServicePermissionsProps(jsii.compat.TypedDict, total=False):
    allowedPrincipals: typing.List[str]
    """``AWS::EC2::VPCEndpointServicePermissions.AllowedPrincipals``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservicepermissions.html#cfn-ec2-vpcendpointservicepermissions-allowedprincipals
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointServicePermissionsProps", jsii_struct_bases=[_CfnVPCEndpointServicePermissionsProps])
class CfnVPCEndpointServicePermissionsProps(_CfnVPCEndpointServicePermissionsProps):
    """Properties for defining a ``AWS::EC2::VPCEndpointServicePermissions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservicepermissions.html
    """
    serviceId: str
    """``AWS::EC2::VPCEndpointServicePermissions.ServiceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservicepermissions.html#cfn-ec2-vpcendpointservicepermissions-serviceid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCEndpointServiceProps(jsii.compat.TypedDict, total=False):
    acceptanceRequired: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::VPCEndpointService.AcceptanceRequired``.

    See:
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservice.html#cfn-ec2-vpcendpointservice-acceptancerequired
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCEndpointServiceProps", jsii_struct_bases=[_CfnVPCEndpointServiceProps])
class CfnVPCEndpointServiceProps(_CfnVPCEndpointServiceProps):
    """Properties for defining a ``AWS::EC2::VPCEndpointService``.

    See:
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservice.html
    """
    networkLoadBalancerArns: typing.List[str]
    """``AWS::EC2::VPCEndpointService.NetworkLoadBalancerArns``.

    See:
        https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcendpointservice.html#cfn-ec2-vpcendpointservice-networkloadbalancerarns
    """

class CfnVPCGatewayAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCGatewayAttachment"):
    """A CloudFormation ``AWS::EC2::VPCGatewayAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html
    cloudformationResource:
        AWS::EC2::VPCGatewayAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc_id: str, internet_gateway_id: typing.Optional[str]=None, vpn_gateway_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::VPCGatewayAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            vpcId: ``AWS::EC2::VPCGatewayAttachment.VpcId``.
            internetGatewayId: ``AWS::EC2::VPCGatewayAttachment.InternetGatewayId``.
            vpnGatewayId: ``AWS::EC2::VPCGatewayAttachment.VpnGatewayId``.
        """
        props: CfnVPCGatewayAttachmentProps = {"vpcId": vpc_id}

        if internet_gateway_id is not None:
            props["internetGatewayId"] = internet_gateway_id

        if vpn_gateway_id is not None:
            props["vpnGatewayId"] = vpn_gateway_id

        jsii.create(CfnVPCGatewayAttachment, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCGatewayAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpcGatewayAttachmentName")
    def vpc_gateway_attachment_name(self) -> str:
        return jsii.get(self, "vpcGatewayAttachmentName")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCGatewayAttachmentProps(jsii.compat.TypedDict, total=False):
    internetGatewayId: str
    """``AWS::EC2::VPCGatewayAttachment.InternetGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html#cfn-ec2-vpcgatewayattachment-internetgatewayid
    """
    vpnGatewayId: str
    """``AWS::EC2::VPCGatewayAttachment.VpnGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html#cfn-ec2-vpcgatewayattachment-vpngatewayid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCGatewayAttachmentProps", jsii_struct_bases=[_CfnVPCGatewayAttachmentProps])
class CfnVPCGatewayAttachmentProps(_CfnVPCGatewayAttachmentProps):
    """Properties for defining a ``AWS::EC2::VPCGatewayAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html
    """
    vpcId: str
    """``AWS::EC2::VPCGatewayAttachment.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc-gateway-attachment.html#cfn-ec2-vpcgatewayattachment-vpcid
    """

class CfnVPCPeeringConnection(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPCPeeringConnection"):
    """A CloudFormation ``AWS::EC2::VPCPeeringConnection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html
    cloudformationResource:
        AWS::EC2::VPCPeeringConnection
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, peer_vpc_id: str, vpc_id: str, peer_owner_id: typing.Optional[str]=None, peer_region: typing.Optional[str]=None, peer_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::VPCPeeringConnection``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            peerVpcId: ``AWS::EC2::VPCPeeringConnection.PeerVpcId``.
            vpcId: ``AWS::EC2::VPCPeeringConnection.VpcId``.
            peerOwnerId: ``AWS::EC2::VPCPeeringConnection.PeerOwnerId``.
            peerRegion: ``AWS::EC2::VPCPeeringConnection.PeerRegion``.
            peerRoleArn: ``AWS::EC2::VPCPeeringConnection.PeerRoleArn``.
            tags: ``AWS::EC2::VPCPeeringConnection.Tags``.
        """
        props: CfnVPCPeeringConnectionProps = {"peerVpcId": peer_vpc_id, "vpcId": vpc_id}

        if peer_owner_id is not None:
            props["peerOwnerId"] = peer_owner_id

        if peer_region is not None:
            props["peerRegion"] = peer_region

        if peer_role_arn is not None:
            props["peerRoleArn"] = peer_role_arn

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVPCPeeringConnection, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPCPeeringConnectionProps":
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

    @property
    @jsii.member(jsii_name="vpcPeeringConnectionName")
    def vpc_peering_connection_name(self) -> str:
        return jsii.get(self, "vpcPeeringConnectionName")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCPeeringConnectionProps(jsii.compat.TypedDict, total=False):
    peerOwnerId: str
    """``AWS::EC2::VPCPeeringConnection.PeerOwnerId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html#cfn-ec2-vpcpeeringconnection-peerownerid
    """
    peerRegion: str
    """``AWS::EC2::VPCPeeringConnection.PeerRegion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html#cfn-ec2-vpcpeeringconnection-peerregion
    """
    peerRoleArn: str
    """``AWS::EC2::VPCPeeringConnection.PeerRoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html#cfn-ec2-vpcpeeringconnection-peerrolearn
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::VPCPeeringConnection.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html#cfn-ec2-vpcpeeringconnection-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCPeeringConnectionProps", jsii_struct_bases=[_CfnVPCPeeringConnectionProps])
class CfnVPCPeeringConnectionProps(_CfnVPCPeeringConnectionProps):
    """Properties for defining a ``AWS::EC2::VPCPeeringConnection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html
    """
    peerVpcId: str
    """``AWS::EC2::VPCPeeringConnection.PeerVpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html#cfn-ec2-vpcpeeringconnection-peervpcid
    """

    vpcId: str
    """``AWS::EC2::VPCPeeringConnection.VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpcpeeringconnection.html#cfn-ec2-vpcpeeringconnection-vpcid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPCProps(jsii.compat.TypedDict, total=False):
    enableDnsHostnames: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::VPC.EnableDnsHostnames``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-EnableDnsHostnames
    """
    enableDnsSupport: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::VPC.EnableDnsSupport``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-EnableDnsSupport
    """
    instanceTenancy: str
    """``AWS::EC2::VPC.InstanceTenancy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-instancetenancy
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::VPC.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPCProps", jsii_struct_bases=[_CfnVPCProps])
class CfnVPCProps(_CfnVPCProps):
    """Properties for defining a ``AWS::EC2::VPC``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html
    """
    cidrBlock: str
    """``AWS::EC2::VPC.CidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpc.html#cfn-aws-ec2-vpc-cidrblock
    """

class CfnVPNConnection(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNConnection"):
    """A CloudFormation ``AWS::EC2::VPNConnection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html
    cloudformationResource:
        AWS::EC2::VPNConnection
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, customer_gateway_id: str, type: str, vpn_gateway_id: str, static_routes_only: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpn_tunnel_options_specifications: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "VpnTunnelOptionsSpecificationProperty"]]]]]=None) -> None:
        """Create a new ``AWS::EC2::VPNConnection``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            customerGatewayId: ``AWS::EC2::VPNConnection.CustomerGatewayId``.
            type: ``AWS::EC2::VPNConnection.Type``.
            vpnGatewayId: ``AWS::EC2::VPNConnection.VpnGatewayId``.
            staticRoutesOnly: ``AWS::EC2::VPNConnection.StaticRoutesOnly``.
            tags: ``AWS::EC2::VPNConnection.Tags``.
            vpnTunnelOptionsSpecifications: ``AWS::EC2::VPNConnection.VpnTunnelOptionsSpecifications``.
        """
        props: CfnVPNConnectionProps = {"customerGatewayId": customer_gateway_id, "type": type, "vpnGatewayId": vpn_gateway_id}

        if static_routes_only is not None:
            props["staticRoutesOnly"] = static_routes_only

        if tags is not None:
            props["tags"] = tags

        if vpn_tunnel_options_specifications is not None:
            props["vpnTunnelOptionsSpecifications"] = vpn_tunnel_options_specifications

        jsii.create(CfnVPNConnection, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPNConnectionProps":
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

    @property
    @jsii.member(jsii_name="vpnConnectionName")
    def vpn_connection_name(self) -> str:
        return jsii.get(self, "vpnConnectionName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNConnection.VpnTunnelOptionsSpecificationProperty", jsii_struct_bases=[])
    class VpnTunnelOptionsSpecificationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-vpnconnection-vpntunneloptionsspecification.html
        """
        preSharedKey: str
        """``CfnVPNConnection.VpnTunnelOptionsSpecificationProperty.PreSharedKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-vpnconnection-vpntunneloptionsspecification.html#cfn-ec2-vpnconnection-vpntunneloptionsspecification-presharedkey
        """

        tunnelInsideCidr: str
        """``CfnVPNConnection.VpnTunnelOptionsSpecificationProperty.TunnelInsideCidr``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-vpnconnection-vpntunneloptionsspecification.html#cfn-ec2-vpnconnection-vpntunneloptionsspecification-tunnelinsidecidr
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPNConnectionProps(jsii.compat.TypedDict, total=False):
    staticRoutesOnly: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::VPNConnection.StaticRoutesOnly``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html#cfn-ec2-vpnconnection-StaticRoutesOnly
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::VPNConnection.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html#cfn-ec2-vpnconnection-tags
    """
    vpnTunnelOptionsSpecifications: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnVPNConnection.VpnTunnelOptionsSpecificationProperty"]]]
    """``AWS::EC2::VPNConnection.VpnTunnelOptionsSpecifications``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html#cfn-ec2-vpnconnection-vpntunneloptionsspecifications
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNConnectionProps", jsii_struct_bases=[_CfnVPNConnectionProps])
class CfnVPNConnectionProps(_CfnVPNConnectionProps):
    """Properties for defining a ``AWS::EC2::VPNConnection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html
    """
    customerGatewayId: str
    """``AWS::EC2::VPNConnection.CustomerGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html#cfn-ec2-vpnconnection-customergatewayid
    """

    type: str
    """``AWS::EC2::VPNConnection.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html#cfn-ec2-vpnconnection-type
    """

    vpnGatewayId: str
    """``AWS::EC2::VPNConnection.VpnGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection.html#cfn-ec2-vpnconnection-vpngatewayid
    """

class CfnVPNConnectionRoute(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNConnectionRoute"):
    """A CloudFormation ``AWS::EC2::VPNConnectionRoute``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection-route.html
    cloudformationResource:
        AWS::EC2::VPNConnectionRoute
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination_cidr_block: str, vpn_connection_id: str) -> None:
        """Create a new ``AWS::EC2::VPNConnectionRoute``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            destinationCidrBlock: ``AWS::EC2::VPNConnectionRoute.DestinationCidrBlock``.
            vpnConnectionId: ``AWS::EC2::VPNConnectionRoute.VpnConnectionId``.
        """
        props: CfnVPNConnectionRouteProps = {"destinationCidrBlock": destination_cidr_block, "vpnConnectionId": vpn_connection_id}

        jsii.create(CfnVPNConnectionRoute, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPNConnectionRouteProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpnConnectionRouteName")
    def vpn_connection_route_name(self) -> str:
        return jsii.get(self, "vpnConnectionRouteName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNConnectionRouteProps", jsii_struct_bases=[])
class CfnVPNConnectionRouteProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::VPNConnectionRoute``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection-route.html
    """
    destinationCidrBlock: str
    """``AWS::EC2::VPNConnectionRoute.DestinationCidrBlock``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection-route.html#cfn-ec2-vpnconnectionroute-cidrblock
    """

    vpnConnectionId: str
    """``AWS::EC2::VPNConnectionRoute.VpnConnectionId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-connection-route.html#cfn-ec2-vpnconnectionroute-connectionid
    """

class CfnVPNGateway(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNGateway"):
    """A CloudFormation ``AWS::EC2::VPNGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html
    cloudformationResource:
        AWS::EC2::VPNGateway
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, type: str, amazon_side_asn: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::EC2::VPNGateway``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            type: ``AWS::EC2::VPNGateway.Type``.
            amazonSideAsn: ``AWS::EC2::VPNGateway.AmazonSideAsn``.
            tags: ``AWS::EC2::VPNGateway.Tags``.
        """
        props: CfnVPNGatewayProps = {"type": type}

        if amazon_side_asn is not None:
            props["amazonSideAsn"] = amazon_side_asn

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnVPNGateway, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPNGatewayProps":
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

    @property
    @jsii.member(jsii_name="vpnGatewayName")
    def vpn_gateway_name(self) -> str:
        return jsii.get(self, "vpnGatewayName")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVPNGatewayProps(jsii.compat.TypedDict, total=False):
    amazonSideAsn: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::VPNGateway.AmazonSideAsn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html#cfn-ec2-vpngateway-amazonsideasn
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::VPNGateway.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html#cfn-ec2-vpngateway-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNGatewayProps", jsii_struct_bases=[_CfnVPNGatewayProps])
class CfnVPNGatewayProps(_CfnVPNGatewayProps):
    """Properties for defining a ``AWS::EC2::VPNGateway``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html
    """
    type: str
    """``AWS::EC2::VPNGateway.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gateway.html#cfn-ec2-vpngateway-type
    """

class CfnVPNGatewayRoutePropagation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVPNGatewayRoutePropagation"):
    """A CloudFormation ``AWS::EC2::VPNGatewayRoutePropagation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gatewayrouteprop.html
    cloudformationResource:
        AWS::EC2::VPNGatewayRoutePropagation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, route_table_ids: typing.List[str], vpn_gateway_id: str) -> None:
        """Create a new ``AWS::EC2::VPNGatewayRoutePropagation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            routeTableIds: ``AWS::EC2::VPNGatewayRoutePropagation.RouteTableIds``.
            vpnGatewayId: ``AWS::EC2::VPNGatewayRoutePropagation.VpnGatewayId``.
        """
        props: CfnVPNGatewayRoutePropagationProps = {"routeTableIds": route_table_ids, "vpnGatewayId": vpn_gateway_id}

        jsii.create(CfnVPNGatewayRoutePropagation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVPNGatewayRoutePropagationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="vpnGatewayRoutePropagationName")
    def vpn_gateway_route_propagation_name(self) -> str:
        return jsii.get(self, "vpnGatewayRoutePropagationName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVPNGatewayRoutePropagationProps", jsii_struct_bases=[])
class CfnVPNGatewayRoutePropagationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::VPNGatewayRoutePropagation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gatewayrouteprop.html
    """
    routeTableIds: typing.List[str]
    """``AWS::EC2::VPNGatewayRoutePropagation.RouteTableIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gatewayrouteprop.html#cfn-ec2-vpngatewayrouteprop-routetableids
    """

    vpnGatewayId: str
    """``AWS::EC2::VPNGatewayRoutePropagation.VpnGatewayId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ec2-vpn-gatewayrouteprop.html#cfn-ec2-vpngatewayrouteprop-vpngatewayid
    """

class CfnVolume(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVolume"):
    """A CloudFormation ``AWS::EC2::Volume``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html
    cloudformationResource:
        AWS::EC2::Volume
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, auto_enable_io: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, iops: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, kms_key_id: typing.Optional[str]=None, size: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, snapshot_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, volume_type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EC2::Volume``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            availabilityZone: ``AWS::EC2::Volume.AvailabilityZone``.
            autoEnableIo: ``AWS::EC2::Volume.AutoEnableIO``.
            encrypted: ``AWS::EC2::Volume.Encrypted``.
            iops: ``AWS::EC2::Volume.Iops``.
            kmsKeyId: ``AWS::EC2::Volume.KmsKeyId``.
            size: ``AWS::EC2::Volume.Size``.
            snapshotId: ``AWS::EC2::Volume.SnapshotId``.
            tags: ``AWS::EC2::Volume.Tags``.
            volumeType: ``AWS::EC2::Volume.VolumeType``.
        """
        props: CfnVolumeProps = {"availabilityZone": availability_zone}

        if auto_enable_io is not None:
            props["autoEnableIo"] = auto_enable_io

        if encrypted is not None:
            props["encrypted"] = encrypted

        if iops is not None:
            props["iops"] = iops

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if size is not None:
            props["size"] = size

        if snapshot_id is not None:
            props["snapshotId"] = snapshot_id

        if tags is not None:
            props["tags"] = tags

        if volume_type is not None:
            props["volumeType"] = volume_type

        jsii.create(CfnVolume, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVolumeProps":
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

    @property
    @jsii.member(jsii_name="volumeId")
    def volume_id(self) -> str:
        return jsii.get(self, "volumeId")


class CfnVolumeAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CfnVolumeAttachment"):
    """A CloudFormation ``AWS::EC2::VolumeAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html
    cloudformationResource:
        AWS::EC2::VolumeAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, device: str, instance_id: str, volume_id: str) -> None:
        """Create a new ``AWS::EC2::VolumeAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            device: ``AWS::EC2::VolumeAttachment.Device``.
            instanceId: ``AWS::EC2::VolumeAttachment.InstanceId``.
            volumeId: ``AWS::EC2::VolumeAttachment.VolumeId``.
        """
        props: CfnVolumeAttachmentProps = {"device": device, "instanceId": instance_id, "volumeId": volume_id}

        jsii.create(CfnVolumeAttachment, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnVolumeAttachmentProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="volumeAttachmentId")
    def volume_attachment_id(self) -> str:
        return jsii.get(self, "volumeAttachmentId")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVolumeAttachmentProps", jsii_struct_bases=[])
class CfnVolumeAttachmentProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::EC2::VolumeAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html
    """
    device: str
    """``AWS::EC2::VolumeAttachment.Device``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html#cfn-ec2-ebs-volumeattachment-device
    """

    instanceId: str
    """``AWS::EC2::VolumeAttachment.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html#cfn-ec2-ebs-volumeattachment-instanceid
    """

    volumeId: str
    """``AWS::EC2::VolumeAttachment.VolumeId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volumeattachment.html#cfn-ec2-ebs-volumeattachment-volumeid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnVolumeProps(jsii.compat.TypedDict, total=False):
    autoEnableIo: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Volume.AutoEnableIO``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-autoenableio
    """
    encrypted: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EC2::Volume.Encrypted``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-encrypted
    """
    iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::Volume.Iops``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-iops
    """
    kmsKeyId: str
    """``AWS::EC2::Volume.KmsKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-kmskeyid
    """
    size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EC2::Volume.Size``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-size
    """
    snapshotId: str
    """``AWS::EC2::Volume.SnapshotId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-snapshotid
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::EC2::Volume.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-tags
    """
    volumeType: str
    """``AWS::EC2::Volume.VolumeType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-volumetype
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.CfnVolumeProps", jsii_struct_bases=[_CfnVolumeProps])
class CfnVolumeProps(_CfnVolumeProps):
    """Properties for defining a ``AWS::EC2::Volume``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html
    """
    availabilityZone: str
    """``AWS::EC2::Volume.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ec2-ebs-volume.html#cfn-ec2-ebs-volume-availabilityzone
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ConnectionRule(jsii.compat.TypedDict, total=False):
    description: str
    """Description of this connection.

    It is applied to both the ingress rule
    and the egress rule.

    Default:
        No description
    """
    protocol: str
    """The IP protocol name (tcp, udp, icmp) or number (see Protocol Numbers). Use -1 to specify all protocols. If you specify -1, or a protocol number other than tcp, udp, icmp, or 58 (ICMPv6), traffic on all ports is allowed, regardless of any ports you specify. For tcp, udp, and icmp, you must specify a port range. For protocol 58 (ICMPv6), you can optionally specify a port range; if you don't, traffic for all types and codes is allowed.

    Default:
        tcp
    """
    toPort: jsii.Number
    """End of port range for the TCP and UDP protocols, or an ICMP code.

    If you specify icmp for the IpProtocol property, you can specify -1 as a
    wildcard (i.e., any ICMP code).

    Default:
        If toPort is not specified, it will be the same as fromPort.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.ConnectionRule", jsii_struct_bases=[_ConnectionRule])
class ConnectionRule(_ConnectionRule):
    fromPort: jsii.Number
    """Start of port range for the TCP and UDP protocols, or an ICMP type number.

    If you specify icmp for the IpProtocol property, you can specify
    -1 as a wildcard (i.e., any ICMP type number).
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.ConnectionsProps", jsii_struct_bases=[])
class ConnectionsProps(jsii.compat.TypedDict, total=False):
    """Properties to intialize a new Connections object."""
    defaultPortRange: "IPortRange"
    """Default port range for initiating connections to and from this object.

    Default:
        No default port range
    """

    securityGroupRule: "ISecurityGroupRule"
    """Class that represents the rule by which others can connect to this connectable.

    This object is required, but will be derived from securityGroup if that is passed.

    Default:
        Derived from securityGroup if set.
    """

    securityGroups: typing.List["ISecurityGroup"]
    """What securityGroup(s) this object is managing connections for.

    Default:
        No security groups
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.DefaultInstanceTenancy")
class DefaultInstanceTenancy(enum.Enum):
    """The default tenancy of instances launched into the VPC."""
    Default = "Default"
    """Instances can be launched with any tenancy."""
    Dedicated = "Dedicated"
    """Any instance launched into the VPC automatically has dedicated tenancy, unless you launch it with the default tenancy."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _GatewayVpcEndpointOptions(jsii.compat.TypedDict, total=False):
    subnets: typing.List["SubnetSelection"]
    """Where to add endpoint routing.

    Default:
        private subnets
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.GatewayVpcEndpointOptions", jsii_struct_bases=[_GatewayVpcEndpointOptions])
class GatewayVpcEndpointOptions(_GatewayVpcEndpointOptions):
    """Options to add a gateway endpoint to a VPC."""
    service: "IGatewayVpcEndpointService"
    """The service to use for this gateway VPC endpoint."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.GatewayVpcEndpointProps", jsii_struct_bases=[GatewayVpcEndpointOptions])
class GatewayVpcEndpointProps(GatewayVpcEndpointOptions, jsii.compat.TypedDict):
    """Construction properties for a GatewayVpcEndpoint."""
    vpc: "IVpc"
    """The VPC network in which the gateway endpoint will be used."""

@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IConnectable")
class IConnectable(jsii.compat.Protocol):
    """The goal of this module is to make possible to write statements like this:.

    Example::

        *  database.connections.allowFrom(fleet);
        *  fleet.connections.allowTo(database);
        *  rdgw.connections.allowFromCidrIp('0.3.1.5/86');
        *  rgdw.connections.allowTrafficTo(fleet, new AllPorts());
        *  ```

       The insight here is that some connecting peers have information on what ports should
       be involved in the connection, and some don't.
       An object that has a Connections object
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _IConnectableProxy

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        ...


class _IConnectableProxy():
    """The goal of this module is to make possible to write statements like this:.

    Example::

        *  database.connections.allowFrom(fleet);
        *  fleet.connections.allowTo(database);
        *  rdgw.connections.allowFromCidrIp('0.3.1.5/86');
        *  rgdw.connections.allowTrafficTo(fleet, new AllPorts());
        *  ```

       The insight here is that some connecting peers have information on what ports should
       be involved in the connection, and some don't.
       An object that has a Connections object
    """
    __jsii_type__ = "@aws-cdk/aws-ec2.IConnectable"
    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")


@jsii.implements(IConnectable)
class Connections(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.Connections"):
    """Manage the allowed network connections for constructs with Security Groups.

    Security Groups can be thought of as a firewall for network-connected
    devices. This class makes it easy to allow network connections to and
    from security groups, and between security groups individually. When
    establishing connectivity between security groups, it will automatically
    add rules in both security groups

    This object can manage one or more security groups.
    """
    def __init__(self, *, default_port_range: typing.Optional["IPortRange"]=None, security_group_rule: typing.Optional["ISecurityGroupRule"]=None, security_groups: typing.Optional[typing.List["ISecurityGroup"]]=None) -> None:
        """
        Arguments:
            props: -
            defaultPortRange: Default port range for initiating connections to and from this object. Default: No default port range
            securityGroupRule: Class that represents the rule by which others can connect to this connectable. This object is required, but will be derived from securityGroup if that is passed. Default: Derived from securityGroup if set.
            securityGroups: What securityGroup(s) this object is managing connections for. Default: No security groups
        """
        props: ConnectionsProps = {}

        if default_port_range is not None:
            props["defaultPortRange"] = default_port_range

        if security_group_rule is not None:
            props["securityGroupRule"] = security_group_rule

        if security_groups is not None:
            props["securityGroups"] = security_groups

        jsii.create(Connections, self, [props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, *security_groups: "ISecurityGroup") -> None:
        """Add a security group to the list of security groups managed by this object.

        Arguments:
            securityGroups: -
        """
        return jsii.invoke(self, "addSecurityGroup", [security_groups])

    @jsii.member(jsii_name="allowDefaultPortFrom")
    def allow_default_port_from(self, other: "IConnectable", description: typing.Optional[str]=None) -> None:
        """Allow connections from the peer on our default port.

        Even if the peer has a default port, we will always use our default port.

        Arguments:
            other: -
            description: -
        """
        return jsii.invoke(self, "allowDefaultPortFrom", [other, description])

    @jsii.member(jsii_name="allowDefaultPortFromAnyIpv4")
    def allow_default_port_from_any_ipv4(self, description: typing.Optional[str]=None) -> None:
        """Allow default connections from all IPv4 ranges.

        Arguments:
            description: -
        """
        return jsii.invoke(self, "allowDefaultPortFromAnyIpv4", [description])

    @jsii.member(jsii_name="allowDefaultPortInternally")
    def allow_default_port_internally(self, description: typing.Optional[str]=None) -> None:
        """Allow hosts inside the security group to connect to each other.

        Arguments:
            description: -
        """
        return jsii.invoke(self, "allowDefaultPortInternally", [description])

    @jsii.member(jsii_name="allowDefaultPortTo")
    def allow_default_port_to(self, other: "IConnectable", description: typing.Optional[str]=None) -> None:
        """Allow connections from the peer on our default port.

        Even if the peer has a default port, we will always use our default port.

        Arguments:
            other: -
            description: -
        """
        return jsii.invoke(self, "allowDefaultPortTo", [other, description])

    @jsii.member(jsii_name="allowFrom")
    def allow_from(self, other: "IConnectable", port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        """Allow connections from the peer on the given port.

        Arguments:
            other: -
            portRange: -
            description: -
        """
        return jsii.invoke(self, "allowFrom", [other, port_range, description])

    @jsii.member(jsii_name="allowFromAnyIPv4")
    def allow_from_any_i_pv4(self, port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        """Allow from any IPv4 ranges.

        Arguments:
            portRange: -
            description: -
        """
        return jsii.invoke(self, "allowFromAnyIPv4", [port_range, description])

    @jsii.member(jsii_name="allowInternally")
    def allow_internally(self, port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        """Allow hosts inside the security group to connect to each other on the given port.

        Arguments:
            portRange: -
            description: -
        """
        return jsii.invoke(self, "allowInternally", [port_range, description])

    @jsii.member(jsii_name="allowTo")
    def allow_to(self, other: "IConnectable", port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        """Allow connections to the peer on the given port.

        Arguments:
            other: -
            portRange: -
            description: -
        """
        return jsii.invoke(self, "allowTo", [other, port_range, description])

    @jsii.member(jsii_name="allowToAnyIPv4")
    def allow_to_any_i_pv4(self, port_range: "IPortRange", description: typing.Optional[str]=None) -> None:
        """Allow to all IPv4 ranges.

        Arguments:
            portRange: -
            description: -
        """
        return jsii.invoke(self, "allowToAnyIPv4", [port_range, description])

    @jsii.member(jsii_name="allowToDefaultPort")
    def allow_to_default_port(self, other: "IConnectable", description: typing.Optional[str]=None) -> None:
        """Allow connections to the security group on their default port.

        Arguments:
            other: -
            description: -
        """
        return jsii.invoke(self, "allowToDefaultPort", [other, description])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.List["ISecurityGroup"]:
        return jsii.get(self, "securityGroups")

    @property
    @jsii.member(jsii_name="defaultPortRange")
    def default_port_range(self) -> typing.Optional["IPortRange"]:
        """The default port configured for this connection peer, if available."""
        return jsii.get(self, "defaultPortRange")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IGatewayVpcEndpointService")
class IGatewayVpcEndpointService(jsii.compat.Protocol):
    """A service for a gateway VPC endpoint."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IGatewayVpcEndpointServiceProxy

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the service."""
        ...


class _IGatewayVpcEndpointServiceProxy():
    """A service for a gateway VPC endpoint."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IGatewayVpcEndpointService"
    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the service."""
        return jsii.get(self, "name")


@jsii.implements(IGatewayVpcEndpointService)
class GatewayVpcEndpointAwsService(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.GatewayVpcEndpointAwsService"):
    """An AWS service for a gateway VPC endpoint."""
    def __init__(self, name: str, prefix: typing.Optional[str]=None) -> None:
        """
        Arguments:
            name: -
            prefix: -
        """
        jsii.create(GatewayVpcEndpointAwsService, self, [name, prefix])

    @classproperty
    @jsii.member(jsii_name="DynamoDb")
    def DYNAMO_DB(cls) -> "GatewayVpcEndpointAwsService":
        return jsii.sget(cls, "DynamoDb")

    @classproperty
    @jsii.member(jsii_name="S3")
    def S3(cls) -> "GatewayVpcEndpointAwsService":
        return jsii.sget(cls, "S3")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the service."""
        return jsii.get(self, "name")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IInterfaceVpcEndpointService")
class IInterfaceVpcEndpointService(jsii.compat.Protocol):
    """A service for an interface VPC endpoint."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IInterfaceVpcEndpointServiceProxy

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the service."""
        ...

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The port of the service."""
        ...


class _IInterfaceVpcEndpointServiceProxy():
    """A service for an interface VPC endpoint."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IInterfaceVpcEndpointService"
    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the service."""
        return jsii.get(self, "name")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The port of the service."""
        return jsii.get(self, "port")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IMachineImageSource")
class IMachineImageSource(jsii.compat.Protocol):
    """Interface for classes that can select an appropriate machine image to use."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IMachineImageSourceProxy

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        """Return the image to use in the given context.

        Arguments:
            scope: -
        """
        ...


class _IMachineImageSourceProxy():
    """Interface for classes that can select an appropriate machine image to use."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IMachineImageSource"
    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        """Return the image to use in the given context.

        Arguments:
            scope: -
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.implements(IMachineImageSource)
class AmazonLinuxImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AmazonLinuxImage"):
    """Selects the latest version of Amazon Linux.

    The AMI ID is selected using the values published to the SSM parameter store.
    """
    def __init__(self, *, edition: typing.Optional["AmazonLinuxEdition"]=None, generation: typing.Optional["AmazonLinuxGeneration"]=None, storage: typing.Optional["AmazonLinuxStorage"]=None, virtualization: typing.Optional["AmazonLinuxVirt"]=None) -> None:
        """
        Arguments:
            props: -
            edition: What edition of Amazon Linux to use. Default: Standard
            generation: What generation of Amazon Linux to use. Default: AmazonLinux
            storage: What storage backed image to use. Default: GeneralPurpose
            virtualization: Virtualization type. Default: HVM
        """
        props: AmazonLinuxImageProps = {}

        if edition is not None:
            props["edition"] = edition

        if generation is not None:
            props["generation"] = generation

        if storage is not None:
            props["storage"] = storage

        if virtualization is not None:
            props["virtualization"] = virtualization

        jsii.create(AmazonLinuxImage, self, [props])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        """Return the image to use in the given context.

        Arguments:
            scope: -
        """
        return jsii.invoke(self, "getImage", [scope])


@jsii.implements(IMachineImageSource)
class GenericLinuxImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.GenericLinuxImage"):
    """Construct a Linux machine image from an AMI map.

    Linux images IDs are not published to SSM parameter store yet, so you'll have to
    manually specify an AMI map.
    """
    def __init__(self, ami_map: typing.Mapping[str,str]) -> None:
        """
        Arguments:
            amiMap: -
        """
        jsii.create(GenericLinuxImage, self, [ami_map])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        """Return the image to use in the given context.

        Arguments:
            scope: -
        """
        return jsii.invoke(self, "getImage", [scope])

    @property
    @jsii.member(jsii_name="amiMap")
    def ami_map(self) -> typing.Mapping[str,str]:
        return jsii.get(self, "amiMap")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IPortRange")
class IPortRange(jsii.compat.Protocol):
    """Interface for classes that provide the connection-specification parts of a security group rule."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IPortRangeProxy

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        ...

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        ...


class _IPortRangeProxy():
    """Interface for classes that provide the connection-specification parts of a security group rule."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IPortRange"
    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])


@jsii.implements(IPortRange)
class AllTraffic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AllTraffic"):
    """All Traffic."""
    def __init__(self) -> None:
        jsii.create(AllTraffic, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.ISecurityGroupRule")
class ISecurityGroupRule(jsii.compat.Protocol):
    """Interface for classes that provide the peer-specification parts of a security group rule."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecurityGroupRuleProxy

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule can be inlined into a SecurityGroup or not."""
        ...

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A unique identifier for this connection peer."""
        ...

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        """Produce the egress rule JSON for the given connection."""
        ...

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        """Produce the ingress rule JSON for the given connection."""
        ...


class _ISecurityGroupRuleProxy():
    """Interface for classes that provide the peer-specification parts of a security group rule."""
    __jsii_type__ = "@aws-cdk/aws-ec2.ISecurityGroupRule"
    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule can be inlined into a SecurityGroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A unique identifier for this connection peer."""
        return jsii.get(self, "uniqueId")

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        """Produce the egress rule JSON for the given connection."""
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        """Produce the ingress rule JSON for the given connection."""
        return jsii.invoke(self, "toIngressRuleJSON", [])


@jsii.implements(ISecurityGroupRule, IConnectable)
class CidrIPv4(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CidrIPv4"):
    """A connection to and from a given IP range."""
    def __init__(self, cidr_ip: str) -> None:
        """
        Arguments:
            cidrIp: -
        """
        jsii.create(CidrIPv4, self, [cidr_ip])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        """Produce the egress rule JSON for the given connection."""
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        """Produce the ingress rule JSON for the given connection."""
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule can be inlined into a SecurityGroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="cidrIp")
    def cidr_ip(self) -> str:
        return jsii.get(self, "cidrIp")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A unique identifier for this connection peer."""
        return jsii.get(self, "uniqueId")


class AnyIPv4(CidrIPv4, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AnyIPv4"):
    """Any IPv4 address."""
    def __init__(self) -> None:
        jsii.create(AnyIPv4, self, [])


@jsii.implements(ISecurityGroupRule, IConnectable)
class CidrIPv6(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.CidrIPv6"):
    """A connection to a from a given IPv6 range."""
    def __init__(self, cidr_ipv6: str) -> None:
        """
        Arguments:
            cidrIpv6: -
        """
        jsii.create(CidrIPv6, self, [cidr_ipv6])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        """Produce the egress rule JSON for the given connection."""
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        """Produce the ingress rule JSON for the given connection."""
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule can be inlined into a SecurityGroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="cidrIpv6")
    def cidr_ipv6(self) -> str:
        return jsii.get(self, "cidrIpv6")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A unique identifier for this connection peer."""
        return jsii.get(self, "uniqueId")


class AnyIPv6(CidrIPv6, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.AnyIPv6"):
    """Any IPv6 address."""
    def __init__(self) -> None:
        jsii.create(AnyIPv6, self, [])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.ISecurityGroup")
class ISecurityGroup(aws_cdk.cdk.IResource, ISecurityGroupRule, IConnectable, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISecurityGroupProxy

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """ID for the current security group.

        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        """Add an egress rule for the current security group.

        ``remoteRule`` controls where the Rule object is created if the peer is also a
        securityGroup and they are in different stack. If false (default) the
        rule object is created under the current SecurityGroup object. If true and the
        peer is also a SecurityGroup, the rule object is created under the remote
        SecurityGroup object.

        Arguments:
            peer: -
            connection: -
            description: -
            remoteRule: -
        """
        ...

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        """Add an ingress rule for the current security group.

        ``remoteRule`` controls where the Rule object is created if the peer is also a
        securityGroup and they are in different stack. If false (default) the
        rule object is created under the current SecurityGroup object. If true and the
        peer is also a SecurityGroup, the rule object is created under the remote
        SecurityGroup object.

        Arguments:
            peer: -
            connection: -
            description: -
            remoteRule: -
        """
        ...


class _ISecurityGroupProxy(jsii.proxy_for(aws_cdk.cdk.IResource), jsii.proxy_for(ISecurityGroupRule), jsii.proxy_for(IConnectable)):
    __jsii_type__ = "@aws-cdk/aws-ec2.ISecurityGroup"
    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """ID for the current security group.

        attribute:
            true
        """
        return jsii.get(self, "securityGroupId")

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        """Add an egress rule for the current security group.

        ``remoteRule`` controls where the Rule object is created if the peer is also a
        securityGroup and they are in different stack. If false (default) the
        rule object is created under the current SecurityGroup object. If true and the
        peer is also a SecurityGroup, the rule object is created under the remote
        SecurityGroup object.

        Arguments:
            peer: -
            connection: -
            description: -
            remoteRule: -
        """
        return jsii.invoke(self, "addEgressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        """Add an ingress rule for the current security group.

        ``remoteRule`` controls where the Rule object is created if the peer is also a
        securityGroup and they are in different stack. If false (default) the
        rule object is created under the current SecurityGroup object. If true and the
        peer is also a SecurityGroup, the rule object is created under the remote
        SecurityGroup object.

        Arguments:
            peer: -
            connection: -
            description: -
            remoteRule: -
        """
        return jsii.invoke(self, "addIngressRule", [peer, connection, description, remote_rule])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.ISubnet")
class ISubnet(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ISubnetProxy

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> str:
        """The Availability Zone the subnet is located in."""
        ...

    @property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> aws_cdk.cdk.IDependable:
        """Dependable that can be depended upon to force internet connectivity established on the VPC."""
        ...

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        """The subnetId for this particular subnet.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> typing.Optional[str]:
        """Route table ID."""
        ...


class _ISubnetProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-ec2.ISubnet"
    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> str:
        """The Availability Zone the subnet is located in."""
        return jsii.get(self, "availabilityZone")

    @property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> aws_cdk.cdk.IDependable:
        """Dependable that can be depended upon to force internet connectivity established on the VPC."""
        return jsii.get(self, "internetConnectivityEstablished")

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        """The subnetId for this particular subnet.

        attribute:
            true
        """
        return jsii.get(self, "subnetId")

    @property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> typing.Optional[str]:
        """Route table ID."""
        return jsii.get(self, "routeTableId")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IPrivateSubnet")
class IPrivateSubnet(ISubnet, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPrivateSubnetProxy

    pass

class _IPrivateSubnetProxy(jsii.proxy_for(ISubnet)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IPrivateSubnet"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IPublicSubnet")
class IPublicSubnet(ISubnet, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPublicSubnetProxy

    pass

class _IPublicSubnetProxy(jsii.proxy_for(ISubnet)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IPublicSubnet"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IVpc")
class IVpc(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IVpcProxy

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        """AZs for this VPC."""
        ...

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["ISubnet"]:
        """List of isolated subnets in this VPC."""
        ...

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["ISubnet"]:
        """List of private subnets in this VPC."""
        ...

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["ISubnet"]:
        """List of public subnets in this VPC."""
        ...

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """Region where this VPC is located."""
        ...

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        """Identifier for this VPC.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        """Identifier for the VPN gateway."""
        ...

    @jsii.member(jsii_name="addInterfaceEndpoint")
    def add_interface_endpoint(self, id: str, *, service: "IInterfaceVpcEndpointService", private_dns_enabled: typing.Optional[bool]=None, subnets: typing.Optional["SubnetSelection"]=None) -> "InterfaceVpcEndpoint":
        """Adds a new interface endpoint to this VPC.

        Arguments:
            id: -
            options: -
            service: The service to use for this interface VPC endpoint.
            privateDnsEnabled: Whether to associate a private hosted zone with the specified VPC. This allows you to make requests to the service using its default DNS hostname. Default: true
            subnets: The subnets in which to create an endpoint network interface. At most one per availability zone. Default: private subnets
        """
        ...

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(self, id: str, *, ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> "VpnConnection":
        """Adds a new VPN connection to this VPC.

        Arguments:
            id: -
            options: -
            ip: The ip address of the customer gateway.
            asn: The ASN of the customer gateway. Default: 65000
            staticRoutes: The static routes to be routed from the VPN gateway to the customer gateway. Default: Dynamic routing (BGP)
            tunnelOptions: The tunnel options for the VPN connection. At most two elements (one per tunnel). Duplicates not allowed. Default: Amazon generated tunnel options
        """
        ...

    @jsii.member(jsii_name="isPublicSubnets")
    def is_public_subnets(self, subnet_ids: typing.List[str]) -> bool:
        """Return whether all of the given subnets are from the VPC's public subnets.

        Arguments:
            subnetIds: -
        """
        ...

    @jsii.member(jsii_name="selectSubnetIds")
    def select_subnet_ids(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List[str]:
        """Return IDs of the subnets appropriate for the given selection strategy.

        Requires that at least one subnet is matched, throws a descriptive
        error message otherwise.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private

        Deprecated:
            Use selectSubnets() instead.
        """
        ...

    @jsii.member(jsii_name="selectSubnets")
    def select_subnets(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> "SelectedSubnets":
        """Return information on the subnets appropriate for the given selection strategy.

        Requires that at least one subnet is matched, throws a descriptive
        error message otherwise.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private
        """
        ...


class _IVpcProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IVpc"
    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        """AZs for this VPC."""
        return jsii.get(self, "availabilityZones")

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["ISubnet"]:
        """List of isolated subnets in this VPC."""
        return jsii.get(self, "isolatedSubnets")

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["ISubnet"]:
        """List of private subnets in this VPC."""
        return jsii.get(self, "privateSubnets")

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["ISubnet"]:
        """List of public subnets in this VPC."""
        return jsii.get(self, "publicSubnets")

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """Region where this VPC is located."""
        return jsii.get(self, "region")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        """Identifier for this VPC.

        attribute:
            true
        """
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        """Identifier for the VPN gateway."""
        return jsii.get(self, "vpnGatewayId")

    @jsii.member(jsii_name="addInterfaceEndpoint")
    def add_interface_endpoint(self, id: str, *, service: "IInterfaceVpcEndpointService", private_dns_enabled: typing.Optional[bool]=None, subnets: typing.Optional["SubnetSelection"]=None) -> "InterfaceVpcEndpoint":
        """Adds a new interface endpoint to this VPC.

        Arguments:
            id: -
            options: -
            service: The service to use for this interface VPC endpoint.
            privateDnsEnabled: Whether to associate a private hosted zone with the specified VPC. This allows you to make requests to the service using its default DNS hostname. Default: true
            subnets: The subnets in which to create an endpoint network interface. At most one per availability zone. Default: private subnets
        """
        options: InterfaceVpcEndpointOptions = {"service": service}

        if private_dns_enabled is not None:
            options["privateDnsEnabled"] = private_dns_enabled

        if subnets is not None:
            options["subnets"] = subnets

        return jsii.invoke(self, "addInterfaceEndpoint", [id, options])

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(self, id: str, *, ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> "VpnConnection":
        """Adds a new VPN connection to this VPC.

        Arguments:
            id: -
            options: -
            ip: The ip address of the customer gateway.
            asn: The ASN of the customer gateway. Default: 65000
            staticRoutes: The static routes to be routed from the VPN gateway to the customer gateway. Default: Dynamic routing (BGP)
            tunnelOptions: The tunnel options for the VPN connection. At most two elements (one per tunnel). Duplicates not allowed. Default: Amazon generated tunnel options
        """
        options: VpnConnectionOptions = {"ip": ip}

        if asn is not None:
            options["asn"] = asn

        if static_routes is not None:
            options["staticRoutes"] = static_routes

        if tunnel_options is not None:
            options["tunnelOptions"] = tunnel_options

        return jsii.invoke(self, "addVpnConnection", [id, options])

    @jsii.member(jsii_name="isPublicSubnets")
    def is_public_subnets(self, subnet_ids: typing.List[str]) -> bool:
        """Return whether all of the given subnets are from the VPC's public subnets.

        Arguments:
            subnetIds: -
        """
        return jsii.invoke(self, "isPublicSubnets", [subnet_ids])

    @jsii.member(jsii_name="selectSubnetIds")
    def select_subnet_ids(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List[str]:
        """Return IDs of the subnets appropriate for the given selection strategy.

        Requires that at least one subnet is matched, throws a descriptive
        error message otherwise.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private

        Deprecated:
            Use selectSubnets() instead.
        """
        selection: SubnetSelection = {}

        if one_per_az is not None:
            selection["onePerAz"] = one_per_az

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "selectSubnetIds", [selection])

    @jsii.member(jsii_name="selectSubnets")
    def select_subnets(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> "SelectedSubnets":
        """Return information on the subnets appropriate for the given selection strategy.

        Requires that at least one subnet is matched, throws a descriptive
        error message otherwise.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private
        """
        selection: SubnetSelection = {}

        if one_per_az is not None:
            selection["onePerAz"] = one_per_az

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "selectSubnets", [selection])


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IVpcEndpoint")
class IVpcEndpoint(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """A VPC endpoint."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IVpcEndpointProxy

    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        """The VPC endpoint identifier.

        attribute:
            true
        """
        ...


class _IVpcEndpointProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """A VPC endpoint."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IVpcEndpoint"
    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        """The VPC endpoint identifier.

        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointId")


@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IGatewayVpcEndpoint")
class IGatewayVpcEndpoint(IVpcEndpoint, jsii.compat.Protocol):
    """A gateway VPC endpoint."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IGatewayVpcEndpointProxy

    pass

class _IGatewayVpcEndpointProxy(jsii.proxy_for(IVpcEndpoint)):
    """A gateway VPC endpoint."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IGatewayVpcEndpoint"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IInterfaceVpcEndpoint")
class IInterfaceVpcEndpoint(IVpcEndpoint, IConnectable, jsii.compat.Protocol):
    """An interface VPC endpoint."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IInterfaceVpcEndpointProxy

    pass

class _IInterfaceVpcEndpointProxy(jsii.proxy_for(IVpcEndpoint), jsii.proxy_for(IConnectable)):
    """An interface VPC endpoint."""
    __jsii_type__ = "@aws-cdk/aws-ec2.IInterfaceVpcEndpoint"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-ec2.IVpnConnection")
class IVpnConnection(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IVpnConnectionProxy

    @property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        """The ASN of the customer gateway."""
        ...

    @property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> str:
        """The id of the customer gateway."""
        ...

    @property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> str:
        """The ip address of the customer gateway."""
        ...

    @property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> str:
        """The id of the VPN connection."""
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this VPNConnection.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        ...

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The bytes received through the VPN tunnel.

        Sum over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        ...

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The bytes sent through the VPN tunnel.

        Sum over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        ...

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The state of the tunnel. 0 indicates DOWN and 1 indicates UP.

        Average over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        ...


class _IVpnConnectionProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    __jsii_type__ = "@aws-cdk/aws-ec2.IVpnConnection"
    @property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        """The ASN of the customer gateway."""
        return jsii.get(self, "customerGatewayAsn")

    @property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> str:
        """The id of the customer gateway."""
        return jsii.get(self, "customerGatewayId")

    @property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> str:
        """The ip address of the customer gateway."""
        return jsii.get(self, "customerGatewayIp")

    @property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> str:
        """The id of the VPN connection."""
        return jsii.get(self, "vpnId")

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this VPNConnection.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The bytes received through the VPN tunnel.

        Sum over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTunnelDataIn", [props])

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The bytes sent through the VPN tunnel.

        Sum over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTunnelDataOut", [props])

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The state of the tunnel. 0 indicates DOWN and 1 indicates UP.

        Average over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTunnelState", [props])


@jsii.implements(IPortRange)
class IcmpAllTypeCodes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpAllTypeCodes"):
    """All ICMP Codes for a given ICMP Type."""
    def __init__(self, type: jsii.Number) -> None:
        """
        Arguments:
            type: -
        """
        jsii.create(IcmpAllTypeCodes, self, [type])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return jsii.get(self, "type")


@jsii.implements(IPortRange)
class IcmpAllTypesAndCodes(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpAllTypesAndCodes"):
    """All ICMP Types & Codes."""
    def __init__(self) -> None:
        jsii.create(IcmpAllTypesAndCodes, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class IcmpPing(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpPing"):
    """ICMP Ping traffic."""
    def __init__(self) -> None:
        jsii.create(IcmpPing, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class IcmpTypeAndCode(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.IcmpTypeAndCode"):
    """A set of matching ICMP Type & Code."""
    def __init__(self, type: jsii.Number, code: jsii.Number) -> None:
        """
        Arguments:
            type: -
            code: -
        """
        jsii.create(IcmpTypeAndCode, self, [type, code])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="code")
    def code(self) -> jsii.Number:
        return jsii.get(self, "code")

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> jsii.Number:
        return jsii.get(self, "type")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.InstanceClass")
class InstanceClass(enum.Enum):
    """What class and generation of instance to use.

    We have both symbolic and concrete enums for every type.

    The first are for people that want to specify by purpose,
    the second one are for people who already know exactly what
    'R4' means.
    """
    Standard3 = "Standard3"
    """Standard instances, 3rd generation."""
    Standard4 = "Standard4"
    """Standard instances, 4th generation."""
    Standard5 = "Standard5"
    """Standard instances, 5th generation."""
    Memory3 = "Memory3"
    """Memory optimized instances, 3rd generation."""
    Memory4 = "Memory4"
    """Memory optimized instances, 3rd generation."""
    Compute3 = "Compute3"
    """Compute optimized instances, 3rd generation."""
    Compute4 = "Compute4"
    """Compute optimized instances, 4th generation."""
    Compute5 = "Compute5"
    """Compute optimized instances, 5th generation."""
    Storage2 = "Storage2"
    """Storage-optimized instances, 2nd generation."""
    StorageCompute1 = "StorageCompute1"
    """Storage/compute balanced instances, 1st generation."""
    Io3 = "Io3"
    """I/O-optimized instances, 3rd generation."""
    Burstable2 = "Burstable2"
    """Burstable instances, 2nd generation."""
    Burstable3 = "Burstable3"
    """Burstable instances, 3rd generation."""
    MemoryIntensive1 = "MemoryIntensive1"
    """Memory-intensive instances, 1st generation."""
    MemoryIntensive1Extended = "MemoryIntensive1Extended"
    """Memory-intensive instances, extended, 1st generation."""
    Fpga1 = "Fpga1"
    """Instances with customizable hardware acceleration, 1st generation."""
    Graphics3 = "Graphics3"
    """Graphics-optimized instances, 3rd generation."""
    Parallel2 = "Parallel2"
    """Parallel-processing optimized instances, 2nd generation."""
    Parallel3 = "Parallel3"
    """Parallel-processing optimized instances, 3nd generation."""

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.InstanceSize")
class InstanceSize(enum.Enum):
    """What size of instance to use."""
    Nano = "Nano"
    Micro = "Micro"
    Small = "Small"
    Medium = "Medium"
    Large = "Large"
    XLarge = "XLarge"
    XLarge2 = "XLarge2"
    XLarge4 = "XLarge4"
    XLarge8 = "XLarge8"
    XLarge9 = "XLarge9"
    XLarge10 = "XLarge10"
    XLarge12 = "XLarge12"
    XLarge16 = "XLarge16"
    XLarge18 = "XLarge18"
    XLarge24 = "XLarge24"
    XLarge32 = "XLarge32"

class InstanceType(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.InstanceType"):
    """Instance type for EC2 instances.

    This class takes a literal string, good if you already
    know the identifier of the type you want.
    """
    def __init__(self, instance_type_identifier: str) -> None:
        """
        Arguments:
            instanceTypeIdentifier: -
        """
        jsii.create(InstanceType, self, [instance_type_identifier])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Return the instance type as a dotted string."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="instanceTypeIdentifier")
    def instance_type_identifier(self) -> str:
        return jsii.get(self, "instanceTypeIdentifier")


class InstanceTypePair(InstanceType, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.InstanceTypePair"):
    """Instance type for EC2 instances.

    This class takes a combination of a class and size.

    Be aware that not all combinations of class and size are available, and not all
    classes are available in all regions.
    """
    def __init__(self, instance_class: "InstanceClass", instance_size: "InstanceSize") -> None:
        """
        Arguments:
            instanceClass: -
            instanceSize: -
        """
        jsii.create(InstanceTypePair, self, [instance_class, instance_size])

    @property
    @jsii.member(jsii_name="instanceClass")
    def instance_class(self) -> "InstanceClass":
        return jsii.get(self, "instanceClass")

    @property
    @jsii.member(jsii_name="instanceSize")
    def instance_size(self) -> "InstanceSize":
        return jsii.get(self, "instanceSize")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.InterfaceVpcEndpointAttributes", jsii_struct_bases=[])
class InterfaceVpcEndpointAttributes(jsii.compat.TypedDict):
    """Construction properties for an ImportedInterfaceVpcEndpoint."""
    port: jsii.Number
    """The port of the service of the interface VPC endpoint."""

    securityGroupId: str
    """The identifier of the security group associated with the interface VPC endpoint."""

    vpcEndpointId: str
    """The interface VPC endpoint identifier."""

@jsii.implements(IInterfaceVpcEndpointService)
class InterfaceVpcEndpointAwsService(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.InterfaceVpcEndpointAwsService"):
    """An AWS service for an interface VPC endpoint."""
    def __init__(self, name: str, prefix: typing.Optional[str]=None, port: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            name: -
            prefix: -
            port: -
        """
        jsii.create(InterfaceVpcEndpointAwsService, self, [name, prefix, port])

    @classproperty
    @jsii.member(jsii_name="ApiGateway")
    def API_GATEWAY(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "ApiGateway")

    @classproperty
    @jsii.member(jsii_name="CloudFormation")
    def CLOUD_FORMATION(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CloudFormation")

    @classproperty
    @jsii.member(jsii_name="CloudTrail")
    def CLOUD_TRAIL(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CloudTrail")

    @classproperty
    @jsii.member(jsii_name="CloudWatch")
    def CLOUD_WATCH(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CloudWatch")

    @classproperty
    @jsii.member(jsii_name="CloudWatchEvents")
    def CLOUD_WATCH_EVENTS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CloudWatchEvents")

    @classproperty
    @jsii.member(jsii_name="CloudWatchLogs")
    def CLOUD_WATCH_LOGS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CloudWatchLogs")

    @classproperty
    @jsii.member(jsii_name="CodeBuild")
    def CODE_BUILD(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodeBuild")

    @classproperty
    @jsii.member(jsii_name="CodeBuildFips")
    def CODE_BUILD_FIPS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodeBuildFips")

    @classproperty
    @jsii.member(jsii_name="CodeCommit")
    def CODE_COMMIT(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodeCommit")

    @classproperty
    @jsii.member(jsii_name="CodeCommitFips")
    def CODE_COMMIT_FIPS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodeCommitFips")

    @classproperty
    @jsii.member(jsii_name="CodeCommitGit")
    def CODE_COMMIT_GIT(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodeCommitGit")

    @classproperty
    @jsii.member(jsii_name="CodeCommitGitFips")
    def CODE_COMMIT_GIT_FIPS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodeCommitGitFips")

    @classproperty
    @jsii.member(jsii_name="CodePipeline")
    def CODE_PIPELINE(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "CodePipeline")

    @classproperty
    @jsii.member(jsii_name="Config")
    def CONFIG(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Config")

    @classproperty
    @jsii.member(jsii_name="Ec2")
    def EC2(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Ec2")

    @classproperty
    @jsii.member(jsii_name="Ec2Messages")
    def EC2_MESSAGES(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Ec2Messages")

    @classproperty
    @jsii.member(jsii_name="Ecr")
    def ECR(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Ecr")

    @classproperty
    @jsii.member(jsii_name="EcrDocker")
    def ECR_DOCKER(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "EcrDocker")

    @classproperty
    @jsii.member(jsii_name="Ecs")
    def ECS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Ecs")

    @classproperty
    @jsii.member(jsii_name="EcsAgent")
    def ECS_AGENT(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "EcsAgent")

    @classproperty
    @jsii.member(jsii_name="EcsTelemetry")
    def ECS_TELEMETRY(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "EcsTelemetry")

    @classproperty
    @jsii.member(jsii_name="ElasticInferenceRuntime")
    def ELASTIC_INFERENCE_RUNTIME(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "ElasticInferenceRuntime")

    @classproperty
    @jsii.member(jsii_name="ElasticLoadBalancing")
    def ELASTIC_LOAD_BALANCING(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "ElasticLoadBalancing")

    @classproperty
    @jsii.member(jsii_name="KinesisStreams")
    def KINESIS_STREAMS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "KinesisStreams")

    @classproperty
    @jsii.member(jsii_name="Kms")
    def KMS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Kms")

    @classproperty
    @jsii.member(jsii_name="SageMakerApi")
    def SAGE_MAKER_API(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "SageMakerApi")

    @classproperty
    @jsii.member(jsii_name="SageMakerNotebook")
    def SAGE_MAKER_NOTEBOOK(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "SageMakerNotebook")

    @classproperty
    @jsii.member(jsii_name="SageMakerRuntime")
    def SAGE_MAKER_RUNTIME(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "SageMakerRuntime")

    @classproperty
    @jsii.member(jsii_name="SageMakerRuntimeFips")
    def SAGE_MAKER_RUNTIME_FIPS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "SageMakerRuntimeFips")

    @classproperty
    @jsii.member(jsii_name="SecretsManager")
    def SECRETS_MANAGER(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "SecretsManager")

    @classproperty
    @jsii.member(jsii_name="ServiceCatalog")
    def SERVICE_CATALOG(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "ServiceCatalog")

    @classproperty
    @jsii.member(jsii_name="Sns")
    def SNS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Sns")

    @classproperty
    @jsii.member(jsii_name="Sqs")
    def SQS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Sqs")

    @classproperty
    @jsii.member(jsii_name="Ssm")
    def SSM(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Ssm")

    @classproperty
    @jsii.member(jsii_name="SsmMessages")
    def SSM_MESSAGES(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "SsmMessages")

    @classproperty
    @jsii.member(jsii_name="Sts")
    def STS(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Sts")

    @classproperty
    @jsii.member(jsii_name="Transfer")
    def TRANSFER(cls) -> "InterfaceVpcEndpointAwsService":
        return jsii.sget(cls, "Transfer")

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        """The name of the service."""
        return jsii.get(self, "name")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The port of the service."""
        return jsii.get(self, "port")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _InterfaceVpcEndpointOptions(jsii.compat.TypedDict, total=False):
    privateDnsEnabled: bool
    """Whether to associate a private hosted zone with the specified VPC.

    This
    allows you to make requests to the service using its default DNS hostname.

    Default:
        true
    """
    subnets: "SubnetSelection"
    """The subnets in which to create an endpoint network interface.

    At most one
    per availability zone.

    Default:
        private subnets
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.InterfaceVpcEndpointOptions", jsii_struct_bases=[_InterfaceVpcEndpointOptions])
class InterfaceVpcEndpointOptions(_InterfaceVpcEndpointOptions):
    """Options to add an interface endpoint to a VPC."""
    service: "IInterfaceVpcEndpointService"
    """The service to use for this interface VPC endpoint."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.InterfaceVpcEndpointProps", jsii_struct_bases=[InterfaceVpcEndpointOptions])
class InterfaceVpcEndpointProps(InterfaceVpcEndpointOptions, jsii.compat.TypedDict):
    """Construction properties for an InterfaceVpcEndpoint."""
    vpc: "IVpc"
    """The VPC network in which the interface endpoint will be used."""

class MachineImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.MachineImage"):
    """Representation of a machine to be launched.

    Combines an AMI ID with an OS.
    """
    def __init__(self, image_id: str, os: "OperatingSystem") -> None:
        """
        Arguments:
            imageId: -
            os: -
        """
        jsii.create(MachineImage, self, [image_id, os])

    @property
    @jsii.member(jsii_name="imageId")
    def image_id(self) -> str:
        return jsii.get(self, "imageId")

    @property
    @jsii.member(jsii_name="os")
    def os(self) -> "OperatingSystem":
        return jsii.get(self, "os")


class OperatingSystem(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ec2.OperatingSystem"):
    """Abstraction of OS features we need to be aware of."""
    @staticmethod
    def __jsii_proxy_class__():
        return _OperatingSystemProxy

    def __init__(self) -> None:
        jsii.create(OperatingSystem, self, [])

    @jsii.member(jsii_name="createUserData")
    @abc.abstractmethod
    def create_user_data(self, scripts: typing.List[str]) -> str:
        """
        Arguments:
            scripts: -
        """
        ...

    @property
    @jsii.member(jsii_name="type")
    @abc.abstractmethod
    def type(self) -> "OperatingSystemType":
        ...


class _OperatingSystemProxy(OperatingSystem):
    @jsii.member(jsii_name="createUserData")
    def create_user_data(self, scripts: typing.List[str]) -> str:
        """
        Arguments:
            scripts: -
        """
        return jsii.invoke(self, "createUserData", [scripts])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "OperatingSystemType":
        return jsii.get(self, "type")


class LinuxOS(OperatingSystem, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.LinuxOS"):
    """OS features specialized for Linux."""
    def __init__(self) -> None:
        jsii.create(LinuxOS, self, [])

    @jsii.member(jsii_name="createUserData")
    def create_user_data(self, scripts: typing.List[str]) -> str:
        """
        Arguments:
            scripts: -
        """
        return jsii.invoke(self, "createUserData", [scripts])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "OperatingSystemType":
        return jsii.get(self, "type")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.OperatingSystemType")
class OperatingSystemType(enum.Enum):
    """The OS type of a particular image."""
    Linux = "Linux"
    Windows = "Windows"

@jsii.implements(ISecurityGroupRule, IConnectable)
class PrefixList(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.PrefixList"):
    """A prefix list.

    Prefix lists are used to allow traffic to VPC-local service endpoints.

    For more information, see this page:

    https://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/vpc-endpoints.html
    """
    def __init__(self, prefix_list_id: str) -> None:
        """
        Arguments:
            prefixListId: -
        """
        jsii.create(PrefixList, self, [prefix_list_id])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        """Produce the egress rule JSON for the given connection."""
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        """Produce the ingress rule JSON for the given connection."""
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule can be inlined into a SecurityGroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="prefixListId")
    def prefix_list_id(self) -> str:
        return jsii.get(self, "prefixListId")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A unique identifier for this connection peer."""
        return jsii.get(self, "uniqueId")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.Protocol")
class Protocol(enum.Enum):
    """Protocol for use in Connection Rules."""
    All = "All"
    Tcp = "Tcp"
    Udp = "Udp"
    Icmp = "Icmp"
    Icmpv6 = "Icmpv6"

@jsii.implements(ISecurityGroup)
class SecurityGroup(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.SecurityGroup"):
    """Creates an Amazon EC2 security group within a VPC.

    This class has an additional optimization over imported security groups that it can also create
    inline ingress and egress rule (which saves on the total number of resources inside
    the template).
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: "IVpc", allow_all_outbound: typing.Optional[bool]=None, description: typing.Optional[str]=None, group_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            vpc: The VPC in which to create the security group.
            allowAllOutbound: Whether to allow all outbound traffic by default. If this is set to true, there will only be a single egress rule which allows all outbound traffic. If this is set to false, no outbound traffic will be allowed by default and all egress traffic must be explicitly authorized. Default: true
            description: A description of the security group. Default: The default name will be the construct's CDK path.
            groupName: The name of the security group. For valid values, see the GroupName parameter of the CreateSecurityGroup action in the Amazon EC2 API Reference. It is not recommended to use an explicit group name. Default: If you don't specify a GroupName, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        """
        props: SecurityGroupProps = {"vpc": vpc}

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if description is not None:
            props["description"] = description

        if group_name is not None:
            props["groupName"] = group_name

        jsii.create(SecurityGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromSecurityGroupId")
    @classmethod
    def from_security_group_id(cls, scope: aws_cdk.cdk.Construct, id: str, security_group_id: str) -> "ISecurityGroup":
        """Import an existing security group into this app.

        Arguments:
            scope: -
            id: -
            securityGroupId: -
        """
        return jsii.sinvoke(cls, "fromSecurityGroupId", [scope, id, security_group_id])

    @jsii.member(jsii_name="isSecurityGroup")
    @classmethod
    def is_security_group(cls, construct: typing.Any) -> bool:
        """Return whether the indicated object is a security group.

        Arguments:
            construct: -
        """
        return jsii.sinvoke(cls, "isSecurityGroup", [construct])

    @jsii.member(jsii_name="addEgressRule")
    def add_egress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        """Add an egress rule for the current security group.

        ``remoteRule`` controls where the Rule object is created if the peer is also a
        securityGroup and they are in different stack. If false (default) the
        rule object is created under the current SecurityGroup object. If true and the
        peer is also a SecurityGroup, the rule object is created under the remote
        SecurityGroup object.

        Arguments:
            peer: -
            connection: -
            description: -
            remoteRule: -
        """
        return jsii.invoke(self, "addEgressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="addIngressRule")
    def add_ingress_rule(self, peer: "ISecurityGroupRule", connection: "IPortRange", description: typing.Optional[str]=None, remote_rule: typing.Optional[bool]=None) -> None:
        """Add an ingress rule for the current security group.

        ``remoteRule`` controls where the Rule object is created if the peer is also a
        securityGroup and they are in different stack. If false (default) the
        rule object is created under the current SecurityGroup object. If true and the
        peer is also a SecurityGroup, the rule object is created under the remote
        SecurityGroup object.

        Arguments:
            peer: -
            connection: -
            description: -
            remoteRule: -
        """
        return jsii.invoke(self, "addIngressRule", [peer, connection, description, remote_rule])

    @jsii.member(jsii_name="toEgressRuleJSON")
    def to_egress_rule_json(self) -> typing.Any:
        """Produce the egress rule JSON for the given connection."""
        return jsii.invoke(self, "toEgressRuleJSON", [])

    @jsii.member(jsii_name="toIngressRuleJSON")
    def to_ingress_rule_json(self) -> typing.Any:
        """Produce the ingress rule JSON for the given connection."""
        return jsii.invoke(self, "toIngressRuleJSON", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule can be inlined into a SecurityGroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """The ID of the security group.

        attribute:
            true
        """
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="securityGroupName")
    def security_group_name(self) -> str:
        """An attribute that represents the security group name.

        attribute:
            true
        """
        return jsii.get(self, "securityGroupName")

    @property
    @jsii.member(jsii_name="securityGroupVpcId")
    def security_group_vpc_id(self) -> str:
        """The VPC ID this security group is part of.

        attribute:
            true
        """
        return jsii.get(self, "securityGroupVpcId")

    @property
    @jsii.member(jsii_name="uniqueId")
    def unique_id(self) -> str:
        """A unique identifier for this connection peer."""
        return jsii.get(self, "uniqueId")

    @property
    @jsii.member(jsii_name="defaultPortRange")
    def default_port_range(self) -> typing.Optional["IPortRange"]:
        """FIXME: Where to place this??"""
        return jsii.get(self, "defaultPortRange")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _SecurityGroupProps(jsii.compat.TypedDict, total=False):
    allowAllOutbound: bool
    """Whether to allow all outbound traffic by default.

    If this is set to true, there will only be a single egress rule which allows all
    outbound traffic. If this is set to false, no outbound traffic will be allowed by
    default and all egress traffic must be explicitly authorized.

    Default:
        true
    """
    description: str
    """A description of the security group.

    Default:
        The default name will be the construct's CDK path.
    """
    groupName: str
    """The name of the security group.

    For valid values, see the GroupName
    parameter of the CreateSecurityGroup action in the Amazon EC2 API
    Reference.

    It is not recommended to use an explicit group name.

    Default:
        If you don't specify a GroupName, AWS CloudFormation generates a
        unique physical ID and uses that ID for the group name.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SecurityGroupProps", jsii_struct_bases=[_SecurityGroupProps])
class SecurityGroupProps(_SecurityGroupProps):
    vpc: "IVpc"
    """The VPC in which to create the security group."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SelectedSubnets", jsii_struct_bases=[])
class SelectedSubnets(jsii.compat.TypedDict):
    """Result of selecting a subset of subnets from a VPC."""
    availabilityZones: typing.List[str]
    """The respective AZs of each subnet."""

    internetConnectedDependency: aws_cdk.cdk.IDependable
    """Dependency representing internet connectivity for these subnets."""

    routeTableIds: typing.List[str]
    """Route table IDs of each respective subnet."""

    subnetIds: typing.List[str]
    """The subnet IDs."""

@jsii.implements(ISubnet)
class Subnet(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.Subnet"):
    """Represents a new VPC subnet resource.

    resource:
        AWS::EC2::Subnet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, cidr_block: str, vpc_id: str, map_public_ip_on_launch: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            availabilityZone: The availability zone for the subnet.
            cidrBlock: The CIDR notation for this subnet.
            vpcId: The VPC which this subnet is part of.
            mapPublicIpOnLaunch: Controls if a public IP is associated to an instance at launch. Default: true in Subnet.Public, false in Subnet.Private or Subnet.Isolated.
        """
        props: SubnetProps = {"availabilityZone": availability_zone, "cidrBlock": cidr_block, "vpcId": vpc_id}

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        jsii.create(Subnet, self, [scope, id, props])

    @jsii.member(jsii_name="fromSubnetAttributes")
    @classmethod
    def from_subnet_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, subnet_id: str) -> "ISubnet":
        """
        Arguments:
            scope: -
            id: -
            attrs: -
            availabilityZone: The Availability Zone the subnet is located in.
            subnetId: The subnetId for this particular subnet.
        """
        attrs: SubnetAttributes = {"availabilityZone": availability_zone, "subnetId": subnet_id}

        return jsii.sinvoke(cls, "fromSubnetAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="isVpcSubnet")
    @classmethod
    def is_vpc_subnet(cls, o: typing.Any) -> bool:
        """
        Arguments:
            o: -
        """
        return jsii.sinvoke(cls, "isVpcSubnet", [o])

    @jsii.member(jsii_name="addDefaultInternetRoute")
    def add_default_internet_route(self, gateway_id: str, gateway_attachment: aws_cdk.cdk.IDependable) -> None:
        """Create a default route that points to a passed IGW, with a dependency on the IGW's attachment to the VPC.

        Arguments:
            gatewayId: the logical ID (ref) of the gateway attached to your VPC.
            gatewayAttachment: the gateway attachment construct to be added as a dependency.
        """
        return jsii.invoke(self, "addDefaultInternetRoute", [gateway_id, gateway_attachment])

    @jsii.member(jsii_name="addDefaultNatRoute")
    def add_default_nat_route(self, nat_gateway_id: str) -> None:
        """Adds an entry to this subnets route table that points to the passed NATGatwayId.

        Arguments:
            natGatewayId: The ID of the NAT gateway.
        """
        return jsii.invoke(self, "addDefaultNatRoute", [nat_gateway_id])

    @property
    @jsii.member(jsii_name="availabilityZone")
    def availability_zone(self) -> str:
        """The Availability Zone the subnet is located in."""
        return jsii.get(self, "availabilityZone")

    @property
    @jsii.member(jsii_name="dependencyElements")
    def dependency_elements(self) -> typing.List[aws_cdk.cdk.IDependable]:
        """Parts of this VPC subnet."""
        return jsii.get(self, "dependencyElements")

    @property
    @jsii.member(jsii_name="internetConnectivityEstablished")
    def internet_connectivity_established(self) -> aws_cdk.cdk.IDependable:
        """Dependable that can be depended upon to force internet connectivity established on the VPC."""
        return jsii.get(self, "internetConnectivityEstablished")

    @property
    @jsii.member(jsii_name="subnetAvailabilityZone")
    def subnet_availability_zone(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "subnetAvailabilityZone")

    @property
    @jsii.member(jsii_name="subnetId")
    def subnet_id(self) -> str:
        """The subnetId for this particular subnet."""
        return jsii.get(self, "subnetId")

    @property
    @jsii.member(jsii_name="subnetIpv6CidrBlocks")
    def subnet_ipv6_cidr_blocks(self) -> typing.List[str]:
        """
        attribute:
            true
        """
        return jsii.get(self, "subnetIpv6CidrBlocks")

    @property
    @jsii.member(jsii_name="subnetNetworkAclAssociationId")
    def subnet_network_acl_association_id(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "subnetNetworkAclAssociationId")

    @property
    @jsii.member(jsii_name="subnetVpcId")
    def subnet_vpc_id(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "subnetVpcId")

    @property
    @jsii.member(jsii_name="routeTableId")
    def route_table_id(self) -> typing.Optional[str]:
        """The routeTableId attached to this subnet."""
        return jsii.get(self, "routeTableId")


@jsii.implements(IPrivateSubnet)
class PrivateSubnet(Subnet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.PrivateSubnet"):
    """Represents a private VPC subnet resource."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, cidr_block: str, vpc_id: str, map_public_ip_on_launch: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            availabilityZone: The availability zone for the subnet.
            cidrBlock: The CIDR notation for this subnet.
            vpcId: The VPC which this subnet is part of.
            mapPublicIpOnLaunch: Controls if a public IP is associated to an instance at launch. Default: true in Subnet.Public, false in Subnet.Private or Subnet.Isolated.
        """
        props: PrivateSubnetProps = {"availabilityZone": availability_zone, "cidrBlock": cidr_block, "vpcId": vpc_id}

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        jsii.create(PrivateSubnet, self, [scope, id, props])

    @jsii.member(jsii_name="fromPrivateSubnetAttributes")
    @classmethod
    def from_private_subnet_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, subnet_id: str) -> "IPrivateSubnet":
        """
        Arguments:
            scope: -
            id: -
            attrs: -
            availabilityZone: The Availability Zone the subnet is located in.
            subnetId: The subnetId for this particular subnet.
        """
        attrs: PrivateSubnetAttributes = {"availabilityZone": availability_zone, "subnetId": subnet_id}

        return jsii.sinvoke(cls, "fromPrivateSubnetAttributes", [scope, id, attrs])


@jsii.implements(IPublicSubnet)
class PublicSubnet(Subnet, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.PublicSubnet"):
    """Represents a public VPC subnet resource."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, cidr_block: str, vpc_id: str, map_public_ip_on_launch: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            availabilityZone: The availability zone for the subnet.
            cidrBlock: The CIDR notation for this subnet.
            vpcId: The VPC which this subnet is part of.
            mapPublicIpOnLaunch: Controls if a public IP is associated to an instance at launch. Default: true in Subnet.Public, false in Subnet.Private or Subnet.Isolated.
        """
        props: PublicSubnetProps = {"availabilityZone": availability_zone, "cidrBlock": cidr_block, "vpcId": vpc_id}

        if map_public_ip_on_launch is not None:
            props["mapPublicIpOnLaunch"] = map_public_ip_on_launch

        jsii.create(PublicSubnet, self, [scope, id, props])

    @jsii.member(jsii_name="fromPublicSubnetAttributes")
    @classmethod
    def from_public_subnet_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, availability_zone: str, subnet_id: str) -> "IPublicSubnet":
        """
        Arguments:
            scope: -
            id: -
            attrs: -
            availabilityZone: The Availability Zone the subnet is located in.
            subnetId: The subnetId for this particular subnet.
        """
        attrs: PublicSubnetAttributes = {"availabilityZone": availability_zone, "subnetId": subnet_id}

        return jsii.sinvoke(cls, "fromPublicSubnetAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addNatGateway")
    def add_nat_gateway(self) -> "CfnNatGateway":
        """Creates a new managed NAT gateway attached to this public subnet. Also adds the EIP for the managed NAT.

        Returns:
            A ref to the the NAT Gateway ID
        """
        return jsii.invoke(self, "addNatGateway", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SubnetAttributes", jsii_struct_bases=[])
class SubnetAttributes(jsii.compat.TypedDict):
    availabilityZone: str
    """The Availability Zone the subnet is located in."""

    subnetId: str
    """The subnetId for this particular subnet."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.PrivateSubnetAttributes", jsii_struct_bases=[SubnetAttributes])
class PrivateSubnetAttributes(SubnetAttributes, jsii.compat.TypedDict):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.PublicSubnetAttributes", jsii_struct_bases=[SubnetAttributes])
class PublicSubnetAttributes(SubnetAttributes, jsii.compat.TypedDict):
    pass

@jsii.data_type_optionals(jsii_struct_bases=[])
class _SubnetConfiguration(jsii.compat.TypedDict, total=False):
    cidrMask: jsii.Number
    """The CIDR Mask or the number of leading 1 bits in the routing mask.

    Valid values are 16 - 28
    """
    reserved: bool
    """Controls if subnet IP space needs to be reserved.

    When true, the IP space for the subnet is reserved but no actual
    resources are provisioned. This space is only dependent on the
    number of availibility zones and on ``cidrMask`` - all other subnet
    properties are ignored.

    Default:
        false
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SubnetConfiguration", jsii_struct_bases=[_SubnetConfiguration])
class SubnetConfiguration(_SubnetConfiguration):
    """Specify configuration parameters for a VPC to be built."""
    name: str
    """The common Logical Name for the ``VpcSubnet``.

    This name will be suffixed with an integer correlating to a specific
    availability zone.
    """

    subnetType: "SubnetType"
    """The type of Subnet to configure.

    The Subnet type will control the ability to route and connect to the
    Internet.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _SubnetProps(jsii.compat.TypedDict, total=False):
    mapPublicIpOnLaunch: bool
    """Controls if a public IP is associated to an instance at launch.

    Default:
        true in Subnet.Public, false in Subnet.Private or Subnet.Isolated.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SubnetProps", jsii_struct_bases=[_SubnetProps])
class SubnetProps(_SubnetProps):
    """Specify configuration parameters for a VPC subnet."""
    availabilityZone: str
    """The availability zone for the subnet."""

    cidrBlock: str
    """The CIDR notation for this subnet."""

    vpcId: str
    """The VPC which this subnet is part of."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.PrivateSubnetProps", jsii_struct_bases=[SubnetProps])
class PrivateSubnetProps(SubnetProps, jsii.compat.TypedDict):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.PublicSubnetProps", jsii_struct_bases=[SubnetProps])
class PublicSubnetProps(SubnetProps, jsii.compat.TypedDict):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.SubnetSelection", jsii_struct_bases=[])
class SubnetSelection(jsii.compat.TypedDict, total=False):
    """Customize subnets that are selected for placement of ENIs.

    Constructs that allow customization of VPC placement use parameters of this
    type to provide placement settings.

    By default, the instances are placed in the private subnets.
    """
    onePerAz: bool
    """If true, return at most one subnet per AZ.

    defautl:
        false
    """

    subnetName: str
    """Place the instances in the subnets with the given name.

    (This is the name supplied in subnetConfiguration).

    At most one of ``subnetType`` and ``subnetName`` can be supplied.

    Default:
        name
    """

    subnetType: "SubnetType"
    """Place the instances in the subnets of the given type.

    At most one of ``subnetType`` and ``subnetName`` can be supplied.

    Default:
        SubnetType.Private
    """

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.SubnetType")
class SubnetType(enum.Enum):
    """The type of Subnet."""
    Isolated = "Isolated"
    """Isolated Subnets do not route Outbound traffic.

    This can be good for subnets with RDS or
    Elasticache endpoints
    """
    Private = "Private"
    """Subnet that routes to the internet, but not vice versa.

    Instances in a private subnet can connect to the Internet, but will not
    allow connections to be initiated from the Internet.

    Outbound traffic will be routed via a NAT Gateway. Preference being in
    the same AZ, but if not available will use another AZ (control by
    specifing ``maxGateways`` on VpcNetwork). This might be used for
    experimental cost conscious accounts or accounts where HA outbound
    traffic is not needed.
    """
    Public = "Public"
    """Subnet connected to the Internet.

    Instances in a Public subnet can connect to the Internet and can be
    connected to from the Internet as long as they are launched with public
    IPs (controlled on the AutoScalingGroup or other constructs that launch
    instances).

    Public subnets route outbound traffic via an Internet Gateway.
    """

@jsii.implements(IPortRange)
class TcpAllPorts(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpAllPorts"):
    """All TCP Ports."""
    def __init__(self) -> None:
        jsii.create(TcpAllPorts, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class TcpPort(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpPort"):
    """A single TCP port."""
    def __init__(self, port: jsii.Number) -> None:
        """
        Arguments:
            port: -
        """
        jsii.create(TcpPort, self, [port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return jsii.get(self, "port")


@jsii.implements(IPortRange)
class TcpPortRange(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.TcpPortRange"):
    """A TCP port range."""
    def __init__(self, start_port: jsii.Number, end_port: jsii.Number) -> None:
        """
        Arguments:
            startPort: -
            endPort: -
        """
        jsii.create(TcpPortRange, self, [start_port, end_port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="endPort")
    def end_port(self) -> jsii.Number:
        return jsii.get(self, "endPort")

    @property
    @jsii.member(jsii_name="startPort")
    def start_port(self) -> jsii.Number:
        return jsii.get(self, "startPort")


@jsii.implements(IPortRange)
class UdpAllPorts(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpAllPorts"):
    """All UDP Ports."""
    def __init__(self) -> None:
        jsii.create(UdpAllPorts, self, [])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")


@jsii.implements(IPortRange)
class UdpPort(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpPort"):
    """A single UDP port."""
    def __init__(self, port: jsii.Number) -> None:
        """
        Arguments:
            port: -
        """
        jsii.create(UdpPort, self, [port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        return jsii.get(self, "port")


@jsii.implements(IPortRange)
class UdpPortRange(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.UdpPortRange"):
    """A UDP port range."""
    def __init__(self, start_port: jsii.Number, end_port: jsii.Number) -> None:
        """
        Arguments:
            startPort: -
            endPort: -
        """
        jsii.create(UdpPortRange, self, [start_port, end_port])

    @jsii.member(jsii_name="toRuleJSON")
    def to_rule_json(self) -> typing.Any:
        """Produce the ingress/egress rule JSON for the given connection."""
        return jsii.invoke(self, "toRuleJSON", [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> str:
        """Returns a string representation of an object."""
        return jsii.invoke(self, "toString", [])

    @property
    @jsii.member(jsii_name="canInlineRule")
    def can_inline_rule(self) -> bool:
        """Whether the rule containing this port range can be inlined into a securitygroup or not."""
        return jsii.get(self, "canInlineRule")

    @property
    @jsii.member(jsii_name="endPort")
    def end_port(self) -> jsii.Number:
        return jsii.get(self, "endPort")

    @property
    @jsii.member(jsii_name="startPort")
    def start_port(self) -> jsii.Number:
        return jsii.get(self, "startPort")


@jsii.implements(IVpc)
class Vpc(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.Vpc"):
    """VpcNetwork deploys an AWS VPC, with public and private subnets per Availability Zone. For example:.

    import { Vpc } from '@aws-cdk/aws-ec2'

    const vpc = new Vpc(this, {
    cidr: "10.0.0.0/16"
    })

    // Iterate the public subnets
    for (let subnet of vpc.publicSubnets) {

    }

    // Iterate the private subnets
    for (let subnet of vpc.privateSubnets) {

    }

    resource:
        AWS::EC2::VPC
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cidr: typing.Optional[str]=None, default_instance_tenancy: typing.Optional["DefaultInstanceTenancy"]=None, enable_dns_hostnames: typing.Optional[bool]=None, enable_dns_support: typing.Optional[bool]=None, gateway_endpoints: typing.Optional[typing.Mapping[str,"GatewayVpcEndpointOptions"]]=None, max_a_zs: typing.Optional[jsii.Number]=None, nat_gateways: typing.Optional[jsii.Number]=None, nat_gateway_subnets: typing.Optional["SubnetSelection"]=None, subnet_configuration: typing.Optional[typing.List["SubnetConfiguration"]]=None, vpn_connections: typing.Optional[typing.Mapping[str,"VpnConnectionOptions"]]=None, vpn_gateway: typing.Optional[bool]=None, vpn_gateway_asn: typing.Optional[jsii.Number]=None, vpn_route_propagation: typing.Optional[typing.List["SubnetSelection"]]=None) -> None:
        """VpcNetwork creates a VPC that spans a whole region. It will automatically divide the provided VPC CIDR range, and create public and private subnets per Availability Zone. Network routing for the public subnets will be configured to allow outbound access directly via an Internet Gateway. Network routing for the private subnets will be configured to allow outbound access via a set of resilient NAT Gateways (one per AZ).

        Arguments:
            scope: -
            id: -
            props: -
            cidr: The CIDR range to use for the VPC (e.g. '10.0.0.0/16'). Should be a minimum of /28 and maximum size of /16. The range will be split evenly into two subnets per Availability Zone (one public, one private). Default: Vpc.DEFAULT_CIDR_RANGE
            defaultInstanceTenancy: The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy. Default: DefaultInstanceTenancy.Default (shared) tenancy
            enableDnsHostnames: Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true. Default: true
            enableDnsSupport: Indicates whether the DNS resolution is supported for the VPC. If this attribute is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames to IP addresses is not enabled. If this attribute is true, queries to the Amazon provided DNS server at the 169.254.169.253 IP address, or the reserved IP address at the base of the VPC IPv4 network range plus two will succeed. Default: true
            gatewayEndpoints: Gateway endpoints to add to this VPC. Default: - None.
            maxAZs: Define the maximum number of AZs to use in this region. If the region has more AZs than you want to use (for example, because of EIP limits), pick a lower number here. The AZs will be sorted and picked from the start of the list. If you pick a higher number than the number of AZs in the region, all AZs in the region will be selected. To use "all AZs" available to your account, use a high number (such as 99). Default: 3
            natGateways: The number of NAT Gateways to create. For example, if set this to 1 and your subnet configuration is for 3 Public subnets then only one of the Public subnets will have a gateway and all Private subnets will route to this NAT Gateway. Default: maxAZs
            natGatewaySubnets: Configures the subnets which will have NAT Gateways. You can pick a specific group of subnets by specifying the group name; the picked subnets must be public subnets. Default: - All public subnets.
            subnetConfiguration: Configure the subnets to build for each AZ. The subnets are constructed in the context of the VPC so you only need specify the configuration. The VPC details (VPC ID, specific CIDR, specific AZ will be calculated during creation) For example if you want 1 public subnet, 1 private subnet, and 1 isolated subnet in each AZ provide the following: subnetConfiguration: [ { cidrMask: 24, name: 'ingress', subnetType: SubnetType.Public, }, { cidrMask: 24, name: 'application', subnetType: SubnetType.Private, }, { cidrMask: 28, name: 'rds', subnetType: SubnetType.Isolated, } ] ``cidrMask`` is optional and if not provided the IP space in the VPC will be evenly divided between the requested subnets. Default: - The VPC CIDR will be evenly divided between 1 public and 1 private subnet per AZ.
            vpnConnections: VPN connections to this VPC. Default: - No connections.
            vpnGateway: Indicates whether a VPN gateway should be created and attached to this VPC. Default: - true when vpnGatewayAsn or vpnConnections is specified.
            vpnGatewayAsn: The private Autonomous System Number (ASN) for the VPN gateway. Default: - Amazon default ASN.
            vpnRoutePropagation: Where to propagate VPN routes. Default: - On the route tables associated with private subnets.
        """
        props: VpcProps = {}

        if cidr is not None:
            props["cidr"] = cidr

        if default_instance_tenancy is not None:
            props["defaultInstanceTenancy"] = default_instance_tenancy

        if enable_dns_hostnames is not None:
            props["enableDnsHostnames"] = enable_dns_hostnames

        if enable_dns_support is not None:
            props["enableDnsSupport"] = enable_dns_support

        if gateway_endpoints is not None:
            props["gatewayEndpoints"] = gateway_endpoints

        if max_a_zs is not None:
            props["maxAZs"] = max_a_zs

        if nat_gateways is not None:
            props["natGateways"] = nat_gateways

        if nat_gateway_subnets is not None:
            props["natGatewaySubnets"] = nat_gateway_subnets

        if subnet_configuration is not None:
            props["subnetConfiguration"] = subnet_configuration

        if vpn_connections is not None:
            props["vpnConnections"] = vpn_connections

        if vpn_gateway is not None:
            props["vpnGateway"] = vpn_gateway

        if vpn_gateway_asn is not None:
            props["vpnGatewayAsn"] = vpn_gateway_asn

        if vpn_route_propagation is not None:
            props["vpnRoutePropagation"] = vpn_route_propagation

        jsii.create(Vpc, self, [scope, id, props])

    @jsii.member(jsii_name="fromLookup")
    @classmethod
    def from_lookup(cls, scope: aws_cdk.cdk.Construct, id: str, *, is_default: typing.Optional[bool]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, vpc_id: typing.Optional[str]=None, vpc_name: typing.Optional[str]=None) -> "IVpc":
        """Import an existing VPC from by querying the AWS environment this stack is deployed to.

        Arguments:
            scope: -
            id: -
            options: -
            isDefault: Whether to match the default VPC. Default: Don't care whether we return the default VPC
            tags: Tags on the VPC. The VPC must have all of these tags Default: Don't filter on tags
            vpcId: The ID of the VPC. If given, will import exactly this VPC. Default: Don't filter on vpcId
            vpcName: The name of the VPC. If given, will import the VPC with this name. Default: Don't filter on vpcName
        """
        options: VpcLookupOptions = {}

        if is_default is not None:
            options["isDefault"] = is_default

        if tags is not None:
            options["tags"] = tags

        if vpc_id is not None:
            options["vpcId"] = vpc_id

        if vpc_name is not None:
            options["vpcName"] = vpc_name

        return jsii.sinvoke(cls, "fromLookup", [scope, id, options])

    @jsii.member(jsii_name="fromVpcAttributes")
    @classmethod
    def from_vpc_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, availability_zones: typing.List[str], vpc_id: str, isolated_subnet_ids: typing.Optional[typing.List[str]]=None, isolated_subnet_names: typing.Optional[typing.List[str]]=None, private_subnet_ids: typing.Optional[typing.List[str]]=None, private_subnet_names: typing.Optional[typing.List[str]]=None, public_subnet_ids: typing.Optional[typing.List[str]]=None, public_subnet_names: typing.Optional[typing.List[str]]=None, vpn_gateway_id: typing.Optional[str]=None) -> "IVpc":
        """Import an exported VPC.

        Arguments:
            scope: -
            id: -
            attrs: -
            availabilityZones: List of availability zones for the subnets in this VPC.
            vpcId: VPC's identifier.
            isolatedSubnetIds: List of isolated subnet IDs. Must be undefined or match the availability zones in length and order.
            isolatedSubnetNames: List of names for the isolated subnets. Must be undefined or have a name for every isolated subnet group.
            privateSubnetIds: List of private subnet IDs. Must be undefined or match the availability zones in length and order.
            privateSubnetNames: List of names for the private subnets. Must be undefined or have a name for every private subnet group.
            publicSubnetIds: List of public subnet IDs. Must be undefined or match the availability zones in length and order.
            publicSubnetNames: List of names for the public subnets. Must be undefined or have a name for every public subnet group.
            vpnGatewayId: VPN gateway's identifier.
        """
        attrs: VpcAttributes = {"availabilityZones": availability_zones, "vpcId": vpc_id}

        if isolated_subnet_ids is not None:
            attrs["isolatedSubnetIds"] = isolated_subnet_ids

        if isolated_subnet_names is not None:
            attrs["isolatedSubnetNames"] = isolated_subnet_names

        if private_subnet_ids is not None:
            attrs["privateSubnetIds"] = private_subnet_ids

        if private_subnet_names is not None:
            attrs["privateSubnetNames"] = private_subnet_names

        if public_subnet_ids is not None:
            attrs["publicSubnetIds"] = public_subnet_ids

        if public_subnet_names is not None:
            attrs["publicSubnetNames"] = public_subnet_names

        if vpn_gateway_id is not None:
            attrs["vpnGatewayId"] = vpn_gateway_id

        return jsii.sinvoke(cls, "fromVpcAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addDynamoDbEndpoint")
    def add_dynamo_db_endpoint(self, id: str, subnets: typing.Optional[typing.List["SubnetSelection"]]=None) -> "GatewayVpcEndpoint":
        """Adds a new DynamoDB gateway endpoint to this VPC.

        Arguments:
            id: -
            subnets: -
        """
        return jsii.invoke(self, "addDynamoDbEndpoint", [id, subnets])

    @jsii.member(jsii_name="addGatewayEndpoint")
    def add_gateway_endpoint(self, id: str, *, service: "IGatewayVpcEndpointService", subnets: typing.Optional[typing.List["SubnetSelection"]]=None) -> "GatewayVpcEndpoint":
        """Adds a new gateway endpoint to this VPC.

        Arguments:
            id: -
            options: -
            service: The service to use for this gateway VPC endpoint.
            subnets: Where to add endpoint routing. Default: private subnets
        """
        options: GatewayVpcEndpointOptions = {"service": service}

        if subnets is not None:
            options["subnets"] = subnets

        return jsii.invoke(self, "addGatewayEndpoint", [id, options])

    @jsii.member(jsii_name="addInterfaceEndpoint")
    def add_interface_endpoint(self, id: str, *, service: "IInterfaceVpcEndpointService", private_dns_enabled: typing.Optional[bool]=None, subnets: typing.Optional["SubnetSelection"]=None) -> "InterfaceVpcEndpoint":
        """Adds a new interface endpoint to this VPC.

        Arguments:
            id: -
            options: -
            service: The service to use for this interface VPC endpoint.
            privateDnsEnabled: Whether to associate a private hosted zone with the specified VPC. This allows you to make requests to the service using its default DNS hostname. Default: true
            subnets: The subnets in which to create an endpoint network interface. At most one per availability zone. Default: private subnets
        """
        options: InterfaceVpcEndpointOptions = {"service": service}

        if private_dns_enabled is not None:
            options["privateDnsEnabled"] = private_dns_enabled

        if subnets is not None:
            options["subnets"] = subnets

        return jsii.invoke(self, "addInterfaceEndpoint", [id, options])

    @jsii.member(jsii_name="addS3Endpoint")
    def add_s3_endpoint(self, id: str, subnets: typing.Optional[typing.List["SubnetSelection"]]=None) -> "GatewayVpcEndpoint":
        """Adds a new S3 gateway endpoint to this VPC.

        Arguments:
            id: -
            subnets: -
        """
        return jsii.invoke(self, "addS3Endpoint", [id, subnets])

    @jsii.member(jsii_name="addVpnConnection")
    def add_vpn_connection(self, id: str, *, ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> "VpnConnection":
        """Adds a new VPN connection to this VPC.

        Arguments:
            id: -
            options: -
            ip: The ip address of the customer gateway.
            asn: The ASN of the customer gateway. Default: 65000
            staticRoutes: The static routes to be routed from the VPN gateway to the customer gateway. Default: Dynamic routing (BGP)
            tunnelOptions: The tunnel options for the VPN connection. At most two elements (one per tunnel). Duplicates not allowed. Default: Amazon generated tunnel options
        """
        options: VpnConnectionOptions = {"ip": ip}

        if asn is not None:
            options["asn"] = asn

        if static_routes is not None:
            options["staticRoutes"] = static_routes

        if tunnel_options is not None:
            options["tunnelOptions"] = tunnel_options

        return jsii.invoke(self, "addVpnConnection", [id, options])

    @jsii.member(jsii_name="isPublicSubnets")
    def is_public_subnets(self, subnet_ids: typing.List[str]) -> bool:
        """Return whether all of the given subnets are from the VPC's public subnets.

        Arguments:
            subnetIds: -
        """
        return jsii.invoke(self, "isPublicSubnets", [subnet_ids])

    @jsii.member(jsii_name="selectSubnetIds")
    def select_subnet_ids(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List[str]:
        """Return IDs of the subnets appropriate for the given selection strategy.

        Requires that at least one subnet is matched, throws a descriptive
        error message otherwise.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private
        """
        selection: SubnetSelection = {}

        if one_per_az is not None:
            selection["onePerAz"] = one_per_az

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "selectSubnetIds", [selection])

    @jsii.member(jsii_name="selectSubnetObjects")
    def _select_subnet_objects(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> typing.List["ISubnet"]:
        """Return the subnets appropriate for the placement strategy.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private
        """
        selection: SubnetSelection = {}

        if one_per_az is not None:
            selection["onePerAz"] = one_per_az

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "selectSubnetObjects", [selection])

    @jsii.member(jsii_name="selectSubnets")
    def select_subnets(self, *, one_per_az: typing.Optional[bool]=None, subnet_name: typing.Optional[str]=None, subnet_type: typing.Optional["SubnetType"]=None) -> "SelectedSubnets":
        """Returns IDs of selected subnets.

        Arguments:
            selection: -
            onePerAz: If true, return at most one subnet per AZ.
            subnetName: Place the instances in the subnets with the given name. (This is the name supplied in subnetConfiguration). At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: name
            subnetType: Place the instances in the subnets of the given type. At most one of ``subnetType`` and ``subnetName`` can be supplied. Default: SubnetType.Private
        """
        selection: SubnetSelection = {}

        if one_per_az is not None:
            selection["onePerAz"] = one_per_az

        if subnet_name is not None:
            selection["subnetName"] = subnet_name

        if subnet_type is not None:
            selection["subnetType"] = subnet_type

        return jsii.invoke(self, "selectSubnets", [selection])

    @classproperty
    @jsii.member(jsii_name="DEFAULT_CIDR_RANGE")
    def DEFAULT_CIDR_RANGE(cls) -> str:
        """The default CIDR range used when creating VPCs. This can be overridden using VpcNetworkProps when creating a VPCNetwork resource. e.g. new VpcResource(this, { cidr: '192.168.0.0./16' })."""
        return jsii.sget(cls, "DEFAULT_CIDR_RANGE")

    @classproperty
    @jsii.member(jsii_name="DEFAULT_SUBNETS")
    def DEFAULT_SUBNETS(cls) -> typing.List["SubnetConfiguration"]:
        """The default subnet configuration.

        1 Public and 1 Private subnet per AZ evenly split
        """
        return jsii.sget(cls, "DEFAULT_SUBNETS")

    @property
    @jsii.member(jsii_name="availabilityZones")
    def availability_zones(self) -> typing.List[str]:
        """AZs for this VPC."""
        return jsii.get(self, "availabilityZones")

    @property
    @jsii.member(jsii_name="internetDependencies")
    def internet_dependencies(self) -> typing.List[aws_cdk.cdk.IConstruct]:
        """Dependencies for internet connectivity."""
        return jsii.get(self, "internetDependencies")

    @property
    @jsii.member(jsii_name="isolatedSubnets")
    def isolated_subnets(self) -> typing.List["ISubnet"]:
        """List of isolated subnets in this VPC."""
        return jsii.get(self, "isolatedSubnets")

    @property
    @jsii.member(jsii_name="natDependencies")
    def nat_dependencies(self) -> typing.List[aws_cdk.cdk.IConstruct]:
        """Dependencies for NAT connectivity."""
        return jsii.get(self, "natDependencies")

    @property
    @jsii.member(jsii_name="privateSubnets")
    def private_subnets(self) -> typing.List["ISubnet"]:
        """List of private subnets in this VPC."""
        return jsii.get(self, "privateSubnets")

    @property
    @jsii.member(jsii_name="publicSubnets")
    def public_subnets(self) -> typing.List["ISubnet"]:
        """List of public subnets in this VPC."""
        return jsii.get(self, "publicSubnets")

    @property
    @jsii.member(jsii_name="region")
    def region(self) -> str:
        """The region where this VPC is defined."""
        return jsii.get(self, "region")

    @property
    @jsii.member(jsii_name="vpcCidrBlock")
    def vpc_cidr_block(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcCidrBlock")

    @property
    @jsii.member(jsii_name="vpcCidrBlockAssociations")
    def vpc_cidr_block_associations(self) -> typing.List[str]:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcCidrBlockAssociations")

    @property
    @jsii.member(jsii_name="vpcDefaultNetworkAcl")
    def vpc_default_network_acl(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcDefaultNetworkAcl")

    @property
    @jsii.member(jsii_name="vpcDefaultSecurityGroup")
    def vpc_default_security_group(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcDefaultSecurityGroup")

    @property
    @jsii.member(jsii_name="vpcId")
    def vpc_id(self) -> str:
        """Identifier for this VPC."""
        return jsii.get(self, "vpcId")

    @property
    @jsii.member(jsii_name="vpcIpv6CidrBlocks")
    def vpc_ipv6_cidr_blocks(self) -> typing.List[str]:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcIpv6CidrBlocks")

    @property
    @jsii.member(jsii_name="vpnGatewayId")
    def vpn_gateway_id(self) -> typing.Optional[str]:
        """Identifier for the VPN gateway."""
        return jsii.get(self, "vpnGatewayId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _VpcAttributes(jsii.compat.TypedDict, total=False):
    isolatedSubnetIds: typing.List[str]
    """List of isolated subnet IDs.

    Must be undefined or match the availability zones in length and order.
    """
    isolatedSubnetNames: typing.List[str]
    """List of names for the isolated subnets.

    Must be undefined or have a name for every isolated subnet group.
    """
    privateSubnetIds: typing.List[str]
    """List of private subnet IDs.

    Must be undefined or match the availability zones in length and order.
    """
    privateSubnetNames: typing.List[str]
    """List of names for the private subnets.

    Must be undefined or have a name for every private subnet group.
    """
    publicSubnetIds: typing.List[str]
    """List of public subnet IDs.

    Must be undefined or match the availability zones in length and order.
    """
    publicSubnetNames: typing.List[str]
    """List of names for the public subnets.

    Must be undefined or have a name for every public subnet group.
    """
    vpnGatewayId: str
    """VPN gateway's identifier."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcAttributes", jsii_struct_bases=[_VpcAttributes])
class VpcAttributes(_VpcAttributes):
    """Properties that reference an external VpcNetwork."""
    availabilityZones: typing.List[str]
    """List of availability zones for the subnets in this VPC."""

    vpcId: str
    """VPC's identifier."""

@jsii.implements(IVpcEndpoint)
class VpcEndpoint(aws_cdk.cdk.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-ec2.VpcEndpoint"):
    @staticmethod
    def __jsii_proxy_class__():
        return _VpcEndpointProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        """Creates a new construct node.

        Arguments:
            scope: The scope in which to define this construct.
            id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        """
        jsii.create(VpcEndpoint, self, [scope, id])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the policy document of the VPC endpoint. The statement must have a Principal.

        Not all interface VPC endpoints support policy. For more information
        see https://docs.aws.amazon.com/vpc/latest/userguide/vpce-interface.html

        Arguments:
            statement: the IAM statement to add.
        """
        return jsii.invoke(self, "addToPolicy", [statement])

    @property
    @jsii.member(jsii_name="vpcEndpointId")
    @abc.abstractmethod
    def vpc_endpoint_id(self) -> str:
        """The VPC endpoint identifier."""
        ...

    @property
    @jsii.member(jsii_name="policyDocument")
    def _policy_document(self) -> typing.Optional[aws_cdk.aws_iam.PolicyDocument]:
        return jsii.get(self, "policyDocument")

    @_policy_document.setter
    def _policy_document(self, value: typing.Optional[aws_cdk.aws_iam.PolicyDocument]):
        return jsii.set(self, "policyDocument", value)


class _VpcEndpointProxy(VpcEndpoint, jsii.proxy_for(aws_cdk.cdk.Resource)):
    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        """The VPC endpoint identifier."""
        return jsii.get(self, "vpcEndpointId")


@jsii.implements(IGatewayVpcEndpoint)
class GatewayVpcEndpoint(VpcEndpoint, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.GatewayVpcEndpoint"):
    """A gateway VPC endpoint.

    resource:
        AWS::EC2::VPCEndpoint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: "IVpc", service: "IGatewayVpcEndpointService", subnets: typing.Optional[typing.List["SubnetSelection"]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            vpc: The VPC network in which the gateway endpoint will be used.
            service: The service to use for this gateway VPC endpoint.
            subnets: Where to add endpoint routing. Default: private subnets
        """
        props: GatewayVpcEndpointProps = {"vpc": vpc, "service": service}

        if subnets is not None:
            props["subnets"] = subnets

        jsii.create(GatewayVpcEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="fromGatewayVpcEndpointId")
    @classmethod
    def from_gateway_vpc_endpoint_id(cls, scope: aws_cdk.cdk.Construct, id: str, gateway_vpc_endpoint_id: str) -> "IGatewayVpcEndpoint":
        """
        Arguments:
            scope: -
            id: -
            gatewayVpcEndpointId: -
        """
        return jsii.sinvoke(cls, "fromGatewayVpcEndpointId", [scope, id, gateway_vpc_endpoint_id])

    @property
    @jsii.member(jsii_name="vpcEndpointCreationTimestamp")
    def vpc_endpoint_creation_timestamp(self) -> str:
        """The date and time the gateway VPC endpoint was created.

        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointCreationTimestamp")

    @property
    @jsii.member(jsii_name="vpcEndpointDnsEntries")
    def vpc_endpoint_dns_entries(self) -> typing.List[str]:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointDnsEntries")

    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        """The gateway VPC endpoint identifier."""
        return jsii.get(self, "vpcEndpointId")

    @property
    @jsii.member(jsii_name="vpcEndpointNetworkInterfaceIds")
    def vpc_endpoint_network_interface_ids(self) -> typing.List[str]:
        """
        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointNetworkInterfaceIds")


@jsii.implements(IInterfaceVpcEndpoint)
class InterfaceVpcEndpoint(VpcEndpoint, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.InterfaceVpcEndpoint"):
    """A interface VPC endpoint.

    resource:
        AWS::EC2::VPCEndpoint
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: "IVpc", service: "IInterfaceVpcEndpointService", private_dns_enabled: typing.Optional[bool]=None, subnets: typing.Optional["SubnetSelection"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            vpc: The VPC network in which the interface endpoint will be used.
            service: The service to use for this interface VPC endpoint.
            privateDnsEnabled: Whether to associate a private hosted zone with the specified VPC. This allows you to make requests to the service using its default DNS hostname. Default: true
            subnets: The subnets in which to create an endpoint network interface. At most one per availability zone. Default: private subnets
        """
        props: InterfaceVpcEndpointProps = {"vpc": vpc, "service": service}

        if private_dns_enabled is not None:
            props["privateDnsEnabled"] = private_dns_enabled

        if subnets is not None:
            props["subnets"] = subnets

        jsii.create(InterfaceVpcEndpoint, self, [scope, id, props])

    @jsii.member(jsii_name="fromInterfaceVpcEndpointAttributes")
    @classmethod
    def from_interface_vpc_endpoint_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, port: jsii.Number, security_group_id: str, vpc_endpoint_id: str) -> "IInterfaceVpcEndpoint":
        """Imports an existing interface VPC endpoint.

        Arguments:
            scope: -
            id: -
            attrs: -
            port: The port of the service of the interface VPC endpoint.
            securityGroupId: The identifier of the security group associated with the interface VPC endpoint.
            vpcEndpointId: The interface VPC endpoint identifier.
        """
        attrs: InterfaceVpcEndpointAttributes = {"port": port, "securityGroupId": security_group_id, "vpcEndpointId": vpc_endpoint_id}

        return jsii.sinvoke(cls, "fromInterfaceVpcEndpointAttributes", [scope, id, attrs])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> "Connections":
        """Access to network connections."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """The identifier of the security group associated with this interface VPC endpoint."""
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="vpcEndpointCreationTimestamp")
    def vpc_endpoint_creation_timestamp(self) -> str:
        """The date and time the interface VPC endpoint was created.

        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointCreationTimestamp")

    @property
    @jsii.member(jsii_name="vpcEndpointDnsEntries")
    def vpc_endpoint_dns_entries(self) -> typing.List[str]:
        """The DNS entries for the interface VPC endpoint.

        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointDnsEntries")

    @property
    @jsii.member(jsii_name="vpcEndpointId")
    def vpc_endpoint_id(self) -> str:
        """The interface VPC endpoint identifier."""
        return jsii.get(self, "vpcEndpointId")

    @property
    @jsii.member(jsii_name="vpcEndpointNetworkInterfaceIds")
    def vpc_endpoint_network_interface_ids(self) -> typing.List[str]:
        """One or more network interfaces for the interface VPC endpoint.

        attribute:
            true
        """
        return jsii.get(self, "vpcEndpointNetworkInterfaceIds")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.VpcEndpointType")
class VpcEndpointType(enum.Enum):
    """The type of VPC endpoint."""
    Interface = "Interface"
    """Interface.

    An interface endpoint is an elastic network interface with a private IP
    address that serves as an entry point for traffic destined to a supported
    service.
    """
    Gateway = "Gateway"
    """Gateway.

    A gateway endpoint is a gateway that is a target for a specified route in
    your route table, used for traffic destined to a supported AWS service.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcLookupOptions", jsii_struct_bases=[])
class VpcLookupOptions(jsii.compat.TypedDict, total=False):
    """Properties for looking up an existing VPC.

    The combination of properties must specify filter down to exactly one
    non-default VPC, otherwise an error is raised.
    """
    isDefault: bool
    """Whether to match the default VPC.

    Default:
        Don't care whether we return the default VPC
    """

    tags: typing.Mapping[str,str]
    """Tags on the VPC.

    The VPC must have all of these tags

    Default:
        Don't filter on tags
    """

    vpcId: str
    """The ID of the VPC.

    If given, will import exactly this VPC.

    Default:
        Don't filter on vpcId
    """

    vpcName: str
    """The name of the VPC.

    If given, will import the VPC with this name.

    Default:
        Don't filter on vpcName
    """

class VpcNetworkProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpcNetworkProvider"):
    """Context provider to discover and import existing VPCs."""
    def __init__(self, context: aws_cdk.cdk.Construct, *, is_default: typing.Optional[bool]=None, tags: typing.Optional[typing.Mapping[str,str]]=None, vpc_id: typing.Optional[str]=None, vpc_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            context: -
            options: -
            isDefault: Whether to match the default VPC. Default: Don't care whether we return the default VPC
            tags: Tags on the VPC. The VPC must have all of these tags Default: Don't filter on tags
            vpcId: The ID of the VPC. If given, will import exactly this VPC. Default: Don't filter on vpcId
            vpcName: The name of the VPC. If given, will import the VPC with this name. Default: Don't filter on vpcName
        """
        options: VpcLookupOptions = {}

        if is_default is not None:
            options["isDefault"] = is_default

        if tags is not None:
            options["tags"] = tags

        if vpc_id is not None:
            options["vpcId"] = vpc_id

        if vpc_name is not None:
            options["vpcName"] = vpc_name

        jsii.create(VpcNetworkProvider, self, [context, options])

    @property
    @jsii.member(jsii_name="vpcProps")
    def vpc_props(self) -> "VpcAttributes":
        """Return the VPC import props matching the filter."""
        return jsii.get(self, "vpcProps")


@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpcProps", jsii_struct_bases=[])
class VpcProps(jsii.compat.TypedDict, total=False):
    """Configuration for Vpc."""
    cidr: str
    """The CIDR range to use for the VPC (e.g. '10.0.0.0/16'). Should be a minimum of /28 and maximum size of /16. The range will be split evenly into two subnets per Availability Zone (one public, one private).

    Default:
        Vpc.DEFAULT_CIDR_RANGE
    """

    defaultInstanceTenancy: "DefaultInstanceTenancy"
    """The default tenancy of instances launched into the VPC. By setting this to dedicated tenancy, instances will be launched on hardware dedicated to a single AWS customer, unless specifically specified at instance launch time. Please note, not all instance types are usable with Dedicated tenancy.

    Default:
        DefaultInstanceTenancy.Default (shared) tenancy
    """

    enableDnsHostnames: bool
    """Indicates whether the instances launched in the VPC get public DNS hostnames. If this attribute is true, instances in the VPC get public DNS hostnames, but only if the enableDnsSupport attribute is also set to true.

    Default:
        true
    """

    enableDnsSupport: bool
    """Indicates whether the DNS resolution is supported for the VPC.

    If this attribute
    is false, the Amazon-provided DNS server in the VPC that resolves public DNS hostnames
    to IP addresses is not enabled. If this attribute is true, queries to the Amazon
    provided DNS server at the 169.254.169.253 IP address, or the reserved IP address
    at the base of the VPC IPv4 network range plus two will succeed.

    Default:
        true
    """

    gatewayEndpoints: typing.Mapping[str,"GatewayVpcEndpointOptions"]
    """Gateway endpoints to add to this VPC.

    Default:
        - None.
    """

    maxAZs: jsii.Number
    """Define the maximum number of AZs to use in this region.

    If the region has more AZs than you want to use (for example, because of EIP limits),
    pick a lower number here. The AZs will be sorted and picked from the start of the list.

    If you pick a higher number than the number of AZs in the region, all AZs in
    the region will be selected. To use "all AZs" available to your account, use a
    high number (such as 99).

    Default:
        3
    """

    natGateways: jsii.Number
    """The number of NAT Gateways to create.

    For example, if set this to 1 and your subnet configuration is for 3 Public subnets then only
    one of the Public subnets will have a gateway and all Private subnets will route to this NAT Gateway.

    Default:
        maxAZs
    """

    natGatewaySubnets: "SubnetSelection"
    """Configures the subnets which will have NAT Gateways.

    You can pick a specific group of subnets by specifying the group name;
    the picked subnets must be public subnets.

    Default:
        - All public subnets.
    """

    subnetConfiguration: typing.List["SubnetConfiguration"]
    """Configure the subnets to build for each AZ.

    The subnets are constructed in the context of the VPC so you only need
    specify the configuration. The VPC details (VPC ID, specific CIDR,
    specific AZ will be calculated during creation)

    For example if you want 1 public subnet, 1 private subnet, and 1 isolated
    subnet in each AZ provide the following:
    subnetConfiguration: [
    {
    cidrMask: 24,
    name: 'ingress',
    subnetType: SubnetType.Public,
    },
    {
    cidrMask: 24,
    name: 'application',
    subnetType: SubnetType.Private,
    },
    {
    cidrMask: 28,
    name: 'rds',
    subnetType: SubnetType.Isolated,
    }
    ]

    ``cidrMask`` is optional and if not provided the IP space in the VPC will be
    evenly divided between the requested subnets.

    Default:
        - The VPC CIDR will be evenly divided between 1 public and 1
          private subnet per AZ.
    """

    vpnConnections: typing.Mapping[str,"VpnConnectionOptions"]
    """VPN connections to this VPC.

    Default:
        - No connections.
    """

    vpnGateway: bool
    """Indicates whether a VPN gateway should be created and attached to this VPC.

    Default:
        - true when vpnGatewayAsn or vpnConnections is specified.
    """

    vpnGatewayAsn: jsii.Number
    """The private Autonomous System Number (ASN) for the VPN gateway.

    Default:
        - Amazon default ASN.
    """

    vpnRoutePropagation: typing.List["SubnetSelection"]
    """Where to propagate VPN routes.

    Default:
        - On the route tables associated with private subnets.
    """

@jsii.implements(IVpnConnection)
class VpnConnection(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.VpnConnection"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: "IVpc", ip: str, asn: typing.Optional[jsii.Number]=None, static_routes: typing.Optional[typing.List[str]]=None, tunnel_options: typing.Optional[typing.List["VpnTunnelOption"]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            vpc: The VPC to connect to.
            ip: The ip address of the customer gateway.
            asn: The ASN of the customer gateway. Default: 65000
            staticRoutes: The static routes to be routed from the VPN gateway to the customer gateway. Default: Dynamic routing (BGP)
            tunnelOptions: The tunnel options for the VPN connection. At most two elements (one per tunnel). Duplicates not allowed. Default: Amazon generated tunnel options
        """
        props: VpnConnectionProps = {"vpc": vpc, "ip": ip}

        if asn is not None:
            props["asn"] = asn

        if static_routes is not None:
            props["staticRoutes"] = static_routes

        if tunnel_options is not None:
            props["tunnelOptions"] = tunnel_options

        jsii.create(VpnConnection, self, [scope, id, props])

    @jsii.member(jsii_name="metricAll")
    @classmethod
    def metric_all(cls, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for all VPN connections in the account/region.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.sinvoke(cls, "metricAll", [metric_name, props])

    @jsii.member(jsii_name="metricAllTunnelDataIn")
    @classmethod
    def metric_all_tunnel_data_in(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the tunnel data in of all VPN connections in the account/region.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.sinvoke(cls, "metricAllTunnelDataIn", [props])

    @jsii.member(jsii_name="metricAllTunnelDataOut")
    @classmethod
    def metric_all_tunnel_data_out(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the tunnel data out of all VPN connections.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            sum over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.sinvoke(cls, "metricAllTunnelDataOut", [props])

    @jsii.member(jsii_name="metricAllTunnelState")
    @classmethod
    def metric_all_tunnel_state(cls, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the tunnel state of all VPN connections in the account/region.

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.

        Default:
            average over 5 minutes
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.sinvoke(cls, "metricAllTunnelState", [props])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this VPNConnection.

        Arguments:
            metricName: -
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metric", [metric_name, props])

    @jsii.member(jsii_name="metricTunnelDataIn")
    def metric_tunnel_data_in(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The bytes received through the VPN tunnel.

        Sum over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTunnelDataIn", [props])

    @jsii.member(jsii_name="metricTunnelDataOut")
    def metric_tunnel_data_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The bytes sent through the VPN tunnel.

        Sum over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTunnelDataOut", [props])

    @jsii.member(jsii_name="metricTunnelState")
    def metric_tunnel_state(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The state of the tunnel. 0 indicates DOWN and 1 indicates UP.

        Average over 5 minutes

        Arguments:
            props: -
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: aws_cdk.aws_cloudwatch.MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "metricTunnelState", [props])

    @property
    @jsii.member(jsii_name="customerGatewayAsn")
    def customer_gateway_asn(self) -> jsii.Number:
        """The ASN of the customer gateway."""
        return jsii.get(self, "customerGatewayAsn")

    @property
    @jsii.member(jsii_name="customerGatewayId")
    def customer_gateway_id(self) -> str:
        """The id of the customer gateway."""
        return jsii.get(self, "customerGatewayId")

    @property
    @jsii.member(jsii_name="customerGatewayIp")
    def customer_gateway_ip(self) -> str:
        """The ip address of the customer gateway."""
        return jsii.get(self, "customerGatewayIp")

    @property
    @jsii.member(jsii_name="vpnId")
    def vpn_id(self) -> str:
        """The id of the VPN connection."""
        return jsii.get(self, "vpnId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _VpnConnectionOptions(jsii.compat.TypedDict, total=False):
    asn: jsii.Number
    """The ASN of the customer gateway.

    Default:
        65000
    """
    staticRoutes: typing.List[str]
    """The static routes to be routed from the VPN gateway to the customer gateway.

    Default:
        Dynamic routing (BGP)
    """
    tunnelOptions: typing.List["VpnTunnelOption"]
    """The tunnel options for the VPN connection.

    At most two elements (one per tunnel).
    Duplicates not allowed.

    Default:
        Amazon generated tunnel options
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpnConnectionOptions", jsii_struct_bases=[_VpnConnectionOptions])
class VpnConnectionOptions(_VpnConnectionOptions):
    ip: str
    """The ip address of the customer gateway."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpnConnectionProps", jsii_struct_bases=[VpnConnectionOptions])
class VpnConnectionProps(VpnConnectionOptions, jsii.compat.TypedDict):
    vpc: "IVpc"
    """The VPC to connect to."""

@jsii.enum(jsii_type="@aws-cdk/aws-ec2.VpnConnectionType")
class VpnConnectionType(enum.Enum):
    """The VPN connection type."""
    IPsec1 = "IPsec1"
    """The IPsec 1 VPN connection type."""
    Dummy = "Dummy"
    """Dummy member TODO: remove once https://github.com/awslabs/jsii/issues/231 is fixed."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ec2.VpnTunnelOption", jsii_struct_bases=[])
class VpnTunnelOption(jsii.compat.TypedDict, total=False):
    preSharedKey: str
    """The pre-shared key (PSK) to establish initial authentication between the virtual private gateway and customer gateway.

    Allowed characters are alphanumeric characters
    and ._. Must be between 8 and 64 characters in length and cannot start with zero (0).

    Default:
        an Amazon generated pre-shared key
    """

    tunnelInsideCidr: str
    """The range of inside IP addresses for the tunnel.

    Any specified CIDR blocks must be
    unique across all VPN connections that use the same virtual private gateway.
    A size /30 CIDR block from the 169.254.0.0/16 range.

    Default:
        an Amazon generated inside IP CIDR
    """

@jsii.implements(IMachineImageSource)
class WindowsImage(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.WindowsImage"):
    """Select the latest version of the indicated Windows version.

    The AMI ID is selected using the values published to the SSM parameter store.

    https://aws.amazon.com/blogs/mt/query-for-the-latest-windows-ami-using-systems-manager-parameter-store/
    """
    def __init__(self, version: "WindowsVersion") -> None:
        """
        Arguments:
            version: -
        """
        jsii.create(WindowsImage, self, [version])

    @jsii.member(jsii_name="getImage")
    def get_image(self, scope: aws_cdk.cdk.Construct) -> "MachineImage":
        """Return the image to use in the given context.

        Arguments:
            scope: -
        """
        return jsii.invoke(self, "getImage", [scope])

    @property
    @jsii.member(jsii_name="version")
    def version(self) -> "WindowsVersion":
        return jsii.get(self, "version")


class WindowsOS(OperatingSystem, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ec2.WindowsOS"):
    """OS features specialized for Windows."""
    def __init__(self) -> None:
        jsii.create(WindowsOS, self, [])

    @jsii.member(jsii_name="createUserData")
    def create_user_data(self, scripts: typing.List[str]) -> str:
        """
        Arguments:
            scripts: -
        """
        return jsii.invoke(self, "createUserData", [scripts])

    @property
    @jsii.member(jsii_name="type")
    def type(self) -> "OperatingSystemType":
        return jsii.get(self, "type")


@jsii.enum(jsii_type="@aws-cdk/aws-ec2.WindowsVersion")
class WindowsVersion(enum.Enum):
    """The Windows version to use for the WindowsImage."""
    WindowsServer2008SP2English64BitSQL2008SP4Express = "WindowsServer2008SP2English64BitSQL2008SP4Express"
    WindowsServer2012R2RTMChineseSimplified64BitBase = "WindowsServer2012R2RTMChineseSimplified64BitBase"
    WindowsServer2012R2RTMChineseTraditional64BitBase = "WindowsServer2012R2RTMChineseTraditional64BitBase"
    WindowsServer2012R2RTMDutch64BitBase = "WindowsServer2012R2RTMDutch64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Enterprise"
    WindowsServer2012R2RTMHungarian64BitBase = "WindowsServer2012R2RTMHungarian64BitBase"
    WindowsServer2012R2RTMJapanese64BitBase = "WindowsServer2012R2RTMJapanese64BitBase"
    WindowsServer2016EnglishCoreContainers = "WindowsServer2016EnglishCoreContainers"
    WindowsServer2016EnglishCoreSQL2016SP1Web = "WindowsServer2016EnglishCoreSQL2016SP1Web"
    WindowsServer2016GermanFullBase = "WindowsServer2016GermanFullBase"
    WindowsServer2003R2SP2LanguagePacks32BitBase = "WindowsServer2003R2SP2LanguagePacks32BitBase"
    WindowsServer2008R2SP1English64BitSQL2008R2SP3Web = "WindowsServer2008R2SP1English64BitSQL2008R2SP3Web"
    WindowsServer2008R2SP1English64BitSQL2012SP4Express = "WindowsServer2008R2SP1English64BitSQL2012SP4Express"
    WindowsServer2008R2SP1PortugueseBrazil64BitCore = "WindowsServer2008R2SP1PortugueseBrazil64BitCore"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Standard = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Standard"
    WindowsServer2012RTMEnglish64BitSQL2014SP2Express = "WindowsServer2012RTMEnglish64BitSQL2014SP2Express"
    WindowsServer2012RTMItalian64BitBase = "WindowsServer2012RTMItalian64BitBase"
    WindowsServer2016EnglishCoreSQL2016SP1Express = "WindowsServer2016EnglishCoreSQL2016SP1Express"
    WindowsServer2016EnglishDeepLearning = "WindowsServer2016EnglishDeepLearning"
    WindowsServer2019ItalianFullBase = "WindowsServer2019ItalianFullBase"
    WindowsServer2008R2SP1Korean64BitBase = "WindowsServer2008R2SP1Korean64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Express = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Express"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Web = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Web"
    WindowsServer2016JapaneseFullSQL2016SP2Web = "WindowsServer2016JapaneseFullSQL2016SP2Web"
    WindowsServer2016KoreanFullBase = "WindowsServer2016KoreanFullBase"
    WindowsServer2016KoreanFullSQL2016SP2Standard = "WindowsServer2016KoreanFullSQL2016SP2Standard"
    WindowsServer2016PortuguesePortugalFullBase = "WindowsServer2016PortuguesePortugalFullBase"
    WindowsServer2019EnglishFullSQL2017Web = "WindowsServer2019EnglishFullSQL2017Web"
    WindowsServer2019FrenchFullBase = "WindowsServer2019FrenchFullBase"
    WindowsServer2019KoreanFullBase = "WindowsServer2019KoreanFullBase"
    WindowsServer2008R2SP1ChineseHongKongSAR64BitBase = "WindowsServer2008R2SP1ChineseHongKongSAR64BitBase"
    WindowsServer2008R2SP1ChinesePRC64BitBase = "WindowsServer2008R2SP1ChinesePRC64BitBase"
    WindowsServer2012RTMFrench64BitBase = "WindowsServer2012RTMFrench64BitBase"
    WindowsServer2016EnglishFullContainers = "WindowsServer2016EnglishFullContainers"
    WindowsServer2016EnglishFullSQL2016SP1Standard = "WindowsServer2016EnglishFullSQL2016SP1Standard"
    WindowsServer2016RussianFullBase = "WindowsServer2016RussianFullBase"
    WindowsServer2019ChineseSimplifiedFullBase = "WindowsServer2019ChineseSimplifiedFullBase"
    WindowsServer2019EnglishFullSQL2016SP2Standard = "WindowsServer2019EnglishFullSQL2016SP2Standard"
    WindowsServer2019HungarianFullBase = "WindowsServer2019HungarianFullBase"
    WindowsServer2008R2SP1English64BitSQL2008R2SP3Express = "WindowsServer2008R2SP1English64BitSQL2008R2SP3Express"
    WindowsServer2008R2SP1LanguagePacks64BitBase = "WindowsServer2008R2SP1LanguagePacks64BitBase"
    WindowsServer2008SP2English32BitBase = "WindowsServer2008SP2English32BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2012SP4Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2012SP4Enterprise"
    WindowsServer2012RTMChineseTraditional64BitBase = "WindowsServer2012RTMChineseTraditional64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2008R2SP3Express = "WindowsServer2012RTMEnglish64BitSQL2008R2SP3Express"
    WindowsServer2012RTMEnglish64BitSQL2014SP2Standard = "WindowsServer2012RTMEnglish64BitSQL2014SP2Standard"
    WindowsServer2012RTMJapanese64BitSQL2014SP2Express = "WindowsServer2012RTMJapanese64BitSQL2014SP2Express"
    WindowsServer2016PolishFullBase = "WindowsServer2016PolishFullBase"
    WindowsServer2019EnglishFullSQL2016SP2Web = "WindowsServer2019EnglishFullSQL2016SP2Web"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Standard = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Standard"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Express = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Express"
    WindowsServer2012R2RTMEnglishDeepLearning = "WindowsServer2012R2RTMEnglishDeepLearning"
    WindowsServer2012R2RTMGerman64BitBase = "WindowsServer2012R2RTMGerman64BitBase"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Express = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Express"
    WindowsServer2012R2RTMRussian64BitBase = "WindowsServer2012R2RTMRussian64BitBase"
    WindowsServer2012RTMChineseTraditionalHongKongSAR64BitBase = "WindowsServer2012RTMChineseTraditionalHongKongSAR64BitBase"
    WindowsServer2012RTMHungarian64BitBase = "WindowsServer2012RTMHungarian64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2014SP3Standard = "WindowsServer2012RTMJapanese64BitSQL2014SP3Standard"
    WindowsServer2019EnglishFullHyperV = "WindowsServer2019EnglishFullHyperV"
    WindowsServer2003R2SP2English64BitSQL2005SP4Express = "WindowsServer2003R2SP2English64BitSQL2005SP4Express"
    WindowsServer2008R2SP1Japanese64BitSQL2012SP4Express = "WindowsServer2008R2SP1Japanese64BitSQL2012SP4Express"
    WindowsServer2012RTMGerman64BitBase = "WindowsServer2012RTMGerman64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2008R2SP3Standard = "WindowsServer2012RTMJapanese64BitSQL2008R2SP3Standard"
    WindowsServer2016EnglishFullSQL2016SP2Standard = "WindowsServer2016EnglishFullSQL2016SP2Standard"
    WindowsServer2019EnglishFullSQL2017Express = "WindowsServer2019EnglishFullSQL2017Express"
    WindowsServer2019JapaneseFullBase = "WindowsServer2019JapaneseFullBase"
    WindowsServer2019RussianFullBase = "WindowsServer2019RussianFullBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Standard = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Standard"
    WindowsServer2012R2RTMItalian64BitBase = "WindowsServer2012R2RTMItalian64BitBase"
    WindowsServer2012RTMEnglish64BitBase = "WindowsServer2012RTMEnglish64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2008R2SP3Standard = "WindowsServer2012RTMEnglish64BitSQL2008R2SP3Standard"
    WindowsServer2016EnglishFullHyperV = "WindowsServer2016EnglishFullHyperV"
    WindowsServer2016EnglishFullSQL2016SP2Enterprise = "WindowsServer2016EnglishFullSQL2016SP2Enterprise"
    WindowsServer2019ChineseTraditionalFullBase = "WindowsServer2019ChineseTraditionalFullBase"
    WindowsServer2019EnglishCoreBase = "WindowsServer2019EnglishCoreBase"
    WindowsServer2019EnglishCoreContainersLatest = "WindowsServer2019EnglishCoreContainersLatest"
    WindowsServer2008SP2English64BitBase = "WindowsServer2008SP2English64BitBase"
    WindowsServer2012R2RTMFrench64BitBase = "WindowsServer2012R2RTMFrench64BitBase"
    WindowsServer2012R2RTMPolish64BitBase = "WindowsServer2012R2RTMPolish64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2012SP4Express = "WindowsServer2012RTMEnglish64BitSQL2012SP4Express"
    WindowsServer2012RTMEnglish64BitSQL2014SP3Standard = "WindowsServer2012RTMEnglish64BitSQL2014SP3Standard"
    WindowsServer2012RTMJapanese64BitSQL2012SP4Standard = "WindowsServer2012RTMJapanese64BitSQL2012SP4Standard"
    WindowsServer2016EnglishCoreContainersLatest = "WindowsServer2016EnglishCoreContainersLatest"
    WindowsServer2019EnglishFullSQL2016SP2Express = "WindowsServer2019EnglishFullSQL2016SP2Express"
    WindowsServer2019TurkishFullBase = "WindowsServer2019TurkishFullBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Express = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Express"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Web = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Web"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Web = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Web"
    WindowsServer2012R2RTMPortugueseBrazil64BitBase = "WindowsServer2012R2RTMPortugueseBrazil64BitBase"
    WindowsServer2012R2RTMPortuguesePortugal64BitBase = "WindowsServer2012R2RTMPortuguesePortugal64BitBase"
    WindowsServer2012R2RTMSwedish64BitBase = "WindowsServer2012R2RTMSwedish64BitBase"
    WindowsServer2016EnglishFullSQL2016SP1Express = "WindowsServer2016EnglishFullSQL2016SP1Express"
    WindowsServer2016ItalianFullBase = "WindowsServer2016ItalianFullBase"
    WindowsServer2016SpanishFullBase = "WindowsServer2016SpanishFullBase"
    WindowsServer2019EnglishFullSQL2017Standard = "WindowsServer2019EnglishFullSQL2017Standard"
    WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Standard = "WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Standard"
    WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Standard = "WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Standard"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Standard = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Standard"
    WindowsServer2012RTMEnglish64BitSQL2008R2SP3Web = "WindowsServer2012RTMEnglish64BitSQL2008R2SP3Web"
    WindowsServer2012RTMJapanese64BitSQL2014SP2Web = "WindowsServer2012RTMJapanese64BitSQL2014SP2Web"
    WindowsServer2016EnglishCoreSQL2016SP2Enterprise = "WindowsServer2016EnglishCoreSQL2016SP2Enterprise"
    WindowsServer2016PortugueseBrazilFullBase = "WindowsServer2016PortugueseBrazilFullBase"
    WindowsServer2019EnglishFullBase = "WindowsServer2019EnglishFullBase"
    WindowsServer2003R2SP2English32BitBase = "WindowsServer2003R2SP2English32BitBase"
    WindowsServer2012R2RTMCzech64BitBase = "WindowsServer2012R2RTMCzech64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Standard = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Standard"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP2Express = "WindowsServer2012R2RTMJapanese64BitSQL2014SP2Express"
    WindowsServer2012RTMEnglish64BitSQL2012SP4Standard = "WindowsServer2012RTMEnglish64BitSQL2012SP4Standard"
    WindowsServer2016EnglishCoreSQL2016SP1Enterprise = "WindowsServer2016EnglishCoreSQL2016SP1Enterprise"
    WindowsServer2016JapaneseFullSQL2016SP1Web = "WindowsServer2016JapaneseFullSQL2016SP1Web"
    WindowsServer2016SwedishFullBase = "WindowsServer2016SwedishFullBase"
    WindowsServer2016TurkishFullBase = "WindowsServer2016TurkishFullBase"
    WindowsServer2008R2SP1English64BitCoreSQL2012SP4Standard = "WindowsServer2008R2SP1English64BitCoreSQL2012SP4Standard"
    WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Standard = "WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Standard"
    WindowsServer2012RTMCzech64BitBase = "WindowsServer2012RTMCzech64BitBase"
    WindowsServer2012RTMTurkish64BitBase = "WindowsServer2012RTMTurkish64BitBase"
    WindowsServer2016DutchFullBase = "WindowsServer2016DutchFullBase"
    WindowsServer2016EnglishFullSQL2016SP2Express = "WindowsServer2016EnglishFullSQL2016SP2Express"
    WindowsServer2016EnglishFullSQL2017Enterprise = "WindowsServer2016EnglishFullSQL2017Enterprise"
    WindowsServer2016HungarianFullBase = "WindowsServer2016HungarianFullBase"
    WindowsServer2016KoreanFullSQL2016SP1Standard = "WindowsServer2016KoreanFullSQL2016SP1Standard"
    WindowsServer2019SpanishFullBase = "WindowsServer2019SpanishFullBase"
    WindowsServer2003R2SP2English64BitBase = "WindowsServer2003R2SP2English64BitBase"
    WindowsServer2008R2SP1English64BitBase = "WindowsServer2008R2SP1English64BitBase"
    WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Express = "WindowsServer2008R2SP1LanguagePacks64BitSQL2008R2SP3Express"
    WindowsServer2008SP2PortugueseBrazil64BitBase = "WindowsServer2008SP2PortugueseBrazil64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Web = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Web"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP3Express = "WindowsServer2012R2RTMJapanese64BitSQL2014SP3Express"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Enterprise = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Enterprise"
    WindowsServer2012RTMJapanese64BitBase = "WindowsServer2012RTMJapanese64BitBase"
    WindowsServer2019EnglishFullContainersLatest = "WindowsServer2019EnglishFullContainersLatest"
    WindowsServer2019EnglishFullSQL2017Enterprise = "WindowsServer2019EnglishFullSQL2017Enterprise"
    WindowsServer1709EnglishCoreContainersLatest = "WindowsServer1709EnglishCoreContainersLatest"
    WindowsServer1803EnglishCoreBase = "WindowsServer1803EnglishCoreBase"
    WindowsServer2008R2SP1English64BitSQL2012SP4Web = "WindowsServer2008R2SP1English64BitSQL2012SP4Web"
    WindowsServer2008R2SP1Japanese64BitBase = "WindowsServer2008R2SP1Japanese64BitBase"
    WindowsServer2008SP2English64BitSQL2008SP4Standard = "WindowsServer2008SP2English64BitSQL2008SP4Standard"
    WindowsServer2012R2RTMEnglish64BitBase = "WindowsServer2012R2RTMEnglish64BitBase"
    WindowsServer2012RTMPortugueseBrazil64BitBase = "WindowsServer2012RTMPortugueseBrazil64BitBase"
    WindowsServer2016EnglishFullSQL2016SP1Web = "WindowsServer2016EnglishFullSQL2016SP1Web"
    WindowsServer2016EnglishP3 = "WindowsServer2016EnglishP3"
    WindowsServer2016JapaneseFullSQL2016SP1Enterprise = "WindowsServer2016JapaneseFullSQL2016SP1Enterprise"
    WindowsServer2003R2SP2LanguagePacks64BitBase = "WindowsServer2003R2SP2LanguagePacks64BitBase"
    WindowsServer2012R2RTMChineseTraditionalHongKong64BitBase = "WindowsServer2012R2RTMChineseTraditionalHongKong64BitBase"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Express = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Express"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Enterprise"
    WindowsServer2012RTMChineseSimplified64BitBase = "WindowsServer2012RTMChineseSimplified64BitBase"
    WindowsServer2012RTMEnglish64BitSQL2012SP4Web = "WindowsServer2012RTMEnglish64BitSQL2012SP4Web"
    WindowsServer2012RTMJapanese64BitSQL2014SP3Web = "WindowsServer2012RTMJapanese64BitSQL2014SP3Web"
    WindowsServer2016JapaneseFullBase = "WindowsServer2016JapaneseFullBase"
    WindowsServer2016JapaneseFullSQL2016SP1Express = "WindowsServer2016JapaneseFullSQL2016SP1Express"
    WindowsServer1803EnglishCoreContainersLatest = "WindowsServer1803EnglishCoreContainersLatest"
    WindowsServer2008R2SP1Japanese64BitSQL2012SP4Standard = "WindowsServer2008R2SP1Japanese64BitSQL2012SP4Standard"
    WindowsServer2012R2RTMEnglish64BitCore = "WindowsServer2012R2RTMEnglish64BitCore"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP2Web = "WindowsServer2012R2RTMEnglish64BitSQL2014SP2Web"
    WindowsServer2012R2RTMEnglish64BitSQL2014SP3Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2014SP3Enterprise"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Standard = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Standard"
    WindowsServer2012RTMEnglish64BitSQL2014SP3Web = "WindowsServer2012RTMEnglish64BitSQL2014SP3Web"
    WindowsServer2012RTMSwedish64BitBase = "WindowsServer2012RTMSwedish64BitBase"
    WindowsServer2016ChineseSimplifiedFullBase = "WindowsServer2016ChineseSimplifiedFullBase"
    WindowsServer2019PolishFullBase = "WindowsServer2019PolishFullBase"
    WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Web = "WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Web"
    WindowsServer2008R2SP1PortugueseBrazil64BitBase = "WindowsServer2008R2SP1PortugueseBrazil64BitBase"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP1Enterprise = "WindowsServer2012R2RTMJapanese64BitSQL2016SP1Enterprise"
    WindowsServer2012R2RTMJapanese64BitSQL2016SP2Express = "WindowsServer2012R2RTMJapanese64BitSQL2016SP2Express"
    WindowsServer2012RTMEnglish64BitSQL2014SP3Express = "WindowsServer2012RTMEnglish64BitSQL2014SP3Express"
    WindowsServer2012RTMJapanese64BitSQL2014SP2Standard = "WindowsServer2012RTMJapanese64BitSQL2014SP2Standard"
    WindowsServer2016EnglishCoreBase = "WindowsServer2016EnglishCoreBase"
    WindowsServer2016EnglishFullBase = "WindowsServer2016EnglishFullBase"
    WindowsServer2016EnglishFullSQL2017Web = "WindowsServer2016EnglishFullSQL2017Web"
    WindowsServer2019GermanFullBase = "WindowsServer2019GermanFullBase"
    WindowsServer2003R2SP2English64BitSQL2005SP4Standard = "WindowsServer2003R2SP2English64BitSQL2005SP4Standard"
    WindowsServer2008R2SP1English64BitSQL2012SP4Enterprise = "WindowsServer2008R2SP1English64BitSQL2012SP4Enterprise"
    WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Express = "WindowsServer2008R2SP1Japanese64BitSQL2008R2SP3Express"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP1Enterprise = "WindowsServer2012R2RTMEnglish64BitSQL2016SP1Enterprise"
    WindowsServer2012RTMEnglish64BitSQL2014SP2Web = "WindowsServer2012RTMEnglish64BitSQL2014SP2Web"
    WindowsServer2012RTMJapanese64BitSQL2008R2SP3Express = "WindowsServer2012RTMJapanese64BitSQL2008R2SP3Express"
    WindowsServer2016FrenchFullBase = "WindowsServer2016FrenchFullBase"
    WindowsServer2016JapaneseFullSQL2016SP2Enterprise = "WindowsServer2016JapaneseFullSQL2016SP2Enterprise"
    WindowsServer2019CzechFullBase = "WindowsServer2019CzechFullBase"
    WindowsServer1809EnglishCoreBase = "WindowsServer1809EnglishCoreBase"
    WindowsServer1809EnglishCoreContainersLatest = "WindowsServer1809EnglishCoreContainersLatest"
    WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Express = "WindowsServer2003R2SP2LanguagePacks64BitSQL2005SP4Express"
    WindowsServer2012R2RTMTurkish64BitBase = "WindowsServer2012R2RTMTurkish64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2012SP4Web = "WindowsServer2012RTMJapanese64BitSQL2012SP4Web"
    WindowsServer2012RTMPolish64BitBase = "WindowsServer2012RTMPolish64BitBase"
    WindowsServer2012RTMSpanish64BitBase = "WindowsServer2012RTMSpanish64BitBase"
    WindowsServer2016EnglishFullSQL2016SP1Enterprise = "WindowsServer2016EnglishFullSQL2016SP1Enterprise"
    WindowsServer2016JapaneseFullSQL2016SP2Express = "WindowsServer2016JapaneseFullSQL2016SP2Express"
    WindowsServer2019EnglishFullSQL2016SP2Enterprise = "WindowsServer2019EnglishFullSQL2016SP2Enterprise"
    WindowsServer1709EnglishCoreBase = "WindowsServer1709EnglishCoreBase"
    WindowsServer2008R2SP1English64BitSQL2012RTMSP2Enterprise = "WindowsServer2008R2SP1English64BitSQL2012RTMSP2Enterprise"
    WindowsServer2008R2SP1English64BitSQL2012SP4Standard = "WindowsServer2008R2SP1English64BitSQL2012SP4Standard"
    WindowsServer2008SP2PortugueseBrazil32BitBase = "WindowsServer2008SP2PortugueseBrazil32BitBase"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP2Standard = "WindowsServer2012R2RTMJapanese64BitSQL2014SP2Standard"
    WindowsServer2012RTMJapanese64BitSQL2012SP4Express = "WindowsServer2012RTMJapanese64BitSQL2012SP4Express"
    WindowsServer2012RTMPortuguesePortugal64BitBase = "WindowsServer2012RTMPortuguesePortugal64BitBase"
    WindowsServer2016CzechFullBase = "WindowsServer2016CzechFullBase"
    WindowsServer2016JapaneseFullSQL2016SP1Standard = "WindowsServer2016JapaneseFullSQL2016SP1Standard"
    WindowsServer2019DutchFullBase = "WindowsServer2019DutchFullBase"
    WindowsServer2008R2SP1English64BitCore = "WindowsServer2008R2SP1English64BitCore"
    WindowsServer2012R2RTMEnglish64BitSQL2016SP2Web = "WindowsServer2012R2RTMEnglish64BitSQL2016SP2Web"
    WindowsServer2012R2RTMKorean64BitBase = "WindowsServer2012R2RTMKorean64BitBase"
    WindowsServer2012RTMDutch64BitBase = "WindowsServer2012RTMDutch64BitBase"
    WindowsServer2016English64BitSQL2012SP4Enterprise = "WindowsServer2016English64BitSQL2012SP4Enterprise"
    WindowsServer2016EnglishCoreSQL2016SP1Standard = "WindowsServer2016EnglishCoreSQL2016SP1Standard"
    WindowsServer2016EnglishCoreSQL2016SP2Express = "WindowsServer2016EnglishCoreSQL2016SP2Express"
    WindowsServer2016EnglishCoreSQL2016SP2Web = "WindowsServer2016EnglishCoreSQL2016SP2Web"
    WindowsServer2016EnglishFullSQL2017Standard = "WindowsServer2016EnglishFullSQL2017Standard"
    WindowsServer2019PortugueseBrazilFullBase = "WindowsServer2019PortugueseBrazilFullBase"
    WindowsServer2008R2SP1English64BitSQL2008R2SP3Standard = "WindowsServer2008R2SP1English64BitSQL2008R2SP3Standard"
    WindowsServer2008R2SP1English64BitSharePoint2010SP2Foundation = "WindowsServer2008R2SP1English64BitSharePoint2010SP2Foundation"
    WindowsServer2012R2RTMEnglishP3 = "WindowsServer2012R2RTMEnglishP3"
    WindowsServer2012R2RTMJapanese64BitSQL2014SP3Standard = "WindowsServer2012R2RTMJapanese64BitSQL2014SP3Standard"
    WindowsServer2012R2RTMSpanish64BitBase = "WindowsServer2012R2RTMSpanish64BitBase"
    WindowsServer2012RTMJapanese64BitSQL2014SP3Express = "WindowsServer2012RTMJapanese64BitSQL2014SP3Express"
    WindowsServer2016EnglishCoreSQL2016SP2Standard = "WindowsServer2016EnglishCoreSQL2016SP2Standard"
    WindowsServer2016JapaneseFullSQL2016SP2Standard = "WindowsServer2016JapaneseFullSQL2016SP2Standard"
    WindowsServer2019PortuguesePortugalFullBase = "WindowsServer2019PortuguesePortugalFullBase"
    WindowsServer2019SwedishFullBase = "WindowsServer2019SwedishFullBase"
    WindowsServer2012R2RTMEnglish64BitHyperV = "WindowsServer2012R2RTMEnglish64BitHyperV"
    WindowsServer2012RTMKorean64BitBase = "WindowsServer2012RTMKorean64BitBase"
    WindowsServer2012RTMRussian64BitBase = "WindowsServer2012RTMRussian64BitBase"
    WindowsServer2016ChineseTraditionalFullBase = "WindowsServer2016ChineseTraditionalFullBase"
    WindowsServer2016EnglishFullSQL2016SP2Web = "WindowsServer2016EnglishFullSQL2016SP2Web"
    WindowsServer2016EnglishFullSQL2017Express = "WindowsServer2016EnglishFullSQL2017Express"

__all__ = ["AllTraffic", "AmazonLinuxEdition", "AmazonLinuxGeneration", "AmazonLinuxImage", "AmazonLinuxImageProps", "AmazonLinuxStorage", "AmazonLinuxVirt", "AnyIPv4", "AnyIPv6", "CfnCustomerGateway", "CfnCustomerGatewayProps", "CfnDHCPOptions", "CfnDHCPOptionsProps", "CfnEC2Fleet", "CfnEC2FleetProps", "CfnEIP", "CfnEIPAssociation", "CfnEIPAssociationProps", "CfnEIPProps", "CfnEgressOnlyInternetGateway", "CfnEgressOnlyInternetGatewayProps", "CfnFlowLog", "CfnFlowLogProps", "CfnHost", "CfnHostProps", "CfnInstance", "CfnInstanceProps", "CfnInternetGateway", "CfnInternetGatewayProps", "CfnLaunchTemplate", "CfnLaunchTemplateProps", "CfnNatGateway", "CfnNatGatewayProps", "CfnNetworkAcl", "CfnNetworkAclEntry", "CfnNetworkAclEntryProps", "CfnNetworkAclProps", "CfnNetworkInterface", "CfnNetworkInterfaceAttachment", "CfnNetworkInterfaceAttachmentProps", "CfnNetworkInterfacePermission", "CfnNetworkInterfacePermissionProps", "CfnNetworkInterfaceProps", "CfnPlacementGroup", "CfnPlacementGroupProps", "CfnRoute", "CfnRouteProps", "CfnRouteTable", "CfnRouteTableProps", "CfnSecurityGroup", "CfnSecurityGroupEgress", "CfnSecurityGroupEgressProps", "CfnSecurityGroupIngress", "CfnSecurityGroupIngressProps", "CfnSecurityGroupProps", "CfnSpotFleet", "CfnSpotFleetProps", "CfnSubnet", "CfnSubnetCidrBlock", "CfnSubnetCidrBlockProps", "CfnSubnetNetworkAclAssociation", "CfnSubnetNetworkAclAssociationProps", "CfnSubnetProps", "CfnSubnetRouteTableAssociation", "CfnSubnetRouteTableAssociationProps", "CfnTransitGateway", "CfnTransitGatewayAttachment", "CfnTransitGatewayAttachmentProps", "CfnTransitGatewayProps", "CfnTransitGatewayRoute", "CfnTransitGatewayRouteProps", "CfnTransitGatewayRouteTable", "CfnTransitGatewayRouteTableAssociation", "CfnTransitGatewayRouteTableAssociationProps", "CfnTransitGatewayRouteTablePropagation", "CfnTransitGatewayRouteTablePropagationProps", "CfnTransitGatewayRouteTableProps", "CfnVPC", "CfnVPCCidrBlock", "CfnVPCCidrBlockProps", "CfnVPCDHCPOptionsAssociation", "CfnVPCDHCPOptionsAssociationProps", "CfnVPCEndpoint", "CfnVPCEndpointConnectionNotification", "CfnVPCEndpointConnectionNotificationProps", "CfnVPCEndpointProps", "CfnVPCEndpointService", "CfnVPCEndpointServicePermissions", "CfnVPCEndpointServicePermissionsProps", "CfnVPCEndpointServiceProps", "CfnVPCGatewayAttachment", "CfnVPCGatewayAttachmentProps", "CfnVPCPeeringConnection", "CfnVPCPeeringConnectionProps", "CfnVPCProps", "CfnVPNConnection", "CfnVPNConnectionProps", "CfnVPNConnectionRoute", "CfnVPNConnectionRouteProps", "CfnVPNGateway", "CfnVPNGatewayProps", "CfnVPNGatewayRoutePropagation", "CfnVPNGatewayRoutePropagationProps", "CfnVolume", "CfnVolumeAttachment", "CfnVolumeAttachmentProps", "CfnVolumeProps", "CidrIPv4", "CidrIPv6", "ConnectionRule", "Connections", "ConnectionsProps", "DefaultInstanceTenancy", "GatewayVpcEndpoint", "GatewayVpcEndpointAwsService", "GatewayVpcEndpointOptions", "GatewayVpcEndpointProps", "GenericLinuxImage", "IConnectable", "IGatewayVpcEndpoint", "IGatewayVpcEndpointService", "IInterfaceVpcEndpoint", "IInterfaceVpcEndpointService", "IMachineImageSource", "IPortRange", "IPrivateSubnet", "IPublicSubnet", "ISecurityGroup", "ISecurityGroupRule", "ISubnet", "IVpc", "IVpcEndpoint", "IVpnConnection", "IcmpAllTypeCodes", "IcmpAllTypesAndCodes", "IcmpPing", "IcmpTypeAndCode", "InstanceClass", "InstanceSize", "InstanceType", "InstanceTypePair", "InterfaceVpcEndpoint", "InterfaceVpcEndpointAttributes", "InterfaceVpcEndpointAwsService", "InterfaceVpcEndpointOptions", "InterfaceVpcEndpointProps", "LinuxOS", "MachineImage", "OperatingSystem", "OperatingSystemType", "PrefixList", "PrivateSubnet", "PrivateSubnetAttributes", "PrivateSubnetProps", "Protocol", "PublicSubnet", "PublicSubnetAttributes", "PublicSubnetProps", "SecurityGroup", "SecurityGroupProps", "SelectedSubnets", "Subnet", "SubnetAttributes", "SubnetConfiguration", "SubnetProps", "SubnetSelection", "SubnetType", "TcpAllPorts", "TcpPort", "TcpPortRange", "UdpAllPorts", "UdpPort", "UdpPortRange", "Vpc", "VpcAttributes", "VpcEndpoint", "VpcEndpointType", "VpcLookupOptions", "VpcNetworkProvider", "VpcProps", "VpnConnection", "VpnConnectionOptions", "VpnConnectionProps", "VpnConnectionType", "VpnTunnelOption", "WindowsImage", "WindowsOS", "WindowsVersion", "__jsii_assembly__"]

publication.publish()
