"""Return request models and enums."""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class ReturnReason(Enum):
    """Possible reasons for returning an item."""

    DAMAGED = "damaged"
    WRONG_ITEM = "wrong_item"
    SIZE_ISSUE = "size_issue"
    BUYER_REMORSE = "buyer_remorse"
    NOT_AS_DESCRIBED = "not_as_described"
    DEFECTIVE = "defective"
    OTHER = "other"


class ReturnStatus(Enum):
    """Status of a return request."""

    INITIATED = "initiated"
    LABEL_GENERATED = "label_generated"
    IN_TRANSIT = "in_transit"
    RECEIVED = "received"
    REFUND_PENDING = "refund_pending"
    REFUND_PROCESSED = "refund_processed"
    REJECTED = "rejected"
    DISPUTED = "disputed"


@dataclass
class ReturnRequest:
    """Represents a product return request."""

    return_id: str
    order_id: str
    user_id: str
    item_id: str
    reason: ReturnReason
    status: ReturnStatus = ReturnStatus.INITIATED
    created_at: datetime = field(default_factory=datetime.now)
    refund_amount: float = 0.0
    notes: str = ""
    label_url: Optional[str] = None
    qr_code_url: Optional[str] = None
    tracking_number: Optional[str] = None
    fraud_risk_score: float = 0.0

    def generate_return_id(self) -> str:
        """Generate a unique return ID."""
        timestamp = int(self.created_at.timestamp())
        return f"RET-{self.order_id}-{timestamp}"

    def is_high_risk(self, threshold: float = 0.7) -> bool:
        """Check if return has high fraud risk."""
        return self.fraud_risk_score >= threshold
