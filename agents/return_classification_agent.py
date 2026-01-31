"""Return Classification Agent - Classifies return reasons and checks eligibility."""

from typing import Dict, Any
import re

from .base_agent import BaseAgent, AgentResponse
from models.return_request import ReturnReason
from database.mock_db import MockDatabase


class ReturnClassificationAgent(BaseAgent):
    """Classifies the reason for return and validates eligibility."""

    def __init__(self, database: MockDatabase):
        """Initialize the Return Classification Agent."""
        super().__init__("ReturnClassificationAgent")
        self.db = database

        # Reason classification patterns
        self.reason_patterns = {
            ReturnReason.DAMAGED: [
                r"(damaged|broken|cracked|shattered)",
                r"arrived.*damaged",
                r"(defective|doesn't work)",
                r"not working",
                r"poor (condition|presentation)",
                r"(shipping )?box.*damaged",
                r"product.*damaged",
            ],
            ReturnReason.WRONG_ITEM: [
                r"(wrong|incorrect) (item|product)",
                r"(received|got) the wrong",
                r"not what.*ordered",
                r"wrong item.*sent",
            ],
            ReturnReason.SIZE_ISSUE: [
                r"(too|doesn't) (big|small|fit)",
                r"wrong size",
                r"(size|fit) (issue|problem)",
                r"too (large|long)",
                r"too (small|short)",
            ],
            ReturnReason.BUYER_REMORSE: [
                r"(changed|change) (my )?mind",
                r"don't (want|need)",
                r"no longer (want|need)",
                r"decided not to",
                r"better price",
                r"found.*cheaper",
                r"price.*available",
            ],
            ReturnReason.NOT_AS_DESCRIBED: [
                r"not as (described|advertised|shown)",
                r"(different|not) (from|what).*picture",
                r"(misleading|false) description",
                r"style.*(not|isn't|different|expected)",
                r"fabric.*(not|isn't|different|feels|expected)",
                r"material.*(not|isn't|different|expected)",
                r"color.*(not|isn't|different|doesn't|match|expected)",
                r"pattern.*(not|isn't|different|expected)",
                r"inaccurate.*description",
                r"(website|listing).*inaccurate",
            ],
        }

    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Classify return reason and check eligibility.

        Args:
            user_input: The user's voice input describing the reason
            context: Conversation context with order and item info

        Returns:
            AgentResponse with classification and next steps
        """
        # Classify the return reason
        reason = self._classify_reason(user_input)

        if reason == ReturnReason.OTHER:
            return AgentResponse(
                success=False,
                message="I didn't quite catch that. Can you tell me more about why you're returning this item? Is it damaged, the wrong item, a size issue, or something else?",
                requires_clarification=True,
            )

        # Calculate fraud risk
        fraud_risk = self._calculate_fraud_risk(context, reason)

        # Check if return is eligible
        order_id = context.get("selected_order_id")
        order = self.db.get_order(order_id)

        if not order or not order.is_returnable():
            return AgentResponse(
                success=False,
                message="I'm sorry, but this item is outside the return window and cannot be returned.",
                next_action="end",
            )

        # Generate appropriate response based on reason
        response_messages = {
            ReturnReason.DAMAGED: "I'm sorry to hear the item arrived damaged. We'll process a full refund for you.",
            ReturnReason.WRONG_ITEM: "I apologize for sending the wrong item. We'll get this sorted out with a full refund.",
            ReturnReason.SIZE_ISSUE: "No problem! We'll process your return for the sizing issue.",
            ReturnReason.BUYER_REMORSE: "That's perfectly fine. We'll process your return.",
            ReturnReason.NOT_AS_DESCRIBED: "I understand. We'll process your return since the item didn't match the description.",
        }

        item_price = context.get("item_price", 0.0)

        # Store classification in context
        context["return_reason"] = reason.value
        context["fraud_risk_score"] = fraud_risk

        return AgentResponse(
            success=True,
            message=response_messages.get(reason, "I've noted your reason. Let me process your return."),
            data={
                "reason": reason.value,
                "refund_amount": item_price,
                "fraud_risk_score": fraud_risk,
            },
            next_action="return_processing",
        )

    def _classify_reason(self, user_input: str) -> ReturnReason:
        """
        Classify the return reason from user input.

        Args:
            user_input: User's description of why they're returning

        Returns:
            ReturnReason enum
        """
        user_input_lower = user_input.lower()

        for reason, patterns in self.reason_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return reason

        return ReturnReason.OTHER

    def _calculate_fraud_risk(self, context: Dict[str, Any], reason: ReturnReason) -> float:
        """
        Calculate basic fraud risk score.

        Args:
            context: Conversation context with user info
            reason: The classified return reason

        Returns:
            Fraud risk score (0.0 to 1.0)
        """
        risk_score = 0.0

        # Base risk by reason
        reason_risk = {
            ReturnReason.DAMAGED: 0.1,
            ReturnReason.WRONG_ITEM: 0.1,
            ReturnReason.SIZE_ISSUE: 0.2,
            ReturnReason.BUYER_REMORSE: 0.3,
            ReturnReason.NOT_AS_DESCRIBED: 0.2,
            ReturnReason.OTHER: 0.4,
        }
        risk_score += reason_risk.get(reason, 0.3)

        # Adjust based on user history
        user_id = context.get("user_id")
        if user_id:
            user = self.db.get_user(user_id)
            if user:
                risk_score *= user.get_fraud_risk_multiplier()

        # Cap at 1.0
        return min(risk_score, 1.0)
