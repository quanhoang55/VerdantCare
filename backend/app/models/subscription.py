# ==========================================================================
# PURPOSE: SUBSCRIPTION MODEL
# ==========================================================================
# IMPORTS & MODULE LOADING
# ==========================================================================

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel

# ==========================================================================
# CLASSES / DATA STRUCTURE: Plan Tier
# ==========================================================================


class PlanTier(StrEnum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"


class SubscriptionStatus(StrEnum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    TRIALING = "trialing"
    CANCELED = "canceled"
    PAST_DUE = "past_due"


# ==========================================================================
# MAIN MODEL
# ==========================================================================
class Subscription(BaseModel):
    user_id: str
    plan: PlanTier = PlanTier.FREE
    status: SubscriptionStatus = SubscriptionStatus.INACTIVE
    current_period_end: datetime | None = None

    def is_entitled(self) -> bool:
        """True when the user has an active or trialing paid plan."""
        return self.plan != PlanTier.FREE and self.status in {
            SubscriptionStatus.ACTIVE,
            SubscriptionStatus.TRIALING,
        }
