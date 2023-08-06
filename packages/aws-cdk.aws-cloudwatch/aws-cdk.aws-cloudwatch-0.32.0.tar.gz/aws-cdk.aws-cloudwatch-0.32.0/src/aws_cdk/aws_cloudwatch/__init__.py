import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.aws_iam
import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-cloudwatch", "0.32.0", __name__, "aws-cloudwatch@0.32.0.jsii.tgz")
@jsii.data_type_optionals(jsii_struct_bases=[])
class _AlarmMetricJson(jsii.compat.TypedDict, total=False):
    dimensions: typing.List["Dimension"]
    """The dimensions to apply to the alarm."""
    extendedStatistic: str
    """Percentile aggregation function to use."""
    statistic: "Statistic"
    """Simple aggregation function to use."""
    unit: "Unit"
    """The unit of the alarm."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmMetricJson", jsii_struct_bases=[_AlarmMetricJson])
class AlarmMetricJson(_AlarmMetricJson):
    """Properties used to construct the Metric identifying part of an Alarm."""
    metricName: str
    """Name of the metric."""

    namespace: str
    """Namespace of the metric."""

    period: jsii.Number
    """How many seconds to aggregate over."""

class CfnAlarm(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm"):
    """A CloudFormation ``AWS::CloudWatch::Alarm``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
    cloudformationResource:
        AWS::CloudWatch::Alarm
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, comparison_operator: str, evaluation_periods: typing.Union[jsii.Number, aws_cdk.cdk.Token], threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token], actions_enabled: typing.Optional[typing.Union[typing.Optional[bool], typing.Optional[aws_cdk.cdk.Token]]]=None, alarm_actions: typing.Optional[typing.List[str]]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, datapoints_to_alarm: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, dimensions: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "DimensionProperty"]]]]]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, extended_statistic: typing.Optional[str]=None, insufficient_data_actions: typing.Optional[typing.List[str]]=None, metric_name: typing.Optional[str]=None, metrics: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "MetricDataQueryProperty"]]]]]=None, namespace: typing.Optional[str]=None, ok_actions: typing.Optional[typing.List[str]]=None, period: typing.Optional[typing.Union[typing.Optional[jsii.Number], typing.Optional[aws_cdk.cdk.Token]]]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional[str]=None, unit: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudWatch::Alarm``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            comparisonOperator: ``AWS::CloudWatch::Alarm.ComparisonOperator``.
            evaluationPeriods: ``AWS::CloudWatch::Alarm.EvaluationPeriods``.
            threshold: ``AWS::CloudWatch::Alarm.Threshold``.
            actionsEnabled: ``AWS::CloudWatch::Alarm.ActionsEnabled``.
            alarmActions: ``AWS::CloudWatch::Alarm.AlarmActions``.
            alarmDescription: ``AWS::CloudWatch::Alarm.AlarmDescription``.
            alarmName: ``AWS::CloudWatch::Alarm.AlarmName``.
            datapointsToAlarm: ``AWS::CloudWatch::Alarm.DatapointsToAlarm``.
            dimensions: ``AWS::CloudWatch::Alarm.Dimensions``.
            evaluateLowSampleCountPercentile: ``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.
            extendedStatistic: ``AWS::CloudWatch::Alarm.ExtendedStatistic``.
            insufficientDataActions: ``AWS::CloudWatch::Alarm.InsufficientDataActions``.
            metricName: ``AWS::CloudWatch::Alarm.MetricName``.
            metrics: ``AWS::CloudWatch::Alarm.Metrics``.
            namespace: ``AWS::CloudWatch::Alarm.Namespace``.
            okActions: ``AWS::CloudWatch::Alarm.OKActions``.
            period: ``AWS::CloudWatch::Alarm.Period``.
            statistic: ``AWS::CloudWatch::Alarm.Statistic``.
            treatMissingData: ``AWS::CloudWatch::Alarm.TreatMissingData``.
            unit: ``AWS::CloudWatch::Alarm.Unit``.
        """
        props: CfnAlarmProps = {"comparisonOperator": comparison_operator, "evaluationPeriods": evaluation_periods, "threshold": threshold}

        if actions_enabled is not None:
            props["actionsEnabled"] = actions_enabled

        if alarm_actions is not None:
            props["alarmActions"] = alarm_actions

        if alarm_description is not None:
            props["alarmDescription"] = alarm_description

        if alarm_name is not None:
            props["alarmName"] = alarm_name

        if datapoints_to_alarm is not None:
            props["datapointsToAlarm"] = datapoints_to_alarm

        if dimensions is not None:
            props["dimensions"] = dimensions

        if evaluate_low_sample_count_percentile is not None:
            props["evaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile

        if extended_statistic is not None:
            props["extendedStatistic"] = extended_statistic

        if insufficient_data_actions is not None:
            props["insufficientDataActions"] = insufficient_data_actions

        if metric_name is not None:
            props["metricName"] = metric_name

        if metrics is not None:
            props["metrics"] = metrics

        if namespace is not None:
            props["namespace"] = namespace

        if ok_actions is not None:
            props["okActions"] = ok_actions

        if period is not None:
            props["period"] = period

        if statistic is not None:
            props["statistic"] = statistic

        if treat_missing_data is not None:
            props["treatMissingData"] = treat_missing_data

        if unit is not None:
            props["unit"] = unit

        jsii.create(CfnAlarm, self, [scope, id, props])

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
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "alarmArn")

    @property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        return jsii.get(self, "alarmName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAlarmProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.DimensionProperty", jsii_struct_bases=[])
    class DimensionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html
        """
        name: str
        """``CfnAlarm.DimensionProperty.Name``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-name
        """

        value: str
        """``CfnAlarm.DimensionProperty.Value``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-dimension.html#cfn-cloudwatch-alarm-dimension-value
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _MetricDataQueryProperty(jsii.compat.TypedDict, total=False):
        expression: str
        """``CfnAlarm.MetricDataQueryProperty.Expression``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-expression
        """
        label: str
        """``CfnAlarm.MetricDataQueryProperty.Label``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-label
        """
        metricStat: typing.Union[aws_cdk.cdk.Token, "CfnAlarm.MetricStatProperty"]
        """``CfnAlarm.MetricDataQueryProperty.MetricStat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-metricstat
        """
        returnData: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnAlarm.MetricDataQueryProperty.ReturnData``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-returndata
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricDataQueryProperty", jsii_struct_bases=[_MetricDataQueryProperty])
    class MetricDataQueryProperty(_MetricDataQueryProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html
        """
        id: str
        """``CfnAlarm.MetricDataQueryProperty.Id``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricdataquery.html#cfn-cloudwatch-alarm-metricdataquery-id
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricProperty", jsii_struct_bases=[])
    class MetricProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html
        """
        dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlarm.DimensionProperty"]]]
        """``CfnAlarm.MetricProperty.Dimensions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-dimensions
        """

        metricName: str
        """``CfnAlarm.MetricProperty.MetricName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-metricname
        """

        namespace: str
        """``CfnAlarm.MetricProperty.Namespace``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metric.html#cfn-cloudwatch-alarm-metric-namespace
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _MetricStatProperty(jsii.compat.TypedDict, total=False):
        unit: str
        """``CfnAlarm.MetricStatProperty.Unit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-unit
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarm.MetricStatProperty", jsii_struct_bases=[_MetricStatProperty])
    class MetricStatProperty(_MetricStatProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html
        """
        metric: typing.Union[aws_cdk.cdk.Token, "CfnAlarm.MetricProperty"]
        """``CfnAlarm.MetricStatProperty.Metric``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-metric
        """

        period: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnAlarm.MetricStatProperty.Period``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-period
        """

        stat: str
        """``CfnAlarm.MetricStatProperty.Stat``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cloudwatch-alarm-metricstat.html#cfn-cloudwatch-alarm-metricstat-stat
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnAlarmProps(jsii.compat.TypedDict, total=False):
    actionsEnabled: typing.Union[bool, aws_cdk.cdk.Token]
    """``AWS::CloudWatch::Alarm.ActionsEnabled``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-actionsenabled
    """
    alarmActions: typing.List[str]
    """``AWS::CloudWatch::Alarm.AlarmActions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmactions
    """
    alarmDescription: str
    """``AWS::CloudWatch::Alarm.AlarmDescription``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmdescription
    """
    alarmName: str
    """``AWS::CloudWatch::Alarm.AlarmName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-alarmname
    """
    datapointsToAlarm: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::CloudWatch::Alarm.DatapointsToAlarm``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-datapointstoalarm
    """
    dimensions: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlarm.DimensionProperty"]]]
    """``AWS::CloudWatch::Alarm.Dimensions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-dimension
    """
    evaluateLowSampleCountPercentile: str
    """``AWS::CloudWatch::Alarm.EvaluateLowSampleCountPercentile``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluatelowsamplecountpercentile
    """
    extendedStatistic: str
    """``AWS::CloudWatch::Alarm.ExtendedStatistic``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-extendedstatistic
    """
    insufficientDataActions: typing.List[str]
    """``AWS::CloudWatch::Alarm.InsufficientDataActions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-insufficientdataactions
    """
    metricName: str
    """``AWS::CloudWatch::Alarm.MetricName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-metricname
    """
    metrics: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnAlarm.MetricDataQueryProperty"]]]
    """``AWS::CloudWatch::Alarm.Metrics``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarm-metrics
    """
    namespace: str
    """``AWS::CloudWatch::Alarm.Namespace``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-namespace
    """
    okActions: typing.List[str]
    """``AWS::CloudWatch::Alarm.OKActions``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-okactions
    """
    period: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::CloudWatch::Alarm.Period``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-period
    """
    statistic: str
    """``AWS::CloudWatch::Alarm.Statistic``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-statistic
    """
    treatMissingData: str
    """``AWS::CloudWatch::Alarm.TreatMissingData``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-treatmissingdata
    """
    unit: str
    """``AWS::CloudWatch::Alarm.Unit``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-unit
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnAlarmProps", jsii_struct_bases=[_CfnAlarmProps])
class CfnAlarmProps(_CfnAlarmProps):
    """Properties for defining a ``AWS::CloudWatch::Alarm``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html
    """
    comparisonOperator: str
    """``AWS::CloudWatch::Alarm.ComparisonOperator``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-comparisonoperator
    """

    evaluationPeriods: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::CloudWatch::Alarm.EvaluationPeriods``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-evaluationperiods
    """

    threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
    """``AWS::CloudWatch::Alarm.Threshold``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-cw-alarm.html#cfn-cloudwatch-alarms-threshold
    """

class CfnDashboard(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboard"):
    """A CloudFormation ``AWS::CloudWatch::Dashboard``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
    cloudformationResource:
        AWS::CloudWatch::Dashboard
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dashboard_body: str, dashboard_name: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::CloudWatch::Dashboard``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            dashboardBody: ``AWS::CloudWatch::Dashboard.DashboardBody``.
            dashboardName: ``AWS::CloudWatch::Dashboard.DashboardName``.
        """
        props: CfnDashboardProps = {"dashboardBody": dashboard_body}

        if dashboard_name is not None:
            props["dashboardName"] = dashboard_name

        jsii.create(CfnDashboard, self, [scope, id, props])

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
    @jsii.member(jsii_name="dashboardName")
    def dashboard_name(self) -> str:
        return jsii.get(self, "dashboardName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDashboardProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDashboardProps(jsii.compat.TypedDict, total=False):
    dashboardName: str
    """``AWS::CloudWatch::Dashboard.DashboardName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardname
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.CfnDashboardProps", jsii_struct_bases=[_CfnDashboardProps])
class CfnDashboardProps(_CfnDashboardProps):
    """Properties for defining a ``AWS::CloudWatch::Dashboard``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html
    """
    dashboardBody: str
    """``AWS::CloudWatch::Dashboard.DashboardBody``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-cloudwatch-dashboard.html#cfn-cloudwatch-dashboard-dashboardbody
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.ComparisonOperator")
class ComparisonOperator(enum.Enum):
    """Comparison operator for evaluating alarms."""
    GreaterThanOrEqualToThreshold = "GreaterThanOrEqualToThreshold"
    GreaterThanThreshold = "GreaterThanThreshold"
    LessThanThreshold = "LessThanThreshold"
    LessThanOrEqualToThreshold = "LessThanOrEqualToThreshold"

class Dashboard(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Dashboard"):
    """A CloudWatch dashboard."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, dashboard_name: typing.Optional[str]=None, end: typing.Optional[str]=None, period_override: typing.Optional["PeriodOverride"]=None, start: typing.Optional[str]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            dashboardName: Name of the dashboard. Default: Automatically generated name
            end: The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the end date will be the current time.
            periodOverride: Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed. Default: Auto
            start: The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z. Default: When the dashboard loads, the start time will be the default time range.
        """
        props: DashboardProps = {}

        if dashboard_name is not None:
            props["dashboardName"] = dashboard_name

        if end is not None:
            props["end"] = end

        if period_override is not None:
            props["periodOverride"] = period_override

        if start is not None:
            props["start"] = start

        jsii.create(Dashboard, self, [scope, id, props])

    @jsii.member(jsii_name="add")
    def add(self, *widgets: "IWidget") -> None:
        """Add a widget to the dashboard.

        Widgets given in multiple calls to add() will be laid out stacked on
        top of each other.

        Multiple widgets added in the same call to add() will be laid out next
        to each other.

        Arguments:
            widgets: -
        """
        return jsii.invoke(self, "add", [widgets])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.DashboardProps", jsii_struct_bases=[])
class DashboardProps(jsii.compat.TypedDict, total=False):
    dashboardName: str
    """Name of the dashboard.

    Default:
        Automatically generated name
    """

    end: str
    """The end of the time range to use for each widget on the dashboard when the dashboard loads. If you specify a value for end, you must also specify a value for start. Specify an absolute time in the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

    Default:
        When the dashboard loads, the end date will be the current time.
    """

    periodOverride: "PeriodOverride"
    """Use this field to specify the period for the graphs when the dashboard loads. Specifying ``Auto`` causes the period of all graphs on the dashboard to automatically adapt to the time range of the dashboard. Specifying ``Inherit`` ensures that the period set for each graph is always obeyed.

    Default:
        Auto
    """

    start: str
    """The start of the time range to use for each widget on the dashboard. You can specify start without specifying end to specify a relative time range that ends with the current time. In this case, the value of start must begin with -P, and you can use M, H, D, W and M as abbreviations for minutes, hours, days, weeks and months. For example, -PT8H shows the last 8 hours and -P3M shows the last three months. You can also use start along with an end field, to specify an absolute time range. When specifying an absolute time range, use the ISO 8601 format. For example, 2018-12-17T06:00:00.000Z.

    Default:
        When the dashboard loads, the start time will be the default time range.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.Dimension", jsii_struct_bases=[])
class Dimension(jsii.compat.TypedDict):
    """Metric dimension."""
    name: str
    """Name of the dimension."""

    value: typing.Any
    """Value of the dimension."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _HorizontalAnnotation(jsii.compat.TypedDict, total=False):
    color: str
    """Hex color code to be used for the annotation.

    Default:
        Automatic color
    """
    fill: "Shading"
    """Add shading above or below the annotation.

    Default:
        No shading
    """
    label: str
    """Label for the annotation.

    Default:
        No label
    """
    visible: bool
    """Whether the annotation is visible.

    Default:
        true
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.HorizontalAnnotation", jsii_struct_bases=[_HorizontalAnnotation])
class HorizontalAnnotation(_HorizontalAnnotation):
    """Horizontal annotation to be added to a graph."""
    value: jsii.Number
    """The value of the annotation."""

@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarm")
class IAlarm(aws_cdk.cdk.IResource, jsii.compat.Protocol):
    @staticmethod
    def __jsii_proxy_class__():
        return _IAlarmProxy

    @property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """
        attribute:
            true
        """
        ...

    @property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        """
        attribute:
            true
        """
        ...


class _IAlarmProxy(jsii.proxy_for(aws_cdk.cdk.IResource)):
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IAlarm"
    @property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "alarmArn")

    @property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        """
        attribute:
            true
        """
        return jsii.get(self, "alarmName")


