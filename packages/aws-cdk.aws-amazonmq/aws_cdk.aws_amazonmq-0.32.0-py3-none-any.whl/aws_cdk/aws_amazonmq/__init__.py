import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-amazonmq", "0.32.0", __name__, "aws-amazonmq@0.32.0.jsii.tgz")
class CfnBroker(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amazonmq.CfnBroker"):
    """A CloudFormation ``AWS::AmazonMQ::Broker``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
    cloudformationResource:
        AWS::AmazonMQ::Broker
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_minor_version_upgrade: typing.Union[bool, aws_cdk.cdk.Token], broker_name: str, deployment_mode: str, engine_type: str, engine_version: str, host_instance_type: str, publicly_accessible: typing.Union[bool, aws_cdk.cdk.Token], users: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "UserProperty"]]], configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ConfigurationIdProperty"]]]=None, logs: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["LogListProperty"]]]=None, maintenance_window_start_time: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["MaintenanceWindowProperty"]]]=None, security_groups: typing.Optional[typing.List[str]]=None, subnet_ids: typing.Optional[typing.List[str]]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::AmazonMQ::Broker``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            autoMinorVersionUpgrade: ``AWS::AmazonMQ::Broker.AutoMinorVersionUpgrade``.
            brokerName: ``AWS::AmazonMQ::Broker.BrokerName``.
            deploymentMode: ``AWS::AmazonMQ::Broker.DeploymentMode``.
            engineType: ``AWS::AmazonMQ::Broker.EngineType``.
            engineVersion: ``AWS::AmazonMQ::Broker.EngineVersion``.
            hostInstanceType: ``AWS::AmazonMQ::Broker.HostInstanceType``.
            publiclyAccessible: ``AWS::AmazonMQ::Broker.PubliclyAccessible``.
            users: ``AWS::AmazonMQ::Broker.Users``.
            configuration: ``AWS::AmazonMQ::Broker.Configuration``.
            logs: ``AWS::AmazonMQ::Broker.Logs``.
            maintenanceWindowStartTime: ``AWS::AmazonMQ::Broker.MaintenanceWindowStartTime``.
            securityGroups: ``AWS::AmazonMQ::Broker.SecurityGroups``.
            subnetIds: ``AWS::AmazonMQ::Broker.SubnetIds``.
            tags: ``AWS::AmazonMQ::Broker.Tags``.
        """
        props: CfnBrokerProps = {"autoMinorVersionUpgrade": auto_minor_version_upgrade, "brokerName": broker_name, "deploymentMode": deployment_mode, "engineType": engine_type, "engineVersion": engine_version, "hostInstanceType": host_instance_type, "publiclyAccessible": publicly_accessible, "users": users}

        if configuration is not None:
            props["configuration"] = configuration

        if logs is not None:
            props["logs"] = logs

        if maintenance_window_start_time is not None:
            props["maintenanceWindowStartTime"] = maintenance_window_start_time

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if subnet_ids is not None:
            props["subnetIds"] = subnet_ids

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnBroker, self, [scope, id, props])

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
    @jsii.member(jsii_name="brokerAmqpEndpoints")
    def broker_amqp_endpoints(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            AmqpEndpoints
        """
        return jsii.get(self, "brokerAmqpEndpoints")

    @property
    @jsii.member(jsii_name="brokerArn")
    def broker_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "brokerArn")

    @property
    @jsii.member(jsii_name="brokerConfigurationId")
    def broker_configuration_id(self) -> str:
        """
        cloudformationAttribute:
            ConfigurationId
        """
        return jsii.get(self, "brokerConfigurationId")

    @property
    @jsii.member(jsii_name="brokerConfigurationRevision")
    def broker_configuration_revision(self) -> aws_cdk.cdk.Token:
        """
        cloudformationAttribute:
            ConfigurationRevision
        """
        return jsii.get(self, "brokerConfigurationRevision")

    @property
    @jsii.member(jsii_name="brokerId")
    def broker_id(self) -> str:
        return jsii.get(self, "brokerId")

    @property
    @jsii.member(jsii_name="brokerIpAddresses")
    def broker_ip_addresses(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            IpAddresses
        """
        return jsii.get(self, "brokerIpAddresses")

    @property
    @jsii.member(jsii_name="brokerMqttEndpoints")
    def broker_mqtt_endpoints(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            MqttEndpoints
        """
        return jsii.get(self, "brokerMqttEndpoints")

    @property
    @jsii.member(jsii_name="brokerOpenWireEndpoints")
    def broker_open_wire_endpoints(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            OpenWireEndpoints
        """
        return jsii.get(self, "brokerOpenWireEndpoints")

    @property
    @jsii.member(jsii_name="brokerStompEndpoints")
    def broker_stomp_endpoints(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            StompEndpoints
        """
        return jsii.get(self, "brokerStompEndpoints")

    @property
    @jsii.member(jsii_name="brokerWssEndpoints")
    def broker_wss_endpoints(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            WssEndpoints
        """
        return jsii.get(self, "brokerWssEndpoints")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBrokerProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.ConfigurationIdProperty", jsii_struct_bases=[])
    class ConfigurationIdProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html
        """
        id: str
        """``CfnBroker.ConfigurationIdProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-id
        """

        revision: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnBroker.ConfigurationIdProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-configurationid.html#cfn-amazonmq-broker-configurationid-revision
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.LogListProperty", jsii_struct_bases=[])
    class LogListProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html
        """
        audit: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBroker.LogListProperty.Audit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-audit
        """

        general: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBroker.LogListProperty.General``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-loglist.html#cfn-amazonmq-broker-loglist-general
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.MaintenanceWindowProperty", jsii_struct_bases=[])
    class MaintenanceWindowProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html
        """
        dayOfWeek: str
        """``CfnBroker.MaintenanceWindowProperty.DayOfWeek``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-dayofweek
        """

        timeOfDay: str
        """``CfnBroker.MaintenanceWindowProperty.TimeOfDay``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timeofday
        """

        timeZone: str
        """``CfnBroker.MaintenanceWindowProperty.TimeZone``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-maintenancewindow.html#cfn-amazonmq-broker-maintenancewindow-timezone
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.TagsEntryProperty", jsii_struct_bases=[])
    class TagsEntryProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html
        """
        key: str
        """``CfnBroker.TagsEntryProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-key
        """

        value: str
        """``CfnBroker.TagsEntryProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-tagsentry.html#cfn-amazonmq-broker-tagsentry-value
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _UserProperty(jsii.compat.TypedDict, total=False):
        consoleAccess: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBroker.UserProperty.ConsoleAccess``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-consoleaccess
        """
        groups: typing.List[str]
        """``CfnBroker.UserProperty.Groups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-groups
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBroker.UserProperty", jsii_struct_bases=[_UserProperty])
    class UserProperty(_UserProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html
        """
        password: str
        """``CfnBroker.UserProperty.Password``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-password
        """

        username: str
        """``CfnBroker.UserProperty.Username``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-broker-user.html#cfn-amazonmq-broker-user-username
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnBrokerProps(jsii.compat.TypedDict, total=False):
    configuration: typing.Union[aws_cdk.cdk.Token, "CfnBroker.ConfigurationIdProperty"]
    """``AWS::AmazonMQ::Broker.Configuration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-configuration
    """
    logs: typing.Union[aws_cdk.cdk.Token, "CfnBroker.LogListProperty"]
    """``AWS::AmazonMQ::Broker.Logs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-logs
    """
    maintenanceWindowStartTime: typing.Union[aws_cdk.cdk.Token, "CfnBroker.MaintenanceWindowProperty"]
    """``AWS::AmazonMQ::Broker.MaintenanceWindowStartTime``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-maintenancewindowstarttime
    """
    securityGroups: typing.List[str]
    """``AWS::AmazonMQ::Broker.SecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-securitygroups
    """
    subnetIds: typing.List[str]
    """``AWS::AmazonMQ::Broker.SubnetIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-subnetids
    """
    tags: typing.List["CfnBroker.TagsEntryProperty"]
    """``AWS::AmazonMQ::Broker.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnBrokerProps", jsii_struct_bases=[_CfnBrokerProps])
class CfnBrokerProps(_CfnBrokerProps):
    """Properties for defining a ``AWS::AmazonMQ::Broker``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html
    """
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AmazonMQ::Broker.AutoMinorVersionUpgrade``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-autominorversionupgrade
    """

    brokerName: str
    """``AWS::AmazonMQ::Broker.BrokerName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-brokername
    """

    deploymentMode: str
    """``AWS::AmazonMQ::Broker.DeploymentMode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-deploymentmode
    """

    engineType: str
    """``AWS::AmazonMQ::Broker.EngineType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-enginetype
    """

    engineVersion: str
    """``AWS::AmazonMQ::Broker.EngineVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-engineversion
    """

    hostInstanceType: str
    """``AWS::AmazonMQ::Broker.HostInstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-hostinstancetype
    """

    publiclyAccessible: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AmazonMQ::Broker.PubliclyAccessible``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-publiclyaccessible
    """

    users: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBroker.UserProperty"]]]
    """``AWS::AmazonMQ::Broker.Users``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-broker.html#cfn-amazonmq-broker-users
    """

class CfnConfiguration(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amazonmq.CfnConfiguration"):
    """A CloudFormation ``AWS::AmazonMQ::Configuration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
    cloudformationResource:
        AWS::AmazonMQ::Configuration
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, data: str, engine_type: str, engine_version: str, name: str, description: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagsEntryProperty"]]=None) -> None:
        """Create a new ``AWS::AmazonMQ::Configuration``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            data: ``AWS::AmazonMQ::Configuration.Data``.
            engineType: ``AWS::AmazonMQ::Configuration.EngineType``.
            engineVersion: ``AWS::AmazonMQ::Configuration.EngineVersion``.
            name: ``AWS::AmazonMQ::Configuration.Name``.
            description: ``AWS::AmazonMQ::Configuration.Description``.
            tags: ``AWS::AmazonMQ::Configuration.Tags``.
        """
        props: CfnConfigurationProps = {"data": data, "engineType": engine_type, "engineVersion": engine_version, "name": name}

        if description is not None:
            props["description"] = description

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationArn")
    def configuration_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "configurationArn")

    @property
    @jsii.member(jsii_name="configurationId")
    def configuration_id(self) -> str:
        """
        cloudformationAttribute:
            Id
        """
        return jsii.get(self, "configurationId")

    @property
    @jsii.member(jsii_name="configurationRevision")
    def configuration_revision(self) -> aws_cdk.cdk.Token:
        """
        cloudformationAttribute:
            Revision
        """
        return jsii.get(self, "configurationRevision")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfiguration.TagsEntryProperty", jsii_struct_bases=[])
    class TagsEntryProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html
        """
        key: str
        """``CfnConfiguration.TagsEntryProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-key
        """

        value: str
        """``CfnConfiguration.TagsEntryProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configuration-tagsentry.html#cfn-amazonmq-configuration-tagsentry-value
        """


class CfnConfigurationAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociation"):
    """A CloudFormation ``AWS::AmazonMQ::ConfigurationAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
    cloudformationResource:
        AWS::AmazonMQ::ConfigurationAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, broker: str, configuration: typing.Union[aws_cdk.cdk.Token, "ConfigurationIdProperty"]) -> None:
        """Create a new ``AWS::AmazonMQ::ConfigurationAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            broker: ``AWS::AmazonMQ::ConfigurationAssociation.Broker``.
            configuration: ``AWS::AmazonMQ::ConfigurationAssociation.Configuration``.
        """
        props: CfnConfigurationAssociationProps = {"broker": broker, "configuration": configuration}

        jsii.create(CfnConfigurationAssociation, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationAssociationId")
    def configuration_association_id(self) -> str:
        return jsii.get(self, "configurationAssociationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociation.ConfigurationIdProperty", jsii_struct_bases=[])
    class ConfigurationIdProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html
        """
        id: str
        """``CfnConfigurationAssociation.ConfigurationIdProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-id
        """

        revision: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnConfigurationAssociation.ConfigurationIdProperty.Revision``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amazonmq-configurationassociation-configurationid.html#cfn-amazonmq-configurationassociation-configurationid-revision
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationAssociationProps", jsii_struct_bases=[])
class CfnConfigurationAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::AmazonMQ::ConfigurationAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html
    """
    broker: str
    """``AWS::AmazonMQ::ConfigurationAssociation.Broker``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-broker
    """

    configuration: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationAssociation.ConfigurationIdProperty"]
    """``AWS::AmazonMQ::ConfigurationAssociation.Configuration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configurationassociation.html#cfn-amazonmq-configurationassociation-configuration
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigurationProps(jsii.compat.TypedDict, total=False):
    description: str
    """``AWS::AmazonMQ::Configuration.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-description
    """
    tags: typing.List["CfnConfiguration.TagsEntryProperty"]
    """``AWS::AmazonMQ::Configuration.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-amazonmq.CfnConfigurationProps", jsii_struct_bases=[_CfnConfigurationProps])
class CfnConfigurationProps(_CfnConfigurationProps):
    """Properties for defining a ``AWS::AmazonMQ::Configuration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html
    """
    data: str
    """``AWS::AmazonMQ::Configuration.Data``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-data
    """

    engineType: str
    """``AWS::AmazonMQ::Configuration.EngineType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-enginetype
    """

    engineVersion: str
    """``AWS::AmazonMQ::Configuration.EngineVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-engineversion
    """

    name: str
    """``AWS::AmazonMQ::Configuration.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amazonmq-configuration.html#cfn-amazonmq-configuration-name
    """

__all__ = ["CfnBroker", "CfnBrokerProps", "CfnConfiguration", "CfnConfigurationAssociation", "CfnConfigurationAssociationProps", "CfnConfigurationProps", "__jsii_assembly__"]

publication.publish()
