## VocalBridge AI Integration

Complete guide for using VocalBridge AI with ReturnFlow Voice Agent.

---

## 📋 Overview

The ReturnFlow Voice Agent now supports **real voice input/output** through VocalBridge AI integration.

### Features

✅ **Speech-to-Text** - Convert user speech to text
✅ **Text-to-Speech** - Generate natural voice responses
✅ **Session Management** - Maintain conversation state
✅ **Streaming Audio** - Real-time voice processing
✅ **Hybrid Mode** - Mix text and voice input
✅ **Mock Mode** - Test without API keys

---

## 🚀 Quick Start

### 1. Add Your API Key

Edit `.env` and add your VocalBridge API key:

```env
# Uncomment and add your key
VOCALBRIDGE_API_KEY=your_actual_api_key_here
VOCALBRIDGE_ENDPOINT=https://api.vocalbridge.ai/v1

# Enable real APIs
USE_MOCK_APIS=false
```

### 2. Run Voice CLI

```bash
python3 voice_cli.py
```

### 3. Start Talking!

Press Enter to record, speak naturally:
- "I want to return my headphones"
- "It arrived damaged"
- "Where is the nearest UPS?"

---

## 📦 Components

### 1. VocalBridgeClient (`services/vocalbridge_client.py`)

Low-level client for VocalBridge API.

```python
from services import VocalBridgeClient

client = VocalBridgeClient()

# Speech to text
audio = open('speech.wav', 'rb').read()
text = client.speech_to_text(audio)

# Text to speech
audio = client.text_to_speech("Hello, how can I help?")
with open('response.mp3', 'wb') as f:
    f.write(audio)

# Session management
session_id = client.create_session("user123")
```

### 2. VoiceInterface (`services/voice_interface.py`)

High-level interface connecting VocalBridge to agents.

```python
from services import create_voice_interface

interface = create_voice_interface()

# Start conversation
orch_session, voice_session = interface.start_voice_conversation("USER001")

# Process voice input
with open('user_audio.wav', 'rb') as f:
    audio = f.read()

success, text_response, audio_response = interface.process_voice_input(audio)

# Play audio_response to user
```

### 3. Voice CLI (`voice_cli.py`)

Interactive voice-enabled command line interface.

**Features:**
- Voice input via microphone
- Load audio from files
- Hybrid text/voice mode
- Automatic session management

---

## 🎯 Usage Examples

### Example 1: Simple Voice Transcription

```python
from services import get_vocalbridge_client

client = get_vocalbridge_client()

# Record or load audio
with open('user_speech.wav', 'rb') as f:
    audio_data = f.read()

# Transcribe
text = client.speech_to_text(audio_data, format='wav')
print(f"User said: {text}")
```

### Example 2: Generate Voice Response

```python
from services import get_vocalbridge_client

client = get_vocalbridge_client()

# Generate speech
response_text = "Your return has been processed. The label will be emailed to you."
audio_data = client.text_to_speech(response_text)

# Save or play
with open('response.mp3', 'wb') as f:
    f.write(audio_data)
```

### Example 3: Full Voice Conversation

```python
from services import create_voice_interface

# Initialize
interface = create_voice_interface()
orch_session, voice_session = interface.start_voice_conversation("USER001")

# User speaks: "I want to return my coffee maker"
with open('user_input.wav', 'rb') as f:
    audio_in = f.read()

success, text, audio_out = interface.process_voice_input(audio_in)

print(f"Agent: {text}")
# Play audio_out to user

# Continue conversation...

interface.end_conversation()
```

### Example 4: Hybrid Mode (Text In, Voice Out)

```python
from services import create_voice_interface

interface = create_voice_interface()
interface.start_voice_conversation("USER001")

# User types text
user_text = "Track my return"

# Get voice response
success, response_text, response_audio = interface.process_text_input(user_text)

print(f"Agent: {response_text}")
# Play response_audio
```

### Example 5: Streaming Audio

```python
from services import create_voice_interface

def on_transcript(text):
    print(f"User: {text}")

def on_response(text, audio):
    print(f"Agent: {text}")
    play_audio(audio)  # Your audio playback function

interface = create_voice_interface()
interface.start_voice_conversation("USER001")

# Stream from microphone
mic_stream = get_microphone_stream()  # Your mic implementation

interface.stream_conversation(
    mic_stream,
    on_transcript=on_transcript,
    on_response=on_response
)
```

---

## 🔧 Configuration

### Environment Variables

```env
# Required
VOCALBRIDGE_API_KEY=your_key_here

# Optional
VOCALBRIDGE_ENDPOINT=https://api.vocalbridge.ai/v1  # Default endpoint
USE_MOCK_APIS=false  # Set to true for testing without API

# Voice Settings
DEFAULT_VOICE=en-US-Neural2-A
DEFAULT_LANGUAGE=en-US
```

### Python Configuration

```python
from config import config

# Check if VocalBridge is configured
if config.has_vocalbridge():
    print("VocalBridge ready!")
    print(f"Endpoint: {config.vocalbridge_endpoint}")

# Check mode
if config.use_mock_apis:
    print("Running in mock mode")
else:
    print("Using real VocalBridge API")
```

---

## 🎤 Voice CLI Guide

### Starting the Voice CLI

```bash
python3 voice_cli.py
```

### Voice Mode

When microphone is available:
1. Press **Enter** to record (5 seconds)
2. Speak your request
3. Agent responds with voice

```
🎤 [Press Enter to record] or command: [ENTER]
🎤 Recording for 5 seconds...
✅ Recording complete!

🤖 Agent: I'll help you start a return. Let me look up your recent orders.
```

### Text Mode (Hybrid)

Type text, get voice responses:

