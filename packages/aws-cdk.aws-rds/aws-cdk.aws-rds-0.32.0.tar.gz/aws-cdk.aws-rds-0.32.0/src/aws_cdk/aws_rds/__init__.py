import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_ec2
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.aws_sam
import aws_cdk.aws_secretsmanager
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-rds", "0.32.0", __name__, "aws-rds@0.32.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _BackupProps(jsii.compat.TypedDict, total=False):
    preferredWindow: str
    """A daily time range in 24-hours UTC format in which backups preferably execute.

    Must be at least 30 minutes long.

    Example: '01:00-02:00'
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.BackupProps", jsii_struct_bases=[_BackupProps])
class BackupProps(_BackupProps):
    """Backup configuration for RDS databases.

    Default:
        - The retention period for automated backups is 1 day.
          The preferred backup window will be a 30-minute window selected at random
          from an 8-hour block of time for each AWS Region.

    See:
        https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow.Aurora
    """
    retentionDays: jsii.Number
    """How many days to retain the backup."""

class CfnDBCluster(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBCluster"):
    """A CloudFormation ``AWS::RDS::DBCluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
    cloudformationResource:
        AWS::RDS::DBCluster
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, engine: str, availability_zones: typing.Optional[typing.List[str]]=None, backtrack_window: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, backup_retention_period: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, database_name: typing.Optional[str]=None, db_cluster_identifier: typing.Optional[str]=None, db_cluster_parameter_group_name: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, deletion_protection: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, enable_iam_database_authentication: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, engine_mode: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, kms_key_id: typing.Optional[str]=None, master_username: typing.Optional[str]=None, master_user_password: typing.Optional[str]=None, port: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, replication_source_identifier: typing.Optional[str]=None, scaling_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ScalingConfigurationProperty"]]]=None, snapshot_identifier: typing.Optional[str]=None, source_region: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, vpc_security_group_ids: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::RDS::DBCluster``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            engine: ``AWS::RDS::DBCluster.Engine``.
            availabilityZones: ``AWS::RDS::DBCluster.AvailabilityZones``.
            backtrackWindow: ``AWS::RDS::DBCluster.BacktrackWindow``.
            backupRetentionPeriod: ``AWS::RDS::DBCluster.BackupRetentionPeriod``.
            databaseName: ``AWS::RDS::DBCluster.DatabaseName``.
            dbClusterIdentifier: ``AWS::RDS::DBCluster.DBClusterIdentifier``.
            dbClusterParameterGroupName: ``AWS::RDS::DBCluster.DBClusterParameterGroupName``.
            dbSubnetGroupName: ``AWS::RDS::DBCluster.DBSubnetGroupName``.
            deletionProtection: ``AWS::RDS::DBCluster.DeletionProtection``.
            enableCloudwatchLogsExports: ``AWS::RDS::DBCluster.EnableCloudwatchLogsExports``.
            enableIamDatabaseAuthentication: ``AWS::RDS::DBCluster.EnableIAMDatabaseAuthentication``.
            engineMode: ``AWS::RDS::DBCluster.EngineMode``.
            engineVersion: ``AWS::RDS::DBCluster.EngineVersion``.
            kmsKeyId: ``AWS::RDS::DBCluster.KmsKeyId``.
            masterUsername: ``AWS::RDS::DBCluster.MasterUsername``.
            masterUserPassword: ``AWS::RDS::DBCluster.MasterUserPassword``.
            port: ``AWS::RDS::DBCluster.Port``.
            preferredBackupWindow: ``AWS::RDS::DBCluster.PreferredBackupWindow``.
            preferredMaintenanceWindow: ``AWS::RDS::DBCluster.PreferredMaintenanceWindow``.
            replicationSourceIdentifier: ``AWS::RDS::DBCluster.ReplicationSourceIdentifier``.
            scalingConfiguration: ``AWS::RDS::DBCluster.ScalingConfiguration``.
            snapshotIdentifier: ``AWS::RDS::DBCluster.SnapshotIdentifier``.
            sourceRegion: ``AWS::RDS::DBCluster.SourceRegion``.
            storageEncrypted: ``AWS::RDS::DBCluster.StorageEncrypted``.
            tags: ``AWS::RDS::DBCluster.Tags``.
            vpcSecurityGroupIds: ``AWS::RDS::DBCluster.VpcSecurityGroupIds``.
        """
        props: CfnDBClusterProps = {"engine": engine}

        if availability_zones is not None:
            props["availabilityZones"] = availability_zones

        if backtrack_window is not None:
            props["backtrackWindow"] = backtrack_window

        if backup_retention_period is not None:
            props["backupRetentionPeriod"] = backup_retention_period

        if database_name is not None:
            props["databaseName"] = database_name

        if db_cluster_identifier is not None:
            props["dbClusterIdentifier"] = db_cluster_identifier

        if db_cluster_parameter_group_name is not None:
            props["dbClusterParameterGroupName"] = db_cluster_parameter_group_name

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if enable_cloudwatch_logs_exports is not None:
            props["enableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports

        if enable_iam_database_authentication is not None:
            props["enableIamDatabaseAuthentication"] = enable_iam_database_authentication

        if engine_mode is not None:
            props["engineMode"] = engine_mode

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if master_username is not None:
            props["masterUsername"] = master_username

        if master_user_password is not None:
            props["masterUserPassword"] = master_user_password

        if port is not None:
            props["port"] = port

        if preferred_backup_window is not None:
            props["preferredBackupWindow"] = preferred_backup_window

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if replication_source_identifier is not None:
            props["replicationSourceIdentifier"] = replication_source_identifier

        if scaling_configuration is not None:
            props["scalingConfiguration"] = scaling_configuration

        if snapshot_identifier is not None:
            props["snapshotIdentifier"] = snapshot_identifier

        if source_region is not None:
            props["sourceRegion"] = source_region

        if storage_encrypted is not None:
            props["storageEncrypted"] = storage_encrypted

        if tags is not None:
            props["tags"] = tags

        if vpc_security_group_ids is not None:
            props["vpcSecurityGroupIds"] = vpc_security_group_ids

        jsii.create(CfnDBCluster, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbClusterEndpointAddress")
    def db_cluster_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
            Endpoint.Address
        """
        return jsii.get(self, "dbClusterEndpointAddress")

    @property
    @jsii.member(jsii_name="dbClusterEndpointPort")
    def db_cluster_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
            Endpoint.Port
        """
        return jsii.get(self, "dbClusterEndpointPort")

    @property
    @jsii.member(jsii_name="dbClusterName")
    def db_cluster_name(self) -> str:
        return jsii.get(self, "dbClusterName")

    @property
    @jsii.member(jsii_name="dbClusterReadEndpointAddress")
    def db_cluster_read_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
            ReadEndpoint.Address
        """
        return jsii.get(self, "dbClusterReadEndpointAddress")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBClusterProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBCluster.ScalingConfigurationProperty", jsii_struct_bases=[])
    class ScalingConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html
        """
        autoPause: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDBCluster.ScalingConfigurationProperty.AutoPause``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-autopause
        """

        maxCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDBCluster.ScalingConfigurationProperty.MaxCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-maxcapacity
        """

        minCapacity: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDBCluster.ScalingConfigurationProperty.MinCapacity``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-mincapacity
        """

        secondsUntilAutoPause: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDBCluster.ScalingConfigurationProperty.SecondsUntilAutoPause``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbcluster-scalingconfiguration.html#cfn-rds-dbcluster-scalingconfiguration-secondsuntilautopause
        """


class CfnDBClusterParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBClusterParameterGroup"):
    """A CloudFormation ``AWS::RDS::DBClusterParameterGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html
    cloudformationResource:
        AWS::RDS::DBClusterParameterGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token], tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::RDS::DBClusterParameterGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            description: ``AWS::RDS::DBClusterParameterGroup.Description``.
            family: ``AWS::RDS::DBClusterParameterGroup.Family``.
            parameters: ``AWS::RDS::DBClusterParameterGroup.Parameters``.
            tags: ``AWS::RDS::DBClusterParameterGroup.Tags``.
        """
        props: CfnDBClusterParameterGroupProps = {"description": description, "family": family, "parameters": parameters}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBClusterParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbClusterParameterGroupName")
    def db_cluster_parameter_group_name(self) -> str:
        return jsii.get(self, "dbClusterParameterGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBClusterParameterGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBClusterParameterGroupProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::DBClusterParameterGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBClusterParameterGroupProps", jsii_struct_bases=[_CfnDBClusterParameterGroupProps])
class CfnDBClusterParameterGroupProps(_CfnDBClusterParameterGroupProps):
    """Properties for defining a ``AWS::RDS::DBClusterParameterGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html
    """
    description: str
    """``AWS::RDS::DBClusterParameterGroup.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-description
    """

    family: str
    """``AWS::RDS::DBClusterParameterGroup.Family``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-family
    """

    parameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::RDS::DBClusterParameterGroup.Parameters``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbclusterparametergroup.html#cfn-rds-dbclusterparametergroup-parameters
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBClusterProps(jsii.compat.TypedDict, total=False):
    availabilityZones: typing.List[str]
    """``AWS::RDS::DBCluster.AvailabilityZones``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-availabilityzones
    """
    backtrackWindow: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBCluster.BacktrackWindow``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backtrackwindow
    """
    backupRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBCluster.BackupRetentionPeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-backuprententionperiod
    """
    databaseName: str
    """``AWS::RDS::DBCluster.DatabaseName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-databasename
    """
    dbClusterIdentifier: str
    """``AWS::RDS::DBCluster.DBClusterIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusteridentifier
    """
    dbClusterParameterGroupName: str
    """``AWS::RDS::DBCluster.DBClusterParameterGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbclusterparametergroupname
    """
    dbSubnetGroupName: str
    """``AWS::RDS::DBCluster.DBSubnetGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-dbsubnetgroupname
    """
    deletionProtection: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBCluster.DeletionProtection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-deletionprotection
    """
    enableCloudwatchLogsExports: typing.List[str]
    """``AWS::RDS::DBCluster.EnableCloudwatchLogsExports``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enablecloudwatchlogsexports
    """
    enableIamDatabaseAuthentication: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBCluster.EnableIAMDatabaseAuthentication``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enableiamdatabaseauthentication
    """
    engineMode: str
    """``AWS::RDS::DBCluster.EngineMode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-enginemode
    """
    engineVersion: str
    """``AWS::RDS::DBCluster.EngineVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engineversion
    """
    kmsKeyId: str
    """``AWS::RDS::DBCluster.KmsKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-kmskeyid
    """
    masterUsername: str
    """``AWS::RDS::DBCluster.MasterUsername``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masterusername
    """
    masterUserPassword: str
    """``AWS::RDS::DBCluster.MasterUserPassword``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-masteruserpassword
    """
    port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBCluster.Port``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-port
    """
    preferredBackupWindow: str
    """``AWS::RDS::DBCluster.PreferredBackupWindow``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredbackupwindow
    """
    preferredMaintenanceWindow: str
    """``AWS::RDS::DBCluster.PreferredMaintenanceWindow``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-preferredmaintenancewindow
    """
    replicationSourceIdentifier: str
    """``AWS::RDS::DBCluster.ReplicationSourceIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-replicationsourceidentifier
    """
    scalingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDBCluster.ScalingConfigurationProperty"]
    """``AWS::RDS::DBCluster.ScalingConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-scalingconfiguration
    """
    snapshotIdentifier: str
    """``AWS::RDS::DBCluster.SnapshotIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-snapshotidentifier
    """
    sourceRegion: str
    """``AWS::RDS::DBCluster.SourceRegion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-sourceregion
    """
    storageEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBCluster.StorageEncrypted``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-storageencrypted
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::DBCluster.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-tags
    """
    vpcSecurityGroupIds: typing.List[str]
    """``AWS::RDS::DBCluster.VpcSecurityGroupIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-vpcsecuritygroupids
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBClusterProps", jsii_struct_bases=[_CfnDBClusterProps])
class CfnDBClusterProps(_CfnDBClusterProps):
    """Properties for defining a ``AWS::RDS::DBCluster``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html
    """
    engine: str
    """``AWS::RDS::DBCluster.Engine``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbcluster.html#cfn-rds-dbcluster-engine
    """

