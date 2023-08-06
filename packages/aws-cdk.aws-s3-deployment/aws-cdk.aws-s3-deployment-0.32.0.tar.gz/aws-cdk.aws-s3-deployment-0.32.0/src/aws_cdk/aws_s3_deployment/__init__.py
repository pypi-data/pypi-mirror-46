import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.assets
import aws_cdk.aws_cloudformation
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-s3-deployment", "0.32.0", __name__, "aws-s3-deployment@0.32.0.jsii.tgz")
class BucketDeployment(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.BucketDeployment"):
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, destination_bucket: aws_cdk.aws_s3.IBucket, source: "ISource", destination_key_prefix: typing.Optional[str]=None, retain_on_delete: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            destinationBucket: The S3 bucket to sync the contents of the zip file to.
            source: The source from which to deploy the contents of this bucket.
            destinationKeyPrefix: Key prefix in the destination bucket. Default: "/" (unzip to root of the destination bucket)
            retainOnDelete: If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated. NOTICE: if this is set to "false" and destination bucket/prefix is updated, all files in the previous destination will first be deleted and then uploaded to the new destination location. This could have availablity implications on your users. Default: true - when resource is deleted/updated, files are retained
        """
        props: BucketDeploymentProps = {"destinationBucket": destination_bucket, "source": source}

        if destination_key_prefix is not None:
            props["destinationKeyPrefix"] = destination_key_prefix

        if retain_on_delete is not None:
            props["retainOnDelete"] = retain_on_delete

        jsii.create(BucketDeployment, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _BucketDeploymentProps(jsii.compat.TypedDict, total=False):
    destinationKeyPrefix: str
    """Key prefix in the destination bucket.

    Default:
        "/" (unzip to root of the destination bucket)
    """
    retainOnDelete: bool
    """If this is set to "false", the destination files will be deleted when the resource is deleted or the destination is updated.

    NOTICE: if this is set to "false" and destination bucket/prefix is updated,
    all files in the previous destination will first be deleted and then
    uploaded to the new destination location. This could have availablity
    implications on your users.

    Default:
        true - when resource is deleted/updated, files are retained
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.BucketDeploymentProps", jsii_struct_bases=[_BucketDeploymentProps])
class BucketDeploymentProps(_BucketDeploymentProps):
    destinationBucket: aws_cdk.aws_s3.IBucket
    """The S3 bucket to sync the contents of the zip file to."""

    source: "ISource"
    """The source from which to deploy the contents of this bucket."""

@jsii.interface(jsii_type="@aws-cdk/aws-s3-deployment.ISource")
class ISource(jsii.compat.Protocol):
    """Represents a source for bucket deployments."""
    @staticmethod
    def __jsii_proxy_class__():
        return _ISourceProxy

    @jsii.member(jsii_name="bind")
    def bind(self, context: aws_cdk.cdk.Construct) -> "SourceProps":
        """Binds the source to a bucket deployment.

        Arguments:
            context: The construct tree context.
        """
        ...


class _ISourceProxy():
    """Represents a source for bucket deployments."""
    __jsii_type__ = "@aws-cdk/aws-s3-deployment.ISource"
    @jsii.member(jsii_name="bind")
    def bind(self, context: aws_cdk.cdk.Construct) -> "SourceProps":
        """Binds the source to a bucket deployment.

        Arguments:
            context: The construct tree context.
        """
        return jsii.invoke(self, "bind", [context])


class Source(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-s3-deployment.Source"):
    """Specifies bucket deployment source.

    Usage::

        Source.bucket(bucket, key)
        Source.asset('/local/path/to/directory')
        Source.asset('/local/path/to/a/file.zip')
    """
    @jsii.member(jsii_name="asset")
    @classmethod
    def asset(cls, path: str) -> "ISource":
        """Uses a local asset as the deployment source.

        Arguments:
            path: The path to a local .zip file or a directory.
        """
        return jsii.sinvoke(cls, "asset", [path])

    @jsii.member(jsii_name="bucket")
    @classmethod
    def bucket(cls, bucket: aws_cdk.aws_s3.IBucket, zip_object_key: str) -> "ISource":
        """Uses a .zip file stored in an S3 bucket as the source for the destination bucket contents.

        Arguments:
            bucket: The S3 Bucket.
            zipObjectKey: The S3 object key of the zip file with contents.
        """
        return jsii.sinvoke(cls, "bucket", [bucket, zip_object_key])


@jsii.data_type(jsii_type="@aws-cdk/aws-s3-deployment.SourceProps", jsii_struct_bases=[])
class SourceProps(jsii.compat.TypedDict):
    bucket: aws_cdk.aws_s3.IBucket
    """The source bucket to deploy from."""

    zipObjectKey: str
    """An S3 object key in the source bucket that points to a zip file."""

__all__ = ["BucketDeployment", "BucketDeploymentProps", "ISource", "Source", "SourceProps", "__jsii_assembly__"]

publication.publish()
