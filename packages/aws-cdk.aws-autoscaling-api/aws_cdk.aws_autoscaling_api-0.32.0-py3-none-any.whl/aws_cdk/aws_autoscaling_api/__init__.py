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
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-autoscaling-api", "0.32.0", __name__, "aws-autoscaling-api@0.32.0.jsii.tgz")
@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-api.ILifecycleHook")
class ILifecycleHook(jsii.compat.Protocol):
    """A basic lifecycle hook object."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookProxy

    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role for the lifecycle hook to execute."""
        ...


class _ILifecycleHookProxy():
    """A basic lifecycle hook object."""
    __jsii_type__ = "@aws-cdk/aws-autoscaling-api.ILifecycleHook"
    @property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        """The role for the lifecycle hook to execute."""
        return jsii.get(self, "role")


@jsii.interface(jsii_type="@aws-cdk/aws-autoscaling-api.ILifecycleHookTarget")
class ILifecycleHookTarget(jsii.compat.Protocol):
    """Interface for autoscaling lifecycle hook targets."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILifecycleHookTargetProxy

    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: "ILifecycleHook") -> "LifecycleHookTargetProps":
        """Called when this object is used as the target of a lifecycle hook.

        Arguments:
            lifecycleHook: -
        """
        ...


class _ILifecycleHookTargetProxy():
    """Interface for autoscaling lifecycle hook targets."""
    __jsii_type__ = "@aws-cdk/aws-autoscaling-api.ILifecycleHookTarget"
    @jsii.member(jsii_name="asLifecycleHookTarget")
    def as_lifecycle_hook_target(self, lifecycle_hook: "ILifecycleHook") -> "LifecycleHookTargetProps":
        """Called when this object is used as the target of a lifecycle hook.

        Arguments:
            lifecycleHook: -
        """
        return jsii.invoke(self, "asLifecycleHookTarget", [lifecycle_hook])


@jsii.data_type(jsii_type="@aws-cdk/aws-autoscaling-api.LifecycleHookTargetProps", jsii_struct_bases=[])
class LifecycleHookTargetProps(jsii.compat.TypedDict):
    """Properties to add the target to a lifecycle hook."""
    notificationTargetArn: str
    """The ARN to use as the notification target."""

__all__ = ["ILifecycleHook", "ILifecycleHookTarget", "LifecycleHookTargetProps", "__jsii_assembly__"]

publication.publish()
