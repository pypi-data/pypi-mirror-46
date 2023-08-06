import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_api
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3_notifications
import aws_cdk.aws_sqs
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-sns", "0.32.0", __name__, "aws-sns@0.32.0.jsii.tgz")
class CfnSubscription(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnSubscription"):
    """A CloudFormation ``AWS::SNS::Subscription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
    cloudformationResource:
        AWS::SNS::Subscription
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, protocol: str, topic_arn: str, delivery_policy: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, endpoint: typing.Optional[str]=None, filter_policy: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, raw_message_delivery: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, region: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SNS::Subscription``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            protocol: ``AWS::SNS::Subscription.Protocol``.
            topicArn: ``AWS::SNS::Subscription.TopicArn``.
            deliveryPolicy: ``AWS::SNS::Subscription.DeliveryPolicy``.
            endpoint: ``AWS::SNS::Subscription.Endpoint``.
            filterPolicy: ``AWS::SNS::Subscription.FilterPolicy``.
            rawMessageDelivery: ``AWS::SNS::Subscription.RawMessageDelivery``.
            region: ``AWS::SNS::Subscription.Region``.
        """
        props: CfnSubscriptionProps = {"protocol": protocol, "topicArn": topic_arn}

        if delivery_policy is not None:
            props["deliveryPolicy"] = delivery_policy

        if endpoint is not None:
            props["endpoint"] = endpoint

        if filter_policy is not None:
            props["filterPolicy"] = filter_policy

        if raw_message_delivery is not None:
            props["rawMessageDelivery"] = raw_message_delivery

        if region is not None:
            props["region"] = region

        jsii.create(CfnSubscription, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSubscriptionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="subscriptionArn")
    def subscription_arn(self) -> str:
        return jsii.get(self, "subscriptionArn")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSubscriptionProps(jsii.compat.TypedDict, total=False):
    deliveryPolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::SNS::Subscription.DeliveryPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-deliverypolicy
    """
    endpoint: str
    """``AWS::SNS::Subscription.Endpoint``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-endpoint
    """
    filterPolicy: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::SNS::Subscription.FilterPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-filterpolicy
    """
    rawMessageDelivery: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::SNS::Subscription.RawMessageDelivery``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-rawmessagedelivery
    """
    region: str
    """``AWS::SNS::Subscription.Region``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-subscription-region
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnSubscriptionProps", jsii_struct_bases=[_CfnSubscriptionProps])
class CfnSubscriptionProps(_CfnSubscriptionProps):
    """Properties for defining a ``AWS::SNS::Subscription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html
    """
    protocol: str
    """``AWS::SNS::Subscription.Protocol``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#cfn-sns-protocol
    """

    topicArn: str
    """``AWS::SNS::Subscription.TopicArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-sns-subscription.html#topicarn
    """

class CfnTopic(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnTopic"):
    """A CloudFormation ``AWS::SNS::Topic``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
    cloudformationResource:
        AWS::SNS::Topic
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, display_name: typing.Optional[str]=None, kms_master_key_id: typing.Optional[str]=None, subscription: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "SubscriptionProperty"]]]]]=None, topic_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::SNS::Topic``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            displayName: ``AWS::SNS::Topic.DisplayName``.
            kmsMasterKeyId: ``AWS::SNS::Topic.KmsMasterKeyId``.
            subscription: ``AWS::SNS::Topic.Subscription``.
            topicName: ``AWS::SNS::Topic.TopicName``.
        """
        props: CfnTopicProps = {}

        if display_name is not None:
            props["displayName"] = display_name

        if kms_master_key_id is not None:
            props["kmsMasterKeyId"] = kms_master_key_id

        if subscription is not None:
            props["subscription"] = subscription

        if topic_name is not None:
            props["topicName"] = topic_name

        jsii.create(CfnTopic, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTopicProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        """
        cloudformationAttribute:
            TopicName
        """
        return jsii.get(self, "topicName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopic.SubscriptionProperty", jsii_struct_bases=[])
    class SubscriptionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html
        """
        endpoint: str
        """``CfnTopic.SubscriptionProperty.Endpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html#cfn-sns-topic-subscription-endpoint
        """

        protocol: str
        """``CfnTopic.SubscriptionProperty.Protocol``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-subscription.html#cfn-sns-topic-subscription-protocol
        """


class CfnTopicPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.CfnTopicPolicy"):
    """A CloudFormation ``AWS::SNS::TopicPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
    cloudformationResource:
        AWS::SNS::TopicPolicy
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_document: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], topics: typing.List[str]) -> None:
        """Create a new ``AWS::SNS::TopicPolicy``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            policyDocument: ``AWS::SNS::TopicPolicy.PolicyDocument``.
            topics: ``AWS::SNS::TopicPolicy.Topics``.
        """
        props: CfnTopicPolicyProps = {"policyDocument": policy_document, "topics": topics}

        jsii.create(CfnTopicPolicy, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnTopicPolicyProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopicPolicyProps", jsii_struct_bases=[])
class CfnTopicPolicyProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::SNS::TopicPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html
    """
    policyDocument: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::SNS::TopicPolicy.PolicyDocument``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-policydocument
    """

    topics: typing.List[str]
    """``AWS::SNS::TopicPolicy.Topics``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-policy.html#cfn-sns-topicpolicy-topics
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.CfnTopicProps", jsii_struct_bases=[])
class CfnTopicProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::SNS::Topic``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html
    """
    displayName: str
    """``AWS::SNS::Topic.DisplayName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-displayname
    """

    kmsMasterKeyId: str
    """``AWS::SNS::Topic.KmsMasterKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-kmsmasterkeyid
    """

    subscription: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnTopic.SubscriptionProperty"]]]
    """``AWS::SNS::Topic.Subscription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-subscription
    """

    topicName: str
    """``AWS::SNS::Topic.TopicName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-sns-topic.html#cfn-sns-topic-topicname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.EmailSubscriptionOptions", jsii_struct_bases=[])
class EmailSubscriptionOptions(jsii.compat.TypedDict, total=False):
    """Options for email subscriptions."""
    json: bool
    """Indicates if the full notification JSON should be sent to the email address or just the message text.

    Default:
        Message text (false)
    """

@jsii.interface(jsii_type="@aws-cdk/aws-sns.ITopic")
class ITopic(aws_cdk.cdk.IResource, aws_cdk.aws_cloudwatch.IAlarmAction, aws_cdk.aws_s3_notifications.IBucketNotificationDestination, aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _ITopicProxy

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        """
        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        """
        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is improted (``Topic.import``), then this is a no-op.

        Arguments:
            statement: -
        """
        ...

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant topic publishing permissions to the given identity.

        Arguments:
            identity: -
        """
        ...

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Topic.

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages published to your Amazon SNS topics.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that Amazon SNS failed to deliver.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

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

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

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

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the size of messages published through this topic.

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

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

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

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The rate of successful SMS message deliveries.

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

    @jsii.member(jsii_name="subscribe")
    def subscribe(self, name: str, endpoint: str, protocol: "SubscriptionProtocol", raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Subscribe some endpoint to this topic.

        Arguments:
            name: -
            endpoint: -
            protocol: -
            rawMessageDelivery: -
        """
        ...

    @jsii.member(jsii_name="subscribeEmail")
    def subscribe_email(self, name: str, email_address: str, *, json: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an email address.

        Arguments:
            name: A name for the subscription.
            emailAddress: The email address to use.
            options: Options to use for email subscription.
            json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: Message text (false)
        """
        ...

    @jsii.member(jsii_name="subscribeLambda")
    def subscribe_lambda(self, lambda_function: aws_cdk.aws_lambda.IFunction) -> "Subscription":
        """Defines a subscription from this SNS Topic to a Lambda function.

        The Lambda's resource policy will be updated to allow this topic to
        invoke the function.

        Arguments:
            lambdaFunction: The Lambda function to invoke.
        """
        ...

    @jsii.member(jsii_name="subscribeQueue")
    def subscribe_queue(self, queue: aws_cdk.aws_sqs.IQueue, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an SQS queue.

        The queue resource policy will be updated to allow this SNS topic to send
        messages to the queue.

        Arguments:
            queue: The target queue.
            rawMessageDelivery: Enable raw message delivery.
        """
        ...

    @jsii.member(jsii_name="subscribeUrl")
    def subscribe_url(self, name: str, url: str, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an http:// or https:// URL.

        Arguments:
            name: A name for the subscription.
            url: The URL to invoke.
            rawMessageDelivery: Enable raw message delivery.
        """
        ...


class _ITopicProxy(jsii.proxy_for(aws_cdk.cdk.IResource), jsii.proxy_for(aws_cdk.aws_cloudwatch.IAlarmAction), jsii.proxy_for(aws_cdk.aws_s3_notifications.IBucketNotificationDestination), jsii.proxy_for(aws_cdk.aws_autoscaling_api.ILifecycleHookTarget)):
    __jsii_type__ = "@aws-cdk/aws-sns.ITopic"
    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "topicName")

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is improted (``Topic.import``), then this is a no-op.

        Arguments:
            statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, identity: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant topic publishing permissions to the given identity.

        Arguments:
            identity: -
        """
        return jsii.invoke(self, "grantPublish", [identity])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Topic.

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages published to your Amazon SNS topics.

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

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

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

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that Amazon SNS failed to deliver.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the size of messages published through this topic.

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

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

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

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The rate of successful SMS message deliveries.

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

        return jsii.invoke(self, "metricSMSSuccessRate", [props])

    @jsii.member(jsii_name="subscribe")
    def subscribe(self, name: str, endpoint: str, protocol: "SubscriptionProtocol", raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Subscribe some endpoint to this topic.

        Arguments:
            name: -
            endpoint: -
            protocol: -
            rawMessageDelivery: -
        """
        return jsii.invoke(self, "subscribe", [name, endpoint, protocol, raw_message_delivery])

    @jsii.member(jsii_name="subscribeEmail")
    def subscribe_email(self, name: str, email_address: str, *, json: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an email address.

        Arguments:
            name: A name for the subscription.
            emailAddress: The email address to use.
            options: Options to use for email subscription.
            json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: Message text (false)
        """
        options: EmailSubscriptionOptions = {}

        if json is not None:
            options["json"] = json

        return jsii.invoke(self, "subscribeEmail", [name, email_address, options])

    @jsii.member(jsii_name="subscribeLambda")
    def subscribe_lambda(self, lambda_function: aws_cdk.aws_lambda.IFunction) -> "Subscription":
        """Defines a subscription from this SNS Topic to a Lambda function.

        The Lambda's resource policy will be updated to allow this topic to
        invoke the function.

        Arguments:
            lambdaFunction: The Lambda function to invoke.
        """
        return jsii.invoke(self, "subscribeLambda", [lambda_function])

    @jsii.member(jsii_name="subscribeQueue")
    def subscribe_queue(self, queue: aws_cdk.aws_sqs.IQueue, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an SQS queue.

        The queue resource policy will be updated to allow this SNS topic to send
        messages to the queue.

        Arguments:
            queue: The target queue.
            rawMessageDelivery: Enable raw message delivery.
        """
        return jsii.invoke(self, "subscribeQueue", [queue, raw_message_delivery])

    @jsii.member(jsii_name="subscribeUrl")
    def subscribe_url(self, name: str, url: str, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an http:// or https:// URL.

        Arguments:
            name: A name for the subscription.
            url: The URL to invoke.
            rawMessageDelivery: Enable raw message delivery.
        """
        return jsii.invoke(self, "subscribeUrl", [name, url, raw_message_delivery])


class Subscription(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.Subscription"):
    """A new subscription.

    Prefer to use the ``ITopic.subscribeXxx()`` methods to creating instances of
    this class.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, endpoint: typing.Any, protocol: "SubscriptionProtocol", topic: "ITopic", raw_message_delivery: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            endpoint: The subscription endpoint. The meaning of this value depends on the value for 'protocol'.
            protocol: What type of subscription to add.
            topic: The topic to subscribe to.
            rawMessageDelivery: true if raw message delivery is enabled for the subscription. Raw messages are free of JSON formatting and can be sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple Notification Service API Reference. Default: false
        """
        props: SubscriptionProps = {"endpoint": endpoint, "protocol": protocol, "topic": topic}

        if raw_message_delivery is not None:
            props["rawMessageDelivery"] = raw_message_delivery

        jsii.create(Subscription, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _SubscriptionProps(jsii.compat.TypedDict, total=False):
    rawMessageDelivery: bool
    """true if raw message delivery is enabled for the subscription.

    Raw messages are free of JSON formatting and can be
    sent to HTTP/S and Amazon SQS endpoints. For more information, see GetSubscriptionAttributes in the Amazon Simple
    Notification Service API Reference.

    Default:
        false
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.SubscriptionProps", jsii_struct_bases=[_SubscriptionProps])
class SubscriptionProps(_SubscriptionProps):
    """Properties for creating a new subscription."""
    endpoint: typing.Any
    """The subscription endpoint.

    The meaning of this value depends on the value for 'protocol'.
    """

    protocol: "SubscriptionProtocol"
    """What type of subscription to add."""

    topic: "ITopic"
    """The topic to subscribe to."""

@jsii.enum(jsii_type="@aws-cdk/aws-sns.SubscriptionProtocol")
class SubscriptionProtocol(enum.Enum):
    """The type of subscription, controlling the type of the endpoint parameter."""
    Http = "Http"
    """JSON-encoded message is POSTED to an HTTP url."""
    Https = "Https"
    """JSON-encoded message is POSTed to an HTTPS url."""
    Email = "Email"
    """Notifications are sent via email."""
    EmailJson = "EmailJson"
    """Notifications are JSON-encoded and sent via mail."""
    Sms = "Sms"
    """Notification is delivered by SMS."""
    Sqs = "Sqs"
    """Notifications are enqueued into an SQS queue."""
    Application = "Application"
    """JSON-encoded notifications are sent to a mobile app endpoint."""
    Lambda = "Lambda"
    """Notifications trigger a Lambda function."""

@jsii.implements(ITopic)
class TopicBase(aws_cdk.cdk.Resource, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-sns.TopicBase"):
    """Either a new or imported Topic."""
    @staticmethod
    def __jsii_proxy_class__():
        return _TopicBaseProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str) -> None:
        """Creates a new construct node.

        Arguments:
            scope: The scope in which to define this construct.
            id: The scoped construct ID. Must be unique amongst siblings. If the ID includes a path separator (``/``), then it will be replaced by double dash ``--``.
        """
        jsii.create(TopicBase, self, [scope, id])

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM resource policy associated with this topic.

        If this topic was created in this stack (``new Topic``), a topic policy
        will be automatically created upon the first call to ``addToPolicy``. If
        the topic is improted (``Topic.import``), then this is a no-op.

        Arguments:
            statement: -
        """
        return jsii.invoke(self, "addToResourcePolicy", [statement])

    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> aws_cdk.aws_s3_notifications.BucketNotificationDestinationProps:
        """Implements the IBucketNotificationDestination interface, allowing topics to be used as bucket notification destinations.

        Arguments:
            bucketArn: The ARN of the bucket sending the notifications.
            bucketId: A unique ID of the bucket.
        """
        return jsii.invoke(self, "asBucketNotificationDestination", [bucket_arn, bucket_id])

    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: aws_cdk.aws_autoscaling_api.ILifecycleHook) -> aws_cdk.aws_autoscaling_api.LifecycleHookTargetProps:
        """Allow using SNS topics as lifecycle hook targets.

        Arguments:
            lifecycleHook: -
        """
        return jsii.invoke(self, "asLifecycleHookTarget", [lifecycle_hook])

    @jsii.member(jsii_name="grantPublish")
    def grant_publish(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant topic publishing permissions to the given identity.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantPublish", [grantee])

    @jsii.member(jsii_name="metric")
    def metric(self, metric_name: str, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Return the given named metric for this Topic.

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

    @jsii.member(jsii_name="metricNumberOfMessagesPublished")
    def metric_number_of_messages_published(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages published to your Amazon SNS topics.

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

        return jsii.invoke(self, "metricNumberOfMessagesPublished", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsDelivered")
    def metric_number_of_notifications_delivered(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages successfully delivered from your Amazon SNS topics to subscribing endpoints.

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

        return jsii.invoke(self, "metricNumberOfNotificationsDelivered", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFailed")
    def metric_number_of_notifications_failed(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that Amazon SNS failed to deliver.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFailed", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOut")
    def metric_number_of_notifications_filtered_out(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOut", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutInvalidAttributes")
    def metric_number_of_notifications_filtered_out_invalid_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages' attributes are invalid.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutInvalidAttributes", [props])

    @jsii.member(jsii_name="metricNumberOfNotificationsFilteredOutNoMessageAttributes")
    def metric_number_of_notifications_filtered_out_no_message_attributes(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The number of messages that were rejected by subscription filter policies because the messages have no attributes.

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

        return jsii.invoke(self, "metricNumberOfNotificationsFilteredOutNoMessageAttributes", [props])

    @jsii.member(jsii_name="metricPublishSize")
    def metric_publish_size(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """Metric for the size of messages published through this topic.

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

        return jsii.invoke(self, "metricPublishSize", [props])

    @jsii.member(jsii_name="metricSMSMonthToDateSpentUSD")
    def metric_sms_month_to_date_spent_usd(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The charges you have accrued since the start of the current calendar month for sending SMS messages.

        Maximum over 5 minutes

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

        return jsii.invoke(self, "metricSMSMonthToDateSpentUSD", [props])

    @jsii.member(jsii_name="metricSMSSuccessRate")
    def metric_sms_success_rate(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional[aws_cdk.aws_cloudwatch.Unit]=None) -> aws_cdk.aws_cloudwatch.Metric:
        """The rate of successful SMS message deliveries.

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

        return jsii.invoke(self, "metricSMSSuccessRate", [props])

    @jsii.member(jsii_name="subscribe")
    def subscribe(self, name: str, endpoint: str, protocol: "SubscriptionProtocol", raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Subscribe some endpoint to this topic.

        Arguments:
            name: -
            endpoint: -
            protocol: -
            rawMessageDelivery: -
        """
        return jsii.invoke(self, "subscribe", [name, endpoint, protocol, raw_message_delivery])

    @jsii.member(jsii_name="subscribeEmail")
    def subscribe_email(self, name: str, email_address: str, *, json: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an email address.

        Arguments:
            name: A name for the subscription.
            emailAddress: The email address to use.
            options: Options for the email delivery format.
            json: Indicates if the full notification JSON should be sent to the email address or just the message text. Default: Message text (false)
        """
        options: EmailSubscriptionOptions = {}

        if json is not None:
            options["json"] = json

        return jsii.invoke(self, "subscribeEmail", [name, email_address, options])

    @jsii.member(jsii_name="subscribeLambda")
    def subscribe_lambda(self, lambda_function: aws_cdk.aws_lambda.IFunction) -> "Subscription":
        """Defines a subscription from this SNS Topic to a Lambda function.

        The Lambda's resource policy will be updated to allow this topic to
        invoke the function.

        Arguments:
            lambdaFunction: The Lambda function to invoke.
        """
        return jsii.invoke(self, "subscribeLambda", [lambda_function])

    @jsii.member(jsii_name="subscribeQueue")
    def subscribe_queue(self, queue: aws_cdk.aws_sqs.IQueue, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an SQS queue.

        The queue resource policy will be updated to allow this SNS topic to send
        messages to the queue.

        Arguments:
            queue: The target queue.
            rawMessageDelivery: Enable raw message delivery.
        """
        return jsii.invoke(self, "subscribeQueue", [queue, raw_message_delivery])

    @jsii.member(jsii_name="subscribeUrl")
    def subscribe_url(self, name: str, url: str, raw_message_delivery: typing.Optional[bool]=None) -> "Subscription":
        """Defines a subscription from this SNS topic to an http:// or https:// URL.

        Arguments:
            name: A name for the subscription.
            url: The URL to invoke.
            rawMessageDelivery: Enable raw message delivery.
        """
        return jsii.invoke(self, "subscribeUrl", [name, url, raw_message_delivery])

    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        """Return the ARN that should be used for a CloudWatch Alarm action."""
        return jsii.get(self, "alarmActionArn")

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    @abc.abstractmethod
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        ...

    @property
    @jsii.member(jsii_name="topicArn")
    @abc.abstractmethod
    def topic_arn(self) -> str:
        ...

    @property
    @jsii.member(jsii_name="topicName")
    @abc.abstractmethod
    def topic_name(self) -> str:
        ...


class _TopicBaseProxy(TopicBase, jsii.proxy_for(aws_cdk.cdk.Resource)):
    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        return jsii.get(self, "autoCreatePolicy")

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")


class Topic(TopicBase, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.Topic"):
    """A new SNS topic."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, display_name: typing.Optional[str]=None, topic_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            displayName: A developer-defined string that can be used to identify this SNS topic. Default: None
            topicName: A name for the topic. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the topic name. For more information, see Name Type. Default: Generated name
        """
        props: TopicProps = {}

        if display_name is not None:
            props["displayName"] = display_name

        if topic_name is not None:
            props["topicName"] = topic_name

        jsii.create(Topic, self, [scope, id, props])

    @jsii.member(jsii_name="fromTopicArn")
    @classmethod
    def from_topic_arn(cls, scope: aws_cdk.cdk.Construct, id: str, topic_arn: str) -> "ITopic":
        """
        Arguments:
            scope: -
            id: -
            topicArn: -
        """
        return jsii.sinvoke(cls, "fromTopicArn", [scope, id, topic_arn])

    @property
    @jsii.member(jsii_name="autoCreatePolicy")
    def _auto_create_policy(self) -> bool:
        """Controls automatic creation of policy objects.

        Set by subclasses.
        """
        return jsii.get(self, "autoCreatePolicy")

    @property
    @jsii.member(jsii_name="topicArn")
    def topic_arn(self) -> str:
        return jsii.get(self, "topicArn")

    @property
    @jsii.member(jsii_name="topicName")
    def topic_name(self) -> str:
        return jsii.get(self, "topicName")


class TopicPolicy(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-sns.TopicPolicy"):
    """Applies a policy to SNS topics."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, topics: typing.List["ITopic"]) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            topics: The set of topics this policy applies to.
        """
        props: TopicPolicyProps = {"topics": topics}

        jsii.create(TopicPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="document")
    def document(self) -> aws_cdk.aws_iam.PolicyDocument:
        """The IAM policy document for this policy."""
        return jsii.get(self, "document")


@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicPolicyProps", jsii_struct_bases=[])
class TopicPolicyProps(jsii.compat.TypedDict):
    topics: typing.List["ITopic"]
    """The set of topics this policy applies to."""

@jsii.data_type(jsii_type="@aws-cdk/aws-sns.TopicProps", jsii_struct_bases=[])
class TopicProps(jsii.compat.TypedDict, total=False):
    """Properties for a new SNS topic."""
    displayName: str
    """A developer-defined string that can be used to identify this SNS topic.

    Default:
        None
    """

    topicName: str
    """A name for the topic.

    If you don't specify a name, AWS CloudFormation generates a unique
    physical ID and uses that ID for the topic name. For more information,
    see Name Type.

    Default:
        Generated name
    """

__all__ = ["CfnSubscription", "CfnSubscriptionProps", "CfnTopic", "CfnTopicPolicy", "CfnTopicPolicyProps", "CfnTopicProps", "EmailSubscriptionOptions", "ITopic", "Subscription", "SubscriptionProps", "SubscriptionProtocol", "Topic", "TopicBase", "TopicPolicy", "TopicPolicyProps", "TopicProps", "__jsii_assembly__"]

publication.publish()