```
💬 You: I want to return my headphones
🤖 Agent: I found 2 recent orders...
    [🔊 Voice response generated]
```

### Loading Audio Files

```
🎤 [Press Enter to record] or command: load my_recording.wav
🤖 Agent: [Processes audio and responds]
```

### Switching Modes

- In voice mode, type: `text`
- In text mode, type: `voice`

### Commands

- `help` - Show help
- `quit` / `exit` - Exit
- `load <file>` - Load audio file
- `voice` / `text` - Switch modes

---

## 📊 API Methods

### VocalBridgeClient

#### Speech-to-Text

```python
client.speech_to_text(
    audio_data: bytes,
    format: str = "wav",      # wav, mp3, ogg
    language: str = "en-US"   # Language code
) -> str
```

#### Text-to-Speech

```python
client.text_to_speech(
    text: str,
    voice: str = "en-US-Neural2-A",  # Voice ID
    format: str = "mp3"               # mp3, wav, ogg
) -> bytes
```

#### Session Management

```python
# Create session
session_id = client.create_session(
    user_id: str,
    language: str = "en-US",
    voice: str = "en-US-Neural2-A"
)

# End session
client.end_session(session_id: str)
```

#### Utility Methods

```python
# List available voices
voices = client.get_available_voices(language="en-US")

# Health check
is_healthy = client.health_check()
```

### VoiceInterface

#### Start Conversation

```python
orch_session, voice_session = interface.start_voice_conversation(user_id: str)
```

#### Process Voice Input

```python
success, text, audio = interface.process_voice_input(
    audio_data: bytes,
    audio_format: str = "wav"
)
```

#### Process Text Input

```python
success, text, audio = interface.process_text_input(text: str)
```

#### End Conversation

```python
interface.end_conversation()
```

---

## 🧪 Testing

### Mock Mode (No API Key)

```env
USE_MOCK_APIS=true
```

All voice functions return mock data:
- STT returns: `"[Mock STT] User speech transcription"`
- TTS returns: `b"[Mock TTS audio bytes]"`

### With API Key

```env
USE_MOCK_APIS=false
VOCALBRIDGE_API_KEY=your_key
```

Real speech recognition and synthesis.

### Test Script

```python
from services import get_vocalbridge_client

client = get_vocalbridge_client()

# Test health
if client.health_check():
    print("✅ VocalBridge API is healthy")

# Test voices
voices = client.get_available_voices()
print(f"Available voices: {len(voices)}")

# Test TTS
audio = client.text_to_speech("Testing one two three")
print(f"Generated {len(audio)} bytes of audio")
```

---

## 🔒 Security

### Best Practices

1. **Never commit `.env`** with real API keys
2. **Use environment variables** in production
3. **Rotate keys regularly**
4. **Monitor API usage**
5. **Use HTTPS** for all API calls

### Production Deployment

```bash
# Set environment variable (don't use .env file)
export VOCALBRIDGE_API_KEY="your_production_key"
export USE_MOCK_APIS=false

# Run application
python3 voice_cli.py
```

### AWS Secrets Manager Example

```python
import boto3
from config import config

def get_vocalbridge_key():
    if config.environment == 'production':
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId='vocalbridge-api-key')
        return response['SecretString']
    else:
        return config.vocalbridge_api_key
```

---

## 🐛 Troubleshooting

### Issue: "VocalBridge API key not found"

**Solution:**
```bash
# Check .env file
cat .env | grep VOCALBRIDGE

# Should show (uncommented):
VOCALBRIDGE_API_KEY=your_key_here
```

### Issue: "requests library required"

**Solution:**
```bash
pip install requests
```

### Issue: "PyAudio not installed"

**Solution:**
```bash
# macOS
brew install portaudio
pip install pyaudio

# Ubuntu/Debian
sudo apt-get install portaudio19-dev
pip install pyaudio

# Windows
pip install pipwin
pipwin install pyaudio
```

### Issue: Mock mode still active

**Solution:**
```bash
# Edit .env
USE_MOCK_APIS=false
```

### Issue: API returns 401 Unauthorized

**Solution:**
- Check API key is correct
- Verify key hasn't expired
- Check endpoint URL is correct

---

## 📈 Performance

### Typical Response Times

- **STT (5 sec audio):** ~500ms - 1s
- **TTS (short phrase):** ~300ms - 500ms
- **Full round-trip:** ~1-2 seconds

### Optimization Tips

1. **Use streaming** for real-time conversations
2. **Cache TTS** for common responses
3. **Pre-generate** welcome messages
4. **Use appropriate audio formats** (MP3 for smaller size)
5. **Implement timeouts** for API calls

---

## 🔄 Migration from Text to Voice

### Phase 1: Text-Only (Current)

```python
# Text CLI
python3 main.py
```

### Phase 2: Hybrid (Text in, Voice out)

```python
# Text input, voice responses
python3 voice_cli.py
# Type: text mode
```

### Phase 3: Full Voice

```python
# Voice input and output
python3 voice_cli.py
# Press Enter to record
```

---

## 📚 Additional Resources

- VocalBridge API Documentation: (vendor-specific)
- Speech Recognition Best Practices
- Voice UI Design Guidelines
- Audio Format Specifications

---

## ✅ Checklist

Before going live with voice:

- [ ] VocalBridge API key added to `.env`
- [ ] `USE_MOCK_APIS=false` in `.env`
- [ ] Tested with sample audio files
- [ ] Microphone tested (if using)
- [ ] Error handling tested
- [ ] API rate limits understood
- [ ] Production keys in secrets manager
- [ ] Monitoring/logging configured

---

**Status:** ✅ VocalBridge integration complete and ready to use!

Add your API key to `.env` and run `python3 voice_cli.py` to start voice conversations.
