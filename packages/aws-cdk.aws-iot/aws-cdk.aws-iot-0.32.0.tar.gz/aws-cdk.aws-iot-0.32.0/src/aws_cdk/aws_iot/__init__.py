import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iot", "0.32.0", __name__, "aws-iot@0.32.0.jsii.tgz")
class CfnCertificate(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnCertificate"):
    """A CloudFormation ``AWS::IoT::Certificate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html
    cloudformationResource:
        AWS::IoT::Certificate
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, certificate_signing_request: str, status: str) -> None:
        """Create a new ``AWS::IoT::Certificate``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            certificateSigningRequest: ``AWS::IoT::Certificate.CertificateSigningRequest``.
            status: ``AWS::IoT::Certificate.Status``.
        """
        props: CfnCertificateProps = {"certificateSigningRequest": certificate_signing_request, "status": status}

        jsii.create(CfnCertificate, self, [scope, id, props])

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
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "certificateArn")

    @property
    @jsii.member(jsii_name="certificateId")
    def certificate_id(self) -> str:
        return jsii.get(self, "certificateId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnCertificateProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnCertificateProps", jsii_struct_bases=[])
class CfnCertificateProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::IoT::Certificate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html
    """
    certificateSigningRequest: str
    """``AWS::IoT::Certificate.CertificateSigningRequest``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html#cfn-iot-certificate-certificatesigningrequest
    """

    status: str
    """``AWS::IoT::Certificate.Status``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-certificate.html#cfn-iot-certificate-status
    """

class CfnPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnPolicy"):
    """A CloudFormation ``AWS::IoT::Policy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html
    cloudformationResource:
        AWS::IoT::Policy
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], policy_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::Policy``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            policyDocument: ``AWS::IoT::Policy.PolicyDocument``.
            policyName: ``AWS::IoT::Policy.PolicyName``.
        """
        props: CfnPolicyProps = {"policyDocument": policy_document}

        if policy_name is not None:
            props["policyName"] = policy_name

        jsii.create(CfnPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="policyArn")
    def policy_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "policyArn")

    @property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> str:
        return jsii.get(self, "policyName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPolicyProps":
        return jsii.get(self, "propertyOverrides")


class CfnPolicyPrincipalAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnPolicyPrincipalAttachment"):
    """A CloudFormation ``AWS::IoT::PolicyPrincipalAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html
    cloudformationResource:
        AWS::IoT::PolicyPrincipalAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_name: str, principal: str) -> None:
        """Create a new ``AWS::IoT::PolicyPrincipalAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            policyName: ``AWS::IoT::PolicyPrincipalAttachment.PolicyName``.
            principal: ``AWS::IoT::PolicyPrincipalAttachment.Principal``.
        """
        props: CfnPolicyPrincipalAttachmentProps = {"policyName": policy_name, "principal": principal}

        jsii.create(CfnPolicyPrincipalAttachment, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnPolicyPrincipalAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnPolicyPrincipalAttachmentProps", jsii_struct_bases=[])
class CfnPolicyPrincipalAttachmentProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::IoT::PolicyPrincipalAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html
    """
    policyName: str
    """``AWS::IoT::PolicyPrincipalAttachment.PolicyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html#cfn-iot-policyprincipalattachment-policyname
    """

    principal: str
    """``AWS::IoT::PolicyPrincipalAttachment.Principal``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policyprincipalattachment.html#cfn-iot-policyprincipalattachment-principal
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPolicyProps(jsii.compat.TypedDict, total=False):
    policyName: str
    """``AWS::IoT::Policy.PolicyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html#cfn-iot-policy-policyname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnPolicyProps", jsii_struct_bases=[_CfnPolicyProps])
class CfnPolicyProps(_CfnPolicyProps):
    """Properties for defining a ``AWS::IoT::Policy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html
    """
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::IoT::Policy.PolicyDocument``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-policy.html#cfn-iot-policy-policydocument
    """

class CfnThing(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnThing"):
    """A CloudFormation ``AWS::IoT::Thing``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html
    cloudformationResource:
        AWS::IoT::Thing
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, attribute_payload: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["AttributePayloadProperty"]]]=None, thing_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::Thing``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            attributePayload: ``AWS::IoT::Thing.AttributePayload``.
            thingName: ``AWS::IoT::Thing.ThingName``.
        """
        props: CfnThingProps = {}

        if attribute_payload is not None:
            props["attributePayload"] = attribute_payload

        if thing_name is not None:
            props["thingName"] = thing_name

        jsii.create(CfnThing, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnThingProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="thingName")
    def thing_name(self) -> str:
        return jsii.get(self, "thingName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThing.AttributePayloadProperty", jsii_struct_bases=[])
    class AttributePayloadProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-thing-attributepayload.html
        """
        attributes: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnThing.AttributePayloadProperty.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-thing-attributepayload.html#cfn-iot-thing-attributepayload-attributes
        """


class CfnThingPrincipalAttachment(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnThingPrincipalAttachment"):
    """A CloudFormation ``AWS::IoT::ThingPrincipalAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html
    cloudformationResource:
        AWS::IoT::ThingPrincipalAttachment
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, principal: str, thing_name: str) -> None:
        """Create a new ``AWS::IoT::ThingPrincipalAttachment``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            principal: ``AWS::IoT::ThingPrincipalAttachment.Principal``.
            thingName: ``AWS::IoT::ThingPrincipalAttachment.ThingName``.
        """
        props: CfnThingPrincipalAttachmentProps = {"principal": principal, "thingName": thing_name}

        jsii.create(CfnThingPrincipalAttachment, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnThingPrincipalAttachmentProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThingPrincipalAttachmentProps", jsii_struct_bases=[])
class CfnThingPrincipalAttachmentProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::IoT::ThingPrincipalAttachment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html
    """
    principal: str
    """``AWS::IoT::ThingPrincipalAttachment.Principal``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html#cfn-iot-thingprincipalattachment-principal
    """

    thingName: str
    """``AWS::IoT::ThingPrincipalAttachment.ThingName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thingprincipalattachment.html#cfn-iot-thingprincipalattachment-thingname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnThingProps", jsii_struct_bases=[])
class CfnThingProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::IoT::Thing``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html
    """
    attributePayload: typing.Union[aws_cdk.cdk.Token, "CfnThing.AttributePayloadProperty"]
    """``AWS::IoT::Thing.AttributePayload``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html#cfn-iot-thing-attributepayload
    """

    thingName: str
    """``AWS::IoT::Thing.ThingName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-thing.html#cfn-iot-thing-thingname
    """

class CfnTopicRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iot.CfnTopicRule"):
    """A CloudFormation ``AWS::IoT::TopicRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html
    cloudformationResource:
        AWS::IoT::TopicRule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, topic_rule_payload: typing.Union[aws_cdk.cdk.Token, "TopicRulePayloadProperty"], rule_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::IoT::TopicRule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            topicRulePayload: ``AWS::IoT::TopicRule.TopicRulePayload``.
            ruleName: ``AWS::IoT::TopicRule.RuleName``.
        """
        props: CfnTopicRuleProps = {"topicRulePayload": topic_rule_payload}

        if rule_name is not None:
            props["ruleName"] = rule_name

        jsii.create(CfnTopicRule, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTopicRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="topicRuleArn")
    def topic_rule_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "topicRuleArn")

    @property
    @jsii.member(jsii_name="topicRuleName")
    def topic_rule_name(self) -> str:
        return jsii.get(self, "topicRuleName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.ActionProperty", jsii_struct_bases=[])
    class ActionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html
        """
        cloudwatchAlarm: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.CloudwatchAlarmActionProperty"]
        """``CfnTopicRule.ActionProperty.CloudwatchAlarm``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-cloudwatchalarm
        """

        cloudwatchMetric: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.CloudwatchMetricActionProperty"]
        """``CfnTopicRule.ActionProperty.CloudwatchMetric``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-cloudwatchmetric
        """

        dynamoDb: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.DynamoDBActionProperty"]
        """``CfnTopicRule.ActionProperty.DynamoDB``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-dynamodb
        """

        dynamoDBv2: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.DynamoDBv2ActionProperty"]
        """``CfnTopicRule.ActionProperty.DynamoDBv2``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-dynamodbv2
        """

        elasticsearch: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.ElasticsearchActionProperty"]
        """``CfnTopicRule.ActionProperty.Elasticsearch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-elasticsearch
        """

        firehose: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.FirehoseActionProperty"]
        """``CfnTopicRule.ActionProperty.Firehose``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-firehose
        """

        iotAnalytics: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.IotAnalyticsActionProperty"]
        """``CfnTopicRule.ActionProperty.IotAnalytics``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-iotanalytics
        """

        kinesis: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.KinesisActionProperty"]
        """``CfnTopicRule.ActionProperty.Kinesis``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-kinesis
        """

        lambda_: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.LambdaActionProperty"]
        """``CfnTopicRule.ActionProperty.Lambda``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-lambda
        """

        republish: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.RepublishActionProperty"]
        """``CfnTopicRule.ActionProperty.Republish``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-republish
        """

        s3: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.S3ActionProperty"]
        """``CfnTopicRule.ActionProperty.S3``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-s3
        """

        sns: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.SnsActionProperty"]
        """``CfnTopicRule.ActionProperty.Sns``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-sns
        """

        sqs: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.SqsActionProperty"]
        """``CfnTopicRule.ActionProperty.Sqs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-sqs
        """

        stepFunctions: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.StepFunctionsActionProperty"]
        """``CfnTopicRule.ActionProperty.StepFunctions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-action.html#cfn-iot-topicrule-action-stepfunctions
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.CloudwatchAlarmActionProperty", jsii_struct_bases=[])
    class CloudwatchAlarmActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html
        """
        alarmName: str
        """``CfnTopicRule.CloudwatchAlarmActionProperty.AlarmName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-alarmname
        """

        roleArn: str
        """``CfnTopicRule.CloudwatchAlarmActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-rolearn
        """

        stateReason: str
        """``CfnTopicRule.CloudwatchAlarmActionProperty.StateReason``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-statereason
        """

        stateValue: str
        """``CfnTopicRule.CloudwatchAlarmActionProperty.StateValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchalarmaction.html#cfn-iot-topicrule-cloudwatchalarmaction-statevalue
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CloudwatchMetricActionProperty(jsii.compat.TypedDict, total=False):
        metricTimestamp: str
        """``CfnTopicRule.CloudwatchMetricActionProperty.MetricTimestamp``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metrictimestamp
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.CloudwatchMetricActionProperty", jsii_struct_bases=[_CloudwatchMetricActionProperty])
    class CloudwatchMetricActionProperty(_CloudwatchMetricActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html
        """
        metricName: str
        """``CfnTopicRule.CloudwatchMetricActionProperty.MetricName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricname
        """

        metricNamespace: str
        """``CfnTopicRule.CloudwatchMetricActionProperty.MetricNamespace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricnamespace
        """

        metricUnit: str
        """``CfnTopicRule.CloudwatchMetricActionProperty.MetricUnit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricunit
        """

        metricValue: str
        """``CfnTopicRule.CloudwatchMetricActionProperty.MetricValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-metricvalue
        """

        roleArn: str
        """``CfnTopicRule.CloudwatchMetricActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-cloudwatchmetricaction.html#cfn-iot-topicrule-cloudwatchmetricaction-rolearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _DynamoDBActionProperty(jsii.compat.TypedDict, total=False):
        hashKeyType: str
        """``CfnTopicRule.DynamoDBActionProperty.HashKeyType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-hashkeytype
        """
        payloadField: str
        """``CfnTopicRule.DynamoDBActionProperty.PayloadField``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-payloadfield
        """
        rangeKeyField: str
        """``CfnTopicRule.DynamoDBActionProperty.RangeKeyField``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rangekeyfield
        """
        rangeKeyType: str
        """``CfnTopicRule.DynamoDBActionProperty.RangeKeyType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rangekeytype
        """
        rangeKeyValue: str
        """``CfnTopicRule.DynamoDBActionProperty.RangeKeyValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rangekeyvalue
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.DynamoDBActionProperty", jsii_struct_bases=[_DynamoDBActionProperty])
    class DynamoDBActionProperty(_DynamoDBActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html
        """
        hashKeyField: str
        """``CfnTopicRule.DynamoDBActionProperty.HashKeyField``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-hashkeyfield
        """

        hashKeyValue: str
        """``CfnTopicRule.DynamoDBActionProperty.HashKeyValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-hashkeyvalue
        """

        roleArn: str
        """``CfnTopicRule.DynamoDBActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-rolearn
        """

        tableName: str
        """``CfnTopicRule.DynamoDBActionProperty.TableName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbaction.html#cfn-iot-topicrule-dynamodbaction-tablename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.DynamoDBv2ActionProperty", jsii_struct_bases=[])
    class DynamoDBv2ActionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbv2action.html
        """
        putItem: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.PutItemInputProperty"]
        """``CfnTopicRule.DynamoDBv2ActionProperty.PutItem``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbv2action.html#cfn-iot-topicrule-dynamodbv2action-putitem
        """

        roleArn: str
        """``CfnTopicRule.DynamoDBv2ActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-dynamodbv2action.html#cfn-iot-topicrule-dynamodbv2action-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.ElasticsearchActionProperty", jsii_struct_bases=[])
    class ElasticsearchActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html
        """
        endpoint: str
        """``CfnTopicRule.ElasticsearchActionProperty.Endpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-endpoint
        """

        id: str
        """``CfnTopicRule.ElasticsearchActionProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-id
        """

        index: str
        """``CfnTopicRule.ElasticsearchActionProperty.Index``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-index
        """

        roleArn: str
        """``CfnTopicRule.ElasticsearchActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-rolearn
        """

        type: str
        """``CfnTopicRule.ElasticsearchActionProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-elasticsearchaction.html#cfn-iot-topicrule-elasticsearchaction-type
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FirehoseActionProperty(jsii.compat.TypedDict, total=False):
        separator: str
        """``CfnTopicRule.FirehoseActionProperty.Separator``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html#cfn-iot-topicrule-firehoseaction-separator
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.FirehoseActionProperty", jsii_struct_bases=[_FirehoseActionProperty])
    class FirehoseActionProperty(_FirehoseActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html
        """
        deliveryStreamName: str
        """``CfnTopicRule.FirehoseActionProperty.DeliveryStreamName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html#cfn-iot-topicrule-firehoseaction-deliverystreamname
        """

        roleArn: str
        """``CfnTopicRule.FirehoseActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-firehoseaction.html#cfn-iot-topicrule-firehoseaction-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.IotAnalyticsActionProperty", jsii_struct_bases=[])
    class IotAnalyticsActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotanalyticsaction.html
        """
        channelName: str
        """``CfnTopicRule.IotAnalyticsActionProperty.ChannelName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotanalyticsaction.html#cfn-iot-topicrule-iotanalyticsaction-channelname
        """

        roleArn: str
        """``CfnTopicRule.IotAnalyticsActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-iotanalyticsaction.html#cfn-iot-topicrule-iotanalyticsaction-rolearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _KinesisActionProperty(jsii.compat.TypedDict, total=False):
        partitionKey: str
        """``CfnTopicRule.KinesisActionProperty.PartitionKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html#cfn-iot-topicrule-kinesisaction-partitionkey
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.KinesisActionProperty", jsii_struct_bases=[_KinesisActionProperty])
    class KinesisActionProperty(_KinesisActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html
        """
        roleArn: str
        """``CfnTopicRule.KinesisActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html#cfn-iot-topicrule-kinesisaction-rolearn
        """

        streamName: str
        """``CfnTopicRule.KinesisActionProperty.StreamName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-kinesisaction.html#cfn-iot-topicrule-kinesisaction-streamname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.LambdaActionProperty", jsii_struct_bases=[])
    class LambdaActionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-lambdaaction.html
        """
        functionArn: str
        """``CfnTopicRule.LambdaActionProperty.FunctionArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-lambdaaction.html#cfn-iot-topicrule-lambdaaction-functionarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.PutItemInputProperty", jsii_struct_bases=[])
    class PutItemInputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putiteminput.html
        """
        tableName: str
        """``CfnTopicRule.PutItemInputProperty.TableName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-putiteminput.html#cfn-iot-topicrule-putiteminput-tablename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.RepublishActionProperty", jsii_struct_bases=[])
    class RepublishActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html
        """
        roleArn: str
        """``CfnTopicRule.RepublishActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html#cfn-iot-topicrule-republishaction-rolearn
        """

        topic: str
        """``CfnTopicRule.RepublishActionProperty.Topic``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-republishaction.html#cfn-iot-topicrule-republishaction-topic
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.S3ActionProperty", jsii_struct_bases=[])
    class S3ActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html
        """
        bucketName: str
        """``CfnTopicRule.S3ActionProperty.BucketName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html#cfn-iot-topicrule-s3action-bucketname
        """

        key: str
        """``CfnTopicRule.S3ActionProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html#cfn-iot-topicrule-s3action-key
        """

        roleArn: str
        """``CfnTopicRule.S3ActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-s3action.html#cfn-iot-topicrule-s3action-rolearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SnsActionProperty(jsii.compat.TypedDict, total=False):
        messageFormat: str
        """``CfnTopicRule.SnsActionProperty.MessageFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html#cfn-iot-topicrule-snsaction-messageformat
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SnsActionProperty", jsii_struct_bases=[_SnsActionProperty])
    class SnsActionProperty(_SnsActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html
        """
        roleArn: str
        """``CfnTopicRule.SnsActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html#cfn-iot-topicrule-snsaction-rolearn
        """

        targetArn: str
        """``CfnTopicRule.SnsActionProperty.TargetArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-snsaction.html#cfn-iot-topicrule-snsaction-targetarn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SqsActionProperty(jsii.compat.TypedDict, total=False):
        useBase64: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnTopicRule.SqsActionProperty.UseBase64``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html#cfn-iot-topicrule-sqsaction-usebase64
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.SqsActionProperty", jsii_struct_bases=[_SqsActionProperty])
    class SqsActionProperty(_SqsActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html
        """
        queueUrl: str
        """``CfnTopicRule.SqsActionProperty.QueueUrl``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html#cfn-iot-topicrule-sqsaction-queueurl
        """

        roleArn: str
        """``CfnTopicRule.SqsActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-sqsaction.html#cfn-iot-topicrule-sqsaction-rolearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StepFunctionsActionProperty(jsii.compat.TypedDict, total=False):
        executionNamePrefix: str
        """``CfnTopicRule.StepFunctionsActionProperty.ExecutionNamePrefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html#cfn-iot-topicrule-stepfunctionsaction-executionnameprefix
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.StepFunctionsActionProperty", jsii_struct_bases=[_StepFunctionsActionProperty])
    class StepFunctionsActionProperty(_StepFunctionsActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html
        """
        roleArn: str
        """``CfnTopicRule.StepFunctionsActionProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html#cfn-iot-topicrule-stepfunctionsaction-rolearn
        """

        stateMachineName: str
        """``CfnTopicRule.StepFunctionsActionProperty.StateMachineName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-stepfunctionsaction.html#cfn-iot-topicrule-stepfunctionsaction-statemachinename
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TopicRulePayloadProperty(jsii.compat.TypedDict, total=False):
        awsIotSqlVersion: str
        """``CfnTopicRule.TopicRulePayloadProperty.AwsIotSqlVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-awsiotsqlversion
        """
        description: str
        """``CfnTopicRule.TopicRulePayloadProperty.Description``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-description
        """
        errorAction: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.ActionProperty"]
        """``CfnTopicRule.TopicRulePayloadProperty.ErrorAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-erroraction
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRule.TopicRulePayloadProperty", jsii_struct_bases=[_TopicRulePayloadProperty])
    class TopicRulePayloadProperty(_TopicRulePayloadProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html
        """
        actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.ActionProperty"]]]
        """``CfnTopicRule.TopicRulePayloadProperty.Actions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-actions
        """

        ruleDisabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnTopicRule.TopicRulePayloadProperty.RuleDisabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-ruledisabled
        """

        sql: str
        """``CfnTopicRule.TopicRulePayloadProperty.Sql``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iot-topicrule-topicrulepayload.html#cfn-iot-topicrule-topicrulepayload-sql
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnTopicRuleProps(jsii.compat.TypedDict, total=False):
    ruleName: str
    """``AWS::IoT::TopicRule.RuleName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html#cfn-iot-topicrule-rulename
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-iot.CfnTopicRuleProps", jsii_struct_bases=[_CfnTopicRuleProps])
class CfnTopicRuleProps(_CfnTopicRuleProps):
    """Properties for defining a ``AWS::IoT::TopicRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html
    """
    topicRulePayload: typing.Union[aws_cdk.cdk.Token, "CfnTopicRule.TopicRulePayloadProperty"]
    """``AWS::IoT::TopicRule.TopicRulePayload``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iot-topicrule.html#cfn-iot-topicrule-topicrulepayload
    """

__all__ = ["CfnCertificate", "CfnCertificateProps", "CfnPolicy", "CfnPolicyPrincipalAttachment", "CfnPolicyPrincipalAttachmentProps", "CfnPolicyProps", "CfnThing", "CfnThingPrincipalAttachment", "CfnThingPrincipalAttachmentProps", "CfnThingProps", "CfnTopicRule", "CfnTopicRuleProps", "__jsii_assembly__"]

publication.publish()
