from typing import Dict

from fares.dimension import resolve_slot_dimensions, resolve_user_dimensions
from fares.subscription_offering import SubscriptionOffering


def is_subscription_offering_applicable_for_usage(
    subscription_offering: SubscriptionOffering, slot: Dict
):
    rule_set = subscription_offering.usage_applicability_rules()
    context = resolve_slot_dimensions(slot)
    return rule_set.evaluate(context)


def is_subscription_offering_applicable_for_purchase(
    subscription_offering: SubscriptionOffering, user: Dict
):
    rule_set = subscription_offering.purchase_applicability_rules()
    context = resolve_user_dimensions(user)
    return rule_set.evaluate(context)