@jsii.implements(IAlarm)
class Alarm(aws_cdk.cdk.Resource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Alarm"):
    """An alarm on a CloudWatch metric."""
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, metric: "Metric", evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> None:
        """
        Arguments:
            scope: -
            id: -
            props: -
            metric: The metric to add the alarm on. Metric objects can be obtained from most resources, or you can construct custom Metric objects by instantiating one.
            evaluationPeriods: The number of periods over which data is compared to the specified threshold.
            threshold: The value against which the specified statistic is compared.
            actionsEnabled: Whether the actions for this alarm are enabled. Default: true
            alarmDescription: Description for the alarm. Default: No description
            alarmName: Name of the alarm. Default: Automatically generated name
            comparisonOperator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
            datapointsToAlarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
            evaluateLowSampleCountPercentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            treatMissingData: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props: AlarmProps = {"metric": metric, "evaluationPeriods": evaluation_periods, "threshold": threshold}

        if actions_enabled is not None:
            props["actionsEnabled"] = actions_enabled

        if alarm_description is not None:
            props["alarmDescription"] = alarm_description

        if alarm_name is not None:
            props["alarmName"] = alarm_name

        if comparison_operator is not None:
            props["comparisonOperator"] = comparison_operator

        if datapoints_to_alarm is not None:
            props["datapointsToAlarm"] = datapoints_to_alarm

        if evaluate_low_sample_count_percentile is not None:
            props["evaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if treat_missing_data is not None:
            props["treatMissingData"] = treat_missing_data

        jsii.create(Alarm, self, [scope, id, props])

    @jsii.member(jsii_name="fromAlarmArn")
    @classmethod
    def from_alarm_arn(cls, scope: aws_cdk.cdk.Construct, id: str, alarm_arn: str) -> "IAlarm":
        """
        Arguments:
            scope: -
            id: -
            alarmArn: -
        """
        return jsii.sinvoke(cls, "fromAlarmArn", [scope, id, alarm_arn])

    @jsii.member(jsii_name="addAlarmAction")
    def add_alarm_action(self, *actions: "IAlarmAction") -> None:
        """Trigger this action if the alarm fires.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        Arguments:
            actions: -
        """
        return jsii.invoke(self, "addAlarmAction", [actions])

    @jsii.member(jsii_name="addInsufficientDataAction")
    def add_insufficient_data_action(self, *actions: "IAlarmAction") -> None:
        """Trigger this action if there is insufficient data to evaluate the alarm.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        Arguments:
            actions: -
        """
        return jsii.invoke(self, "addInsufficientDataAction", [actions])

    @jsii.member(jsii_name="addOkAction")
    def add_ok_action(self, *actions: "IAlarmAction") -> None:
        """Trigger this action if the alarm returns from breaching state into ok state.

        Typically the ARN of an SNS topic or ARN of an AutoScaling policy.

        Arguments:
            actions: -
        """
        return jsii.invoke(self, "addOkAction", [actions])

    @jsii.member(jsii_name="toAnnotation")
    def to_annotation(self) -> "HorizontalAnnotation":
        """Turn this alarm into a horizontal annotation.

        This is useful if you want to represent an Alarm in a non-AlarmWidget.
        An ``AlarmWidget`` can directly show an alarm, but it can only show a
        single alarm and no other metrics. Instead, you can convert the alarm to
        a HorizontalAnnotation and add it as an annotation to another graph.

        This might be useful if:

        - You want to show multiple alarms inside a single graph, for example if
          you have both a "small margin/long period" alarm as well as a
          "large margin/short period" alarm.
        - You want to show an Alarm line in a graph with multiple metrics in it.
        """
        return jsii.invoke(self, "toAnnotation", [])

    @property
    @jsii.member(jsii_name="alarmArn")
    def alarm_arn(self) -> str:
        """ARN of this alarm.

        attribute:
            true
        """
        return jsii.get(self, "alarmArn")

    @property
    @jsii.member(jsii_name="alarmName")
    def alarm_name(self) -> str:
        """Name of this alarm.

        attribute:
            true
        """
        return jsii.get(self, "alarmName")

    @property
    @jsii.member(jsii_name="metric")
    def metric(self) -> "Metric":
        """The metric object this alarm was based on."""
        return jsii.get(self, "metric")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IAlarmAction")
class IAlarmAction(jsii.compat.Protocol):
    """Interface for objects that can be the targets of CloudWatch alarm actions."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IAlarmActionProxy

    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        """Return the ARN that should be used for a CloudWatch Alarm action."""
        ...


class _IAlarmActionProxy():
    """Interface for objects that can be the targets of CloudWatch alarm actions."""
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IAlarmAction"
    @property
    @jsii.member(jsii_name="alarmActionArn")
    def alarm_action_arn(self) -> str:
        """Return the ARN that should be used for a CloudWatch Alarm action."""
        return jsii.get(self, "alarmActionArn")


@jsii.interface(jsii_type="@aws-cdk/aws-cloudwatch.IWidget")
class IWidget(jsii.compat.Protocol):
    """A single dashboard widget."""
    @staticmethod
    def __jsii_proxy_class__():
        return _IWidgetProxy

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        ...

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        ...

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            x: -
            y: -
        """
        ...

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        ...


class _IWidgetProxy():
    """A single dashboard widget."""
    __jsii_type__ = "@aws-cdk/aws-cloudwatch.IWidget"
    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            x: -
            y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.implements(IWidget)
class Column(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Column"):
    """A widget that contains other widgets in a vertical column.

    Widgets will be laid out next to each other
    """
    def __init__(self, *widgets: "IWidget") -> None:
        """
        Arguments:
            widgets: -
        """
        jsii.create(Column, self, [widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            x: -
            y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.implements(IWidget)
class ConcreteWidget(metaclass=jsii.JSIIAbstractClass, jsii_type="@aws-cdk/aws-cloudwatch.ConcreteWidget"):
    """A real CloudWatch widget that has its own fixed size and remembers its position.

    This is in contrast to other widgets which exist for layout purposes.
    """
    @staticmethod
    def __jsii_proxy_class__():
        return _ConcreteWidgetProxy

    def __init__(self, width: jsii.Number, height: jsii.Number) -> None:
        """
        Arguments:
            width: -
            height: -
        """
        jsii.create(ConcreteWidget, self, [width, height])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            x: -
            y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    @abc.abstractmethod
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        ...

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")

    @property
    @jsii.member(jsii_name="x")
    def _x(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "x")

    @_x.setter
    def _x(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "x", value)

    @property
    @jsii.member(jsii_name="y")
    def _y(self) -> typing.Optional[jsii.Number]:
        return jsii.get(self, "y")

    @_y.setter
    def _y(self, value: typing.Optional[jsii.Number]):
        return jsii.set(self, "y", value)


class _ConcreteWidgetProxy(ConcreteWidget):
    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class AlarmWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidget"):
    """Display the metric associated with an alarm, including the alarm line."""
    def __init__(self, *, alarm: "Alarm", left_axis_range: typing.Optional["YAxisRange"]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            props: -
            alarm: The alarm to show.
            leftAxisRange: Range of left Y axis. Default: 0..automatic
            height: Height of the widget. Default: Depends on the type of widget
            region: The region the metrics of this graph should be taken from. Default: Current region
            title: Title for the graph.
            width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props: AlarmWidgetProps = {"alarm": alarm}

        if left_axis_range is not None:
            props["leftAxisRange"] = left_axis_range

        if height is not None:
            props["height"] = height

        if region is not None:
            props["region"] = region

        if title is not None:
            props["title"] = title

        if width is not None:
            props["width"] = width

        jsii.create(AlarmWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class GraphWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.GraphWidget"):
    """A dashboard widget that displays metrics."""
    def __init__(self, *, left: typing.Optional[typing.List["Metric"]]=None, left_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, left_axis_range: typing.Optional["YAxisRange"]=None, right: typing.Optional[typing.List["Metric"]]=None, right_annotations: typing.Optional[typing.List["HorizontalAnnotation"]]=None, right_axis_range: typing.Optional["YAxisRange"]=None, stacked: typing.Optional[bool]=None, height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            props: -
            left: Metrics to display on left Y axis.
            leftAnnotations: Annotations for the left Y axis.
            leftAxisRange: Range of left Y axis. Default: 0..automatic
            right: Metrics to display on right Y axis.
            rightAnnotations: Annotations for the right Y axis.
            rightAxisRange: Range of right Y axis. Default: 0..automatic
            stacked: Whether the graph should be shown as stacked lines.
            height: Height of the widget. Default: Depends on the type of widget
            region: The region the metrics of this graph should be taken from. Default: Current region
            title: Title for the graph.
            width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props: GraphWidgetProps = {}

        if left is not None:
            props["left"] = left

        if left_annotations is not None:
            props["leftAnnotations"] = left_annotations

        if left_axis_range is not None:
            props["leftAxisRange"] = left_axis_range

        if right is not None:
            props["right"] = right

        if right_annotations is not None:
            props["rightAnnotations"] = right_annotations

        if right_axis_range is not None:
            props["rightAxisRange"] = right_axis_range

        if stacked is not None:
            props["stacked"] = stacked

        if height is not None:
            props["height"] = height

        if region is not None:
            props["region"] = region

        if title is not None:
            props["title"] = title

        if width is not None:
            props["width"] = width

        jsii.create(GraphWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


class Metric(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Metric"):
    """A metric emitted by a service.

    The metric is a combination of a metric identifier (namespace, name and dimensions)
    and an aggregation function (statistic, period and unit).

    It also contains metadata which is used only in graphs, such as color and label.
    It makes sense to embed this in here, so that compound constructs can attach
    that metadata to metrics they expose.

    This class does not represent a resource, so hence is not a construct. Instead,
    Metric is an abstraction that makes it easy to specify metrics for use in both
    alarms and graphs.
    """
    def __init__(self, *, metric_name: str, namespace: str, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None) -> None:
        """
        Arguments:
            props: -
            metricName: Name of the metric.
            namespace: Namespace of the metric.
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following (case insensitive) - "minimum" | "min" - "maximum" | "max" - "average" | "avg" - "sum" - "samplecount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: MetricProps = {"metricName": metric_name, "namespace": namespace}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        jsii.create(Metric, self, [props])

    @jsii.member(jsii_name="grantPutMetricData")
    @classmethod
    def grant_put_metric_data(cls, grantee: aws_cdk.aws_iam.IGrantable) -> aws_cdk.aws_iam.Grant:
        """Grant permissions to the given identity to write metrics.

        Arguments:
            grantee: The IAM identity to give permissions to.
        """
        return jsii.sinvoke(cls, "grantPutMetricData", [grantee])

    @jsii.member(jsii_name="dimensionsAsList")
    def dimensions_as_list(self) -> typing.List["Dimension"]:
        """Return the dimensions of this Metric as a list of Dimension."""
        return jsii.invoke(self, "dimensionsAsList", [])

    @jsii.member(jsii_name="newAlarm")
    def new_alarm(self, scope: aws_cdk.cdk.Construct, id: str, *, evaluation_periods: jsii.Number, threshold: jsii.Number, actions_enabled: typing.Optional[bool]=None, alarm_description: typing.Optional[str]=None, alarm_name: typing.Optional[str]=None, comparison_operator: typing.Optional["ComparisonOperator"]=None, datapoints_to_alarm: typing.Optional[jsii.Number]=None, evaluate_low_sample_count_percentile: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, treat_missing_data: typing.Optional["TreatMissingData"]=None) -> "Alarm":
        """Make a new Alarm for this metric.

        Combines both properties that may adjust the metric (aggregation) as well
        as alarm properties.

        Arguments:
            scope: -
            id: -
            props: -
            evaluationPeriods: The number of periods over which data is compared to the specified threshold.
            threshold: The value against which the specified statistic is compared.
            actionsEnabled: Whether the actions for this alarm are enabled. Default: true
            alarmDescription: Description for the alarm. Default: No description
            alarmName: Name of the alarm. Default: Automatically generated name
            comparisonOperator: Comparison to use to check if metric is breaching. Default: GreaterThanOrEqualToThreshold
            datapointsToAlarm: The number of datapoints that must be breaching to trigger the alarm. This is used only if you are setting an "M out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon CloudWatch User Guide. Default: ``evaluationPeriods``
            evaluateLowSampleCountPercentile: Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant. Used only for alarms that are based on percentiles. Default: - Not configured.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            treatMissingData: Sets how this alarm is to handle missing data points. Default: TreatMissingData.Missing
        """
        props: MetricAlarmProps = {"evaluationPeriods": evaluation_periods, "threshold": threshold}

        if actions_enabled is not None:
            props["actionsEnabled"] = actions_enabled

        if alarm_description is not None:
            props["alarmDescription"] = alarm_description

        if alarm_name is not None:
            props["alarmName"] = alarm_name

        if comparison_operator is not None:
            props["comparisonOperator"] = comparison_operator

        if datapoints_to_alarm is not None:
            props["datapointsToAlarm"] = datapoints_to_alarm

        if evaluate_low_sample_count_percentile is not None:
            props["evaluateLowSampleCountPercentile"] = evaluate_low_sample_count_percentile

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if treat_missing_data is not None:
            props["treatMissingData"] = treat_missing_data

        return jsii.invoke(self, "newAlarm", [scope, id, props])

    @jsii.member(jsii_name="with")
    def with_(self, *, color: typing.Optional[str]=None, dimensions: typing.Optional[typing.Mapping[str,typing.Any]]=None, label: typing.Optional[str]=None, period_sec: typing.Optional[jsii.Number]=None, statistic: typing.Optional[str]=None, unit: typing.Optional["Unit"]=None) -> "Metric":
        """Return a copy of Metric with properties changed.

        All properties except namespace and metricName can be changed.

        Arguments:
            props: The set of properties to change.
            color: Color for this metric when added to a Graph in a Dashboard.
            dimensions: Dimensions of the metric. Default: - No dimensions.
            label: Label for this metric when added to a Graph in a Dashboard.
            periodSec: The period over which the specified statistic is applied. Specify time in seconds, in multiples of 60. Default: 300
            statistic: What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
            unit: Unit for the metric that is associated with the alarm.
        """
        props: MetricOptions = {}

        if color is not None:
            props["color"] = color

        if dimensions is not None:
            props["dimensions"] = dimensions

        if label is not None:
            props["label"] = label

        if period_sec is not None:
            props["periodSec"] = period_sec

        if statistic is not None:
            props["statistic"] = statistic

        if unit is not None:
            props["unit"] = unit

        return jsii.invoke(self, "with", [props])

    @property
    @jsii.member(jsii_name="metricName")
    def metric_name(self) -> str:
        return jsii.get(self, "metricName")

    @property
    @jsii.member(jsii_name="namespace")
    def namespace(self) -> str:
        return jsii.get(self, "namespace")

    @property
    @jsii.member(jsii_name="periodSec")
    def period_sec(self) -> jsii.Number:
        return jsii.get(self, "periodSec")

    @property
    @jsii.member(jsii_name="statistic")
    def statistic(self) -> str:
        return jsii.get(self, "statistic")

    @property
    @jsii.member(jsii_name="color")
    def color(self) -> typing.Optional[str]:
        return jsii.get(self, "color")

    @property
    @jsii.member(jsii_name="dimensions")
    def dimensions(self) -> typing.Optional[typing.Mapping[str,typing.Any]]:
        return jsii.get(self, "dimensions")

    @property
    @jsii.member(jsii_name="label")
    def label(self) -> typing.Optional[str]:
        return jsii.get(self, "label")

    @property
    @jsii.member(jsii_name="unit")
    def unit(self) -> typing.Optional["Unit"]:
        return jsii.get(self, "unit")


@jsii.data_type_optionals(jsii_struct_bases=[])
class _MetricAlarmProps(jsii.compat.TypedDict, total=False):
    actionsEnabled: bool
    """Whether the actions for this alarm are enabled.

    Default:
        true
    """
    alarmDescription: str
    """Description for the alarm.

    Default:
        No description
    """
    alarmName: str
    """Name of the alarm.

    Default:
        Automatically generated name
    """
    comparisonOperator: "ComparisonOperator"
    """Comparison to use to check if metric is breaching.

    Default:
        GreaterThanOrEqualToThreshold
    """
    datapointsToAlarm: jsii.Number
    """The number of datapoints that must be breaching to trigger the alarm.

    This is used only if you are setting an "M
    out of N" alarm. In that case, this value is the M. For more information, see Evaluating an Alarm in the Amazon
    CloudWatch User Guide.

    Default:
        ``evaluationPeriods``

    See:
        https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html#alarm-evaluation
    """
    evaluateLowSampleCountPercentile: str
    """Specifies whether to evaluate the data and potentially change the alarm state if there are too few data points to be statistically significant.

    Used only for alarms that are based on percentiles.

    Default:
        - Not configured.
    """
    periodSec: jsii.Number
    """The period over which the specified statistic is applied.

    Specify time in seconds, in multiples of 60.

    Default:
        300
    """
    statistic: str
    """What function to use for aggregating.

    Can be one of the following:

    - "Minimum" | "min"
    - "Maximum" | "max"
    - "Average" | "avg"
    - "Sum" | "sum"
    - "SampleCount | "n"
    - "pNN.NN"

    Default:
        Average
    """
    treatMissingData: "TreatMissingData"
    """Sets how this alarm is to handle missing data points.

    Default:
        TreatMissingData.Missing
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricAlarmProps", jsii_struct_bases=[_MetricAlarmProps])
class MetricAlarmProps(_MetricAlarmProps):
    """Properties needed to make an alarm from a metric."""
    evaluationPeriods: jsii.Number
    """The number of periods over which data is compared to the specified threshold."""

    threshold: jsii.Number
    """The value against which the specified statistic is compared."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmProps", jsii_struct_bases=[MetricAlarmProps])
