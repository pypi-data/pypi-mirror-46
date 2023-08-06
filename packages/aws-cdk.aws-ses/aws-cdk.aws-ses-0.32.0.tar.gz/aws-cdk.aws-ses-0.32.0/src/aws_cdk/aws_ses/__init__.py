import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ses", "0.32.0", __name__, "aws-ses@0.32.0.jsii.tgz")
class CfnConfigurationSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnConfigurationSet"):
    """A CloudFormation ``AWS::SES::ConfigurationSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html
    cloudformationResource:
        AWS::SES::ConfigurationSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SES::ConfigurationSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::SES::ConfigurationSet.Name``.
        """
        props: CfnConfigurationSetProps = {}

        if name is not None:
            props["name"] = name

        jsii.create(CfnConfigurationSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationSetName")
    def configuration_set_name(self) -> str:
        return jsii.get(self, "configurationSetName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationSetProps":
        return jsii.get(self, "propertyOverrides")


class CfnConfigurationSetEventDestination(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination"):
    """A CloudFormation ``AWS::SES::ConfigurationSetEventDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html
    cloudformationResource:
        AWS::SES::ConfigurationSetEventDestination
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, configuration_set_name: str, event_destination: typing.Union["EventDestinationProperty", aws_cdk.cdk.Token]) -> None:
        """Create a new ``AWS::SES::ConfigurationSetEventDestination``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            configurationSetName: ``AWS::SES::ConfigurationSetEventDestination.ConfigurationSetName``.
            eventDestination: ``AWS::SES::ConfigurationSetEventDestination.EventDestination``.
        """
        props: CfnConfigurationSetEventDestinationProps = {"configurationSetName": configuration_set_name, "eventDestination": event_destination}

        jsii.create(CfnConfigurationSetEventDestination, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnConfigurationSetEventDestinationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.CloudWatchDestinationProperty", jsii_struct_bases=[])
    class CloudWatchDestinationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-cloudwatchdestination.html
        """
        dimensionConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.DimensionConfigurationProperty"]]]
        """``CfnConfigurationSetEventDestination.CloudWatchDestinationProperty.DimensionConfigurations``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-cloudwatchdestination.html#cfn-ses-configurationseteventdestination-cloudwatchdestination-dimensionconfigurations
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.DimensionConfigurationProperty", jsii_struct_bases=[])
    class DimensionConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html
        """
        defaultDimensionValue: str
        """``CfnConfigurationSetEventDestination.DimensionConfigurationProperty.DefaultDimensionValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-defaultdimensionvalue
        """

        dimensionName: str
        """``CfnConfigurationSetEventDestination.DimensionConfigurationProperty.DimensionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-dimensionname
        """

        dimensionValueSource: str
        """``CfnConfigurationSetEventDestination.DimensionConfigurationProperty.DimensionValueSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-dimensionconfiguration.html#cfn-ses-configurationseteventdestination-dimensionconfiguration-dimensionvaluesource
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _EventDestinationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.CloudWatchDestinationProperty"]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.CloudWatchDestination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-cloudwatchdestination
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-enabled
        """
        kinesisFirehoseDestination: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty"]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.KinesisFirehoseDestination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-kinesisfirehosedestination
        """
        name: str
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.EventDestinationProperty", jsii_struct_bases=[_EventDestinationProperty])
    class EventDestinationProperty(_EventDestinationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html
        """
        matchingEventTypes: typing.List[str]
        """``CfnConfigurationSetEventDestination.EventDestinationProperty.MatchingEventTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-eventdestination.html#cfn-ses-configurationseteventdestination-eventdestination-matchingeventtypes
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty", jsii_struct_bases=[])
    class KinesisFirehoseDestinationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html
        """
        deliveryStreamArn: str
        """``CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty.DeliveryStreamARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html#cfn-ses-configurationseteventdestination-kinesisfirehosedestination-deliverystreamarn
        """

        iamRoleArn: str
        """``CfnConfigurationSetEventDestination.KinesisFirehoseDestinationProperty.IAMRoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-configurationseteventdestination-kinesisfirehosedestination.html#cfn-ses-configurationseteventdestination-kinesisfirehosedestination-iamrolearn
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetEventDestinationProps", jsii_struct_bases=[])
class CfnConfigurationSetEventDestinationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::SES::ConfigurationSetEventDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html
    """
    configurationSetName: str
    """``AWS::SES::ConfigurationSetEventDestination.ConfigurationSetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-configurationsetname
    """

    eventDestination: typing.Union["CfnConfigurationSetEventDestination.EventDestinationProperty", aws_cdk.cdk.Token]
    """``AWS::SES::ConfigurationSetEventDestination.EventDestination``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationseteventdestination.html#cfn-ses-configurationseteventdestination-eventdestination
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnConfigurationSetProps", jsii_struct_bases=[])
class CfnConfigurationSetProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::SES::ConfigurationSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html
    """
    name: str
    """``AWS::SES::ConfigurationSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-configurationset.html#cfn-ses-configurationset-name
    """

class CfnReceiptFilter(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter"):
    """A CloudFormation ``AWS::SES::ReceiptFilter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html
    cloudformationResource:
        AWS::SES::ReceiptFilter
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, filter: typing.Union[aws_cdk.cdk.Token, "FilterProperty"]) -> None:
        """Create a new ``AWS::SES::ReceiptFilter``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            filter: ``AWS::SES::ReceiptFilter.Filter``.
        """
        props: CfnReceiptFilterProps = {"filter": filter}

        jsii.create(CfnReceiptFilter, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnReceiptFilterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="receiptFilterName")
    def receipt_filter_name(self) -> str:
        return jsii.get(self, "receiptFilterName")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FilterProperty(jsii.compat.TypedDict, total=False):
        name: str
        """``CfnReceiptFilter.FilterProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html#cfn-ses-receiptfilter-filter-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter.FilterProperty", jsii_struct_bases=[_FilterProperty])
    class FilterProperty(_FilterProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html
        """
        ipFilter: typing.Union[aws_cdk.cdk.Token, "CfnReceiptFilter.IpFilterProperty"]
        """``CfnReceiptFilter.FilterProperty.IpFilter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-filter.html#cfn-ses-receiptfilter-filter-ipfilter
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptFilter.IpFilterProperty", jsii_struct_bases=[])
    class IpFilterProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html
        """
        cidr: str
        """``CfnReceiptFilter.IpFilterProperty.Cidr``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html#cfn-ses-receiptfilter-ipfilter-cidr
        """

        policy: str
        """``CfnReceiptFilter.IpFilterProperty.Policy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptfilter-ipfilter.html#cfn-ses-receiptfilter-ipfilter-policy
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptFilterProps", jsii_struct_bases=[])
class CfnReceiptFilterProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::SES::ReceiptFilter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html
    """
    filter: typing.Union[aws_cdk.cdk.Token, "CfnReceiptFilter.FilterProperty"]
    """``AWS::SES::ReceiptFilter.Filter``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptfilter.html#cfn-ses-receiptfilter-filter
    """

class CfnReceiptRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnReceiptRule"):
    """A CloudFormation ``AWS::SES::ReceiptRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html
    cloudformationResource:
        AWS::SES::ReceiptRule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule: typing.Union[aws_cdk.cdk.Token, "RuleProperty"], rule_set_name: str, after: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SES::ReceiptRule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            rule: ``AWS::SES::ReceiptRule.Rule``.
            ruleSetName: ``AWS::SES::ReceiptRule.RuleSetName``.
            after: ``AWS::SES::ReceiptRule.After``.
        """
        props: CfnReceiptRuleProps = {"rule": rule, "ruleSetName": rule_set_name}

        if after is not None:
            props["after"] = after

        jsii.create(CfnReceiptRule, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnReceiptRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> str:
        return jsii.get(self, "receiptRuleName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.ActionProperty", jsii_struct_bases=[])
    class ActionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html
        """
        addHeaderAction: typing.Union["CfnReceiptRule.AddHeaderActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.AddHeaderAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-addheaderaction
        """

        bounceAction: typing.Union["CfnReceiptRule.BounceActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.BounceAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-bounceaction
        """

        lambdaAction: typing.Union["CfnReceiptRule.LambdaActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.LambdaAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-lambdaaction
        """

        s3Action: typing.Union["CfnReceiptRule.S3ActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.S3Action``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-s3action
        """

        snsAction: typing.Union["CfnReceiptRule.SNSActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.SNSAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-snsaction
        """

        stopAction: typing.Union["CfnReceiptRule.StopActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.StopAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-stopaction
        """

        workmailAction: typing.Union["CfnReceiptRule.WorkmailActionProperty", aws_cdk.cdk.Token]
        """``CfnReceiptRule.ActionProperty.WorkmailAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-action.html#cfn-ses-receiptrule-action-workmailaction
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.AddHeaderActionProperty", jsii_struct_bases=[])
    class AddHeaderActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html
        """
        headerName: str
        """``CfnReceiptRule.AddHeaderActionProperty.HeaderName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headername
        """

        headerValue: str
        """``CfnReceiptRule.AddHeaderActionProperty.HeaderValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-addheaderaction.html#cfn-ses-receiptrule-addheaderaction-headervalue
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _BounceActionProperty(jsii.compat.TypedDict, total=False):
        statusCode: str
        """``CfnReceiptRule.BounceActionProperty.StatusCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-statuscode
        """
        topicArn: str
        """``CfnReceiptRule.BounceActionProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-topicarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.BounceActionProperty", jsii_struct_bases=[_BounceActionProperty])
    class BounceActionProperty(_BounceActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html
        """
        message: str
        """``CfnReceiptRule.BounceActionProperty.Message``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-message
        """

        sender: str
        """``CfnReceiptRule.BounceActionProperty.Sender``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-sender
        """

        smtpReplyCode: str
        """``CfnReceiptRule.BounceActionProperty.SmtpReplyCode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-bounceaction.html#cfn-ses-receiptrule-bounceaction-smtpreplycode
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LambdaActionProperty(jsii.compat.TypedDict, total=False):
        invocationType: str
        """``CfnReceiptRule.LambdaActionProperty.InvocationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-invocationtype
        """
        topicArn: str
        """``CfnReceiptRule.LambdaActionProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-topicarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.LambdaActionProperty", jsii_struct_bases=[_LambdaActionProperty])
    class LambdaActionProperty(_LambdaActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html
        """
        functionArn: str
        """``CfnReceiptRule.LambdaActionProperty.FunctionArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-lambdaaction.html#cfn-ses-receiptrule-lambdaaction-functionarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.RuleProperty", jsii_struct_bases=[])
    class RuleProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html
        """
        actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnReceiptRule.ActionProperty"]]]
        """``CfnReceiptRule.RuleProperty.Actions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-actions
        """

        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnReceiptRule.RuleProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-enabled
        """

        name: str
        """``CfnReceiptRule.RuleProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-name
        """

        recipients: typing.List[str]
        """``CfnReceiptRule.RuleProperty.Recipients``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-recipients
        """

        scanEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnReceiptRule.RuleProperty.ScanEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-scanenabled
        """

        tlsPolicy: str
        """``CfnReceiptRule.RuleProperty.TlsPolicy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-rule.html#cfn-ses-receiptrule-rule-tlspolicy
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _S3ActionProperty(jsii.compat.TypedDict, total=False):
        kmsKeyArn: str
        """``CfnReceiptRule.S3ActionProperty.KmsKeyArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-kmskeyarn
        """
        objectKeyPrefix: str
        """``CfnReceiptRule.S3ActionProperty.ObjectKeyPrefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-objectkeyprefix
        """
        topicArn: str
        """``CfnReceiptRule.S3ActionProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-topicarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.S3ActionProperty", jsii_struct_bases=[_S3ActionProperty])
    class S3ActionProperty(_S3ActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html
        """
        bucketName: str
        """``CfnReceiptRule.S3ActionProperty.BucketName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-s3action.html#cfn-ses-receiptrule-s3action-bucketname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.SNSActionProperty", jsii_struct_bases=[])
    class SNSActionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html
        """
        encoding: str
        """``CfnReceiptRule.SNSActionProperty.Encoding``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-encoding
        """

        topicArn: str
        """``CfnReceiptRule.SNSActionProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-snsaction.html#cfn-ses-receiptrule-snsaction-topicarn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StopActionProperty(jsii.compat.TypedDict, total=False):
        topicArn: str
        """``CfnReceiptRule.StopActionProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-topicarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.StopActionProperty", jsii_struct_bases=[_StopActionProperty])
    class StopActionProperty(_StopActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html
        """
        scope: str
        """``CfnReceiptRule.StopActionProperty.Scope``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-stopaction.html#cfn-ses-receiptrule-stopaction-scope
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _WorkmailActionProperty(jsii.compat.TypedDict, total=False):
        topicArn: str
        """``CfnReceiptRule.WorkmailActionProperty.TopicArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-topicarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRule.WorkmailActionProperty", jsii_struct_bases=[_WorkmailActionProperty])
    class WorkmailActionProperty(_WorkmailActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html
        """
        organizationArn: str
        """``CfnReceiptRule.WorkmailActionProperty.OrganizationArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-receiptrule-workmailaction.html#cfn-ses-receiptrule-workmailaction-organizationarn
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnReceiptRuleProps(jsii.compat.TypedDict, total=False):
    after: str
    """``AWS::SES::ReceiptRule.After``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-after
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleProps", jsii_struct_bases=[_CfnReceiptRuleProps])
class CfnReceiptRuleProps(_CfnReceiptRuleProps):
    """Properties for defining a ``AWS::SES::ReceiptRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html
    """
    rule: typing.Union[aws_cdk.cdk.Token, "CfnReceiptRule.RuleProperty"]
    """``AWS::SES::ReceiptRule.Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rule
    """

    ruleSetName: str
    """``AWS::SES::ReceiptRule.RuleSetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptrule.html#cfn-ses-receiptrule-rulesetname
    """

class CfnReceiptRuleSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleSet"):
    """A CloudFormation ``AWS::SES::ReceiptRuleSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html
    cloudformationResource:
        AWS::SES::ReceiptRuleSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule_set_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SES::ReceiptRuleSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            ruleSetName: ``AWS::SES::ReceiptRuleSet.RuleSetName``.
        """
        props: CfnReceiptRuleSetProps = {}

        if rule_set_name is not None:
            props["ruleSetName"] = rule_set_name

        jsii.create(CfnReceiptRuleSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnReceiptRuleSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> str:
        return jsii.get(self, "receiptRuleSetName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnReceiptRuleSetProps", jsii_struct_bases=[])
class CfnReceiptRuleSetProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::SES::ReceiptRuleSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html
    """
    ruleSetName: str
    """``AWS::SES::ReceiptRuleSet.RuleSetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-receiptruleset.html#cfn-ses-receiptruleset-rulesetname
    """

class CfnTemplate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.CfnTemplate"):
    """A CloudFormation ``AWS::SES::Template``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html
    cloudformationResource:
        AWS::SES::Template
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, template: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["TemplateProperty"]]]=None) -> None:
        """Create a new ``AWS::SES::Template``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            template: ``AWS::SES::Template.Template``.
        """
        props: CfnTemplateProps = {}

        if template is not None:
            props["template"] = template

        jsii.create(CfnTemplate, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTemplateProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="templateId")
    def template_id(self) -> str:
        return jsii.get(self, "templateId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnTemplate.TemplateProperty", jsii_struct_bases=[])
    class TemplateProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html
        """
        htmlPart: str
        """``CfnTemplate.TemplateProperty.HtmlPart``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-htmlpart
        """

        subjectPart: str
        """``CfnTemplate.TemplateProperty.SubjectPart``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-subjectpart
        """

        templateName: str
        """``CfnTemplate.TemplateProperty.TemplateName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-templatename
        """

        textPart: str
        """``CfnTemplate.TemplateProperty.TextPart``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-ses-template-template.html#cfn-ses-template-template-textpart
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.CfnTemplateProps", jsii_struct_bases=[])
class CfnTemplateProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::SES::Template``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html
    """
    template: typing.Union[aws_cdk.cdk.Token, "CfnTemplate.TemplateProperty"]
    """``AWS::SES::Template.Template``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-ses-template.html#cfn-ses-template-template
    """

class DropSpamReceiptRule(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.DropSpamReceiptRule"):
    """A rule added at the top of the rule set to drop spam/virus.

    See:
        https://docs.aws.amazon.com/ses/latest/DeveloperGuide/receiving-email-action-lambda-example-functions.html
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule_set: "IReceiptRuleSet", actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            ruleSet: The name of the rule set that the receipt rule will be added to.
            actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
            after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
            enabled: Whether the rule is active. Default: true
            name: The name for the rule. Default: - A CloudFormation generated name.
            recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
            scanEnabled: Whether to scan for spam and viruses. Default: false
            tlsPolicy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        """
        props: DropSpamReceiptRuleProps = {"ruleSet": rule_set}

        if actions is not None:
            props["actions"] = actions

        if after is not None:
            props["after"] = after

        if enabled is not None:
            props["enabled"] = enabled

        if name is not None:
            props["name"] = name

        if recipients is not None:
            props["recipients"] = recipients

        if scan_enabled is not None:
            props["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            props["tlsPolicy"] = tls_policy

        jsii.create(DropSpamReceiptRule, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="rule")
    def rule(self) -> "ReceiptRule":
        return jsii.get(self, "rule")


@jsii.enum(jsii_type="@aws-cdk/aws-ses.EmailEncoding")
class EmailEncoding(enum.Enum):
    """The type of email encoding to use for a SNS action."""
    Base64 = "Base64"
    """Base 64."""
    UTF8 = "UTF8"
    """UTF-8."""

@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRule")
class IReceiptRule(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """A receipt rule."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IReceiptRuleProxy

    @property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> str:
        """The name of the receipt rule.

        attribute:
            true
        """
        ...


class _IReceiptRuleProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """A receipt rule."""
    __jsii_type__ = "@aws-cdk/aws-ses.IReceiptRule"
    @property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> str:
        """The name of the receipt rule.

        attribute:
            true
        """
        return jsii.get(self, "receiptRuleName")


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRuleAction")
class IReceiptRuleAction(jsii.compat.Protocol):
    """An abstract action for a receipt rule."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IReceiptRuleActionProxy

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        ...


class _IReceiptRuleActionProxy():
    """An abstract action for a receipt rule."""
    __jsii_type__ = "@aws-cdk/aws-ses.IReceiptRuleAction"
    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])


@jsii.interface(jsii_type="@aws-cdk/aws-ses.IReceiptRuleSet")
class IReceiptRuleSet(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """A receipt rule set."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IReceiptRuleSetProxy

    @property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> str:
        """The receipt rule set name.

        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="addRule")
    def add_rule(self, id: str, *, actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> "ReceiptRule":
        """Adds a new receipt rule in this rule set.

        The new rule is added after
        the last added rule unless ``after`` is specified.

        Arguments:
            id: -
            options: -
            actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
            after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
            enabled: Whether the rule is active. Default: true
            name: The name for the rule. Default: - A CloudFormation generated name.
            recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
            scanEnabled: Whether to scan for spam and viruses. Default: false
            tlsPolicy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        """
        ...


class _IReceiptRuleSetProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """A receipt rule set."""
    __jsii_type__ = "@aws-cdk/aws-ses.IReceiptRuleSet"
    @property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> str:
        """The receipt rule set name.

        attribute:
            true
        """
        return jsii.get(self, "receiptRuleSetName")

    @jsii.member(jsii_name="addRule")
    def add_rule(self, id: str, *, actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> "ReceiptRule":
        """Adds a new receipt rule in this rule set.

        The new rule is added after
        the last added rule unless ``after`` is specified.

        Arguments:
            id: -
            options: -
            actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
            after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
            enabled: Whether the rule is active. Default: true
            name: The name for the rule. Default: - A CloudFormation generated name.
            recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
            scanEnabled: Whether to scan for spam and viruses. Default: false
            tlsPolicy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        """
        options: ReceiptRuleOptions = {}

        if actions is not None:
            options["actions"] = actions

        if after is not None:
            options["after"] = after

        if enabled is not None:
            options["enabled"] = enabled

        if name is not None:
            options["name"] = name

        if recipients is not None:
            options["recipients"] = recipients

        if scan_enabled is not None:
            options["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            options["tlsPolicy"] = tls_policy

        return jsii.invoke(self, "addRule", [id, options])


@jsii.enum(jsii_type="@aws-cdk/aws-ses.LambdaInvocationType")
class LambdaInvocationType(enum.Enum):
    """The type of invocation to use for a Lambda Action."""
    Event = "Event"
    """The function will be invoked asynchronously."""
    RequestResponse = "RequestResponse"
    """The function will be invoked sychronously.

    Use RequestResponse only when
    you want to make a mail flow decision, such as whether to stop the receipt
    rule or the receipt rule set.
    """

class ReceiptFilter(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptFilter"):
    """A receipt filter.

    When instantiated without props, it creates a
    block all receipt filter.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ip: typing.Optional[str]=None, name: typing.Optional[str]=None, policy: typing.Optional["ReceiptFilterPolicy"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            ip: The ip address or range to filter. Default: 0.0.0.0/0
            name: The name for the receipt filter. Default: a CloudFormation generated name
            policy: The policy for the filter. Default: Block
        """
        props: ReceiptFilterProps = {}

        if ip is not None:
            props["ip"] = ip

        if name is not None:
            props["name"] = name

        if policy is not None:
            props["policy"] = policy

        jsii.create(ReceiptFilter, self, [scope, id, props])


@jsii.enum(jsii_type="@aws-cdk/aws-ses.ReceiptFilterPolicy")
class ReceiptFilterPolicy(enum.Enum):
    """The policy for the receipt filter."""
    Allow = "Allow"
    """Allow the ip address or range."""
    Block = "Block"
    """Block the ip address or range."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptFilterProps", jsii_struct_bases=[])
class ReceiptFilterProps(jsii.compat.TypedDict, total=False):
    """Construction properties for a ReceiptFilter."""
    ip: str
    """The ip address or range to filter.

    Default:
        0.0.0.0/0
    """

    name: str
    """The name for the receipt filter.

    Default:
        a CloudFormation generated name
    """

    policy: "ReceiptFilterPolicy"
    """The policy for the filter.

    Default:
        Block
    """

@jsii.implements(IReceiptRule)
class ReceiptRule(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRule"):
    """A new receipt rule."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, rule_set: "IReceiptRuleSet", actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            ruleSet: The name of the rule set that the receipt rule will be added to.
            actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
            after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
            enabled: Whether the rule is active. Default: true
            name: The name for the rule. Default: - A CloudFormation generated name.
            recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
            scanEnabled: Whether to scan for spam and viruses. Default: false
            tlsPolicy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        """
        props: ReceiptRuleProps = {"ruleSet": rule_set}

        if actions is not None:
            props["actions"] = actions

        if after is not None:
            props["after"] = after

        if enabled is not None:
            props["enabled"] = enabled

        if name is not None:
            props["name"] = name

        if recipients is not None:
            props["recipients"] = recipients

        if scan_enabled is not None:
            props["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            props["tlsPolicy"] = tls_policy

        jsii.create(ReceiptRule, self, [scope, id, props])

    @jsii.member(jsii_name="fromReceiptRuleName")
    @classmethod
    def from_receipt_rule_name(cls, scope: aws_cdk.cdk.Construct, id: str, receipt_rule_name: str) -> "IReceiptRule":
        """
        Arguments:
            scope: -
            id: -
            receiptRuleName: -
        """
        return jsii.sinvoke(cls, "fromReceiptRuleName", [scope, id, receipt_rule_name])

    @jsii.member(jsii_name="addAction")
    def add_action(self, action: "IReceiptRuleAction") -> None:
        """Adds an action to this receipt rule.

        Arguments:
            action: -
        """
        return jsii.invoke(self, "addAction", [action])

    @property
    @jsii.member(jsii_name="receiptRuleName")
    def receipt_rule_name(self) -> str:
        """The name of the receipt rule."""
        return jsii.get(self, "receiptRuleName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleActionProps", jsii_struct_bases=[])
class ReceiptRuleActionProps(jsii.compat.TypedDict, total=False):
    """Properties for a receipt rule action."""
    addHeaderAction: "CfnReceiptRule.AddHeaderActionProperty"
    """Adds a header to the received email."""

    bounceAction: "CfnReceiptRule.BounceActionProperty"
    """Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS."""

    lambdaAction: "CfnReceiptRule.LambdaActionProperty"
    """Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS."""

    s3Action: "CfnReceiptRule.S3ActionProperty"
    """Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS."""

    snsAction: "CfnReceiptRule.SNSActionProperty"
    """Publishes the email content within a notification to Amazon SNS."""

    stopAction: "CfnReceiptRule.StopActionProperty"
    """Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS."""

    workmailAction: "CfnReceiptRule.WorkmailActionProperty"
    """Calls Amazon WorkMail and, optionally, publishes a notification to Amazon SNS."""

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleAddHeaderAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleAddHeaderAction"):
    """Adds a header to the received email."""
    def __init__(self, *, name: str, value: str) -> None:
        """
        Arguments:
            props: -
            name: The name of the header to add. Must be between 1 and 50 characters, inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters and dashes only.
            value: The value of the header to add. Must be less than 2048 characters, and must not contain newline characters ("\r" or "\n").
        """
        props: ReceiptRuleAddHeaderActionProps = {"name": name, "value": value}

        jsii.create(ReceiptRuleAddHeaderAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleAddHeaderActionProps", jsii_struct_bases=[])
class ReceiptRuleAddHeaderActionProps(jsii.compat.TypedDict):
    """Construction properties for a ReceiptRuleAddHeaderAction."""
    name: str
    """The name of the header to add.

    Must be between 1 and 50 characters,
    inclusive, and consist of alphanumeric (a-z, A-Z, 0-9) characters
    and dashes only.
    """

    value: str
    """The value of the header to add.

    Must be less than 2048 characters,
    and must not contain newline characters ("\r" or "\n").
    """

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleBounceAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceAction"):
    """Rejects the received email by returning a bounce response to the sender and, optionally, publishes a notification to Amazon SNS."""
    def __init__(self, *, sender: str, template: "ReceiptRuleBounceActionTemplate", topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        """
        Arguments:
            props: -
            sender: The email address of the sender of the bounced email. This is the address from which the bounce message will be sent.
            template: The template containing the message, reply code and status code.
            topic: The SNS topic to notify when the bounce action is taken. Default: no notification
        """
        props: ReceiptRuleBounceActionProps = {"sender": sender, "template": template}

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleBounceAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleBounceActionProps":
        return jsii.get(self, "props")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ReceiptRuleBounceActionProps(jsii.compat.TypedDict, total=False):
    topic: aws_cdk.aws_sns.ITopic
    """The SNS topic to notify when the bounce action is taken.

    Default:
        no notification
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceActionProps", jsii_struct_bases=[_ReceiptRuleBounceActionProps])
class ReceiptRuleBounceActionProps(_ReceiptRuleBounceActionProps):
    """Construction properties for a ReceiptRuleBounceAction."""
    sender: str
    """The email address of the sender of the bounced email.

    This is the address
    from which the bounce message will be sent.
    """

    template: "ReceiptRuleBounceActionTemplate"
    """The template containing the message, reply code and status code."""

class ReceiptRuleBounceActionTemplate(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceActionTemplate"):
    """A bounce action template."""
    def __init__(self, *, message: str, smtp_reply_code: str, status_code: typing.Optional[str]=None) -> None:
        """
        Arguments:
            props: -
            message: Human-readable text to include in the bounce message.
            smtpReplyCode: The SMTP reply code, as defined by RFC 5321.
            statusCode: The SMTP enhanced status code, as defined by RFC 3463.
        """
        props: ReceiptRuleBounceActionTemplateProps = {"message": message, "smtpReplyCode": smtp_reply_code}

        if status_code is not None:
            props["statusCode"] = status_code

        jsii.create(ReceiptRuleBounceActionTemplate, self, [props])

    @classproperty
    @jsii.member(jsii_name="MailboxDoesNotExist")
    def MAILBOX_DOES_NOT_EXIST(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MailboxDoesNotExist")

    @classproperty
    @jsii.member(jsii_name="MailboxFull")
    def MAILBOX_FULL(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MailboxFull")

    @classproperty
    @jsii.member(jsii_name="MessageContentRejected")
    def MESSAGE_CONTENT_REJECTED(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MessageContentRejected")

    @classproperty
    @jsii.member(jsii_name="MessageTooLarge")
    def MESSAGE_TOO_LARGE(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "MessageTooLarge")

    @classproperty
    @jsii.member(jsii_name="TemporaryFailure")
    def TEMPORARY_FAILURE(cls) -> "ReceiptRuleBounceActionTemplate":
        return jsii.sget(cls, "TemporaryFailure")

    @property
    @jsii.member(jsii_name="message")
    def message(self) -> str:
        return jsii.get(self, "message")

    @property
    @jsii.member(jsii_name="smtpReplyCode")
    def smtp_reply_code(self) -> str:
        return jsii.get(self, "smtpReplyCode")

    @property
    @jsii.member(jsii_name="statusCode")
    def status_code(self) -> typing.Optional[str]:
        return jsii.get(self, "statusCode")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ReceiptRuleBounceActionTemplateProps(jsii.compat.TypedDict, total=False):
    statusCode: str
    """The SMTP enhanced status code, as defined by RFC 3463.

    See:
        https://tools.ietf.org/html/rfc3463
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleBounceActionTemplateProps", jsii_struct_bases=[_ReceiptRuleBounceActionTemplateProps])
class ReceiptRuleBounceActionTemplateProps(_ReceiptRuleBounceActionTemplateProps):
    """Construction properties for a ReceiptRuleBounceActionTemplate."""
    message: str
    """Human-readable text to include in the bounce message."""

    smtpReplyCode: str
    """The SMTP reply code, as defined by RFC 5321.

    See:
        https://tools.ietf.org/html/rfc5321
    """

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleLambdaAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleLambdaAction"):
    """Calls an AWS Lambda function, and optionally, publishes a notification to Amazon SNS."""
    def __init__(self, *, function: aws_cdk.aws_lambda.IFunction, invocation_type: typing.Optional["LambdaInvocationType"]=None, topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        """
        Arguments:
            props: -
            function: The Lambda function to invoke.
            invocationType: The invocation type of the Lambda function. Default: Event
            topic: The SNS topic to notify when the Lambda action is taken. Default: no notification
        """
        props: ReceiptRuleLambdaActionProps = {"function": function}

        if invocation_type is not None:
            props["invocationType"] = invocation_type

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleLambdaAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleLambdaActionProps":
        return jsii.get(self, "props")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ReceiptRuleLambdaActionProps(jsii.compat.TypedDict, total=False):
    invocationType: "LambdaInvocationType"
    """The invocation type of the Lambda function.

    Default:
        Event
    """
    topic: aws_cdk.aws_sns.ITopic
    """The SNS topic to notify when the Lambda action is taken.

    Default:
        no notification
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleLambdaActionProps", jsii_struct_bases=[_ReceiptRuleLambdaActionProps])
class ReceiptRuleLambdaActionProps(_ReceiptRuleLambdaActionProps):
    """Construction properties for a ReceiptRuleLambdaAction."""
    function: aws_cdk.aws_lambda.IFunction
    """The Lambda function to invoke."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleOptions", jsii_struct_bases=[])
class ReceiptRuleOptions(jsii.compat.TypedDict, total=False):
    """Options to add a receipt rule to a receipt rule set."""
    actions: typing.List["IReceiptRuleAction"]
    """An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule.

    Default:
        - No actions.
    """

    after: "IReceiptRule"
    """An existing rule after which the new rule will be placed.

    Default:
        - The new rule is inserted at the beginning of the rule list.
    """

    enabled: bool
    """Whether the rule is active.

    Default:
        true
    """

    name: str
    """The name for the rule.

    Default:
        - A CloudFormation generated name.
    """

    recipients: typing.List[str]
    """The recipient domains and email addresses that the receipt rule applies to.

    Default:
        - Match all recipients under all verified domains.
    """

    scanEnabled: bool
    """Whether to scan for spam and viruses.

    Default:
        false
    """

    tlsPolicy: "TlsPolicy"
    """Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS).

    Default:
        - Optional which will not check for TLS.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleProps", jsii_struct_bases=[ReceiptRuleOptions])
class ReceiptRuleProps(ReceiptRuleOptions, jsii.compat.TypedDict):
    """Construction properties for a ReceiptRule."""
    ruleSet: "IReceiptRuleSet"
    """The name of the rule set that the receipt rule will be added to."""

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.DropSpamReceiptRuleProps", jsii_struct_bases=[ReceiptRuleProps])
class DropSpamReceiptRuleProps(ReceiptRuleProps, jsii.compat.TypedDict):
    pass

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleS3Action(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleS3Action"):
    """Saves the received message to an Amazon S3 bucket and, optionally, publishes a notification to Amazon SNS."""
    def __init__(self, *, bucket: aws_cdk.aws_s3.IBucket, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, object_key_prefix: typing.Optional[str]=None, topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        """
        Arguments:
            props: -
            bucket: The S3 bucket that incoming email will be saved to.
            kmsKey: The master key that SES should use to encrypt your emails before saving them to the S3 bucket. Default: no encryption
            objectKeyPrefix: The key prefix of the S3 bucket. Default: no prefix
            topic: The SNS topic to notify when the S3 action is taken. Default: no notification
        """
        props: ReceiptRuleS3ActionProps = {"bucket": bucket}

        if kms_key is not None:
            props["kmsKey"] = kms_key

        if object_key_prefix is not None:
            props["objectKeyPrefix"] = object_key_prefix

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleS3Action, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleS3ActionProps":
        return jsii.get(self, "props")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ReceiptRuleS3ActionProps(jsii.compat.TypedDict, total=False):
    kmsKey: aws_cdk.aws_kms.IKey
    """The master key that SES should use to encrypt your emails before saving them to the S3 bucket.

    Default:
        no encryption
    """
    objectKeyPrefix: str
    """The key prefix of the S3 bucket.

    Default:
        no prefix
    """
    topic: aws_cdk.aws_sns.ITopic
    """The SNS topic to notify when the S3 action is taken.

    Default:
        no notification
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleS3ActionProps", jsii_struct_bases=[_ReceiptRuleS3ActionProps])
class ReceiptRuleS3ActionProps(_ReceiptRuleS3ActionProps):
    """Construction properties for a ReceiptRuleS3Action."""
    bucket: aws_cdk.aws_s3.IBucket
    """The S3 bucket that incoming email will be saved to."""

@jsii.implements(IReceiptRuleSet)
class ReceiptRuleSet(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleSet"):
    """A new receipt rule set."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, drop_spam: typing.Optional[bool]=None, name: typing.Optional[str]=None, rules: typing.Optional[typing.List["ReceiptRuleOptions"]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            dropSpam: Whether to add a first rule to stop processing messages that have at least one spam indicator. Default: false
            name: The name for the receipt rule set. Default: - A CloudFormation generated name.
            rules: The list of rules to add to this rule set. Rules are added in the same order as they appear in the list. Default: - No rules are added to the rule set.
        """
        props: ReceiptRuleSetProps = {}

        if drop_spam is not None:
            props["dropSpam"] = drop_spam

        if name is not None:
            props["name"] = name

        if rules is not None:
            props["rules"] = rules

        jsii.create(ReceiptRuleSet, self, [scope, id, props])

    @jsii.member(jsii_name="fromReceiptRuleSetName")
    @classmethod
    def from_receipt_rule_set_name(cls, scope: aws_cdk.cdk.Construct, id: str, receipt_rule_set_name: str) -> "IReceiptRuleSet":
        """Import an exported receipt rule set.

        Arguments:
            scope: -
            id: -
            receiptRuleSetName: -
        """
        return jsii.sinvoke(cls, "fromReceiptRuleSetName", [scope, id, receipt_rule_set_name])

    @jsii.member(jsii_name="addDropSpamRule")
    def _add_drop_spam_rule(self) -> None:
        """Adds a drop spam rule."""
        return jsii.invoke(self, "addDropSpamRule", [])

    @jsii.member(jsii_name="addRule")
    def add_rule(self, id: str, *, actions: typing.Optional[typing.List["IReceiptRuleAction"]]=None, after: typing.Optional["IReceiptRule"]=None, enabled: typing.Optional[bool]=None, name: typing.Optional[str]=None, recipients: typing.Optional[typing.List[str]]=None, scan_enabled: typing.Optional[bool]=None, tls_policy: typing.Optional["TlsPolicy"]=None) -> "ReceiptRule":
        """Adds a new receipt rule in this rule set.

        The new rule is added after
        the last added rule unless ``after`` is specified.

        Arguments:
            id: -
            options: -
            actions: An ordered list of actions to perform on messages that match at least one of the recipient email addresses or domains specified in the receipt rule. Default: - No actions.
            after: An existing rule after which the new rule will be placed. Default: - The new rule is inserted at the beginning of the rule list.
            enabled: Whether the rule is active. Default: true
            name: The name for the rule. Default: - A CloudFormation generated name.
            recipients: The recipient domains and email addresses that the receipt rule applies to. Default: - Match all recipients under all verified domains.
            scanEnabled: Whether to scan for spam and viruses. Default: false
            tlsPolicy: Whether Amazon SES should require that incoming email is delivered over a connection encrypted with Transport Layer Security (TLS). Default: - Optional which will not check for TLS.
        """
        options: ReceiptRuleOptions = {}

        if actions is not None:
            options["actions"] = actions

        if after is not None:
            options["after"] = after

        if enabled is not None:
            options["enabled"] = enabled

        if name is not None:
            options["name"] = name

        if recipients is not None:
            options["recipients"] = recipients

        if scan_enabled is not None:
            options["scanEnabled"] = scan_enabled

        if tls_policy is not None:
            options["tlsPolicy"] = tls_policy

        return jsii.invoke(self, "addRule", [id, options])

    @property
    @jsii.member(jsii_name="receiptRuleSetName")
    def receipt_rule_set_name(self) -> str:
        """The receipt rule set name."""
        return jsii.get(self, "receiptRuleSetName")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleSetProps", jsii_struct_bases=[])
class ReceiptRuleSetProps(jsii.compat.TypedDict, total=False):
    """Construction properties for a ReceiptRuleSet."""
    dropSpam: bool
    """Whether to add a first rule to stop processing messages that have at least one spam indicator.

    Default:
        false
    """

    name: str
    """The name for the receipt rule set.

    Default:
        - A CloudFormation generated name.
    """

    rules: typing.List["ReceiptRuleOptions"]
    """The list of rules to add to this rule set.

    Rules are added in the same
    order as they appear in the list.

    Default:
        - No rules are added to the rule set.
    """

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleSnsAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleSnsAction"):
    """Publishes the email content within a notification to Amazon SNS."""
    def __init__(self, *, topic: aws_cdk.aws_sns.ITopic, encoding: typing.Optional["EmailEncoding"]=None) -> None:
        """
        Arguments:
            props: -
            topic: The SNS topic to notify.
            encoding: The encoding to use for the email within the Amazon SNS notification. Default: UTF-8
        """
        props: ReceiptRuleSnsActionProps = {"topic": topic}

        if encoding is not None:
            props["encoding"] = encoding

        jsii.create(ReceiptRuleSnsAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> "ReceiptRuleSnsActionProps":
        return jsii.get(self, "props")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ReceiptRuleSnsActionProps(jsii.compat.TypedDict, total=False):
    encoding: "EmailEncoding"
    """The encoding to use for the email within the Amazon SNS notification.

    Default:
        UTF-8
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleSnsActionProps", jsii_struct_bases=[_ReceiptRuleSnsActionProps])
class ReceiptRuleSnsActionProps(_ReceiptRuleSnsActionProps):
    """Construction properties for a ReceiptRuleSnsAction."""
    topic: aws_cdk.aws_sns.ITopic
    """The SNS topic to notify."""

@jsii.implements(IReceiptRuleAction)
class ReceiptRuleStopAction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.ReceiptRuleStopAction"):
    """Terminates the evaluation of the receipt rule set and optionally publishes a notification to Amazon SNS."""
    def __init__(self, *, topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None) -> None:
        """
        Arguments:
            props: -
            topic: The SNS topic to notify when the stop action is taken.
        """
        props: ReceiptRuleStopActionProps = {}

        if topic is not None:
            props["topic"] = topic

        jsii.create(ReceiptRuleStopAction, self, [props])

    @jsii.member(jsii_name="render")
    def render(self) -> "ReceiptRuleActionProps":
        """Renders the action specification."""
        return jsii.invoke(self, "render", [])

    @property
    @jsii.member(jsii_name="props")
    def props(self) -> typing.Optional["ReceiptRuleStopActionProps"]:
        return jsii.get(self, "props")


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.ReceiptRuleStopActionProps", jsii_struct_bases=[])
class ReceiptRuleStopActionProps(jsii.compat.TypedDict, total=False):
    """Construction properties for a ReceiptRuleStopAction."""
    topic: aws_cdk.aws_sns.ITopic
    """The SNS topic to notify when the stop action is taken."""

@jsii.enum(jsii_type="@aws-cdk/aws-ses.TlsPolicy")
class TlsPolicy(enum.Enum):
    """The type of TLS policy for a receipt rule."""
    Optional = "Optional"
    """Do not check for TLS."""
    Require = "Require"
    """Bounce emails that are not received over TLS."""

class WhiteListReceiptFilter(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ses.WhiteListReceiptFilter"):
    """A white list receipt filter."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, ips: typing.List[str]) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            ips: A list of ip addresses or ranges to white list.
        """
        props: WhiteListReceiptFilterProps = {"ips": ips}

        jsii.create(WhiteListReceiptFilter, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-ses.WhiteListReceiptFilterProps", jsii_struct_bases=[])
class WhiteListReceiptFilterProps(jsii.compat.TypedDict):
    """Construction properties for a WhiteListReceiptFilter."""
    ips: typing.List[str]
    """A list of ip addresses or ranges to white list."""

__all__ = ["CfnConfigurationSet", "CfnConfigurationSetEventDestination", "CfnConfigurationSetEventDestinationProps", "CfnConfigurationSetProps", "CfnReceiptFilter", "CfnReceiptFilterProps", "CfnReceiptRule", "CfnReceiptRuleProps", "CfnReceiptRuleSet", "CfnReceiptRuleSetProps", "CfnTemplate", "CfnTemplateProps", "DropSpamReceiptRule", "DropSpamReceiptRuleProps", "EmailEncoding", "IReceiptRule", "IReceiptRuleAction", "IReceiptRuleSet", "LambdaInvocationType", "ReceiptFilter", "ReceiptFilterPolicy", "ReceiptFilterProps", "ReceiptRule", "ReceiptRuleActionProps", "ReceiptRuleAddHeaderAction", "ReceiptRuleAddHeaderActionProps", "ReceiptRuleBounceAction", "ReceiptRuleBounceActionProps", "ReceiptRuleBounceActionTemplate", "ReceiptRuleBounceActionTemplateProps", "ReceiptRuleLambdaAction", "ReceiptRuleLambdaActionProps", "ReceiptRuleOptions", "ReceiptRuleProps", "ReceiptRuleS3Action", "ReceiptRuleS3ActionProps", "ReceiptRuleSet", "ReceiptRuleSetProps", "ReceiptRuleSnsAction", "ReceiptRuleSnsActionProps", "ReceiptRuleStopAction", "ReceiptRuleStopActionProps", "TlsPolicy", "WhiteListReceiptFilter", "WhiteListReceiptFilterProps", "__jsii_assembly__"]

publication.publish()
