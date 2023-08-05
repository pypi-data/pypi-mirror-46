import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codecommit", "0.31.0", __name__, "aws-codecommit@0.31.0.jsii.tgz")
class CfnRepository(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codecommit.CfnRepository"):
    """A CloudFormation ``AWS::CodeCommit::Repository``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
    cloudformationResource:
        AWS::CodeCommit::Repository
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, repository_name: str, repository_description: typing.Optional[str]=None, triggers: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union["RepositoryTriggerProperty", aws_cdk.cdk.Token]]]]]=None) -> None:
        """Create a new ``AWS::CodeCommit::Repository``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            repositoryName: ``AWS::CodeCommit::Repository.RepositoryName``.
            repositoryDescription: ``AWS::CodeCommit::Repository.RepositoryDescription``.
            triggers: ``AWS::CodeCommit::Repository.Triggers``.
        """
        props: CfnRepositoryProps = {"repositoryName": repository_name}

        if repository_description is not None:
            props["repositoryDescription"] = repository_description

        if triggers is not None:
            props["triggers"] = triggers

        jsii.create(CfnRepository, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRepositoryProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """
        cloudformationAttribute:
            CloneUrlHttp
        """
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """
        cloudformationAttribute:
            CloneUrlSsh
        """
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryId")
    def repository_id(self) -> str:
        return jsii.get(self, "repositoryId")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """
        cloudformationAttribute:
            Name
        """
        return jsii.get(self, "repositoryName")

    @jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.CfnRepository.RepositoryTriggerProperty", jsii_struct_bases=[])
    class RepositoryTriggerProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html
        """
        branches: typing.List[str]
        """``CfnRepository.RepositoryTriggerProperty.Branches``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-branches
        """

        customData: str
        """``CfnRepository.RepositoryTriggerProperty.CustomData``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-customdata
        """

        destinationArn: str
        """``CfnRepository.RepositoryTriggerProperty.DestinationArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-destinationarn
        """

        events: typing.List[str]
        """``CfnRepository.RepositoryTriggerProperty.Events``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-events
        """

        name: str
        """``CfnRepository.RepositoryTriggerProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codecommit-repository-repositorytrigger.html#cfn-codecommit-repository-repositorytrigger-name
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRepositoryProps(jsii.compat.TypedDict, total=False):
    repositoryDescription: str
    """``AWS::CodeCommit::Repository.RepositoryDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositorydescription
    """
    triggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnRepository.RepositoryTriggerProperty", aws_cdk.cdk.Token]]]
    """``AWS::CodeCommit::Repository.Triggers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-triggers
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.CfnRepositoryProps", jsii_struct_bases=[_CfnRepositoryProps])
class CfnRepositoryProps(_CfnRepositoryProps):
    """Properties for defining a ``AWS::CodeCommit::Repository``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html
    """
    repositoryName: str
    """``AWS::CodeCommit::Repository.RepositoryName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-codecommit-repository.html#cfn-codecommit-repository-repositoryname
    """

@jsii.interface(jsii_type="@aws-cdk/aws-codecommit.IRepository")
class IRepository(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRepositoryProxy

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of this Repository.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """The HTTP clone URL.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """The SSH clone URL.

        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The human-visible name of this Repository.

        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryAttributes":
        """Exports this Repository.

        Allows the same Repository to be used in 2 different Stacks.

        See:
            import
        """
        ...

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, branch: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        Arguments:
            name: -
            target: The target of the event.
            branch: The branch to monitor. Defaults to all branches.
        """
        ...

    @jsii.member(jsii_name="onEvent")
    def on_event(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a pull request state is changed.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        ...


class _IRepositoryProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-codecommit.IRepository"
    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of this Repository.

        attribute:
            true
        """
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """The HTTP clone URL.

        attribute:
            true
        """
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """The SSH clone URL.

        attribute:
            true
        """
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The human-visible name of this Repository.

        attribute:
            true
        """
        return jsii.get(self, "repositoryName")

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryAttributes":
        """Exports this Repository.

        Allows the same Repository to be used in 2 different Stacks.

        See:
            import
        """
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnCommit", [name, target, options])

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnPullRequest", [name, target, options])

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, branch: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        Arguments:
            name: -
            target: The target of the event.
            branch: The branch to monitor. Defaults to all branches.
        """
        return jsii.invoke(self, "onCommit", [name, target, branch])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onEvent", [name, target, options])

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a pull request state is changed.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onPullRequestStateChange", [name, target, options])

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceCreated", [name, target, options])

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceDeleted", [name, target, options])

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceUpdated", [name, target, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onStateChange", [name, target, options])


@jsii.implements(IRepository)
class Repository(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-codecommit.Repository"):
    """Provides a CodeCommit Repository."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, repository_name: str, description: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            repositoryName: Name of the repository. This property is required for all repositories.
            description: A description of the repository. Use the description to identify the purpose of the repository.
        """
        props: RepositoryProps = {"repositoryName": repository_name}

        if description is not None:
            props["description"] = description

        jsii.create(Repository, self, [scope, id, props])

    @jsii.member(jsii_name="fromRepositoryArn")
    @classmethod
    def from_repository_arn(cls, scope: aws_cdk.cdk.Construct, id: str, repository_arn: str) -> "IRepository":
        """Imports a codecommit repository.

        Arguments:
            scope: -
            id: -
            repositoryArn: (e.g. ``arn:aws:codecommit:us-east-1:123456789012:MyDemoRepo``).
        """
        return jsii.sinvoke(cls, "fromRepositoryArn", [scope, id, repository_arn])

    @jsii.member(jsii_name="export")
    def export(self) -> "RepositoryAttributes":
        """Exports this Repository.

        Allows the same Repository to be used in 2 different Stacks.

        See:
            import
        """
        return jsii.invoke(self, "export", [])

    @jsii.member(jsii_name="notify")
    def notify(self, arn: str, *, branches: typing.Optional[typing.List[str]]=None, custom_data: typing.Optional[str]=None, events: typing.Optional[typing.List["RepositoryEventTrigger"]]=None, name: typing.Optional[str]=None) -> "Repository":
        """Create a trigger to notify another service to run actions on repository events.

        Arguments:
            arn: Arn of the resource that repository events will notify.
            options: Trigger options to run actions.
            branches: The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger. If you don't specify at least one branch, the trigger applies to all branches.
            customData: When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target.
            events: The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events.
            name: A name for the trigger.Triggers on a repository must have unique names.
        """
        options: RepositoryTriggerOptions = {}

        if branches is not None:
            options["branches"] = branches

        if custom_data is not None:
            options["customData"] = custom_data

        if events is not None:
            options["events"] = events

        if name is not None:
            options["name"] = name

        return jsii.invoke(self, "notify", [arn, options])

    @jsii.member(jsii_name="onCommentOnCommit")
    def on_comment_on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a comment is made on a commit.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnCommit", [name, target, options])

    @jsii.member(jsii_name="onCommentOnPullRequest")
    def on_comment_on_pull_request(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a comment is made on a pull request.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onCommentOnPullRequest", [name, target, options])

    @jsii.member(jsii_name="onCommit")
    def on_commit(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, branch: typing.Optional[str]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a commit is pushed to a branch.

        Arguments:
            name: -
            target: The target of the event.
            branch: The branch to monitor. Defaults to all branches.
        """
        return jsii.invoke(self, "onCommit", [name, target, branch])

    @jsii.member(jsii_name="onEvent")
    def on_event(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers for repository events.

        Use
        ``rule.addEventPattern(pattern)`` to specify a filter.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onEvent", [name, target, options])

    @jsii.member(jsii_name="onPullRequestStateChange")
    def on_pull_request_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a pull request state is changed.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onPullRequestStateChange", [name, target, options])

    @jsii.member(jsii_name="onReferenceCreated")
    def on_reference_created(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is created (i.e. a new branch/tag is created) to the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceCreated", [name, target, options])

    @jsii.member(jsii_name="onReferenceDeleted")
    def on_reference_deleted(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is delete (i.e. a branch/tag is deleted) from the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceDeleted", [name, target, options])

    @jsii.member(jsii_name="onReferenceUpdated")
    def on_reference_updated(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a reference is updated (i.e. a commit is pushed to an existing or new branch) from the repository.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onReferenceUpdated", [name, target, options])

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(self, name: str, target: typing.Optional[aws_cdk.aws_events.IEventRuleTarget]=None, *, description: typing.Optional[str]=None, enabled: typing.Optional[bool]=None, event_pattern: typing.Optional[aws_cdk.aws_events.EventPattern]=None, rule_name: typing.Optional[str]=None, schedule_expression: typing.Optional[str]=None, targets: typing.Optional[typing.List[aws_cdk.aws_events.IEventRuleTarget]]=None) -> aws_cdk.aws_events.EventRule:
        """Defines a CloudWatch event rule which triggers when a "CodeCommit Repository State Change" event occurs.

        Arguments:
            name: -
            target: -
            options: -
            description: A description of the rule's purpose.
            enabled: Indicates whether the rule is enabled. Default: Rule is enabled
            eventPattern: Describes which events CloudWatch Events routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon CloudWatch User Guide.
            ruleName: A name for the rule. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``.
        """
        options: aws_cdk.aws_events.EventRuleProps = {}

        if description is not None:
            options["description"] = description

        if enabled is not None:
            options["enabled"] = enabled

        if event_pattern is not None:
            options["eventPattern"] = event_pattern

        if rule_name is not None:
            options["ruleName"] = rule_name

        if schedule_expression is not None:
            options["scheduleExpression"] = schedule_expression

        if targets is not None:
            options["targets"] = targets

        return jsii.invoke(self, "onStateChange", [name, target, options])

    @property
    @jsii.member(jsii_name="repositoryArn")
    def repository_arn(self) -> str:
        """The ARN of this Repository."""
        return jsii.get(self, "repositoryArn")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlHttp")
    def repository_clone_url_http(self) -> str:
        """The HTTP clone URL."""
        return jsii.get(self, "repositoryCloneUrlHttp")

    @property
    @jsii.member(jsii_name="repositoryCloneUrlSsh")
    def repository_clone_url_ssh(self) -> str:
        """The SSH clone URL."""
        return jsii.get(self, "repositoryCloneUrlSsh")

    @property
    @jsii.member(jsii_name="repositoryName")
    def repository_name(self) -> str:
        """The human-visible name of this Repository."""
        return jsii.get(self, "repositoryName")


@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.RepositoryAttributes", jsii_struct_bases=[])
class RepositoryAttributes(jsii.compat.TypedDict):
    """Properties for the {@link Repository.import} method."""
    repositoryName: str
    """The name of an existing CodeCommit Repository that we are referencing. Must be in the same account and region as the root Stack."""

@jsii.enum(jsii_type="@aws-cdk/aws-codecommit.RepositoryEventTrigger")
class RepositoryEventTrigger(enum.Enum):
    """Repository events that will cause the trigger to run actions in another service."""
    All = "All"
    UpdateRef = "UpdateRef"
    CreateRef = "CreateRef"
    DeleteRef = "DeleteRef"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _RepositoryProps(jsii.compat.TypedDict, total=False):
    description: str
    """A description of the repository.

    Use the description to identify the
    purpose of the repository.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.RepositoryProps", jsii_struct_bases=[_RepositoryProps])
class RepositoryProps(_RepositoryProps):
    repositoryName: str
    """Name of the repository.

    This property is required for all repositories.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-codecommit.RepositoryTriggerOptions", jsii_struct_bases=[])
class RepositoryTriggerOptions(jsii.compat.TypedDict, total=False):
    """Creates for a repository trigger to an SNS topic or Lambda function."""
    branches: typing.List[str]
    """The names of the branches in the AWS CodeCommit repository that contain events that you want to include in the trigger.

    If you don't specify at
    least one branch, the trigger applies to all branches.
    """

    customData: str
    """When an event is triggered, additional information that AWS CodeCommit includes when it sends information to the target."""

    events: typing.List["RepositoryEventTrigger"]
    """The repository events for which AWS CodeCommit sends information to the target, which you specified in the DestinationArn property.If you don't specify events, the trigger runs for all repository events."""

    name: str
    """A name for the trigger.Triggers on a repository must have unique names."""

__all__ = ["CfnRepository", "CfnRepositoryProps", "IRepository", "Repository", "RepositoryAttributes", "RepositoryEventTrigger", "RepositoryProps", "RepositoryTriggerOptions", "__jsii_assembly__"]

publication.publish()
