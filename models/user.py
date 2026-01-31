"""User model."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """Represents a customer user."""

    user_id: str
    name: str
    email: str
    phone: str
    address: Optional[str] = None
    return_count: int = 0
    account_age_days: int = 0

    def get_fraud_risk_multiplier(self) -> float:
        """Calculate fraud risk multiplier based on user history."""
        # New accounts with many returns are higher risk
        if self.account_age_days < 90 and self.return_count > 5:
            return 1.5
        elif self.return_count > 20:
            return 1.3
        elif self.return_count > 10:
            return 1.1
        return 1.0
