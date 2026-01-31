"""Order and OrderItem models."""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class OrderItem:
    """Represents an item in an order."""

    item_id: str
    product_name: str
    price: float
    quantity: int = 1
    category: str = "General"

    @property
    def total_price(self) -> float:
        """Calculate total price for this item."""
        return self.price * self.quantity


@dataclass
class Order:
    """Represents a customer order."""

    order_id: str
    user_id: str
    items: List[OrderItem]
    order_date: datetime
    total_amount: float
    status: str = "delivered"

    def __post_init__(self):
        """Calculate total if not provided."""
        if self.total_amount == 0:
            self.total_amount = sum(item.total_price for item in self.items)

    def get_item_by_id(self, item_id: str) -> OrderItem | None:
        """Find an item in the order by ID."""
        for item in self.items:
            if item.item_id == item_id:
                return item
        return None

    def is_returnable(self, days: int = 30) -> bool:
        """Check if order is within return window."""
        days_since_order = (datetime.now() - self.order_date).days
        return days_since_order <= days
