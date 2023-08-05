import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.aws_s3
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/assets", "0.31.0", __name__, "assets@0.31.0.jsii.tgz")
class Asset(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.Asset"):
    """An asset represents a local file or directory, which is automatically uploaded to S3 and then can be referenced within a CDK application."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, packaging: "AssetPackaging", path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            packaging: The packaging type for this asset.
            path: The disk location of the asset.
            readers: A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later.
        """
        props: AssetProps = {"packaging": packaging, "path": path}

        if readers is not None:
            props["readers"] = readers

        jsii.create(Asset, self, [scope, id, props])

    @jsii.member(jsii_name="addResourceMetadata")
    def add_resource_metadata(self, resource: aws_cdk.cdk.CfnResource, resource_property: str) -> None:
        """Adds CloudFormation template metadata to the specified resource with information that indicates which resource property is mapped to this local asset.

        This can be used by tools such as SAM CLI to provide local
        experience such as local invocation and debugging of Lambda functions.

        Asset metadata will only be included if the stack is synthesized with the
        "aws:cdk:enable-asset-metadata" context key defined, which is the default
        behavior when synthesizing via the CDK Toolkit.

        Arguments:
            resource: The CloudFormation resource which is using this asset.
            resourceProperty: The property name where this asset is referenced (e.g. "Code" for AWS::Lambda::Function).

        See:
            https://github.com/awslabs/aws-cdk/issues/1432
        """
        return jsii.invoke(self, "addResourceMetadata", [resource, resource_property])

    @jsii.member(jsii_name="grantRead")
    def grant_read(self, grantee: aws_cdk.aws_iam.IGrantable) -> None:
        """Grants read permissions to the principal on the asset's S3 object.

        Arguments:
            grantee: -
        """
        return jsii.invoke(self, "grantRead", [grantee])

    @property
    @jsii.member(jsii_name="assetPath")
    def asset_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.
        """
        return jsii.get(self, "assetPath")

    @property
    @jsii.member(jsii_name="bucket")
    def bucket(self) -> aws_cdk.aws_s3.IBucket:
        """The S3 bucket in which this asset resides."""
        return jsii.get(self, "bucket")

    @property
    @jsii.member(jsii_name="isZipArchive")
    def is_zip_archive(self) -> bool:
        """Indicates if this asset is a zip archive.

        Allows constructs to ensure that the
        correct file type was used.
        """
        return jsii.get(self, "isZipArchive")

    @property
    @jsii.member(jsii_name="s3BucketName")
    def s3_bucket_name(self) -> str:
        """Attribute that represents the name of the bucket this asset exists in."""
        return jsii.get(self, "s3BucketName")

    @property
    @jsii.member(jsii_name="s3ObjectKey")
    def s3_object_key(self) -> str:
        """Attribute which represents the S3 object key of this asset."""
        return jsii.get(self, "s3ObjectKey")

    @property
    @jsii.member(jsii_name="s3Url")
    def s3_url(self) -> str:
        """Attribute which represents the S3 URL of this asset.

        Example::
            https://s3.us-west-1.amazonaws.com/bucket/key
        """
        return jsii.get(self, "s3Url")


@jsii.enum(jsii_type="@aws-cdk/assets.AssetPackaging")
class AssetPackaging(enum.Enum):
    """Defines the way an asset is packaged before it is uploaded to S3."""
    ZipDirectory = "ZipDirectory"
    """Path refers to a directory on disk, the contents of the directory is archived into a .zip."""
    File = "File"
    """Path refers to a single file on disk.

    The file is uploaded as-is.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _AssetProps(jsii.compat.TypedDict, total=False):
    readers: typing.List[aws_cdk.aws_iam.IGrantable]
    """A list of principals that should be able to read this asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later."""

@jsii.data_type(jsii_type="@aws-cdk/assets.AssetProps", jsii_struct_bases=[_AssetProps])
class AssetProps(_AssetProps):
    packaging: "AssetPackaging"
    """The packaging type for this asset."""

    path: str
    """The disk location of the asset."""

class FileAsset(Asset, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.FileAsset"):
    """An asset that represents a file on disk."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            path: File path.
            readers: A list of principals that should be able to read this file asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later.
        """
        props: FileAssetProps = {"path": path}

        if readers is not None:
            props["readers"] = readers

        jsii.create(FileAsset, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _FileAssetProps(jsii.compat.TypedDict, total=False):
    readers: typing.List[aws_cdk.aws_iam.IGrantable]
    """A list of principals that should be able to read this file asset from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later."""

@jsii.data_type(jsii_type="@aws-cdk/assets.FileAssetProps", jsii_struct_bases=[_FileAssetProps])
class FileAssetProps(_FileAssetProps):
    path: str
    """File path."""

class Staging(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.Staging"):
    """Stages a file or directory from a location on the file system into a staging directory.

    This is controlled by the context key 'aws:cdk:asset-staging-dir' and enabled
    by the CLI by default in order to ensure that when the CDK app exists, all
    assets are available for deployment. Otherwise, if an app references assets
    in temporary locations, those will not be available when it exists (see
    https://github.com/awslabs/aws-cdk/issues/1716).

    The ``stagedPath`` property is a stringified token that represents the location
    of the file or directory after staging. It will be resolved only during the
    "prepare" stage and may be either the original path or the staged path
    depending on the context setting.

    The file/directory are staged based on their content hash (fingerprint). This
    means that only if content was changed, copy will happen.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, source_path: str) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            sourcePath: -
        """
        props: StagingProps = {"sourcePath": source_path}

        jsii.create(Staging, self, [scope, id, props])

    @jsii.member(jsii_name="prepare")
    def _prepare(self) -> None:
        """Perform final modifications before synthesis.

        This method can be implemented by derived constructs in order to perform
        final changes before synthesis. prepare() will be called after child
        constructs have been prepared.

        This is an advanced framework feature. Only use this if you
        understand the implications.
        """
        return jsii.invoke(self, "prepare", [])

    @property
    @jsii.member(jsii_name="sourcePath")
    def source_path(self) -> str:
        """The path of the asset as it was referenced by the user."""
        return jsii.get(self, "sourcePath")

    @property
    @jsii.member(jsii_name="stagedPath")
    def staged_path(self) -> str:
        """The path to the asset (stringinfied token).

        If asset staging is disabled, this will just be the original path.
        If asset staging is enabled it will be the staged path.
        """
        return jsii.get(self, "stagedPath")


@jsii.data_type(jsii_type="@aws-cdk/assets.StagingProps", jsii_struct_bases=[])
class StagingProps(jsii.compat.TypedDict):
    sourcePath: str

class ZipDirectoryAsset(Asset, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets.ZipDirectoryAsset"):
    """An asset that represents a ZIP archive of a directory on disk."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, path: str, readers: typing.Optional[typing.List[aws_cdk.aws_iam.IGrantable]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            path: Path of the directory.
            readers: A list of principals that should be able to read this ZIP file from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later.
        """
        props: ZipDirectoryAssetProps = {"path": path}

        if readers is not None:
            props["readers"] = readers

        jsii.create(ZipDirectoryAsset, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _ZipDirectoryAssetProps(jsii.compat.TypedDict, total=False):
    readers: typing.List[aws_cdk.aws_iam.IGrantable]
    """A list of principals that should be able to read this ZIP file from S3. You can use ``asset.grantRead(principal)`` to grant read permissions later."""

@jsii.data_type(jsii_type="@aws-cdk/assets.ZipDirectoryAssetProps", jsii_struct_bases=[_ZipDirectoryAssetProps])
class ZipDirectoryAssetProps(_ZipDirectoryAssetProps):
    path: str
    """Path of the directory."""

__all__ = ["Asset", "AssetPackaging", "AssetProps", "FileAsset", "FileAssetProps", "Staging", "StagingProps", "ZipDirectoryAsset", "ZipDirectoryAssetProps", "__jsii_assembly__"]

publication.publish()