class CfnDBInstance(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBInstance"):
    """A CloudFormation ``AWS::RDS::DBInstance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html
    cloudformationResource:
        AWS::RDS::DBInstance
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_instance_class: str, allocated_storage: typing.Optional[str]=None, allow_major_version_upgrade: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, auto_minor_version_upgrade: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, availability_zone: typing.Optional[str]=None, backup_retention_period: typing.Optional[str]=None, character_set_name: typing.Optional[str]=None, copy_tags_to_snapshot: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, db_cluster_identifier: typing.Optional[str]=None, db_instance_identifier: typing.Optional[str]=None, db_name: typing.Optional[str]=None, db_parameter_group_name: typing.Optional[str]=None, db_security_groups: typing.Optional[typing.List[str]]=None, db_snapshot_identifier: typing.Optional[str]=None, db_subnet_group_name: typing.Optional[str]=None, delete_automated_backups: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, deletion_protection: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, domain: typing.Optional[str]=None, domain_iam_role_name: typing.Optional[str]=None, enable_cloudwatch_logs_exports: typing.Optional[typing.List[str]]=None, enable_iam_database_authentication: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, enable_performance_insights: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, engine: typing.Optional[str]=None, engine_version: typing.Optional[str]=None, iops: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, kms_key_id: typing.Optional[str]=None, license_model: typing.Optional[str]=None, master_username: typing.Optional[str]=None, master_user_password: typing.Optional[str]=None, monitoring_interval: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, monitoring_role_arn: typing.Optional[str]=None, multi_az: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, option_group_name: typing.Optional[str]=None, performance_insights_kms_key_id: typing.Optional[str]=None, performance_insights_retention_period: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, port: typing.Optional[str]=None, preferred_backup_window: typing.Optional[str]=None, preferred_maintenance_window: typing.Optional[str]=None, processor_features: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "ProcessorFeatureProperty"]]]]]=None, promotion_tier: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, publicly_accessible: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, source_db_instance_identifier: typing.Optional[str]=None, source_region: typing.Optional[str]=None, storage_encrypted: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, storage_type: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, timezone: typing.Optional[str]=None, use_default_processor_features: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, vpc_security_groups: typing.Optional[typing.List[str]]=None) -> None:
        """Create a new ``AWS::RDS::DBInstance``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            dbInstanceClass: ``AWS::RDS::DBInstance.DBInstanceClass``.
            allocatedStorage: ``AWS::RDS::DBInstance.AllocatedStorage``.
            allowMajorVersionUpgrade: ``AWS::RDS::DBInstance.AllowMajorVersionUpgrade``.
            autoMinorVersionUpgrade: ``AWS::RDS::DBInstance.AutoMinorVersionUpgrade``.
            availabilityZone: ``AWS::RDS::DBInstance.AvailabilityZone``.
            backupRetentionPeriod: ``AWS::RDS::DBInstance.BackupRetentionPeriod``.
            characterSetName: ``AWS::RDS::DBInstance.CharacterSetName``.
            copyTagsToSnapshot: ``AWS::RDS::DBInstance.CopyTagsToSnapshot``.
            dbClusterIdentifier: ``AWS::RDS::DBInstance.DBClusterIdentifier``.
            dbInstanceIdentifier: ``AWS::RDS::DBInstance.DBInstanceIdentifier``.
            dbName: ``AWS::RDS::DBInstance.DBName``.
            dbParameterGroupName: ``AWS::RDS::DBInstance.DBParameterGroupName``.
            dbSecurityGroups: ``AWS::RDS::DBInstance.DBSecurityGroups``.
            dbSnapshotIdentifier: ``AWS::RDS::DBInstance.DBSnapshotIdentifier``.
            dbSubnetGroupName: ``AWS::RDS::DBInstance.DBSubnetGroupName``.
            deleteAutomatedBackups: ``AWS::RDS::DBInstance.DeleteAutomatedBackups``.
            deletionProtection: ``AWS::RDS::DBInstance.DeletionProtection``.
            domain: ``AWS::RDS::DBInstance.Domain``.
            domainIamRoleName: ``AWS::RDS::DBInstance.DomainIAMRoleName``.
            enableCloudwatchLogsExports: ``AWS::RDS::DBInstance.EnableCloudwatchLogsExports``.
            enableIamDatabaseAuthentication: ``AWS::RDS::DBInstance.EnableIAMDatabaseAuthentication``.
            enablePerformanceInsights: ``AWS::RDS::DBInstance.EnablePerformanceInsights``.
            engine: ``AWS::RDS::DBInstance.Engine``.
            engineVersion: ``AWS::RDS::DBInstance.EngineVersion``.
            iops: ``AWS::RDS::DBInstance.Iops``.
            kmsKeyId: ``AWS::RDS::DBInstance.KmsKeyId``.
            licenseModel: ``AWS::RDS::DBInstance.LicenseModel``.
            masterUsername: ``AWS::RDS::DBInstance.MasterUsername``.
            masterUserPassword: ``AWS::RDS::DBInstance.MasterUserPassword``.
            monitoringInterval: ``AWS::RDS::DBInstance.MonitoringInterval``.
            monitoringRoleArn: ``AWS::RDS::DBInstance.MonitoringRoleArn``.
            multiAz: ``AWS::RDS::DBInstance.MultiAZ``.
            optionGroupName: ``AWS::RDS::DBInstance.OptionGroupName``.
            performanceInsightsKmsKeyId: ``AWS::RDS::DBInstance.PerformanceInsightsKMSKeyId``.
            performanceInsightsRetentionPeriod: ``AWS::RDS::DBInstance.PerformanceInsightsRetentionPeriod``.
            port: ``AWS::RDS::DBInstance.Port``.
            preferredBackupWindow: ``AWS::RDS::DBInstance.PreferredBackupWindow``.
            preferredMaintenanceWindow: ``AWS::RDS::DBInstance.PreferredMaintenanceWindow``.
            processorFeatures: ``AWS::RDS::DBInstance.ProcessorFeatures``.
            promotionTier: ``AWS::RDS::DBInstance.PromotionTier``.
            publiclyAccessible: ``AWS::RDS::DBInstance.PubliclyAccessible``.
            sourceDbInstanceIdentifier: ``AWS::RDS::DBInstance.SourceDBInstanceIdentifier``.
            sourceRegion: ``AWS::RDS::DBInstance.SourceRegion``.
            storageEncrypted: ``AWS::RDS::DBInstance.StorageEncrypted``.
            storageType: ``AWS::RDS::DBInstance.StorageType``.
            tags: ``AWS::RDS::DBInstance.Tags``.
            timezone: ``AWS::RDS::DBInstance.Timezone``.
            useDefaultProcessorFeatures: ``AWS::RDS::DBInstance.UseDefaultProcessorFeatures``.
            vpcSecurityGroups: ``AWS::RDS::DBInstance.VPCSecurityGroups``.
        """
        props: CfnDBInstanceProps = {"dbInstanceClass": db_instance_class}

        if allocated_storage is not None:
            props["allocatedStorage"] = allocated_storage

        if allow_major_version_upgrade is not None:
            props["allowMajorVersionUpgrade"] = allow_major_version_upgrade

        if auto_minor_version_upgrade is not None:
            props["autoMinorVersionUpgrade"] = auto_minor_version_upgrade

        if availability_zone is not None:
            props["availabilityZone"] = availability_zone

        if backup_retention_period is not None:
            props["backupRetentionPeriod"] = backup_retention_period

        if character_set_name is not None:
            props["characterSetName"] = character_set_name

        if copy_tags_to_snapshot is not None:
            props["copyTagsToSnapshot"] = copy_tags_to_snapshot

        if db_cluster_identifier is not None:
            props["dbClusterIdentifier"] = db_cluster_identifier

        if db_instance_identifier is not None:
            props["dbInstanceIdentifier"] = db_instance_identifier

        if db_name is not None:
            props["dbName"] = db_name

        if db_parameter_group_name is not None:
            props["dbParameterGroupName"] = db_parameter_group_name

        if db_security_groups is not None:
            props["dbSecurityGroups"] = db_security_groups

        if db_snapshot_identifier is not None:
            props["dbSnapshotIdentifier"] = db_snapshot_identifier

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if delete_automated_backups is not None:
            props["deleteAutomatedBackups"] = delete_automated_backups

        if deletion_protection is not None:
            props["deletionProtection"] = deletion_protection

        if domain is not None:
            props["domain"] = domain

        if domain_iam_role_name is not None:
            props["domainIamRoleName"] = domain_iam_role_name

        if enable_cloudwatch_logs_exports is not None:
            props["enableCloudwatchLogsExports"] = enable_cloudwatch_logs_exports

        if enable_iam_database_authentication is not None:
            props["enableIamDatabaseAuthentication"] = enable_iam_database_authentication

        if enable_performance_insights is not None:
            props["enablePerformanceInsights"] = enable_performance_insights

        if engine is not None:
            props["engine"] = engine

        if engine_version is not None:
            props["engineVersion"] = engine_version

        if iops is not None:
            props["iops"] = iops

        if kms_key_id is not None:
            props["kmsKeyId"] = kms_key_id

        if license_model is not None:
            props["licenseModel"] = license_model

        if master_username is not None:
            props["masterUsername"] = master_username

        if master_user_password is not None:
            props["masterUserPassword"] = master_user_password

        if monitoring_interval is not None:
            props["monitoringInterval"] = monitoring_interval

        if monitoring_role_arn is not None:
            props["monitoringRoleArn"] = monitoring_role_arn

        if multi_az is not None:
            props["multiAz"] = multi_az

        if option_group_name is not None:
            props["optionGroupName"] = option_group_name

        if performance_insights_kms_key_id is not None:
            props["performanceInsightsKmsKeyId"] = performance_insights_kms_key_id

        if performance_insights_retention_period is not None:
            props["performanceInsightsRetentionPeriod"] = performance_insights_retention_period

        if port is not None:
            props["port"] = port

        if preferred_backup_window is not None:
            props["preferredBackupWindow"] = preferred_backup_window

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if processor_features is not None:
            props["processorFeatures"] = processor_features

        if promotion_tier is not None:
            props["promotionTier"] = promotion_tier

        if publicly_accessible is not None:
            props["publiclyAccessible"] = publicly_accessible

        if source_db_instance_identifier is not None:
            props["sourceDbInstanceIdentifier"] = source_db_instance_identifier

        if source_region is not None:
            props["sourceRegion"] = source_region

        if storage_encrypted is not None:
            props["storageEncrypted"] = storage_encrypted

        if storage_type is not None:
            props["storageType"] = storage_type

        if tags is not None:
            props["tags"] = tags

        if timezone is not None:
            props["timezone"] = timezone

        if use_default_processor_features is not None:
            props["useDefaultProcessorFeatures"] = use_default_processor_features

        if vpc_security_groups is not None:
            props["vpcSecurityGroups"] = vpc_security_groups

        jsii.create(CfnDBInstance, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbInstanceEndpointAddress")
    def db_instance_endpoint_address(self) -> str:
        """
        cloudformationAttribute:
            Endpoint.Address
        """
        return jsii.get(self, "dbInstanceEndpointAddress")

    @property
    @jsii.member(jsii_name="dbInstanceEndpointPort")
    def db_instance_endpoint_port(self) -> str:
        """
        cloudformationAttribute:
            Endpoint.Port
        """
        return jsii.get(self, "dbInstanceEndpointPort")

    @property
    @jsii.member(jsii_name="dbInstanceId")
    def db_instance_id(self) -> str:
        return jsii.get(self, "dbInstanceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBInstanceProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBInstance.ProcessorFeatureProperty", jsii_struct_bases=[])
    class ProcessorFeatureProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html
        """
        name: str
        """``CfnDBInstance.ProcessorFeatureProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html#cfn-rds-dbinstance-processorfeature-name
        """

        value: str
        """``CfnDBInstance.ProcessorFeatureProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbinstance-processorfeature.html#cfn-rds-dbinstance-processorfeature-value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBInstanceProps(jsii.compat.TypedDict, total=False):
    allocatedStorage: str
    """``AWS::RDS::DBInstance.AllocatedStorage``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-allocatedstorage
    """
    allowMajorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.AllowMajorVersionUpgrade``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-allowmajorversionupgrade
    """
    autoMinorVersionUpgrade: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.AutoMinorVersionUpgrade``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-autominorversionupgrade
    """
    availabilityZone: str
    """``AWS::RDS::DBInstance.AvailabilityZone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-availabilityzone
    """
    backupRetentionPeriod: str
    """``AWS::RDS::DBInstance.BackupRetentionPeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-backupretentionperiod
    """
    characterSetName: str
    """``AWS::RDS::DBInstance.CharacterSetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-charactersetname
    """
    copyTagsToSnapshot: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.CopyTagsToSnapshot``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-copytagstosnapshot
    """
    dbClusterIdentifier: str
    """``AWS::RDS::DBInstance.DBClusterIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbclusteridentifier
    """
    dbInstanceIdentifier: str
    """``AWS::RDS::DBInstance.DBInstanceIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbinstanceidentifier
    """
    dbName: str
    """``AWS::RDS::DBInstance.DBName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbname
    """
    dbParameterGroupName: str
    """``AWS::RDS::DBInstance.DBParameterGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbparametergroupname
    """
    dbSecurityGroups: typing.List[str]
    """``AWS::RDS::DBInstance.DBSecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsecuritygroups
    """
    dbSnapshotIdentifier: str
    """``AWS::RDS::DBInstance.DBSnapshotIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsnapshotidentifier
    """
    dbSubnetGroupName: str
    """``AWS::RDS::DBInstance.DBSubnetGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbsubnetgroupname
    """
    deleteAutomatedBackups: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.DeleteAutomatedBackups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-deleteautomatedbackups
    """
    deletionProtection: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.DeletionProtection``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-deletionprotection
    """
    domain: str
    """``AWS::RDS::DBInstance.Domain``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-domain
    """
    domainIamRoleName: str
    """``AWS::RDS::DBInstance.DomainIAMRoleName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-domainiamrolename
    """
    enableCloudwatchLogsExports: typing.List[str]
    """``AWS::RDS::DBInstance.EnableCloudwatchLogsExports``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enablecloudwatchlogsexports
    """
    enableIamDatabaseAuthentication: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.EnableIAMDatabaseAuthentication``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableiamdatabaseauthentication
    """
    enablePerformanceInsights: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.EnablePerformanceInsights``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-enableperformanceinsights
    """
    engine: str
    """``AWS::RDS::DBInstance.Engine``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engine
    """
    engineVersion: str
    """``AWS::RDS::DBInstance.EngineVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-engineversion
    """
    iops: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.Iops``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-iops
    """
    kmsKeyId: str
    """``AWS::RDS::DBInstance.KmsKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-kmskeyid
    """
    licenseModel: str
    """``AWS::RDS::DBInstance.LicenseModel``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-licensemodel
    """
    masterUsername: str
    """``AWS::RDS::DBInstance.MasterUsername``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-masterusername
    """
    masterUserPassword: str
    """``AWS::RDS::DBInstance.MasterUserPassword``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-masteruserpassword
    """
    monitoringInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.MonitoringInterval``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-monitoringinterval
    """
    monitoringRoleArn: str
    """``AWS::RDS::DBInstance.MonitoringRoleArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-monitoringrolearn
    """
    multiAz: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.MultiAZ``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-multiaz
    """
    optionGroupName: str
    """``AWS::RDS::DBInstance.OptionGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-optiongroupname
    """
    performanceInsightsKmsKeyId: str
    """``AWS::RDS::DBInstance.PerformanceInsightsKMSKeyId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-performanceinsightskmskeyid
    """
    performanceInsightsRetentionPeriod: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.PerformanceInsightsRetentionPeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-performanceinsightsretentionperiod
    """
    port: str
    """``AWS::RDS::DBInstance.Port``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-port
    """
    preferredBackupWindow: str
    """``AWS::RDS::DBInstance.PreferredBackupWindow``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-preferredbackupwindow
    """
    preferredMaintenanceWindow: str
    """``AWS::RDS::DBInstance.PreferredMaintenanceWindow``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-preferredmaintenancewindow
    """
    processorFeatures: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDBInstance.ProcessorFeatureProperty"]]]
    """``AWS::RDS::DBInstance.ProcessorFeatures``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-processorfeatures
    """
    promotionTier: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.PromotionTier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-promotiontier
    """
    publiclyAccessible: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.PubliclyAccessible``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-publiclyaccessible
    """
    sourceDbInstanceIdentifier: str
    """``AWS::RDS::DBInstance.SourceDBInstanceIdentifier``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-sourcedbinstanceidentifier
    """
    sourceRegion: str
    """``AWS::RDS::DBInstance.SourceRegion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-sourceregion
    """
    storageEncrypted: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.StorageEncrypted``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-storageencrypted
    """
    storageType: str
    """``AWS::RDS::DBInstance.StorageType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-storagetype
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::DBInstance.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-tags
    """
    timezone: str
    """``AWS::RDS::DBInstance.Timezone``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-timezone
    """
    useDefaultProcessorFeatures: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::DBInstance.UseDefaultProcessorFeatures``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-usedefaultprocessorfeatures
    """
    vpcSecurityGroups: typing.List[str]
    """``AWS::RDS::DBInstance.VPCSecurityGroups``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-vpcsecuritygroups
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBInstanceProps", jsii_struct_bases=[_CfnDBInstanceProps])
class CfnDBInstanceProps(_CfnDBInstanceProps):
    """Properties for defining a ``AWS::RDS::DBInstance``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html
    """
    dbInstanceClass: str
    """``AWS::RDS::DBInstance.DBInstanceClass``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-database-instance.html#cfn-rds-dbinstance-dbinstanceclass
    """

class CfnDBParameterGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBParameterGroup"):
    """A CloudFormation ``AWS::RDS::DBParameterGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html
    cloudformationResource:
        AWS::RDS::DBParameterGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.Mapping[str,str]]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::RDS::DBParameterGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            description: ``AWS::RDS::DBParameterGroup.Description``.
            family: ``AWS::RDS::DBParameterGroup.Family``.
            parameters: ``AWS::RDS::DBParameterGroup.Parameters``.
            tags: ``AWS::RDS::DBParameterGroup.Tags``.
        """
        props: CfnDBParameterGroupProps = {"description": description, "family": family}

        if parameters is not None:
            props["parameters"] = parameters

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBParameterGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbParameterGroupName")
    def db_parameter_group_name(self) -> str:
        return jsii.get(self, "dbParameterGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBParameterGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBParameterGroupProps(jsii.compat.TypedDict, total=False):
    parameters: typing.Union[aws_cdk.cdk.Token, typing.Mapping[str,str]]
    """``AWS::RDS::DBParameterGroup.Parameters``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-parameters
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::DBParameterGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBParameterGroupProps", jsii_struct_bases=[_CfnDBParameterGroupProps])
class CfnDBParameterGroupProps(_CfnDBParameterGroupProps):
    """Properties for defining a ``AWS::RDS::DBParameterGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html
    """
    description: str
    """``AWS::RDS::DBParameterGroup.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-description
    """

    family: str
    """``AWS::RDS::DBParameterGroup.Family``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-dbparametergroup.html#cfn-rds-dbparametergroup-family
    """

class CfnDBSecurityGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroup"):
    """A CloudFormation ``AWS::RDS::DBSecurityGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html
    cloudformationResource:
        AWS::RDS::DBSecurityGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_security_group_ingress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "IngressProperty"]]], group_description: str, ec2_vpc_id: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::RDS::DBSecurityGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            dbSecurityGroupIngress: ``AWS::RDS::DBSecurityGroup.DBSecurityGroupIngress``.
            groupDescription: ``AWS::RDS::DBSecurityGroup.GroupDescription``.
            ec2VpcId: ``AWS::RDS::DBSecurityGroup.EC2VpcId``.
            tags: ``AWS::RDS::DBSecurityGroup.Tags``.
        """
        props: CfnDBSecurityGroupProps = {"dbSecurityGroupIngress": db_security_group_ingress, "groupDescription": group_description}

        if ec2_vpc_id is not None:
            props["ec2VpcId"] = ec2_vpc_id

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBSecurityGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbSecurityGroupName")
    def db_security_group_name(self) -> str:
        return jsii.get(self, "dbSecurityGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBSecurityGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroup.IngressProperty", jsii_struct_bases=[])
    class IngressProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html
        """
        cidrip: str
        """``CfnDBSecurityGroup.IngressProperty.CIDRIP``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-cidrip
        """

        ec2SecurityGroupId: str
        """``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-ec2securitygroupid
        """

        ec2SecurityGroupName: str
        """``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-ec2securitygroupname
        """

        ec2SecurityGroupOwnerId: str
        """``CfnDBSecurityGroup.IngressProperty.EC2SecurityGroupOwnerId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group-rule.html#cfn-rds-securitygroup-ec2securitygroupownerid
        """


class CfnDBSecurityGroupIngress(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroupIngress"):
    """A CloudFormation ``AWS::RDS::DBSecurityGroupIngress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html
    cloudformationResource:
        AWS::RDS::DBSecurityGroupIngress
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_security_group_name: str, cidrip: typing.Optional[str]=None, ec2_security_group_id: typing.Optional[str]=None, ec2_security_group_name: typing.Optional[str]=None, ec2_security_group_owner_id: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::RDS::DBSecurityGroupIngress``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            dbSecurityGroupName: ``AWS::RDS::DBSecurityGroupIngress.DBSecurityGroupName``.
            cidrip: ``AWS::RDS::DBSecurityGroupIngress.CIDRIP``.
            ec2SecurityGroupId: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupId``.
            ec2SecurityGroupName: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupName``.
            ec2SecurityGroupOwnerId: ``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupOwnerId``.
        """
        props: CfnDBSecurityGroupIngressProps = {"dbSecurityGroupName": db_security_group_name}

        if cidrip is not None:
            props["cidrip"] = cidrip

        if ec2_security_group_id is not None:
            props["ec2SecurityGroupId"] = ec2_security_group_id

        if ec2_security_group_name is not None:
            props["ec2SecurityGroupName"] = ec2_security_group_name

        if ec2_security_group_owner_id is not None:
            props["ec2SecurityGroupOwnerId"] = ec2_security_group_owner_id

        jsii.create(CfnDBSecurityGroupIngress, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbSecurityGroupIngressName")
    def db_security_group_ingress_name(self) -> str:
        return jsii.get(self, "dbSecurityGroupIngressName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBSecurityGroupIngressProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBSecurityGroupIngressProps(jsii.compat.TypedDict, total=False):
    cidrip: str
    """``AWS::RDS::DBSecurityGroupIngress.CIDRIP``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-cidrip
    """
    ec2SecurityGroupId: str
    """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupid
    """
    ec2SecurityGroupName: str
    """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupname
    """
    ec2SecurityGroupOwnerId: str
    """``AWS::RDS::DBSecurityGroupIngress.EC2SecurityGroupOwnerId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-ec2securitygroupownerid
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroupIngressProps", jsii_struct_bases=[_CfnDBSecurityGroupIngressProps])
class CfnDBSecurityGroupIngressProps(_CfnDBSecurityGroupIngressProps):
    """Properties for defining a ``AWS::RDS::DBSecurityGroupIngress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html
    """
    dbSecurityGroupName: str
    """``AWS::RDS::DBSecurityGroupIngress.DBSecurityGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-security-group-ingress.html#cfn-rds-securitygroup-ingress-dbsecuritygroupname
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBSecurityGroupProps(jsii.compat.TypedDict, total=False):
    ec2VpcId: str
    """``AWS::RDS::DBSecurityGroup.EC2VpcId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-ec2vpcid
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::DBSecurityGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSecurityGroupProps", jsii_struct_bases=[_CfnDBSecurityGroupProps])
class CfnDBSecurityGroupProps(_CfnDBSecurityGroupProps):
    """Properties for defining a ``AWS::RDS::DBSecurityGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html
    """
    dbSecurityGroupIngress: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDBSecurityGroup.IngressProperty"]]]
    """``AWS::RDS::DBSecurityGroup.DBSecurityGroupIngress``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-dbsecuritygroupingress
    """

    groupDescription: str
    """``AWS::RDS::DBSecurityGroup.GroupDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-security-group.html#cfn-rds-dbsecuritygroup-groupdescription
    """

class CfnDBSubnetGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnDBSubnetGroup"):
    """A CloudFormation ``AWS::RDS::DBSubnetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html
    cloudformationResource:
        AWS::RDS::DBSubnetGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, db_subnet_group_description: str, subnet_ids: typing.List[str], db_subnet_group_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::RDS::DBSubnetGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            dbSubnetGroupDescription: ``AWS::RDS::DBSubnetGroup.DBSubnetGroupDescription``.
            subnetIds: ``AWS::RDS::DBSubnetGroup.SubnetIds``.
            dbSubnetGroupName: ``AWS::RDS::DBSubnetGroup.DBSubnetGroupName``.
            tags: ``AWS::RDS::DBSubnetGroup.Tags``.
        """
        props: CfnDBSubnetGroupProps = {"dbSubnetGroupDescription": db_subnet_group_description, "subnetIds": subnet_ids}

        if db_subnet_group_name is not None:
            props["dbSubnetGroupName"] = db_subnet_group_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDBSubnetGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="dbSubnetGroupName")
    def db_subnet_group_name(self) -> str:
        return jsii.get(self, "dbSubnetGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDBSubnetGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDBSubnetGroupProps(jsii.compat.TypedDict, total=False):
    dbSubnetGroupName: str
    """``AWS::RDS::DBSubnetGroup.DBSubnetGroupName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-dbsubnetgroupname
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::DBSubnetGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnDBSubnetGroupProps", jsii_struct_bases=[_CfnDBSubnetGroupProps])
class CfnDBSubnetGroupProps(_CfnDBSubnetGroupProps):
    """Properties for defining a ``AWS::RDS::DBSubnetGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html
    """
    dbSubnetGroupDescription: str
    """``AWS::RDS::DBSubnetGroup.DBSubnetGroupDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-dbsubnetgroupdescription
    """

    subnetIds: typing.List[str]
    """``AWS::RDS::DBSubnetGroup.SubnetIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-dbsubnet-group.html#cfn-rds-dbsubnetgroup-subnetids
    """

class CfnEventSubscription(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnEventSubscription"):
    """A CloudFormation ``AWS::RDS::EventSubscription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html
    cloudformationResource:
        AWS::RDS::EventSubscription
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, sns_topic_arn: str, enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, event_categories: typing.Optional[typing.List[str]]=None, source_ids: typing.Optional[typing.List[str]]=None, source_type: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::RDS::EventSubscription``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            snsTopicArn: ``AWS::RDS::EventSubscription.SnsTopicArn``.
            enabled: ``AWS::RDS::EventSubscription.Enabled``.
            eventCategories: ``AWS::RDS::EventSubscription.EventCategories``.
            sourceIds: ``AWS::RDS::EventSubscription.SourceIds``.
            sourceType: ``AWS::RDS::EventSubscription.SourceType``.
        """
        props: CfnEventSubscriptionProps = {"snsTopicArn": sns_topic_arn}

        if enabled is not None:
            props["enabled"] = enabled

        if event_categories is not None:
            props["eventCategories"] = event_categories

        if source_ids is not None:
            props["sourceIds"] = source_ids

        if source_type is not None:
            props["sourceType"] = source_type

        jsii.create(CfnEventSubscription, self, [scope, id, props])

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
    @jsii.member(jsii_name="eventSubscriptionName")
    def event_subscription_name(self) -> str:
        return jsii.get(self, "eventSubscriptionName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnEventSubscriptionProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnEventSubscriptionProps(jsii.compat.TypedDict, total=False):
    enabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::RDS::EventSubscription.Enabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-enabled
    """
    eventCategories: typing.List[str]
    """``AWS::RDS::EventSubscription.EventCategories``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-eventcategories
    """
    sourceIds: typing.List[str]
    """``AWS::RDS::EventSubscription.SourceIds``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourceids
    """
    sourceType: str
    """``AWS::RDS::EventSubscription.SourceType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-sourcetype
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnEventSubscriptionProps", jsii_struct_bases=[_CfnEventSubscriptionProps])
class CfnEventSubscriptionProps(_CfnEventSubscriptionProps):
    """Properties for defining a ``AWS::RDS::EventSubscription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html
    """
    snsTopicArn: str
    """``AWS::RDS::EventSubscription.SnsTopicArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-eventsubscription.html#cfn-rds-eventsubscription-snstopicarn
    """

class CfnOptionGroup(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.CfnOptionGroup"):
    """A CloudFormation ``AWS::RDS::OptionGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html
    cloudformationResource:
        AWS::RDS::OptionGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, engine_name: str, major_engine_version: str, option_configurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "OptionConfigurationProperty"]]], option_group_description: str, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::RDS::OptionGroup``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            engineName: ``AWS::RDS::OptionGroup.EngineName``.
            majorEngineVersion: ``AWS::RDS::OptionGroup.MajorEngineVersion``.
            optionConfigurations: ``AWS::RDS::OptionGroup.OptionConfigurations``.
            optionGroupDescription: ``AWS::RDS::OptionGroup.OptionGroupDescription``.
            tags: ``AWS::RDS::OptionGroup.Tags``.
        """
        props: CfnOptionGroupProps = {"engineName": engine_name, "majorEngineVersion": major_engine_version, "optionConfigurations": option_configurations, "optionGroupDescription": option_group_description}

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnOptionGroup, self, [scope, id, props])

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
    @jsii.member(jsii_name="optionGroupName")
    def option_group_name(self) -> str:
        return jsii.get(self, "optionGroupName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnOptionGroupProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="tags")
    def tags(self) -> aws_cdk.cdk.TagManager:
        """The ``TagManager`` handles setting, removing and formatting tags.

        Tags should be managed either passing them as properties during
        initiation or by calling methods on this object. If both techniques are
        used only the tags from the TagManager will be used. ``Tag`` (aspect)
        will use the manager.
        """
        return jsii.get(self, "tags")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OptionConfigurationProperty(jsii.compat.TypedDict, total=False):
        dbSecurityGroupMemberships: typing.List[str]
        """``CfnOptionGroup.OptionConfigurationProperty.DBSecurityGroupMemberships``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-dbsecuritygroupmemberships
        """
        optionSettings: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnOptionGroup.OptionSettingProperty"]]]
        """``CfnOptionGroup.OptionConfigurationProperty.OptionSettings``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-optionsettings
        """
        optionVersion: str
        """``CfnOptionGroup.OptionConfigurationProperty.OptionVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfiguration-optionversion
        """
        port: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnOptionGroup.OptionConfigurationProperty.Port``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-port
        """
        vpcSecurityGroupMemberships: typing.List[str]
        """``CfnOptionGroup.OptionConfigurationProperty.VpcSecurityGroupMemberships``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-vpcsecuritygroupmemberships
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnOptionGroup.OptionConfigurationProperty", jsii_struct_bases=[_OptionConfigurationProperty])
    class OptionConfigurationProperty(_OptionConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html
        """
        optionName: str
        """``CfnOptionGroup.OptionConfigurationProperty.OptionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations.html#cfn-rds-optiongroup-optionconfigurations-optionname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnOptionGroup.OptionSettingProperty", jsii_struct_bases=[])
    class OptionSettingProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations-optionsettings.html
        """
        name: str
        """``CfnOptionGroup.OptionSettingProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations-optionsettings.html#cfn-rds-optiongroup-optionconfigurations-optionsettings-name
        """

        value: str
        """``CfnOptionGroup.OptionSettingProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-rds-optiongroup-optionconfigurations-optionsettings.html#cfn-rds-optiongroup-optionconfigurations-optionsettings-value
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnOptionGroupProps(jsii.compat.TypedDict, total=False):
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::RDS::OptionGroup.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.CfnOptionGroupProps", jsii_struct_bases=[_CfnOptionGroupProps])
class CfnOptionGroupProps(_CfnOptionGroupProps):
    """Properties for defining a ``AWS::RDS::OptionGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html
    """
    engineName: str
    """``AWS::RDS::OptionGroup.EngineName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-enginename
    """

    majorEngineVersion: str
    """``AWS::RDS::OptionGroup.MajorEngineVersion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-majorengineversion
    """

    optionConfigurations: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnOptionGroup.OptionConfigurationProperty"]]]
    """``AWS::RDS::OptionGroup.OptionConfigurations``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optionconfigurations
    """

    optionGroupDescription: str
    """``AWS::RDS::OptionGroup.OptionGroupDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-rds-optiongroup.html#cfn-rds-optiongroup-optiongroupdescription
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.ClusterParameterGroupImportProps", jsii_struct_bases=[])
class ClusterParameterGroupImportProps(jsii.compat.TypedDict):
    """Properties to reference a cluster parameter group."""
    parameterGroupName: str

