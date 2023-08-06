import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3-notifications", "0.32.0", __name__, "aws-s3-notifications@0.32.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _BucketNotificationDestinationProps(jsii.compat.TypedDict, total=False):
    dependencies: typing.List[aws_cdk.cdk.IDependable]
    """Any additional dependencies that should be resolved before the bucket notification can be configured (for example, the SNS Topic Policy resource)."""

@jsii.data_type(jsii_type="@aws-cdk/aws-s3-notifications.BucketNotificationDestinationProps", jsii_struct_bases=[_BucketNotificationDestinationProps])
class BucketNotificationDestinationProps(_BucketNotificationDestinationProps):
    """Represents the properties of a notification destination."""
    arn: str
    """The ARN of the destination (i.e. Lambda, SNS, SQS)."""

    type: "BucketNotificationDestinationType"
    """The notification type."""

@jsii.enum(jsii_type="@aws-cdk/aws-s3-notifications.BucketNotificationDestinationType")
class BucketNotificationDestinationType(enum.Enum):
    """Supported types of notification destinations."""
    Lambda = "Lambda"
    Queue = "Queue"
    Topic = "Topic"

@jsii.interface(jsii_type="@aws-cdk/aws-s3-notifications.IBucketNotificationDestination")
class IBucketNotificationDestination(jsii.compat.Protocol):
    """Implemented by constructs that can be used as bucket notification destinations."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IBucketNotificationDestinationProxy

    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> "BucketNotificationDestinationProps":
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        Arguments:
            bucketArn: The ARN of the bucket.
            bucketId: A unique ID of this bucket in the stack.
        """
        ...


class _IBucketNotificationDestinationProxy():
    """Implemented by constructs that can be used as bucket notification destinations."""
    __jsii_type__ = "@aws-cdk/aws-s3-notifications.IBucketNotificationDestination"
    @jsii.member(jsii_name="asBucketNotificationDestination")
    def as_bucket_notification_destination(self, bucket_arn: str, bucket_id: str) -> "BucketNotificationDestinationProps":
        """Registers this resource to receive notifications for the specified bucket.

        This method will only be called once for each destination/bucket
        pair and the result will be cached, so there is no need to implement
        idempotency in each destination.

        Arguments:
            bucketArn: The ARN of the bucket.
            bucketId: A unique ID of this bucket in the stack.
        """
        return jsii.invoke(self, "asBucketNotificationDestination", [bucket_arn, bucket_id])


__all__ = ["BucketNotificationDestinationProps", "BucketNotificationDestinationType", "IBucketNotificationDestination", "__jsii_assembly__"]

publication.publish()
