"""Tracking & Refund Agent - Handles tracking, refund status, and disputes."""

from typing import Dict, Any
from datetime import datetime, timedelta
import random

from .base_agent import BaseAgent, AgentResponse
from models.tracking import TrackingInfo, ShipmentStatus
from models.return_request import ReturnStatus
from database.mock_db import MockDatabase


class TrackingRefundAgent(BaseAgent):
    """Provides tracking information and handles refund queries and disputes."""

    def __init__(self, database: MockDatabase):
        """Initialize the Tracking & Refund Agent."""
        super().__init__("TrackingRefundAgent")
        self.db = database

    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Handle tracking and refund queries.

        Args:
            user_input: The user's voice input
            context: Conversation context

        Returns:
            AgentResponse with tracking/refund information
        """
        user_input_lower = user_input.lower()

        # Determine what the user wants
        if "dispute" in user_input_lower or "wrong" in user_input_lower or "less" in user_input_lower:
            return self._handle_dispute(user_input, context)
        elif "refund" in user_input_lower:
            return self._handle_refund_status(context)
        else:
            return self._handle_tracking_status(context)

    def _handle_tracking_status(self, context: Dict[str, Any]) -> AgentResponse:
        """Provide tracking status for a return."""
        user_id = context.get("user_id")
        return_id = context.get("return_id")

        if not user_id:
            return AgentResponse(
                success=False,
                message="I need to identify you first. Can you provide your phone number or return ID?",
                requires_clarification=True,
            )

        # Get user's returns
        if return_id:
            return_request = self.db.get_return(return_id)
            if not return_request:
                return AgentResponse(
                    success=False,
                    message="I couldn't find that return. Can you provide your return ID?",
                    requires_clarification=True,
                )
        else:
            # Get most recent return
            user_returns = self.db.get_user_returns(user_id)
            if not user_returns:
                return AgentResponse(
                    success=False,
                    message="I couldn't find any returns for your account.",
                    next_action="end",
                )
            return_request = user_returns[-1]  # Most recent

        # Get or create tracking info
        tracking_info = self._get_or_create_tracking(return_request)

        # Generate status message
        message = f"""Let me check your return status for {return_request.return_id}.

{tracking_info.get_status_message()}