@jsii.data_type_optionals(jsii_struct_bases=[])
class _ClusterParameterGroupProps(jsii.compat.TypedDict, total=False):
    parameters: typing.Mapping[str,typing.Any]
    """The parameters in this parameter group.

    Default:
        - No parameters.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.ClusterParameterGroupProps", jsii_struct_bases=[_ClusterParameterGroupProps])
class ClusterParameterGroupProps(_ClusterParameterGroupProps):
    """Properties for a cluster parameter group."""
    description: str
    """Description for this parameter group."""

    family: str
    """Database family of this parameter group."""

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.DatabaseClusterAttributes", jsii_struct_bases=[])
class DatabaseClusterAttributes(jsii.compat.TypedDict):
    """Properties that describe an existing cluster instance."""
    clusterEndpointAddress: str
    """Cluster endpoint address."""

    clusterIdentifier: str
    """Identifier for the cluster."""

    instanceEndpointAddresses: typing.List[str]
    """Endpoint addresses of individual instances."""

    instanceIdentifiers: typing.List[str]
    """Identifier for the instances."""

    port: jsii.Number
    """The database port."""

    readerEndpointAddress: str
    """Reader endpoint address."""

    securityGroupId: str
    """The security group for this database cluster."""

@jsii.enum(jsii_type="@aws-cdk/aws-rds.DatabaseClusterEngine")
class DatabaseClusterEngine(enum.Enum):
    """The engine for the database cluster."""
    Aurora = "Aurora"
    AuroraMysql = "AuroraMysql"
    AuroraPostgresql = "AuroraPostgresql"
    Neptune = "Neptune"

@jsii.data_type_optionals(jsii_struct_bases=[])
class _DatabaseClusterProps(jsii.compat.TypedDict, total=False):
    backup: "BackupProps"
    """Backup settings.

    Default:
        - Backup retention period for automated backups is 1 day.
          Backup preferred window is set to a 30-minute window selected at random from an
          8-hour block of time for each AWS Region, occurring on a random day of the week.

    See:
        https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow.Aurora
    """
    clusterIdentifier: str
    """An optional identifier for the cluster.

    Default:
        - A name is automatically generated.
    """
    defaultDatabaseName: str
    """Name of a database which is automatically created inside the cluster.

    Default:
        - Database is not created in cluster.
    """
    deleteReplacePolicy: aws_cdk.cdk.DeletionPolicy
    """The CloudFormation policy to apply when the cluster and its instances are removed from the stack or replaced during an update.

    Default:
        - Retain cluster.
    """
    instanceIdentifierBase: str
    """Base identifier for instances.

    Every replica is named by appending the replica number to this string, 1-based.

    Default:
        - clusterIdentifier is used with the word "Instance" appended.
          If clusterIdentifier is not provided, the identifier is automatically generated.
    """
    instances: jsii.Number
    """How many replicas/instances to create.

    Has to be at least 1.

    Default:
        2
    """
    kmsKey: aws_cdk.aws_kms.IKey
    """The KMS key for storage encryption.

    If specified ``storageEncrypted``
    will be set to ``true``.

    Default:
        - default master key.
    """
    parameterGroup: "IClusterParameterGroup"
    """Additional parameters to pass to the database engine.

    Default:
        - No parameter group.
    """
    port: jsii.Number
    """What port to listen on.

    Default:
        - The default for the engine is used.
    """
    preferredMaintenanceWindow: str
    """A daily time range in 24-hours UTC format in which backups preferably execute.

    Must be at least 30 minutes long.

    Example: '01:00-02:00'

    Default:
        - 30-minute window selected at random from an 8-hour block of time for
          each AWS Region, occurring on a random day of the week.

    See:
        https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_UpgradeDBInstance.Maintenance.html#AdjustingTheMaintenanceWindow.Aurora
    """
    storageEncrypted: bool
    """Whether to enable storage encryption.

    Default:
        false
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.DatabaseClusterProps", jsii_struct_bases=[_DatabaseClusterProps])
class DatabaseClusterProps(_DatabaseClusterProps):
    """Properties for a new database cluster."""
    engine: "DatabaseClusterEngine"
    """What kind of database to start."""

    instanceProps: "InstanceProps"
    """Settings for the individual instances that are launched."""

    masterUser: "Login"
    """Username and password for the administrative user."""

