import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_codebuild
import aws_cdk.aws_codepipeline
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_sns
import aws_cdk.aws_stepfunctions
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-events-targets", "0.31.0", __name__, "aws-events-targets@0.31.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_events.IEventRuleTarget)
class CodeBuildProject(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.CodeBuildProject"):
    """Start a CodeBuild build when an AWS CloudWatch events rule is triggered."""
    def __init__(self, project: aws_cdk.aws_codebuild.IProject) -> None:
        """
        Arguments:
            project: -
        """
        jsii.create(CodeBuildProject, self, [project])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        """Allows using build projects as event rule targets.

        Arguments:
            _ruleArn: -
            _ruleId: -
        """
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @property
    @jsii.member(jsii_name="project")
    def project(self) -> aws_cdk.aws_codebuild.IProject:
        return jsii.get(self, "project")


@jsii.implements(aws_cdk.aws_events.IEventRuleTarget)
class LambdaFunction(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.LambdaFunction"):
    """Use an AWS Lambda function as an event rule target."""
    def __init__(self, handler: aws_cdk.aws_lambda.IFunction) -> None:
        """
        Arguments:
            handler: The lambda function.
        """
        jsii.create(LambdaFunction, self, [handler])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, rule_arn: str, rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        """Returns a RuleTarget that can be used to trigger this Lambda as a result from a CloudWatch event.

        Arguments:
            ruleArn: -
            ruleId: -
        """
        return jsii.invoke(self, "asEventRuleTarget", [rule_arn, rule_id])

    @property
    @jsii.member(jsii_name="handler")
    def handler(self) -> aws_cdk.aws_lambda.IFunction:
        """The lambda function."""
        return jsii.get(self, "handler")


@jsii.implements(aws_cdk.aws_events.IEventRuleTarget)
class SnsTopic(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-events-targets.SnsTopic"):
    """Use an SNS topic as a target for AWS CloudWatch event rules.

    Example::
        // publish to an SNS topic every time code is committed
        // to a CodeCommit repository
        repository.onCommit(new targets.SnsTopic(topic));
    """
    def __init__(self, topic: aws_cdk.aws_sns.ITopic) -> None:
        """
        Arguments:
            topic: -
        """
        jsii.create(SnsTopic, self, [topic])

    @jsii.member(jsii_name="asEventRuleTarget")
    def as_event_rule_target(self, _rule_arn: str, _rule_id: str) -> aws_cdk.aws_events.EventRuleTargetProps:
        """Returns a RuleTarget that can be used to trigger this SNS topic as a result from a CloudWatch event.

        Arguments:
            _ruleArn: -
            _ruleId: -

        See:
            https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/resource-based-policies-cwe.html#sns-permissions
        """
        return jsii.invoke(self, "asEventRuleTarget", [_rule_arn, _rule_id])

    @property
    @jsii.member(jsii_name="topic")
    def topic(self) -> aws_cdk.aws_sns.ITopic:
        return jsii.get(self, "topic")


__all__ = ["CodeBuildProject", "LambdaFunction", "SnsTopic", "__jsii_assembly__"]

publication.publish()
