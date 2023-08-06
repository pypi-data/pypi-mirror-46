import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_cloudformation
import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_rds
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-quickstarts", "0.32.0", __name__, "aws-quickstarts@0.32.0.jsii.tgz")
@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class RemoteDesktopGateway(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-quickstarts.RemoteDesktopGateway"):
    """Embed the Remote Desktop Gateway AWS QuickStart."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, admin_password: str, key_pair_name: str, rdgw_cidr: str, vpc: aws_cdk.aws_ec2.IVpc, admin_user: typing.Optional[str]=None, domain_dns_name: typing.Optional[str]=None, number_of_rdgw_hosts: typing.Optional[jsii.Number]=None, qss3_bucket_name: typing.Optional[str]=None, qss3_key_prefix: typing.Optional[str]=None, rdgw_instance_type: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            adminPassword: -
            keyPairName: -
            rdgwCIDR: -
            vpc: -
            adminUser: -
            domainDNSName: -
            numberOfRDGWHosts: -
            qss3BucketName: -
            qss3KeyPrefix: -
            rdgwInstanceType: -
        """
        props: RemoteDesktopGatewayProps = {"adminPassword": admin_password, "keyPairName": key_pair_name, "rdgwCIDR": rdgw_cidr, "vpc": vpc}

        if admin_user is not None:
            props["adminUser"] = admin_user

        if domain_dns_name is not None:
            props["domainDNSName"] = domain_dns_name

        if number_of_rdgw_hosts is not None:
            props["numberOfRDGWHosts"] = number_of_rdgw_hosts

        if qss3_bucket_name is not None:
            props["qss3BucketName"] = qss3_bucket_name

        if qss3_key_prefix is not None:
            props["qss3KeyPrefix"] = qss3_key_prefix

        if rdgw_instance_type is not None:
            props["rdgwInstanceType"] = rdgw_instance_type

        jsii.create(RemoteDesktopGateway, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _RemoteDesktopGatewayProps(jsii.compat.TypedDict, total=False):
    adminUser: str
    domainDNSName: str
    numberOfRDGWHosts: jsii.Number
    qss3BucketName: str
    qss3KeyPrefix: str
    rdgwInstanceType: str

@jsii.data_type(jsii_type="@aws-cdk/aws-quickstarts.RemoteDesktopGatewayProps", jsii_struct_bases=[_RemoteDesktopGatewayProps])
class RemoteDesktopGatewayProps(_RemoteDesktopGatewayProps):
    adminPassword: str

    keyPairName: str

    rdgwCIDR: str

    vpc: aws_cdk.aws_ec2.IVpc

@jsii.implements(aws_cdk.aws_ec2.IConnectable)
class SqlServer(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-quickstarts.SqlServer"):
    """An instance of Microsoft SQL server with associated security groups."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, master_password: str, master_username: str, vpc: aws_cdk.aws_ec2.IVpc, allocated_storage: typing.Optional[jsii.Number]=None, engine: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, instance_class: typing.Optional[str]=None, license_model: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            masterPassword: -
            masterUsername: -
            vpc: -
            allocatedStorage: -
            engine: -
            engineVersion: -
            instanceClass: -
            licenseModel: -
        """
        props: SqlServerProps = {"masterPassword": master_password, "masterUsername": master_username, "vpc": vpc}

        if allocated_storage is not None:
            props["allocatedStorage"] = allocated_storage

        if engine is not None:
            props["engine"] = engine

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if instance_class is not None:
            props["instanceClass"] = instance_class

        if license_model is not None:
            props["licenseModel"] = license_model

        jsii.create(SqlServer, self, [scope, id, props])

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        return jsii.get(self, "connections")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _SqlServerProps(jsii.compat.TypedDict, total=False):
    allocatedStorage: jsii.Number
    engine: str
    engineVersion: str
    instanceClass: str
    licenseModel: str

@jsii.data_type(jsii_type="@aws-cdk/aws-quickstarts.SqlServerProps", jsii_struct_bases=[_SqlServerProps])
class SqlServerProps(_SqlServerProps):
    masterPassword: str

    masterUsername: str

    vpc: aws_cdk.aws_ec2.IVpc

__all__ = ["RemoteDesktopGateway", "RemoteDesktopGatewayProps", "SqlServer", "SqlServerProps", "__jsii_assembly__"]

publication.publish()
