import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-kinesisanalytics", "0.32.0", __name__, "aws-kinesisanalytics@0.32.0.jsii.tgz")
class CfnApplication(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication"):
    """A CloudFormation ``AWS::KinesisAnalytics::Application``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html
    cloudformationResource:
        AWS::KinesisAnalytics::Application
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, inputs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["InputProperty", aws_cdk.cdk.Token]]], application_code: typing.Optional[str]=None, application_description: typing.Optional[str]=None, application_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::KinesisAnalytics::Application``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            inputs: ``AWS::KinesisAnalytics::Application.Inputs``.
            applicationCode: ``AWS::KinesisAnalytics::Application.ApplicationCode``.
            applicationDescription: ``AWS::KinesisAnalytics::Application.ApplicationDescription``.
            applicationName: ``AWS::KinesisAnalytics::Application.ApplicationName``.
        """
        props: CfnApplicationProps = {"inputs": inputs}

        if application_code is not None:
            props["applicationCode"] = application_code

        if application_description is not None:
            props["applicationDescription"] = application_description

        if application_name is not None:
            props["applicationName"] = application_name

        jsii.create(CfnApplication, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationId")
    def application_id(self) -> str:
        return jsii.get(self, "applicationId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.CSVMappingParametersProperty", jsii_struct_bases=[])
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html
        """
        recordColumnDelimiter: str
        """``CfnApplication.CSVMappingParametersProperty.RecordColumnDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html#cfn-kinesisanalytics-application-csvmappingparameters-recordcolumndelimiter
        """

        recordRowDelimiter: str
        """``CfnApplication.CSVMappingParametersProperty.RecordRowDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-csvmappingparameters.html#cfn-kinesisanalytics-application-csvmappingparameters-recordrowdelimiter
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputLambdaProcessorProperty", jsii_struct_bases=[])
    class InputLambdaProcessorProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html
        """
        resourceArn: str
        """``CfnApplication.InputLambdaProcessorProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html#cfn-kinesisanalytics-application-inputlambdaprocessor-resourcearn
        """

        roleArn: str
        """``CfnApplication.InputLambdaProcessorProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputlambdaprocessor.html#cfn-kinesisanalytics-application-inputlambdaprocessor-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputParallelismProperty", jsii_struct_bases=[])
    class InputParallelismProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputparallelism.html
        """
        count: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplication.InputParallelismProperty.Count``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputparallelism.html#cfn-kinesisanalytics-application-inputparallelism-count
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputProcessingConfigurationProperty", jsii_struct_bases=[])
    class InputProcessingConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html
        """
        inputLambdaProcessor: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputLambdaProcessorProperty"]
        """``CfnApplication.InputProcessingConfigurationProperty.InputLambdaProcessor``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputprocessingconfiguration.html#cfn-kinesisanalytics-application-inputprocessingconfiguration-inputlambdaprocessor
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _InputProperty(jsii.compat.TypedDict, total=False):
        inputParallelism: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputParallelismProperty"]
        """``CfnApplication.InputProperty.InputParallelism``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputparallelism
        """
        inputProcessingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputProcessingConfigurationProperty"]
        """``CfnApplication.InputProperty.InputProcessingConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputprocessingconfiguration
        """
        kinesisFirehoseInput: typing.Union[aws_cdk.cdk.Token, "CfnApplication.KinesisFirehoseInputProperty"]
        """``CfnApplication.InputProperty.KinesisFirehoseInput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-kinesisfirehoseinput
        """
        kinesisStreamsInput: typing.Union[aws_cdk.cdk.Token, "CfnApplication.KinesisStreamsInputProperty"]
        """``CfnApplication.InputProperty.KinesisStreamsInput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-kinesisstreamsinput
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputProperty", jsii_struct_bases=[_InputProperty])
    class InputProperty(_InputProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html
        """
        inputSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplication.InputSchemaProperty"]
        """``CfnApplication.InputProperty.InputSchema``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-inputschema
        """

        namePrefix: str
        """``CfnApplication.InputProperty.NamePrefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-input.html#cfn-kinesisanalytics-application-input-nameprefix
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _InputSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str
        """``CfnApplication.InputSchemaProperty.RecordEncoding``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordencoding
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.InputSchemaProperty", jsii_struct_bases=[_InputSchemaProperty])
    class InputSchemaProperty(_InputSchemaProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html
        """
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplication.RecordColumnProperty"]]]
        """``CfnApplication.InputSchemaProperty.RecordColumns``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordcolumns
        """

        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplication.RecordFormatProperty"]
        """``CfnApplication.InputSchemaProperty.RecordFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-inputschema.html#cfn-kinesisanalytics-application-inputschema-recordformat
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.JSONMappingParametersProperty", jsii_struct_bases=[])
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-jsonmappingparameters.html
        """
        recordRowPath: str
        """``CfnApplication.JSONMappingParametersProperty.RecordRowPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-jsonmappingparameters.html#cfn-kinesisanalytics-application-jsonmappingparameters-recordrowpath
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.KinesisFirehoseInputProperty", jsii_struct_bases=[])
    class KinesisFirehoseInputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html
        """
        resourceArn: str
        """``CfnApplication.KinesisFirehoseInputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html#cfn-kinesisanalytics-application-kinesisfirehoseinput-resourcearn
        """

        roleArn: str
        """``CfnApplication.KinesisFirehoseInputProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisfirehoseinput.html#cfn-kinesisanalytics-application-kinesisfirehoseinput-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.KinesisStreamsInputProperty", jsii_struct_bases=[])
    class KinesisStreamsInputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html
        """
        resourceArn: str
        """``CfnApplication.KinesisStreamsInputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html#cfn-kinesisanalytics-application-kinesisstreamsinput-resourcearn
        """

        roleArn: str
        """``CfnApplication.KinesisStreamsInputProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-kinesisstreamsinput.html#cfn-kinesisanalytics-application-kinesisstreamsinput-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.MappingParametersProperty", jsii_struct_bases=[])
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html
        """
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplication.CSVMappingParametersProperty"]
        """``CfnApplication.MappingParametersProperty.CSVMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html#cfn-kinesisanalytics-application-mappingparameters-csvmappingparameters
        """

        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplication.JSONMappingParametersProperty"]
        """``CfnApplication.MappingParametersProperty.JSONMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-mappingparameters.html#cfn-kinesisanalytics-application-mappingparameters-jsonmappingparameters
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str
        """``CfnApplication.RecordColumnProperty.Mapping``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-mapping
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.RecordColumnProperty", jsii_struct_bases=[_RecordColumnProperty])
    class RecordColumnProperty(_RecordColumnProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html
        """
        name: str
        """``CfnApplication.RecordColumnProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-name
        """

        sqlType: str
        """``CfnApplication.RecordColumnProperty.SqlType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordcolumn.html#cfn-kinesisanalytics-application-recordcolumn-sqltype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplication.MappingParametersProperty"]
        """``CfnApplication.RecordFormatProperty.MappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html#cfn-kinesisanalytics-application-recordformat-mappingparameters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplication.RecordFormatProperty", jsii_struct_bases=[_RecordFormatProperty])
    class RecordFormatProperty(_RecordFormatProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html
        """
        recordFormatType: str
        """``CfnApplication.RecordFormatProperty.RecordFormatType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-application-recordformat.html#cfn-kinesisanalytics-application-recordformat-recordformattype
        """


class CfnApplicationCloudWatchLoggingOptionV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2"):
    """A CloudFormation ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html
    cloudformationResource:
        AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, cloud_watch_logging_option: typing.Union[aws_cdk.cdk.Token, "CloudWatchLoggingOptionProperty"]) -> None:
        """Create a new ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.ApplicationName``.
            cloudWatchLoggingOption: ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.CloudWatchLoggingOption``.
        """
        props: CfnApplicationCloudWatchLoggingOptionV2Props = {"applicationName": application_name, "cloudWatchLoggingOption": cloud_watch_logging_option}

        jsii.create(CfnApplicationCloudWatchLoggingOptionV2, self, [scope, id, props])

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
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationCloudWatchLoggingOptionV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty", jsii_struct_bases=[])
    class CloudWatchLoggingOptionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption.html
        """
        logStreamArn: str
        """``CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty.LogStreamARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption-logstreamarn
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationCloudWatchLoggingOptionV2Props", jsii_struct_bases=[])
class CfnApplicationCloudWatchLoggingOptionV2Props(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html
    """
    applicationName: str
    """``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-applicationname
    """

    cloudWatchLoggingOption: typing.Union[aws_cdk.cdk.Token, "CfnApplicationCloudWatchLoggingOptionV2.CloudWatchLoggingOptionProperty"]
    """``AWS::KinesisAnalyticsV2::ApplicationCloudWatchLoggingOption.CloudWatchLoggingOption``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationcloudwatchloggingoption.html#cfn-kinesisanalyticsv2-applicationcloudwatchloggingoption-cloudwatchloggingoption
    """

class CfnApplicationOutput(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput"):
    """A CloudFormation ``AWS::KinesisAnalytics::ApplicationOutput``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html
    cloudformationResource:
        AWS::KinesisAnalytics::ApplicationOutput
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, output: typing.Union[aws_cdk.cdk.Token, "OutputProperty"]) -> None:
        """Create a new ``AWS::KinesisAnalytics::ApplicationOutput``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::KinesisAnalytics::ApplicationOutput.ApplicationName``.
            output: ``AWS::KinesisAnalytics::ApplicationOutput.Output``.
        """
        props: CfnApplicationOutputProps = {"applicationName": application_name, "output": output}

        jsii.create(CfnApplicationOutput, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationOutputId")
    def application_output_id(self) -> str:
        return jsii.get(self, "applicationOutputId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationOutputProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.DestinationSchemaProperty", jsii_struct_bases=[])
    class DestinationSchemaProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-destinationschema.html
        """
        recordFormatType: str
        """``CfnApplicationOutput.DestinationSchemaProperty.RecordFormatType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-destinationschema.html#cfn-kinesisanalytics-applicationoutput-destinationschema-recordformattype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.KinesisFirehoseOutputProperty", jsii_struct_bases=[])
    class KinesisFirehoseOutputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html
        """
        resourceArn: str
        """``CfnApplicationOutput.KinesisFirehoseOutputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisfirehoseoutput-resourcearn
        """

        roleArn: str
        """``CfnApplicationOutput.KinesisFirehoseOutputProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisfirehoseoutput-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.KinesisStreamsOutputProperty", jsii_struct_bases=[])
    class KinesisStreamsOutputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html
        """
        resourceArn: str
        """``CfnApplicationOutput.KinesisStreamsOutputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisstreamsoutput-resourcearn
        """

        roleArn: str
        """``CfnApplicationOutput.KinesisStreamsOutputProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalytics-applicationoutput-kinesisstreamsoutput-rolearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.LambdaOutputProperty", jsii_struct_bases=[])
    class LambdaOutputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html
        """
        resourceArn: str
        """``CfnApplicationOutput.LambdaOutputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html#cfn-kinesisanalytics-applicationoutput-lambdaoutput-resourcearn
        """

        roleArn: str
        """``CfnApplicationOutput.LambdaOutputProperty.RoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-lambdaoutput.html#cfn-kinesisanalytics-applicationoutput-lambdaoutput-rolearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OutputProperty(jsii.compat.TypedDict, total=False):
        kinesisFirehoseOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.KinesisFirehoseOutputProperty"]
        """``CfnApplicationOutput.OutputProperty.KinesisFirehoseOutput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-kinesisfirehoseoutput
        """
        kinesisStreamsOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.KinesisStreamsOutputProperty"]
        """``CfnApplicationOutput.OutputProperty.KinesisStreamsOutput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-kinesisstreamsoutput
        """
        lambdaOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.LambdaOutputProperty"]
        """``CfnApplicationOutput.OutputProperty.LambdaOutput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-lambdaoutput
        """
        name: str
        """``CfnApplicationOutput.OutputProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutput.OutputProperty", jsii_struct_bases=[_OutputProperty])
    class OutputProperty(_OutputProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html
        """
        destinationSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.DestinationSchemaProperty"]
        """``CfnApplicationOutput.OutputProperty.DestinationSchema``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationoutput-output.html#cfn-kinesisanalytics-applicationoutput-output-destinationschema
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputProps", jsii_struct_bases=[])
class CfnApplicationOutputProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::KinesisAnalytics::ApplicationOutput``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html
    """
    applicationName: str
    """``AWS::KinesisAnalytics::ApplicationOutput.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-applicationname
    """

    output: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutput.OutputProperty"]
    """``AWS::KinesisAnalytics::ApplicationOutput.Output``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationoutput.html#cfn-kinesisanalytics-applicationoutput-output
    """

class CfnApplicationOutputV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2"):
    """A CloudFormation ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html
    cloudformationResource:
        AWS::KinesisAnalyticsV2::ApplicationOutput
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, output: typing.Union[aws_cdk.cdk.Token, "OutputProperty"]) -> None:
        """Create a new ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::KinesisAnalyticsV2::ApplicationOutput.ApplicationName``.
            output: ``AWS::KinesisAnalyticsV2::ApplicationOutput.Output``.
        """
        props: CfnApplicationOutputV2Props = {"applicationName": application_name, "output": output}

        jsii.create(CfnApplicationOutputV2, self, [scope, id, props])

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
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationOutputV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.DestinationSchemaProperty", jsii_struct_bases=[])
    class DestinationSchemaProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-destinationschema.html
        """
        recordFormatType: str
        """``CfnApplicationOutputV2.DestinationSchemaProperty.RecordFormatType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-destinationschema.html#cfn-kinesisanalyticsv2-applicationoutput-destinationschema-recordformattype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.KinesisFirehoseOutputProperty", jsii_struct_bases=[])
    class KinesisFirehoseOutputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput.html
        """
        resourceArn: str
        """``CfnApplicationOutputV2.KinesisFirehoseOutputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput.html#cfn-kinesisanalyticsv2-applicationoutput-kinesisfirehoseoutput-resourcearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.KinesisStreamsOutputProperty", jsii_struct_bases=[])
    class KinesisStreamsOutputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput.html
        """
        resourceArn: str
        """``CfnApplicationOutputV2.KinesisStreamsOutputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput.html#cfn-kinesisanalyticsv2-applicationoutput-kinesisstreamsoutput-resourcearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.LambdaOutputProperty", jsii_struct_bases=[])
    class LambdaOutputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-lambdaoutput.html
        """
        resourceArn: str
        """``CfnApplicationOutputV2.LambdaOutputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-lambdaoutput.html#cfn-kinesisanalyticsv2-applicationoutput-lambdaoutput-resourcearn
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OutputProperty(jsii.compat.TypedDict, total=False):
        kinesisFirehoseOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.KinesisFirehoseOutputProperty"]
        """``CfnApplicationOutputV2.OutputProperty.KinesisFirehoseOutput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-kinesisfirehoseoutput
        """
        kinesisStreamsOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.KinesisStreamsOutputProperty"]
        """``CfnApplicationOutputV2.OutputProperty.KinesisStreamsOutput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-kinesisstreamsoutput
        """
        lambdaOutput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.LambdaOutputProperty"]
        """``CfnApplicationOutputV2.OutputProperty.LambdaOutput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-lambdaoutput
        """
        name: str
        """``CfnApplicationOutputV2.OutputProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2.OutputProperty", jsii_struct_bases=[_OutputProperty])
    class OutputProperty(_OutputProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html
        """
        destinationSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.DestinationSchemaProperty"]
        """``CfnApplicationOutputV2.OutputProperty.DestinationSchema``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationoutput-output.html#cfn-kinesisanalyticsv2-applicationoutput-output-destinationschema
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationOutputV2Props", jsii_struct_bases=[])
class CfnApplicationOutputV2Props(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::KinesisAnalyticsV2::ApplicationOutput``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html
    """
    applicationName: str
    """``AWS::KinesisAnalyticsV2::ApplicationOutput.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-applicationname
    """

    output: typing.Union[aws_cdk.cdk.Token, "CfnApplicationOutputV2.OutputProperty"]
    """``AWS::KinesisAnalyticsV2::ApplicationOutput.Output``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationoutput.html#cfn-kinesisanalyticsv2-applicationoutput-output
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnApplicationProps(jsii.compat.TypedDict, total=False):
    applicationCode: str
    """``AWS::KinesisAnalytics::Application.ApplicationCode``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationcode
    """
    applicationDescription: str
    """``AWS::KinesisAnalytics::Application.ApplicationDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationdescription
    """
    applicationName: str
    """``AWS::KinesisAnalytics::Application.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-applicationname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationProps", jsii_struct_bases=[_CfnApplicationProps])
class CfnApplicationProps(_CfnApplicationProps):
    """Properties for defining a ``AWS::KinesisAnalytics::Application``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html
    """
    inputs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnApplication.InputProperty", aws_cdk.cdk.Token]]]
    """``AWS::KinesisAnalytics::Application.Inputs``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-application.html#cfn-kinesisanalytics-application-inputs
    """

class CfnApplicationReferenceDataSource(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource"):
    """A CloudFormation ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html
    cloudformationResource:
        AWS::KinesisAnalytics::ApplicationReferenceDataSource
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, reference_data_source: typing.Union[aws_cdk.cdk.Token, "ReferenceDataSourceProperty"]) -> None:
        """Create a new ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ApplicationName``.
            referenceDataSource: ``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ReferenceDataSource``.
        """
        props: CfnApplicationReferenceDataSourceProps = {"applicationName": application_name, "referenceDataSource": reference_data_source}

        jsii.create(CfnApplicationReferenceDataSource, self, [scope, id, props])

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
    @jsii.member(jsii_name="applicationReferenceDataSourceId")
    def application_reference_data_source_id(self) -> str:
        return jsii.get(self, "applicationReferenceDataSourceId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationReferenceDataSourceProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.CSVMappingParametersProperty", jsii_struct_bases=[])
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html
        """
        recordColumnDelimiter: str
        """``CfnApplicationReferenceDataSource.CSVMappingParametersProperty.RecordColumnDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-csvmappingparameters-recordcolumndelimiter
        """

        recordRowDelimiter: str
        """``CfnApplicationReferenceDataSource.CSVMappingParametersProperty.RecordRowDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-csvmappingparameters-recordrowdelimiter
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.JSONMappingParametersProperty", jsii_struct_bases=[])
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters.html
        """
        recordRowPath: str
        """``CfnApplicationReferenceDataSource.JSONMappingParametersProperty.RecordRowPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-jsonmappingparameters-recordrowpath
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.MappingParametersProperty", jsii_struct_bases=[])
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html
        """
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.CSVMappingParametersProperty"]
        """``CfnApplicationReferenceDataSource.MappingParametersProperty.CSVMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-mappingparameters-csvmappingparameters
        """

        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.JSONMappingParametersProperty"]
        """``CfnApplicationReferenceDataSource.MappingParametersProperty.JSONMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalytics-applicationreferencedatasource-mappingparameters-jsonmappingparameters
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str
        """``CfnApplicationReferenceDataSource.RecordColumnProperty.Mapping``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-mapping
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.RecordColumnProperty", jsii_struct_bases=[_RecordColumnProperty])
    class RecordColumnProperty(_RecordColumnProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html
        """
        name: str
        """``CfnApplicationReferenceDataSource.RecordColumnProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-name
        """

        sqlType: str
        """``CfnApplicationReferenceDataSource.RecordColumnProperty.SqlType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalytics-applicationreferencedatasource-recordcolumn-sqltype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.MappingParametersProperty"]
        """``CfnApplicationReferenceDataSource.RecordFormatProperty.MappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html#cfn-kinesisanalytics-applicationreferencedatasource-recordformat-mappingparameters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.RecordFormatProperty", jsii_struct_bases=[_RecordFormatProperty])
    class RecordFormatProperty(_RecordFormatProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html
        """
        recordFormatType: str
        """``CfnApplicationReferenceDataSource.RecordFormatProperty.RecordFormatType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-recordformat.html#cfn-kinesisanalytics-applicationreferencedatasource-recordformat-recordformattype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ReferenceDataSourceProperty(jsii.compat.TypedDict, total=False):
        s3ReferenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty"]
        """``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.S3ReferenceDataSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-s3referencedatasource
        """
        tableName: str
        """``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.TableName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-tablename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.ReferenceDataSourceProperty", jsii_struct_bases=[_ReferenceDataSourceProperty])
    class ReferenceDataSourceProperty(_ReferenceDataSourceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html
        """
        referenceSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.ReferenceSchemaProperty"]
        """``CfnApplicationReferenceDataSource.ReferenceDataSourceProperty.ReferenceSchema``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource-referenceschema
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ReferenceSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str
        """``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordEncoding``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordencoding
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.ReferenceSchemaProperty", jsii_struct_bases=[_ReferenceSchemaProperty])
    class ReferenceSchemaProperty(_ReferenceSchemaProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html
        """
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.RecordColumnProperty"]]]
        """``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordColumns``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordcolumns
        """

        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.RecordFormatProperty"]
        """``CfnApplicationReferenceDataSource.ReferenceSchemaProperty.RecordFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalytics-applicationreferencedatasource-referenceschema-recordformat
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty", jsii_struct_bases=[])
    class S3ReferenceDataSourceProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html
        """
        bucketArn: str
        """``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.BucketARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-bucketarn
        """

        fileKey: str
        """``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.FileKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-filekey
        """

        referenceRoleArn: str
        """``CfnApplicationReferenceDataSource.S3ReferenceDataSourceProperty.ReferenceRoleARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalytics-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-s3referencedatasource-referencerolearn
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceProps", jsii_struct_bases=[])
class CfnApplicationReferenceDataSourceProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::KinesisAnalytics::ApplicationReferenceDataSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html
    """
    applicationName: str
    """``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-applicationname
    """

    referenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSource.ReferenceDataSourceProperty"]
    """``AWS::KinesisAnalytics::ApplicationReferenceDataSource.ReferenceDataSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalytics-applicationreferencedatasource.html#cfn-kinesisanalytics-applicationreferencedatasource-referencedatasource
    """

class CfnApplicationReferenceDataSourceV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2"):
    """A CloudFormation ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html
    cloudformationResource:
        AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, application_name: str, reference_data_source: typing.Union[aws_cdk.cdk.Token, "ReferenceDataSourceProperty"]) -> None:
        """Create a new ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            applicationName: ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ApplicationName``.
            referenceDataSource: ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ReferenceDataSource``.
        """
        props: CfnApplicationReferenceDataSourceV2Props = {"applicationName": application_name, "referenceDataSource": reference_data_source}

        jsii.create(CfnApplicationReferenceDataSourceV2, self, [scope, id, props])

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
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationReferenceDataSourceV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty", jsii_struct_bases=[])
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html
        """
        recordColumnDelimiter: str
        """``CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty.RecordColumnDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters-recordcolumndelimiter
        """

        recordRowDelimiter: str
        """``CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty.RecordRowDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-csvmappingparameters-recordrowdelimiter
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty", jsii_struct_bases=[])
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters.html
        """
        recordRowPath: str
        """``CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty.RecordRowPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-jsonmappingparameters-recordrowpath
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.MappingParametersProperty", jsii_struct_bases=[])
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html
        """
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.CSVMappingParametersProperty"]
        """``CfnApplicationReferenceDataSourceV2.MappingParametersProperty.CSVMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters-csvmappingparameters
        """

        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.JSONMappingParametersProperty"]
        """``CfnApplicationReferenceDataSourceV2.MappingParametersProperty.JSONMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-mappingparameters-jsonmappingparameters
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str
        """``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.Mapping``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-mapping
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.RecordColumnProperty", jsii_struct_bases=[_RecordColumnProperty])
    class RecordColumnProperty(_RecordColumnProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html
        """
        name: str
        """``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-name
        """

        sqlType: str
        """``CfnApplicationReferenceDataSourceV2.RecordColumnProperty.SqlType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordcolumn-sqltype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.MappingParametersProperty"]
        """``CfnApplicationReferenceDataSourceV2.RecordFormatProperty.MappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordformat-mappingparameters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.RecordFormatProperty", jsii_struct_bases=[_RecordFormatProperty])
    class RecordFormatProperty(_RecordFormatProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html
        """
        recordFormatType: str
        """``CfnApplicationReferenceDataSourceV2.RecordFormatProperty.RecordFormatType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-recordformat.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-recordformat-recordformattype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ReferenceDataSourceProperty(jsii.compat.TypedDict, total=False):
        s3ReferenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty"]
        """``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.S3ReferenceDataSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-s3referencedatasource
        """
        tableName: str
        """``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.TableName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-tablename
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty", jsii_struct_bases=[_ReferenceDataSourceProperty])
    class ReferenceDataSourceProperty(_ReferenceDataSourceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html
        """
        referenceSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty"]
        """``CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty.ReferenceSchema``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource-referenceschema
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ReferenceSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str
        """``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordEncoding``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordencoding
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty", jsii_struct_bases=[_ReferenceSchemaProperty])
    class ReferenceSchemaProperty(_ReferenceSchemaProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html
        """
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.RecordColumnProperty"]]]
        """``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordColumns``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordcolumns
        """

        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.RecordFormatProperty"]
        """``CfnApplicationReferenceDataSourceV2.ReferenceSchemaProperty.RecordFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-referenceschema.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referenceschema-recordformat
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty", jsii_struct_bases=[])
    class S3ReferenceDataSourceProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html
        """
        bucketArn: str
        """``CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty.BucketARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource-bucketarn
        """

        fileKey: str
        """``CfnApplicationReferenceDataSourceV2.S3ReferenceDataSourceProperty.FileKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-s3referencedatasource-filekey
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationReferenceDataSourceV2Props", jsii_struct_bases=[])
class CfnApplicationReferenceDataSourceV2Props(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html
    """
    applicationName: str
    """``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-applicationname
    """

    referenceDataSource: typing.Union[aws_cdk.cdk.Token, "CfnApplicationReferenceDataSourceV2.ReferenceDataSourceProperty"]
    """``AWS::KinesisAnalyticsV2::ApplicationReferenceDataSource.ReferenceDataSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-applicationreferencedatasource.html#cfn-kinesisanalyticsv2-applicationreferencedatasource-referencedatasource
    """

class CfnApplicationV2(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2"):
    """A CloudFormation ``AWS::KinesisAnalyticsV2::Application``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html
    cloudformationResource:
        AWS::KinesisAnalyticsV2::Application
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, runtime_environment: str, service_execution_role: str, application_configuration: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ApplicationConfigurationProperty"]]]=None, application_description: typing.Optional[str]=None, application_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::KinesisAnalyticsV2::Application``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            runtimeEnvironment: ``AWS::KinesisAnalyticsV2::Application.RuntimeEnvironment``.
            serviceExecutionRole: ``AWS::KinesisAnalyticsV2::Application.ServiceExecutionRole``.
            applicationConfiguration: ``AWS::KinesisAnalyticsV2::Application.ApplicationConfiguration``.
            applicationDescription: ``AWS::KinesisAnalyticsV2::Application.ApplicationDescription``.
            applicationName: ``AWS::KinesisAnalyticsV2::Application.ApplicationName``.
        """
        props: CfnApplicationV2Props = {"runtimeEnvironment": runtime_environment, "serviceExecutionRole": service_execution_role}

        if application_configuration is not None:
            props["applicationConfiguration"] = application_configuration

        if application_description is not None:
            props["applicationDescription"] = application_description

        if application_name is not None:
            props["applicationName"] = application_name

        jsii.create(CfnApplicationV2, self, [scope, id, props])

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
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnApplicationV2Props":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ApplicationCodeConfigurationProperty", jsii_struct_bases=[])
    class ApplicationCodeConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html
        """
        codeContent: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.CodeContentProperty"]
        """``CfnApplicationV2.ApplicationCodeConfigurationProperty.CodeContent``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html#cfn-kinesisanalyticsv2-application-applicationcodeconfiguration-codecontent
        """

        codeContentType: str
        """``CfnApplicationV2.ApplicationCodeConfigurationProperty.CodeContentType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationcodeconfiguration.html#cfn-kinesisanalyticsv2-application-applicationcodeconfiguration-codecontenttype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ApplicationConfigurationProperty", jsii_struct_bases=[])
    class ApplicationConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html
        """
        applicationCodeConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ApplicationCodeConfigurationProperty"]
        """``CfnApplicationV2.ApplicationConfigurationProperty.ApplicationCodeConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationcodeconfiguration
        """

        applicationSnapshotConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ApplicationSnapshotConfigurationProperty"]
        """``CfnApplicationV2.ApplicationConfigurationProperty.ApplicationSnapshotConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-applicationsnapshotconfiguration
        """

        environmentProperties: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.EnvironmentPropertiesProperty"]
        """``CfnApplicationV2.ApplicationConfigurationProperty.EnvironmentProperties``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-environmentproperties
        """

        flinkApplicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.FlinkApplicationConfigurationProperty"]
        """``CfnApplicationV2.ApplicationConfigurationProperty.FlinkApplicationConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-flinkapplicationconfiguration
        """

        sqlApplicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.SqlApplicationConfigurationProperty"]
        """``CfnApplicationV2.ApplicationConfigurationProperty.SqlApplicationConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationconfiguration.html#cfn-kinesisanalyticsv2-application-applicationconfiguration-sqlapplicationconfiguration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ApplicationSnapshotConfigurationProperty", jsii_struct_bases=[])
    class ApplicationSnapshotConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsnapshotconfiguration.html
        """
        snapshotsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplicationV2.ApplicationSnapshotConfigurationProperty.SnapshotsEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-applicationsnapshotconfiguration.html#cfn-kinesisanalyticsv2-application-applicationsnapshotconfiguration-snapshotsenabled
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.CSVMappingParametersProperty", jsii_struct_bases=[])
    class CSVMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html
        """
        recordColumnDelimiter: str
        """``CfnApplicationV2.CSVMappingParametersProperty.RecordColumnDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html#cfn-kinesisanalyticsv2-application-csvmappingparameters-recordcolumndelimiter
        """

        recordRowDelimiter: str
        """``CfnApplicationV2.CSVMappingParametersProperty.RecordRowDelimiter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-csvmappingparameters.html#cfn-kinesisanalyticsv2-application-csvmappingparameters-recordrowdelimiter
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _CheckpointConfigurationProperty(jsii.compat.TypedDict, total=False):
        checkpointingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplicationV2.CheckpointConfigurationProperty.CheckpointingEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-checkpointingenabled
        """
        checkpointInterval: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplicationV2.CheckpointConfigurationProperty.CheckpointInterval``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-checkpointinterval
        """
        minPauseBetweenCheckpoints: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplicationV2.CheckpointConfigurationProperty.MinPauseBetweenCheckpoints``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-minpausebetweencheckpoints
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.CheckpointConfigurationProperty", jsii_struct_bases=[_CheckpointConfigurationProperty])
    class CheckpointConfigurationProperty(_CheckpointConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html
        """
        configurationType: str
        """``CfnApplicationV2.CheckpointConfigurationProperty.ConfigurationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-checkpointconfiguration.html#cfn-kinesisanalyticsv2-application-checkpointconfiguration-configurationtype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.CodeContentProperty", jsii_struct_bases=[])
    class CodeContentProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html
        """
        s3ContentLocation: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.S3ContentLocationProperty"]
        """``CfnApplicationV2.CodeContentProperty.S3ContentLocation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-s3contentlocation
        """

        textContent: str
        """``CfnApplicationV2.CodeContentProperty.TextContent``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-textcontent
        """

        zipFileContent: str
        """``CfnApplicationV2.CodeContentProperty.ZipFileContent``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-codecontent.html#cfn-kinesisanalyticsv2-application-codecontent-zipfilecontent
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.EnvironmentPropertiesProperty", jsii_struct_bases=[])
    class EnvironmentPropertiesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-environmentproperties.html
        """
        propertyGroups: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.PropertyGroupProperty"]]]
        """``CfnApplicationV2.EnvironmentPropertiesProperty.PropertyGroups``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-environmentproperties.html#cfn-kinesisanalyticsv2-application-environmentproperties-propertygroups
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.FlinkApplicationConfigurationProperty", jsii_struct_bases=[])
    class FlinkApplicationConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html
        """
        checkpointConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.CheckpointConfigurationProperty"]
        """``CfnApplicationV2.FlinkApplicationConfigurationProperty.CheckpointConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-checkpointconfiguration
        """

        monitoringConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.MonitoringConfigurationProperty"]
        """``CfnApplicationV2.FlinkApplicationConfigurationProperty.MonitoringConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-monitoringconfiguration
        """

        parallelismConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ParallelismConfigurationProperty"]
        """``CfnApplicationV2.FlinkApplicationConfigurationProperty.ParallelismConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-flinkapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-flinkapplicationconfiguration-parallelismconfiguration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputLambdaProcessorProperty", jsii_struct_bases=[])
    class InputLambdaProcessorProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputlambdaprocessor.html
        """
        resourceArn: str
        """``CfnApplicationV2.InputLambdaProcessorProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputlambdaprocessor.html#cfn-kinesisanalyticsv2-application-inputlambdaprocessor-resourcearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputParallelismProperty", jsii_struct_bases=[])
    class InputParallelismProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputparallelism.html
        """
        count: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplicationV2.InputParallelismProperty.Count``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputparallelism.html#cfn-kinesisanalyticsv2-application-inputparallelism-count
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputProcessingConfigurationProperty", jsii_struct_bases=[])
    class InputProcessingConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputprocessingconfiguration.html
        """
        inputLambdaProcessor: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputLambdaProcessorProperty"]
        """``CfnApplicationV2.InputProcessingConfigurationProperty.InputLambdaProcessor``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputprocessingconfiguration.html#cfn-kinesisanalyticsv2-application-inputprocessingconfiguration-inputlambdaprocessor
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _InputProperty(jsii.compat.TypedDict, total=False):
        inputParallelism: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputParallelismProperty"]
        """``CfnApplicationV2.InputProperty.InputParallelism``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputparallelism
        """
        inputProcessingConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputProcessingConfigurationProperty"]
        """``CfnApplicationV2.InputProperty.InputProcessingConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputprocessingconfiguration
        """
        kinesisFirehoseInput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.KinesisFirehoseInputProperty"]
        """``CfnApplicationV2.InputProperty.KinesisFirehoseInput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-kinesisfirehoseinput
        """
        kinesisStreamsInput: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.KinesisStreamsInputProperty"]
        """``CfnApplicationV2.InputProperty.KinesisStreamsInput``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-kinesisstreamsinput
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputProperty", jsii_struct_bases=[_InputProperty])
    class InputProperty(_InputProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html
        """
        inputSchema: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputSchemaProperty"]
        """``CfnApplicationV2.InputProperty.InputSchema``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-inputschema
        """

        namePrefix: str
        """``CfnApplicationV2.InputProperty.NamePrefix``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-input.html#cfn-kinesisanalyticsv2-application-input-nameprefix
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _InputSchemaProperty(jsii.compat.TypedDict, total=False):
        recordEncoding: str
        """``CfnApplicationV2.InputSchemaProperty.RecordEncoding``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordencoding
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.InputSchemaProperty", jsii_struct_bases=[_InputSchemaProperty])
    class InputSchemaProperty(_InputSchemaProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html
        """
        recordColumns: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.RecordColumnProperty"]]]
        """``CfnApplicationV2.InputSchemaProperty.RecordColumns``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordcolumns
        """

        recordFormat: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.RecordFormatProperty"]
        """``CfnApplicationV2.InputSchemaProperty.RecordFormat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-inputschema.html#cfn-kinesisanalyticsv2-application-inputschema-recordformat
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.JSONMappingParametersProperty", jsii_struct_bases=[])
    class JSONMappingParametersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-jsonmappingparameters.html
        """
        recordRowPath: str
        """``CfnApplicationV2.JSONMappingParametersProperty.RecordRowPath``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-jsonmappingparameters.html#cfn-kinesisanalyticsv2-application-jsonmappingparameters-recordrowpath
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.KinesisFirehoseInputProperty", jsii_struct_bases=[])
    class KinesisFirehoseInputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisfirehoseinput.html
        """
        resourceArn: str
        """``CfnApplicationV2.KinesisFirehoseInputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisfirehoseinput.html#cfn-kinesisanalyticsv2-application-kinesisfirehoseinput-resourcearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.KinesisStreamsInputProperty", jsii_struct_bases=[])
    class KinesisStreamsInputProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisstreamsinput.html
        """
        resourceArn: str
        """``CfnApplicationV2.KinesisStreamsInputProperty.ResourceARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-kinesisstreamsinput.html#cfn-kinesisanalyticsv2-application-kinesisstreamsinput-resourcearn
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.MappingParametersProperty", jsii_struct_bases=[])
    class MappingParametersProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html
        """
        csvMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.CSVMappingParametersProperty"]
        """``CfnApplicationV2.MappingParametersProperty.CSVMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html#cfn-kinesisanalyticsv2-application-mappingparameters-csvmappingparameters
        """

        jsonMappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.JSONMappingParametersProperty"]
        """``CfnApplicationV2.MappingParametersProperty.JSONMappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-mappingparameters.html#cfn-kinesisanalyticsv2-application-mappingparameters-jsonmappingparameters
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _MonitoringConfigurationProperty(jsii.compat.TypedDict, total=False):
        logLevel: str
        """``CfnApplicationV2.MonitoringConfigurationProperty.LogLevel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-loglevel
        """
        metricsLevel: str
        """``CfnApplicationV2.MonitoringConfigurationProperty.MetricsLevel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-metricslevel
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.MonitoringConfigurationProperty", jsii_struct_bases=[_MonitoringConfigurationProperty])
    class MonitoringConfigurationProperty(_MonitoringConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html
        """
        configurationType: str
        """``CfnApplicationV2.MonitoringConfigurationProperty.ConfigurationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-monitoringconfiguration.html#cfn-kinesisanalyticsv2-application-monitoringconfiguration-configurationtype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ParallelismConfigurationProperty(jsii.compat.TypedDict, total=False):
        autoScalingEnabled: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnApplicationV2.ParallelismConfigurationProperty.AutoScalingEnabled``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-autoscalingenabled
        """
        parallelism: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplicationV2.ParallelismConfigurationProperty.Parallelism``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-parallelism
        """
        parallelismPerKpu: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnApplicationV2.ParallelismConfigurationProperty.ParallelismPerKPU``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-parallelismperkpu
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.ParallelismConfigurationProperty", jsii_struct_bases=[_ParallelismConfigurationProperty])
    class ParallelismConfigurationProperty(_ParallelismConfigurationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html
        """
        configurationType: str
        """``CfnApplicationV2.ParallelismConfigurationProperty.ConfigurationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-parallelismconfiguration.html#cfn-kinesisanalyticsv2-application-parallelismconfiguration-configurationtype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.PropertyGroupProperty", jsii_struct_bases=[])
    class PropertyGroupProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html
        """
        propertyGroupId: str
        """``CfnApplicationV2.PropertyGroupProperty.PropertyGroupId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html#cfn-kinesisanalyticsv2-application-propertygroup-propertygroupid
        """

        propertyMap: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        """``CfnApplicationV2.PropertyGroupProperty.PropertyMap``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-propertygroup.html#cfn-kinesisanalyticsv2-application-propertygroup-propertymap
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordColumnProperty(jsii.compat.TypedDict, total=False):
        mapping: str
        """``CfnApplicationV2.RecordColumnProperty.Mapping``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-mapping
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.RecordColumnProperty", jsii_struct_bases=[_RecordColumnProperty])
    class RecordColumnProperty(_RecordColumnProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html
        """
        name: str
        """``CfnApplicationV2.RecordColumnProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-name
        """

        sqlType: str
        """``CfnApplicationV2.RecordColumnProperty.SqlType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordcolumn.html#cfn-kinesisanalyticsv2-application-recordcolumn-sqltype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _RecordFormatProperty(jsii.compat.TypedDict, total=False):
        mappingParameters: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.MappingParametersProperty"]
        """``CfnApplicationV2.RecordFormatProperty.MappingParameters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html#cfn-kinesisanalyticsv2-application-recordformat-mappingparameters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.RecordFormatProperty", jsii_struct_bases=[_RecordFormatProperty])
    class RecordFormatProperty(_RecordFormatProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html
        """
        recordFormatType: str
        """``CfnApplicationV2.RecordFormatProperty.RecordFormatType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-recordformat.html#cfn-kinesisanalyticsv2-application-recordformat-recordformattype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.S3ContentLocationProperty", jsii_struct_bases=[])
    class S3ContentLocationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html
        """
        bucketArn: str
        """``CfnApplicationV2.S3ContentLocationProperty.BucketARN``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-bucketarn
        """

        fileKey: str
        """``CfnApplicationV2.S3ContentLocationProperty.FileKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-filekey
        """

        objectVersion: str
        """``CfnApplicationV2.S3ContentLocationProperty.ObjectVersion``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-s3contentlocation.html#cfn-kinesisanalyticsv2-application-s3contentlocation-objectversion
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2.SqlApplicationConfigurationProperty", jsii_struct_bases=[])
    class SqlApplicationConfigurationProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-sqlapplicationconfiguration.html
        """
        inputs: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.InputProperty"]]]
        """``CfnApplicationV2.SqlApplicationConfigurationProperty.Inputs``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-kinesisanalyticsv2-application-sqlapplicationconfiguration.html#cfn-kinesisanalyticsv2-application-sqlapplicationconfiguration-inputs
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnApplicationV2Props(jsii.compat.TypedDict, total=False):
    applicationConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnApplicationV2.ApplicationConfigurationProperty"]
    """``AWS::KinesisAnalyticsV2::Application.ApplicationConfiguration``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationconfiguration
    """
    applicationDescription: str
    """``AWS::KinesisAnalyticsV2::Application.ApplicationDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationdescription
    """
    applicationName: str
    """``AWS::KinesisAnalyticsV2::Application.ApplicationName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-applicationname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-kinesisanalytics.CfnApplicationV2Props", jsii_struct_bases=[_CfnApplicationV2Props])
class CfnApplicationV2Props(_CfnApplicationV2Props):
    """Properties for defining a ``AWS::KinesisAnalyticsV2::Application``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html
    """
    runtimeEnvironment: str
    """``AWS::KinesisAnalyticsV2::Application.RuntimeEnvironment``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-runtimeenvironment
    """

    serviceExecutionRole: str
    """``AWS::KinesisAnalyticsV2::Application.ServiceExecutionRole``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-kinesisanalyticsv2-application.html#cfn-kinesisanalyticsv2-application-serviceexecutionrole
    """

__all__ = ["CfnApplication", "CfnApplicationCloudWatchLoggingOptionV2", "CfnApplicationCloudWatchLoggingOptionV2Props", "CfnApplicationOutput", "CfnApplicationOutputProps", "CfnApplicationOutputV2", "CfnApplicationOutputV2Props", "CfnApplicationProps", "CfnApplicationReferenceDataSource", "CfnApplicationReferenceDataSourceProps", "CfnApplicationReferenceDataSourceV2", "CfnApplicationReferenceDataSourceV2Props", "CfnApplicationV2", "CfnApplicationV2Props", "__jsii_assembly__"]

publication.publish()
