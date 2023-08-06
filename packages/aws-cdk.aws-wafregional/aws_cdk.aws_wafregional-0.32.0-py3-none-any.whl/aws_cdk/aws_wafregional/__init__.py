import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-wafregional", "0.32.0", __name__, "aws-wafregional@0.32.0.jsii.tgz")
class CfnByteMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSet"):
    """A CloudFormation ``AWS::WAFRegional::ByteMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html
    cloudformationResource:
        AWS::WAFRegional::ByteMatchSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, byte_match_tuples: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union["ByteMatchTupleProperty", aws_cdk.cdk.Token]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::ByteMatchSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAFRegional::ByteMatchSet.Name``.
            byteMatchTuples: ``AWS::WAFRegional::ByteMatchSet.ByteMatchTuples``.
        """
        props: CfnByteMatchSetProps = {"name": name}

        if byte_match_tuples is not None:
            props["byteMatchTuples"] = byte_match_tuples

        jsii.create(CfnByteMatchSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="byteMatchSetId")
    def byte_match_set_id(self) -> str:
        return jsii.get(self, "byteMatchSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnByteMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _ByteMatchTupleProperty(jsii.compat.TypedDict, total=False):
        targetString: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.TargetString``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-targetstring
        """
        targetStringBase64: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.TargetStringBase64``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-targetstringbase64
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSet.ByteMatchTupleProperty", jsii_struct_bases=[_ByteMatchTupleProperty])
    class ByteMatchTupleProperty(_ByteMatchTupleProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html
        """
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnByteMatchSet.FieldToMatchProperty"]
        """``CfnByteMatchSet.ByteMatchTupleProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-fieldtomatch
        """

        positionalConstraint: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.PositionalConstraint``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-positionalconstraint
        """

        textTransformation: str
        """``CfnByteMatchSet.ByteMatchTupleProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-bytematchtuple.html#cfn-wafregional-bytematchset-bytematchtuple-texttransformation
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnByteMatchSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html#cfn-wafregional-bytematchset-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html
        """
        type: str
        """``CfnByteMatchSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-bytematchset-fieldtomatch.html#cfn-wafregional-bytematchset-fieldtomatch-type
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnByteMatchSetProps(jsii.compat.TypedDict, total=False):
    byteMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union["CfnByteMatchSet.ByteMatchTupleProperty", aws_cdk.cdk.Token]]]
    """``AWS::WAFRegional::ByteMatchSet.ByteMatchTuples``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-bytematchtuples
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnByteMatchSetProps", jsii_struct_bases=[_CfnByteMatchSetProps])
class CfnByteMatchSetProps(_CfnByteMatchSetProps):
    """Properties for defining a ``AWS::WAFRegional::ByteMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html
    """
    name: str
    """``AWS::WAFRegional::ByteMatchSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-bytematchset.html#cfn-wafregional-bytematchset-name
    """

class CfnIPSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnIPSet"):
    """A CloudFormation ``AWS::WAFRegional::IPSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html
    cloudformationResource:
        AWS::WAFRegional::IPSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, ip_set_descriptors: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "IPSetDescriptorProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::IPSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAFRegional::IPSet.Name``.
            ipSetDescriptors: ``AWS::WAFRegional::IPSet.IPSetDescriptors``.
        """
        props: CfnIPSetProps = {"name": name}

        if ip_set_descriptors is not None:
            props["ipSetDescriptors"] = ip_set_descriptors

        jsii.create(CfnIPSet, self, [scope, id, props])

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
    @jsii.member(jsii_name="ipSetId")
    def ip_set_id(self) -> str:
        return jsii.get(self, "ipSetId")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnIPSetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.interface(jsii_type="@aws-cdk/aws-wafregional.CfnIPSet.IPSetDescriptorProperty")
    class IPSetDescriptorProperty(jsii.compat.Protocol):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html
        """
        @staticmethod
        def __jsii_proxy_class__():
            return _IPSetDescriptorPropertyProxy

        @property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Type``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-type
            """
            ...

        @property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Value``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-value
            """
            ...


    class _IPSetDescriptorPropertyProxy():
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html
        """
        __jsii_type__ = "@aws-cdk/aws-wafregional.CfnIPSet.IPSetDescriptorProperty"
        @property
        @jsii.member(jsii_name="type")
        def type(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Type``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-type
            """
            return jsii.get(self, "type")

        @property
        @jsii.member(jsii_name="value")
        def value(self) -> str:
            """``CfnIPSet.IPSetDescriptorProperty.Value``.

            See:
                http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-ipset-ipsetdescriptor.html#cfn-wafregional-ipset-ipsetdescriptor-value
            """
            return jsii.get(self, "value")



