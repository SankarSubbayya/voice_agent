"""Intent Router Agent - Routes user requests to appropriate specialist agents."""

from enum import Enum
from typing import Dict, Any
import re

from .base_agent import BaseAgent, AgentResponse


class Intent(Enum):
    """Possible user intents."""

    START_RETURN = "start_return"
    TRACK_RETURN = "track_return"
    PACKAGING_HELP = "packaging_help"
    REFUND_STATUS = "refund_status"
    DISPUTE_REFUND = "dispute_refund"
    GENERAL_INQUIRY = "general_inquiry"
    UNKNOWN = "unknown"


class IntentRouter(BaseAgent):
    """Routes user input to the appropriate specialist agent."""

    def __init__(self):
        """Initialize the Intent Router."""
        super().__init__("IntentRouter")

        # Intent patterns for classification
        self.intent_patterns = {
            Intent.START_RETURN: [
                r"(return|send back|give back)",
                r"(want to|need to|how do i) return",
                r"return (something|item|product|purchase)",
                r"bought.*wrong",
                r"(damaged|defective|broken)",
            ],
            Intent.TRACK_RETURN: [
                r"(track|where is|status of) (my )?return",
                r"return.*tracking",
                r"(shipped|sent) back",
            ],
            Intent.PACKAGING_HELP: [
                r"how (do|to) (pack|package)",
                r"packaging (instructions|help)",
                r"(where|how) (do|to) (drop off|ship)",
                r"(ups|usps|fedex) (location|store)",
            ],
            Intent.REFUND_STATUS: [
                r"(where is|when|status of) (my )?refund",
                r"refund.*processing",
                r"(money|payment) back",
                r"been refunded",
            ],
            Intent.DISPUTE_REFUND: [
                r"(wrong|incorrect|less) refund",
                r"dispute.*refund",
                r"refund.*wrong",
                r"(didn't|haven't) (get|receive).*refund",
                r"refund.*amount",
            ],
        }

    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Classify user intent and route to appropriate agent.

        Args:
            user_input: The user's voice input
            context: Conversation context

        Returns:
            AgentResponse with routing information
        """
        intent = self._classify_intent(user_input)

        # Map intent to next agent
        intent_to_agent = {
            Intent.START_RETURN: "purchase_retrieval",
            Intent.TRACK_RETURN: "tracking_refund",
            Intent.PACKAGING_HELP: "logistics",
            Intent.REFUND_STATUS: "tracking_refund",
            Intent.DISPUTE_REFUND: "tracking_refund",
        }

        next_agent = intent_to_agent.get(intent)

        if intent == Intent.UNKNOWN:
            return AgentResponse(
                success=False,
                message="I'm not sure what you'd like to do. You can start a return, track a return, get packaging help, or check your refund status. How can I help you?",
                requires_clarification=True,
            )

        # Generate appropriate response message
        messages = {
            Intent.START_RETURN: "I'll help you start a return. Let me look up your recent orders.",
            Intent.TRACK_RETURN: "I'll help you track your return. Let me check the status.",
            Intent.PACKAGING_HELP: "I'll help you with packaging and drop-off instructions.",
            Intent.REFUND_STATUS: "I'll check your refund status for you.",
            Intent.DISPUTE_REFUND: "I'll help you with your refund issue. Let me review your return.",
        }

        return AgentResponse(
            success=True,
            message=messages.get(intent, "How can I help you?"),
            data={"intent": intent.value},
            next_action=next_agent,
        )

    def _classify_intent(self, user_input: str) -> Intent:
        """
        Classify the user's intent from their input.

        Args:
            user_input: The user's text input

        Returns:
            Detected Intent
        """
        user_input_lower = user_input.lower()

        # Check each intent pattern
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input_lower):
                    return intent

        return Intent.UNKNOWN
