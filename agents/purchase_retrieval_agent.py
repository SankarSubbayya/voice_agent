"""Purchase Retrieval Agent - Fetches and presents user's recent orders."""

from typing import Dict, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentResponse
from database.mock_db import MockDatabase


class PurchaseRetrievalAgent(BaseAgent):
    """Fetches user's recent purchases and helps them select items to return."""

    def __init__(self, database: MockDatabase):
        """Initialize the Purchase Retrieval Agent."""
        super().__init__("PurchaseRetrievalAgent")
        self.db = database

    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Fetch and present user's recent orders.

        Args:
            user_input: The user's voice input
            context: Conversation context with user_id

        Returns:
            AgentResponse with order information
        """
        user_id = context.get("user_id")

        if not user_id:
            return AgentResponse(
                success=False,
                message="I need to identify you first. Can you provide your phone number or order ID?",
                requires_clarification=True,
            )

        # Check if user is selecting an item
        if "selected_order_id" in context and "selected_item_id" not in context:
            return self._handle_item_selection(user_input, context)

        # Check if user is selecting an order from multiple orders
        if context.get("awaiting_order_selection"):
            orders = context.get("available_orders", [])
            selected_order = self._select_order_from_input(user_input, orders)
            if selected_order:
                context["selected_order_id"] = selected_order.order_id
                context["awaiting_order_selection"] = False
                # Now check if there are multiple items
                if len(selected_order.items) == 1:
                    item = selected_order.items[0]
                    context["selected_item_id"] = item.item_id
                    context["item_name"] = item.product_name
                    context["item_price"] = item.price
                    return AgentResponse(
                        success=True,
                        message=f"Got it, you want to return the {item.product_name}. Can you tell me why you're returning it?",
                        data={
                            "order_id": selected_order.order_id,
                            "item_id": item.item_id,
                            "item_name": item.product_name,
                            "item_price": item.price,
                        },
                        next_action="return_classification",
                    )
                else:
                    # Multiple items, ask which one
                    items_text = ", ".join([item.product_name for item in selected_order.items])
                    return AgentResponse(
                        success=True,
                        message=f"This order contains: {items_text}. Which one would you like to return?",
                        requires_clarification=True,
                    )

        # Fetch user's recent orders
        orders = self.db.get_user_orders(user_id, limit=5)

        if not orders:
            return AgentResponse(
                success=False,
                message="I couldn't find any recent orders for your account. Can you provide an order number?",
                requires_clarification=True,
            )

        # Store orders in context for selection
        context["available_orders"] = orders
        context["awaiting_order_selection"] = True

        # Present orders to user
        response_message = self._format_orders_message(orders)

        return AgentResponse(
            success=True,
            message=response_message,
            data={
                "orders": [
                    {
                        "order_id": order.order_id,
                        "items": [
                            {"item_id": item.item_id, "product_name": item.product_name}
                            for item in order.items
                        ],
                        "order_date": order.order_date.isoformat(),
                    }
                    for order in orders
                ],
            },
            next_action="await_order_selection",
        )

    def _format_orders_message(self, orders) -> str:
        """Format orders into a conversational message."""
        if len(orders) == 1:
            order = orders[0]
            items_text = ", ".join([item.product_name for item in order.items])
            days_ago = (datetime.now() - order.order_date).days
            return f"I found your order from {days_ago} days ago containing {items_text}. Which item would you like to return?"

        message = f"I found {len(orders)} recent orders. "
        for i, order in enumerate(orders[:3], 1):
            days_ago = (datetime.now() - order.order_date).days
            items_text = ", ".join([item.product_name for item in order.items])
            message += f"Order {i}: {items_text} from {days_ago} days ago. "

        message += "Which order contains the item you want to return?"
        return message

    def _handle_item_selection(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """Handle user selecting a specific item from an order."""
        order_id = context.get("selected_order_id")
        order = self.db.get_order(order_id)

        if not order:
            return AgentResponse(
                success=False,
                message="I couldn't find that order. Let me look up your orders again.",
                next_action="purchase_retrieval",
            )

        # Simple item matching based on keywords in user input
        user_input_lower = user_input.lower()
        selected_item = None

        # Check for specific product names
        for item in order.items:
            if item.product_name.lower() in user_input_lower:
                selected_item = item
                break

        # Check for ordinal/numeric selection
        if not selected_item:
            if "first" in user_input_lower or "1" in user_input_lower or len(order.items) == 1:
                selected_item = order.items[0]
            elif "second" in user_input_lower or "2" in user_input_lower:
                selected_item = order.items[1] if len(order.items) > 1 else None

        # If user is describing a return reason, they likely mean the only/first item
        reason_keywords = ["damaged", "wrong", "broken", "defective", "size", "remorse", "described"]
        if not selected_item and any(keyword in user_input_lower for keyword in reason_keywords):
            selected_item = order.items[0]

        # If no match, ask for clarification
        if not selected_item and len(order.items) > 1:
            items_text = ", ".join([item.product_name for item in order.items])
            return AgentResponse(
                success=False,
                message=f"This order contains: {items_text}. Which one would you like to return?",
                requires_clarification=True,
            )
        elif not selected_item:
            selected_item = order.items[0]

        # Check if item is returnable
        if not order.is_returnable():
            return AgentResponse(
                success=False,
                message=f"I'm sorry, but this order is outside the 30-day return window. The order was placed {(datetime.now() - order.order_date).days} days ago.",
                next_action="end",
            )

        context["selected_item_id"] = selected_item.item_id
        context["item_name"] = selected_item.product_name
        context["item_price"] = selected_item.price

        return AgentResponse(
            success=True,
            message=f"Got it, you want to return the {selected_item.product_name}. Can you tell me why you're returning it?",
            data={
                "order_id": order_id,
                "item_id": selected_item.item_id,
                "item_name": selected_item.product_name,
                "item_price": selected_item.price,
            },
            next_action="return_classification",
        )

    def _select_order_from_input(self, user_input: str, orders):
        """Select an order based on user input."""
        user_input_lower = user_input.lower()

        # Check for ordinal numbers
        if "first" in user_input_lower or "1" in user_input_lower:
            return orders[0] if orders else None
        elif "second" in user_input_lower or "2" in user_input_lower:
            return orders[1] if len(orders) > 1 else None
        elif "third" in user_input_lower or "3" in user_input_lower:
            return orders[2] if len(orders) > 2 else None

        # Check for product names mentioned
        for order in orders:
            for item in order.items:
                if item.product_name.lower() in user_input_lower:
                    return order

        # Default to first order if ambiguous
        return orders[0] if orders else None
