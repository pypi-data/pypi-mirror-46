import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-efs", "0.32.0", __name__, "aws-efs@0.32.0.jsii.tgz")
class CfnFileSystem(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.CfnFileSystem"):
    """A CloudFormation ``AWS::EFS::FileSystem``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    cloudformationResource:
        AWS::EFS::FileSystem
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, file_system_tags: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ElasticFileSystemTagProperty"]]]]]=None, kms_key_id: typing.Optional[str]=None, performance_mode: typing.Optional[str]=None, provisioned_throughput_in_mibps: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, throughput_mode: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EFS::FileSystem``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            encrypted: ``AWS::EFS::FileSystem.Encrypted``.
            fileSystemTags: ``AWS::EFS::FileSystem.FileSystemTags``.
            kmsKeyId: ``AWS::EFS::FileSystem.KmsKeyId``.
            performanceMode: ``AWS::EFS::FileSystem.PerformanceMode``.
            provisionedThroughputInMibps: ``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.
            throughputMode: ``AWS::EFS::FileSystem.ThroughputMode``.
        """
        props: CfnFileSystemProps = {}

        if encrypted is not None:
            props["encrypted"] = encrypted

        if file_system_tags is not None:
            props["fileSystemTags"] = file_system_tags

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if performance_mode is not None:
            props["performanceMode"] = performance_mode

        if provisioned_throughput_in_mibps is not None:
            props["provisionedThroughputInMibps"] = provisioned_throughput_in_mibps

        if throughput_mode is not None:
            props["throughputMode"] = throughput_mode

        jsii.create(CfnFileSystem, self, [scope, id, props])

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
    @jsii.member(jsii_name="fileSystemId")
    def file_system_id(self) -> str:
        return jsii.get(self, "fileSystemId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnFileSystemProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystem.ElasticFileSystemTagProperty", jsii_struct_bases=[])
    class ElasticFileSystemTagProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-filesystemtags.html
        """
        key: str
        """``CfnFileSystem.ElasticFileSystemTagProperty.Key``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-filesystemtags.html#cfn-efs-filesystem-filesystemtags-key
        """

        value: str
        """``CfnFileSystem.ElasticFileSystemTagProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-efs-filesystem-filesystemtags.html#cfn-efs-filesystem-filesystemtags-value
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnFileSystemProps", jsii_struct_bases=[])
class CfnFileSystemProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::EFS::FileSystem``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html
    """
    encrypted: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::EFS::FileSystem.Encrypted``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-encrypted
    """

    fileSystemTags: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnFileSystem.ElasticFileSystemTagProperty"]]]
    """``AWS::EFS::FileSystem.FileSystemTags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-filesystemtags
    """

    kmsKeyId: str
    """``AWS::EFS::FileSystem.KmsKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-kmskeyid
    """

    performanceMode: str
    """``AWS::EFS::FileSystem.PerformanceMode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-efs-filesystem-performancemode
    """

    provisionedThroughputInMibps: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::EFS::FileSystem.ProvisionedThroughputInMibps``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-provisionedthroughputinmibps
    """

    throughputMode: str
    """``AWS::EFS::FileSystem.ThroughputMode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-filesystem.html#cfn-elasticfilesystem-filesystem-throughputmode
    """

class CfnMountTarget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-efs.CfnMountTarget"):
    """A CloudFormation ``AWS::EFS::MountTarget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
    cloudformationResource:
        AWS::EFS::MountTarget
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, file_system_id: str, security_groups: typing.List[str], subnet_id: str, ip_address: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::EFS::MountTarget``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            fileSystemId: ``AWS::EFS::MountTarget.FileSystemId``.
            securityGroups: ``AWS::EFS::MountTarget.SecurityGroups``.
            subnetId: ``AWS::EFS::MountTarget.SubnetId``.
            ipAddress: ``AWS::EFS::MountTarget.IpAddress``.
        """
        props: CfnMountTargetProps = {"fileSystemId": file_system_id, "securityGroups": security_groups, "subnetId": subnet_id}

        if ip_address is not None:
            props["ipAddress"] = ip_address

        jsii.create(CfnMountTarget, self, [scope, id, props])

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
    @jsii.member(jsii_name="mountTargetId")
    def mount_target_id(self) -> str:
        return jsii.get(self, "mountTargetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnMountTargetProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnMountTargetProps(jsii.compat.TypedDict, total=False):
    ipAddress: str
    """``AWS::EFS::MountTarget.IpAddress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-ipaddress
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-efs.CfnMountTargetProps", jsii_struct_bases=[_CfnMountTargetProps])
class CfnMountTargetProps(_CfnMountTargetProps):
    """Properties for defining a ``AWS::EFS::MountTarget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html
    """
    fileSystemId: str
    """``AWS::EFS::MountTarget.FileSystemId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-filesystemid
    """

    securityGroups: typing.List[str]
    """``AWS::EFS::MountTarget.SecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-securitygroups
    """

    subnetId: str
    """``AWS::EFS::MountTarget.SubnetId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-efs-mounttarget.html#cfn-efs-mounttarget-subnetid
    """

__all__ = ["CfnFileSystem", "CfnFileSystemProps", "CfnMountTarget", "CfnMountTargetProps", "__jsii_assembly__"]

publication.publish()
