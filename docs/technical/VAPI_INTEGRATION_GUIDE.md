# VAPI Integration Guide for ReturnFlow Voice Agent

## Overview

You're using **VAPI** (vapi.ai), not a generic VocalBridge service. VAPI is a complete voice agent platform that works differently from simple STT/TTS APIs.

## How VAPI Works

### Traditional STT/TTS API (what we initially built for):
```
Your App → Send audio → STT API → Get text
Your App → Send text → TTS API → Get audio
```

### VAPI (how it actually works):
```
Your App → Start call with Assistant ID → VAPI handles everything
VAPI manages: STT + LLM + TTS + conversation flow
Your App ← Receives events and can send function calls
```

## Integration Options

### Option 1: Web SDK (Recommended for your use case)
Use VAPI's Web SDK to add voice conversations directly in a web interface.

**Install:**
```bash
npm install @vapi-ai/web
```

**Usage:**
```javascript
import Vapi from '@vapi-ai/web';

// Initialize with PUBLIC key
const vapi = new Vapi('YOUR_PUBLIC_KEY_HERE');

// Start a call with your assistant
vapi.start('YOUR_ASSISTANT_ID');

// Listen to events
vapi.on('call-start', () => console.log('Call started'));
vapi.on('call-end', () => console.log('Call ended'));
vapi.on('message', (message) => console.log('Message:', message));
```

### Option 2: Server SDK (For backend automation)
Use VAPI's Server SDK to create outbound calls programmatically.

**Install:**
```bash
pip install vapi-python
```

**Usage:**
```python
from vapi import Vapi

# Initialize with PRIVATE key
vapi = Vapi(api_key='YOUR_PRIVATE_KEY_HERE')

# Create an outbound call
call = vapi.calls.create(
    assistant_id='YOUR_ASSISTANT_ID',
    customer={
        'number': '+1234567890'
    }
)
```

## API Key Types

VAPI uses two types of keys:

1. **Public Key** - For web/client-side applications
   - Format: Usually starts with `pk_` or similar
   - Used in browsers
   - Safe to expose in frontend code

2. **Private Key** - For server-side applications
   - Format: Usually starts with `sk_` or similar
   - Keep secret
   - Used for backend API calls

## Getting Your API Keys

1. Go to your VAPI dashboard: https://dashboard.vapi.ai
2. Click "API Keys" in the top right
3. You'll see both Public and Private keys
4. Copy the appropriate key for your use case

## Getting Your Assistant ID

From your screenshot, your assistant is named "voice_agent". To get the ID:

1. In the VAPI dashboard, go to your assistant
2. The assistant ID is in the URL or shown in the assistant details
3. Format: Usually a UUID like `12345678-1234-1234-1234-123456789012`

## Current Implementation Status

### What We Built
- Multi-agent orchestrator system (Intent Router, Purchase Retrieval, Classification, etc.)
- Complete return flow logic
- Mock STT/TTS for testing

### What Needs to Change for VAPI

VAPI doesn't provide raw STT/TTS APIs. Instead, it manages the entire conversation.

**Two integration approaches:**

#### Approach A: Use VAPI as Full Voice Interface
Let VAPI handle the entire voice conversation using its built-in LLM and your system prompt.

**Pros:**
- Easiest integration
- VAPI handles all voice aspects
- Just configure your prompt in VAPI dashboard

**Cons:**
- Your Python multi-agent system becomes unused
- All logic must be in VAPI's prompt or custom tools

#### Approach B: VAPI + Custom Tools (Recommended)
Use VAPI for voice, but call your Python agents as "custom tools" via API.

**How it works:**
1. User speaks → VAPI handles STT
2. VAPI's LLM determines intent
3. VAPI calls your Python backend as a "custom tool"
4. Your agents process the request
5. Return data to VAPI
6. VAPI speaks the response

**Implementation:**
```python
# Create Flask/FastAPI endpoint
@app.post("/tools/process-return")
def process_return(request_data):
    # Use your existing orchestrator
    success, response, data = orchestrator.process_input(
        session_id,
        request_data['message']
    )
    return {'response': response, 'data': data}
```

Then configure in VAPI dashboard:
- Add custom tool
- Point to your API endpoint
- VAPI will call it when needed

## Next Steps

1. **Get correct API keys from VAPI dashboard**
   - Click "API Keys" button
   - Note the key format (pk_ or sk_)

2. **Get your Assistant ID**
   - From your voice_agent assistant page

3. **Choose integration approach:**
   - Simple: Just use VAPI with system prompt
   - Advanced: VAPI + your Python agents as custom tools

4. **Update .env file:**
   ```env
   VAPI_PUBLIC_KEY=pk_...
   VAPI_PRIVATE_KEY=sk_...
   VAPI_ASSISTANT_ID=...
   ```

## Resources

- [VAPI Web SDK Docs](https://docs.vapi.ai/quickstart/web)
- [VAPI Server SDK Docs](https://docs.vapi.ai/quickstart/phone)
- [Custom Tools Guide](https://docs.vapi.ai/tools/custom-tools)
- [VAPI GitHub Examples](https://github.com/VapiAI/client-sdk-web)

## Questions?

The key you provided (`vb_...`) doesn't match VAPI's format. Please check your VAPI dashboard for the actual API keys.