Tracking number: {return_request.tracking_number}
Current status: {tracking_info.status.value.replace('_', ' ').title()}
"""

        if tracking_info.current_location:
            message += f"Current location: {tracking_info.current_location}\n"

        if tracking_info.estimated_delivery:
            days_until = (tracking_info.estimated_delivery - datetime.now()).days
            message += f"Expected at our facility in {days_until} days\n"

        # Add refund timeline
        if tracking_info.status == ShipmentStatus.DELIVERED:
            message += "\nYour refund will be processed within 3-5 business days after delivery."
        else:
            message += "\nYour refund will be processed once we receive the item."

        return AgentResponse(
            success=True,
            message=message,
            data={
                "return_id": return_request.return_id,
                "tracking_number": return_request.tracking_number,
                "status": tracking_info.status.value,
                "refund_amount": return_request.refund_amount,
            },
            next_action="end",
        )

    def _handle_refund_status(self, context: Dict[str, Any]) -> AgentResponse:
        """Provide refund status information."""
        user_id = context.get("user_id")

        if not user_id:
            return AgentResponse(
                success=False,
                message="I need to identify you first. Can you provide your phone number?",
                requires_clarification=True,
            )

        # Get user's returns
        user_returns = self.db.get_user_returns(user_id)
        if not user_returns:
            return AgentResponse(
                success=False,
                message="I couldn't find any returns for your account.",
                next_action="end",
            )

        # Get most recent return
        return_request = user_returns[-1]

        # Determine refund status based on return status
        refund_messages = {
            ReturnStatus.INITIATED: f"Your refund of ${return_request.refund_amount:.2f} will be processed once we receive your return.",
            ReturnStatus.LABEL_GENERATED: f"Your refund of ${return_request.refund_amount:.2f} will be processed once we receive your return. Please ship the item back using the label provided.",
            ReturnStatus.IN_TRANSIT: f"Your return is on its way to us. Your refund of ${return_request.refund_amount:.2f} will be processed within 3-5 business days after we receive it.",
            ReturnStatus.RECEIVED: f"We've received your return! Your refund of ${return_request.refund_amount:.2f} is being processed and should appear in your account within 3-5 business days.",
            ReturnStatus.REFUND_PROCESSED: f"Good news! Your refund of ${return_request.refund_amount:.2f} has been processed. It should appear in your original payment method within 3-5 business days.",
        }

        message = refund_messages.get(
            return_request.status,
            f"Your refund status is {return_request.status.value}. The refund amount is ${return_request.refund_amount:.2f}.",
        )

        return AgentResponse(
            success=True,
            message=message,
            data={
                "return_id": return_request.return_id,
                "refund_amount": return_request.refund_amount,
                "status": return_request.status.value,
            },
            next_action="end",
        )

    def _handle_dispute(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """Handle refund disputes."""
        user_id = context.get("user_id")

        if not user_id:
            return AgentResponse(
                success=False,
                message="I need to identify you first. Can you provide your phone number?",
                requires_clarification=True,
            )

        # Get user's returns
        user_returns = self.db.get_user_returns(user_id)
        if not user_returns:
            return AgentResponse(
                success=False,
                message="I couldn't find any returns for your account.",
                next_action="end",
            )

        # Get most recent return
        return_request = user_returns[-1]

        # Review the original reason and calculate expected refund
        order = self.db.get_order(return_request.order_id)
        if not order:
            return AgentResponse(
                success=False,
                message="I'm having trouble finding your order information. Let me escalate this to a specialist.",
                next_action="escalate",
            )

        item = order.get_item_by_id(return_request.item_id)
        expected_refund = item.price if item else return_request.refund_amount

        message = f"""Let me review your refund for return {return_request.return_id}.

Original item price: ${expected_refund:.2f}
Refund issued: ${return_request.refund_amount:.2f}
Return reason: {return_request.reason.value.replace('_', ' ').title()}
"""

        # Check for discrepancy
        if abs(expected_refund - return_request.refund_amount) > 0.01:
            message += f"\nI see there's a difference of ${abs(expected_refund - return_request.refund_amount):.2f}. "
            message += "This might be due to a restocking fee or the item's condition. Let me escalate this to a specialist who can review your case and help resolve this. You should hear back within 24 hours."

            # Update return status to disputed
            self.db.update_return_status(return_request.return_id, ReturnStatus.DISPUTED)

            return AgentResponse(
                success=True,
                message=message,
                data={"escalated": True, "return_id": return_request.return_id},
                next_action="escalate",
            )
        else:
            message += "\nYour refund amount appears to be correct. If you believe there's still an issue, I can escalate this to a specialist. Would you like me to do that?"

            return AgentResponse(
                success=True,
                message=message,
                requires_clarification=True,
            )

    def _get_or_create_tracking(self, return_request) -> TrackingInfo:
        """Get existing tracking info or create mock tracking."""
        tracking_info = self.db.get_tracking(return_request.tracking_number)

        if not tracking_info:
            # Create mock tracking based on return status
            status_map = {
                ReturnStatus.LABEL_GENERATED: ShipmentStatus.LABEL_CREATED,
                ReturnStatus.IN_TRANSIT: ShipmentStatus.IN_TRANSIT,
                ReturnStatus.RECEIVED: ShipmentStatus.DELIVERED,
            }

            status = status_map.get(return_request.status, ShipmentStatus.LABEL_CREATED)

            tracking_info = TrackingInfo(
                tracking_number=return_request.tracking_number,
                carrier="UPS",
                status=status,
                last_update=datetime.now(),
                estimated_delivery=datetime.now() + timedelta(days=random.randint(3, 7)),
                current_location="In Transit" if status == ShipmentStatus.IN_TRANSIT else None,
            )

            self.db.create_tracking(tracking_info)

        return tracking_info