@jsii.enum(jsii_type="@aws-cdk/aws-rds.DatabaseEngine")
class DatabaseEngine(enum.Enum):
    """The RDS database engine."""
    MariaDb = "MariaDb"
    """MariaDB."""
    Mysql = "Mysql"
    """MySQL."""
    Oracle = "Oracle"
    """Oracle."""
    Postgres = "Postgres"
    """PostgreSQL."""
    SqlServer = "SqlServer"
    """SQL Server."""

class DatabaseSecret(aws_cdk.aws_secretsmanager.Secret, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.DatabaseSecret"):
    """A database secret.

    resource:
        AWS::SecretsManager::Secret
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, username: str, encryption_key: typing.Optional[aws_cdk.aws_kms.IKey]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            username: The username.
            encryptionKey: The KMS key to use to encrypt the secret. Default: default master key
        """
        props: DatabaseSecretProps = {"username": username}

        if encryption_key is not None:
            props["encryptionKey"] = encryption_key

        jsii.create(DatabaseSecret, self, [scope, id, props])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _DatabaseSecretProps(jsii.compat.TypedDict, total=False):
    encryptionKey: aws_cdk.aws_kms.IKey
    """The KMS key to use to encrypt the secret.

    Default:
        default master key
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.DatabaseSecretProps", jsii_struct_bases=[_DatabaseSecretProps])
class DatabaseSecretProps(_DatabaseSecretProps):
    """Construction properties for a DatabaseSecret."""
    username: str
    """The username."""

class Endpoint(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.Endpoint"):
    """Connection endpoint of a database cluster or instance.

    Consists of a combination of hostname and port.
    """
    def __init__(self, address: str, port: jsii.Number) -> None:
        """
        Arguments:
            address: -
            port: -
        """
        jsii.create(Endpoint, self, [address, port])

    @property
    @jsii.member(jsii_name="hostname")
    def hostname(self) -> str:
        """The hostname of the endpoint."""
        return jsii.get(self, "hostname")

    @property
    @jsii.member(jsii_name="port")
    def port(self) -> jsii.Number:
        """The port of the endpoint."""
        return jsii.get(self, "port")

    @property
    @jsii.member(jsii_name="socketAddress")
    def socket_address(self) -> str:
        """The combination of "HOSTNAME:PORT" for this endpoint."""
        return jsii.get(self, "socketAddress")


@jsii.interface(jsii_type="@aws-cdk/aws-rds.IClusterParameterGroup")
class IClusterParameterGroup(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    """A cluster parameter group."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IClusterParameterGroupProxy

    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        """Name of this parameter group."""
        ...


class _IClusterParameterGroupProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    """A cluster parameter group."""
    __jsii_type__ = "@aws-cdk/aws-rds.IClusterParameterGroup"
    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        """Name of this parameter group."""
        return jsii.get(self, "parameterGroupName")


@jsii.implements(IClusterParameterGroup)
class ClusterParameterGroup(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.ClusterParameterGroup"):
    """Defina a cluster parameter group.

    resource:
        AWS::RDS::DBClusterParameterGroup
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, description: str, family: str, parameters: typing.Optional[typing.Mapping[str,typing.Any]]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            description: Description for this parameter group.
            family: Database family of this parameter group.
            parameters: The parameters in this parameter group. Default: - No parameters.
        """
        props: ClusterParameterGroupProps = {"description": description, "family": family}

        if parameters is not None:
            props["parameters"] = parameters

        jsii.create(ClusterParameterGroup, self, [scope, id, props])

    @jsii.member(jsii_name="fromParameterGroupName")
    @classmethod
    def from_parameter_group_name(cls, scope: aws_cdk.cdk.Construct, id: str, parameter_group_name: str) -> "IClusterParameterGroup":
        """Import a parameter group.

        Arguments:
            scope: -
            id: -
            parameterGroupName: -
        """
        return jsii.sinvoke(cls, "fromParameterGroupName", [scope, id, parameter_group_name])

    @jsii.member(jsii_name="removeParameter")
    def remove_parameter(self, key: str) -> None:
        """Remove a previously-set parameter from this parameter group.

        Arguments:
            key: -
        """
        return jsii.invoke(self, "removeParameter", [key])

    @jsii.member(jsii_name="setParameter")
    def set_parameter(self, key: str, value: typing.Optional[str]=None) -> None:
        """Set a single parameter in this parameter group.

        Arguments:
            key: -
            value: -
        """
        return jsii.invoke(self, "setParameter", [key, value])

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[str]:
        """Validate this construct."""
        return jsii.invoke(self, "validate", [])

    @property
    @jsii.member(jsii_name="parameterGroupName")
    def parameter_group_name(self) -> str:
        """Name of this parameter group."""
        return jsii.get(self, "parameterGroupName")


@jsii.interface(jsii_type="@aws-cdk/aws-rds.IDatabaseCluster")
class IDatabaseCluster(aws_cdk.cdk.IResource, aws_cdk.aws_ec2.IConnectable, aws_cdk.aws_secretsmanager.ISecretAttachmentTarget, jsii.compat.Protocol):
    """Create a clustered database with a given number of instances."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IDatabaseClusterProxy

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        attribute:
            dbClusterEndpointAddress,dbClusterEndpointPort
        """
        ...

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster."""
        ...

    @property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        attribute:
            dbClusterReadEndpointAddress
        """
        ...

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica."""
        ...

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas."""
        ...

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """The security group for this database cluster."""
        ...


class _IDatabaseClusterProxy(jsii.proxy_for(aws_cdk.cdk.IResource), jsii.proxy_for(aws_cdk.aws_ec2.IConnectable), jsii.proxy_for(aws_cdk.aws_secretsmanager.ISecretAttachmentTarget)):
    """Create a clustered database with a given number of instances."""
    __jsii_type__ = "@aws-cdk/aws-rds.IDatabaseCluster"
    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations.

        attribute:
            dbClusterEndpointAddress,dbClusterEndpointPort
        """
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster."""
        return jsii.get(self, "clusterIdentifier")

    @property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations.

        attribute:
            dbClusterReadEndpointAddress
        """
        return jsii.get(self, "clusterReadEndpoint")

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica."""
        return jsii.get(self, "instanceEndpoints")

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas."""
        return jsii.get(self, "instanceIdentifiers")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """The security group for this database cluster."""
        return jsii.get(self, "securityGroupId")


@jsii.implements(IDatabaseCluster)
class DatabaseCluster(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.DatabaseCluster"):
    """Create a clustered database with a given number of instances.

    resource:
        AWS::RDS::DBCluster
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, engine: "DatabaseClusterEngine", instance_props: "InstanceProps", master_user: "Login", backup: typing.Optional["BackupProps"]=None, cluster_identifier: typing.Optional[str]=None, default_database_name: typing.Optional[str]=None, delete_replace_policy: typing.Optional[aws_cdk.cdk.DeletionPolicy]=None, instance_identifier_base: typing.Optional[str]=None, instances: typing.Optional[jsii.Number]=None, kms_key: typing.Optional[aws_cdk.aws_kms.IKey]=None, parameter_group: typing.Optional["IClusterParameterGroup"]=None, port: typing.Optional[jsii.Number]=None, preferred_maintenance_window: typing.Optional[str]=None, storage_encrypted: typing.Optional[bool]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            engine: What kind of database to start.
            instanceProps: Settings for the individual instances that are launched.
            masterUser: Username and password for the administrative user.
            backup: Backup settings. Default: - Backup retention period for automated backups is 1 day. Backup preferred window is set to a 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
            clusterIdentifier: An optional identifier for the cluster. Default: - A name is automatically generated.
            defaultDatabaseName: Name of a database which is automatically created inside the cluster. Default: - Database is not created in cluster.
            deleteReplacePolicy: The CloudFormation policy to apply when the cluster and its instances are removed from the stack or replaced during an update. Default: - Retain cluster.
            instanceIdentifierBase: Base identifier for instances. Every replica is named by appending the replica number to this string, 1-based. Default: - clusterIdentifier is used with the word "Instance" appended. If clusterIdentifier is not provided, the identifier is automatically generated.
            instances: How many replicas/instances to create. Has to be at least 1. Default: 2
            kmsKey: The KMS key for storage encryption. If specified ``storageEncrypted`` will be set to ``true``. Default: - default master key.
            parameterGroup: Additional parameters to pass to the database engine. Default: - No parameter group.
            port: What port to listen on. Default: - The default for the engine is used.
            preferredMaintenanceWindow: A daily time range in 24-hours UTC format in which backups preferably execute. Must be at least 30 minutes long. Example: '01:00-02:00' Default: - 30-minute window selected at random from an 8-hour block of time for each AWS Region, occurring on a random day of the week.
            storageEncrypted: Whether to enable storage encryption. Default: false
        """
        props: DatabaseClusterProps = {"engine": engine, "instanceProps": instance_props, "masterUser": master_user}

        if backup is not None:
            props["backup"] = backup

        if cluster_identifier is not None:
            props["clusterIdentifier"] = cluster_identifier

        if default_database_name is not None:
            props["defaultDatabaseName"] = default_database_name

        if delete_replace_policy is not None:
            props["deleteReplacePolicy"] = delete_replace_policy

        if instance_identifier_base is not None:
            props["instanceIdentifierBase"] = instance_identifier_base

        if instances is not None:
            props["instances"] = instances

        if kms_key is not None:
            props["kmsKey"] = kms_key

        if parameter_group is not None:
            props["parameterGroup"] = parameter_group

        if port is not None:
            props["port"] = port

        if preferred_maintenance_window is not None:
            props["preferredMaintenanceWindow"] = preferred_maintenance_window

        if storage_encrypted is not None:
            props["storageEncrypted"] = storage_encrypted

        jsii.create(DatabaseCluster, self, [scope, id, props])

    @jsii.member(jsii_name="fromDatabaseClusterAttributes")
    @classmethod
    def from_database_cluster_attributes(cls, scope: aws_cdk.cdk.Construct, id: str, *, cluster_endpoint_address: str, cluster_identifier: str, instance_endpoint_addresses: typing.List[str], instance_identifiers: typing.List[str], port: jsii.Number, reader_endpoint_address: str, security_group_id: str) -> "IDatabaseCluster":
        """Import an existing DatabaseCluster from properties.

        Arguments:
            scope: -
            id: -
            attrs: -
            clusterEndpointAddress: Cluster endpoint address.
            clusterIdentifier: Identifier for the cluster.
            instanceEndpointAddresses: Endpoint addresses of individual instances.
            instanceIdentifiers: Identifier for the instances.
            port: The database port.
            readerEndpointAddress: Reader endpoint address.
            securityGroupId: The security group for this database cluster.
        """
        attrs: DatabaseClusterAttributes = {"clusterEndpointAddress": cluster_endpoint_address, "clusterIdentifier": cluster_identifier, "instanceEndpointAddresses": instance_endpoint_addresses, "instanceIdentifiers": instance_identifiers, "port": port, "readerEndpointAddress": reader_endpoint_address, "securityGroupId": security_group_id}

        return jsii.sinvoke(cls, "fromDatabaseClusterAttributes", [scope, id, attrs])

    @jsii.member(jsii_name="addRotationSingleUser")
    def add_rotation_single_user(self, id: str, *, automatically_after_days: typing.Optional[jsii.Number]=None, serverless_application_location: typing.Optional["ServerlessApplicationLocation"]=None) -> "RotationSingleUser":
        """Adds the single user rotation of the master password to this cluster.

        Arguments:
            id: -
            options: -
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30 days
            serverlessApplicationLocation: The location of the serverless application for the rotation. Default: derived from the target's engine
        """
        options: RotationSingleUserOptions = {}

        if automatically_after_days is not None:
            options["automaticallyAfterDays"] = automatically_after_days

        if serverless_application_location is not None:
            options["serverlessApplicationLocation"] = serverless_application_location

        return jsii.invoke(self, "addRotationSingleUser", [id, options])

    @jsii.member(jsii_name="asSecretAttachmentTarget")
    def as_secret_attachment_target(self) -> aws_cdk.aws_secretsmanager.SecretAttachmentTargetProps:
        """Renders the secret attachment target specifications."""
        return jsii.invoke(self, "asSecretAttachmentTarget", [])

    @property
    @jsii.member(jsii_name="clusterEndpoint")
    def cluster_endpoint(self) -> "Endpoint":
        """The endpoint to use for read/write operations."""
        return jsii.get(self, "clusterEndpoint")

    @property
    @jsii.member(jsii_name="clusterIdentifier")
    def cluster_identifier(self) -> str:
        """Identifier of the cluster."""
        return jsii.get(self, "clusterIdentifier")

    @property
    @jsii.member(jsii_name="clusterReadEndpoint")
    def cluster_read_endpoint(self) -> "Endpoint":
        """Endpoint to use for load-balanced read-only operations."""
        return jsii.get(self, "clusterReadEndpoint")

    @property
    @jsii.member(jsii_name="connections")
    def connections(self) -> aws_cdk.aws_ec2.Connections:
        """Access to the network connections."""
        return jsii.get(self, "connections")

    @property
    @jsii.member(jsii_name="engine")
    def engine(self) -> "DatabaseClusterEngine":
        """The database engine of this cluster."""
        return jsii.get(self, "engine")

    @property
    @jsii.member(jsii_name="instanceEndpoints")
    def instance_endpoints(self) -> typing.List["Endpoint"]:
        """Endpoints which address each individual replica."""
        return jsii.get(self, "instanceEndpoints")

    @property
    @jsii.member(jsii_name="instanceIdentifiers")
    def instance_identifiers(self) -> typing.List[str]:
        """Identifiers of the replicas."""
        return jsii.get(self, "instanceIdentifiers")

    @property
    @jsii.member(jsii_name="securityGroupId")
    def security_group_id(self) -> str:
        """Security group identifier of this database."""
        return jsii.get(self, "securityGroupId")

    @property
    @jsii.member(jsii_name="secret")
    def secret(self) -> typing.Optional[aws_cdk.aws_secretsmanager.ISecret]:
        """The secret attached to this cluster."""
        return jsii.get(self, "secret")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _InstanceProps(jsii.compat.TypedDict, total=False):
    securityGroup: aws_cdk.aws_ec2.ISecurityGroup
    """Security group.

    If not specified a new one will be created.
    """
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection
    """Where to place the instances within the VPC."""

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.InstanceProps", jsii_struct_bases=[_InstanceProps])
class InstanceProps(_InstanceProps):
    """Instance properties for database instances."""
    instanceType: aws_cdk.aws_ec2.InstanceType
    """What type of instance to start for the replicas."""

    vpc: aws_cdk.aws_ec2.IVpc
    """What subnets to run the RDS instances in.

    Must be at least 2 subnets in two different AZs.
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _Login(jsii.compat.TypedDict, total=False):
    kmsKey: aws_cdk.aws_kms.IKey
    """KMS encryption key to encrypt the generated secret.

    Default:
        default master key
    """
    password: aws_cdk.cdk.SecretValue
    """Password.

    Do not put passwords in your CDK code directly.

    Default:
        a Secrets Manager generated password
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.Login", jsii_struct_bases=[_Login])
class Login(_Login):
    """Username and password combination."""
    username: str
    """Username."""

class RotationSingleUser(aws_cdk.cdk.Construct, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.RotationSingleUser"):
    """Single user secret rotation for a database instance or cluster."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, secret: aws_cdk.aws_secretsmanager.ISecret, target: aws_cdk.aws_ec2.IConnectable, vpc: aws_cdk.aws_ec2.IVpc, engine: typing.Optional["DatabaseEngine"]=None, vpc_subnets: typing.Optional[aws_cdk.aws_ec2.SubnetSelection]=None, automatically_after_days: typing.Optional[jsii.Number]=None, serverless_application_location: typing.Optional["ServerlessApplicationLocation"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            secret: The secret to rotate. It must be a JSON string with the following format: { 'engine': <required: database engine>, 'host': <required: instance host name>, 'username': <required: username>, 'password': <required: password>, 'dbname': <optional: database name>, 'port': <optional: if not specified, default port will be used> } This is typically the case for a secret referenced from an AWS::SecretsManager::SecretTargetAttachment https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
            target: The target database cluster or instance.
            vpc: The VPC where the Lambda rotation function will run.
            engine: The database engine. Either ``serverlessApplicationLocation`` or ``engine`` must be specified. Default: - No engine specified.
            vpcSubnets: The type of subnets in the VPC where the Lambda rotation function will run. Default: - Private subnets.
            automaticallyAfterDays: Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation. Default: 30 days
            serverlessApplicationLocation: The location of the serverless application for the rotation. Default: derived from the target's engine
        """
        props: RotationSingleUserProps = {"secret": secret, "target": target, "vpc": vpc}

        if engine is not None:
            props["engine"] = engine

        if vpc_subnets is not None:
            props["vpcSubnets"] = vpc_subnets

        if automatically_after_days is not None:
            props["automaticallyAfterDays"] = automatically_after_days

        if serverless_application_location is not None:
            props["serverlessApplicationLocation"] = serverless_application_location

        jsii.create(RotationSingleUser, self, [scope, id, props])


@jsii.data_type(jsii_type="@aws-cdk/aws-rds.RotationSingleUserOptions", jsii_struct_bases=[])
class RotationSingleUserOptions(jsii.compat.TypedDict, total=False):
    """Options to add single user rotation to a database instance or cluster."""
    automaticallyAfterDays: jsii.Number
    """Specifies the number of days after the previous rotation before Secrets Manager triggers the next automatic rotation.

    Default:
        30 days
    """

    serverlessApplicationLocation: "ServerlessApplicationLocation"
    """The location of the serverless application for the rotation.

    Default:
        derived from the target's engine
    """

@jsii.data_type_optionals(jsii_struct_bases=[RotationSingleUserOptions])
class _RotationSingleUserProps(RotationSingleUserOptions, jsii.compat.TypedDict, total=False):
    engine: "DatabaseEngine"
    """The database engine.

    Either ``serverlessApplicationLocation`` or ``engine`` must be specified.

    Default:
        - No engine specified.
    """
    vpcSubnets: aws_cdk.aws_ec2.SubnetSelection
    """The type of subnets in the VPC where the Lambda rotation function will run.

    Default:
        - Private subnets.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-rds.RotationSingleUserProps", jsii_struct_bases=[_RotationSingleUserProps])
class RotationSingleUserProps(_RotationSingleUserProps):
    """Construction properties for a RotationSingleUser."""
    secret: aws_cdk.aws_secretsmanager.ISecret
    """The secret to rotate.

    It must be a JSON string with the following format:
    {
    'engine': <required: database engine>,
    'host': <required: instance host name>,
    'username': <required: username>,
    'password': <required: password>,
    'dbname': <optional: database name>,
    'port': <optional: if not specified, default port will be used>
    }

    This is typically the case for a secret referenced from an AWS::SecretsManager::SecretTargetAttachment
    https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-secretsmanager-secrettargetattachment.html
    """

    target: aws_cdk.aws_ec2.IConnectable
    """The target database cluster or instance."""

    vpc: aws_cdk.aws_ec2.IVpc
    """The VPC where the Lambda rotation function will run."""

class ServerlessApplicationLocation(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-rds.ServerlessApplicationLocation"):
    """A serverless application location."""
    def __init__(self, application_id: str, semantic_version: str) -> None:
        """
        Arguments:
            applicationId: -
            semanticVersion: -
        """
        jsii.create(ServerlessApplicationLocation, self, [application_id, semantic_version])

    @classproperty
    @jsii.member(jsii_name="MariaDbRotationSingleUser")
    def MARIA_DB_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "MariaDbRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="MysqlRotationSingleUser")
    def MYSQL_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "MysqlRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="OracleRotationSingleUser")
    def ORACLE_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "OracleRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="PostgresRotationSingleUser")
    def POSTGRES_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "PostgresRotationSingleUser")

    @classproperty
    @jsii.member(jsii_name="SqlServerRotationSingleUser")
    def SQL_SERVER_ROTATION_SINGLE_USER(cls) -> "ServerlessApplicationLocation":
        return jsii.sget(cls, "SqlServerRotationSingleUser")

    @property
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        return jsii.get(self, "applicationId")

    @property
    @jsii.member(jsii_name="semanticVersion")
    def semantic_version(self) -> str:
        return jsii.get(self, "semanticVersion")


__all__ = ["BackupProps", "CfnDBCluster", "CfnDBClusterParameterGroup", "CfnDBClusterParameterGroupProps", "CfnDBClusterProps", "CfnDBInstance", "CfnDBInstanceProps", "CfnDBParameterGroup", "CfnDBParameterGroupProps", "CfnDBSecurityGroup", "CfnDBSecurityGroupIngress", "CfnDBSecurityGroupIngressProps", "CfnDBSecurityGroupProps", "CfnDBSubnetGroup", "CfnDBSubnetGroupProps", "CfnEventSubscription", "CfnEventSubscriptionProps", "CfnOptionGroup", "CfnOptionGroupProps", "ClusterParameterGroup", "ClusterParameterGroupImportProps", "ClusterParameterGroupProps", "DatabaseCluster", "DatabaseClusterAttributes", "DatabaseClusterEngine", "DatabaseClusterProps", "DatabaseEngine", "DatabaseSecret", "DatabaseSecretProps", "Endpoint", "IClusterParameterGroup", "IDatabaseCluster", "InstanceProps", "Login", "RotationSingleUser", "RotationSingleUserOptions", "RotationSingleUserProps", "ServerlessApplicationLocation", "__jsii_assembly__"]

publication.publish()
