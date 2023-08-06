import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_autoscaling_api
import aws_cdk.aws_autoscaling_common
import aws_cdk.aws_cloudwatch
import aws_cdk.aws_ec2
import aws_cdk.aws_elasticloadbalancing
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_iam
import aws_cdk.aws_sns
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling", "0.32.0", __name__, "aws-autoscaling@0.32.0.jsii.tgz")
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

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentTier", jsii_struct_bases=[_AdjustmentTier])
class AdjustmentTier(_AdjustmentTier):
    """An adjustment."""
    adjustment: jsii.Number
    """What number to adjust the capacity with.

    The number is interpeted as an added capacity, a new fixed capacity or an
    added percentage depending on the AdjustmentType value of the
    StepScalingPolicy.

    Can be positive or negative.
    """

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.AdjustmentType")
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

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BaseTargetTrackingProps", jsii_struct_bases=[])
class BaseTargetTrackingProps(jsii.compat.TypedDict, total=False):
    """Base interface for target tracking props.

    Contains the attributes that are common to target tracking policies,
    except the ones relating to the metric and to the scalable target.

    This interface is reused by more specific target tracking props objects.
    """
    cooldownSeconds: jsii.Number
    """Period after a scaling completes before another scaling activity can start.

    Default:
        - The default cooldown configured on the AutoScalingGroup.
    """

    disableScaleIn: bool
    """Indicates whether scale in by the target tracking policy is disabled.

    If the value is true, scale in is disabled and the target tracking policy
    won't remove capacity from the autoscaling group. Otherwise, scale in is
    enabled and the target tracking policy can remove capacity from the
    group.

    Default:
        false
    """

    estimatedInstanceWarmupSeconds: jsii.Number
    """Estimated time until a newly launched instance can send metrics to CloudWatch.

    Default:
        - Same as the cooldown.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BasicLifecycleHookProps(jsii.compat.TypedDict, total=False):
    defaultResult: "DefaultResult"
    """The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs.

    Default:
        Continue
    """
    heartbeatTimeoutSec: jsii.Number
    """Maximum time between calls to RecordLifecycleActionHeartbeat for the hook.

    If the lifecycle hook times out, perform the action in DefaultResult.

    Default:
        - No heartbeat timeout.
    """
    lifecycleHookName: str
    """Name of the lifecycle hook.

    Default:
        - Automatically generated name.
    """
    notificationMetadata: str
    """Additional data to pass to the lifecycle hook target.

    Default:
        - No metadata.
    """
    role: aws_cdk.aws_iam.IRole
    """The role that allows publishing to the notification target.

    Default:
        - A role is automatically created.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicLifecycleHookProps", jsii_struct_bases=[_BasicLifecycleHookProps])
class BasicLifecycleHookProps(_BasicLifecycleHookProps):
    """Basic properties for a lifecycle hook."""
    lifecycleTransition: "LifecycleTransition"
    """The state of the Amazon EC2 instance to which you want to attach the lifecycle hook."""

    notificationTarget: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget
    """The target of the lifecycle hook."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BasicScheduledActionProps(jsii.compat.TypedDict, total=False):
    desiredCapacity: jsii.Number
    """The new desired capacity.

    At the scheduled time, set the desired capacity to the given capacity.

    At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

    Default:
        - No new desired capacity.
    """
    endTime: datetime.datetime
    """When this scheduled action expires.

    Default:
        - The rule never expires.
    """
    maxCapacity: jsii.Number
    """The new maximum capacity.

    At the scheduled time, set the maximum capacity to the given capacity.

    At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

    Default:
        - No new maximum capacity.
    """
    minCapacity: jsii.Number
    """The new minimum capacity.

    At the scheduled time, set the minimum capacity to the given capacity.

    At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied.

    Default:
        - No new minimum capacity.
    """
    startTime: datetime.datetime
    """When this scheduled action becomes active.

    Default:
        - The rule is activate immediately.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicScheduledActionProps", jsii_struct_bases=[_BasicScheduledActionProps])
class BasicScheduledActionProps(_BasicScheduledActionProps):
    """Properties for a scheduled scaling action."""
    schedule: str
    """When to perform this action.

    Supports cron expressions.

    For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.

    Example::
        0 8 * * ?
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _BasicStepScalingPolicyProps(jsii.compat.TypedDict, total=False):
    adjustmentType: "AdjustmentType"
    """How the adjustment numbers inside 'intervals' are interpreted.

    Default:
        ChangeInCapacity
    """
    cooldownSeconds: jsii.Number
    """Grace period after scaling activity.

    Default:
        Default cooldown period on your AutoScalingGroup
    """
    estimatedInstanceWarmupSeconds: jsii.Number
    """Estimated time until a newly launched instance can send metrics to CloudWatch.

    Default:
        Same as the cooldown
    """
    minAdjustmentMagnitude: jsii.Number
    """Minimum absolute number to adjust capacity with as result of percentage scaling.

    Only when using AdjustmentType = PercentChangeInCapacity, this number controls
    the minimum absolute effect size.

    Default:
        No minimum scaling effect
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicStepScalingPolicyProps", jsii_struct_bases=[_BasicStepScalingPolicyProps])
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
        - No predefined metric.
    """
    resourceLabel: str
    """The resource label associated with the predefined metric.

    Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the
    format should be:

    app///targetgroup//

    Default:
        - No resource label.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.BasicTargetTrackingScalingPolicyProps", jsii_struct_bases=[_BasicTargetTrackingScalingPolicyProps])
class BasicTargetTrackingScalingPolicyProps(_BasicTargetTrackingScalingPolicyProps):
    """Properties for a Target Tracking policy that include the metric but exclude the target."""
    targetValue: jsii.Number
    """The target value for the metric."""

class CfnAutoScalingGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup"):
    """A CloudFormation ``AWS::AutoScaling::AutoScalingGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
    cloudformationResource:
        AWS::AutoScaling::AutoScalingGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, max_size: str, min_size: str, auto_scaling_group_name: typing.Optional[str]=None, availability_zones: typing.Optional[typing.List[str]]=None, cooldown: typing.Optional[str]=None, desired_capacity: typing.Optional[str]=None, health_check_grace_period: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, health_check_type: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, launch_template: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["LaunchTemplateSpecificationProperty"]]]=None, lifecycle_hook_specification_list: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "LifecycleHookSpecificationProperty"]]]]]=None, load_balancer_names: typing.Optional[typing.List[str]]=None, metrics_collection: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "MetricsCollectionProperty"]]]]]=None, mixed_instances_policy: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["MixedInstancesPolicyProperty"]]]=None, notification_configurations: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "NotificationConfigurationProperty"]]]]]=None, placement_group: typing.Optional[str]=None, service_linked_role_arn: typing.Optional[str]=None, tags: typing.Optional[typing.List["TagPropertyProperty"]]=None, target_group_arns: typing.Optional[typing.List[str]]=None, termination_policies: typing.Optional[typing.List[str]]=None, vpc_zone_identifier: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::AutoScaling::AutoScalingGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            maxSize: ``AWS::AutoScaling::AutoScalingGroup.MaxSize``.
            minSize: ``AWS::AutoScaling::AutoScalingGroup.MinSize``.
            autoScalingGroupName: ``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.
            availabilityZones: ``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.
            cooldown: ``AWS::AutoScaling::AutoScalingGroup.Cooldown``.
            desiredCapacity: ``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.
            healthCheckGracePeriod: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.
            healthCheckType: ``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.
            instanceId: ``AWS::AutoScaling::AutoScalingGroup.InstanceId``.
            launchConfigurationName: ``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.
            launchTemplate: ``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.
            lifecycleHookSpecificationList: ``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.
            loadBalancerNames: ``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.
            metricsCollection: ``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.
            mixedInstancesPolicy: ``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.
            notificationConfigurations: ``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.
            placementGroup: ``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.
            serviceLinkedRoleArn: ``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.
            tags: ``AWS::AutoScaling::AutoScalingGroup.Tags``.
            targetGroupArns: ``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.
            terminationPolicies: ``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.
            vpcZoneIdentifier: ``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.
        """
        props: CfnAutoScalingGroupProps = {"maxSize": max_size, "minSize": min_size}

        if auto_scaling_group_name is not None:
            props["autoScalingGroupName"] = auto_scaling_group_name

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if cooldown is not None:
            props["cooldown"] = cooldown

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if health_check_grace_period is not None:
            props["healthCheckGracePeriod"] = health_check_grace_period

        if health_check_type is not None:
            props["healthCheckType"] = health_check_type

        if instance_id is not None:
            props["instanceId"] = instance_id

        if launch_configuration_name is not None:
            props["launchConfigurationName"] = launch_configuration_name

        if launch_template is not None:
            props["launchTemplate"] = launch_template

        if lifecycle_hook_specification_list is not None:
            props["lifecycleHookSpecificationList"] = lifecycle_hook_specification_list

        if load_balancer_names is not None:
            props["loadBalancerNames"] = load_balancer_names

        if metrics_collection is not None:
            props["metricsCollection"] = metrics_collection

        if mixed_instances_policy is not None:
            props["mixedInstancesPolicy"] = mixed_instances_policy

        if notification_configurations is not None:
            props["notificationConfigurations"] = notification_configurations

        if placement_group is not None:
            props["placementGroup"] = placement_group

        if service_linked_role_arn is not None:
            props["serviceLinkedRoleArn"] = service_linked_role_arn

        if tags is not None:
            props["tags"] = tags

        if target_group_arns is not None:
            props["targetGroupArns"] = target_group_arns

        if termination_policies is not None:
            props["terminationPolicies"] = termination_policies

        if vpc_zone_identifier is not None:
            props["vpcZoneIdentifier"] = vpc_zone_identifier

        jsii.create(CfnAutoScalingGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        return jsii.get(self, "autoScalingGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAutoScalingGroupProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.InstancesDistributionProperty", jsii_struct_bases=[])
    class InstancesDistributionProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html
        """
        onDemandAllocationStrategy: str
        """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandAllocationStrategy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandallocationstrategy
        """

        onDemandBaseCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandBaseCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandbasecapacity
        """

        onDemandPercentageAboveBaseCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnAutoScalingGroup.InstancesDistributionProperty.OnDemandPercentageAboveBaseCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-ondemandpercentageabovebasecapacity
        """

        spotAllocationStrategy: str
        """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotAllocationStrategy``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotallocationstrategy
        """

        spotInstancePools: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotInstancePools``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotinstancepools
        """

        spotMaxPrice: str
        """``CfnAutoScalingGroup.InstancesDistributionProperty.SpotMaxPrice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-instancesdistribution.html#cfn-autoscaling-autoscalinggroup-instancesdistribution-spotmaxprice
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateOverridesProperty", jsii_struct_bases=[])
    class LaunchTemplateOverridesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html
        """
        instanceType: str
        """``CfnAutoScalingGroup.LaunchTemplateOverridesProperty.InstanceType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplateoverrides.html#cfn-autoscaling-autoscalinggroup-launchtemplateoverrides-instancetype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LaunchTemplateProperty(jsii.compat.TypedDict, total=False):
        overrides: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateOverridesProperty"]]]
        """``CfnAutoScalingGroup.LaunchTemplateProperty.Overrides``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html#cfn-as-mixedinstancespolicy-overrides
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateProperty", jsii_struct_bases=[_LaunchTemplateProperty])
    class LaunchTemplateProperty(_LaunchTemplateProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html
        """
        launchTemplateSpecification: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]
        """``CfnAutoScalingGroup.LaunchTemplateProperty.LaunchTemplateSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-mixedinstancespolicy-launchtemplate.html#cfn-as-group-launchtemplate
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LaunchTemplateSpecificationProperty(jsii.compat.TypedDict, total=False):
        launchTemplateId: str
        """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplateid
        """
        launchTemplateName: str
        """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.LaunchTemplateName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-launchtemplatename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LaunchTemplateSpecificationProperty", jsii_struct_bases=[_LaunchTemplateSpecificationProperty])
    class LaunchTemplateSpecificationProperty(_LaunchTemplateSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html
        """
        version: str
        """``CfnAutoScalingGroup.LaunchTemplateSpecificationProperty.Version``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-launchtemplatespecification.html#cfn-autoscaling-autoscalinggroup-launchtemplatespecification-version
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _LifecycleHookSpecificationProperty(jsii.compat.TypedDict, total=False):
        defaultResult: str
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.DefaultResult``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-defaultresult
        """
        heartbeatTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.HeartbeatTimeout``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-heartbeattimeout
        """
        notificationMetadata: str
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationMetadata``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationmetadata
        """
        notificationTargetArn: str
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.NotificationTargetARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-notificationtargetarn
        """
        roleArn: str
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.LifecycleHookSpecificationProperty", jsii_struct_bases=[_LifecycleHookSpecificationProperty])
    class LifecycleHookSpecificationProperty(_LifecycleHookSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html
        """
        lifecycleHookName: str
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleHookName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecyclehookname
        """

        lifecycleTransition: str
        """``CfnAutoScalingGroup.LifecycleHookSpecificationProperty.LifecycleTransition``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-autoscalinggroup-lifecyclehookspecification.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecification-lifecycletransition
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _MetricsCollectionProperty(jsii.compat.TypedDict, total=False):
        metrics: typing.List[str]
        """``CfnAutoScalingGroup.MetricsCollectionProperty.Metrics``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html#cfn-as-metricscollection-metrics
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MetricsCollectionProperty", jsii_struct_bases=[_MetricsCollectionProperty])
    class MetricsCollectionProperty(_MetricsCollectionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html
        """
        granularity: str
        """``CfnAutoScalingGroup.MetricsCollectionProperty.Granularity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-metricscollection.html#cfn-as-metricscollection-granularity
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _MixedInstancesPolicyProperty(jsii.compat.TypedDict, total=False):
        instancesDistribution: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.InstancesDistributionProperty"]
        """``CfnAutoScalingGroup.MixedInstancesPolicyProperty.InstancesDistribution``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html#cfn-as-mixedinstancespolicy-instancesdistribution
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.MixedInstancesPolicyProperty", jsii_struct_bases=[_MixedInstancesPolicyProperty])
    class MixedInstancesPolicyProperty(_MixedInstancesPolicyProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html
        """
        launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateProperty"]
        """``CfnAutoScalingGroup.MixedInstancesPolicyProperty.LaunchTemplate``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/cfn-as-group-mixedinstancespolicy.html#cfn-as-mixedinstancespolicy-launchtemplate
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _NotificationConfigurationProperty(jsii.compat.TypedDict, total=False):
        notificationTypes: typing.List[str]
        """``CfnAutoScalingGroup.NotificationConfigurationProperty.NotificationTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html#cfn-as-group-notificationconfigurations-notificationtypes
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.NotificationConfigurationProperty", jsii_struct_bases=[_NotificationConfigurationProperty])
    class NotificationConfigurationProperty(_NotificationConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html
        """
        topicArn: str
        """``CfnAutoScalingGroup.NotificationConfigurationProperty.TopicARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-notificationconfigurations.html#cfn-autoscaling-autoscalinggroup-notificationconfigurations-topicarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroup.TagPropertyProperty", jsii_struct_bases=[])
    class TagPropertyProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html
        """
        key: str
        """``CfnAutoScalingGroup.TagPropertyProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-Key
        """

        propagateAtLaunch: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnAutoScalingGroup.TagPropertyProperty.PropagateAtLaunch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-PropagateAtLaunch
        """

        value: str
        """``CfnAutoScalingGroup.TagPropertyProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-tags.html#cfn-as-tags-Value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnAutoScalingGroupProps(jsii.compat.TypedDict, total=False):
    autoScalingGroupName: str
    """``AWS::AutoScaling::AutoScalingGroup.AutoScalingGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-autoscalinggroupname
    """
    availabilityZones: typing.List[str]
    """``AWS::AutoScaling::AutoScalingGroup.AvailabilityZones``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-availabilityzones
    """
    cooldown: str
    """``AWS::AutoScaling::AutoScalingGroup.Cooldown``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-cooldown
    """
    desiredCapacity: str
    """``AWS::AutoScaling::AutoScalingGroup.DesiredCapacity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-desiredcapacity
    """
    healthCheckGracePeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::AutoScalingGroup.HealthCheckGracePeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthcheckgraceperiod
    """
    healthCheckType: str
    """``AWS::AutoScaling::AutoScalingGroup.HealthCheckType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-healthchecktype
    """
    instanceId: str
    """``AWS::AutoScaling::AutoScalingGroup.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-instanceid
    """
    launchConfigurationName: str
    """``AWS::AutoScaling::AutoScalingGroup.LaunchConfigurationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchconfigurationname
    """
    launchTemplate: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LaunchTemplateSpecificationProperty"]
    """``AWS::AutoScaling::AutoScalingGroup.LaunchTemplate``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-launchtemplate
    """
    lifecycleHookSpecificationList: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.LifecycleHookSpecificationProperty"]]]
    """``AWS::AutoScaling::AutoScalingGroup.LifecycleHookSpecificationList``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-lifecyclehookspecificationlist
    """
    loadBalancerNames: typing.List[str]
    """``AWS::AutoScaling::AutoScalingGroup.LoadBalancerNames``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-loadbalancernames
    """
    metricsCollection: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.MetricsCollectionProperty"]]]
    """``AWS::AutoScaling::AutoScalingGroup.MetricsCollection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-metricscollection
    """
    mixedInstancesPolicy: typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.MixedInstancesPolicyProperty"]
    """``AWS::AutoScaling::AutoScalingGroup.MixedInstancesPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-mixedinstancespolicy
    """
    notificationConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAutoScalingGroup.NotificationConfigurationProperty"]]]
    """``AWS::AutoScaling::AutoScalingGroup.NotificationConfigurations``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-notificationconfigurations
    """
    placementGroup: str
    """``AWS::AutoScaling::AutoScalingGroup.PlacementGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-placementgroup
    """
    serviceLinkedRoleArn: str
    """``AWS::AutoScaling::AutoScalingGroup.ServiceLinkedRoleARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-autoscaling-autoscalinggroup-servicelinkedrolearn
    """
    tags: typing.List["CfnAutoScalingGroup.TagPropertyProperty"]
    """``AWS::AutoScaling::AutoScalingGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-tags
    """
    targetGroupArns: typing.List[str]
    """``AWS::AutoScaling::AutoScalingGroup.TargetGroupARNs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-targetgrouparns
    """
    terminationPolicies: typing.List[str]
    """``AWS::AutoScaling::AutoScalingGroup.TerminationPolicies``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-termpolicy
    """
    vpcZoneIdentifier: typing.List[str]
    """``AWS::AutoScaling::AutoScalingGroup.VPCZoneIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-vpczoneidentifier
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnAutoScalingGroupProps", jsii_struct_bases=[_CfnAutoScalingGroupProps])
class CfnAutoScalingGroupProps(_CfnAutoScalingGroupProps):
    """Properties for defining a ``AWS::AutoScaling::AutoScalingGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html
    """
    maxSize: str
    """``AWS::AutoScaling::AutoScalingGroup.MaxSize``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-maxsize
    """

    minSize: str
    """``AWS::AutoScaling::AutoScalingGroup.MinSize``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-group.html#cfn-as-group-minsize
    """

class CfnLaunchConfiguration(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration"):
    """A CloudFormation ``AWS::AutoScaling::LaunchConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
    cloudformationResource:
        AWS::AutoScaling::LaunchConfiguration
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, image_id: str, instance_type: str, associate_public_ip_address: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, block_device_mappings: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "BlockDeviceMappingProperty"]]]]]=None, classic_link_vpc_id: typing.Optional[str]=None, classic_link_vpc_security_groups: typing.Optional[typing.List[str]]=None, ebs_optimized: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, iam_instance_profile: typing.Optional[str]=None, instance_id: typing.Optional[str]=None, instance_monitoring: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, kernel_id: typing.Optional[str]=None, key_name: typing.Optional[str]=None, launch_configuration_name: typing.Optional[str]=None, placement_tenancy: typing.Optional[str]=None, ram_disk_id: typing.Optional[str]=None, security_groups: typing.Optional[typing.List[str]]=None, spot_price: typing.Optional[str]=None, user_data: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AutoScaling::LaunchConfiguration``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            imageId: ``AWS::AutoScaling::LaunchConfiguration.ImageId``.
            instanceType: ``AWS::AutoScaling::LaunchConfiguration.InstanceType``.
            associatePublicIpAddress: ``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.
            blockDeviceMappings: ``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.
            classicLinkVpcId: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.
            classicLinkVpcSecurityGroups: ``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.
            ebsOptimized: ``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.
            iamInstanceProfile: ``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.
            instanceId: ``AWS::AutoScaling::LaunchConfiguration.InstanceId``.
            instanceMonitoring: ``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.
            kernelId: ``AWS::AutoScaling::LaunchConfiguration.KernelId``.
            keyName: ``AWS::AutoScaling::LaunchConfiguration.KeyName``.
            launchConfigurationName: ``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.
            placementTenancy: ``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.
            ramDiskId: ``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.
            securityGroups: ``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.
            spotPrice: ``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.
            userData: ``AWS::AutoScaling::LaunchConfiguration.UserData``.
        """
        props: CfnLaunchConfigurationProps = {"imageId": image_id, "instanceType": instance_type}

        if associate_public_ip_address is not None:
            props["associatePublicIpAddress"] = associate_public_ip_address

        if block_device_mappings is not None:
            props["blockDeviceMappings"] = block_device_mappings

        if classic_link_vpc_id is not None:
            props["classicLinkVpcId"] = classic_link_vpc_id

        if classic_link_vpc_security_groups is not None:
            props["classicLinkVpcSecurityGroups"] = classic_link_vpc_security_groups

        if ebs_optimized is not None:
            props["ebsOptimized"] = ebs_optimized

        if iam_instance_profile is not None:
            props["iamInstanceProfile"] = iam_instance_profile

        if instance_id is not None:
            props["instanceId"] = instance_id

        if instance_monitoring is not None:
            props["instanceMonitoring"] = instance_monitoring

        if kernel_id is not None:
            props["kernelId"] = kernel_id

        if key_name is not None:
            props["keyName"] = key_name

        if launch_configuration_name is not None:
            props["launchConfigurationName"] = launch_configuration_name

        if placement_tenancy is not None:
            props["placementTenancy"] = placement_tenancy

        if ram_disk_id is not None:
            props["ramDiskId"] = ram_disk_id

        if security_groups is not None:
            props["securityGroups"] = security_groups

        if spot_price is not None:
            props["spotPrice"] = spot_price

        if user_data is not None:
            props["userData"] = user_data

        jsii.create(CfnLaunchConfiguration, self, [scope, id, props])

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
    @jsii.member(jsii_name="launchConfigurationName")
    def launch_configuration_name(self) -> str:
        return jsii.get(self, "launchConfigurationName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLaunchConfigurationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _BlockDeviceMappingProperty(jsii.compat.TypedDict, total=False):
        ebs: typing.Union[aws_cdk.cdk.Token, "CfnLaunchConfiguration.BlockDeviceProperty"]
        """``CfnLaunchConfiguration.BlockDeviceMappingProperty.Ebs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-ebs
        """
        noDevice: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchConfiguration.BlockDeviceMappingProperty.NoDevice``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-nodevice
        """
        virtualName: str
        """``CfnLaunchConfiguration.BlockDeviceMappingProperty.VirtualName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-virtualname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceMappingProperty", jsii_struct_bases=[_BlockDeviceMappingProperty])
    class BlockDeviceMappingProperty(_BlockDeviceMappingProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html
        """
        deviceName: str
        """``CfnLaunchConfiguration.BlockDeviceMappingProperty.DeviceName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-mapping.html#cfn-as-launchconfig-blockdev-mapping-devicename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfiguration.BlockDeviceProperty", jsii_struct_bases=[])
    class BlockDeviceProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html
        """
        deleteOnTermination: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchConfiguration.BlockDeviceProperty.DeleteOnTermination``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-deleteonterm
        """

        encrypted: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnLaunchConfiguration.BlockDeviceProperty.Encrypted``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-encrypted
        """

        iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchConfiguration.BlockDeviceProperty.Iops``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-iops
        """

        snapshotId: str
        """``CfnLaunchConfiguration.BlockDeviceProperty.SnapshotId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-snapshotid
        """

        volumeSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnLaunchConfiguration.BlockDeviceProperty.VolumeSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-volumesize
        """

        volumeType: str
        """``CfnLaunchConfiguration.BlockDeviceProperty.VolumeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig-blockdev-template.html#cfn-as-launchconfig-blockdev-template-volumetype
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLaunchConfigurationProps(jsii.compat.TypedDict, total=False):
    associatePublicIpAddress: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::LaunchConfiguration.AssociatePublicIpAddress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cf-as-launchconfig-associatepubip
    """
    blockDeviceMappings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnLaunchConfiguration.BlockDeviceMappingProperty"]]]
    """``AWS::AutoScaling::LaunchConfiguration.BlockDeviceMappings``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-blockdevicemappings
    """
    classicLinkVpcId: str
    """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcid
    """
    classicLinkVpcSecurityGroups: typing.List[str]
    """``AWS::AutoScaling::LaunchConfiguration.ClassicLinkVPCSecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-classiclinkvpcsecuritygroups
    """
    ebsOptimized: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::LaunchConfiguration.EbsOptimized``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ebsoptimized
    """
    iamInstanceProfile: str
    """``AWS::AutoScaling::LaunchConfiguration.IamInstanceProfile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-iaminstanceprofile
    """
    instanceId: str
    """``AWS::AutoScaling::LaunchConfiguration.InstanceId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instanceid
    """
    instanceMonitoring: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::LaunchConfiguration.InstanceMonitoring``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancemonitoring
    """
    kernelId: str
    """``AWS::AutoScaling::LaunchConfiguration.KernelId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-kernelid
    """
    keyName: str
    """``AWS::AutoScaling::LaunchConfiguration.KeyName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-keyname
    """
    launchConfigurationName: str
    """``AWS::AutoScaling::LaunchConfiguration.LaunchConfigurationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-autoscaling-launchconfig-launchconfigurationname
    """
    placementTenancy: str
    """``AWS::AutoScaling::LaunchConfiguration.PlacementTenancy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-placementtenancy
    """
    ramDiskId: str
    """``AWS::AutoScaling::LaunchConfiguration.RamDiskId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-ramdiskid
    """
    securityGroups: typing.List[str]
    """``AWS::AutoScaling::LaunchConfiguration.SecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-securitygroups
    """
    spotPrice: str
    """``AWS::AutoScaling::LaunchConfiguration.SpotPrice``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-spotprice
    """
    userData: str
    """``AWS::AutoScaling::LaunchConfiguration.UserData``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-userdata
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLaunchConfigurationProps", jsii_struct_bases=[_CfnLaunchConfigurationProps])
class CfnLaunchConfigurationProps(_CfnLaunchConfigurationProps):
    """Properties for defining a ``AWS::AutoScaling::LaunchConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html
    """
    imageId: str
    """``AWS::AutoScaling::LaunchConfiguration.ImageId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-imageid
    """

    instanceType: str
    """``AWS::AutoScaling::LaunchConfiguration.InstanceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-launchconfig.html#cfn-as-launchconfig-instancetype
    """

class CfnLifecycleHook(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHook"):
    """A CloudFormation ``AWS::AutoScaling::LifecycleHook``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html
    cloudformationResource:
        AWS::AutoScaling::LifecycleHook
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group_name: str, lifecycle_transition: str, default_result: typing.Optional[str]=None, heartbeat_timeout: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, notification_target_arn: typing.Optional[str]=None, role_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AutoScaling::LifecycleHook``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            autoScalingGroupName: ``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.
            lifecycleTransition: ``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.
            defaultResult: ``AWS::AutoScaling::LifecycleHook.DefaultResult``.
            heartbeatTimeout: ``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.
            lifecycleHookName: ``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.
            notificationMetadata: ``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.
            notificationTargetArn: ``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.
            roleArn: ``AWS::AutoScaling::LifecycleHook.RoleARN``.
        """
        props: CfnLifecycleHookProps = {"autoScalingGroupName": auto_scaling_group_name, "lifecycleTransition": lifecycle_transition}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout is not None:
            props["heartbeatTimeout"] = heartbeat_timeout

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if notification_target_arn is not None:
            props["notificationTargetArn"] = notification_target_arn

        if role_arn is not None:
            props["roleArn"] = role_arn

        jsii.create(CfnLifecycleHook, self, [scope, id, props])

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
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> str:
        return jsii.get(self, "lifecycleHookName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnLifecycleHookProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnLifecycleHookProps(jsii.compat.TypedDict, total=False):
    defaultResult: str
    """``AWS::AutoScaling::LifecycleHook.DefaultResult``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-defaultresult
    """
    heartbeatTimeout: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::LifecycleHook.HeartbeatTimeout``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-heartbeattimeout
    """
    lifecycleHookName: str
    """``AWS::AutoScaling::LifecycleHook.LifecycleHookName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-autoscaling-lifecyclehook-lifecyclehookname
    """
    notificationMetadata: str
    """``AWS::AutoScaling::LifecycleHook.NotificationMetadata``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationmetadata
    """
    notificationTargetArn: str
    """``AWS::AutoScaling::LifecycleHook.NotificationTargetARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-notificationtargetarn
    """
    roleArn: str
    """``AWS::AutoScaling::LifecycleHook.RoleARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-rolearn
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnLifecycleHookProps", jsii_struct_bases=[_CfnLifecycleHookProps])
class CfnLifecycleHookProps(_CfnLifecycleHookProps):
    """Properties for defining a ``AWS::AutoScaling::LifecycleHook``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html
    """
    autoScalingGroupName: str
    """``AWS::AutoScaling::LifecycleHook.AutoScalingGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-autoscalinggroupname
    """

    lifecycleTransition: str
    """``AWS::AutoScaling::LifecycleHook.LifecycleTransition``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-lifecyclehook.html#cfn-as-lifecyclehook-lifecycletransition
    """

class CfnScalingPolicy(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy"):
    """A CloudFormation ``AWS::AutoScaling::ScalingPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
    cloudformationResource:
        AWS::AutoScaling::ScalingPolicy
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group_name: str, adjustment_type: typing.Optional[str]=None, cooldown: typing.Optional[str]=None, estimated_instance_warmup: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, metric_aggregation_type: typing.Optional[str]=None, min_adjustment_magnitude: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, policy_type: typing.Optional[str]=None, scaling_adjustment: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, step_adjustments: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "StepAdjustmentProperty"]]]]]=None, target_tracking_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["TargetTrackingConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::AutoScaling::ScalingPolicy``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            autoScalingGroupName: ``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.
            adjustmentType: ``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.
            cooldown: ``AWS::AutoScaling::ScalingPolicy.Cooldown``.
            estimatedInstanceWarmup: ``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.
            metricAggregationType: ``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.
            minAdjustmentMagnitude: ``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.
            policyType: ``AWS::AutoScaling::ScalingPolicy.PolicyType``.
            scalingAdjustment: ``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.
            stepAdjustments: ``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.
            targetTrackingConfiguration: ``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.
        """
        props: CfnScalingPolicyProps = {"autoScalingGroupName": auto_scaling_group_name}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown is not None:
            props["cooldown"] = cooldown

        if estimated_instance_warmup is not None:
            props["estimatedInstanceWarmup"] = estimated_instance_warmup

        if metric_aggregation_type is not None:
            props["metricAggregationType"] = metric_aggregation_type

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        if policy_type is not None:
            props["policyType"] = policy_type

        if scaling_adjustment is not None:
            props["scalingAdjustment"] = scaling_adjustment

        if step_adjustments is not None:
            props["stepAdjustments"] = step_adjustments

        if target_tracking_configuration is not None:
            props["targetTrackingConfiguration"] = target_tracking_configuration

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
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-dimensions
        """
        unit: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Unit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-unit
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.CustomizedMetricSpecificationProperty", jsii_struct_bases=[_CustomizedMetricSpecificationProperty])
    class CustomizedMetricSpecificationProperty(_CustomizedMetricSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html
        """
        metricName: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.MetricName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-metricname
        """

        namespace: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Namespace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-namespace
        """

        statistic: str
        """``CfnScalingPolicy.CustomizedMetricSpecificationProperty.Statistic``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-customizedmetricspecification.html#cfn-autoscaling-scalingpolicy-customizedmetricspecification-statistic
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.MetricDimensionProperty", jsii_struct_bases=[])
    class MetricDimensionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html
        """
        name: str
        """``CfnScalingPolicy.MetricDimensionProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-name
        """

        value: str
        """``CfnScalingPolicy.MetricDimensionProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-metricdimension.html#cfn-autoscaling-scalingpolicy-metricdimension-value
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _PredefinedMetricSpecificationProperty(jsii.compat.TypedDict, total=False):
        resourceLabel: str
        """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.ResourceLabel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-resourcelabel
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.PredefinedMetricSpecificationProperty", jsii_struct_bases=[_PredefinedMetricSpecificationProperty])
    class PredefinedMetricSpecificationProperty(_PredefinedMetricSpecificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html
        """
        predefinedMetricType: str
        """``CfnScalingPolicy.PredefinedMetricSpecificationProperty.PredefinedMetricType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-predefinedmetricspecification.html#cfn-autoscaling-scalingpolicy-predefinedmetricspecification-predefinedmetrictype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _StepAdjustmentProperty(jsii.compat.TypedDict, total=False):
        metricIntervalLowerBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalLowerBound``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervallowerbound
        """
        metricIntervalUpperBound: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepAdjustmentProperty.MetricIntervalUpperBound``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-metricintervalupperbound
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.StepAdjustmentProperty", jsii_struct_bases=[_StepAdjustmentProperty])
    class StepAdjustmentProperty(_StepAdjustmentProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html
        """
        scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.StepAdjustmentProperty.ScalingAdjustment``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-stepadjustments.html#cfn-autoscaling-scalingpolicy-stepadjustment-scalingadjustment
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _TargetTrackingConfigurationProperty(jsii.compat.TypedDict, total=False):
        customizedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.CustomizedMetricSpecificationProperty"]
        """``CfnScalingPolicy.TargetTrackingConfigurationProperty.CustomizedMetricSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-customizedmetricspecification
        """
        disableScaleIn: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.TargetTrackingConfigurationProperty.DisableScaleIn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-disablescalein
        """
        predefinedMetricSpecification: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.PredefinedMetricSpecificationProperty"]
        """``CfnScalingPolicy.TargetTrackingConfigurationProperty.PredefinedMetricSpecification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-predefinedmetricspecification
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicy.TargetTrackingConfigurationProperty", jsii_struct_bases=[_TargetTrackingConfigurationProperty])
    class TargetTrackingConfigurationProperty(_TargetTrackingConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html
        """
        targetValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnScalingPolicy.TargetTrackingConfigurationProperty.TargetValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-autoscaling-scalingpolicy-targettrackingconfiguration.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration-targetvalue
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnScalingPolicyProps(jsii.compat.TypedDict, total=False):
    adjustmentType: str
    """``AWS::AutoScaling::ScalingPolicy.AdjustmentType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-adjustmenttype
    """
    cooldown: str
    """``AWS::AutoScaling::ScalingPolicy.Cooldown``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-cooldown
    """
    estimatedInstanceWarmup: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::ScalingPolicy.EstimatedInstanceWarmup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-estimatedinstancewarmup
    """
    metricAggregationType: str
    """``AWS::AutoScaling::ScalingPolicy.MetricAggregationType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-metricaggregationtype
    """
    minAdjustmentMagnitude: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::ScalingPolicy.MinAdjustmentMagnitude``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-minadjustmentmagnitude
    """
    policyType: str
    """``AWS::AutoScaling::ScalingPolicy.PolicyType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-policytype
    """
    scalingAdjustment: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::ScalingPolicy.ScalingAdjustment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-scalingadjustment
    """
    stepAdjustments: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.StepAdjustmentProperty"]]]
    """``AWS::AutoScaling::ScalingPolicy.StepAdjustments``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-stepadjustments
    """
    targetTrackingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnScalingPolicy.TargetTrackingConfigurationProperty"]
    """``AWS::AutoScaling::ScalingPolicy.TargetTrackingConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-autoscaling-scalingpolicy-targettrackingconfiguration
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScalingPolicyProps", jsii_struct_bases=[_CfnScalingPolicyProps])
class CfnScalingPolicyProps(_CfnScalingPolicyProps):
    """Properties for defining a ``AWS::AutoScaling::ScalingPolicy``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html
    """
    autoScalingGroupName: str
    """``AWS::AutoScaling::ScalingPolicy.AutoScalingGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-as-policy.html#cfn-as-scalingpolicy-autoscalinggroupname
    """

class CfnScheduledAction(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledAction"):
    """A CloudFormation ``AWS::AutoScaling::ScheduledAction``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html
    cloudformationResource:
        AWS::AutoScaling::ScheduledAction
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group_name: str, desired_capacity: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, end_time: typing.Optional[str]=None, max_size: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, min_size: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, recurrence: typing.Optional[str]=None, start_time: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::AutoScaling::ScheduledAction``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            autoScalingGroupName: ``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.
            desiredCapacity: ``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.
            endTime: ``AWS::AutoScaling::ScheduledAction.EndTime``.
            maxSize: ``AWS::AutoScaling::ScheduledAction.MaxSize``.
            minSize: ``AWS::AutoScaling::ScheduledAction.MinSize``.
            recurrence: ``AWS::AutoScaling::ScheduledAction.Recurrence``.
            startTime: ``AWS::AutoScaling::ScheduledAction.StartTime``.
        """
        props: CfnScheduledActionProps = {"autoScalingGroupName": auto_scaling_group_name}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_size is not None:
            props["maxSize"] = max_size

        if min_size is not None:
            props["minSize"] = min_size

        if recurrence is not None:
            props["recurrence"] = recurrence

        if start_time is not None:
            props["startTime"] = start_time

        jsii.create(CfnScheduledAction, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnScheduledActionProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="scheduledActionName")
    def scheduled_action_name(self) -> str:
        return jsii.get(self, "scheduledActionName")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnScheduledActionProps(jsii.compat.TypedDict, total=False):
    desiredCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::ScheduledAction.DesiredCapacity``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-desiredcapacity
    """
    endTime: str
    """``AWS::AutoScaling::ScheduledAction.EndTime``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-endtime
    """
    maxSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::ScheduledAction.MaxSize``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-maxsize
    """
    minSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::AutoScaling::ScheduledAction.MinSize``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-minsize
    """
    recurrence: str
    """``AWS::AutoScaling::ScheduledAction.Recurrence``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-recurrence
    """
    startTime: str
    """``AWS::AutoScaling::ScheduledAction.StartTime``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-starttime
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CfnScheduledActionProps", jsii_struct_bases=[_CfnScheduledActionProps])
class CfnScheduledActionProps(_CfnScheduledActionProps):
    """Properties for defining a ``AWS::AutoScaling::ScheduledAction``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html
    """
    autoScalingGroupName: str
    """``AWS::AutoScaling::ScheduledAction.AutoScalingGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-as-scheduledaction.html#cfn-as-scheduledaction-asgname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CommonAutoScalingGroupProps", jsii_struct_bases=[])
class CommonAutoScalingGroupProps(jsii.compat.TypedDict, total=False):
    """Basic properties of an AutoScalingGroup, except the exact machines to run and where they should run.

    Constructs that want to create AutoScalingGroups can inherit
    this interface and specialize the essential parts in various ways.
    """
    allowAllOutbound: bool
    """Whether the instances can initiate connections to anywhere by default.

    Default:
        true
    """

    associatePublicIpAddress: bool
    """Whether instances in the Auto Scaling Group should have public IP addresses associated with them.

    Default:
        - Use subnet setting.
    """

    cooldownSeconds: jsii.Number
    """Default scaling cooldown for this AutoScalingGroup.

    Default:
        300 (5 minutes)
    """

    desiredCapacity: jsii.Number
    """Initial amount of instances in the fleet.

    Default:
        1
    """

    ignoreUnmodifiedSizeProperties: bool
    """If the ASG has scheduled actions, don't reset unchanged group sizes.

    Only used if the ASG has scheduled actions (which may scale your ASG up
    or down regardless of cdk deployments). If true, the size of the group
    will only be reset if it has been changed in the CDK app. If false, the
    sizes will always be changed back to what they were in the CDK app
    on deployment.

    Default:
        true
    """

    keyName: str
    """Name of SSH keypair to grant access to instances.

    Default:
        - No SSH access will be possible.
    """

    maxCapacity: jsii.Number
    """Maximum number of instances in the fleet.

    Default:
        desiredCapacity
    """

    minCapacity: jsii.Number
    """Minimum number of instances in the fleet.

    Default:
        1
    """

    notificationsTopic: aws_cdk.aws_sns.ITopic
    """SNS topic to send notifications about fleet changes.

    Default:
        - No fleet change notifications will be sent.
    """

    replacingUpdateMinSuccessfulInstancesPercent: jsii.Number
    """Configuration for replacing updates.

    Only used if updateType == UpdateType.ReplacingUpdate. Specifies how
    many instances must signal success for the update to succeed.

    Default:
        minSuccessfulInstancesPercent
    """

    resourceSignalCount: jsii.Number
    """How many ResourceSignal calls CloudFormation expects before the resource is considered created.

    Default:
        1
    """

    resourceSignalTimeoutSec: jsii.Number
    """The length of time to wait for the resourceSignalCount.

    The maximum value is 43200 (12 hours).

    Default:
        300 (5 minutes)
    """

    rollingUpdateConfiguration: "RollingUpdateConfiguration"
    """Configuration for rolling updates.

    Only used if updateType == UpdateType.RollingUpdate.

    Default:
        - RollingUpdateConfiguration with defaults.
    """

    updateType: "UpdateType"
    """What to do when an AutoScalingGroup's instance configuration is changed.

    This is applied when any of the settings on the ASG are changed that
    affect how the instances should be created (VPC, instance type, startup
    scripts, etc.). It indicates how the existing instances should be
    replaced with new instances matching the new config. By default, nothing
    is done and only new instances are launched with the new config.

    Default:
        UpdateType.None
    """

    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection
    """Where to place instances within the VPC.

    Default:
        - All Private subnets.
    """

@jsii.data_type_optionals(jsii_struct_bases=[CommonAutoScalingGroupProps])
class _AutoScalingGroupProps(CommonAutoScalingGroupProps, jsii.compat.TypedDict, total=False):
    role: aws_cdk.aws_iam.IRole
    """An IAM role to associate with the instance profile assigned to this Auto Scaling Group.

    The role must be assumable by the service principal ``ec2.amazonaws.com``:

    Default:
        A role will automatically be created, it can be accessed via the ``role`` property

    Example::
        const role = new iam.Role(this, 'MyRole', {
        assumedBy: new iam.ServicePrincipal('ec2.amazonaws.com')
        });
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroupProps", jsii_struct_bases=[_AutoScalingGroupProps])
class AutoScalingGroupProps(_AutoScalingGroupProps):
    """Properties of a Fleet."""
    instanceType: aws_cdk.aws_ec2.InstanceType
    """Type of instance to launch."""

    machineImage: aws_cdk.aws_ec2.IMachineImageSource
    """AMI to launch."""

    vpc: aws_cdk.aws_ec2.IVpc
    """VPC to launch these instances in."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.CpuUtilizationScalingProps", jsii_struct_bases=[BaseTargetTrackingProps])
class CpuUtilizationScalingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    """Properties for enabling scaling based on CPU utilization."""
    targetUtilizationPercent: jsii.Number
    """Target average CPU utilization across the task."""

class Cron(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.Cron"):
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


@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.DefaultResult")
class DefaultResult(enum.Enum):
    Continue = "Continue"
    Abandon = "Abandon"

@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling.IAutoScalingGroup")
class IAutoScalingGroup(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """An AutoScalingGroup."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IAutoScalingGroupProxy

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """The name of the AutoScalingGroup.

        attribute:
            true
        """
        ...

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        Arguments:
            id: -
            props: -
            lifecycleTransition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
            notificationTarget: The target of the lifecycle hook.
            defaultResult: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
            heartbeatTimeoutSec: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
            lifecycleHookName: Name of the lifecycle hook. Default: - Automatically generated name.
            notificationMetadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
            role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        ...

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        Arguments:
            id: -
            props: -
            targetUtilizationPercent: Target average CPU utilization across the task.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        Arguments:
            id: -
            props: -
            targetBytesPerSecond: Target average bytes/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        Arguments:
            id: -
            props: -
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSeconds: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        ...

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        Arguments:
            id: -
            props: -
            targetBytesPerSecond: Target average bytes/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        """Scale out or in based on time.

        Arguments:
            id: -
            props: -
            schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
            desiredCapacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
            endTime: When this scheduled action expires. Default: - The rule never expires.
            maxCapacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
            minCapacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
            startTime: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        ...

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        Arguments:
            id: -
            props: -
            metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
            targetValue: Value to keep the metric around.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        ...


class _IAutoScalingGroupProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """An AutoScalingGroup."""
    __jsii_type__ = "@aws-cdk/aws-autoscaling.IAutoScalingGroup"
    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """The name of the AutoScalingGroup.

        attribute:
            true
        """
        return jsii.get(self, "autoScalingGroupName")

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        Arguments:
            id: -
            props: -
            lifecycleTransition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
            notificationTarget: The target of the lifecycle hook.
            defaultResult: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
            heartbeatTimeoutSec: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
            lifecycleHookName: Name of the lifecycle hook. Default: - Automatically generated name.
            notificationMetadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
            role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props: BasicLifecycleHookProps = {"lifecycleTransition": lifecycle_transition, "notificationTarget": notification_target}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout_sec is not None:
            props["heartbeatTimeoutSec"] = heartbeat_timeout_sec

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if role is not None:
            props["role"] = role

        return jsii.invoke(self, "addLifecycleHook", [id, props])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        Arguments:
            id: -
            props: -
            targetUtilizationPercent: Target average CPU utilization across the task.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: CpuUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        Arguments:
            id: -
            props: -
            targetBytesPerSecond: Target average bytes/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        Arguments:
            id: -
            props: -
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSeconds: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        Arguments:
            id: -
            props: -
            targetBytesPerSecond: Target average bytes/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        """Scale out or in based on time.

        Arguments:
            id: -
            props: -
            schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
            desiredCapacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
            endTime: When this scheduled action expires. Default: - The rule never expires.
            maxCapacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
            minCapacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
            startTime: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props: BasicScheduledActionProps = {"schedule": schedule}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        Arguments:
            id: -
            props: -
            metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
            targetValue: Value to keep the metric around.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: MetricTargetTrackingProps = {"metric": metric, "targetValue": target_value}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])


@jsii.implements(aws_cdk.aws_elasticloadbalancing.ILoadBalancerTarget, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_elasticloadbalancingv2.IApplicationLoadBalancerTarget, aws_cdk.aws_elasticloadbalancingv2.INetworkLoadBalancerTarget, IAutoScalingGroup)
class AutoScalingGroup(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.AutoScalingGroup"):
    """A Fleet represents a managed set of EC2 instances.

    The Fleet models a number of AutoScalingGroups, a launch configuration, a
    security group and an instance role.

    It allows adding arbitrary commands to the startup scripts of the instances
    in the fleet.

    The ASG spans all availability zones.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, instance_type: aws_cdk.aws_ec2.InstanceType, machine_image: aws_cdk.aws_ec2.IMachineImageSource, vpc: aws_cdk.aws_ec2.IVpc, role: typing.Optional[aws_cdk.aws_iam.IRole]=None, allow_all_outbound: typing.Optional[bool]=None, associate_public_ip_address: typing.Optional[bool]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, desired_capacity: typing.Optional[jsii.Number]=None, ignore_unmodified_size_properties: typing.Optional[bool]=None, key_name: typing.Optional[str]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, notifications_topic: typing.Optional[aws_cdk.aws_sns.ITopic]=None, replacing_update_min_successful_instances_percent: typing.Optional[jsii.Number]=None, resource_signal_count: typing.Optional[jsii.Number]=None, resource_signal_timeout_sec: typing.Optional[jsii.Number]=None, rolling_update_configuration: typing.Optional["RollingUpdateConfiguration"]=None, update_type: typing.Optional["UpdateType"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            instanceType: Type of instance to launch.
            machineImage: AMI to launch.
            vpc: VPC to launch these instances in.
            role: An IAM role to associate with the instance profile assigned to this Auto Scaling Group. The role must be assumable by the service principal ``ec2.amazonaws.com``: Default: A role will automatically be created, it can be accessed via the ``role`` property
            allowAllOutbound: Whether the instances can initiate connections to anywhere by default. Default: true
            associatePublicIpAddress: Whether instances in the Auto Scaling Group should have public IP addresses associated with them. Default: - Use subnet setting.
            cooldownSeconds: Default scaling cooldown for this AutoScalingGroup. Default: 300 (5 minutes)
            desiredCapacity: Initial amount of instances in the fleet. Default: 1
            ignoreUnmodifiedSizeProperties: If the ASG has scheduled actions, don't reset unchanged group sizes. Only used if the ASG has scheduled actions (which may scale your ASG up or down regardless of cdk deployments). If true, the size of the group will only be reset if it has been changed in the CDK app. If false, the sizes will always be changed back to what they were in the CDK app on deployment. Default: true
            keyName: Name of SSH keypair to grant access to instances. Default: - No SSH access will be possible.
            maxCapacity: Maximum number of instances in the fleet. Default: desiredCapacity
            minCapacity: Minimum number of instances in the fleet. Default: 1
            notificationsTopic: SNS topic to send notifications about fleet changes. Default: - No fleet change notifications will be sent.
            replacingUpdateMinSuccessfulInstancesPercent: Configuration for replacing updates. Only used if updateType == UpdateType.ReplacingUpdate. Specifies how many instances must signal success for the update to succeed. Default: minSuccessfulInstancesPercent
            resourceSignalCount: How many ResourceSignal calls CloudFormation expects before the resource is considered created. Default: 1
            resourceSignalTimeoutSec: The length of time to wait for the resourceSignalCount. The maximum value is 43200 (12 hours). Default: 300 (5 minutes)
            rollingUpdateConfiguration: Configuration for rolling updates. Only used if updateType == UpdateType.RollingUpdate. Default: - RollingUpdateConfiguration with defaults.
            updateType: What to do when an AutoScalingGroup's instance configuration is changed. This is applied when any of the settings on the ASG are changed that affect how the instances should be created (VPC, instance type, startup scripts, etc.). It indicates how the existing instances should be replaced with new instances matching the new config. By default, nothing is done and only new instances are launched with the new config. Default: UpdateType.None
            vpcSubnets: Where to place instances within the VPC. Default: - All Private subnets.
        """
        props: AutoScalingGroupProps = {"instanceType": instance_type, "machineImage": machine_image, "vpc": vpc}

        if role is not None:
            props["role"] = role

        if allow_all_outbound is not None:
            props["allowAllOutbound"] = allow_all_outbound

        if associate_public_ip_address is not None:
            props["associatePublicIpAddress"] = associate_public_ip_address

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if ignore_unmodified_size_properties is not None:
            props["ignoreUnmodifiedSizeProperties"] = ignore_unmodified_size_properties

        if key_name is not None:
            props["keyName"] = key_name

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if notifications_topic is not None:
            props["notificationsTopic"] = notifications_topic

        if replacing_update_min_successful_instances_percent is not None:
            props["replacingUpdateMinSuccessfulInstancesPercent"] = replacing_update_min_successful_instances_percent

        if resource_signal_count is not None:
            props["resourceSignalCount"] = resource_signal_count

        if resource_signal_timeout_sec is not None:
            props["resourceSignalTimeoutSec"] = resource_signal_timeout_sec

        if rolling_update_configuration is not None:
            props["rollingUpdateConfiguration"] = rolling_update_configuration

        if update_type is not None:
            props["updateType"] = update_type

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        jsii.create(AutoScalingGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromAutoScalingGroupName")
    @classmethod
    def from_auto_scaling_group_name(cls, scope: aws_cdk.cdk.Construct, id: str, auto_scaling_group_name: str) -> "IAutoScalingGroup":
        """
        Arguments:
            scope: -
            id: -
            autoScalingGroupName: -
        """
        return jsii.sinvoke(cls, "fromAutoScalingGroupName", [scope, id, auto_scaling_group_name])

    @jsii.member(jsii_name="addLifecycleHook")
    def add_lifecycle_hook(self, id: str, *, lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> "LifecycleHook":
        """Send a message to either an SQS queue or SNS topic when instances launch or terminate.

        Arguments:
            id: -
            props: -
            lifecycleTransition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
            notificationTarget: The target of the lifecycle hook.
            defaultResult: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
            heartbeatTimeoutSec: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
            lifecycleHookName: Name of the lifecycle hook. Default: - Automatically generated name.
            notificationMetadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
            role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props: BasicLifecycleHookProps = {"lifecycleTransition": lifecycle_transition, "notificationTarget": notification_target}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout_sec is not None:
            props["heartbeatTimeoutSec"] = heartbeat_timeout_sec

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if role is not None:
            props["role"] = role

        return jsii.invoke(self, "addLifecycleHook", [id, props])

    @jsii.member(jsii_name="addSecurityGroup")
    def add_security_group(self, security_group: aws_cdk.aws_ec2.ISecurityGroup) -> None:
        """Add the security group to all instances via the launch configuration security groups array.

        Arguments:
            securityGroup: : The security group to add.
        """
        return jsii.invoke(self, "addSecurityGroup", [security_group])

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: aws_cdk.aws_iam.PolicyStatement) -> None:
        """Adds a statement to the IAM role assumed by instances of this fleet.

        Arguments:
            statement: -
        """
        return jsii.invoke(self, "addToRolePolicy", [statement])

    @jsii.member(jsii_name="addUserData")
    def add_user_data(self, *script_lines: str) -> None:
        """Add command to the startup script of fleet instances. The command must be in the scripting language supported by the fleet's OS (i.e. Linux/Windows).

        Arguments:
            scriptLines: -
        """
        return jsii.invoke(self, "addUserData", [script_lines])

    @jsii.member(jsii_name="attachToApplicationTargetGroup")
    def attach_to_application_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Attach to ELBv2 Application Target Group.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToApplicationTargetGroup", [target_group])

    @jsii.member(jsii_name="attachToClassicLB")
    def attach_to_classic_lb(self, load_balancer: aws_cdk.aws_elasticloadbalancing.LoadBalancer) -> None:
        """Attach to a classic load balancer.

        Arguments:
            loadBalancer: -
        """
        return jsii.invoke(self, "attachToClassicLB", [load_balancer])

    @jsii.member(jsii_name="attachToNetworkTargetGroup")
    def attach_to_network_target_group(self, target_group: aws_cdk.aws_elasticloadbalancingv2.NetworkTargetGroup) -> aws_cdk.aws_elasticloadbalancingv2.LoadBalancerTargetProps:
        """Attach to ELBv2 Application Target Group.

        Arguments:
            targetGroup: -
        """
        return jsii.invoke(self, "attachToNetworkTargetGroup", [target_group])

    @jsii.member(jsii_name="scaleOnCpuUtilization")
    def scale_on_cpu_utilization(self, id: str, *, target_utilization_percent: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target CPU utilization.

        Arguments:
            id: -
            props: -
            targetUtilizationPercent: Target average CPU utilization across the task.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: CpuUtilizationScalingProps = {"targetUtilizationPercent": target_utilization_percent}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnCpuUtilization", [id, props])

    @jsii.member(jsii_name="scaleOnIncomingBytes")
    def scale_on_incoming_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network ingress rate.

        Arguments:
            id: -
            props: -
            targetBytesPerSecond: Target average bytes/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnIncomingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnMetric")
    def scale_on_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> "StepScalingPolicy":
        """Scale out or in, in response to a metric.

        Arguments:
            id: -
            props: -
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSeconds: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: BasicStepScalingPolicyProps = {"metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

        return jsii.invoke(self, "scaleOnMetric", [id, props])

    @jsii.member(jsii_name="scaleOnOutgoingBytes")
    def scale_on_outgoing_bytes(self, id: str, *, target_bytes_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target network egress rate.

        Arguments:
            id: -
            props: -
            targetBytesPerSecond: Target average bytes/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: NetworkUtilizationScalingProps = {"targetBytesPerSecond": target_bytes_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnOutgoingBytes", [id, props])

    @jsii.member(jsii_name="scaleOnRequestCount")
    def scale_on_request_count(self, id: str, *, target_requests_per_second: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in to achieve a target request handling rate.

        The AutoScalingGroup must have been attached to an Application Load Balancer
        in order to be able to call this.

        Arguments:
            id: -
            props: -
            targetRequestsPerSecond: Target average requests/seconds on each instance.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: RequestCountScalingProps = {"targetRequestsPerSecond": target_requests_per_second}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleOnRequestCount", [id, props])

    @jsii.member(jsii_name="scaleOnSchedule")
    def scale_on_schedule(self, id: str, *, schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> "ScheduledAction":
        """Scale out or in based on time.

        Arguments:
            id: -
            props: -
            schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
            desiredCapacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
            endTime: When this scheduled action expires. Default: - The rule never expires.
            maxCapacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
            minCapacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
            startTime: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props: BasicScheduledActionProps = {"schedule": schedule}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        return jsii.invoke(self, "scaleOnSchedule", [id, props])

    @jsii.member(jsii_name="scaleToTrackMetric")
    def scale_to_track_metric(self, id: str, *, metric: aws_cdk.aws_cloudwatch.Metric, target_value: jsii.Number, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> "TargetTrackingScalingPolicy":
        """Scale out or in in order to keep a metric around a target value.

        Arguments:
            id: -
            props: -
            metric: Metric to track. The metric must represent a utilization, so that if it's higher than the target value, your ASG should scale out, and if it's lower it should scale in.
            targetValue: Value to keep the metric around.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: MetricTargetTrackingProps = {"metric": metric, "targetValue": target_value}

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        return jsii.invoke(self, "scaleToTrackMetric", [id, props])

    @property
    @jsii.member(jsii_name="autoScalingGroupName")
    def auto_scaling_group_name(self) -> str:
        """Name of the AutoScalingGroup."""
        return jsii.get(self, "autoScalingGroupName")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Allows specify security group connections for instances of this fleet."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="osType")
    def os_type(self) -> aws_cdk.aws_ec2.OperatingSystemType:
        """The type of OS instances of this fleet are running."""
        return jsii.get(self, "osType")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The IAM role assumed by instances of this fleet."""
        return jsii.get(self, "role")

    @property
    @jsii.member(jsii_name="albTargetGroup")
    def _alb_target_group(self) -> typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]:
        return jsii.get(self, "albTargetGroup")

    @_alb_target_group.setter
    def _alb_target_group(self, value: typing.Optional[aws_cdk.aws_elasticloadbalancingv2.ApplicationTargetGroup]):
        return jsii.set(self, "albTargetGroup", value)


@jsii.implements(aws_cdk.aws_autoscaling_api.ILifecycleHook)
class LifecycleHook(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.LifecycleHook"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", lifecycle_transition: "LifecycleTransition", notification_target: aws_cdk.aws_autoscaling_api.ILifecycleHookTarget, default_result: typing.Optional["DefaultResult"]=None, heartbeat_timeout_sec: typing.Optional[jsii.Number]=None, lifecycle_hook_name: typing.Optional[str]=None, notification_metadata: typing.Optional[str]=None, role: typing.Optional[aws_cdk.aws_iam.IRole]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            autoScalingGroup: The AutoScalingGroup to add the lifecycle hook to.
            lifecycleTransition: The state of the Amazon EC2 instance to which you want to attach the lifecycle hook.
            notificationTarget: The target of the lifecycle hook.
            defaultResult: The action the Auto Scaling group takes when the lifecycle hook timeout elapses or if an unexpected failure occurs. Default: Continue
            heartbeatTimeoutSec: Maximum time between calls to RecordLifecycleActionHeartbeat for the hook. If the lifecycle hook times out, perform the action in DefaultResult. Default: - No heartbeat timeout.
            lifecycleHookName: Name of the lifecycle hook. Default: - Automatically generated name.
            notificationMetadata: Additional data to pass to the lifecycle hook target. Default: - No metadata.
            role: The role that allows publishing to the notification target. Default: - A role is automatically created.
        """
        props: LifecycleHookProps = {"autoScalingGroup": auto_scaling_group, "lifecycleTransition": lifecycle_transition, "notificationTarget": notification_target}

        if default_result is not None:
            props["defaultResult"] = default_result

        if heartbeat_timeout_sec is not None:
            props["heartbeatTimeoutSec"] = heartbeat_timeout_sec

        if lifecycle_hook_name is not None:
            props["lifecycleHookName"] = lifecycle_hook_name

        if notification_metadata is not None:
            props["notificationMetadata"] = notification_metadata

        if role is not None:
            props["role"] = role

        jsii.create(LifecycleHook, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="lifecycleHookName")
    def lifecycle_hook_name(self) -> str:
        """The name of this lifecycle hook.

        attribute:
            true
        """
        return jsii.get(self, "lifecycleHookName")

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role that allows the ASG to publish to the notification target."""
        return jsii.get(self, "role")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.LifecycleHookProps", jsii_struct_bases=[BasicLifecycleHookProps])
class LifecycleHookProps(BasicLifecycleHookProps, jsii.compat.TypedDict):
    """Properties for a Lifecycle hook."""
    autoScalingGroup: "IAutoScalingGroup"
    """The AutoScalingGroup to add the lifecycle hook to."""

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.LifecycleTransition")
class LifecycleTransition(enum.Enum):
    """What instance transition to attach the hook to."""
    InstanceLaunching = "InstanceLaunching"
    """Execute the hook when an instance is about to be added."""
    InstanceTerminating = "InstanceTerminating"
    """Execute the hook when an instance is about to be terminated."""

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.MetricAggregationType")
class MetricAggregationType(enum.Enum):
    """How the scaling metric is going to be aggregated."""
    Average = "Average"
    """Average."""
    Minimum = "Minimum"
    """Minimum."""
    Maximum = "Maximum"
    """Maximum."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.MetricTargetTrackingProps", jsii_struct_bases=[BaseTargetTrackingProps])
class MetricTargetTrackingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    """Properties for enabling tracking of an arbitrary metric."""
    metric: aws_cdk.aws_cloudwatch.Metric
    """Metric to track.

    The metric must represent a utilization, so that if it's higher than the
    target value, your ASG should scale out, and if it's lower it should
    scale in.
    """

    targetValue: jsii.Number
    """Value to keep the metric around."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.NetworkUtilizationScalingProps", jsii_struct_bases=[BaseTargetTrackingProps])
class NetworkUtilizationScalingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    """Properties for enabling scaling based on network utilization."""
    targetBytesPerSecond: jsii.Number
    """Target average bytes/seconds on each instance."""

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.PredefinedMetric")
class PredefinedMetric(enum.Enum):
    """One of the predefined autoscaling metrics."""
    ASGAverageCPUUtilization = "ASGAverageCPUUtilization"
    """Average CPU utilization of the Auto Scaling group."""
    ASGAverageNetworkIn = "ASGAverageNetworkIn"
    """Average number of bytes received on all network interfaces by the Auto Scaling group."""
    ASGAverageNetworkOut = "ASGAverageNetworkOut"
    """Average number of bytes sent out on all network interfaces by the Auto Scaling group."""
    ALBRequestCountPerTarget = "ALBRequestCountPerTarget"
    """Number of requests completed per target in an Application Load Balancer target group.

    Specify the ALB to look at in the ``resourceLabel`` field.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.RequestCountScalingProps", jsii_struct_bases=[BaseTargetTrackingProps])
class RequestCountScalingProps(BaseTargetTrackingProps, jsii.compat.TypedDict):
    """Properties for enabling scaling based on request/second."""
    targetRequestsPerSecond: jsii.Number
    """Target average requests/seconds on each instance."""

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.RollingUpdateConfiguration", jsii_struct_bases=[])
class RollingUpdateConfiguration(jsii.compat.TypedDict, total=False):
    """Additional settings when a rolling update is selected."""
    maxBatchSize: jsii.Number
    """The maximum number of instances that AWS CloudFormation updates at once.

    Default:
        1
    """

    minInstancesInService: jsii.Number
    """The minimum number of instances that must be in service before more instances are replaced.

    This number affects the speed of the replacement.

    Default:
        0
    """

    minSuccessfulInstancesPercent: jsii.Number
    """The percentage of instances that must signal success for an update to succeed.

    If an instance doesn't send a signal within the time specified in the
    pauseTime property, AWS CloudFormation assumes that the instance wasn't
    updated.

    This number affects the success of the replacement.

    If you specify this property, you must also enable the
    waitOnResourceSignals and pauseTime properties.

    Default:
        100
    """

    pauseTimeSec: jsii.Number
    """The pause time after making a change to a batch of instances.

    This is intended to give those instances time to start software applications.

    Specify PauseTime in the ISO8601 duration format (in the format
    PT#H#M#S, where each # is the number of hours, minutes, and seconds,
    respectively). The maximum PauseTime is one hour (PT1H).

    Default:
        300 if the waitOnResourceSignals property is true, otherwise 0
    """

    suspendProcesses: typing.List["ScalingProcess"]
    """Specifies the Auto Scaling processes to suspend during a stack update.

    Suspending processes prevents Auto Scaling from interfering with a stack
    update.

    Default:
        HealthCheck, ReplaceUnhealthy, AZRebalance, AlarmNotification, ScheduledActions.
    """

    waitOnResourceSignals: bool
    """Specifies whether the Auto Scaling group waits on signals from new instances during an update.

    AWS CloudFormation must receive a signal from each new instance within
    the specified PauseTime before continuing the update.

    To have instances wait for an Elastic Load Balancing health check before
    they signal success, add a health-check verification by using the
    cfn-init helper script. For an example, see the verify_instance_health
    command in the Auto Scaling rolling updates sample template.

    Default:
        true if you specified the minSuccessfulInstancesPercent property, false otherwise
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

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ScalingInterval", jsii_struct_bases=[_ScalingInterval])
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

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.ScalingProcess")
class ScalingProcess(enum.Enum):
    Launch = "Launch"
    Terminate = "Terminate"
    HealthCheck = "HealthCheck"
    ReplaceUnhealthy = "ReplaceUnhealthy"
    AZRebalance = "AZRebalance"
    AlarmNotification = "AlarmNotification"
    ScheduledActions = "ScheduledActions"
    AddToLoadBalancer = "AddToLoadBalancer"

class ScheduledAction(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.ScheduledAction"):
    """Define a scheduled scaling action."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", schedule: str, desired_capacity: typing.Optional[jsii.Number]=None, end_time: typing.Optional[datetime.datetime]=None, max_capacity: typing.Optional[jsii.Number]=None, min_capacity: typing.Optional[jsii.Number]=None, start_time: typing.Optional[datetime.datetime]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            autoScalingGroup: The AutoScalingGroup to apply the scheduled actions to.
            schedule: When to perform this action. Supports cron expressions. For more information about cron expressions, see https://en.wikipedia.org/wiki/Cron.
            desiredCapacity: The new desired capacity. At the scheduled time, set the desired capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new desired capacity.
            endTime: When this scheduled action expires. Default: - The rule never expires.
            maxCapacity: The new maximum capacity. At the scheduled time, set the maximum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new maximum capacity.
            minCapacity: The new minimum capacity. At the scheduled time, set the minimum capacity to the given capacity. At least one of maxCapacity, minCapacity, or desiredCapacity must be supplied. Default: - No new minimum capacity.
            startTime: When this scheduled action becomes active. Default: - The rule is activate immediately.
        """
        props: ScheduledActionProps = {"autoScalingGroup": auto_scaling_group, "schedule": schedule}

        if desired_capacity is not None:
            props["desiredCapacity"] = desired_capacity

        if end_time is not None:
            props["endTime"] = end_time

        if max_capacity is not None:
            props["maxCapacity"] = max_capacity

        if min_capacity is not None:
            props["minCapacity"] = min_capacity

        if start_time is not None:
            props["startTime"] = start_time

        jsii.create(ScheduledAction, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.ScheduledActionProps", jsii_struct_bases=[BasicScheduledActionProps])
class ScheduledActionProps(BasicScheduledActionProps, jsii.compat.TypedDict):
    """Properties for a scheduled action on an AutoScalingGroup."""
    autoScalingGroup: "IAutoScalingGroup"
    """The AutoScalingGroup to apply the scheduled actions to."""

@jsii.implements(aws_cdk.aws_cloudwatch.IAlarmAction)
class StepScalingAction(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.StepScalingAction"):
    """Define a step scaling action.

    This kind of scaling policy adjusts the target capacity in configurable
    steps. The size of the step is configurable based on the metric's distance
    to its alarm threshold.

    This Action must be used as the target of a CloudWatch alarm to take effect.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, metric_aggregation_type: typing.Optional["MetricAggregationType"]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            autoScalingGroup: The auto scaling group.
            adjustmentType: How the adjustment numbers are interpreted. Default: ChangeInCapacity
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: The default cooldown configured on the AutoScalingGroup
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
            metricAggregationType: The aggregation type for the CloudWatch metrics. Default: Average
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: StepScalingActionProps = {"autoScalingGroup": auto_scaling_group}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        if metric_aggregation_type is not None:
            props["metricAggregationType"] = metric_aggregation_type

        if min_adjustment_magnitude is not None:
            props["minAdjustmentMagnitude"] = min_adjustment_magnitude

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
    cooldownSeconds: jsii.Number
    """Period after a scaling completes before another scaling activity can start.

    Default:
        The default cooldown configured on the AutoScalingGroup
    """
    estimatedInstanceWarmupSeconds: jsii.Number
    """Estimated time until a newly launched instance can send metrics to CloudWatch.

    Default:
        Same as the cooldown
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

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.StepScalingActionProps", jsii_struct_bases=[_StepScalingActionProps])
class StepScalingActionProps(_StepScalingActionProps):
    """Properties for a scaling policy."""
    autoScalingGroup: "IAutoScalingGroup"
    """The auto scaling group."""

class StepScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicy"):
    """Define a acaling strategy which scales depending on absolute values of some metric.

    You can specify the scaling behavior for various values of the metric.

    Implemented using one or more CloudWatch alarms and Step Scaling Policies.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", metric: aws_cdk.aws_cloudwatch.Metric, scaling_steps: typing.List["ScalingInterval"], adjustment_type: typing.Optional["AdjustmentType"]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None, min_adjustment_magnitude: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            autoScalingGroup: The auto scaling group.
            metric: Metric to scale on.
            scalingSteps: The intervals for scaling. Maps a range of metric values to a particular scaling behavior.
            adjustmentType: How the adjustment numbers inside 'intervals' are interpreted. Default: ChangeInCapacity
            cooldownSeconds: Grace period after scaling activity. Default: Default cooldown period on your AutoScalingGroup
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: Same as the cooldown
            minAdjustmentMagnitude: Minimum absolute number to adjust capacity with as result of percentage scaling. Only when using AdjustmentType = PercentChangeInCapacity, this number controls the minimum absolute effect size. Default: No minimum scaling effect
        """
        props: StepScalingPolicyProps = {"autoScalingGroup": auto_scaling_group, "metric": metric, "scalingSteps": scaling_steps}

        if adjustment_type is not None:
            props["adjustmentType"] = adjustment_type

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

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


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.StepScalingPolicyProps", jsii_struct_bases=[BasicStepScalingPolicyProps])
class StepScalingPolicyProps(BasicStepScalingPolicyProps, jsii.compat.TypedDict):
    autoScalingGroup: "IAutoScalingGroup"
    """The auto scaling group."""

class TargetTrackingScalingPolicy(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicy"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, auto_scaling_group: "IAutoScalingGroup", target_value: jsii.Number, custom_metric: typing.Optional[aws_cdk.aws_cloudwatch.Metric]=None, predefined_metric: typing.Optional["PredefinedMetric"]=None, resource_label: typing.Optional[str]=None, cooldown_seconds: typing.Optional[jsii.Number]=None, disable_scale_in: typing.Optional[bool]=None, estimated_instance_warmup_seconds: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            autoScalingGroup: -
            targetValue: The target value for the metric.
            customMetric: A custom metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No custom metric.
            predefinedMetric: A predefined metric for application autoscaling. The metric must track utilization. Scaling out will happen if the metric is higher than the target value, scaling in will happen in the metric is lower than the target value. Exactly one of customMetric or predefinedMetric must be specified. Default: - No predefined metric.
            resourceLabel: The resource label associated with the predefined metric. Should be supplied if the predefined metric is ALBRequestCountPerTarget, and the format should be: app///targetgroup// Default: - No resource label.
            cooldownSeconds: Period after a scaling completes before another scaling activity can start. Default: - The default cooldown configured on the AutoScalingGroup.
            disableScaleIn: Indicates whether scale in by the target tracking policy is disabled. If the value is true, scale in is disabled and the target tracking policy won't remove capacity from the autoscaling group. Otherwise, scale in is enabled and the target tracking policy can remove capacity from the group. Default: false
            estimatedInstanceWarmupSeconds: Estimated time until a newly launched instance can send metrics to CloudWatch. Default: - Same as the cooldown.
        """
        props: TargetTrackingScalingPolicyProps = {"autoScalingGroup": auto_scaling_group, "targetValue": target_value}

        if custom_metric is not None:
            props["customMetric"] = custom_metric

        if predefined_metric is not None:
            props["predefinedMetric"] = predefined_metric

        if resource_label is not None:
            props["resourceLabel"] = resource_label

        if cooldown_seconds is not None:
            props["cooldownSeconds"] = cooldown_seconds

        if disable_scale_in is not None:
            props["disableScaleIn"] = disable_scale_in

        if estimated_instance_warmup_seconds is not None:
            props["estimatedInstanceWarmupSeconds"] = estimated_instance_warmup_seconds

        jsii.create(TargetTrackingScalingPolicy, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="scalingPolicyArn")
    def scaling_policy_arn(self) -> str:
        """ARN of the scaling policy."""
        return jsii.get(self, "scalingPolicyArn")


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling.TargetTrackingScalingPolicyProps", jsii_struct_bases=[BasicTargetTrackingScalingPolicyProps])
class TargetTrackingScalingPolicyProps(BasicTargetTrackingScalingPolicyProps, jsii.compat.TypedDict):
    """Properties for a concrete TargetTrackingPolicy.

    Adds the scalingTarget.
    """
    autoScalingGroup: "IAutoScalingGroup"

@jsii.enum(jsii_type="@aws-cdk/aws-autoscaling.UpdateType")
class UpdateType(enum.Enum):
    """The type of update to perform on instances in this AutoScalingGroup."""
    None_ = "None"
    """Don't do anything."""
    ReplacingUpdate = "ReplacingUpdate"
    """Replace the entire AutoScalingGroup.

    Builds a new AutoScalingGroup first, then delete the old one.
    """
    RollingUpdate = "RollingUpdate"
    """Replace the instances in the AutoScalingGroup."""

__all__ = ["AdjustmentTier", "AdjustmentType", "AutoScalingGroup", "AutoScalingGroupProps", "BaseTargetTrackingProps", "BasicLifecycleHookProps", "BasicScheduledActionProps", "BasicStepScalingPolicyProps", "BasicTargetTrackingScalingPolicyProps", "CfnAutoScalingGroup", "CfnAutoScalingGroupProps", "CfnLaunchConfiguration", "CfnLaunchConfigurationProps", "CfnLifecycleHook", "CfnLifecycleHookProps", "CfnScalingPolicy", "CfnScalingPolicyProps", "CfnScheduledAction", "CfnScheduledActionProps", "CommonAutoScalingGroupProps", "CpuUtilizationScalingProps", "Cron", "DefaultResult", "IAutoScalingGroup", "LifecycleHook", "LifecycleHookProps", "LifecycleTransition", "MetricAggregationType", "MetricTargetTrackingProps", "NetworkUtilizationScalingProps", "PredefinedMetric", "RequestCountScalingProps", "RollingUpdateConfiguration", "ScalingInterval", "ScalingProcess", "ScheduledAction", "ScheduledActionProps", "StepScalingAction", "StepScalingActionProps", "StepScalingPolicy", "StepScalingPolicyProps", "TargetTrackingScalingPolicy", "TargetTrackingScalingPolicyProps", "UpdateType", "__jsii_assembly__"]

publication.publish()