class AlarmProps(MetricAlarmProps, jsii.compat.TypedDict):
    """Properties for Alarms."""
    metric: "Metric"
    """The metric to add the alarm on.

    Metric objects can be obtained from most resources, or you can construct
    custom Metric objects by instantiating one.
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricOptions", jsii_struct_bases=[])
class MetricOptions(jsii.compat.TypedDict, total=False):
    """Properties of a metric that can be changed."""
    color: str
    """Color for this metric when added to a Graph in a Dashboard."""

    dimensions: typing.Mapping[str,typing.Any]
    """Dimensions of the metric.

    Default:
        - No dimensions.
    """

    label: str
    """Label for this metric when added to a Graph in a Dashboard."""

    periodSec: jsii.Number
    """The period over which the specified statistic is applied.

    Specify time in seconds, in multiples of 60.

    Default:
        300
    """

    statistic: str
    """What function to use for aggregating.

    Can be one of the following:

    - "Minimum" | "min"
    - "Maximum" | "max"
    - "Average" | "avg"
    - "Sum" | "sum"
    - "SampleCount | "n"
    - "pNN.NN"

    Default:
        Average
    """

    unit: "Unit"
    """Unit for the metric that is associated with the alarm."""

@jsii.data_type_optionals(jsii_struct_bases=[])
class _MetricProps(jsii.compat.TypedDict, total=False):
    color: str
    """Color for this metric when added to a Graph in a Dashboard."""
    dimensions: typing.Mapping[str,typing.Any]
    """Dimensions of the metric.

    Default:
        - No dimensions.
    """
    label: str
    """Label for this metric when added to a Graph in a Dashboard."""
    periodSec: jsii.Number
    """The period over which the specified statistic is applied.

    Specify time in seconds, in multiples of 60.

    Default:
        300
    """
    statistic: str
    """What function to use for aggregating.

    Can be one of the following (case insensitive)

    - "minimum" | "min"
    - "maximum" | "max"
    - "average" | "avg"
    - "sum"
    - "samplecount | "n"
    - "pNN.NN"

    Default:
        Average
    """
    unit: "Unit"
    """Unit for the metric that is associated with the alarm."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricProps", jsii_struct_bases=[_MetricProps])
