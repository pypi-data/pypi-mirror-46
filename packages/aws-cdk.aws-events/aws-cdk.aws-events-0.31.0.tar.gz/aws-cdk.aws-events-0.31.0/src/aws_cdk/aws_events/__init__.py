import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-events", "0.31.0", __name__, "aws-events@0.31.0.jsii.tgz")
class CfnEventBusPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy"):
    """A CloudFormation ``AWS::Events::EventBusPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
    cloudformationResource:
        AWS::Events::EventBusPolicy
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, action: str, principal: str, statement_id: str, condition: typing.Optional[typing.Union[typing.Optional["ConditionProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None) -> None:
        """Create a new ``AWS::Events::EventBusPolicy``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            action: ``AWS::Events::EventBusPolicy.Action``.
            principal: ``AWS::Events::EventBusPolicy.Principal``.
            statementId: ``AWS::Events::EventBusPolicy.StatementId``.
            condition: ``AWS::Events::EventBusPolicy.Condition``.
        """
        props: CfnEventBusPolicyProps = {"action": action, "principal": principal, "statementId": statement_id}

        if condition is not None:
            props["condition"] = condition

        jsii.create(CfnEventBusPolicy, self, [scope, id, props])

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
    @jsii.member(jsii_name="eventBusPolicyId")
    def event_bus_policy_id(self) -> str:
        return jsii.get(self, "eventBusPolicyId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEventBusPolicyProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusPolicy.ConditionProperty", jsii_struct_bases=[])
    class ConditionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html
        """
        key: str
        """``CfnEventBusPolicy.ConditionProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-key
        """

        type: str
        """``CfnEventBusPolicy.ConditionProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-type
        """

        value: str
        """``CfnEventBusPolicy.ConditionProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-eventbuspolicy-condition.html#cfn-events-eventbuspolicy-condition-value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnEventBusPolicyProps(jsii.compat.TypedDict, total=False):
    condition: typing.Union["CfnEventBusPolicy.ConditionProperty", aws_cdk.cdk.Token]
    """``AWS::Events::EventBusPolicy.Condition``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-condition
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnEventBusPolicyProps", jsii_struct_bases=[_CfnEventBusPolicyProps])
class CfnEventBusPolicyProps(_CfnEventBusPolicyProps):
    """Properties for defining a ``AWS::Events::EventBusPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html
    """
    action: str
    """``AWS::Events::EventBusPolicy.Action``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-action
    """

    principal: str
    """``AWS::Events::EventBusPolicy.Principal``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-principal
    """

    statementId: str
    """``AWS::Events::EventBusPolicy.StatementId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-eventbuspolicy.html#cfn-events-eventbuspolicy-statementid
    """

class CfnRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.CfnRule"):
    """A CloudFormation ``AWS::Events::Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
    cloudformationResource:
        AWS::Events::Rule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, event_pattern: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, name: typing.Optional[str]=None, role_arn: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, state: typing.Optional[str]=None, targets: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "TargetProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Events::Rule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            description: ``AWS::Events::Rule.Description``.
            eventPattern: ``AWS::Events::Rule.EventPattern``.
            name: ``AWS::Events::Rule.Name``.
            roleArn: ``AWS::Events::Rule.RoleArn``.
            scheduleExpression: ``AWS::Events::Rule.ScheduleExpression``.
            state: ``AWS::Events::Rule.State``.
            targets: ``AWS::Events::Rule.Targets``.
        """
        props: CfnRuleProps = {}

        if description is not None:
            props["description"] = description

        if event_pattern is not None:
            props["eventPattern"] = event_pattern

        if name is not None:
            props["name"] = name

        if role_arn is not None:
            props["roleArn"] = role_arn

        if schedule_expression is not None:
            props["scheduleExpression"] = schedule_expression

        if state is not None:
            props["state"] = state

        if targets is not None:
            props["targets"] = targets

        jsii.create(CfnRule, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "ruleArn")

    @property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> str:
        return jsii.get(self, "ruleId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _EcsParametersProperty(jsii.compat.TypedDict, total=False):
        taskCount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnRule.EcsParametersProperty.TaskCount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskcount
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.EcsParametersProperty", jsii_struct_bases=[_EcsParametersProperty])
    class EcsParametersProperty(_EcsParametersProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html
        """
        taskDefinitionArn: str
        """``CfnRule.EcsParametersProperty.TaskDefinitionArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-ecsparameters.html#cfn-events-rule-ecsparameters-taskdefinitionarn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _InputTransformerProperty(jsii.compat.TypedDict, total=False):
        inputPathsMap: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
        """``CfnRule.InputTransformerProperty.InputPathsMap``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputpathsmap
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.InputTransformerProperty", jsii_struct_bases=[_InputTransformerProperty])
    class InputTransformerProperty(_InputTransformerProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html
        """
        inputTemplate: str
        """``CfnRule.InputTransformerProperty.InputTemplate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-inputtransformer.html#cfn-events-rule-inputtransformer-inputtemplate
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.KinesisParametersProperty", jsii_struct_bases=[])
    class KinesisParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html
        """
        partitionKeyPath: str
        """``CfnRule.KinesisParametersProperty.PartitionKeyPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-kinesisparameters.html#cfn-events-rule-kinesisparameters-partitionkeypath
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandParametersProperty", jsii_struct_bases=[])
    class RunCommandParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html
        """
        runCommandTargets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.RunCommandTargetProperty"]]]
        """``CfnRule.RunCommandParametersProperty.RunCommandTargets``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandparameters.html#cfn-events-rule-runcommandparameters-runcommandtargets
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.RunCommandTargetProperty", jsii_struct_bases=[])
    class RunCommandTargetProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html
        """
        key: str
        """``CfnRule.RunCommandTargetProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-key
        """

        values: typing.List[str]
        """``CfnRule.RunCommandTargetProperty.Values``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-runcommandtarget.html#cfn-events-rule-runcommandtarget-values
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.SqsParametersProperty", jsii_struct_bases=[])
    class SqsParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html
        """
        messageGroupId: str
        """``CfnRule.SqsParametersProperty.MessageGroupId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-sqsparameters.html#cfn-events-rule-sqsparameters-messagegroupid
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TargetProperty(jsii.compat.TypedDict, total=False):
        ecsParameters: typing.Union["CfnRule.EcsParametersProperty", aws_cdk.cdk.Token]
        """``CfnRule.TargetProperty.EcsParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-ecsparameters
        """
        input: str
        """``CfnRule.TargetProperty.Input``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-input
        """
        inputPath: str
        """``CfnRule.TargetProperty.InputPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputpath
        """
        inputTransformer: typing.Union[aws_cdk.cdk.Token, "CfnRule.InputTransformerProperty"]
        """``CfnRule.TargetProperty.InputTransformer``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-inputtransformer
        """
        kinesisParameters: typing.Union["CfnRule.KinesisParametersProperty", aws_cdk.cdk.Token]
        """``CfnRule.TargetProperty.KinesisParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-kinesisparameters
        """
        roleArn: str
        """``CfnRule.TargetProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-rolearn
        """
        runCommandParameters: typing.Union["CfnRule.RunCommandParametersProperty", aws_cdk.cdk.Token]
        """``CfnRule.TargetProperty.RunCommandParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-runcommandparameters
        """
        sqsParameters: typing.Union[aws_cdk.cdk.Token, "CfnRule.SqsParametersProperty"]
        """``CfnRule.TargetProperty.SqsParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-sqsparameters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRule.TargetProperty", jsii_struct_bases=[_TargetProperty])
    class TargetProperty(_TargetProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html
        """
        arn: str
        """``CfnRule.TargetProperty.Arn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-arn
        """

        id: str
        """``CfnRule.TargetProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-events-rule-target.html#cfn-events-rule-target-id
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-events.CfnRuleProps", jsii_struct_bases=[])
class CfnRuleProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::Events::Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html
    """
    description: str
    """``AWS::Events::Rule.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-description
    """

    eventPattern: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::Events::Rule.EventPattern``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-eventpattern
    """

    name: str
    """``AWS::Events::Rule.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-name
    """

    roleArn: str
    """``AWS::Events::Rule.RoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-rolearn
    """

    scheduleExpression: str
    """``AWS::Events::Rule.ScheduleExpression``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-scheduleexpression
    """

    state: str
    """``AWS::Events::Rule.State``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-state
    """

    targets: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.TargetProperty"]]]
    """``AWS::Events::Rule.Targets``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-events-rule.html#cfn-events-rule-targets
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventPattern", jsii_struct_bases=[])
class EventPattern(jsii.compat.TypedDict, total=False):
    """Events in Amazon CloudWatch Events are represented as JSON objects. For more information about JSON objects, see RFC 7159.

    Rules use event patterns to select events and route them to targets. A
    pattern either matches an event or it doesn't. Event patterns are represented
    as JSON objects with a structure that is similar to that of events, for
    example:

    It is important to remember the following about event pattern matching:

    - For a pattern to match an event, the event must contain all the field names
      listed in the pattern. The field names must appear in the event with the
      same nesting structure.
    - Other fields of the event not mentioned in the pattern are ignored;
      effectively, there is a ``"*": "*"`` wildcard for fields not mentioned.
    - The matching is exact (character-by-character), without case-folding or any
      other string normalization.
    - The values being matched follow JSON rules: Strings enclosed in quotes,
      numbers, and the unquoted keywords true, false, and null.
    - Number matching is at the string representation level. For example, 300,
      300.0, and 3.0e2 are not considered equal.

    See:
        https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/CloudWatchEventsandEventPatterns.html
    """
    account: typing.List[str]
    """The 12-digit number identifying an AWS account."""

    detail: typing.Any
    """A JSON object, whose content is at the discretion of the service originating the event."""

    detailType: typing.List[str]
    """Identifies, in combination with the source field, the fields and values that appear in the detail field.

    Represents the "detail-type" event field.
    """

    id: typing.List[str]
    """A unique value is generated for every event.

    This can be helpful in
    tracing events as they move through rules to targets, and are processed.
    """

    region: typing.List[str]
    """Identifies the AWS region where the event originated."""

    resources: typing.List[str]
    """This JSON array contains ARNs that identify resources that are involved in the event.

    Inclusion of these ARNs is at the discretion of the
    service.

    For example, Amazon EC2 instance state-changes include Amazon EC2
    instance ARNs, Auto Scaling events include ARNs for both instances and
    Auto Scaling groups, but API calls with AWS CloudTrail do not include
    resource ARNs.
    """

    source: typing.List[str]
    """Identifies the service that sourced the event.

    All events sourced from
    within AWS begin with "aws." Customer-generated events can have any value
    here, as long as it doesn't begin with "aws." We recommend the use of
    Java package-name style reverse domain-name strings.

    To find the correct value for source for an AWS service, see the table in
    AWS Service Namespaces. For example, the source value for Amazon
    CloudFront is aws.cloudfront.

    See:
        http://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html#genref-aws-service-namespaces
    """

    time: typing.List[str]
    """The event timestamp, which can be specified by the service originating the event.

    If the event spans a time interval, the service might choose
    to report the start time, so this value can be noticeably before the time
    the event is actually received.
    """

    version: typing.List[str]
    """By default, this is set to 0 (zero) in all events."""

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventRuleAttributes", jsii_struct_bases=[])
class EventRuleAttributes(jsii.compat.TypedDict):
    eventRuleArn: str
    """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example."""

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventRuleProps", jsii_struct_bases=[])
class EventRuleProps(jsii.compat.TypedDict, total=False):
    description: str
    """A description of the rule's purpose."""

    enabled: bool
    """Indicates whether the rule is enabled.

    Default:
        Rule is enabled
    """

    eventPattern: "EventPattern"
    """Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.

    See:
        http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/CloudWatchEventsandEventPatterns.html
        
        You must specify this property (either via props or via
        ``addEventPattern``), the ``scheduleExpression`` property, or both. The
        method ``addEventPattern`` can be used to add filter values to the event
        pattern.
    """

    ruleName: str
    """A name for the rule.

    If you don't specify a name, AWS CloudFormation
    generates a unique physical ID and uses that ID for the rule name. For
    more information, see Name Type.
    """

    scheduleExpression: str
    """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

    For more information, see Schedule Expression Syntax for
    Rules in the Amazon CloudWatch User Guide.

    See:
        http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
        
        You must specify this property, the ``eventPattern`` property, or both.
    """

    targets: typing.List["IEventRuleTarget"]
    """Targets to invoke when this rule matches an event.

    Input will be the full matched event. If you wish to specify custom
    target input, use ``addTarget(target[, inputOptions])``.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _EventRuleTargetProps(jsii.compat.TypedDict, total=False):
    ecsParameters: "CfnRule.EcsParametersProperty"
    """The Amazon ECS task definition and task count to use, if the event target is an Amazon ECS task."""
    kinesisParameters: "CfnRule.KinesisParametersProperty"
    """Settings that control shard assignment, when the target is a Kinesis stream.

    If you don't include this parameter, eventId is used as the
    partition key.
    """
    roleArn: str
    """The Amazon Resource Name (ARN) of the AWS Identity and Access Management (IAM) role to use for this target when the rule is triggered.

    If one rule
    triggers multiple targets, you can use a different IAM role for each
    target.
    """
    runCommandParameters: "CfnRule.RunCommandParametersProperty"
    """Parameters used when the rule invokes Amazon EC2 Systems Manager Run Command."""

@jsii.data_type(jsii_type="@aws-cdk/aws-events.EventRuleTargetProps", jsii_struct_bases=[_EventRuleTargetProps])
class EventRuleTargetProps(_EventRuleTargetProps):
    arn: str
    """The Amazon Resource Name (ARN) of the target."""

    id: str
    """A unique, user-defined identifier for the target.

    Acceptable values
    include alphanumeric characters, periods (.), hyphens (-), and
    underscores (_).
    """

@jsii.interface(jsii_type="@aws-cdk/aws-events.IEventRule")
class IEventRule(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IEventRuleProxy

    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "EventRuleAttributes":
        """Exports this rule resource from this stack and returns an import token."""
        ...


class _IEventRuleProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-events.IEventRule"
    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example.

        attribute:
            true
        """
        return jsii.get(self, "ruleArn")

    @jsii.member(jsii_name="export")
    def export(self) -> "EventRuleAttributes":
        """Exports this rule resource from this stack and returns an import token."""
        return jsii.invoke(self, "export", [])


@jsii.implements(IEventRule)
class EventRule(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events.EventRule"):
    """Defines a CloudWatch Event Rule in this stack.

    resource:
        AWS::Events::Rule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional["EventPattern"]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List["IEventRuleTarget"]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        props: EventRuleProps = {}

        if description is not None:
            props["description"] = description

        if enabled is not None:
            props["enabled"] = enabled

        if event_pattern is not None:
            props["eventPattern"] = event_pattern

        if rule_name is not None:
            props["ruleName"] = rule_name

        if schedule_expression is not None:
            props["scheduleExpression"] = schedule_expression

        if targets is not None:
            props["targets"] = targets

        jsii.create(EventRule, self, [scope, id, props])

    @jsii.member(jsii_name="fromEventRuleArn")
    @classmethod
    def from_event_rule_arn(cls, scope: aws_cdk.cdk.Construct, id: str, event_rule_arn: str) -> "IEventRule":
        """
        Arguments:
            scope: -
            id: -
            eventRuleArn: -
        """
        return jsii.sinvoke(cls, "fromEventRuleArn", [scope, id, event_rule_arn])

    @jsii.member(jsii_name="addEventPattern")
    def add_event_pattern(self, *, account: typing.Optional[typing.List[str]]=None, detail: typing.Any=None, detail_type: typing.Optional[typing.List[str]]=None, id: typing.Optional[typing.List[str]]=None, region: typing.Optional[typing.List[str]]=None, resources: typing.Optional[typing.List[str]]=None, source: typing.Optional[typing.List[str]]=None, time: typing.Optional[typing.List[str]]=None, version: typing.Optional[typing.List[str]]=None) -> None:
        """Adds an event pattern filter to this rule.

        If a pattern was already specified,
        these values are merged into the existing pattern.

        For example, if the rule already contains the pattern::

           {
             "resources": [ "r1" ],
             "detail": {
               "hello": [ 1 ]
             }
           }

        And ``addEventPattern`` is called with the pattern::

           {
             "resources": [ "r2" ],
             "detail": {
               "foo": [ "bar" ]
             }
           }

        The resulting event pattern will be::

           {
             "resources": [ "r1", "r2" ],
             "detail": {
               "hello": [ 1 ],
               "foo": [ "bar" ]
             }
           }

        Arguments:
            eventPattern: -
            account: The 12-digit number identifying an AWS account.
            detail: A JSON object, whose content is at the discretion of the service originating the event.
            detailType: Identifies, in combination with the source field, the fields and values that appear in the detail field. Represents the "detail-type" event field.
            id: A unique value is generated for every event. This can be helpful in tracing events as they move through rules to targets, and are processed.
            region: Identifies the AWS region where the event originated.
            resources: This JSON array contains ARNs that identify resources that are involved in the event. Inclusion of these ARNs is at the discretion of the service. For example, Amazon EC2 instance state-changes include Amazon EC2 instance ARNs, Auto Scaling events include ARNs for both instances and Auto Scaling groups, but API calls with AWS CloudTrail do not include resource ARNs.
            source: Identifies the service that sourced the event. All events sourced from within AWS begin with "aws." Customer-generated events can have any value here, as long as it doesn't begin with "aws." We recommend the use of Java package-name style reverse domain-name strings. To find the correct value for source for an AWS service, see the table in AWS Service Namespaces. For example, the source value for Amazon CloudFront is aws.cloudfront.
            time: The event timestamp, which can be specified by the service originating the event. If the event spans a time interval, the service might choose to report the start time, so this value can be noticeably before the time the event is actually received.
            version: By default, this is set to 0 (zero) in all events.
        """
        event_pattern: EventPattern = {}

        if account is not None:
            event_pattern["account"] = account

        if detail is not None:
            event_pattern["detail"] = detail

        if detail_type is not None:
            event_pattern["detailType"] = detail_type

        if id is not None:
            event_pattern["id"] = id

        if region is not None:
            event_pattern["region"] = region

        if resources is not None:
            event_pattern["resources"] = resources

        if source is not None:
            event_pattern["source"] = source

        if time is not None:
            event_pattern["time"] = time

        if version is not None:
            event_pattern["version"] = version

        return jsii.invoke(self, "addEventPattern", [event_pattern])

    @jsii.member(jsii_name="addTarget")
    def add_target(self, target: typing.Optional["IEventRuleTarget"]=None, *, json_template: typing.Any=None, paths_map: typing.Optional[typing.Mapping[str,str]]=None, text_template: typing.Optional[str]=None) -> None:
        """Adds a target to the rule. The abstract class RuleTarget can be extended to define new targets.

        No-op if target is undefined.

        Arguments:
            target: -
            inputOptions: -
            jsonTemplate: Input template where you can use the values of the keys from inputPathsMap to customize the data sent to the target. Enclose each InputPathsMaps value in brackets: This option is mutually exclusive with ``textTemplate``.
            pathsMap: Map of JSON paths to be extracted from the event. These are key-value pairs, where each value is a JSON path. You must use JSON dot notation, not bracket notation.
            textTemplate: Input template where you can use the values of the keys from inputPathsMap to customize the data sent to the target. Enclose each InputPathsMaps value in brackets: The value passed here will be double-quoted to indicate it's a string value. This option is mutually exclusive with ``jsonTemplate``.
        """
        input_options: TargetInputTemplate = {}

        if json_template is not None:
            input_options["jsonTemplate"] = json_template

        if paths_map is not None:
            input_options["pathsMap"] = paths_map

        if text_template is not None:
            input_options["textTemplate"] = text_template

        return jsii.invoke(self, "addTarget", [target, input_options])

    @jsii.member(jsii_name="export")
    def export(self) -> "EventRuleAttributes":
        """Exports this rule resource from this stack and returns an import token."""
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.
        """
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="ruleArn")
    def rule_arn(self) -> str:
        """The value of the event rule Amazon Resource Name (ARN), such as arn:aws:events:us-east-2:123456789012:rule/example."""
        return jsii.get(self, "ruleArn")


@jsii.interface(jsii_type="@aws-cdk/aws-events.IEventRuleTarget")
class IEventRuleTarget(jsii.compat.Protocol):
    """An abstract target for EventRules."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IEventRuleTargetProxy

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, rule_arn: str, rule_unique_id: str) -> "EventRuleTargetProps":
        """Returns the rule target specification. NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        Arguments:
            ruleArn: The ARN of the CloudWatch Event Rule that would trigger this target.
            ruleUniqueId: A unique ID for this rule. Can be used to implement idempotency.
        """
        ...


class _IEventRuleTargetProxy():
    """An abstract target for EventRules."""
    __jsii_type__ = "@aws-cdk/aws-events.IEventRuleTarget"
    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, rule_arn: str, rule_unique_id: str) -> "EventRuleTargetProps":
        """Returns the rule target specification. NOTE: Do not use the various ``inputXxx`` options. They can be set in a call to ``addTarget``.

        Arguments:
            ruleArn: The ARN of the CloudWatch Event Rule that would trigger this target.
            ruleUniqueId: A unique ID for this rule. Can be used to implement idempotency.
        """
        return jsii.invoke(self, "asEventRuleTarget", [rule_arn, rule_unique_id])


@jsii.data_type(jsii_type="@aws-cdk/aws-events.TargetInputTemplate", jsii_struct_bases=[])
class TargetInputTemplate(jsii.compat.TypedDict, total=False):
    """Specifies settings that provide custom input to an Amazon CloudWatch Events rule target based on certain event data.

    See:
        https://docs.aws.amazon.com/AmazonCloudWatchEvents/latest/APIReference/API_InputTransformer.html
    """
    jsonTemplate: typing.Any
    """Input template where you can use the values of the keys from inputPathsMap to customize the data sent to the target.

    Enclose each
    InputPathsMaps value in brackets:

    This option is mutually exclusive with ``textTemplate``.

    Example::
        {
        jsonTemplate: '{ "commands": <commandsToRun> }' ,
        pathsMap: {
        commandsToRun: '$.detail.commands'
        }
        }
    """

    pathsMap: typing.Mapping[str,str]
    """Map of JSON paths to be extracted from the event.

    These are key-value
    pairs, where each value is a JSON path. You must use JSON dot notation,
    not bracket notation.
    """

    textTemplate: str
    """Input template where you can use the values of the keys from inputPathsMap to customize the data sent to the target.

    Enclose each
    InputPathsMaps value in brackets:

    The value passed here will be double-quoted to indicate it's a string value.
    This option is mutually exclusive with ``jsonTemplate``.

    Example::
        {
        textTemplate: 'Build <buildid> started',
        pathsMap: {
        buildid: '$.detail.id'
        }
        }
    """

__all__ = ["CfnEventBusPolicy", "CfnEventBusPolicyProps", "CfnRule", "CfnRuleProps", "EventPattern", "EventRule", "EventRuleAttributes", "EventRuleProps", "EventRuleTargetProps", "IEventRule", "IEventRuleTarget", "TargetInputTemplate", "__jsii_assembly__"]

publication.publish()
