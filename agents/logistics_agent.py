"""Logistics Agent - Provides packaging and drop-off information."""

from typing import Dict, Any, List
import re

from .base_agent import BaseAgent, AgentResponse


class LogisticsAgent(BaseAgent):
    """Provides packaging instructions and carrier drop-off locations."""

    def __init__(self):
        """Initialize the Logistics Agent."""
        super().__init__("LogisticsAgent")

        # Mock carrier locations (in a real system, this would use geolocation API)
        self.carrier_locations = {
            "ups": [
                "UPS Store - 123 Main St, San Francisco, CA 94102 (0.5 miles)",
                "UPS Access Point - Walgreens, 456 Market St, San Francisco, CA 94103 (0.8 miles)",
                "UPS Store - 789 Mission St, San Francisco, CA 94105 (1.2 miles)",
            ],
            "usps": [
                "USPS Post Office - 100 1st St, San Francisco, CA 94102 (0.3 miles)",
                "USPS Post Office - 200 Pine St, San Francisco, CA 94104 (0.9 miles)",
            ],
            "fedex": [
                "FedEx Office - 300 California St, San Francisco, CA 94111 (0.6 miles)",
                "FedEx Drop Box - 400 Montgomery St, San Francisco, CA 94104 (1.0 miles)",
            ],
        }

    def process(self, user_input: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Provide packaging and logistics help.

        Args:
            user_input: The user's voice input
            context: Conversation context

        Returns:
            AgentResponse with logistics information
        """
        user_input_lower = user_input.lower()

        # Determine what the user is asking about
        if self._is_asking_about_packaging(user_input_lower):
            return self._provide_packaging_instructions(context)
        elif self._is_asking_about_location(user_input_lower):
            return self._provide_dropoff_locations(user_input_lower, context)
        elif "yes" in user_input_lower or "help" in user_input_lower:
            # User wants general logistics help
            return self._provide_general_help(context)
        elif "no" in user_input_lower or "done" in user_input_lower:
            return AgentResponse(
                success=True,
                message="Great! Your return is all set. You can track your return status anytime by asking me. Is there anything else I can help you with?",
                next_action="end",
            )
        else:
            return AgentResponse(
                success=True,
                message="I can help you with packaging instructions or finding a drop-off location. What would you like to know?",
                requires_clarification=True,
            )

    def _is_asking_about_packaging(self, user_input: str) -> bool:
        """Check if user is asking about packaging."""
        packaging_keywords = [r"pack", r"package", r"box", r"wrap", r"how to"]
        return any(re.search(keyword, user_input) for keyword in packaging_keywords)

    def _is_asking_about_location(self, user_input: str) -> bool:
        """Check if user is asking about drop-off locations."""
        location_keywords = [
            r"where",
            r"location",
            r"drop off",
            r"drop-off",
            r"nearest",
            r"ups",
            r"usps",
            r"fedex",
        ]
        return any(re.search(keyword, user_input) for keyword in location_keywords)

    def _provide_packaging_instructions(self, context: Dict[str, Any]) -> AgentResponse:
        """Provide packaging instructions."""
        item_name = context.get("item_name", "item")

        message = f"""Here's how to pack your {item_name}:

1. Place the item in its original packaging if you have it
2. If not, use a sturdy box that's slightly larger than the item
3. Wrap the item in bubble wrap or packing paper
4. Fill empty space with packing material to prevent movement
5. Seal the box securely with packing tape
6. Attach your shipping label to the outside of the box

Make sure not to include any personal items or accessories you want to keep!

Would you like help finding a drop-off location?"""

        return AgentResponse(
            success=True,
            message=message,
            next_action="await_user_response",
        )

    def _provide_dropoff_locations(
        self, user_input: str, context: Dict[str, Any]
    ) -> AgentResponse:
        """Provide drop-off location information."""
        # Determine carrier (default to UPS)
        carrier = "ups"
        if "usps" in user_input or "post office" in user_input:
            carrier = "usps"
        elif "fedex" in user_input:
            carrier = "fedex"

        locations = self.carrier_locations.get(carrier, self.carrier_locations["ups"])

        message = f"Here are the nearest {carrier.upper()} locations:\n\n"
        for i, location in enumerate(locations, 1):
            message += f"{i}. {location}\n"

        message += "\nRemember to bring your package with the label attached, or show the QR code if you're using a UPS store."

        return AgentResponse(
            success=True,
            message=message,
            data={"carrier": carrier, "locations": locations},
            next_action="end",
        )

    def _provide_general_help(self, context: Dict[str, Any]) -> AgentResponse:
        """Provide general logistics help."""
        message = """I can help you with:

1. Packaging instructions - how to safely pack your item
2. Drop-off locations - find the nearest UPS, USPS, or FedEx location
3. Shipping label - you already have your label and QR code

What would you like to know more about?"""

        return AgentResponse(
            success=True,
            message=message,
            requires_clarification=True,
        )
