import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_common
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-applicationautoscaling", "0.32.0", __name__, "aws-applicationautoscaling@0.32.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _AdjustmentTier(jsii.compat.TypedDict, total=False):
    lowerBound: jsii.Number
    """Lower bound where this scaling tier applies.

    The scaling tier applies if the difference between the metric
    value and its alarm threshold is higher than this value.

    Default:
        -Infinity if this is the first tier, otherwise the upperBound of the previous tier
    """
    upperBound: jsii.Number
    """Upper bound where this scaling tier applies.

    The scaling tier applies if the difference between the metric
    value and its alarm threshold is lower than this value.

    Default:
        +Infinity
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.AdjustmentTier", jsii_struct_bases=[_AdjustmentTier])
class AdjustmentTier(_AdjustmentTier):
    """An adjustment."""
    adjustment: jsii.Number
    """What number to adjust the capacity with.

    The number is interpeted as an added capacity, a new fixed capacity or an
    added percentage depending on the AdjustmentType value of the
    StepScalingPolicy.

    Can be positive or negative.
    """

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.AdjustmentType")
class AdjustmentType(enum.Enum):
    """How adjustment numbers are interpreted."""
    ChangeInCapacity = "ChangeInCapacity"
    """Add the adjustment number to the current capacity.

    A positive number increases capacity, a negative number decreases capacity.
    """
    PercentChangeInCapacity = "PercentChangeInCapacity"
    """Add this percentage of the current capacity to itself.

    The number must be between -100 and 100; a positive number increases
    capacity and a negative number decreases it.
    """
    ExactCapacity = "ExactCapacity"
    """Make the capacity equal to the exact number given."""

class BaseScalableAttribute(aws_cdk.cdk.Construct, metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-applicationautoscaling.BaseScalableAttribute"):
    """Represent an attribute for which autoscaling can be configured.

    This class is basically a light wrapper around ScalableTarget, but with
    all methods protected instead of public so they can be selectively
    exposed and/or more specific versions of them can be exposed by derived
    classes for individual services support autoscaling.

    Typical use cases:

    - Hide away the PredefinedMetric enum for target tracking policies.
    - Don't expose all scaling methods (for example Dynamo tables don't support
      Step Scaling, so the Dynamo subclass won't expose this method).
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _BaseScalableAttributeProxy

    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dimension: str, resource_id: str, role: aws_cdk.aws_iam.IRole, service_namespace: "ServiceNamespace", max_capacity: jsii.Number, min_capacity: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            dimension: Scalable dimension of the attribute.
            resourceId: Resource ID of the attribute.
            role: Role to use for scaling.
            serviceNamespace: Service namespace of the scalable attribute.
            maxCapacity: Maximum capacity to scale to.
            minCapacity: Minimum capacity to scale to. Default: 1
        """
        props: BaseScalableAttributeProps = {"dimension": dimension, "resourceId": resource_id, "role": role, "serviceNamespace": service_namespace, "maxCapacity": max_capacity}

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        jsii.create(BaseScalableAttribute, self, [scope, id, props])

    @jsii.member(jsii_name="doScaleOnMetric")
    def _do_scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """Scale out or in based on a metric value.

        Arguments:
            id: -
            props: -
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSec: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "doScaleOnMetric", [id, props])

    @jsii.member(jsii_name="doScaleOnSchedule")
    def _do_scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scale out or in based on time.

        Arguments:
            id: -
            props: -
            schedule: When to perform this action. Support formats: - at(yyyy-mm-ddThh:mm:ss) - rate(value unit) - cron(fields) "At" expressions are useful for one-time schedules. Specify the time in UTC. For "rate" expressions, value is a positive integer, and unit is minute, minutes, hour, hours, day, or days. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
            endTime: When this scheduled action expires. Default: The rule never expires.
            maxCapacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
            minCapacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
            startTime: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        props: ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "doScaleOnSchedule", [id, props])

    @jsii.member(jsii_name="doScaleToTrackMetric")
    def _do_scale_to_track_metric(self, id: str, *, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        """Scale out or in in order to keep a metric around a target value.

        Arguments:
            id: -
            props: -
            targetValue: The target value for the metric.
            customMetric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
            predefinedMetric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
            resourceLabel: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policyName: A name for the scaling policy. Default: - Automatically generated name.
            scaleInCooldownSec: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scaleOutCooldownSec: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props: BasicTargetTrackingScalingPolicyProps = {"targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "doScaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="props")
    def _props(self) -> "BaseScalableAttributeProps":
        return jsii.get(self, "props")


class _BaseScalableAttributeProxy(BaseScalableAttribute):
    pass

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BaseTargetTrackingProps", jsii_struct_bases=[])
class BaseTargetTrackingProps(jsii.compat.TypedDict, total=False):
    """Base interface for target tracking props.

    Contains the attributes that are common to target tracking policies,
    except the ones relating to the metric and to the scalable target.

    This interface is reused by more specific target tracking props objects
    in other services.
    """
    disableScaleIn: bool
    """Indicates whether scale in by the target tracking policy is disabled.

    If the value is true, scale in is disabled and the target tracking policy
    won't remove capacity from the scalable resource. Otherwise, scale in is
    enabled and the target tracking policy can remove capacity from the
    scalable resource.

    Default:
        false
    """

    policyName: str
    """A name for the scaling policy.

    Default:
        - Automatically generated name.
    """

    scaleInCooldownSec: jsii.Number
    """Period after a scale in activity completes before another scale in activity can start.

    Default:
        - No scale in cooldown.
    """

    scaleOutCooldownSec: jsii.Number
    """Period after a scale out activity completes before another scale out activity can start.

    Default:
        - No scale out cooldown.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BasicStepScalingPolicyProps(jsii.compat.TypedDict, total=False):
    adjustmentType: "AdjustmentType"
    """How the adjustment numbers inside 'intervals' are interpreted.

    Default:
        ChangeInCapacity
    """
    cooldownSec: jsii.Number
    """Grace period after scaling activity.

    Subsequent scale outs during the cooldown period are squashed so that only
    the biggest scale out happens.

    Subsequent scale ins during the cooldown period are ignored.

    Default:
        No cooldown period

    See:
        https://docs.aws.amazon.com/autoscaling/application/APIReference/API_StepScalingPolicyConfiguration.html
    """
    minAdjustmentMagnitude: jsii.Number
    """Minimum absolute number to adjust capacity with as result of percentage scaling.

    Only when using AdjustmentType = PercentChangeInCapacity, this number controls
    the minimum absolute effect size.

    Default:
        No minimum scaling effect
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BasicStepScalingPolicyProps", jsii_struct_bases=[_BasicStepScalingPolicyProps])
class BasicStepScalingPolicyProps(_BasicStepScalingPolicyProps):
    metric: aws_cdk.aws_cloudwatch.Metric
    """Metric to scale on."""

    scalingSteps: typing.List["ScalingInterval"]
    """The intervals for scaling.

    Maps a range of metric values to a particular scaling behavior.
    """

@jsii.data_type_optionals(jsii_struct_bases=[BaseTargetTrackingProps])
class _BasicTargetTrackingScalingPolicyProps(BaseTargetTrackingProps, jsii.compat.TypedDict, total=False):
    customMetric: aws_cdk.aws_cloudwatch.Metric
    """A custom metric for application autoscaling.

    The metric must track utilization. Scaling out will happen if the metric is higher than
    the target value, scaling in will happen in the metric is lower than the target value.

    Exactly one of customMetric or predefinedMetric must be specified.

    Default:
        - No custom metric.
    """
    predefinedMetric: "PredefinedMetric"
    """A predefined metric for application autoscaling.

    The metric must track utilization. Scaling out will happen if the metric is higher than
    the target value, scaling in will happen in the metric is lower than the target value.

    Exactly one of customMetric or predefinedMetric must be specified.

    Default:
        - No predefined metrics.
    """
    resourceLabel: str
    """Identify the resource associated with the metric type.

    Only used for predefined metric ALBRequestCountPerTarget.

    Default:
        - No resource label.

    Example::
        app/<load-balancer-name>/<load-balancer-id>/targetgroup/<target-group-name>/<target-group-id>
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BasicTargetTrackingScalingPolicyProps", jsii_struct_bases=[_BasicTargetTrackingScalingPolicyProps])
class BasicTargetTrackingScalingPolicyProps(_BasicTargetTrackingScalingPolicyProps):
    """Properties for a Target Tracking policy that include the metric but exclude the target."""
    targetValue: jsii.Number
    """The target value for the metric."""

class CfnScalableTarget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget"):
    """A CloudFormation ``AWS::ApplicationAutoScaling::ScalableTarget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html
    cloudformationResource:
        AWS::ApplicationAutoScaling::ScalableTarget
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_capacity: typing.Union[jsii.Number, aws_cdk.cdk.Token], min_capacity: typing.Union[jsii.Number, aws_cdk.cdk.Token], resource_id: str, role_arn: str, scalable_dimension: str, service_namespace: str, scheduled_actions: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ScheduledActionProperty"]]]]]=None) -> None:
        """Create a new ``AWS::ApplicationAutoScaling::ScalableTarget``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            maxCapacity: ``AWS::ApplicationAutoScaling::ScalableTarget.MaxCapacity``.
            minCapacity: ``AWS::ApplicationAutoScaling::ScalableTarget.MinCapacity``.
            resourceId: ``AWS::ApplicationAutoScaling::ScalableTarget.ResourceId``.
            roleArn: ``AWS::ApplicationAutoScaling::ScalableTarget.RoleARN``.
            scalableDimension: ``AWS::ApplicationAutoScaling::ScalableTarget.ScalableDimension``.
            serviceNamespace: ``AWS::ApplicationAutoScaling::ScalableTarget.ServiceNamespace``.
            scheduledActions: ``AWS::ApplicationAutoScaling::ScalableTarget.ScheduledActions``.
        """
        props: CfnScalableTargetProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity, "resourceId": resource_id, "roleArn": role_arn, "scalableDimension": scalable_dimension, "serviceNamespace": service_namespace}

        if scheduled_actions is not None:
            props["scheduledActions"] = scheduled_actions

        jsii.create(CfnScalableTarget, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnScalableTargetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        return jsii.get(self, "scalableTargetId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.ScalableTargetActionProperty", jsii_struct_bases=[])
    class ScalableTargetActionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html
        """
        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalableTarget.ScalableTargetActionProperty.MaxCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html#cfn-applicationautoscaling-scalabletarget-scalabletargetaction-maxcapacity
        """

        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalableTarget.ScalableTargetActionProperty.MinCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scalabletargetaction.html#cfn-applicationautoscaling-scalabletarget-scalabletargetaction-mincapacity
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ScheduledActionProperty(jsii.compat.TypedDict, total=False):
        endTime: typing.Union[aws_cdk.cdk.Token, datetime.datetime]
        """``CfnScalableTarget.ScheduledActionProperty.EndTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-endtime
        """
        scalableTargetAction: typing.Union[aws_cdk.cdk.Token, "CfnScalableTarget.ScalableTargetActionProperty"]
        """``CfnScalableTarget.ScheduledActionProperty.ScalableTargetAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-scalabletargetaction
        """
        startTime: typing.Union[aws_cdk.cdk.Token, datetime.datetime]
        """``CfnScalableTarget.ScheduledActionProperty.StartTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-starttime
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTarget.ScheduledActionProperty", jsii_struct_bases=[_ScheduledActionProperty])
    class ScheduledActionProperty(_ScheduledActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html
        """
        schedule: str
        """``CfnScalableTarget.ScheduledActionProperty.Schedule``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-schedule
        """

        scheduledActionName: str
        """``CfnScalableTarget.ScheduledActionProperty.ScheduledActionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalabletarget-scheduledaction.html#cfn-applicationautoscaling-scalabletarget-scheduledaction-scheduledactionname
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnScalableTargetProps(jsii.compat.TypedDict, total=False):
    scheduledActions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalableTarget.ScheduledActionProperty"]]]
    """``AWS::ApplicationAutoScaling::ScalableTarget.ScheduledActions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scheduledactions
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalableTargetProps", jsii_struct_bases=[_CfnScalableTargetProps])
class CfnScalableTargetProps(_CfnScalableTargetProps):
    """Properties for defining a ``AWS::ApplicationAutoScaling::ScalableTarget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html
    """
    maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ApplicationAutoScaling::ScalableTarget.MaxCapacity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-maxcapacity
    """

    minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::ApplicationAutoScaling::ScalableTarget.MinCapacity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-mincapacity
    """

    resourceId: str
    """``AWS::ApplicationAutoScaling::ScalableTarget.ResourceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-resourceid
    """

    roleArn: str
    """``AWS::ApplicationAutoScaling::ScalableTarget.RoleARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-rolearn
    """

    scalableDimension: str
    """``AWS::ApplicationAutoScaling::ScalableTarget.ScalableDimension``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-scalabledimension
    """

    serviceNamespace: str
    """``AWS::ApplicationAutoScaling::ScalableTarget.ServiceNamespace``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalabletarget.html#cfn-applicationautoscaling-scalabletarget-servicenamespace
    """

class CfnScalingPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy"):
    """A CloudFormation ``AWS::ApplicationAutoScaling::ScalingPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html
    cloudformationResource:
        AWS::ApplicationAutoScaling::ScalingPolicy
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, policy_name: str, policy_type: str, resource_id: typing.Optional[str]=None, scalable_dimension: typing.Optional[str]=None, scaling_target_id: typing.Optional[str]=None, service_namespace: typing.Optional[str]=None, step_scaling_policy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["StepScalingPolicyConfigurationProperty"]]]=None, target_tracking_scaling_policy_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["TargetTrackingScalingPolicyConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::ApplicationAutoScaling::ScalingPolicy``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            policyName: ``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyName``.
            policyType: ``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyType``.
            resourceId: ``AWS::ApplicationAutoScaling::ScalingPolicy.ResourceId``.
            scalableDimension: ``AWS::ApplicationAutoScaling::ScalingPolicy.ScalableDimension``.
            scalingTargetId: ``AWS::ApplicationAutoScaling::ScalingPolicy.ScalingTargetId``.
            serviceNamespace: ``AWS::ApplicationAutoScaling::ScalingPolicy.ServiceNamespace``.
            stepScalingPolicyConfiguration: ``AWS::ApplicationAutoScaling::ScalingPolicy.StepScalingPolicyConfiguration``.
            targetTrackingScalingPolicyConfiguration: ``AWS::ApplicationAutoScaling::ScalingPolicy.TargetTrackingScalingPolicyConfiguration``.
        """
        props: CfnScalingPolicyProps = {"policyName": policy_name, "policyType": policy_type}

        if resource_id is not None:
            props["resourceId"] = resource_id

        if scalable_dimension is not None:
            props["scalableDimension"] = scalable_dimension

        if scaling_target_id is not None:
            props["scalingTargetId"] = scaling_target_id

        if service_namespace is not None:
            props["serviceNamespace"] = service_namespace

        if step_scaling_policy_configuration is not None:
            props["stepScalingPolicyConfiguration"] = step_scaling_policy_configuration

        if target_tracking_scaling_policy_configuration is not None:
            props["targetTrackingScalingPolicyConfiguration"] = target_tracking_scaling_policy_configuration

        jsii.create(CfnScalingPolicy, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnScalingPolicyProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        return jsii.get(self, "scalingPolicyArn")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CustomizedMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.MetricDimensionProperty"]]]
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Dimensions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-dimensions
        """
        unit: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-unit
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty", jsii_struct_bases=[_CustomizedMetricSpecificationProperty])
    class CustomizedMetricSpecificationProperty(_CustomizedMetricSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html
        """
        metricName: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-metricname
        """

        namespace: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-namespace
        """

        statistic: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-customizedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-customizedmetricspecification-statistic
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.MetricDimensionProperty", jsii_struct_bases=[])
    class MetricDimensionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html
        """
        name: str
        """``CfnScalingPolicy.MetricDimensionProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html#cfn-applicationautoscaling-scalingpolicy-metricdimension-name
        """

        value: str
        """``CfnScalingPolicy.MetricDimensionProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-metricdimension.html#cfn-applicationautoscaling-scalingpolicy-metricdimension-value
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _PredefinedMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceLabel: str
        """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty", jsii_struct_bases=[_PredefinedMetricSpecificationProperty])
    class PredefinedMetricSpecificationProperty(_PredefinedMetricSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html
        """
        predefinedMetricType: str
        """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-applicationautoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StepAdjustmentProperty(jsii.compat.TypedDict, total=False):
        metricIntervalLowerBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment-metricintervallowerbound
        """
        metricIntervalUpperBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment-metricintervalupperbound
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.StepAdjustmentProperty", jsii_struct_bases=[_StepAdjustmentProperty])
    class StepAdjustmentProperty(_StepAdjustmentProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html
        """
        scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustment-scalingadjustment
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.StepScalingPolicyConfigurationProperty", jsii_struct_bases=[])
    class StepScalingPolicyConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html
        """
        adjustmentType: str
        """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.AdjustmentType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-adjustmenttype
        """

        cooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.Cooldown``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-cooldown
        """

        metricAggregationType: str
        """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.MetricAggregationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-metricaggregationtype
        """

        minAdjustmentMagnitude: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.MinAdjustmentMagnitude``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-minadjustmentmagnitude
        """

        stepAdjustments: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.StepAdjustmentProperty"]]]
        """``CfnScalingPolicy.StepScalingPolicyConfigurationProperty.StepAdjustments``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration-stepadjustments
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TargetTrackingScalingPolicyConfigurationProperty(jsii.compat.TypedDict, total=False):
        customizedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.CustomizedMetricSpecificationProperty"]
        """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.CustomizedMetricSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-customizedmetricspecification
        """
        disableScaleIn: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.DisableScaleIn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-disablescalein
        """
        predefinedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.PredefinedMetricSpecificationProperty"]
        """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.PredefinedMetricSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-predefinedmetricspecification
        """
        scaleInCooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.ScaleInCooldown``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-scaleincooldown
        """
        scaleOutCooldown: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.ScaleOutCooldown``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-scaleoutcooldown
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty", jsii_struct_bases=[_TargetTrackingScalingPolicyConfigurationProperty])
    class TargetTrackingScalingPolicyConfigurationProperty(_TargetTrackingScalingPolicyConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html
        """
        targetValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty.TargetValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration-targetvalue
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnScalingPolicyProps(jsii.compat.TypedDict, total=False):
    resourceId: str
    """``AWS::ApplicationAutoScaling::ScalingPolicy.ResourceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-resourceid
    """
    scalableDimension: str
    """``AWS::ApplicationAutoScaling::ScalingPolicy.ScalableDimension``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalabledimension
    """
    scalingTargetId: str
    """``AWS::ApplicationAutoScaling::ScalingPolicy.ScalingTargetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-scalingtargetid
    """
    serviceNamespace: str
    """``AWS::ApplicationAutoScaling::ScalingPolicy.ServiceNamespace``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-servicenamespace
    """
    stepScalingPolicyConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.StepScalingPolicyConfigurationProperty"]
    """``AWS::ApplicationAutoScaling::ScalingPolicy.StepScalingPolicyConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-stepscalingpolicyconfiguration
    """
    targetTrackingScalingPolicyConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.TargetTrackingScalingPolicyConfigurationProperty"]
    """``AWS::ApplicationAutoScaling::ScalingPolicy.TargetTrackingScalingPolicyConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-targettrackingscalingpolicyconfiguration
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.CfnScalingPolicyProps", jsii_struct_bases=[_CfnScalingPolicyProps])
class CfnScalingPolicyProps(_CfnScalingPolicyProps):
    """Properties for defining a ``AWS::ApplicationAutoScaling::ScalingPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html
    """
    policyName: str
    """``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policyname
    """

    policyType: str
    """``AWS::ApplicationAutoScaling::ScalingPolicy.PolicyType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-applicationautoscaling-scalingpolicy.html#cfn-applicationautoscaling-scalingpolicy-policytype
    """

class Cron(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.Cron"):
    """Helper class to generate Cron expressions."""
    def __init__(self) -> None:
        jsii.create(Cron, self, [])

    @jsii.member(jsii_name="dailyUtc")
    @classmethod
    def daily_utc(cls, hour: jsii.Number, minute: typing.Optional[jsii.Number]=None) -> str:
        """Return a cron expression to run every day at a particular time.

        The time is specified in UTC.

        Arguments:
            hour: The hour in UTC to schedule this action.
            minute: The minute in the our to schedule this action (defaults to 0).
        """
        return jsii.sinvoke(cls, "dailyUtc", [hour, minute])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _EnableScalingProps(jsii.compat.TypedDict, total=False):
    minCapacity: jsii.Number
    """Minimum capacity to scale to.

    Default:
        1
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.EnableScalingProps", jsii_struct_bases=[_EnableScalingProps])
class EnableScalingProps(_EnableScalingProps):
    """Properties for enabling DynamoDB capacity scaling."""
    maxCapacity: jsii.Number
    """Maximum capacity to scale to."""

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.BaseScalableAttributeProps", jsii_struct_bases=[EnableScalingProps])
class BaseScalableAttributeProps(EnableScalingProps, jsii.compat.TypedDict):
    """Properties for a ScalableTableAttribute."""
    dimension: str
    """Scalable dimension of the attribute."""

    resourceId: str
    """Resource ID of the attribute."""

    role: aws_cdk.aws_iam.IRole
    """Role to use for scaling."""

    serviceNamespace: "ServiceNamespace"
    """Service namespace of the scalable attribute."""

@jsii.interface(jsii_type="@aws-cdk/aws-applicationautoscaling.IScalableTarget")
class IScalableTarget(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IScalableTargetProxy

    @property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        """
        attribute:
            true
        """
        ...


class _IScalableTargetProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-applicationautoscaling.IScalableTarget"
    @property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "scalableTargetId")


@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    """How the scaling metric is going to be aggregated."""
    Average = "Average"
    """Average."""
    Minimum = "Minimum"
    """Minimum."""
    Maximum = "Maximum"
    """Maximum."""

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    """One of the predefined autoscaling metrics."""
    DynamoDBReadCapacityUtilization = "DynamoDBReadCapacityUtilization"
    DynamoDBWriteCapacityUtilization = "DynamoDBWriteCapacityUtilization"
    ALBRequestCountPerTarget = "ALBRequestCountPerTarget"
    RDSReaderAverageCPUUtilization = "RDSReaderAverageCPUUtilization"
    RDSReaderAverageDatabaseConnections = "RDSReaderAverageDatabaseConnections"
    EC2SpotFleetRequestAverageCPUUtilization = "EC2SpotFleetRequestAverageCPUUtilization"
    EC2SpotFleetRequestAverageNetworkIn = "EC2SpotFleetRequestAverageNetworkIn"
    EC2SpotFleetRequestAverageNetworkOut = "EC2SpotFleetRequestAverageNetworkOut"
    SageMakerVariantInvocationsPerInstance = "SageMakerVariantInvocationsPerInstance"
    ECSServiceAverageCPUUtilization = "ECSServiceAverageCPUUtilization"
    ECSServiceAverageMemoryUtilization = "ECSServiceAverageMemoryUtilization"

@jsii.implements(IScalableTarget)
class ScalableTarget(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.ScalableTarget"):
    """Define a scalable target."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_capacity: jsii.Number, min_capacity: jsii.Number, resource_id: str, scalable_dimension: str, service_namespace: "ServiceNamespace", role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            maxCapacity: The maximum value that Application Auto Scaling can use to scale a target during a scaling activity.
            minCapacity: The minimum value that Application Auto Scaling can use to scale a target during a scaling activity.
            resourceId: The resource identifier to associate with this scalable target. This string consists of the resource type and unique identifier.
            scalableDimension: The scalable dimension that's associated with the scalable target. Specify the service namespace, resource type, and scaling property.
            serviceNamespace: The namespace of the AWS service that provides the resource or custom-resource for a resource provided by your own application or service. For valid AWS service namespace values, see the RegisterScalableTarget action in the Application Auto Scaling API Reference.
            role: Role that allows Application Auto Scaling to modify your scalable target. Default: A role is automatically created
        """
        props: ScalableTargetProps = {"maxCapacity": max_capacity, "minCapacity": min_capacity, "resourceId": resource_id, "scalableDimension": scalable_dimension, "serviceNamespace": service_namespace}

        if role is not None:
            props["role"] = role

        jsii.create(ScalableTarget, self, [scope, id, props])

    @jsii.member(jsii_name="fromScalableTargetId")
    @classmethod
    def from_scalable_target_id(cls, scope: aws_cdk.cdk.Construct, id: str, scalable_target_id: str) -> "IScalableTarget":
        """
        Arguments:
            scope: -
            id: -
            scalableTargetId: -
        """
        return jsii.sinvoke(cls, "fromScalableTargetId", [scope, id, scalable_target_id])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Add a policy statement to the role's policy.

        Arguments:
            statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        Arguments:
            id: -
            props: -
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSec: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """Scale out or in based on time.

        Arguments:
            id: -
            action: -
            schedule: When to perform this action. Support formats: - at(yyyy-mm-ddThh:mm:ss) - rate(value unit) - cron(fields) "At" expressions are useful for one-time schedules. Specify the time in UTC. For "rate" expressions, value is a positive integer, and unit is minute, minutes, hour, hours, day, or days. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
            endTime: When this scheduled action expires. Default: The rule never expires.
            maxCapacity: The new maximum capacity. During the scheduled time, the current capacity is above the maximum capacity, Application Auto Scaling scales in to the maximum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new maximum capacity
            minCapacity: The new minimum capacity. During the scheduled time, if the current capacity is below the minimum capacity, Application Auto Scaling scales out to the minimum capacity. At least one of maxCapacity and minCapacity must be supplied. Default: No new minimum capacity
            startTime: When this scheduled action becomes active. Default: The rule is activate immediately
        """
        action: ScalingSchedule = {"schedule": schedule}

        if end_time is not None:
            action["endTime"] = end_time

        if max_capacity is not None:
            action["maxCapacity"] = max_capacity

        if min_capacity is not None:
            action["minCapacity"] = min_capacity

        if start_time is not None:
            action["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, action])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        Arguments:
            id: -
            props: -
            targetValue: The target value for the metric.
            customMetric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
            predefinedMetric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
            resourceLabel: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policyName: A name for the scaling policy. Default: - Automatically generated name.
            scaleInCooldownSec: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scaleOutCooldownSec: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props: BasicTargetTrackingScalingPolicyProps = {"targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role used to give AutoScaling permissions to your resource."""
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="scalableTargetId")
    def scalable_target_id(self) -> str:
        """ID of the Scalable Target.

        attribute:
            true

        Example::
            service/ecsStack-MyECSCluster-AB12CDE3F4GH/ecsStack-MyECSService-AB12CDE3F4GH|ecs:service:DesiredCount|ecs
        """
        return jsii.get(self, "scalableTargetId")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ScalableTargetProps(jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.IRole
    """Role that allows Application Auto Scaling to modify your scalable target.

    Default:
        A role is automatically created
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalableTargetProps", jsii_struct_bases=[_ScalableTargetProps])
class ScalableTargetProps(_ScalableTargetProps):
    """Properties for a scalable target."""
    maxCapacity: jsii.Number
    """The maximum value that Application Auto Scaling can use to scale a target during a scaling activity."""

    minCapacity: jsii.Number
    """The minimum value that Application Auto Scaling can use to scale a target during a scaling activity."""

    resourceId: str
    """The resource identifier to associate with this scalable target.

    This string consists of the resource type and unique identifier.

    See:
        https://docs.aws.amazon.com/autoscaling/application/APIReference/API_RegisterScalableTarget.html

    Example::
        service/ecsStack-MyECSCluster-AB12CDE3F4GH/ecsStack-MyECSService-AB12CDE3F4GH
    """

    scalableDimension: str
    """The scalable dimension that's associated with the scalable target.

    Specify the service namespace, resource type, and scaling property.

    See:
        https://docs.aws.amazon.com/autoscaling/application/APIReference/API_ScalingPolicy.html

    Example::
        ecs:service:DesiredCount
    """

    serviceNamespace: "ServiceNamespace"
    """The namespace of the AWS service that provides the resource or custom-resource for a resource provided by your own application or service.

    For valid AWS service namespace values, see the RegisterScalableTarget
    action in the Application Auto Scaling API Reference.

    See:
        https://docs.aws.amazon.com/autoscaling/application/APIReference/API_RegisterScalableTarget.html
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ScalingInterval(jsii.compat.TypedDict, total=False):
    lower: jsii.Number
    """The lower bound of the interval.

    The scaling adjustment will be applied if the metric is higher than this value.

    Default:
        Threshold automatically derived from neighbouring intervals
    """
    upper: jsii.Number
    """The upper bound of the interval.

    The scaling adjustment will be applied if the metric is lower than this value.

    Default:
        Threshold automatically derived from neighbouring intervals
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalingInterval", jsii_struct_bases=[_ScalingInterval])
class ScalingInterval(_ScalingInterval):
    """A range of metric values in which to apply a certain scaling operation."""
    change: jsii.Number
    """The capacity adjustment to apply in this interval.

    The number is interpreted differently based on AdjustmentType:

    - ChangeInCapacity: add the adjustment to the current capacity.
      The number can be positive or negative.
    - PercentChangeInCapacity: add or remove the given percentage of the current
      capacity to itself. The number can be in the range [-100..100].
    - ExactCapacity: set the capacity to this number. The number must
      be positive.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ScalingSchedule(jsii.compat.TypedDict, total=False):
    endTime: datetime.datetime
    """When this scheduled action expires.

    Default:
        The rule never expires.
    """
    maxCapacity: jsii.Number
    """The new maximum capacity.

    During the scheduled time, the current capacity is above the maximum
    capacity, Application Auto Scaling scales in to the maximum capacity.

    At least one of maxCapacity and minCapacity must be supplied.

    Default:
        No new maximum capacity
    """
    minCapacity: jsii.Number
    """The new minimum capacity.

    During the scheduled time, if the current capacity is below the minimum
    capacity, Application Auto Scaling scales out to the minimum capacity.

    At least one of maxCapacity and minCapacity must be supplied.

    Default:
        No new minimum capacity
    """
    startTime: datetime.datetime
    """When this scheduled action becomes active.

    Default:
        The rule is activate immediately
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.ScalingSchedule", jsii_struct_bases=[_ScalingSchedule])
class ScalingSchedule(_ScalingSchedule):
    """A scheduled scaling action."""
    schedule: str
    """When to perform this action.

    Support formats:

    - at(yyyy-mm-ddThh:mm:ss)
    - rate(value unit)
    - cron(fields)

    "At" expressions are useful for one-time schedules. Specify the time in
    UTC.

    For "rate" expressions, value is a positive integer, and unit is minute,
    minutes, hour, hours, day, or days.

    For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.

    Example::
        rate(12 hours)
    """

@jsii.enum(jsii_type="@aws-cdk/aws-applicationautoscaling.ServiceNamespace")
class ServiceNamespace(enum.Enum):
    """The service that supports Application AutoScaling."""
    Ecs = "Ecs"
    """Elastic Container Service."""
    ElasticMapReduce = "ElasticMapReduce"
    """Elastic Map Reduce."""
    Ec2 = "Ec2"
    """Elastic Compute Cloud."""
    AppStream = "AppStream"
    """App Stream."""
    DynamoDb = "DynamoDb"
    """Dynamo DB."""
    Rds = "Rds"
    """Relational Database Service."""
    SageMaker = "SageMaker"
    """SageMaker."""
    CustomResource = "CustomResource"
    """Custom Resource."""

@jsii.implements(aws_cdk.aws_cloudwatch.IAlarmAction)
class StepScalingAction(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingAction"):
    """Define a step scaling action.

    This kind of scaling policy adjusts the target capacity in configurable
    steps. The size of the step is configurable based on the metric's distance
    to its alarm threshold.

    This Action must be used as the target of a CloudWatch alarm to take effect.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, scaling_target: "IScalableTarget", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None, policy_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            scalingTarget: The scalable target.
            adjustmentType: How the adjustment numbers are interpreted. Default: ChangeInCapacity
            cooldownSec: Grace period after scaling activity. For scale out policies, multiple scale outs during the cooldown period are squashed so that only the biggest scale out happens. For scale in policies, subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
            metricAggregationType: The aggregation type for the CloudWatch metrics. Default: Average
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
            policyName: A name for the scaling policy. Default: Automatically generated name
        """
        props: StepScalingActionProps = {"scalingTarget": scaling_target}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if metric_aggregation_type is not None:
            props["metricAggregationType"] = metric_aggregation_type

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        if policy_name is not None:
            props["policyName"] = policy_name

        jsii.create(StepScalingAction, self, [scope, id, props])

    @jsii.member(jsii_name="addAdjustment")
    def add_adjustment(self, *, adjustment: jsii.Number, lower_bound: typing.Optional[jsii.Number]=None, upper_bound: typing.Optional[jsii.Number]=None) -> None:
        """Add an adjusment interval to the ScalingAction.

        Arguments:
            adjustment: -
            adjustment: What number to adjust the capacity with. The number is interpeted as an added capacity, a new fixed capacity or an added percentage depending on the AdjustmentType value of the StepScalingPolicy. Can be positive or negative.
            lowerBound: Lower bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is higher than this value. Default: -Infinity if this is the first tier, otherwise the upperBound of the previous tier
            upperBound: Upper bound where this scaling tier applies. The scaling tier applies if the difference between the metric value and its alarm threshold is lower than this value. Default: +Infinity
        """
        adjustment: AdjustmentTier = {"adjustment": adjustment}

        if lower_bound is not None:
            adjustment["lowerBound"] = lower_bound

        if upper_bound is not None:
            adjustment["upperBound"] = upper_bound

        return jsii.invoke(self, "addAdjustment", [adjustment])

    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        """ARN when this scaling policy is used as an Alarm action."""
        return jsii.get(self, "alarmActionArn")

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _StepScalingActionProps(jsii.compat.TypedDict, total=False):
    adjustmentType: "AdjustmentType"
    """How the adjustment numbers are interpreted.

    Default:
        ChangeInCapacity
    """
    cooldownSec: jsii.Number
    """Grace period after scaling activity.

    For scale out policies, multiple scale outs during the cooldown period are
    squashed so that only the biggest scale out happens.

    For scale in policies, subsequent scale ins during the cooldown period are
    ignored.

    Default:
        No cooldown period

    See:
        https://docs.aws.amazon.com/autoscaling/application/APIReference/API_StepScalingPolicyConfiguration.html
    """
    metricAggregationType: "MetricAggregationType"
    """The aggregation type for the CloudWatch metrics.

    Default:
        Average
    """
    minAdjustmentMagnitude: jsii.Number
    """Minimum absolute number to adjust capacity with as result of percentage scaling.

    Only when using AdjustmentType = PercentChangeInCapacity, this number controls
    the minimum absolute effect size.

    Default:
        No minimum scaling effect
    """
    policyName: str
    """A name for the scaling policy.

    Default:
        Automatically generated name
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingActionProps", jsii_struct_bases=[_StepScalingActionProps])
class StepScalingActionProps(_StepScalingActionProps):
    """Properties for a scaling policy."""
    scalingTarget: "IScalableTarget"
    """The scalable target."""

class StepScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingPolicy"):
    """Define a acaling strategy which scales depending on absolute values of some metric.

    You can specify the scaling behavior for various values of the metric.

    Implemented using one or more CloudWatch alarms and Step Scaling Policies.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, scaling_target: "IScalableTarget", metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_sec: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            scalingTarget: The scaling target.
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSec: Grace period after scaling activity. Subsequent scale outs during the cooldown period are squashed so that only the biggest scale out happens. Subsequent scale ins during the cooldown period are ignored. Default: No cooldown period
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: StepScalingPolicyProps = {"scalingTarget": scaling_target, "metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_sec is not None:
            props["cooldownSec"] = cooldown_sec

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        jsii.create(StepScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="lowerAction")
    def lower_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "lowerAction")

    @property
    @jsii.member(jsii_name="lowerAlarm")
    def lower_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "lowerAlarm")

    @property
    @jsii.member(jsii_name="upperAction")
    def upper_action(self) -> typing.Optional["StepScalingAction"]:
        return jsii.get(self, "upperAction")

    @property
    @jsii.member(jsii_name="upperAlarm")
    def upper_alarm(self) -> typing.Optional[aws_cdk.aws_cloudwatch.Alarm]:
        return jsii.get(self, "upperAlarm")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.StepScalingPolicyProps", jsii_struct_bases=[BasicStepScalingPolicyProps])
class StepScalingPolicyProps(BasicStepScalingPolicyProps, jsii.compat.TypedDict):
    scalingTarget: "IScalableTarget"
    """The scaling target."""

class TargetTrackingScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-applicationautoscaling.TargetTrackingScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, scaling_target: "IScalableTarget", target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, disable_scale_in: typing.Optional[bool]=None, policy_name: typing.Optional[str]=None, scale_in_cooldown_sec: typing.Optional[jsii.Number]=None, scale_out_cooldown_sec: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            scalingTarget: -
            targetValue: The target value for the metric.
            customMetric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
            predefinedMetric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metrics.
            resourceLabel: Identify the resource associated with the metric type. Only used for predefined metric ALBRequestCountPerTarget. Default: - No resource label.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the scalable resource. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the scalable resource. Default: false
            policyName: A name for the scaling policy. Default: - Automatically generated name.
            scaleInCooldownSec: Period after a scale in activity completes before another scale in activity can start. Default: - No scale in cooldown.
            scaleOutCooldownSec: Period after a scale out activity completes before another scale out activity can start. Default: - No scale out cooldown.
        """
        props: TargetTrackingScalingPolicyProps = {"scalingTarget": scaling_target, "targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if policy_name is not None:
            props["policyName"] = policy_name

        if scale_in_cooldown_sec is not None:
            props["scaleInCooldownSec"] = scale_in_cooldown_sec

        if scale_out_cooldown_sec is not None:
            props["scaleOutCooldownSec"] = scale_out_cooldown_sec

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-applicationautoscaling.TargetTrackingScalingPolicyProps", jsii_struct_bases=[BasicTargetTrackingScalingPolicyProps])
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps, jsii.compat.TypedDict):
    """Properties for a concrete TargetTrackingPolicy.

    Adds the scalingTarget.
    """
    scalingTarget: "IScalableTarget"

__all__ = ["AdjustmentTier", "AdjustmentType", "BaseScalableAttribute", "BaseScalableAttributeProps", "BaseTargetTrackingProps", "BasicStepScalingPolicyProps", "BasicTargetTrackingScalingPolicyProps", "CfnScalableTarget", "CfnScalableTargetProps", "CfnScalingPolicy", "CfnScalingPolicyProps", "Cron", "EnableScalingProps", "IScalableTarget", "MetricAggregationType", "PredefinedMetric", "ScalableTarget", "ScalableTargetProps", "ScalingInterval", "ScalingSchedule", "ServiceNamespace", "StepScalingAction", "StepScalingActionProps", "StepScalingPolicy", "StepScalingPolicyProps", "TargetTrackingScalingPolicy", "TargetTrackingScalingPolicyProps", "__jsii_assembly__"]

publication.publish()
