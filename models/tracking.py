"""Tracking and shipment models."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class ShipmentStatus(Enum):
    """Status of shipment tracking."""

    LABEL_CREATED = "label_created"
    PICKED_UP = "picked_up"
    IN_TRANSIT = "in_transit"
    OUT_FOR_DELIVERY = "out_for_delivery"
    DELIVERED = "delivered"
    EXCEPTION = "exception"


@dataclass
class TrackingInfo:
    """Represents tracking information for a return shipment."""

    tracking_number: str
    carrier: str
    status: ShipmentStatus
    last_update: datetime
    estimated_delivery: Optional[datetime] = None
    current_location: Optional[str] = None

    def get_status_message(self) -> str:
        """Get a human-readable status message."""
        status_messages = {
            ShipmentStatus.LABEL_CREATED: "Your return label has been created. Please drop off your package.",
            ShipmentStatus.PICKED_UP: "Your return package has been picked up by the carrier.",
            ShipmentStatus.IN_TRANSIT: "Your return is in transit to our facility.",
            ShipmentStatus.OUT_FOR_DELIVERY: "Your return is out for delivery to our warehouse.",
            ShipmentStatus.DELIVERED: "Your return has been delivered. Refund processing will begin shortly.",
            ShipmentStatus.EXCEPTION: "There's an issue with your return shipment. Please contact support.",
        }
        return status_messages.get(self.status, "Status unknown")
