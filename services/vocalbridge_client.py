"""
VocalBridge AI Client Integration

Provides speech-to-text, text-to-speech, and voice conversation
capabilities using the VocalBridge AI platform.
"""

import json
from typing import Optional, Dict, Any
from config import config


class VocalBridgeClient:
    """
    Client for VocalBridge AI voice platform.

    Handles:
    - Speech-to-text (STT)
    - Text-to-speech (TTS)
    - Voice conversation sessions
    - Audio streaming
    """

    def __init__(self, api_key: Optional[str] = None, endpoint: Optional[str] = None):
        """
        Initialize VocalBridge client.

        Args:
            api_key: VocalBridge API key (defaults to config)
            endpoint: API endpoint (defaults to config)
        """
        self.api_key = api_key or config.vocalbridge_api_key
        self.endpoint = endpoint or config.vocalbridge_endpoint

        if not self.api_key:
            raise ValueError(
                "VocalBridge API key not found. "
                "Please set VOCALBRIDGE_API_KEY in .env file"
            )

        self.session_id: Optional[str] = None

    def _get_headers(self) -> Dict[str, str]:
        """Get HTTP headers for API requests."""
        # VocalBridge uses X-API-Key header (recommended method)
        return {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json",
        }

    # ==========================================================================
    # SPEECH-TO-TEXT
    # ==========================================================================

    def speech_to_text(
        self,
        audio_data: bytes,
        format: str = "wav",
        language: str = "en-US"
    ) -> str:
        """
        Convert speech audio to text.

        Args:
            audio_data: Audio bytes (WAV, MP3, etc.)
            format: Audio format (wav, mp3, ogg)
            language: Language code (en-US, es-ES, etc.)

        Returns:
            Transcribed text

        Example:
            >>> client = VocalBridgeClient()
            >>> with open('audio.wav', 'rb') as f:
            >>>     audio = f.read()
            >>> text = client.speech_to_text(audio)
            >>> print(text)
            "I want to return my headphones"
        """
        # In mock mode, return placeholder
        if config.use_mock_apis:
            return "[Mock STT] User speech transcription"

        try:
            import requests

            # VocalBridge STT endpoint
            url = f"{self.endpoint}/speech-to-text"

            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": f"audio/{format}",
            }

            # Send audio data
            response = requests.post(
                url,
                headers=headers,
                data=audio_data,
                params={'language': language},
                timeout=30
            )

            response.raise_for_status()
            result = response.json()

            # Extract transcript from response
            # Adjust this based on actual VocalBridge response format
            if 'transcript' in result:
                return result['transcript']
            elif 'text' in result:
                return result['text']
            else:
                return result.get('transcription', '')

        except ImportError:
            raise ImportError(
                "requests library required. Install with: pip install requests"
            )
        except Exception as e:
            raise Exception(f"Speech-to-text failed: {e}")

    # ==========================================================================
    # TEXT-TO-SPEECH
    # ==========================================================================

    def text_to_speech(
        self,
        text: str,
        voice: str = "en-US-Neural2-A",
        format: str = "mp3"
    ) -> bytes:
        """
        Convert text to speech audio.

        Args:
            text: Text to synthesize
            voice: Voice ID/name
            format: Output format (mp3, wav, ogg)

        Returns:
            Audio bytes

        Example:
            >>> client = VocalBridgeClient()
            >>> audio = client.text_to_speech("Hello, how can I help you?")
            >>> with open('response.mp3', 'wb') as f:
            >>>     f.write(audio)
        """
        # In mock mode, return empty bytes
        if config.use_mock_apis:
            return b"[Mock TTS audio bytes]"

        try:
            import requests

            # VocalBridge TTS endpoint
            url = f"{self.endpoint}/text-to-speech"

            headers = {
                "X-API-Key": self.api_key,
                "Content-Type": "application/json",
            }

            payload = {
                'text': text,
                'voice': voice,
                'format': format,
            }

            response = requests.post(
                url,
                headers=headers,
                json=payload,
                timeout=30
            )

            response.raise_for_status()

            # Return audio bytes
            return response.content

        except ImportError:
            raise ImportError(
                "requests library required. Install with: pip install requests"
            )
        except Exception as e:
            raise Exception(f"Text-to-speech failed: {e}")

    # ==========================================================================
    # CONVERSATION SESSION
    # ==========================================================================

    def create_session(
        self,
        user_id: str,
        language: str = "en-US",
        voice: str = "en-US-Neural2-A"
    ) -> str:
        """
        Create a voice conversation session.

        Args:
            user_id: User identifier
            language: Language code
            voice: Voice to use for responses

        Returns:
            Session ID

        Example:
            >>> client = VocalBridgeClient()
            >>> session_id = client.create_session("user123")
            >>> print(f"Session: {session_id}")
        """
        # In mock mode, generate mock session ID
        if config.use_mock_apis:
            from datetime import datetime
            session_id = f"mock-session-{int(datetime.now().timestamp())}"
            self.session_id = session_id
            return session_id

        try:
            import requests

            url = f"{self.endpoint}/sessions"

            payload = {
                'user_id': user_id,
                'language': language,
                'voice': voice,
            }

            response = requests.post(
                url,
                headers=self._get_headers(),
                json=payload,
                timeout=10
            )

            response.raise_for_status()
            result = response.json()

            session_id = result.get('session_id')
            self.session_id = session_id

            return session_id

        except ImportError:
            raise ImportError(
                "requests library required. Install with: pip install requests"
            )
        except Exception as e:
            raise Exception(f"Session creation failed: {e}")

    def end_session(self, session_id: Optional[str] = None) -> bool:
        """
        End a voice conversation session.

        Args:
            session_id: Session to end (defaults to current session)

        Returns:
            Success status
        """
        session_id = session_id or self.session_id

        if not session_id:
            return False

        # In mock mode, just clear session
        if config.use_mock_apis:
            self.session_id = None
            return True

        try:
            import requests

            url = f"{self.endpoint}/sessions/{session_id}"

            response = requests.delete(
                url,
                headers=self._get_headers(),
                timeout=10
            )

            response.raise_for_status()
            self.session_id = None

            return True

        except Exception:
            return False

    # ==========================================================================
    # STREAMING
    # ==========================================================================

    def stream_audio(
        self,
        audio_stream,
        session_id: Optional[str] = None,
        callback=None
    ):
        """
        Stream audio for real-time transcription.

        Args:
            audio_stream: Audio stream iterator (chunks of bytes)
            session_id: Session ID (optional)
            callback: Function to call with transcription results

        Example:
            >>> def on_transcript(text):
            >>>     print(f"User said: {text}")
            >>>
            >>> client = VocalBridgeClient()
            >>> with microphone.stream() as audio:
            >>>     client.stream_audio(audio, callback=on_transcript)
        """
        # In mock mode, simulate streaming
        if config.use_mock_apis:
            if callback:
                callback("[Mock streaming transcription]")
            return

        try:
            import requests

            url = f"{self.endpoint}/stream"

            headers = self._get_headers()
            if session_id:
                headers['X-Session-ID'] = session_id

            # WebSocket or chunked streaming would go here
            # This is a simplified version
            for chunk in audio_stream:
                # Process audio chunk
                # Call callback with results
                pass

        except Exception as e:
            raise Exception(f"Audio streaming failed: {e}")

    # ==========================================================================
    # UTILITY METHODS
    # ==========================================================================

    def get_available_voices(self, language: str = "en-US") -> list[Dict[str, str]]:
        """
        Get list of available voices.

        Args:
            language: Filter by language

        Returns:
            List of voice metadata
        """
        # In mock mode, return sample voices
        if config.use_mock_apis:
            return [
                {"id": "en-US-Neural2-A", "name": "Female 1", "language": "en-US"},
                {"id": "en-US-Neural2-B", "name": "Male 1", "language": "en-US"},
                {"id": "en-US-Neural2-C", "name": "Female 2", "language": "en-US"},
            ]

        try:
            import requests

            url = f"{self.endpoint}/voices"
            params = {"language": language}

            response = requests.get(
                url,
                headers=self._get_headers(),
                params=params,
                timeout=10
            )

            response.raise_for_status()
            return response.json().get('voices', [])

        except Exception:
            return []

    def health_check(self) -> bool:
        """
        Check if VocalBridge API is accessible.

        Returns:
            True if API is healthy
        """
        # In mock mode, always return True
        if config.use_mock_apis:
            return True

        try:
            import requests

            url = f"{self.endpoint}/health"

            response = requests.get(url, timeout=5)
            return response.status_code == 200

        except Exception:
            return False


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_vocalbridge_client() -> VocalBridgeClient:
    """
    Get a configured VocalBridge client instance.

    Returns:
        VocalBridgeClient instance

    Raises:
        ValueError: If API key is not configured
    """
    return VocalBridgeClient()


def quick_transcribe(audio_file_path: str) -> str:
    """
    Quick helper to transcribe an audio file.

    Args:
        audio_file_path: Path to audio file

    Returns:
        Transcribed text

    Example:
        >>> text = quick_transcribe("recording.wav")
        >>> print(text)
    """
    client = get_vocalbridge_client()

    with open(audio_file_path, 'rb') as f:
        audio_data = f.read()

    # Detect format from extension
    format = audio_file_path.split('.')[-1].lower()

    return client.speech_to_text(audio_data, format=format)


def quick_synthesize(text: str, output_file: str, voice: str = "en-US-Neural2-A"):
    """
    Quick helper to synthesize speech to file.

    Args:
        text: Text to synthesize
        output_file: Output audio file path
        voice: Voice ID to use

    Example:
        >>> quick_synthesize("Hello world", "output.mp3")
    """
    client = get_vocalbridge_client()

    audio = client.text_to_speech(text, voice=voice)

    with open(output_file, 'wb') as f:
        f.write(audio)
