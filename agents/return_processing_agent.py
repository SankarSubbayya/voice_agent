"""Return Processing Agent - Generates return ID, labels, and QR codes."""

from typing import Dict, Any
from datetime import datetime
import random
import string

from .base_agent import BaseAgent, AgentResponse
from models.return_request import ReturnRequest, ReturnReason, ReturnStatus
from database.mock_db import MockDatabase


class ReturnProcessingAgent(BaseAgent):
    """Processes returns, generates labels and QR codes."""

    def __init__(self, database: MockDatabase):
        """Initialize the Return Processing Agent."""
        super().__init__("ReturnProcessingAgent")
        self.db = database

    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Process the return request and generate labels.

        Args:
            user_input: The user's voice input
            context: Conversation context with return details

        Returns:
            AgentResponse with return confirmation and label info
        """
        # Extract context information
        user_id = context.get("user_id")
        order_id = context.get("selected_order_id")
        item_id = context.get("selected_item_id")
        reason_str = context.get("return_reason", "other")
        fraud_risk = context.get("fraud_risk_score", 0.0)

        if not all([user_id, order_id, item_id]):
            return AgentResponse(
                success=False,
                message="I'm missing some information to process your return. Let's start over.",
                next_action="intent_router",
            )

        # Get order and item details
        order = self.db.get_order(order_id)
        if not order:
            return AgentResponse(
                success=False,
                message="I couldn't find that order. Please try again.",
                next_action="purchase_retrieval",
            )

        item = order.get_item_by_id(item_id)
        if not item:
            return AgentResponse(
                success=False,
                message="I couldn't find that item in your order.",
                next_action="purchase_retrieval",
            )

        # Create return request
        return_id = self._generate_return_id(order_id)
        tracking_number = self._generate_tracking_number()

        # Convert reason string to enum
        try:
            reason = ReturnReason(reason_str)
        except ValueError:
            reason = ReturnReason.OTHER

        return_request = ReturnRequest(
            return_id=return_id,
            order_id=order_id,
            user_id=user_id,
            item_id=item_id,
            reason=reason,
            status=ReturnStatus.LABEL_GENERATED,
            refund_amount=item.price,
            fraud_risk_score=fraud_risk,
            tracking_number=tracking_number,
        )

        # Generate label and QR code URLs (mock)
        label_url = self._generate_label_url(return_id)
        qr_code_url = self._generate_qr_code_url(return_id)

        return_request.label_url = label_url
        return_request.qr_code_url = qr_code_url

        # Save to database
        self.db.create_return(return_request)

        # Store in context for future reference
        context["return_id"] = return_id
        context["tracking_number"] = tracking_number

        # Generate response message
        message = f"""Perfect! I've created your return for the {item.product_name}.

Your return ID is {return_id}.

Your refund amount will be ${item.price:.2f}.

I've generated a prepaid shipping label. You can either:
1. Print the label from this link: {label_url}
2. Use this QR code at a UPS drop-off location: {qr_code_url}

Would you like help with packaging instructions or finding a drop-off location?"""

        return AgentResponse(
            success=True,
            message=message,
            data={
                "return_id": return_id,
                "tracking_number": tracking_number,
                "label_url": label_url,
                "qr_code_url": qr_code_url,
                "refund_amount": item.price,
            },
            next_action="logistics",
        )

    def _generate_return_id(self, order_id: str) -> str:
        """Generate a unique return ID."""
        timestamp = int(datetime.now().timestamp())
        return f"RET-{order_id}-{timestamp}"

    def _generate_tracking_number(self) -> str:
        """Generate a mock tracking number."""
        # UPS-style tracking number (1Z + 16 alphanumeric)
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
        return f"1Z{random_chars}"

    def _generate_label_url(self, return_id: str) -> str:
        """Generate a mock label URL."""
        return f"https://returns.example.com/label/{return_id}.pdf"

    def _generate_qr_code_url(self, return_id: str) -> str:
        """Generate a mock QR code URL."""
        return f"https://returns.example.com/qr/{return_id}.png"
