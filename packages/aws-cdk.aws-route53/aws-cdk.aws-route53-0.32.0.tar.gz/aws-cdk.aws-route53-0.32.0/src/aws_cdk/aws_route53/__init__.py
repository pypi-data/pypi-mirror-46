import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_logs
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-route53", "0.32.0", __name__, "aws-route53@0.32.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-route53.AliasRecordProps", jsii_struct_bases=[])
class AliasRecordProps(jsii.compat.TypedDict):
    recordName: str
    """Name for the record.

    This can be the FQDN for the record (foo.example.com) or
    a subdomain of the parent hosted zone (foo, with example.com as the hosted zone).
    """

    target: "IAliasRecordTarget"
    """Target for the alias record."""

    zone: "IHostedZone"
    """The zone in which this alias should be defined."""

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.AliasRecordTargetProps", jsii_struct_bases=[])
class AliasRecordTargetProps(jsii.compat.TypedDict):
    """Represents the properties of an alias target destination."""
    dnsName: str
    """DNS name of the target."""

    hostedZoneId: str
    """Hosted zone ID of the target."""

class CfnHealthCheck(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnHealthCheck"):
    """A CloudFormation ``AWS::Route53::HealthCheck``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html
    cloudformationResource:
        AWS::Route53::HealthCheck
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, health_check_config: typing.Union["HealthCheckConfigProperty", aws_cdk.cdk.Token], health_check_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "HealthCheckTagProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Route53::HealthCheck``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            healthCheckConfig: ``AWS::Route53::HealthCheck.HealthCheckConfig``.
            healthCheckTags: ``AWS::Route53::HealthCheck.HealthCheckTags``.
        """
        props: CfnHealthCheckProps = {"healthCheckConfig": health_check_config}

        if health_check_tags is not None:
            props["healthCheckTags"] = health_check_tags

        jsii.create(CfnHealthCheck, self, [scope, id, props])

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
    @jsii.member(jsii_name="healthCheckId")
    def health_check_id(self) -> str:
        return jsii.get(self, "healthCheckId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHealthCheckProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.AlarmIdentifierProperty", jsii_struct_bases=[])
    class AlarmIdentifierProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html
        """
        name: str
        """``CfnHealthCheck.AlarmIdentifierProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html#cfn-route53-healthcheck-alarmidentifier-name
        """

        region: str
        """``CfnHealthCheck.AlarmIdentifierProperty.Region``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-alarmidentifier.html#cfn-route53-healthcheck-alarmidentifier-region
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _HealthCheckConfigProperty(jsii.compat.TypedDict, total=False):
        alarmIdentifier: typing.Union[aws_cdk.cdk.Token, "CfnHealthCheck.AlarmIdentifierProperty"]
        """``CfnHealthCheck.HealthCheckConfigProperty.AlarmIdentifier``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-alarmidentifier
        """
        childHealthChecks: typing.List[str]
        """``CfnHealthCheck.HealthCheckConfigProperty.ChildHealthChecks``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-childhealthchecks
        """
        enableSni: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.EnableSNI``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-enablesni
        """
        failureThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.FailureThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-failurethreshold
        """
        fullyQualifiedDomainName: str
        """``CfnHealthCheck.HealthCheckConfigProperty.FullyQualifiedDomainName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-fullyqualifieddomainname
        """
        healthThreshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.HealthThreshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-healththreshold
        """
        insufficientDataHealthStatus: str
        """``CfnHealthCheck.HealthCheckConfigProperty.InsufficientDataHealthStatus``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-insufficientdatahealthstatus
        """
        inverted: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.Inverted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-inverted
        """
        ipAddress: str
        """``CfnHealthCheck.HealthCheckConfigProperty.IPAddress``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-ipaddress
        """
        measureLatency: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.MeasureLatency``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-measurelatency
        """
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-port
        """
        regions: typing.List[str]
        """``CfnHealthCheck.HealthCheckConfigProperty.Regions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-regions
        """
        requestInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnHealthCheck.HealthCheckConfigProperty.RequestInterval``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-requestinterval
        """
        resourcePath: str
        """``CfnHealthCheck.HealthCheckConfigProperty.ResourcePath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-resourcepath
        """
        searchString: str
        """``CfnHealthCheck.HealthCheckConfigProperty.SearchString``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-searchstring
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.HealthCheckConfigProperty", jsii_struct_bases=[_HealthCheckConfigProperty])
    class HealthCheckConfigProperty(_HealthCheckConfigProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html
        """
        type: str
        """``CfnHealthCheck.HealthCheckConfigProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthcheckconfig.html#cfn-route53-healthcheck-healthcheckconfig-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheck.HealthCheckTagProperty", jsii_struct_bases=[])
    class HealthCheckTagProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html
        """
        key: str
        """``CfnHealthCheck.HealthCheckTagProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html#cfn-route53-healthchecktags-key
        """

        value: str
        """``CfnHealthCheck.HealthCheckTagProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-healthcheck-healthchecktag.html#cfn-route53-healthchecktags-value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnHealthCheckProps(jsii.compat.TypedDict, total=False):
    healthCheckTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnHealthCheck.HealthCheckTagProperty"]]]
    """``AWS::Route53::HealthCheck.HealthCheckTags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthchecktags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHealthCheckProps", jsii_struct_bases=[_CfnHealthCheckProps])
class CfnHealthCheckProps(_CfnHealthCheckProps):
    """Properties for defining a ``AWS::Route53::HealthCheck``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html
    """
    healthCheckConfig: typing.Union["CfnHealthCheck.HealthCheckConfigProperty", aws_cdk.cdk.Token]
    """``AWS::Route53::HealthCheck.HealthCheckConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-healthcheck.html#cfn-route53-healthcheck-healthcheckconfig
    """

class CfnHostedZone(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnHostedZone"):
    """A CloudFormation ``AWS::Route53::HostedZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html
    cloudformationResource:
        AWS::Route53::HostedZone
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, hosted_zone_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["HostedZoneConfigProperty"]]]=None, hosted_zone_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "HostedZoneTagProperty"]]]]]=None, query_logging_config: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["QueryLoggingConfigProperty"]]]=None, vpcs: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union["VPCProperty", aws_cdk.cdk.Token]]]]]=None) -> None:
        """Create a new ``AWS::Route53::HostedZone``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::Route53::HostedZone.Name``.
            hostedZoneConfig: ``AWS::Route53::HostedZone.HostedZoneConfig``.
            hostedZoneTags: ``AWS::Route53::HostedZone.HostedZoneTags``.
            queryLoggingConfig: ``AWS::Route53::HostedZone.QueryLoggingConfig``.
            vpcs: ``AWS::Route53::HostedZone.VPCs``.
        """
        props: CfnHostedZoneProps = {"name": name}

        if hosted_zone_config is not None:
            props["hostedZoneConfig"] = hosted_zone_config

        if hosted_zone_tags is not None:
            props["hostedZoneTags"] = hosted_zone_tags

        if query_logging_config is not None:
            props["queryLoggingConfig"] = query_logging_config

        if vpcs is not None:
            props["vpcs"] = vpcs

        jsii.create(CfnHostedZone, self, [scope, id, props])

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
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        return jsii.get(self, "hostedZoneId")

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.List[str]:
        """
        cloudformationAttribute:
            NameServers
        """
        return jsii.get(self, "hostedZoneNameServers")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnHostedZoneProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.HostedZoneConfigProperty", jsii_struct_bases=[])
    class HostedZoneConfigProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzoneconfig.html
        """
        comment: str
        """``CfnHostedZone.HostedZoneConfigProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzoneconfig.html#cfn-route53-hostedzone-hostedzoneconfig-comment
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.HostedZoneTagProperty", jsii_struct_bases=[])
    class HostedZoneTagProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetags.html
        """
        key: str
        """``CfnHostedZone.HostedZoneTagProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetags.html#cfn-route53-hostedzonetags-key
        """

        value: str
        """``CfnHostedZone.HostedZoneTagProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-hostedzonetags.html#cfn-route53-hostedzonetags-value
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.QueryLoggingConfigProperty", jsii_struct_bases=[])
    class QueryLoggingConfigProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-queryloggingconfig.html
        """
        cloudWatchLogsLogGroupArn: str
        """``CfnHostedZone.QueryLoggingConfigProperty.CloudWatchLogsLogGroupArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-hostedzone-queryloggingconfig.html#cfn-route53-hostedzone-queryloggingconfig-cloudwatchlogsloggrouparn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZone.VPCProperty", jsii_struct_bases=[])
    class VPCProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone-hostedzonevpcs.html
        """
        vpcId: str
        """``CfnHostedZone.VPCProperty.VPCId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone-hostedzonevpcs.html#cfn-route53-hostedzone-hostedzonevpcs-vpcid
        """

        vpcRegion: str
        """``CfnHostedZone.VPCProperty.VPCRegion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone-hostedzonevpcs.html#cfn-route53-hostedzone-hostedzonevpcs-vpcregion
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnHostedZoneProps(jsii.compat.TypedDict, total=False):
    hostedZoneConfig: typing.Union[aws_cdk.cdk.Token, "CfnHostedZone.HostedZoneConfigProperty"]
    """``AWS::Route53::HostedZone.HostedZoneConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzoneconfig
    """
    hostedZoneTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnHostedZone.HostedZoneTagProperty"]]]
    """``AWS::Route53::HostedZone.HostedZoneTags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-hostedzonetags
    """
    queryLoggingConfig: typing.Union[aws_cdk.cdk.Token, "CfnHostedZone.QueryLoggingConfigProperty"]
    """``AWS::Route53::HostedZone.QueryLoggingConfig``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-queryloggingconfig
    """
    vpcs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnHostedZone.VPCProperty", aws_cdk.cdk.Token]]]
    """``AWS::Route53::HostedZone.VPCs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-vpcs
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnHostedZoneProps", jsii_struct_bases=[_CfnHostedZoneProps])
class CfnHostedZoneProps(_CfnHostedZoneProps):
    """Properties for defining a ``AWS::Route53::HostedZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html
    """
    name: str
    """``AWS::Route53::HostedZone.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-hostedzone.html#cfn-route53-hostedzone-name
    """

class CfnRecordSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnRecordSet"):
    """A CloudFormation ``AWS::Route53::RecordSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html
    cloudformationResource:
        AWS::Route53::RecordSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, type: str, alias_target: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["AliasTargetProperty"]]]=None, comment: typing.Optional[str]=None, failover: typing.Optional[str]=None, geo_location: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["GeoLocationProperty"]]]=None, health_check_id: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, multi_value_answer: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, region: typing.Optional[str]=None, resource_records: typing.Optional[typing.List[str]]=None, set_identifier: typing.Optional[str]=None, ttl: typing.Optional[str]=None, weight: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::Route53::RecordSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::Route53::RecordSet.Name``.
            type: ``AWS::Route53::RecordSet.Type``.
            aliasTarget: ``AWS::Route53::RecordSet.AliasTarget``.
            comment: ``AWS::Route53::RecordSet.Comment``.
            failover: ``AWS::Route53::RecordSet.Failover``.
            geoLocation: ``AWS::Route53::RecordSet.GeoLocation``.
            healthCheckId: ``AWS::Route53::RecordSet.HealthCheckId``.
            hostedZoneId: ``AWS::Route53::RecordSet.HostedZoneId``.
            hostedZoneName: ``AWS::Route53::RecordSet.HostedZoneName``.
            multiValueAnswer: ``AWS::Route53::RecordSet.MultiValueAnswer``.
            region: ``AWS::Route53::RecordSet.Region``.
            resourceRecords: ``AWS::Route53::RecordSet.ResourceRecords``.
            setIdentifier: ``AWS::Route53::RecordSet.SetIdentifier``.
            ttl: ``AWS::Route53::RecordSet.TTL``.
            weight: ``AWS::Route53::RecordSet.Weight``.
        """
        props: CfnRecordSetProps = {"name": name, "type": type}

        if alias_target is not None:
            props["aliasTarget"] = alias_target

        if comment is not None:
            props["comment"] = comment

        if failover is not None:
            props["failover"] = failover

        if geo_location is not None:
            props["geoLocation"] = geo_location

        if health_check_id is not None:
            props["healthCheckId"] = health_check_id

        if hosted_zone_id is not None:
            props["hostedZoneId"] = hosted_zone_id

        if hosted_zone_name is not None:
            props["hostedZoneName"] = hosted_zone_name

        if multi_value_answer is not None:
            props["multiValueAnswer"] = multi_value_answer

        if region is not None:
            props["region"] = region

        if resource_records is not None:
            props["resourceRecords"] = resource_records

        if set_identifier is not None:
            props["setIdentifier"] = set_identifier

        if ttl is not None:
            props["ttl"] = ttl

        if weight is not None:
            props["weight"] = weight

        jsii.create(CfnRecordSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRecordSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="recordSetDomainName")
    def record_set_domain_name(self) -> str:
        return jsii.get(self, "recordSetDomainName")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AliasTargetProperty(jsii.compat.TypedDict, total=False):
        evaluateTargetHealth: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnRecordSet.AliasTargetProperty.EvaluateTargetHealth``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSet.AliasTargetProperty", jsii_struct_bases=[_AliasTargetProperty])
    class AliasTargetProperty(_AliasTargetProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html
        """
        dnsName: str
        """``CfnRecordSet.AliasTargetProperty.DNSName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-dnshostname
        """

        hostedZoneId: str
        """``CfnRecordSet.AliasTargetProperty.HostedZoneId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-hostedzoneid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSet.GeoLocationProperty", jsii_struct_bases=[])
    class GeoLocationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html
        """
        continentCode: str
        """``CfnRecordSet.GeoLocationProperty.ContinentCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-continentcode
        """

        countryCode: str
        """``CfnRecordSet.GeoLocationProperty.CountryCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-countrycode
        """

        subdivisionCode: str
        """``CfnRecordSet.GeoLocationProperty.SubdivisionCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-subdivisioncode
        """


class CfnRecordSetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup"):
    """A CloudFormation ``AWS::Route53::RecordSetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html
    cloudformationResource:
        AWS::Route53::RecordSetGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comment: typing.Optional[str]=None, hosted_zone_id: typing.Optional[str]=None, hosted_zone_name: typing.Optional[str]=None, record_sets: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "RecordSetProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Route53::RecordSetGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            comment: ``AWS::Route53::RecordSetGroup.Comment``.
            hostedZoneId: ``AWS::Route53::RecordSetGroup.HostedZoneId``.
            hostedZoneName: ``AWS::Route53::RecordSetGroup.HostedZoneName``.
            recordSets: ``AWS::Route53::RecordSetGroup.RecordSets``.
        """
        props: CfnRecordSetGroupProps = {}

        if comment is not None:
            props["comment"] = comment

        if hosted_zone_id is not None:
            props["hostedZoneId"] = hosted_zone_id

        if hosted_zone_name is not None:
            props["hostedZoneName"] = hosted_zone_name

        if record_sets is not None:
            props["recordSets"] = record_sets

        jsii.create(CfnRecordSetGroup, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRecordSetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="recordSetGroupName")
    def record_set_group_name(self) -> str:
        return jsii.get(self, "recordSetGroupName")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AliasTargetProperty(jsii.compat.TypedDict, total=False):
        evaluateTargetHealth: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnRecordSetGroup.AliasTargetProperty.EvaluateTargetHealth``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-evaluatetargethealth
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.AliasTargetProperty", jsii_struct_bases=[_AliasTargetProperty])
    class AliasTargetProperty(_AliasTargetProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html
        """
        dnsName: str
        """``CfnRecordSetGroup.AliasTargetProperty.DNSName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-dnshostname
        """

        hostedZoneId: str
        """``CfnRecordSetGroup.AliasTargetProperty.HostedZoneId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-aliastarget.html#cfn-route53-aliastarget-hostedzoneid
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.GeoLocationProperty", jsii_struct_bases=[])
    class GeoLocationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html
        """
        continentCode: str
        """``CfnRecordSetGroup.GeoLocationProperty.ContinentCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordsetgroup-geolocation-continentcode
        """

        countryCode: str
        """``CfnRecordSetGroup.GeoLocationProperty.CountryCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-countrycode
        """

        subdivisionCode: str
        """``CfnRecordSetGroup.GeoLocationProperty.SubdivisionCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset-geolocation.html#cfn-route53-recordset-geolocation-subdivisioncode
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordSetProperty(jsii.compat.TypedDict, total=False):
        aliasTarget: typing.Union[aws_cdk.cdk.Token, "CfnRecordSetGroup.AliasTargetProperty"]
        """``CfnRecordSetGroup.RecordSetProperty.AliasTarget``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-aliastarget
        """
        comment: str
        """``CfnRecordSetGroup.RecordSetProperty.Comment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-comment
        """
        failover: str
        """``CfnRecordSetGroup.RecordSetProperty.Failover``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-failover
        """
        geoLocation: typing.Union[aws_cdk.cdk.Token, "CfnRecordSetGroup.GeoLocationProperty"]
        """``CfnRecordSetGroup.RecordSetProperty.GeoLocation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-geolocation
        """
        healthCheckId: str
        """``CfnRecordSetGroup.RecordSetProperty.HealthCheckId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-healthcheckid
        """
        hostedZoneId: str
        """``CfnRecordSetGroup.RecordSetProperty.HostedZoneId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzoneid
        """
        hostedZoneName: str
        """``CfnRecordSetGroup.RecordSetProperty.HostedZoneName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzonename
        """
        multiValueAnswer: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnRecordSetGroup.RecordSetProperty.MultiValueAnswer``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-multivalueanswer
        """
        region: str
        """``CfnRecordSetGroup.RecordSetProperty.Region``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-region
        """
        resourceRecords: typing.List[str]
        """``CfnRecordSetGroup.RecordSetProperty.ResourceRecords``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-resourcerecords
        """
        setIdentifier: str
        """``CfnRecordSetGroup.RecordSetProperty.SetIdentifier``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-setidentifier
        """
        ttl: str
        """``CfnRecordSetGroup.RecordSetProperty.TTL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-ttl
        """
        weight: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnRecordSetGroup.RecordSetProperty.Weight``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-weight
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroup.RecordSetProperty", jsii_struct_bases=[_RecordSetProperty])
    class RecordSetProperty(_RecordSetProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html
        """
        name: str
        """``CfnRecordSetGroup.RecordSetProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-name
        """

        type: str
        """``CfnRecordSetGroup.RecordSetProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-type
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetGroupProps", jsii_struct_bases=[])
class CfnRecordSetGroupProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::Route53::RecordSetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html
    """
    comment: str
    """``AWS::Route53::RecordSetGroup.Comment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-comment
    """

    hostedZoneId: str
    """``AWS::Route53::RecordSetGroup.HostedZoneId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzoneid
    """

    hostedZoneName: str
    """``AWS::Route53::RecordSetGroup.HostedZoneName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-hostedzonename
    """

    recordSets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRecordSetGroup.RecordSetProperty"]]]
    """``AWS::Route53::RecordSetGroup.RecordSets``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-route53-recordsetgroup.html#cfn-route53-recordsetgroup-recordsets
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRecordSetProps(jsii.compat.TypedDict, total=False):
    aliasTarget: typing.Union[aws_cdk.cdk.Token, "CfnRecordSet.AliasTargetProperty"]
    """``AWS::Route53::RecordSet.AliasTarget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-aliastarget
    """
    comment: str
    """``AWS::Route53::RecordSet.Comment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-comment
    """
    failover: str
    """``AWS::Route53::RecordSet.Failover``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-failover
    """
    geoLocation: typing.Union[aws_cdk.cdk.Token, "CfnRecordSet.GeoLocationProperty"]
    """``AWS::Route53::RecordSet.GeoLocation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-geolocation
    """
    healthCheckId: str
    """``AWS::Route53::RecordSet.HealthCheckId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-healthcheckid
    """
    hostedZoneId: str
    """``AWS::Route53::RecordSet.HostedZoneId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzoneid
    """
    hostedZoneName: str
    """``AWS::Route53::RecordSet.HostedZoneName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-hostedzonename
    """
    multiValueAnswer: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::Route53::RecordSet.MultiValueAnswer``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-multivalueanswer
    """
    region: str
    """``AWS::Route53::RecordSet.Region``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-region
    """
    resourceRecords: typing.List[str]
    """``AWS::Route53::RecordSet.ResourceRecords``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-resourcerecords
    """
    setIdentifier: str
    """``AWS::Route53::RecordSet.SetIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-setidentifier
    """
    ttl: str
    """``AWS::Route53::RecordSet.TTL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-ttl
    """
    weight: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::Route53::RecordSet.Weight``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-weight
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CfnRecordSetProps", jsii_struct_bases=[_CfnRecordSetProps])
class CfnRecordSetProps(_CfnRecordSetProps):
    """Properties for defining a ``AWS::Route53::RecordSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html
    """
    name: str
    """``AWS::Route53::RecordSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-name
    """

    type: str
    """``AWS::Route53::RecordSet.Type``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-route53-recordset.html#cfn-route53-recordset-type
    """

class CnameRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.CnameRecord"):
    """A DNS CNAME record."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, record_name: str, record_value: str, zone: "IHostedZone", ttl: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            recordName: The domain name for this record set.
            recordValue: The value for this record set.
            zone: The hosted zone in which to define the new TXT record.
            ttl: The resource record cache time to live (TTL) in seconds. Default: 1800 seconds
        """
        props: CnameRecordProps = {"recordName": record_name, "recordValue": record_value, "zone": zone}

        if ttl is not None:
            props["ttl"] = ttl

        jsii.create(CnameRecord, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CnameRecordProps(jsii.compat.TypedDict, total=False):
    ttl: jsii.Number
    """The resource record cache time to live (TTL) in seconds.

    Default:
        1800 seconds
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CnameRecordProps", jsii_struct_bases=[_CnameRecordProps])
class CnameRecordProps(_CnameRecordProps):
    recordName: str
    """The domain name for this record set."""

    recordValue: str
    """The value for this record set."""

    zone: "IHostedZone"
    """The hosted zone in which to define the new TXT record."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CommonHostedZoneProps(jsii.compat.TypedDict, total=False):
    comment: str
    """Any comments that you want to include about the hosted zone.

    Default:
        none
    """
    queryLogsLogGroupArn: str
    """The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to.

    Default:
        disabled
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.CommonHostedZoneProps", jsii_struct_bases=[_CommonHostedZoneProps])
class CommonHostedZoneProps(_CommonHostedZoneProps):
    zoneName: str
    """The name of the domain.

    For resource record types that include a domain
    name, specify a fully qualified domain name.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneAttributes", jsii_struct_bases=[])
class HostedZoneAttributes(jsii.compat.TypedDict):
    """Reference to a hosted zone."""
    hostedZoneId: str
    """Identifier of the hosted zone."""

    zoneName: str
    """Name of the hosted zone."""

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneProps", jsii_struct_bases=[CommonHostedZoneProps])
class HostedZoneProps(CommonHostedZoneProps, jsii.compat.TypedDict, total=False):
    """Properties of a new hosted zone."""
    vpcs: typing.List[aws_cdk.aws_ec2.IVpc]
    """A VPC that you want to associate with this hosted zone.

    When you specify
    this property, a private hosted zone will be created.

    You can associate additional VPCs to this private zone using ``addVpc(vpc)``.

    Default:
        public (no VPCs associated)
    """

class HostedZoneProvider(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.HostedZoneProvider"):
    """Context provider that will lookup the Hosted Zone ID for the given arguments."""
    def __init__(self, context: aws_cdk.cdk.Construct, *, domain_name: str, private_zone: typing.Optional[bool]=None, vpc_id: typing.Optional[str]=None) -> None:
        """
        Arguments:
            context: -
            props: -
            domainName: The zone domain e.g. example.com.
            privateZone: Is this a private zone.
            vpcId: If this is a private zone which VPC is assocaitated.
        """
        props: HostedZoneProviderProps = {"domainName": domain_name}

        if private_zone is not None:
            props["privateZone"] = private_zone

        if vpc_id is not None:
            props["vpcId"] = vpc_id

        jsii.create(HostedZoneProvider, self, [context, props])

    @jsii.member(jsii_name="findAndImport")
    def find_and_import(self, scope: aws_cdk.cdk.Construct, id: str) -> "IHostedZone":
        """This method calls ``findHostedZone`` and returns the imported hosted zone.

        Arguments:
            scope: -
            id: -
        """
        return jsii.invoke(self, "findAndImport", [scope, id])

    @jsii.member(jsii_name="findHostedZone")
    def find_hosted_zone(self) -> "HostedZoneAttributes":
        """Return the hosted zone meeting the filter."""
        return jsii.invoke(self, "findHostedZone", [])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _HostedZoneProviderProps(jsii.compat.TypedDict, total=False):
    privateZone: bool
    """Is this a private zone."""
    vpcId: str
    """If this is a private zone which VPC is assocaitated."""

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.HostedZoneProviderProps", jsii_struct_bases=[_HostedZoneProviderProps])
class HostedZoneProviderProps(_HostedZoneProviderProps):
    """Zone properties for looking up the Hosted Zone."""
    domainName: str
    """The zone domain e.g. example.com."""

@jsii.interface(jsii_type="@aws-cdk/aws-route53.IAliasRecord")
class IAliasRecord(aws_cdk.cdk.IConstruct, jsii.compat.Protocol):
    """An alias record."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IAliasRecordProxy

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the record."""
        ...


class _IAliasRecordProxy(jsii.proxy_for(aws_cdk.cdk.IConstruct)):
    """An alias record."""
    __jsii_type__ = "@aws-cdk/aws-route53.IAliasRecord"
    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the record."""
        return jsii.get(self, "domainName")


@jsii.implements(IAliasRecord)
class AliasRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.AliasRecord"):
    """Define a new Route53 alias record."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, record_name: str, target: "IAliasRecordTarget", zone: "IHostedZone") -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            recordName: Name for the record. This can be the FQDN for the record (foo.example.com) or a subdomain of the parent hosted zone (foo, with example.com as the hosted zone).
            target: Target for the alias record.
            zone: The zone in which this alias should be defined.
        """
        props: AliasRecordProps = {"recordName": record_name, "target": target, "zone": zone}

        jsii.create(AliasRecord, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> str:
        """The domain name of the record."""
        return jsii.get(self, "domainName")


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IAliasRecordTarget")
class IAliasRecordTarget(jsii.compat.Protocol):
    """Classes that are valid alias record targets, like CloudFront distributions and load balancers, should implement this interface."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IAliasRecordTargetProxy

    @jsii.member(jsii_name="bind")
    def bind(self, record: "IAliasRecord") -> "AliasRecordTargetProps":
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        Arguments:
            record: -
        """
        ...


class _IAliasRecordTargetProxy():
    """Classes that are valid alias record targets, like CloudFront distributions and load balancers, should implement this interface."""
    __jsii_type__ = "@aws-cdk/aws-route53.IAliasRecordTarget"
    @jsii.member(jsii_name="bind")
    def bind(self, record: "IAliasRecord") -> "AliasRecordTargetProps":
        """Return hosted zone ID and DNS name, usable for Route53 alias targets.

        Arguments:
            record: -
        """
        return jsii.invoke(self, "bind", [record])


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IHostedZone")
class IHostedZone(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """Imported or created hosted zone."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IHostedZoneProxy

    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """ID of this hosted zone, such as "Z23ABC4XYZL05B".

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        """FQDN of this hosted zone."""
        ...

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        """Returns the set of name servers for the specific hosted zone. For example: ns1.example.com.

        This attribute will be undefined for private hosted zones or hosted zones imported from another stack.

        attribute:
            true
        """
        ...


class _IHostedZoneProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """Imported or created hosted zone."""
    __jsii_type__ = "@aws-cdk/aws-route53.IHostedZone"
    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """ID of this hosted zone, such as "Z23ABC4XYZL05B".

        attribute:
            true
        """
        return jsii.get(self, "hostedZoneId")

    @property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        """FQDN of this hosted zone."""
        return jsii.get(self, "zoneName")

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        """Returns the set of name servers for the specific hosted zone. For example: ns1.example.com.

        This attribute will be undefined for private hosted zones or hosted zones imported from another stack.

        attribute:
            true
        """
        return jsii.get(self, "hostedZoneNameServers")


@jsii.implements(IHostedZone)
class HostedZone(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.HostedZone"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpcs: typing.Optional[typing.List[aws_cdk.aws_ec2.IVpc]]=None, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            vpcs: A VPC that you want to associate with this hosted zone. When you specify this property, a private hosted zone will be created. You can associate additional VPCs to this private zone using ``addVpc(vpc)``. Default: public (no VPCs associated)
            zoneName: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
            comment: Any comments that you want to include about the hosted zone. Default: none
            queryLogsLogGroupArn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        props: HostedZoneProps = {"zoneName": zone_name}

        if vpcs is not None:
            props["vpcs"] = vpcs

        if comment is not None:
            props["comment"] = comment

        if query_logs_log_group_arn is not None:
            props["queryLogsLogGroupArn"] = query_logs_log_group_arn

        jsii.create(HostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="fromHostedZoneAttributes")
    @classmethod
    def from_hosted_zone_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, hosted_zone_id: str, zone_name: str) -> "IHostedZone":
        """Imports a hosted zone from another stack.

        Arguments:
            scope: -
            id: -
            attrs: -
            hostedZoneId: Identifier of the hosted zone.
            zoneName: Name of the hosted zone.
        """
        attrs: HostedZoneAttributes = {"hostedZoneId": hosted_zone_id, "zoneName": zone_name}

        return jsii.sinvoke(cls, "fromHostedZoneAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="fromHostedZoneId")
    @classmethod
    def from_hosted_zone_id(cls, scope: aws_cdk.cdk.Construct, id: str, hosted_zone_id: str) -> "IHostedZone":
        """
        Arguments:
            scope: -
            id: -
            hostedZoneId: -
        """
        return jsii.sinvoke(cls, "fromHostedZoneId", [scope, id, hosted_zone_id])

    @jsii.member(jsii_name="addVpc")
    def add_vpc(self, vpc: aws_cdk.aws_ec2.IVpc) -> None:
        """Add another VPC to this private hosted zone.

        Arguments:
            vpc: the other VPC to add.
        """
        return jsii.invoke(self, "addVpc", [vpc])

    @property
    @jsii.member(jsii_name="hostedZoneId")
    def hosted_zone_id(self) -> str:
        """ID of this hosted zone, such as "Z23ABC4XYZL05B"."""
        return jsii.get(self, "hostedZoneId")

    @property
    @jsii.member(jsii_name="vpcs")
    def _vpcs(self) -> typing.List["CfnHostedZone.VPCProperty"]:
        """VPCs to which this hosted zone will be added."""
        return jsii.get(self, "vpcs")

    @property
    @jsii.member(jsii_name="zoneName")
    def zone_name(self) -> str:
        """FQDN of this hosted zone."""
        return jsii.get(self, "zoneName")

    @property
    @jsii.member(jsii_name="hostedZoneNameServers")
    def hosted_zone_name_servers(self) -> typing.Optional[typing.List[str]]:
        """Returns the set of name servers for the specific hosted zone. For example: ns1.example.com.

        This attribute will be undefined for private hosted zones or hosted zones imported from another stack.
        """
        return jsii.get(self, "hostedZoneNameServers")


@jsii.interface(jsii_type="@aws-cdk/aws-route53.IPrivateHostedZone")
class IPrivateHostedZone(IHostedZone, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPrivateHostedZoneProxy

    pass

class _IPrivateHostedZoneProxy(jsii.proxy_for(IHostedZone)):
    __jsii_type__ = "@aws-cdk/aws-route53.IPrivateHostedZone"
    pass

@jsii.interface(jsii_type="@aws-cdk/aws-route53.IPublicHostedZone")
class IPublicHostedZone(IHostedZone, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IPublicHostedZoneProxy

    pass

class _IPublicHostedZoneProxy(jsii.proxy_for(IHostedZone)):
    __jsii_type__ = "@aws-cdk/aws-route53.IPublicHostedZone"
    pass

@jsii.implements(IPrivateHostedZone)
class PrivateHostedZone(HostedZone, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.PrivateHostedZone"):
    """Create a Route53 private hosted zone for use in one or more VPCs.

    Note that ``enableDnsHostnames`` and ``enableDnsSupport`` must have been enabled
    for the VPC you're configuring for private hosted zones.

    resource:
        AWS::Route53::HostedZone
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, vpc: aws_cdk.aws_ec2.IVpc, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            vpc: A VPC that you want to associate with this hosted zone. Private hosted zones must be associated with at least one VPC. You can associated additional VPCs using ``addVpc(vpc)``.
            zoneName: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
            comment: Any comments that you want to include about the hosted zone. Default: none
            queryLogsLogGroupArn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        props: PrivateHostedZoneProps = {"vpc": vpc, "zoneName": zone_name}

        if comment is not None:
            props["comment"] = comment

        if query_logs_log_group_arn is not None:
            props["queryLogsLogGroupArn"] = query_logs_log_group_arn

        jsii.create(PrivateHostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="fromPrivateHostedZoneId")
    @classmethod
    def from_private_hosted_zone_id(cls, scope: aws_cdk.cdk.Construct, id: str, private_hosted_zone_id: str) -> "IPrivateHostedZone":
        """
        Arguments:
            scope: -
            id: -
            privateHostedZoneId: -
        """
        return jsii.sinvoke(cls, "fromPrivateHostedZoneId", [scope, id, private_hosted_zone_id])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.PrivateHostedZoneProps", jsii_struct_bases=[CommonHostedZoneProps])
class PrivateHostedZoneProps(CommonHostedZoneProps, jsii.compat.TypedDict):
    vpc: aws_cdk.aws_ec2.IVpc
    """A VPC that you want to associate with this hosted zone.

    Private hosted zones must be associated with at least one VPC. You can
    associated additional VPCs using ``addVpc(vpc)``.
    """

@jsii.implements(IPublicHostedZone)
class PublicHostedZone(HostedZone, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.PublicHostedZone"):
    """Create a Route53 public hosted zone.

    resource:
        AWS::Route53::HostedZone
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, zone_name: str, comment: typing.Optional[str]=None, query_logs_log_group_arn: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            zoneName: The name of the domain. For resource record types that include a domain name, specify a fully qualified domain name.
            comment: Any comments that you want to include about the hosted zone. Default: none
            queryLogsLogGroupArn: The Amazon Resource Name (ARN) for the log group that you want Amazon Route 53 to send query logs to. Default: disabled
        """
        props: PublicHostedZoneProps = {"zoneName": zone_name}

        if comment is not None:
            props["comment"] = comment

        if query_logs_log_group_arn is not None:
            props["queryLogsLogGroupArn"] = query_logs_log_group_arn

        jsii.create(PublicHostedZone, self, [scope, id, props])

    @jsii.member(jsii_name="fromPublicHostedZoneId")
    @classmethod
    def from_public_hosted_zone_id(cls, scope: aws_cdk.cdk.Construct, id: str, public_hosted_zone_id: str) -> "IPublicHostedZone":
        """
        Arguments:
            scope: -
            id: -
            publicHostedZoneId: -
        """
        return jsii.sinvoke(cls, "fromPublicHostedZoneId", [scope, id, public_hosted_zone_id])

    @jsii.member(jsii_name="addDelegation")
    def add_delegation(self, delegate: "IPublicHostedZone", *, comment: typing.Optional[str]=None, ttl: typing.Optional[jsii.Number]=None) -> None:
        """Adds a delegation from this zone to a designated zone.

        Arguments:
            delegate: the zone being delegated to.
            opts: options for creating the DNS record, if any.
            comment: A comment to add on the DNS record created to incorporate the delegation. Default: none
            ttl: The TTL (Time To Live) of the DNS delegation record in DNS caches. Default: 172800
        """
        opts: ZoneDelegationOptions = {}

        if comment is not None:
            opts["comment"] = comment

        if ttl is not None:
            opts["ttl"] = ttl

        return jsii.invoke(self, "addDelegation", [delegate, opts])

    @jsii.member(jsii_name="addVpc")
    def add_vpc(self, _vpc: aws_cdk.aws_ec2.IVpc) -> None:
        """Add another VPC to this private hosted zone.

        Arguments:
            _vpc: -
        """
        return jsii.invoke(self, "addVpc", [_vpc])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.PublicHostedZoneProps", jsii_struct_bases=[CommonHostedZoneProps])
class PublicHostedZoneProps(CommonHostedZoneProps, jsii.compat.TypedDict):
    pass

class TxtRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.TxtRecord"):
    """A DNS TXT record."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, record_name: str, record_value: str, zone: "IHostedZone", ttl: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            recordName: The domain name for this record set.
            recordValue: The value for this record set.
            zone: The hosted zone in which to define the new TXT record.
            ttl: The resource record cache time to live (TTL) in seconds. Default: 1800 seconds
        """
        props: TxtRecordProps = {"recordName": record_name, "recordValue": record_value, "zone": zone}

        if ttl is not None:
            props["ttl"] = ttl

        jsii.create(TxtRecord, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _TxtRecordProps(jsii.compat.TypedDict, total=False):
    ttl: jsii.Number
    """The resource record cache time to live (TTL) in seconds.

    Default:
        1800 seconds
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.TxtRecordProps", jsii_struct_bases=[_TxtRecordProps])
class TxtRecordProps(_TxtRecordProps):
    recordName: str
    """The domain name for this record set."""

    recordValue: str
    """The value for this record set."""

    zone: "IHostedZone"
    """The hosted zone in which to define the new TXT record."""

@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ZoneDelegationOptions", jsii_struct_bases=[])
class ZoneDelegationOptions(jsii.compat.TypedDict, total=False):
    """Options available when creating a delegation relationship from one PublicHostedZone to another."""
    comment: str
    """A comment to add on the DNS record created to incorporate the delegation.

    Default:
        none
    """

    ttl: jsii.Number
    """The TTL (Time To Live) of the DNS delegation record in DNS caches.

    Default:
        172800
    """

class ZoneDelegationRecord(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-route53.ZoneDelegationRecord"):
    """A record to delegate further lookups to a different set of name servers."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, delegated_zone_name: str, name_servers: typing.List[str], zone: "IHostedZone", comment: typing.Optional[str]=None, ttl: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            delegatedZoneName: The name of the zone that delegation is made to.
            nameServers: The name servers to report in the delegation records.
            zone: The zone in which this delegate is defined.
            comment: A comment to add on the DNS record created to incorporate the delegation. Default: none
            ttl: The TTL (Time To Live) of the DNS delegation record in DNS caches. Default: 172800
        """
        props: ZoneDelegationRecordProps = {"delegatedZoneName": delegated_zone_name, "nameServers": name_servers, "zone": zone}

        if comment is not None:
            props["comment"] = comment

        if ttl is not None:
            props["ttl"] = ttl

        jsii.create(ZoneDelegationRecord, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-route53.ZoneDelegationRecordProps", jsii_struct_bases=[ZoneDelegationOptions])
class ZoneDelegationRecordProps(ZoneDelegationOptions, jsii.compat.TypedDict):
    delegatedZoneName: str
    """The name of the zone that delegation is made to."""

    nameServers: typing.List[str]
    """The name servers to report in the delegation records."""

    zone: "IHostedZone"
    """The zone in which this delegate is defined."""

__all__ = ["AliasRecord", "AliasRecordProps", "AliasRecordTargetProps", "CfnHealthCheck", "CfnHealthCheckProps", "CfnHostedZone", "CfnHostedZoneProps", "CfnRecordSet", "CfnRecordSetGroup", "CfnRecordSetGroupProps", "CfnRecordSetProps", "CnameRecord", "CnameRecordProps", "CommonHostedZoneProps", "HostedZone", "HostedZoneAttributes", "HostedZoneProps", "HostedZoneProvider", "HostedZoneProviderProps", "IAliasRecord", "IAliasRecordTarget", "IHostedZone", "IPrivateHostedZone", "IPublicHostedZone", "PrivateHostedZone", "PrivateHostedZoneProps", "PublicHostedZone", "PublicHostedZoneProps", "TxtRecord", "TxtRecordProps", "ZoneDelegationOptions", "ZoneDelegationRecord", "ZoneDelegationRecordProps", "__jsii_assembly__"]

publication.publish()