@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnIPSetProps(jsii.compat.TypedDict, total=False):
    ipSetDescriptors: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnIPSet.IPSetDescriptorProperty"]]]
    """``AWS::WAFRegional::IPSet.IPSetDescriptors``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-ipsetdescriptors
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnIPSetProps", jsii_struct_bases=[_CfnIPSetProps])
class CfnIPSetProps(_CfnIPSetProps):
    """Properties for defining a ``AWS::WAFRegional::IPSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html
    """
    name: str
    """``AWS::WAFRegional::IPSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-ipset.html#cfn-wafregional-ipset-name
    """

class CfnRule(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnRule"):
    """A CloudFormation ``AWS::WAFRegional::Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html
    cloudformationResource:
        AWS::WAFRegional::Rule
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, metric_name: str, name: str, predicates: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "PredicateProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::Rule``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            metricName: ``AWS::WAFRegional::Rule.MetricName``.
            name: ``AWS::WAFRegional::Rule.Name``.
            predicates: ``AWS::WAFRegional::Rule.Predicates``.
        """
        props: CfnRuleProps = {"metricName": metric_name, "name": name}

        if predicates is not None:
            props["predicates"] = predicates

        jsii.create(CfnRule, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnRuleProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="ruleId")
    def rule_id(self) -> str:
        return jsii.get(self, "ruleId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnRule.PredicateProperty", jsii_struct_bases=[])
    class PredicateProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html
        """
        dataId: str
        """``CfnRule.PredicateProperty.DataId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-dataid
        """

        negated: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnRule.PredicateProperty.Negated``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-negated
        """

        type: str
        """``CfnRule.PredicateProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-rule-predicate.html#cfn-wafregional-rule-predicate-type
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnRuleProps(jsii.compat.TypedDict, total=False):
    predicates: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnRule.PredicateProperty"]]]
    """``AWS::WAFRegional::Rule.Predicates``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-predicates
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnRuleProps", jsii_struct_bases=[_CfnRuleProps])
class CfnRuleProps(_CfnRuleProps):
    """Properties for defining a ``AWS::WAFRegional::Rule``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html
    """
    metricName: str
    """``AWS::WAFRegional::Rule.MetricName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-metricname
    """

    name: str
    """``AWS::WAFRegional::Rule.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-rule.html#cfn-wafregional-rule-name
    """

class CfnSizeConstraintSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSet"):
    """A CloudFormation ``AWS::WAFRegional::SizeConstraintSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html
    cloudformationResource:
        AWS::WAFRegional::SizeConstraintSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, size_constraints: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "SizeConstraintProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::SizeConstraintSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAFRegional::SizeConstraintSet.Name``.
            sizeConstraints: ``AWS::WAFRegional::SizeConstraintSet.SizeConstraints``.
        """
        props: CfnSizeConstraintSetProps = {"name": name}

        if size_constraints is not None:
            props["sizeConstraints"] = size_constraints

        jsii.create(CfnSizeConstraintSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSizeConstraintSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="sizeConstraintSetId")
    def size_constraint_set_id(self) -> str:
        return jsii.get(self, "sizeConstraintSetId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnSizeConstraintSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html#cfn-wafregional-sizeconstraintset-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html
        """
        type: str
        """``CfnSizeConstraintSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-fieldtomatch.html#cfn-wafregional-sizeconstraintset-fieldtomatch-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSet.SizeConstraintProperty", jsii_struct_bases=[])
    class SizeConstraintProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html
        """
        comparisonOperator: str
        """``CfnSizeConstraintSet.SizeConstraintProperty.ComparisonOperator``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-comparisonoperator
        """

        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnSizeConstraintSet.FieldToMatchProperty"]
        """``CfnSizeConstraintSet.SizeConstraintProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-fieldtomatch
        """

        size: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnSizeConstraintSet.SizeConstraintProperty.Size``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-size
        """

        textTransformation: str
        """``CfnSizeConstraintSet.SizeConstraintProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sizeconstraintset-sizeconstraint.html#cfn-wafregional-sizeconstraintset-sizeconstraint-texttransformation
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSizeConstraintSetProps(jsii.compat.TypedDict, total=False):
    sizeConstraints: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSizeConstraintSet.SizeConstraintProperty"]]]
    """``AWS::WAFRegional::SizeConstraintSet.SizeConstraints``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-sizeconstraints
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnSizeConstraintSetProps", jsii_struct_bases=[_CfnSizeConstraintSetProps])
class CfnSizeConstraintSetProps(_CfnSizeConstraintSetProps):
    """Properties for defining a ``AWS::WAFRegional::SizeConstraintSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html
    """
    name: str
    """``AWS::WAFRegional::SizeConstraintSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sizeconstraintset.html#cfn-wafregional-sizeconstraintset-name
    """

class CfnSqlInjectionMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSet"):
    """A CloudFormation ``AWS::WAFRegional::SqlInjectionMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html
    cloudformationResource:
        AWS::WAFRegional::SqlInjectionMatchSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, sql_injection_match_tuples: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "SqlInjectionMatchTupleProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::SqlInjectionMatchSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAFRegional::SqlInjectionMatchSet.Name``.
            sqlInjectionMatchTuples: ``AWS::WAFRegional::SqlInjectionMatchSet.SqlInjectionMatchTuples``.
        """
        props: CfnSqlInjectionMatchSetProps = {"name": name}

        if sql_injection_match_tuples is not None:
            props["sqlInjectionMatchTuples"] = sql_injection_match_tuples

        jsii.create(CfnSqlInjectionMatchSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnSqlInjectionMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="sqlInjectionMatchSetId")
    def sql_injection_match_set_id(self) -> str:
        return jsii.get(self, "sqlInjectionMatchSetId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnSqlInjectionMatchSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html#cfn-wafregional-sqlinjectionmatchset-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html
        """
        type: str
        """``CfnSqlInjectionMatchSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-fieldtomatch.html#cfn-wafregional-sqlinjectionmatchset-fieldtomatch-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty", jsii_struct_bases=[])
    class SqlInjectionMatchTupleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html
        """
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnSqlInjectionMatchSet.FieldToMatchProperty"]
        """``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple-fieldtomatch
        """

        textTransformation: str
        """``CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuple-texttransformation
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnSqlInjectionMatchSetProps(jsii.compat.TypedDict, total=False):
    sqlInjectionMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnSqlInjectionMatchSet.SqlInjectionMatchTupleProperty"]]]
    """``AWS::WAFRegional::SqlInjectionMatchSet.SqlInjectionMatchTuples``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-sqlinjectionmatchtuples
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnSqlInjectionMatchSetProps", jsii_struct_bases=[_CfnSqlInjectionMatchSetProps])
class CfnSqlInjectionMatchSetProps(_CfnSqlInjectionMatchSetProps):
    """Properties for defining a ``AWS::WAFRegional::SqlInjectionMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html
    """
    name: str
    """``AWS::WAFRegional::SqlInjectionMatchSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-sqlinjectionmatchset.html#cfn-wafregional-sqlinjectionmatchset-name
    """