class MetricProps(_MetricProps):
    """Properties for a metric."""
    metricName: str
    """Name of the metric."""

    namespace: str
    """Namespace of the metric."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.MetricWidgetProps", jsii_struct_bases=[])
class MetricWidgetProps(jsii.compat.TypedDict, total=False):
    """Basic properties for widgets that display metrics."""
    height: jsii.Number
    """Height of the widget.

    Default:
        Depends on the type of widget
    """

    region: str
    """The region the metrics of this graph should be taken from.

    Default:
        Current region
    """

    title: str
    """Title for the graph."""

    width: jsii.Number
    """Width of the widget, in a grid of 24 units wide.

    Default:
        6
    """

@jsii.data_type_optionals(jsii_struct_bases=[MetricWidgetProps])
class _AlarmWidgetProps(MetricWidgetProps, jsii.compat.TypedDict, total=False):
    leftAxisRange: "YAxisRange"
    """Range of left Y axis.

    Default:
        0..automatic
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.AlarmWidgetProps", jsii_struct_bases=[_AlarmWidgetProps])
class AlarmWidgetProps(_AlarmWidgetProps):
    """Properties for an AlarmWidget."""
    alarm: "Alarm"
    """The alarm to show."""

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.GraphWidgetProps", jsii_struct_bases=[MetricWidgetProps])
class GraphWidgetProps(MetricWidgetProps, jsii.compat.TypedDict, total=False):
    """Properties for a GraphWidget."""
    left: typing.List["Metric"]
    """Metrics to display on left Y axis."""

    leftAnnotations: typing.List["HorizontalAnnotation"]
    """Annotations for the left Y axis."""

    leftAxisRange: "YAxisRange"
    """Range of left Y axis.

    Default:
        0..automatic
    """

    right: typing.List["Metric"]
    """Metrics to display on right Y axis."""

    rightAnnotations: typing.List["HorizontalAnnotation"]
    """Annotations for the right Y axis."""

    rightAxisRange: "YAxisRange"
    """Range of right Y axis.

    Default:
        0..automatic
    """

    stacked: bool
    """Whether the graph should be shown as stacked lines."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.PeriodOverride")
class PeriodOverride(enum.Enum):
    Auto = "Auto"
    Inherit = "Inherit"

@jsii.implements(IWidget)
class Row(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Row"):
    """A widget that contains other widgets in a horizontal row.

    Widgets will be laid out next to each other
    """
    def __init__(self, *widgets: "IWidget") -> None:
        """
        Arguments:
            widgets: -
        """
        jsii.create(Row, self, [widgets])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            x: -
            y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Shading")
class Shading(enum.Enum):
    None_ = "None"
    """Don't add shading."""
    Above = "Above"
    """Add shading above the annotation."""
    Below = "Below"
    """Add shading below the annotation."""

class SingleValueWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidget"):
    """A dashboard widget that displays the most recent value for every metric."""
    def __init__(self, *, metrics: typing.List["Metric"], height: typing.Optional[jsii.Number]=None, region: typing.Optional[str]=None, title: typing.Optional[str]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            props: -
            metrics: Metrics to display.
            height: Height of the widget. Default: Depends on the type of widget
            region: The region the metrics of this graph should be taken from. Default: Current region
            title: Title for the graph.
            width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props: SingleValueWidgetProps = {"metrics": metrics}

        if height is not None:
            props["height"] = height

        if region is not None:
            props["region"] = region

        if title is not None:
            props["title"] = title

        if width is not None:
            props["width"] = width

        jsii.create(SingleValueWidget, self, [props])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.SingleValueWidgetProps", jsii_struct_bases=[MetricWidgetProps])
class SingleValueWidgetProps(MetricWidgetProps, jsii.compat.TypedDict):
    """Properties for a SingleValueWidget."""
    metrics: typing.List["Metric"]
    """Metrics to display."""

@jsii.implements(IWidget)
class Spacer(metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.Spacer"):
    """A widget that doesn't display anything but takes up space."""
    def __init__(self, *, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            props: -
            height: Height of the spacer. Default: : 1
            width: Width of the spacer. Default: 1
        """
        props: SpacerProps = {}

        if height is not None:
            props["height"] = height

        if width is not None:
            props["width"] = width

        jsii.create(Spacer, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, _x: jsii.Number, _y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            _x: -
            _y: -
        """
        return jsii.invoke(self, "position", [_x, _y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])

    @property
    @jsii.member(jsii_name="height")
    def height(self) -> jsii.Number:
        """The amount of vertical grid units the widget will take up."""
        return jsii.get(self, "height")

    @property
    @jsii.member(jsii_name="width")
    def width(self) -> jsii.Number:
        """The amount of horizontal grid units the widget will take up."""
        return jsii.get(self, "width")


@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.SpacerProps", jsii_struct_bases=[])
class SpacerProps(jsii.compat.TypedDict, total=False):
    """Props of the spacer."""
    height: jsii.Number
    """Height of the spacer.

    Default:
        : 1
    """

    width: jsii.Number
    """Width of the spacer.

    Default:
        1
    """

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Statistic")
class Statistic(enum.Enum):
    """Statistic to use over the aggregation period."""
    SampleCount = "SampleCount"
    Average = "Average"
    Sum = "Sum"
    Minimum = "Minimum"
    Maximum = "Maximum"

class TextWidget(ConcreteWidget, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-cloudwatch.TextWidget"):
    """A dashboard widget that displays MarkDown."""
    def __init__(self, *, markdown: str, height: typing.Optional[jsii.Number]=None, width: typing.Optional[jsii.Number]=None) -> None:
        """
        Arguments:
            props: -
            markdown: The text to display, in MarkDown format.
            height: Height of the widget. Default: 2
            width: Width of the widget, in a grid of 24 units wide. Default: 6
        """
        props: TextWidgetProps = {"markdown": markdown}

        if height is not None:
            props["height"] = height

        if width is not None:
            props["width"] = width

        jsii.create(TextWidget, self, [props])

    @jsii.member(jsii_name="position")
    def position(self, x: jsii.Number, y: jsii.Number) -> None:
        """Place the widget at a given position.

        Arguments:
            x: -
            y: -
        """
        return jsii.invoke(self, "position", [x, y])

    @jsii.member(jsii_name="toJson")
    def to_json(self) -> typing.List[typing.Any]:
        """Return the widget JSON for use in the dashboard."""
        return jsii.invoke(self, "toJson", [])


@jsii.data_type_optionals(jsii_struct_bases=[])
class _TextWidgetProps(jsii.compat.TypedDict, total=False):
    height: jsii.Number
    """Height of the widget.

    Default:
        2
    """
    width: jsii.Number
    """Width of the widget, in a grid of 24 units wide.

    Default:
        6
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.TextWidgetProps", jsii_struct_bases=[_TextWidgetProps])
class TextWidgetProps(_TextWidgetProps):
    """Properties for a Text widget."""
    markdown: str
    """The text to display, in MarkDown format."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.TreatMissingData")
class TreatMissingData(enum.Enum):
    """Specify how missing data points are treated during alarm evaluation."""
    Breaching = "Breaching"
    """Missing data points are treated as breaching the threshold."""
    NotBreaching = "NotBreaching"
    """Missing data points are treated as being within the threshold."""
    Ignore = "Ignore"
    """The current alarm state is maintained."""
    Missing = "Missing"
    """The alarm does not consider missing data points when evaluating whether to change state."""

@jsii.enum(jsii_type="@aws-cdk/aws-cloudwatch.Unit")
class Unit(enum.Enum):
    """Unit for metric."""
    Seconds = "Seconds"
    Microseconds = "Microseconds"
    Milliseconds = "Milliseconds"
    Bytes_ = "Bytes_"
    Kilobytes = "Kilobytes"
    Megabytes = "Megabytes"
    Gigabytes = "Gigabytes"
    Terabytes = "Terabytes"
    Bits = "Bits"
    Kilobits = "Kilobits"
    Megabits = "Megabits"
    Gigabits = "Gigabits"
    Terabits = "Terabits"
    Percent = "Percent"
    Count = "Count"
    BytesPerSecond = "BytesPerSecond"
    KilobytesPerSecond = "KilobytesPerSecond"
    MegabytesPerSecond = "MegabytesPerSecond"
    GigabytesPerSecond = "GigabytesPerSecond"
    TerabytesPerSecond = "TerabytesPerSecond"
    BitsPerSecond = "BitsPerSecond"
    KilobitsPerSecond = "KilobitsPerSecond"
    MegabitsPerSecond = "MegabitsPerSecond"
    GigabitsPerSecond = "GigabitsPerSecond"
    TerabitsPerSecond = "TerabitsPerSecond"
    CountPerSecond = "CountPerSecond"
    None_ = "None"

@jsii.data_type(jsii_type="@aws-cdk/aws-cloudwatch.YAxisRange", jsii_struct_bases=[])
class YAxisRange(jsii.compat.TypedDict, total=False):
    """A minimum and maximum value for either the left or right Y axis."""
    max: jsii.Number
    """The maximum value.

    Default:
        Automatic
    """

    min: jsii.Number
    """The minimum value.

    Default:
        Automatic
    """

__all__ = ["Alarm", "AlarmMetricJson", "AlarmProps", "AlarmWidget", "AlarmWidgetProps", "CfnAlarm", "CfnAlarmProps", "CfnDashboard", "CfnDashboardProps", "Column", "ComparisonOperator", "ConcreteWidget", "Dashboard", "DashboardProps", "Dimension", "GraphWidget", "GraphWidgetProps", "HorizontalAnnotation", "IAlarm", "IAlarmAction", "IWidget", "Metric", "MetricAlarmProps", "MetricOptions", "MetricProps", "MetricWidgetProps", "PeriodOverride", "Row", "Shading", "SingleValueWidget", "SingleValueWidgetProps", "Spacer", "SpacerProps", "Statistic", "TextWidget", "TextWidgetProps", "TreatMissingData", "Unit", "YAxisRange", "__jsii_assembly__"]

publication.publish()
