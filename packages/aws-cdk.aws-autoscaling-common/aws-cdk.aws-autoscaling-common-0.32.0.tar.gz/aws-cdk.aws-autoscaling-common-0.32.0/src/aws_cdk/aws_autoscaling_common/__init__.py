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
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling-common", "0.32.0", __name__, "aws-autoscaling-common@0.32.0.jsii.tgz")
@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.Alarms", jsii_struct_bases=[])
class Alarms(jsii.compat.TypedDict, total=False):
    lowerAlarmIntervalIndex: jsii.Number

    upperAlarmIntervalIndex: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.ArbitraryIntervals", jsii_struct_bases=[])
class ArbitraryIntervals(jsii.compat.TypedDict):
    absolute: bool

    intervals: typing.List["ScalingInterval"]

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CompleteScalingInterval(jsii.compat.TypedDict, total=False):
    change: jsii.Number

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.CompleteScalingInterval", jsii_struct_bases=[_CompleteScalingInterval])
class CompleteScalingInterval(_CompleteScalingInterval):
    lower: jsii.Number

    upper: jsii.Number

@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-common.IRandomGenerator")
class IRandomGenerator(jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IRandomGeneratorProxy

    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> bool:
        ...

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        """
        Arguments:
            min: -
            max: -
        """
        ...


class _IRandomGeneratorProxy():
    __jsii_type__ = "@aws-cdk/aws-autoscaling-common.IRandomGenerator"
    @jsii.member(jsii_name="nextBoolean")
    def next_boolean(self) -> bool:
        return jsii.invoke(self, "nextBoolean", [])

    @jsii.member(jsii_name="nextInt")
    def next_int(self, min: jsii.Number, max: jsii.Number) -> jsii.Number:
        """
        Arguments:
            min: -
            max: -
        """
        return jsii.invoke(self, "nextInt", [min, max])


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

@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-common.ScalingInterval", jsii_struct_bases=[_ScalingInterval])
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

__all__ = ["Alarms", "ArbitraryIntervals", "CompleteScalingInterval", "IRandomGenerator", "ScalingInterval", "__jsii_assembly__"]

publication.publish()