class CfnWebACL(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnWebACL"):
    """A CloudFormation ``AWS::WAFRegional::WebACL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html
    cloudformationResource:
        AWS::WAFRegional::WebACL
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, default_action: typing.Union[aws_cdk.cdk.Token, "ActionProperty"], metric_name: str, name: str, rules: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "RuleProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::WebACL``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            defaultAction: ``AWS::WAFRegional::WebACL.DefaultAction``.
            metricName: ``AWS::WAFRegional::WebACL.MetricName``.
            name: ``AWS::WAFRegional::WebACL.Name``.
            rules: ``AWS::WAFRegional::WebACL.Rules``.
        """
        props: CfnWebACLProps = {"defaultAction": default_action, "metricName": metric_name, "name": name}

        if rules is not None:
            props["rules"] = rules

        jsii.create(CfnWebACL, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnWebACLProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="webAclId")
    def web_acl_id(self) -> str:
        return jsii.get(self, "webAclId")

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnWebACL.ActionProperty", jsii_struct_bases=[])
    class ActionProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-action.html
        """
        type: str
        """``CfnWebACL.ActionProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-action.html#cfn-wafregional-webacl-action-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnWebACL.RuleProperty", jsii_struct_bases=[])
    class RuleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html
        """
        action: typing.Union[aws_cdk.cdk.Token, "CfnWebACL.ActionProperty"]
        """``CfnWebACL.RuleProperty.Action``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-action
        """

        priority: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnWebACL.RuleProperty.Priority``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-priority
        """

        ruleId: str
        """``CfnWebACL.RuleProperty.RuleId``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-webacl-rule.html#cfn-wafregional-webacl-rule-ruleid
        """


class CfnWebACLAssociation(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnWebACLAssociation"):
    """A CloudFormation ``AWS::WAFRegional::WebACLAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html
    cloudformationResource:
        AWS::WAFRegional::WebACLAssociation
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, resource_arn: str, web_acl_id: str) -> None:
        """Create a new ``AWS::WAFRegional::WebACLAssociation``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            resourceArn: ``AWS::WAFRegional::WebACLAssociation.ResourceArn``.
            webAclId: ``AWS::WAFRegional::WebACLAssociation.WebACLId``.
        """
        props: CfnWebACLAssociationProps = {"resourceArn": resource_arn, "webAclId": web_acl_id}

        jsii.create(CfnWebACLAssociation, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnWebACLAssociationProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="webAclAssociationId")
    def web_acl_association_id(self) -> str:
        return jsii.get(self, "webAclAssociationId")


@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnWebACLAssociationProps", jsii_struct_bases=[])
class CfnWebACLAssociationProps(jsii.compat.TypedDict):
    """Properties for defining a ``AWS::WAFRegional::WebACLAssociation``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html
    """
    resourceArn: str
    """``AWS::WAFRegional::WebACLAssociation.ResourceArn``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-resourcearn
    """

    webAclId: str
    """``AWS::WAFRegional::WebACLAssociation.WebACLId``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webaclassociation.html#cfn-wafregional-webaclassociation-webaclid
    """

@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnWebACLProps(jsii.compat.TypedDict, total=False):
    rules: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnWebACL.RuleProperty"]]]
    """``AWS::WAFRegional::WebACL.Rules``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-rules
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnWebACLProps", jsii_struct_bases=[_CfnWebACLProps])
class CfnWebACLProps(_CfnWebACLProps):
    """Properties for defining a ``AWS::WAFRegional::WebACL``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html
    """
    defaultAction: typing.Union[aws_cdk.cdk.Token, "CfnWebACL.ActionProperty"]
    """``AWS::WAFRegional::WebACL.DefaultAction``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-defaultaction
    """

    metricName: str
    """``AWS::WAFRegional::WebACL.MetricName``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-metricname
    """

    name: str
    """``AWS::WAFRegional::WebACL.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-webacl.html#cfn-wafregional-webacl-name
    """

class CfnXssMatchSet(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSet"):
    """A CloudFormation ``AWS::WAFRegional::XssMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html
    cloudformationResource:
        AWS::WAFRegional::XssMatchSet
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, name: str, xss_match_tuples: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "XssMatchTupleProperty"]]]]]=None) -> None:
        """Create a new ``AWS::WAFRegional::XssMatchSet``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            name: ``AWS::WAFRegional::XssMatchSet.Name``.
            xssMatchTuples: ``AWS::WAFRegional::XssMatchSet.XssMatchTuples``.
        """
        props: CfnXssMatchSetProps = {"name": name}

        if xss_match_tuples is not None:
            props["xssMatchTuples"] = xss_match_tuples

        jsii.create(CfnXssMatchSet, self, [scope, id, props])

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
    def property_overrides(self) -> "CfnXssMatchSetProps":
        return jsii.get(self, "propertyOverrides")

    @property
    @jsii.member(jsii_name="xssMatchSetId")
    def xss_match_set_id(self) -> str:
        return jsii.get(self, "xssMatchSetId")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _FieldToMatchProperty(jsii.compat.TypedDict, total=False):
        data: str
        """``CfnXssMatchSet.FieldToMatchProperty.Data``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html#cfn-wafregional-xssmatchset-fieldtomatch-data
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSet.FieldToMatchProperty", jsii_struct_bases=[_FieldToMatchProperty])
    class FieldToMatchProperty(_FieldToMatchProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html
        """
        type: str
        """``CfnXssMatchSet.FieldToMatchProperty.Type``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-fieldtomatch.html#cfn-wafregional-xssmatchset-fieldtomatch-type
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSet.XssMatchTupleProperty", jsii_struct_bases=[])
    class XssMatchTupleProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html
        """
        fieldToMatch: typing.Union[aws_cdk.cdk.Token, "CfnXssMatchSet.FieldToMatchProperty"]
        """``CfnXssMatchSet.XssMatchTupleProperty.FieldToMatch``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html#cfn-wafregional-xssmatchset-xssmatchtuple-fieldtomatch
        """

        textTransformation: str
        """``CfnXssMatchSet.XssMatchTupleProperty.TextTransformation``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-wafregional-xssmatchset-xssmatchtuple.html#cfn-wafregional-xssmatchset-xssmatchtuple-texttransformation
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnXssMatchSetProps(jsii.compat.TypedDict, total=False):
    xssMatchTuples: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnXssMatchSet.XssMatchTupleProperty"]]]
    """``AWS::WAFRegional::XssMatchSet.XssMatchTuples``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-xssmatchtuples
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-wafregional.CfnXssMatchSetProps", jsii_struct_bases=[_CfnXssMatchSetProps])
class CfnXssMatchSetProps(_CfnXssMatchSetProps):
    """Properties for defining a ``AWS::WAFRegional::XssMatchSet``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html
    """
    name: str
    """``AWS::WAFRegional::XssMatchSet.Name``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-wafregional-xssmatchset.html#cfn-wafregional-xssmatchset-name
    """

__all__ = ["CfnByteMatchSet", "CfnByteMatchSetProps", "CfnIPSet", "CfnIPSetProps", "CfnRule", "CfnRuleProps", "CfnSizeConstraintSet", "CfnSizeConstraintSetProps", "CfnSqlInjectionMatchSet", "CfnSqlInjectionMatchSetProps", "CfnWebACL", "CfnWebACLAssociation", "CfnWebACLAssociationProps", "CfnWebACLProps", "CfnXssMatchSet", "CfnXssMatchSetProps", "__jsii_assembly__"]

publication.publish()
