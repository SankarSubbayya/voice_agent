"""
Voice Interface for ReturnFlow Voice Agent

Integrates VocalBridge AI with the multi-agent orchestrator
to enable true voice-based conversations.
"""

from typing import Optional, Callable
from datetime import datetime

from config import config
from services.vocalbridge_client import VocalBridgeClient
from services.orchestrator import VoiceOrchestrator
from database.mock_db import MockDatabase


class VoiceInterface:
    """
    Voice interface that connects VocalBridge AI to the ReturnFlow system.

    This is the bridge between:
    - VocalBridge AI (speech recognition/synthesis)
    - Voice Orchestrator (conversation management)
    - Multi-agent system (return processing)
    """

    def __init__(
        self,
        orchestrator: VoiceOrchestrator,
        vocalbridge_client: Optional[VocalBridgeClient] = None
    ):
        """
        Initialize voice interface.

        Args:
            orchestrator: The voice orchestrator managing agents
            vocalbridge_client: VocalBridge client (optional, will create if not provided)
        """
        self.orchestrator = orchestrator

        # Initialize VocalBridge client
        if vocalbridge_client:
            self.vocal_client = vocalbridge_client
        elif config.has_vocalbridge() and not config.use_mock_apis:
            self.vocal_client = VocalBridgeClient()
        else:
            # Mock mode
            self.vocal_client = VocalBridgeClient()

        self.current_session_id: Optional[str] = None
        self.voice_session_id: Optional[str] = None

    # ==========================================================================
    # VOICE CONVERSATION
    # ==========================================================================

    def start_voice_conversation(self, user_id: str) -> tuple[str, str]:
        """
        Start a voice conversation session.

        Args:
            user_id: User identifier

        Returns:
            Tuple of (orchestrator_session_id, vocalbridge_session_id)

        Example:
            >>> interface = VoiceInterface(orchestrator)
            >>> orch_session, voice_session = interface.start_voice_conversation("USER001")
        """
        # Create orchestrator session
        orch_session_id = self.orchestrator.start_conversation(user_id)
        self.orchestrator.identify_user(orch_session_id, user_id=user_id)

        # Create VocalBridge session
        voice_session_id = self.vocal_client.create_session(user_id)

        self.current_session_id = orch_session_id
        self.voice_session_id = voice_session_id

        return orch_session_id, voice_session_id

    def process_voice_input(
        self,
        audio_data: bytes,
        audio_format: str = "wav"
    ) -> tuple[bool, str, bytes]:
        """
        Process voice input and return voice response.

        Args:
            audio_data: Audio bytes from user
            audio_format: Audio format (wav, mp3, etc.)

        Returns:
            Tuple of (success, text_response, audio_response)

        Example:
            >>> with open('user_speech.wav', 'rb') as f:
            >>>     audio = f.read()
            >>> success, text, audio_response = interface.process_voice_input(audio)
            >>> # Play audio_response to user
        """
        if not self.current_session_id:
            return False, "No active session", b""

        try:
            # Step 1: Speech to text
            user_text = self.vocal_client.speech_to_text(audio_data, format=audio_format)

            # Step 2: Process through orchestrator
            success, response_text, data = self.orchestrator.process_input(
                self.current_session_id,
                user_text
            )

            # Step 3: Text to speech
            response_audio = self.vocal_client.text_to_speech(response_text)

            return success, response_text, response_audio

        except Exception as e:
            error_msg = f"Voice processing error: {e}"
            return False, error_msg, b""

    def process_text_input(self, text: str) -> tuple[bool, str, bytes]:
        """
        Process text input and return voice response.

        Useful for hybrid text/voice interfaces.

        Args:
            text: User's text input

        Returns:
            Tuple of (success, text_response, audio_response)
        """
        if not self.current_session_id:
            return False, "No active session", b""

        try:
            # Process through orchestrator
            success, response_text, data = self.orchestrator.process_input(
                self.current_session_id,
                text
            )

            # Generate voice response
            response_audio = self.vocal_client.text_to_speech(response_text)

            return success, response_text, response_audio

        except Exception as e:
            error_msg = f"Processing error: {e}"
            return False, error_msg, b""

    def end_conversation(self):
        """End the current voice conversation."""
        if self.voice_session_id:
            self.vocal_client.end_session(self.voice_session_id)

        if self.current_session_id:
            self.orchestrator.end_conversation(self.current_session_id)

        self.current_session_id = None
        self.voice_session_id = None

    # ==========================================================================
    # STREAMING (Advanced)
    # ==========================================================================

    def stream_conversation(
        self,
        audio_stream,
        on_transcript: Optional[Callable[[str], None]] = None,
        on_response: Optional[Callable[[str, bytes], None]] = None
    ):
        """
        Stream audio for real-time conversation.

        Args:
            audio_stream: Iterator of audio chunks
            on_transcript: Callback when user speech is transcribed
            on_response: Callback when agent response is ready (text, audio)

        Example:
            >>> def on_user_speech(text):
            >>>     print(f"User: {text}")
            >>>
            >>> def on_agent_response(text, audio):
            >>>     print(f"Agent: {text}")
            >>>     play_audio(audio)
            >>>
            >>> interface.stream_conversation(
            >>>     mic_stream,
            >>>     on_transcript=on_user_speech,
            >>>     on_response=on_agent_response
            >>> )
        """
        def handle_transcript(text: str):
            """Handle transcribed user input."""
            if on_transcript:
                on_transcript(text)

            # Process through orchestrator
            success, response_text, data = self.orchestrator.process_input(
                self.current_session_id,
                text
            )

            # Generate audio response
            response_audio = self.vocal_client.text_to_speech(response_text)

            if on_response:
                on_response(response_text, response_audio)

        # Stream audio through VocalBridge
        self.vocal_client.stream_audio(
            audio_stream,
            session_id=self.voice_session_id,
            callback=handle_transcript
        )

    # ==========================================================================
    # UTILITY
    # ==========================================================================

    def get_conversation_context(self) -> dict:
        """Get the current conversation context."""
        if not self.current_session_id:
            return {}

        return self.orchestrator.get_context(self.current_session_id) or {}

    def is_active(self) -> bool:
        """Check if there's an active conversation."""
        return self.current_session_id is not None


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def create_voice_interface(database: Optional[MockDatabase] = None) -> VoiceInterface:
    """
    Create a fully configured voice interface.

    Args:
        database: Database instance (will create if not provided)

    Returns:
        VoiceInterface instance ready to use

    Example:
        >>> interface = create_voice_interface()
        >>> interface.start_voice_conversation("USER001")
    """
    if database is None:
        database = MockDatabase()

    orchestrator = VoiceOrchestrator(database)
    return VoiceInterface(orchestrator)


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

def example_voice_conversation():
    """
    Example of how to use the voice interface.

    This demonstrates a complete voice-based return flow.
    """
    print("=" * 60)
    print("Voice Interface Example")
    print("=" * 60)
    print()

    # Create interface
    interface = create_voice_interface()

    # Start conversation
    print("Starting voice conversation...")
    orch_session, voice_session = interface.start_voice_conversation("USER001")
    print(f"Sessions created: {orch_session[:20]}...")
    print()

    # Simulate voice inputs (in real use, these would be actual audio)
    test_inputs = [
        "I want to return my headphones",
        "first order",
        "headphones",
        "It's broken",
    ]

    for user_input in test_inputs:
        print(f"User: {user_input}")

        # In real use: audio = record_from_microphone()
        # For demo, we'll use text
        success, response, audio = interface.process_text_input(user_input)

        print(f"Agent: {response[:100]}...")
        print()

    # End conversation
    interface.end_conversation()
    print("Conversation ended.")
    print()
    print("=" * 60)


if __name__ == "__main__":
    example_voice_conversation()
