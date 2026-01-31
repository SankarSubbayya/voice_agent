"""Mock database implementation for testing and demo purposes."""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

from models.order import Order, OrderItem
from models.user import User
from models.return_request import ReturnRequest, ReturnStatus
from models.tracking import TrackingInfo, ShipmentStatus


class MockDatabase:
    """Mock database for storing users, orders, returns, and tracking info."""

    def __init__(self):
        """Initialize mock database with sample data."""
        self.users: Dict[str, User] = {}
        self.orders: Dict[str, Order] = {}
        self.returns: Dict[str, ReturnRequest] = {}
        self.tracking: Dict[str, TrackingInfo] = {}
        self._seed_data()

    def _seed_data(self):
        """Seed database with sample data."""
        # Create sample users
        users_data = [
            User(
                user_id="USER001",
                name="John Doe",
                email="john.doe@email.com",
                phone="+1-555-0001",
                address="123 Main St, San Francisco, CA 94102",
                return_count=2,
                account_age_days=365,
            ),
            User(
                user_id="USER002",
                name="Jane Smith",
                email="jane.smith@email.com",
                phone="+1-555-0002",
                address="456 Oak Ave, Los Angeles, CA 90001",
                return_count=0,
                account_age_days=180,
            ),
        ]
        for user in users_data:
            self.users[user.user_id] = user

        # Create sample orders
        orders_data = [
            Order(
                order_id="ORD001",
                user_id="USER001",
                items=[
                    OrderItem(
                        item_id="ITEM001",
                        product_name="Wireless Headphones",
                        price=149.99,
                        quantity=1,
                        category="Electronics",
                    ),
                    OrderItem(
                        item_id="ITEM002",
                        product_name="Phone Case",
                        price=19.99,
                        quantity=2,
                        category="Accessories",
                    ),
                ],
                order_date=datetime.now() - timedelta(days=7),
                total_amount=189.97,
                status="delivered",
            ),
            Order(
                order_id="ORD002",
                user_id="USER001",
                items=[
                    OrderItem(
                        item_id="ITEM003",
                        product_name="Running Shoes",
                        price=89.99,
                        quantity=1,
                        category="Footwear",
                    ),
                ],
                order_date=datetime.now() - timedelta(days=14),
                total_amount=89.99,
                status="delivered",
            ),
            Order(
                order_id="ORD003",
                user_id="USER002",
                items=[
                    OrderItem(
                        item_id="ITEM004",
                        product_name="Coffee Maker",
                        price=79.99,
                        quantity=1,
                        category="Home & Kitchen",
                    ),
                ],
                order_date=datetime.now() - timedelta(days=3),
                total_amount=79.99,
                status="delivered",
            ),
        ]
        for order in orders_data:
            self.orders[order.order_id] = order

    # User operations
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by ID."""
        return self.users.get(user_id)

    def get_user_by_phone(self, phone: str) -> Optional[User]:
        """Retrieve a user by phone number."""
        for user in self.users.values():
            if user.phone == phone:
                return user
        return None

    # Order operations
    def get_order(self, order_id: str) -> Optional[Order]:
        """Retrieve an order by ID."""
        return self.orders.get(order_id)

    def get_user_orders(self, user_id: str, limit: int = 10) -> List[Order]:
        """Retrieve recent orders for a user."""
        user_orders = [
            order for order in self.orders.values() if order.user_id == user_id
        ]
        # Sort by date, most recent first
        user_orders.sort(key=lambda x: x.order_date, reverse=True)
        return user_orders[:limit]

    # Return operations
    def create_return(self, return_request: ReturnRequest) -> ReturnRequest:
        """Create a new return request."""
        self.returns[return_request.return_id] = return_request
        # Update user return count
        user = self.get_user(return_request.user_id)
        if user:
            user.return_count += 1
        return return_request

    def get_return(self, return_id: str) -> Optional[ReturnRequest]:
        """Retrieve a return request by ID."""
        return self.returns.get(return_id)

    def update_return_status(
        self, return_id: str, status: ReturnStatus
    ) -> Optional[ReturnRequest]:
        """Update the status of a return request."""
        return_request = self.returns.get(return_id)
        if return_request:
            return_request.status = status
        return return_request

    def get_user_returns(self, user_id: str) -> List[ReturnRequest]:
        """Retrieve all returns for a user."""
        return [ret for ret in self.returns.values() if ret.user_id == user_id]

    # Tracking operations
    def create_tracking(self, tracking_info: TrackingInfo) -> TrackingInfo:
        """Create tracking information."""
        self.tracking[tracking_info.tracking_number] = tracking_info
        return tracking_info

    def get_tracking(self, tracking_number: str) -> Optional[TrackingInfo]:
        """Retrieve tracking information."""
        return self.tracking.get(tracking_number)

    def update_tracking_status(
        self, tracking_number: str, status: ShipmentStatus, location: Optional[str] = None
    ) -> Optional[TrackingInfo]:
        """Update tracking status."""
        tracking_info = self.tracking.get(tracking_number)
        if tracking_info:
            tracking_info.status = status
            tracking_info.last_update = datetime.now()
            if location:
                tracking_info.current_location = location
        return tracking_info

    def get_return_by_tracking(self, tracking_number: str) -> Optional[ReturnRequest]:
        """Find a return by tracking number."""
        for return_req in self.returns.values():
            if return_req.tracking_number == tracking_number:
                return return_req
        return None
