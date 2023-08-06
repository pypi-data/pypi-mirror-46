import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-iotanalytics", "0.32.0", __name__, "aws-iotanalytics@0.32.0.jsii.tgz")
class CfnChannel(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnChannel"):
    """A CloudFormation ``AWS::IoTAnalytics::Channel``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html
    cloudformationResource:
        AWS::IoTAnalytics::Channel
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, channel_name: typing.Optional[str]=None, retention_period: typing.Optional[typing.Union[typing.Optional["RetentionPeriodProperty"], typing.Optional[aws_cdk.cdk.Token]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::IoTAnalytics::Channel``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            channelName: ``AWS::IoTAnalytics::Channel.ChannelName``.
            retentionPeriod: ``AWS::IoTAnalytics::Channel.RetentionPeriod``.
            tags: ``AWS::IoTAnalytics::Channel.Tags``.
        """
        props: CfnChannelProps = {}

        if channel_name is not None:
            props["channelName"] = channel_name

        if retention_period is not None:
            props["retentionPeriod"] = retention_period

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnChannel, self, [scope, id, props])

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
    @jsii.member(jsii_name="channelId")
    def channel_id(self) -> str:
        return jsii.get(self, "channelId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnChannelProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnChannel.RetentionPeriodProperty", jsii_struct_bases=[])
    class RetentionPeriodProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html
        """
        numberOfDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnChannel.RetentionPeriodProperty.NumberOfDays``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html#cfn-iotanalytics-channel-retentionperiod-numberofdays
        """

        unlimited: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnChannel.RetentionPeriodProperty.Unlimited``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-channel-retentionperiod.html#cfn-iotanalytics-channel-retentionperiod-unlimited
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnChannelProps", jsii_struct_bases=[])
class CfnChannelProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::IoTAnalytics::Channel``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html
    """
    channelName: str
    """``AWS::IoTAnalytics::Channel.ChannelName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-channelname
    """

    retentionPeriod: typing.Union["CfnChannel.RetentionPeriodProperty", aws_cdk.cdk.Token]
    """``AWS::IoTAnalytics::Channel.RetentionPeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-retentionperiod
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::IoTAnalytics::Channel.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-channel.html#cfn-iotanalytics-channel-tags
    """

class CfnDataset(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset"):
    """A CloudFormation ``AWS::IoTAnalytics::Dataset``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html
    cloudformationResource:
        AWS::IoTAnalytics::Dataset
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActionProperty"]]], dataset_name: typing.Optional[str]=None, retention_period: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["RetentionPeriodProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None, triggers: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "TriggerProperty"]]]]]=None) -> None:
        """Create a new ``AWS::IoTAnalytics::Dataset``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            actions: ``AWS::IoTAnalytics::Dataset.Actions``.
            datasetName: ``AWS::IoTAnalytics::Dataset.DatasetName``.
            retentionPeriod: ``AWS::IoTAnalytics::Dataset.RetentionPeriod``.
            tags: ``AWS::IoTAnalytics::Dataset.Tags``.
            triggers: ``AWS::IoTAnalytics::Dataset.Triggers``.
        """
        props: CfnDatasetProps = {"actions": actions}

        if dataset_name is not None:
            props["datasetName"] = dataset_name

        if retention_period is not None:
            props["retentionPeriod"] = retention_period

        if tags is not None:
            props["tags"] = tags

        if triggers is not None:
            props["triggers"] = triggers

        jsii.create(CfnDataset, self, [scope, id, props])

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
    @jsii.member(jsii_name="datasetId")
    def dataset_id(self) -> str:
        return jsii.get(self, "datasetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDatasetProps":
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
    class _ActionProperty(jsii.compat.TypedDict, total=False):
        containerAction: typing.Union[aws_cdk.cdk.Token, "CfnDataset.ContainerActionProperty"]
        """``CfnDataset.ActionProperty.ContainerAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-containeraction
        """
        queryAction: typing.Union[aws_cdk.cdk.Token, "CfnDataset.QueryActionProperty"]
        """``CfnDataset.ActionProperty.QueryAction``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-queryaction
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ActionProperty", jsii_struct_bases=[_ActionProperty])
    class ActionProperty(_ActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html
        """
        actionName: str
        """``CfnDataset.ActionProperty.ActionName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-action.html#cfn-iotanalytics-dataset-action-actionname
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ContainerActionProperty(jsii.compat.TypedDict, total=False):
        variables: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.VariableProperty"]]]
        """``CfnDataset.ContainerActionProperty.Variables``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-variables
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ContainerActionProperty", jsii_struct_bases=[_ContainerActionProperty])
    class ContainerActionProperty(_ContainerActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html
        """
        executionRoleArn: str
        """``CfnDataset.ContainerActionProperty.ExecutionRoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-executionrolearn
        """

        image: str
        """``CfnDataset.ContainerActionProperty.Image``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-image
        """

        resourceConfiguration: typing.Union[aws_cdk.cdk.Token, "CfnDataset.ResourceConfigurationProperty"]
        """``CfnDataset.ContainerActionProperty.ResourceConfiguration``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-containeraction.html#cfn-iotanalytics-dataset-containeraction-resourceconfiguration
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.DatasetContentVersionValueProperty", jsii_struct_bases=[])
    class DatasetContentVersionValueProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-datasetcontentversionvalue.html
        """
        datasetName: str
        """``CfnDataset.DatasetContentVersionValueProperty.DatasetName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-datasetcontentversionvalue.html#cfn-iotanalytics-dataset-variable-datasetcontentversionvalue-datasetname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.DeltaTimeProperty", jsii_struct_bases=[])
    class DeltaTimeProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html
        """
        offsetSeconds: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDataset.DeltaTimeProperty.OffsetSeconds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html#cfn-iotanalytics-dataset-deltatime-offsetseconds
        """

        timeExpression: str
        """``CfnDataset.DeltaTimeProperty.TimeExpression``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-deltatime.html#cfn-iotanalytics-dataset-deltatime-timeexpression
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.FilterProperty", jsii_struct_bases=[])
    class FilterProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-filter.html
        """
        deltaTime: typing.Union[aws_cdk.cdk.Token, "CfnDataset.DeltaTimeProperty"]
        """``CfnDataset.FilterProperty.DeltaTime``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-filter.html#cfn-iotanalytics-dataset-filter-deltatime
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.OutputFileUriValueProperty", jsii_struct_bases=[])
    class OutputFileUriValueProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-outputfileurivalue.html
        """
        fileName: str
        """``CfnDataset.OutputFileUriValueProperty.FileName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable-outputfileurivalue.html#cfn-iotanalytics-dataset-variable-outputfileurivalue-filename
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _QueryActionProperty(jsii.compat.TypedDict, total=False):
        filters: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.FilterProperty"]]]
        """``CfnDataset.QueryActionProperty.Filters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html#cfn-iotanalytics-dataset-queryaction-filters
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.QueryActionProperty", jsii_struct_bases=[_QueryActionProperty])
    class QueryActionProperty(_QueryActionProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html
        """
        sqlQuery: str
        """``CfnDataset.QueryActionProperty.SqlQuery``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-queryaction.html#cfn-iotanalytics-dataset-queryaction-sqlquery
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ResourceConfigurationProperty", jsii_struct_bases=[])
    class ResourceConfigurationProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html
        """
        computeType: str
        """``CfnDataset.ResourceConfigurationProperty.ComputeType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html#cfn-iotanalytics-dataset-resourceconfiguration-computetype
        """

        volumeSizeInGb: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDataset.ResourceConfigurationProperty.VolumeSizeInGB``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-resourceconfiguration.html#cfn-iotanalytics-dataset-resourceconfiguration-volumesizeingb
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.RetentionPeriodProperty", jsii_struct_bases=[])
    class RetentionPeriodProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html
        """
        numberOfDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDataset.RetentionPeriodProperty.NumberOfDays``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html#cfn-iotanalytics-dataset-retentionperiod-numberofdays
        """

        unlimited: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDataset.RetentionPeriodProperty.Unlimited``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-retentionperiod.html#cfn-iotanalytics-dataset-retentionperiod-unlimited
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.ScheduleProperty", jsii_struct_bases=[])
    class ScheduleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger-schedule.html
        """
        scheduleExpression: str
        """``CfnDataset.ScheduleProperty.ScheduleExpression``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger-schedule.html#cfn-iotanalytics-dataset-trigger-schedule-scheduleexpression
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.TriggerProperty", jsii_struct_bases=[])
    class TriggerProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html
        """
        schedule: typing.Union[aws_cdk.cdk.Token, "CfnDataset.ScheduleProperty"]
        """``CfnDataset.TriggerProperty.Schedule``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html#cfn-iotanalytics-dataset-trigger-schedule
        """

        triggeringDataset: typing.Union[aws_cdk.cdk.Token, "CfnDataset.TriggeringDatasetProperty"]
        """``CfnDataset.TriggerProperty.TriggeringDataset``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-trigger.html#cfn-iotanalytics-dataset-trigger-triggeringdataset
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.TriggeringDatasetProperty", jsii_struct_bases=[])
    class TriggeringDatasetProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-triggeringdataset.html
        """
        datasetName: str
        """``CfnDataset.TriggeringDatasetProperty.DatasetName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-triggeringdataset.html#cfn-iotanalytics-dataset-triggeringdataset-datasetname
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _VariableProperty(jsii.compat.TypedDict, total=False):
        datasetContentVersionValue: typing.Union[aws_cdk.cdk.Token, "CfnDataset.DatasetContentVersionValueProperty"]
        """``CfnDataset.VariableProperty.DatasetContentVersionValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-datasetcontentversionvalue
        """
        doubleValue: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDataset.VariableProperty.DoubleValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-doublevalue
        """
        outputFileUriValue: typing.Union[aws_cdk.cdk.Token, "CfnDataset.OutputFileUriValueProperty"]
        """``CfnDataset.VariableProperty.OutputFileUriValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-outputfileurivalue
        """
        stringValue: str
        """``CfnDataset.VariableProperty.StringValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-stringvalue
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDataset.VariableProperty", jsii_struct_bases=[_VariableProperty])
    class VariableProperty(_VariableProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html
        """
        variableName: str
        """``CfnDataset.VariableProperty.VariableName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-dataset-variable.html#cfn-iotanalytics-dataset-variable-variablename
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDatasetProps(jsii.compat.TypedDict, total=False):
    datasetName: str
    """``AWS::IoTAnalytics::Dataset.DatasetName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-datasetname
    """
    retentionPeriod: typing.Union[aws_cdk.cdk.Token, "CfnDataset.RetentionPeriodProperty"]
    """``AWS::IoTAnalytics::Dataset.RetentionPeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-retentionperiod
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::IoTAnalytics::Dataset.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-tags
    """
    triggers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.TriggerProperty"]]]
    """``AWS::IoTAnalytics::Dataset.Triggers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-triggers
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDatasetProps", jsii_struct_bases=[_CfnDatasetProps])
class CfnDatasetProps(_CfnDatasetProps):
    """Properties for defining a ``AWS::IoTAnalytics::Dataset``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html
    """
    actions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnDataset.ActionProperty"]]]
    """``AWS::IoTAnalytics::Dataset.Actions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-dataset.html#cfn-iotanalytics-dataset-actions
    """

class CfnDatastore(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnDatastore"):
    """A CloudFormation ``AWS::IoTAnalytics::Datastore``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html
    cloudformationResource:
        AWS::IoTAnalytics::Datastore
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, datastore_name: typing.Optional[str]=None, retention_period: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["RetentionPeriodProperty"]]]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::IoTAnalytics::Datastore``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            datastoreName: ``AWS::IoTAnalytics::Datastore.DatastoreName``.
            retentionPeriod: ``AWS::IoTAnalytics::Datastore.RetentionPeriod``.
            tags: ``AWS::IoTAnalytics::Datastore.Tags``.
        """
        props: CfnDatastoreProps = {}

        if datastore_name is not None:
            props["datastoreName"] = datastore_name

        if retention_period is not None:
            props["retentionPeriod"] = retention_period

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnDatastore, self, [scope, id, props])

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
    @jsii.member(jsii_name="datastoreId")
    def datastore_id(self) -> str:
        return jsii.get(self, "datastoreId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDatastoreProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDatastore.RetentionPeriodProperty", jsii_struct_bases=[])
    class RetentionPeriodProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html
        """
        numberOfDays: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnDatastore.RetentionPeriodProperty.NumberOfDays``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html#cfn-iotanalytics-datastore-retentionperiod-numberofdays
        """

        unlimited: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnDatastore.RetentionPeriodProperty.Unlimited``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-datastore-retentionperiod.html#cfn-iotanalytics-datastore-retentionperiod-unlimited
        """


@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnDatastoreProps", jsii_struct_bases=[])
class CfnDatastoreProps(jsii.compat.TypedDict, total=False):
    """Properties for defining a ``AWS::IoTAnalytics::Datastore``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html
    """
    datastoreName: str
    """``AWS::IoTAnalytics::Datastore.DatastoreName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-datastorename
    """

    retentionPeriod: typing.Union[aws_cdk.cdk.Token, "CfnDatastore.RetentionPeriodProperty"]
    """``AWS::IoTAnalytics::Datastore.RetentionPeriod``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-retentionperiod
    """

    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::IoTAnalytics::Datastore.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-datastore.html#cfn-iotanalytics-datastore-tags
    """

class CfnPipeline(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline"):
    """A CloudFormation ``AWS::IoTAnalytics::Pipeline``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html
    cloudformationResource:
        AWS::IoTAnalytics::Pipeline
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, pipeline_activities: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "ActivityProperty"]]], pipeline_name: typing.Optional[str]=None, tags: typing.Optional[typing.List[aws_cdk.cdk.CfnTag]]=None) -> None:
        """Create a new ``AWS::IoTAnalytics::Pipeline``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            pipelineActivities: ``AWS::IoTAnalytics::Pipeline.PipelineActivities``.
            pipelineName: ``AWS::IoTAnalytics::Pipeline.PipelineName``.
            tags: ``AWS::IoTAnalytics::Pipeline.Tags``.
        """
        props: CfnPipelineProps = {"pipelineActivities": pipeline_activities}

        if pipeline_name is not None:
            props["pipelineName"] = pipeline_name

        if tags is not None:
            props["tags"] = tags

        jsii.create(CfnPipeline, self, [scope, id, props])

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
    @jsii.member(jsii_name="pipelineId")
    def pipeline_id(self) -> str:
        return jsii.get(self, "pipelineId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnPipelineProps":
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

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.ActivityProperty", jsii_struct_bases=[])
    class ActivityProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html
        """
        addAttributes: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.AddAttributesProperty"]
        """``CfnPipeline.ActivityProperty.AddAttributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-addattributes
        """

        channel: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ChannelProperty"]
        """``CfnPipeline.ActivityProperty.Channel``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-channel
        """

        datastore: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.DatastoreProperty"]
        """``CfnPipeline.ActivityProperty.Datastore``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-datastore
        """

        deviceRegistryEnrich: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.DeviceRegistryEnrichProperty"]
        """``CfnPipeline.ActivityProperty.DeviceRegistryEnrich``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-deviceregistryenrich
        """

        deviceShadowEnrich: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.DeviceShadowEnrichProperty"]
        """``CfnPipeline.ActivityProperty.DeviceShadowEnrich``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-deviceshadowenrich
        """

        filter: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.FilterProperty"]
        """``CfnPipeline.ActivityProperty.Filter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-filter
        """

        lambda_: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.LambdaProperty"]
        """``CfnPipeline.ActivityProperty.Lambda``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-lambda
        """

        math: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.MathProperty"]
        """``CfnPipeline.ActivityProperty.Math``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-math
        """

        removeAttributes: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.RemoveAttributesProperty"]
        """``CfnPipeline.ActivityProperty.RemoveAttributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-removeattributes
        """

        selectAttributes: typing.Union[aws_cdk.cdk.Token, "CfnPipeline.SelectAttributesProperty"]
        """``CfnPipeline.ActivityProperty.SelectAttributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-activity.html#cfn-iotanalytics-pipeline-activity-selectattributes
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.AddAttributesProperty", jsii_struct_bases=[])
    class AddAttributesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html
        """
        attributes: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        """``CfnPipeline.AddAttributesProperty.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-attributes
        """

        name: str
        """``CfnPipeline.AddAttributesProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-name
        """

        next: str
        """``CfnPipeline.AddAttributesProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-addattributes.html#cfn-iotanalytics-pipeline-addattributes-next
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.ChannelProperty", jsii_struct_bases=[])
    class ChannelProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html
        """
        channelName: str
        """``CfnPipeline.ChannelProperty.ChannelName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-channelname
        """

        name: str
        """``CfnPipeline.ChannelProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-name
        """

        next: str
        """``CfnPipeline.ChannelProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-channel.html#cfn-iotanalytics-pipeline-channel-next
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.DatastoreProperty", jsii_struct_bases=[])
    class DatastoreProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html
        """
        datastoreName: str
        """``CfnPipeline.DatastoreProperty.DatastoreName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html#cfn-iotanalytics-pipeline-datastore-datastorename
        """

        name: str
        """``CfnPipeline.DatastoreProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-datastore.html#cfn-iotanalytics-pipeline-datastore-name
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.DeviceRegistryEnrichProperty", jsii_struct_bases=[])
    class DeviceRegistryEnrichProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html
        """
        attribute: str
        """``CfnPipeline.DeviceRegistryEnrichProperty.Attribute``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-attribute
        """

        name: str
        """``CfnPipeline.DeviceRegistryEnrichProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-name
        """

        next: str
        """``CfnPipeline.DeviceRegistryEnrichProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-next
        """

        roleArn: str
        """``CfnPipeline.DeviceRegistryEnrichProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-rolearn
        """

        thingName: str
        """``CfnPipeline.DeviceRegistryEnrichProperty.ThingName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceregistryenrich.html#cfn-iotanalytics-pipeline-deviceregistryenrich-thingname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.DeviceShadowEnrichProperty", jsii_struct_bases=[])
    class DeviceShadowEnrichProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html
        """
        attribute: str
        """``CfnPipeline.DeviceShadowEnrichProperty.Attribute``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-attribute
        """

        name: str
        """``CfnPipeline.DeviceShadowEnrichProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-name
        """

        next: str
        """``CfnPipeline.DeviceShadowEnrichProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-next
        """

        roleArn: str
        """``CfnPipeline.DeviceShadowEnrichProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-rolearn
        """

        thingName: str
        """``CfnPipeline.DeviceShadowEnrichProperty.ThingName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-deviceshadowenrich.html#cfn-iotanalytics-pipeline-deviceshadowenrich-thingname
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.FilterProperty", jsii_struct_bases=[])
    class FilterProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html
        """
        filter: str
        """``CfnPipeline.FilterProperty.Filter``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-filter
        """

        name: str
        """``CfnPipeline.FilterProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-name
        """

        next: str
        """``CfnPipeline.FilterProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-filter.html#cfn-iotanalytics-pipeline-filter-next
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.LambdaProperty", jsii_struct_bases=[])
    class LambdaProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html
        """
        batchSize: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnPipeline.LambdaProperty.BatchSize``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-batchsize
        """

        lambdaName: str
        """``CfnPipeline.LambdaProperty.LambdaName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-lambdaname
        """

        name: str
        """``CfnPipeline.LambdaProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-name
        """

        next: str
        """``CfnPipeline.LambdaProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-lambda.html#cfn-iotanalytics-pipeline-lambda-next
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.MathProperty", jsii_struct_bases=[])
    class MathProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html
        """
        attribute: str
        """``CfnPipeline.MathProperty.Attribute``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-attribute
        """

        math: str
        """``CfnPipeline.MathProperty.Math``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-math
        """

        name: str
        """``CfnPipeline.MathProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-name
        """

        next: str
        """``CfnPipeline.MathProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-math.html#cfn-iotanalytics-pipeline-math-next
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.RemoveAttributesProperty", jsii_struct_bases=[])
    class RemoveAttributesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html
        """
        attributes: typing.List[str]
        """``CfnPipeline.RemoveAttributesProperty.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-attributes
        """

        name: str
        """``CfnPipeline.RemoveAttributesProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-name
        """

        next: str
        """``CfnPipeline.RemoveAttributesProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-removeattributes.html#cfn-iotanalytics-pipeline-removeattributes-next
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipeline.SelectAttributesProperty", jsii_struct_bases=[])
    class SelectAttributesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html
        """
        attributes: typing.List[str]
        """``CfnPipeline.SelectAttributesProperty.Attributes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-attributes
        """

        name: str
        """``CfnPipeline.SelectAttributesProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-name
        """

        next: str
        """``CfnPipeline.SelectAttributesProperty.Next``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iotanalytics-pipeline-selectattributes.html#cfn-iotanalytics-pipeline-selectattributes-next
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnPipelineProps(jsii.compat.TypedDict, total=False):
    pipelineName: str
    """``AWS::IoTAnalytics::Pipeline.PipelineName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelinename
    """
    tags: typing.List[aws_cdk.cdk.CfnTag]
    """``AWS::IoTAnalytics::Pipeline.Tags``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-tags
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-iotanalytics.CfnPipelineProps", jsii_struct_bases=[_CfnPipelineProps])
class CfnPipelineProps(_CfnPipelineProps):
    """Properties for defining a ``AWS::IoTAnalytics::Pipeline``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html
    """
    pipelineActivities: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnPipeline.ActivityProperty"]]]
    """``AWS::IoTAnalytics::Pipeline.PipelineActivities``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iotanalytics-pipeline.html#cfn-iotanalytics-pipeline-pipelineactivities
    """

__all__ = ["CfnChannel", "CfnChannelProps", "CfnDataset", "CfnDatasetProps", "CfnDatastore", "CfnDatastoreProps", "CfnPipeline", "CfnPipelineProps", "__jsii_assembly__"]

publication.publish()
