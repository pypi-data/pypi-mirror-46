import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kinesisfirehose", "0.32.0", __name__, "aws-kinesisfirehose@0.32.0.jsii.tgz")
class CfnDeliveryStream(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream"):
    """A CloudFormation ``AWS::KinesisFirehose::DeliveryStream``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html
    cloudformationResource:
        AWS::KinesisFirehose::DeliveryStream
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, delivery_stream_name: typing.Optional[str]=None, delivery_stream_type: typing.Optional[str]=None, elasticsearch_destination_configuration: typing.Optional[typing.Union[typing.Optional["ElasticsearchDestinationConfigurationProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None, extended_s3_destination_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ExtendedS3DestinationConfigurationProperty"]]]=None, kinesis_stream_source_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["KinesisStreamSourceConfigurationProperty"]]]=None, redshift_destination_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["RedshiftDestinationConfigurationProperty"]]]=None, s3_destination_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["S3DestinationConfigurationProperty"]]]=None, splunk_destination_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["SplunkDestinationConfigurationProperty"]]]=None) -> None:
        """Create a new ``AWS::KinesisFirehose::DeliveryStream``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            deliveryStreamName: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamName``.
            deliveryStreamType: ``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamType``.
            elasticsearchDestinationConfiguration: ``AWS::KinesisFirehose::DeliveryStream.ElasticsearchDestinationConfiguration``.
            extendedS3DestinationConfiguration: ``AWS::KinesisFirehose::DeliveryStream.ExtendedS3DestinationConfiguration``.
            kinesisStreamSourceConfiguration: ``AWS::KinesisFirehose::DeliveryStream.KinesisStreamSourceConfiguration``.
            redshiftDestinationConfiguration: ``AWS::KinesisFirehose::DeliveryStream.RedshiftDestinationConfiguration``.
            s3DestinationConfiguration: ``AWS::KinesisFirehose::DeliveryStream.S3DestinationConfiguration``.
            splunkDestinationConfiguration: ``AWS::KinesisFirehose::DeliveryStream.SplunkDestinationConfiguration``.
        """
        props: CfnDeliveryStreamProps = {}

        if delivery_stream_name is not None:
            props["deliveryStreamName"] = delivery_stream_name

        if delivery_stream_type is not None:
            props["deliveryStreamType"] = delivery_stream_type

        if elasticsearch_destination_configuration is not None:
            props["elasticsearchDestinationConfiguration"] = elasticsearch_destination_configuration

        if extended_s3_destination_configuration is not None:
            props["extendedS3DestinationConfiguration"] = extended_s3_destination_configuration

        if kinesis_stream_source_configuration is not None:
            props["kinesisStreamSourceConfiguration"] = kinesis_stream_source_configuration

        if redshift_destination_configuration is not None:
            props["redshiftDestinationConfiguration"] = redshift_destination_configuration

        if s3_destination_configuration is not None:
            props["s3DestinationConfiguration"] = s3_destination_configuration

        if splunk_destination_configuration is not None:
            props["splunkDestinationConfiguration"] = splunk_destination_configuration

        jsii.create(CfnDeliveryStream, self, [scope, id, props])

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
    @jsii.member(jsii_name="deliveryStreamArn")
    def delivery_stream_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "deliveryStreamArn")

    @property
    @jsii.member(jsii_name="deliveryStreamName")
    def delivery_stream_name(self) -> str:
        return jsii.get(self, "deliveryStreamName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeliveryStreamProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.BufferingHintsProperty", jsii_struct_bases=[])
    class BufferingHintsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html
        """
        intervalInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.BufferingHintsProperty.IntervalInSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html#cfn-kinesisfirehose-deliverystream-bufferinghints-intervalinseconds
        """

        sizeInMBs: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.BufferingHintsProperty.SizeInMBs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-bufferinghints.html#cfn-kinesisfirehose-deliverystream-bufferinghints-sizeinmbs
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.CloudWatchLoggingOptionsProperty", jsii_struct_bases=[])
    class CloudWatchLoggingOptionsProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-enabled
        """

        logGroupName: str
        """``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.LogGroupName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-loggroupname
        """

        logStreamName: str
        """``CfnDeliveryStream.CloudWatchLoggingOptionsProperty.LogStreamName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-cloudwatchloggingoptions.html#cfn-kinesisfirehose-deliverystream-cloudwatchloggingoptions-logstreamname
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CopyCommandProperty(jsii.compat.TypedDict, total=False):
        copyOptions: str
        """``CfnDeliveryStream.CopyCommandProperty.CopyOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-copyoptions
        """
        dataTableColumns: str
        """``CfnDeliveryStream.CopyCommandProperty.DataTableColumns``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-datatablecolumns
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.CopyCommandProperty", jsii_struct_bases=[_CopyCommandProperty])
    class CopyCommandProperty(_CopyCommandProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html
        """
        dataTableName: str
        """``CfnDeliveryStream.CopyCommandProperty.DataTableName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-copycommand.html#cfn-kinesisfirehose-deliverystream-copycommand-datatablename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchBufferingHintsProperty", jsii_struct_bases=[])
    class ElasticsearchBufferingHintsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html
        """
        intervalInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.ElasticsearchBufferingHintsProperty.IntervalInSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html#cfn-kinesisfirehose-deliverystream-elasticsearchbufferinghints-intervalinseconds
        """

        sizeInMBs: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.ElasticsearchBufferingHintsProperty.SizeInMBs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchbufferinghints.html#cfn-kinesisfirehose-deliverystream-elasticsearchbufferinghints-sizeinmbs
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ElasticsearchDestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.CloudWatchLoggingOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-cloudwatchloggingoptions
        """
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.ProcessingConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-processingconfiguration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty", jsii_struct_bases=[_ElasticsearchDestinationConfigurationProperty])
    class ElasticsearchDestinationConfigurationProperty(_ElasticsearchDestinationConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html
        """
        bufferingHints: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ElasticsearchBufferingHintsProperty"]
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.BufferingHints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-bufferinghints
        """

        domainArn: str
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.DomainARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-domainarn
        """

        indexName: str
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.IndexName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-indexname
        """

        indexRotationPeriod: str
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.IndexRotationPeriod``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-indexrotationperiod
        """

        retryOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ElasticsearchRetryOptionsProperty"]
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.RetryOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-retryoptions
        """

        roleArn: str
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-rolearn
        """

        s3BackupMode: str
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.S3BackupMode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-s3backupmode
        """

        s3Configuration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.S3Configuration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-s3configuration
        """

        typeName: str
        """``CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty.TypeName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration-typename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ElasticsearchRetryOptionsProperty", jsii_struct_bases=[])
    class ElasticsearchRetryOptionsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchretryoptions.html
        """
        durationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.ElasticsearchRetryOptionsProperty.DurationInSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-elasticsearchretryoptions.html#cfn-kinesisfirehose-deliverystream-elasticsearchretryoptions-durationinseconds
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.EncryptionConfigurationProperty", jsii_struct_bases=[])
    class EncryptionConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html
        """
        kmsEncryptionConfig: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.KMSEncryptionConfigProperty"]
        """``CfnDeliveryStream.EncryptionConfigurationProperty.KMSEncryptionConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html#cfn-kinesisfirehose-deliverystream-encryptionconfiguration-kmsencryptionconfig
        """

        noEncryptionConfig: str
        """``CfnDeliveryStream.EncryptionConfigurationProperty.NoEncryptionConfig``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-encryptionconfiguration.html#cfn-kinesisfirehose-deliverystream-encryptionconfiguration-noencryptionconfig
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ExtendedS3DestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.CloudWatchLoggingOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-cloudwatchloggingoptions
        """
        encryptionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.EncryptionConfigurationProperty"]
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.EncryptionConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-encryptionconfiguration
        """
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.ProcessingConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-processingconfiguration
        """
        s3BackupConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.S3BackupConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-s3backupconfiguration
        """
        s3BackupMode: str
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.S3BackupMode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-s3backupmode
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty", jsii_struct_bases=[_ExtendedS3DestinationConfigurationProperty])
    class ExtendedS3DestinationConfigurationProperty(_ExtendedS3DestinationConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html
        """
        bucketArn: str
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.BucketARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-bucketarn
        """

        bufferingHints: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.BufferingHintsProperty"]
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.BufferingHints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-bufferinghints
        """

        compressionFormat: str
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.CompressionFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-compressionformat
        """

        prefix: str
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-prefix
        """

        roleArn: str
        """``CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-extendeds3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.KMSEncryptionConfigProperty", jsii_struct_bases=[])
    class KMSEncryptionConfigProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kmsencryptionconfig.html
        """
        awskmsKeyArn: str
        """``CfnDeliveryStream.KMSEncryptionConfigProperty.AWSKMSKeyARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kmsencryptionconfig.html#cfn-kinesisfirehose-deliverystream-kmsencryptionconfig-awskmskeyarn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.KinesisStreamSourceConfigurationProperty", jsii_struct_bases=[])
    class KinesisStreamSourceConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html
        """
        kinesisStreamArn: str
        """``CfnDeliveryStream.KinesisStreamSourceConfigurationProperty.KinesisStreamARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration-kinesisstreamarn
        """

        roleArn: str
        """``CfnDeliveryStream.KinesisStreamSourceConfigurationProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessingConfigurationProperty", jsii_struct_bases=[])
    class ProcessingConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html
        """
        enabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.ProcessingConfigurationProperty.Enabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html#cfn-kinesisfirehose-deliverystream-processingconfiguration-enabled
        """

        processors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessorProperty"]]]
        """``CfnDeliveryStream.ProcessingConfigurationProperty.Processors``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processingconfiguration.html#cfn-kinesisfirehose-deliverystream-processingconfiguration-processors
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessorParameterProperty", jsii_struct_bases=[])
    class ProcessorParameterProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html
        """
        parameterName: str
        """``CfnDeliveryStream.ProcessorParameterProperty.ParameterName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html#cfn-kinesisfirehose-deliverystream-processorparameter-parametername
        """

        parameterValue: str
        """``CfnDeliveryStream.ProcessorParameterProperty.ParameterValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processorparameter.html#cfn-kinesisfirehose-deliverystream-processorparameter-parametervalue
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.ProcessorProperty", jsii_struct_bases=[])
    class ProcessorProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html
        """
        parameters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessorParameterProperty"]]]
        """``CfnDeliveryStream.ProcessorProperty.Parameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-parameters
        """

        type: str
        """``CfnDeliveryStream.ProcessorProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-processor.html#cfn-kinesisfirehose-deliverystream-processor-type
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RedshiftDestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.CloudWatchLoggingOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-cloudwatchloggingoptions
        """
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.ProcessingConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-processingconfiguration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.RedshiftDestinationConfigurationProperty", jsii_struct_bases=[_RedshiftDestinationConfigurationProperty])
    class RedshiftDestinationConfigurationProperty(_RedshiftDestinationConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html
        """
        clusterJdbcurl: str
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.ClusterJDBCURL``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-clusterjdbcurl
        """

        copyCommand: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CopyCommandProperty"]
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.CopyCommand``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-copycommand
        """

        password: str
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.Password``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-password
        """

        roleArn: str
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-rolearn
        """

        s3Configuration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.S3Configuration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-s3configuration
        """

        username: str
        """``CfnDeliveryStream.RedshiftDestinationConfigurationProperty.Username``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-redshiftdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration-username
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _S3DestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.CloudWatchLoggingOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-cloudwatchloggingoptions
        """
        encryptionConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.EncryptionConfigurationProperty"]
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.EncryptionConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-encryptionconfiguration
        """
        prefix: str
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.Prefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-prefix
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.S3DestinationConfigurationProperty", jsii_struct_bases=[_S3DestinationConfigurationProperty])
    class S3DestinationConfigurationProperty(_S3DestinationConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html
        """
        bucketArn: str
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.BucketARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-bucketarn
        """

        bufferingHints: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.BufferingHintsProperty"]
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.BufferingHints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-bufferinghints
        """

        compressionFormat: str
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.CompressionFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-compressionformat
        """

        roleArn: str
        """``CfnDeliveryStream.S3DestinationConfigurationProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-s3destinationconfiguration.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration-rolearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SplunkDestinationConfigurationProperty(jsii.compat.TypedDict, total=False):
        cloudWatchLoggingOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.CloudWatchLoggingOptionsProperty"]
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.CloudWatchLoggingOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-cloudwatchloggingoptions
        """
        hecAcknowledgmentTimeoutInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECAcknowledgmentTimeoutInSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecacknowledgmenttimeoutinseconds
        """
        processingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ProcessingConfigurationProperty"]
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.ProcessingConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-processingconfiguration
        """
        retryOptions: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.SplunkRetryOptionsProperty"]
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.RetryOptions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-retryoptions
        """
        s3BackupMode: str
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.S3BackupMode``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-s3backupmode
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SplunkDestinationConfigurationProperty", jsii_struct_bases=[_SplunkDestinationConfigurationProperty])
    class SplunkDestinationConfigurationProperty(_SplunkDestinationConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html
        """
        hecEndpoint: str
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECEndpoint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecendpoint
        """

        hecEndpointType: str
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECEndpointType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hecendpointtype
        """

        hecToken: str
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.HECToken``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-hectoken
        """

        s3Configuration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
        """``CfnDeliveryStream.SplunkDestinationConfigurationProperty.S3Configuration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkdestinationconfiguration.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration-s3configuration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStream.SplunkRetryOptionsProperty", jsii_struct_bases=[])
    class SplunkRetryOptionsProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkretryoptions.html
        """
        durationInSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDeliveryStream.SplunkRetryOptionsProperty.DurationInSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisfirehose-deliverystream-splunkretryoptions.html#cfn-kinesisfirehose-deliverystream-splunkretryoptions-durationinseconds
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisfirehose.CfnDeliveryStreamProps", jsii_struct_bases=[])
class CfnDeliveryStreamProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::KinesisFirehose::DeliveryStream``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html
    """
    deliveryStreamName: str
    """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamname
    """

    deliveryStreamType: str
    """``AWS::KinesisFirehose::DeliveryStream.DeliveryStreamType``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-deliverystreamtype
    """

    elasticsearchDestinationConfiguration: typing.Union["CfnDeliveryStream.ElasticsearchDestinationConfigurationProperty", aws_cdk.cdk.Token]
    """``AWS::KinesisFirehose::DeliveryStream.ElasticsearchDestinationConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-elasticsearchdestinationconfiguration
    """

    extendedS3DestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.ExtendedS3DestinationConfigurationProperty"]
    """``AWS::KinesisFirehose::DeliveryStream.ExtendedS3DestinationConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-extendeds3destinationconfiguration
    """

    kinesisStreamSourceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.KinesisStreamSourceConfigurationProperty"]
    """``AWS::KinesisFirehose::DeliveryStream.KinesisStreamSourceConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-kinesisstreamsourceconfiguration
    """

    redshiftDestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.RedshiftDestinationConfigurationProperty"]
    """``AWS::KinesisFirehose::DeliveryStream.RedshiftDestinationConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-redshiftdestinationconfiguration
    """

    s3DestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.S3DestinationConfigurationProperty"]
    """``AWS::KinesisFirehose::DeliveryStream.S3DestinationConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-s3destinationconfiguration
    """

    splunkDestinationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryStream.SplunkDestinationConfigurationProperty"]
    """``AWS::KinesisFirehose::DeliveryStream.SplunkDestinationConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisfirehose-deliverystream.html#cfn-kinesisfirehose-deliverystream-splunkdestinationconfiguration
    """

__all__ = ["CfnDeliveryStream", "CfnDeliveryStreamProps", "__jsii_assembly__"]

publication.publish()
