import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_ecs
import aws_cdk.aws_events
import aws_cdk.aws_events_targets
import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-ecs-patterns", "0.31.0", __name__, "aws-ecs-patterns@0.31.0.jsii.tgz")
class ScheduledEc2Task(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2Task"):
    """A scheduled Ec2 task that will be initiated off of cloudwatch events."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, cluster: aws_cdk.aws_ecs.ICluster, image: aws_cdk.aws_ecs.ContainerImage, schedule_expression: str, command: typing.Optional[typing.List[str]]=None, cpu: typing.Optional[jsii.Number]=None, desired_task_count: typing.Optional[jsii.Number]=None, environment: typing.Optional[typing.Mapping[str,str]]=None, memory_limit_mi_b: typing.Optional[jsii.Number]=None, memory_reservation_mi_b: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            cluster: The cluster where your service will be deployed.
            image: The image to start.
            scheduleExpression: The schedule or rate (frequency) that determines when CloudWatch Events runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon CloudWatch User Guide.
            command: The CMD value to pass to the container. A string with commands delimited by commas. Default: none
            cpu: The minimum number of CPU units to reserve for the container. Default: none
            desiredTaskCount: Number of desired copies of running tasks. Default: 1
            environment: The environment variables to pass to the container. Default: none
            memoryLimitMiB: The hard limit (in MiB) of memory to present to the container. If your container attempts to exceed the allocated memory, the container is terminated. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory limit.
            memoryReservationMiB: The soft limit (in MiB) of memory to reserve for the container. When system memory is under contention, Docker attempts to keep the container memory within the limit. If the container requires more memory, it can consume up to the value specified by the Memory property or all of the available memory on the container instance—whichever comes first. At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services. Default: - No memory reserved.
        """
        props: ScheduledEc2TaskProps = {"cluster": cluster, "image": image, "scheduleExpression": schedule_expression}

        if command is not None:
            props["command"] = command

        if cpu is not None:
            props["cpu"] = cpu

        if desired_task_count is not None:
            props["desiredTaskCount"] = desired_task_count

        if environment is not None:
            props["environment"] = environment

        if memory_limit_mi_b is not None:
            props["memoryLimitMiB"] = memory_limit_mi_b

        if memory_reservation_mi_b is not None:
            props["memoryReservationMiB"] = memory_reservation_mi_b

        jsii.create(ScheduledEc2Task, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ScheduledEc2TaskProps(jsii.compat.TypedDict, total=False):
    command: typing.List[str]
    """The CMD value to pass to the container.

    A string with commands delimited by commas.

    Default:
        none
    """
    cpu: jsii.Number
    """The minimum number of CPU units to reserve for the container.

    Default:
        none
    """
    desiredTaskCount: jsii.Number
    """Number of desired copies of running tasks.

    Default:
        1
    """
    environment: typing.Mapping[str,str]
    """The environment variables to pass to the container.

    Default:
        none
    """
    memoryLimitMiB: jsii.Number
    """The hard limit (in MiB) of memory to present to the container.

    If your container attempts to exceed the allocated memory, the container
    is terminated.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory limit.
    """
    memoryReservationMiB: jsii.Number
    """The soft limit (in MiB) of memory to reserve for the container.

    When system memory is under contention, Docker attempts to keep the
    container memory within the limit. If the container requires more memory,
    it can consume up to the value specified by the Memory property or all of
    the available memory on the container instance—whichever comes first.

    At least one of memoryLimitMiB and memoryReservationMiB is required for non-Fargate services.

    Default:
        - No memory reserved.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-ecs-patterns.ScheduledEc2TaskProps", jsii_struct_bases=[_ScheduledEc2TaskProps])
class ScheduledEc2TaskProps(_ScheduledEc2TaskProps):
    cluster: aws_cdk.aws_ecs.ICluster
    """The cluster where your service will be deployed."""

    image: aws_cdk.aws_ecs.ContainerImage
    """The image to start."""

    scheduleExpression: str
    """The schedule or rate (frequency) that determines when CloudWatch Events runs the rule.

    For more information, see Schedule Expression Syntax for
    Rules in the Amazon CloudWatch User Guide.

    See:
        http://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
    """

__all__ = ["ScheduledEc2Task", "ScheduledEc2TaskProps", "__jsii_assembly__"]

publication.publish()
