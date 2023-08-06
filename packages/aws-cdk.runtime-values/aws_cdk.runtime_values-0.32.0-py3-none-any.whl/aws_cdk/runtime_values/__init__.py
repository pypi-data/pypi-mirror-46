import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_ssm
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/runtime-values", "0.32.0", __name__, "runtime-values@0.32.0.jsii.tgz")
class RuntimeValue(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/runtime-values.RuntimeValue"):
    """Defines a value published from construction code which needs to be accessible by runtime code."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, package: str, value: typing.Any) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            package: A namespace for the runtime value. It is recommended to use the name of the library/package that advertises this value.
            value: The value to advertise. Can be either a primitive value or a token.
        """
        props: RuntimeValueProps = {"package": package, "value": value}

        jsii.create(RuntimeValue, self, [scope, id, props])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grants a principal read permissions on this runtime value.

        Arguments:
            grantee: The principal (e.g. Role, User, Group).
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @classproperty
    @jsii.member(jsii_name="ENV_NAME")
    def ENV_NAME(cls) -> str:
        """The recommended name of the environment variable to use to set the stack name from which the runtime value is published."""
        return jsii.sget(cls, "ENV_NAME")

    @property
    @jsii.member(jsii_name="envValue")
    def env_value(self) -> str:
        """The value to assign to the ``RTV_STACK_NAME`` environment variable."""
        return jsii.get(self, "envValue")

    @property
    @jsii.member(jsii_name="parameterArn")
    def parameter_arn(self) -> str:
        """The ARN fo the SSM parameter used for this runtime value."""
        return jsii.get(self, "parameterArn")

    @property
    @jsii.member(jsii_name="parameterName")
    def parameter_name(self) -> str:
        """The name of the runtime parameter."""
        return jsii.get(self, "parameterName")


@jsii.data_type(jsii_type="@aws-cdk/runtime-values.RuntimeValueProps", jsii_struct_bases=[])
class RuntimeValueProps(jsii.compat.TypedDict):
    package: str
    """A namespace for the runtime value. It is recommended to use the name of the library/package that advertises this value."""

    value: typing.Any
    """The value to advertise.

    Can be either a primitive value or a token.
    """

__all__ = ["RuntimeValue", "RuntimeValueProps", "__jsii_assembly__"]

publication.publish()
