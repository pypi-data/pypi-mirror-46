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
import aws_cdk.aws_ecr
import aws_cdk.aws_iam
import aws_cdk.aws_lambda
import aws_cdk.aws_s3
import aws_cdk.cdk
import aws_cdk.cx_api
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/assets-docker", "0.31.0", __name__, "assets-docker@0.31.0.jsii.tgz")
class DockerImageAsset(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/assets-docker.DockerImageAsset"):
    """An asset that represents a Docker image.

    The image will be created in build time and uploaded to an ECR repository.
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, directory: str, repository_name: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            directory: The directory where the Dockerfile is stored.
            repositoryName: ECR repository name. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: automatically derived from the asset's ID.
        """
        props: DockerImageAssetProps = {"directory": directory}

        if repository_name is not None:
            props["repositoryName"] = repository_name

        jsii.create(DockerImageAsset, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="imageUri")
    def image_uri(self) -> str:
        """The full URI of the image (including a tag).

        Use this reference to pull
        the asset.
        """
        return jsii.get(self, "imageUri")

    @image_uri.setter
    def image_uri(self, value: str):
        return jsii.set(self, "imageUri", value)

    @property
    @jsii.member(jsii_name="repository")
    def repository(self) -> aws_cdk.aws_ecr.IRepository:
        """Repository where the image is stored."""
        return jsii.get(self, "repository")

    @repository.setter
    def repository(self, value: aws_cdk.aws_ecr.IRepository):
        return jsii.set(self, "repository", value)


@jsii.data_type_optionals(jsii_struct_bases=[])
class _DockerImageAssetProps(jsii.compat.TypedDict, total=False):
    repositoryName: str
    """ECR repository name.

    Specify this property if you need to statically address the image, e.g.
    from a Kubernetes Pod. Note, this is only the repository name, without the
    registry and the tag parts.

    Default:
        automatically derived from the asset's ID.
    """

@jsii.data_type(jsii_type="@aws-cdk/assets-docker.DockerImageAssetProps", jsii_struct_bases=[_DockerImageAssetProps])
class DockerImageAssetProps(_DockerImageAssetProps):
    directory: str
    """The directory where the Dockerfile is stored."""

__all__ = ["DockerImageAsset", "DockerImageAssetProps", "__jsii_assembly__"]

publication.publish()
