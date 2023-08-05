import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-config", "0.31.0", __name__, "aws-config@0.31.0.jsii.tgz")
class CfnAggregationAuthorization(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnAggregationAuthorization"):
    """A CloudFormation ``AWS::Config::AggregationAuthorization``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html
    cloudformationResource:
        AWS::Config::AggregationAuthorization
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, authorized_account_id: str, authorized_aws_region: str) -> None:
        """Create a new ``AWS::Config::AggregationAuthorization``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            authorizedAccountId: ``AWS::Config::AggregationAuthorization.AuthorizedAccountId``.
            authorizedAwsRegion: ``AWS::Config::AggregationAuthorization.AuthorizedAwsRegion``.
        """
        props: CfnAggregationAuthorizationProps = {"authorizedAccountId": authorized_account_id, "authorizedAwsRegion": authorized_aws_region}

        jsii.create(CfnAggregationAuthorization, self, [scope, id, props])

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
    @jsii.member(jsii_name="aggregationAuthorizationArn")
    def aggregation_authorization_arn(self) -> str:
        return jsii.get(self, "aggregationAuthorizationArn")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnAggregationAuthorizationProps":
        return jsii.get(self, "propertyOverrides")


@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnAggregationAuthorizationProps", jsii_struct_bases=[])
class CfnAggregationAuthorizationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::Config::AggregationAuthorization``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html
    """
    authorizedAccountId: str
    """``AWS::Config::AggregationAuthorization.AuthorizedAccountId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedaccountid
    """

    authorizedAwsRegion: str
    """``AWS::Config::AggregationAuthorization.AuthorizedAwsRegion``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-aggregationauthorization.html#cfn-config-aggregationauthorization-authorizedawsregion
    """

class CfnConfigRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnConfigRule"):
    """A CloudFormation ``AWS::Config::ConfigRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html
    cloudformationResource:
        AWS::Config::ConfigRule
    """
    def __init__(self, scope_: aws_cdk.cdk.Construct, id: str, *, source: typing.Union["SourceProperty", aws_cdk.cdk.Token], config_rule_name: typing.Optional[str]=None, description: typing.Optional[str]=None, input_parameters: typing.Optional[typing.Union[typing.Optional[typing.Mapping[typing.Any, typing.Any]], typing.Optional[aws_cdk.cdk.Token]]]=None, maximum_execution_frequency: typing.Optional[str]=None, scope: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ScopeProperty"]]]=None) -> None:
        """Create a new ``AWS::Config::ConfigRule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            source: ``AWS::Config::ConfigRule.Source``.
            configRuleName: ``AWS::Config::ConfigRule.ConfigRuleName``.
            description: ``AWS::Config::ConfigRule.Description``.
            inputParameters: ``AWS::Config::ConfigRule.InputParameters``.
            maximumExecutionFrequency: ``AWS::Config::ConfigRule.MaximumExecutionFrequency``.
            scope: ``AWS::Config::ConfigRule.Scope``.
        """
        props: CfnConfigRuleProps = {"source": source}

        if config_rule_name is not None:
            props["configRuleName"] = config_rule_name

        if description is not None:
            props["description"] = description

        if input_parameters is not None:
            props["inputParameters"] = input_parameters

        if maximum_execution_frequency is not None:
            props["maximumExecutionFrequency"] = maximum_execution_frequency

        if scope is not None:
            props["scope"] = scope

        jsii.create(CfnConfigRule, self, [scope, id, props])

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
    @jsii.member(jsii_name="configRuleArn")
    def config_rule_arn(self) -> str:
        """
        cloudformationAttribute:
            Arn
        """
        return jsii.get(self, "configRuleArn")

    @property
    @jsii.member(jsii_name="configRuleComplianceType")
    def config_rule_compliance_type(self) -> str:
        """
        cloudformationAttribute:
            Compliance.Type
        """
        return jsii.get(self, "configRuleComplianceType")

    @property
    @jsii.member(jsii_name="configRuleId")
    def config_rule_id(self) -> str:
        """
        cloudformationAttribute:
            ConfigRuleId
        """
        return jsii.get(self, "configRuleId")

    @property
    @jsii.member(jsii_name="configRuleName")
    def config_rule_name(self) -> str:
        return jsii.get(self, "configRuleName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigRuleProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRule.ScopeProperty", jsii_struct_bases=[])
    class ScopeProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html
        """
        complianceResourceId: str
        """``CfnConfigRule.ScopeProperty.ComplianceResourceId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-complianceresourceid
        """

        complianceResourceTypes: typing.List[str]
        """``CfnConfigRule.ScopeProperty.ComplianceResourceTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-complianceresourcetypes
        """

        tagKey: str
        """``CfnConfigRule.ScopeProperty.TagKey``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-tagkey
        """

        tagValue: str
        """``CfnConfigRule.ScopeProperty.TagValue``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-scope.html#cfn-config-configrule-scope-tagvalue
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SourceDetailProperty(jsii.compat.TypedDict, total=False):
        maximumExecutionFrequency: str
        """``CfnConfigRule.SourceDetailProperty.MaximumExecutionFrequency``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html#cfn-config-configrule-sourcedetail-maximumexecutionfrequency
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRule.SourceDetailProperty", jsii_struct_bases=[_SourceDetailProperty])
    class SourceDetailProperty(_SourceDetailProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html
        """
        eventSource: str
        """``CfnConfigRule.SourceDetailProperty.EventSource``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html#cfn-config-configrule-source-sourcedetail-eventsource
        """

        messageType: str
        """``CfnConfigRule.SourceDetailProperty.MessageType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source-sourcedetails.html#cfn-config-configrule-source-sourcedetail-messagetype
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _SourceProperty(jsii.compat.TypedDict, total=False):
        sourceDetails: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigRule.SourceDetailProperty"]]]
        """``CfnConfigRule.SourceProperty.SourceDetails``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-sourcedetails
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRule.SourceProperty", jsii_struct_bases=[_SourceProperty])
    class SourceProperty(_SourceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html
        """
        owner: str
        """``CfnConfigRule.SourceProperty.Owner``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-owner
        """

        sourceIdentifier: str
        """``CfnConfigRule.SourceProperty.SourceIdentifier``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configrule-source.html#cfn-config-configrule-source-sourceidentifier
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigRuleProps(jsii.compat.TypedDict, total=False):
    configRuleName: str
    """``AWS::Config::ConfigRule.ConfigRuleName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-configrulename
    """
    description: str
    """``AWS::Config::ConfigRule.Description``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-description
    """
    inputParameters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
    """``AWS::Config::ConfigRule.InputParameters``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-inputparameters
    """
    maximumExecutionFrequency: str
    """``AWS::Config::ConfigRule.MaximumExecutionFrequency``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-maximumexecutionfrequency
    """
    scope: typing.Union[aws_cdk.cdk.Token, "CfnConfigRule.ScopeProperty"]
    """``AWS::Config::ConfigRule.Scope``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-scope
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigRuleProps", jsii_struct_bases=[_CfnConfigRuleProps])
class CfnConfigRuleProps(_CfnConfigRuleProps):
    """Properties for defining a ``AWS::Config::ConfigRule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html
    """
    source: typing.Union["CfnConfigRule.SourceProperty", aws_cdk.cdk.Token]
    """``AWS::Config::ConfigRule.Source``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configrule.html#cfn-config-configrule-source
    """

class CfnConfigurationAggregator(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregator"):
    """A CloudFormation ``AWS::Config::ConfigurationAggregator``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
    cloudformationResource:
        AWS::Config::ConfigurationAggregator
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, configuration_aggregator_name: str, account_aggregation_sources: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "AccountAggregationSourceProperty"]]]]]=None, organization_aggregation_source: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["OrganizationAggregationSourceProperty"]]]=None) -> None:
        """Create a new ``AWS::Config::ConfigurationAggregator``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            configurationAggregatorName: ``AWS::Config::ConfigurationAggregator.ConfigurationAggregatorName``.
            accountAggregationSources: ``AWS::Config::ConfigurationAggregator.AccountAggregationSources``.
            organizationAggregationSource: ``AWS::Config::ConfigurationAggregator.OrganizationAggregationSource``.
        """
        props: CfnConfigurationAggregatorProps = {"configurationAggregatorName": configuration_aggregator_name}

        if account_aggregation_sources is not None:
            props["accountAggregationSources"] = account_aggregation_sources

        if organization_aggregation_source is not None:
            props["organizationAggregationSource"] = organization_aggregation_source

        jsii.create(CfnConfigurationAggregator, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationAggregatorName")
    def configuration_aggregator_name(self) -> str:
        return jsii.get(self, "configurationAggregatorName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationAggregatorProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _AccountAggregationSourceProperty(jsii.compat.TypedDict, total=False):
        allAwsRegions: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationAggregator.AccountAggregationSourceProperty.AllAwsRegions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-allawsregions
        """
        awsRegions: typing.List[str]
        """``CfnConfigurationAggregator.AccountAggregationSourceProperty.AwsRegions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-awsregions
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregator.AccountAggregationSourceProperty", jsii_struct_bases=[_AccountAggregationSourceProperty])
    class AccountAggregationSourceProperty(_AccountAggregationSourceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html
        """
        accountIds: typing.List[str]
        """``CfnConfigurationAggregator.AccountAggregationSourceProperty.AccountIds``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-accountaggregationsource.html#cfn-config-configurationaggregator-accountaggregationsource-accountids
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _OrganizationAggregationSourceProperty(jsii.compat.TypedDict, total=False):
        allAwsRegions: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.AllAwsRegions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-allawsregions
        """
        awsRegions: typing.List[str]
        """``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.AwsRegions``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-awsregions
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregator.OrganizationAggregationSourceProperty", jsii_struct_bases=[_OrganizationAggregationSourceProperty])
    class OrganizationAggregationSourceProperty(_OrganizationAggregationSourceProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html
        """
        roleArn: str
        """``CfnConfigurationAggregator.OrganizationAggregationSourceProperty.RoleArn``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationaggregator-organizationaggregationsource.html#cfn-config-configurationaggregator-organizationaggregationsource-rolearn
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigurationAggregatorProps(jsii.compat.TypedDict, total=False):
    accountAggregationSources: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnConfigurationAggregator.AccountAggregationSourceProperty"]]]
    """``AWS::Config::ConfigurationAggregator.AccountAggregationSources``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-accountaggregationsources
    """
    organizationAggregationSource: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationAggregator.OrganizationAggregationSourceProperty"]
    """``AWS::Config::ConfigurationAggregator.OrganizationAggregationSource``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-organizationaggregationsource
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationAggregatorProps", jsii_struct_bases=[_CfnConfigurationAggregatorProps])
class CfnConfigurationAggregatorProps(_CfnConfigurationAggregatorProps):
    """Properties for defining a ``AWS::Config::ConfigurationAggregator``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html
    """
    configurationAggregatorName: str
    """``AWS::Config::ConfigurationAggregator.ConfigurationAggregatorName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationaggregator.html#cfn-config-configurationaggregator-configurationaggregatorname
    """

class CfnConfigurationRecorder(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnConfigurationRecorder"):
    """A CloudFormation ``AWS::Config::ConfigurationRecorder``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html
    cloudformationResource:
        AWS::Config::ConfigurationRecorder
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, role_arn: str, name: typing.Optional[str]=None, recording_group: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["RecordingGroupProperty"]]]=None) -> None:
        """Create a new ``AWS::Config::ConfigurationRecorder``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            roleArn: ``AWS::Config::ConfigurationRecorder.RoleARN``.
            name: ``AWS::Config::ConfigurationRecorder.Name``.
            recordingGroup: ``AWS::Config::ConfigurationRecorder.RecordingGroup``.
        """
        props: CfnConfigurationRecorderProps = {"roleArn": role_arn}

        if name is not None:
            props["name"] = name

        if recording_group is not None:
            props["recordingGroup"] = recording_group

        jsii.create(CfnConfigurationRecorder, self, [scope, id, props])

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
    @jsii.member(jsii_name="configurationRecorderName")
    def configuration_recorder_name(self) -> str:
        return jsii.get(self, "configurationRecorderName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnConfigurationRecorderProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationRecorder.RecordingGroupProperty", jsii_struct_bases=[])
    class RecordingGroupProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html
        """
        allSupported: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationRecorder.RecordingGroupProperty.AllSupported``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-allsupported
        """

        includeGlobalResourceTypes: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnConfigurationRecorder.RecordingGroupProperty.IncludeGlobalResourceTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-includeglobalresourcetypes
        """

        resourceTypes: typing.List[str]
        """``CfnConfigurationRecorder.RecordingGroupProperty.ResourceTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-configurationrecorder-recordinggroup.html#cfn-config-configurationrecorder-recordinggroup-resourcetypes
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnConfigurationRecorderProps(jsii.compat.TypedDict, total=False):
    name: str
    """``AWS::Config::ConfigurationRecorder.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-name
    """
    recordingGroup: typing.Union[aws_cdk.cdk.Token, "CfnConfigurationRecorder.RecordingGroupProperty"]
    """``AWS::Config::ConfigurationRecorder.RecordingGroup``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-recordinggroup
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnConfigurationRecorderProps", jsii_struct_bases=[_CfnConfigurationRecorderProps])
class CfnConfigurationRecorderProps(_CfnConfigurationRecorderProps):
    """Properties for defining a ``AWS::Config::ConfigurationRecorder``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html
    """
    roleArn: str
    """``AWS::Config::ConfigurationRecorder.RoleARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-configurationrecorder.html#cfn-config-configurationrecorder-rolearn
    """

class CfnDeliveryChannel(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-config.CfnDeliveryChannel"):
    """A CloudFormation ``AWS::Config::DeliveryChannel``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html
    cloudformationResource:
        AWS::Config::DeliveryChannel
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, s3_bucket_name: str, config_snapshot_delivery_properties: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional["ConfigSnapshotDeliveryPropertiesProperty"]]]=None, name: typing.Optional[str]=None, s3_key_prefix: typing.Optional[str]=None, sns_topic_arn: typing.Optional[str]=None) -> None:
        """Create a new ``AWS::Config::DeliveryChannel``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            s3BucketName: ``AWS::Config::DeliveryChannel.S3BucketName``.
            configSnapshotDeliveryProperties: ``AWS::Config::DeliveryChannel.ConfigSnapshotDeliveryProperties``.
            name: ``AWS::Config::DeliveryChannel.Name``.
            s3KeyPrefix: ``AWS::Config::DeliveryChannel.S3KeyPrefix``.
            snsTopicArn: ``AWS::Config::DeliveryChannel.SnsTopicARN``.
        """
        props: CfnDeliveryChannelProps = {"s3BucketName": s3_bucket_name}

        if config_snapshot_delivery_properties is not None:
            props["configSnapshotDeliveryProperties"] = config_snapshot_delivery_properties

        if name is not None:
            props["name"] = name

        if s3_key_prefix is not None:
            props["s3KeyPrefix"] = s3_key_prefix

        if sns_topic_arn is not None:
            props["snsTopicArn"] = sns_topic_arn

        jsii.create(CfnDeliveryChannel, self, [scope, id, props])

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
    @jsii.member(jsii_name="deliveryChannelName")
    def delivery_channel_name(self) -> str:
        return jsii.get(self, "deliveryChannelName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnDeliveryChannelProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty", jsii_struct_bases=[])
    class ConfigSnapshotDeliveryPropertiesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-deliverychannel-configsnapshotdeliveryproperties.html
        """
        deliveryFrequency: str
        """``CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty.DeliveryFrequency``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-config-deliverychannel-configsnapshotdeliveryproperties.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties-deliveryfrequency
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnDeliveryChannelProps(jsii.compat.TypedDict, total=False):
    configSnapshotDeliveryProperties: typing.Union[aws_cdk.cdk.Token, "CfnDeliveryChannel.ConfigSnapshotDeliveryPropertiesProperty"]
    """``AWS::Config::DeliveryChannel.ConfigSnapshotDeliveryProperties``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-configsnapshotdeliveryproperties
    """
    name: str
    """``AWS::Config::DeliveryChannel.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-name
    """
    s3KeyPrefix: str
    """``AWS::Config::DeliveryChannel.S3KeyPrefix``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3keyprefix
    """
    snsTopicArn: str
    """``AWS::Config::DeliveryChannel.SnsTopicARN``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-snstopicarn
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-config.CfnDeliveryChannelProps", jsii_struct_bases=[_CfnDeliveryChannelProps])
class CfnDeliveryChannelProps(_CfnDeliveryChannelProps):
    """Properties for defining a ``AWS::Config::DeliveryChannel``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html
    """
    s3BucketName: str
    """``AWS::Config::DeliveryChannel.S3BucketName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-config-deliverychannel.html#cfn-config-deliverychannel-s3bucketname
    """

__all__ = ["CfnAggregationAuthorization", "CfnAggregationAuthorizationProps", "CfnConfigRule", "CfnConfigRuleProps", "CfnConfigurationAggregator", "CfnConfigurationAggregatorProps", "CfnConfigurationRecorder", "CfnConfigurationRecorderProps", "CfnDeliveryChannel", "CfnDeliveryChannelProps", "__jsii_assembly__"]

publication.publish()
