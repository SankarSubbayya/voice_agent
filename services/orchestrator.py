"""Voice Orchestrator - Coordinates agent workflow and conversation flow."""

from typing import Dict, Any, Optional
from datetime import datetime

from agents import (
    IntentRouter,
    PurchaseRetrievalAgent,
    ReturnClassificationAgent,
    ReturnProcessingAgent,
    LogisticsAgent,
    TrackingRefundAgent,
)
from database.mock_db import MockDatabase


class VoiceOrchestrator:
    """
    Orchestrates the multi-agent conversation flow for voice-based returns.

    This is the main coordinator that:
    1. Maintains conversation context
    2. Routes between specialist agents
    3. Manages the conversation state machine
    """

    def __init__(self, database: MockDatabase):
        """Initialize the orchestrator with all agents."""
        self.db = database

        # Initialize all agents
        self.intent_router = IntentRouter()
        self.purchase_agent = PurchaseRetrievalAgent(database)
        self.classification_agent = ReturnClassificationAgent(database)
        self.processing_agent = ReturnProcessingAgent(database)
        self.logistics_agent = LogisticsAgent()
        self.tracking_agent = TrackingRefundAgent(database)

        # Conversation context
        self.sessions: Dict[str, Dict[str, Any]] = {}

    def start_conversation(self, user_id: str) -> str:
        """
        Start a new conversation session.

        Args:
            user_id: Unique identifier for the user

        Returns:
            Session ID
        """
        session_id = f"session_{user_id}_{int(datetime.now().timestamp())}"
        self.sessions[session_id] = {
            "user_id": user_id,
            "current_agent": "intent_router",
            "conversation_history": [],
            "created_at": datetime.now(),
        }
        return session_id

    def process_input(
        self, session_id: str, user_input: str
    ) -> tuple[bool, str, Optional[Dict[str, Any]]]:
        """
        Process user input through the appropriate agent.

        Args:
            session_id: The conversation session ID
            user_input: The user's voice input

        Returns:
            Tuple of (success, response_message, data)
        """
        if session_id not in self.sessions:
            return (
                False,
                "Session not found. Please start a new conversation.",
                None,
            )

        context = self.sessions[session_id]
        current_agent = context.get("current_agent", "intent_router")

        # Add to conversation history
        context["conversation_history"].append(
            {"timestamp": datetime.now(), "user": user_input}
        )

        # Route to appropriate agent
        if current_agent == "intent_router":
            response = self.intent_router.process(user_input, context)
        elif current_agent == "purchase_retrieval" or current_agent == "await_order_selection":
            response = self.purchase_agent.process(user_input, context)
        elif current_agent == "return_classification":
            response = self.classification_agent.process(user_input, context)
        elif current_agent == "return_processing":
            response = self.processing_agent.process(user_input, context)
        elif current_agent == "logistics" or current_agent == "await_user_response":
            response = self.logistics_agent.process(user_input, context)
        elif current_agent == "tracking_refund":
            response = self.tracking_agent.process(user_input, context)
        else:
            # Default to intent router
            response = self.intent_router.process(user_input, context)

        # Update context with next agent
        if response.next_action:
            context["current_agent"] = response.next_action

        # Add response to history
        context["conversation_history"].append(
            {"timestamp": datetime.now(), "agent": response.message}
        )

        return (response.success, response.message, response.data)

    def get_context(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the current conversation context."""
        return self.sessions.get(session_id)

    def end_conversation(self, session_id: str) -> None:
        """End a conversation session."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def identify_user(self, session_id: str, phone: str = None, user_id: str = None) -> bool:
        """
        Identify user by phone or user_id.

        Args:
            session_id: The conversation session ID
            phone: User's phone number
            user_id: User's ID

        Returns:
            True if user identified successfully
        """
        if session_id not in self.sessions:
            return False

        context = self.sessions[session_id]

        if phone:
            user = self.db.get_user_by_phone(phone)
            if user:
                context["user_id"] = user.user_id
                context["user"] = user
                return True
        elif user_id:
            user = self.db.get_user(user_id)
            if user:
                context["user_id"] = user.user_id
                context["user"] = user
                return True

        return False
