import abc
import datetime
import enum
import typing

import jsii
import jsii.compat
import publication

from jsii.python import classproperty

import aws_cdk.cdk
__jsii_assembly__ = jsii.JSIIAssembly.load("@aws-cdk/aws-budgets", "0.32.0", __name__, "aws-budgets@0.32.0.jsii.tgz")
class CfnBudget(aws_cdk.cdk.CfnResource, metaclass=jsii.JSIIMeta, jsii_type="@aws-cdk/aws-budgets.CfnBudget"):
    """A CloudFormation ``AWS::Budgets::Budget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html
    cloudformationResource:
        AWS::Budgets::Budget
    """
    def __init__(self, scope: aws_cdk.cdk.Construct, id: str, *, budget: typing.Union["BudgetDataProperty", aws_cdk.cdk.Token], notifications_with_subscribers: typing.Optional[typing.Union[typing.Optional[aws_cdk.cdk.Token], typing.Optional[typing.List[typing.Union[aws_cdk.cdk.Token, "NotificationWithSubscribersProperty"]]]]]=None) -> None:
        """Create a new ``AWS::Budgets::Budget``.

        Arguments:
            scope: - scope in which this resource is defined.
            id: - scoped id of the resource.
            props: - resource properties.
            budget: ``AWS::Budgets::Budget.Budget``.
            notificationsWithSubscribers: ``AWS::Budgets::Budget.NotificationsWithSubscribers``.
        """
        props: CfnBudgetProps = {"budget": budget}

        if notifications_with_subscribers is not None:
            props["notificationsWithSubscribers"] = notifications_with_subscribers

        jsii.create(CfnBudget, self, [scope, id, props])

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
    @jsii.member(jsii_name="budgetName")
    def budget_name(self) -> str:
        return jsii.get(self, "budgetName")

    @property
    @jsii.member(jsii_name="propertyOverrides")
    def property_overrides(self) -> "CfnBudgetProps":
        return jsii.get(self, "propertyOverrides")

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _BudgetDataProperty(jsii.compat.TypedDict, total=False):
        budgetLimit: typing.Union[aws_cdk.cdk.Token, "CfnBudget.SpendProperty"]
        """``CfnBudget.BudgetDataProperty.BudgetLimit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-budgetlimit
        """
        budgetName: str
        """``CfnBudget.BudgetDataProperty.BudgetName``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-budgetname
        """
        costFilters: typing.Union[typing.Mapping[typing.Any, typing.Any], aws_cdk.cdk.Token]
        """``CfnBudget.BudgetDataProperty.CostFilters``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-costfilters
        """
        costTypes: typing.Union[aws_cdk.cdk.Token, "CfnBudget.CostTypesProperty"]
        """``CfnBudget.BudgetDataProperty.CostTypes``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-costtypes
        """
        timePeriod: typing.Union[aws_cdk.cdk.Token, "CfnBudget.TimePeriodProperty"]
        """``CfnBudget.BudgetDataProperty.TimePeriod``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-timeperiod
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.BudgetDataProperty", jsii_struct_bases=[_BudgetDataProperty])
    class BudgetDataProperty(_BudgetDataProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html
        """
        budgetType: str
        """``CfnBudget.BudgetDataProperty.BudgetType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-budgettype
        """

        timeUnit: str
        """``CfnBudget.BudgetDataProperty.TimeUnit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-budgetdata.html#cfn-budgets-budget-budgetdata-timeunit
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.CostTypesProperty", jsii_struct_bases=[])
    class CostTypesProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html
        """
        includeCredit: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeCredit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includecredit
        """

        includeDiscount: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeDiscount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includediscount
        """

        includeOtherSubscription: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeOtherSubscription``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includeothersubscription
        """

        includeRecurring: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeRecurring``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includerecurring
        """

        includeRefund: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeRefund``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includerefund
        """

        includeSubscription: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeSubscription``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includesubscription
        """

        includeSupport: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeSupport``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includesupport
        """

        includeTax: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeTax``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includetax
        """

        includeUpfront: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.IncludeUpfront``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-includeupfront
        """

        useAmortized: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.UseAmortized``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-useamortized
        """

        useBlended: typing.Union[bool, aws_cdk.cdk.Token]
        """``CfnBudget.CostTypesProperty.UseBlended``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-costtypes.html#cfn-budgets-budget-costtypes-useblended
        """

    @jsii.data_type_optionals(jsii_struct_bases=[])
    class _NotificationProperty(jsii.compat.TypedDict, total=False):
        thresholdType: str
        """``CfnBudget.NotificationProperty.ThresholdType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-thresholdtype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.NotificationProperty", jsii_struct_bases=[_NotificationProperty])
    class NotificationProperty(_NotificationProperty):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html
        """
        comparisonOperator: str
        """``CfnBudget.NotificationProperty.ComparisonOperator``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-comparisonoperator
        """

        notificationType: str
        """``CfnBudget.NotificationProperty.NotificationType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-notificationtype
        """

        threshold: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnBudget.NotificationProperty.Threshold``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notification.html#cfn-budgets-budget-notification-threshold
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.NotificationWithSubscribersProperty", jsii_struct_bases=[])
    class NotificationWithSubscribersProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notificationwithsubscribers.html
        """
        notification: typing.Union[aws_cdk.cdk.Token, "CfnBudget.NotificationProperty"]
        """``CfnBudget.NotificationWithSubscribersProperty.Notification``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notificationwithsubscribers.html#cfn-budgets-budget-notificationwithsubscribers-notification
        """

        subscribers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBudget.SubscriberProperty"]]]
        """``CfnBudget.NotificationWithSubscribersProperty.Subscribers``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-notificationwithsubscribers.html#cfn-budgets-budget-notificationwithsubscribers-subscribers
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.SpendProperty", jsii_struct_bases=[])
    class SpendProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-spend.html
        """
        amount: typing.Union[jsii.Number, aws_cdk.cdk.Token]
        """``CfnBudget.SpendProperty.Amount``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-spend.html#cfn-budgets-budget-spend-amount
        """

        unit: str
        """``CfnBudget.SpendProperty.Unit``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-spend.html#cfn-budgets-budget-spend-unit
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.SubscriberProperty", jsii_struct_bases=[])
    class SubscriberProperty(jsii.compat.TypedDict):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-subscriber.html
        """
        address: str
        """``CfnBudget.SubscriberProperty.Address``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-subscriber.html#cfn-budgets-budget-subscriber-address
        """

        subscriptionType: str
        """``CfnBudget.SubscriberProperty.SubscriptionType``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-subscriber.html#cfn-budgets-budget-subscriber-subscriptiontype
        """

    @jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudget.TimePeriodProperty", jsii_struct_bases=[])
    class TimePeriodProperty(jsii.compat.TypedDict, total=False):
        """
        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-timeperiod.html
        """
        end: str
        """``CfnBudget.TimePeriodProperty.End``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-timeperiod.html#cfn-budgets-budget-timeperiod-end
        """

        start: str
        """``CfnBudget.TimePeriodProperty.Start``.

        See:
            http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-budgets-budget-timeperiod.html#cfn-budgets-budget-timeperiod-start
        """


@jsii.data_type_optionals(jsii_struct_bases=[])
class _CfnBudgetProps(jsii.compat.TypedDict, total=False):
    notificationsWithSubscribers: typing.Union[aws_cdk.cdk.Token, typing.List[typing.Union[aws_cdk.cdk.Token, "CfnBudget.NotificationWithSubscribersProperty"]]]
    """``AWS::Budgets::Budget.NotificationsWithSubscribers``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html#cfn-budgets-budget-notificationswithsubscribers
    """

@jsii.data_type(jsii_type="@aws-cdk/aws-budgets.CfnBudgetProps", jsii_struct_bases=[_CfnBudgetProps])
class CfnBudgetProps(_CfnBudgetProps):
    """Properties for defining a ``AWS::Budgets::Budget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html
    """
    budget: typing.Union["CfnBudget.BudgetDataProperty", aws_cdk.cdk.Token]
    """``AWS::Budgets::Budget.Budget``.

    See:
        http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-budgets-budget.html#cfn-budgets-budget-budget
    """

__all__ = ["CfnBudget", "CfnBudgetProps", "__jsii_assembly__"]

publication.publish()
