from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from rule_engine.operator import In, Equals
from rule_engine.rule import RuleSet, Rule


@dataclass(frozen=True)
class Applicability:
    origin_cluster_id: str
    destination_cluster_id: str
    session: str


class SubscriptionType(Enum):
    TRIAL = "TRIAL"
    STANDARD = "STANDARD"


@dataclass
class SubscriptionOffering:
    id: str
    name: str
    rides: int
    currency: str
    validity_in_days: int
    is_carry_forward: bool
    activation_date: datetime
    deactivation_date: datetime
    zone_id: str
    amount: int
    subscription_type: SubscriptionType
    applicability: [Applicability]
    created_at: datetime

    @classmethod
    def from_json(cls, subscription_offering):
        # TODO : This was done to allow older subscriptions to run according to previous system.Remove it.
        def _applicability_rules(subscription_offering):
            applicability_rules = []

            for app in subscription_offering["applicability"]:
                applicability_rules.append(
                    Applicability(
                        app["origin_cluster_id"],
                        app["destination_cluster_id"],
                        "MORNING",
                    )
                )
                applicability_rules.append(
                    Applicability(
                        app["origin_cluster_id"],
                        app["destination_cluster_id"],
                        "EVENING",
                    )
                )

            return applicability_rules

        return SubscriptionOffering(
            id=subscription_offering["id"],
            name=subscription_offering["name"],
            rides=subscription_offering["rides"],
            currency=subscription_offering["currency"],
            validity_in_days=subscription_offering["validity_in_days"],
            is_carry_forward=subscription_offering["is_carry_forward"],
            activation_date=subscription_offering["activation_date"],
            deactivation_date=subscription_offering["deactivation_date"],
            zone_id=subscription_offering["zone_id"],
            amount=subscription_offering["amount"],
            subscription_type=SubscriptionType(
                subscription_offering["subscription_type"]
            ),
            applicability=_applicability_rules(subscription_offering),
            created_at=datetime.fromisoformat(subscription_offering["created_at"]),
        )

    def usage_applicability_rules(self) -> RuleSet:
        return RuleSet(
            [
                Rule(
                    "slot.od_cluster_session",
                    In(),
                    [
                        (app.origin_cluster_id, app.destination_cluster_id, app.session)
                        for app in self.applicability
                    ],
                )
            ]
        )

    def purchase_applicability_rules(self) -> RuleSet:

        if SubscriptionType.STANDARD == self.subscription_type:
            return RuleSet([])

        return RuleSet([Rule("user.pass_purchase_count", Equals(), 0)])
