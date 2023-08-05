import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-codedeploy-api", "0.31.0", __name__, "aws-codedeploy-api@0.31.0.jsii.tgz")
@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy-api.ILoadBalancer")
class ILoadBalancer(jsii.compat.Protocol):
    """An interface of an abstract laod balancer, as needed by CodeDeploy."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerProxy

    @jsii.member(jsii_name="asCodeDeployLoadBalancer")
    def as_code_deploy_load_balancer(self) -> "ILoadBalancerProps":
        """Specify the CodeDeploy-required properties of this load balancer."""
        ...


class _ILoadBalancerProxy():
    """An interface of an abstract laod balancer, as needed by CodeDeploy."""
    __jsii_type__ = "@aws-cdk/aws-codedeploy-api.ILoadBalancer"
    @jsii.member(jsii_name="asCodeDeployLoadBalancer")
    def as_code_deploy_load_balancer(self) -> "ILoadBalancerProps":
        """Specify the CodeDeploy-required properties of this load balancer."""
        return jsii.invoke(self, "asCodeDeployLoadBalancer", [])


@jsii.interface(jsii_type="@aws-cdk/aws-codedeploy-api.ILoadBalancerProps")
class ILoadBalancerProps(jsii.compat.Protocol):
    """The properties CodeDeploy requires of a load balancer."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ILoadBalancerPropsProxy

    @property
    @jsii.member(jsii_name="generation")
    def generation(self) -> "LoadBalancerGeneration":
        ...

    @generation.setter
    def generation(self, value: "LoadBalancerGeneration"):
        ...

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        ...

    @name.setter
    def name(self, value: str):
        ...


class _ILoadBalancerPropsProxy():
    """The properties CodeDeploy requires of a load balancer."""
    __jsii_type__ = "@aws-cdk/aws-codedeploy-api.ILoadBalancerProps"
    @property
    @jsii.member(jsii_name="generation")
    def generation(self) -> "LoadBalancerGeneration":
        return jsii.get(self, "generation")

    @generation.setter
    def generation(self, value: "LoadBalancerGeneration"):
        return jsii.set(self, "generation", value)

    @property
    @jsii.member(jsii_name="name")
    def name(self) -> str:
        return jsii.get(self, "name")

    @name.setter
    def name(self, value: str):
        return jsii.set(self, "name", value)


@jsii.enum(jsii_type="@aws-cdk/aws-codedeploy-api.LoadBalancerGeneration")
class LoadBalancerGeneration(enum.Enum):
    """The generations of AWS load balancing solutions."""
    First = "First"
    """The first generation (ELB Classic)."""
    Second = "Second"
    """The second generation (ALB and NLB)."""

__all__ = ["ILoadBalancer", "ILoadBalancerProps", "LoadBalancerGeneration", "__jsii_assembly__"]

publication.publish()
