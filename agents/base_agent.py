"""Base agent class for all specialized agents."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AgentResponse:
    """Standard response format for all agents."""

    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    next_action: Optional[str] = None
    requires_clarification: bool = False


class BaseAgent(ABC):
    """Base class for all agents in the system."""

    def __init__(self, name: str):
        """Initialize the agent."""
        self.name = name
        self.context: Dict[str, Any] = {}

    @abstractmethod
    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Process user input and return a response.

        Args:
            user_input: The user's voice input
            context: Conversation context and session data

        Returns:
            AgentResponse with the agent's response
        """
        pass

    def update_context(self, key: str, value: Any) -> None:
        """Update the agent's context."""
        self.context[key] = value

    def get_context(self, key: str, default: Any = None) -> Any:
        """Get a value from the agent's context."""
        return self.context.get(key, default)

    def clear_context(self) -> None:
        """Clear the agent's context."""
        self.context.clear()
