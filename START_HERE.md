# 🎙️ Start Here - Test Your Voice Agent

## ✅ FIXED! Ready to Test (One Command)

```bash
python3 working_voice_server.py
```

**What was fixed**: LiveKit SDK now loads correctly from local server.

---

## 🚀 Server is Already Running!

The server is currently running on **http://localhost:5040**

Just open your browser to:
```
http://localhost:5040
```

---

## 📋 What You'll See:

1. **Page loads** with a **green box**:
   ```
   ✅ LiveKit SDK Loaded (Local)
   ```
   ⚠️ If you see a red error, refresh the page (Cmd+R or Ctrl+R)

2. **Status box** says:
   ```
   Ready
   Click "Get Credentials" to start
   ```

3. **Two buttons**:
   - "Step 1: Get Credentials"
   - "Step 2: Start Voice Call" (hidden initially)

---

## 🎯 Follow These 4 Simple Steps:

### **Step 1:** Click "Get Credentials"
Should immediately show:
```
✅ Ready to Connect
Click "Start Voice Call"
```

The second button will appear!

### **Step 2:** Click "Start Voice Call"
- Browser asks for **microphone permission** → Click **Allow**
- Wait for green messages in the log:
  ```
  ✅ Connected to LiveKit room!
  🎤 Microphone enabled!
  🗣️  START SPEAKING NOW!
  ```

### **Step 3:** Start Talking!
Say clearly:
```
"I want to return my headphones to Amazon"
```

### **Step 4:** Listen for Agent Response
Within 2-3 seconds, the agent will speak:
> "Welcome to Vice Agent. Are you looking to return an item to Amazon or Walmart today?"

**Keep talking naturally!** The agent will guide you through the return process.

---

## 🎤 Expected Conversation Flow:

```
Agent: "Welcome to Vice Agent. Are you looking to return
        an item to Amazon or Walmart today?"

You:   "Amazon"

Agent: "I can help with that. What type of item would you
        like to return?"

You:   "Headphones"

Agent: "May I have the order number for that purchase, please?"

You:   "123456789"

Agent: "What is the reason for your return?"

You:   "They don't fit properly"

Agent: "Let me confirm the details..."
```

---

## 📊 Watch the Log (Black Box at Bottom)

Real-time updates showing what's happening:

```
[7:42:11 AM] Voice test interface ready
[7:42:11 AM] LiveKit loaded from local server
[7:42:15 AM] Requesting credentials from backend...
[7:42:16 AM] ✅ Credentials received!
[7:42:16 AM] LiveKit URL: wss://tutor-j7bhwjbm.livekit.cloud
[7:42:16 AM] Room: user-633715bf-agent-953ece37-api-xxxxx
[7:42:20 AM] Connecting to LiveKit room...
[7:42:22 AM] ✅ Connected to LiveKit room!
[7:42:23 AM] 🎤 Microphone enabled!
[7:42:23 AM] 🗣️  START SPEAKING NOW!
[7:42:25 AM] 🔊 AGENT AUDIO RECEIVED!
[7:42:25 AM] You should hear the agent speaking!
[7:42:26 AM] ▶️  Audio playing
```

Color coding:
- ✅ **Green** = Success
- ❌ **Red** = Error
- ⚠️ **Orange** = Warning
- 📡 **Blue** = Info

---

## 🐛 Troubleshooting:

### Issue: Still see "❌ LiveKit SDK Failed"
**Fix**: Hard refresh the page
- Mac: **Cmd+Shift+R**
- Windows: **Ctrl+Shift+R**
- Or clear browser cache

### Issue: No sound from agent
**Checks**:
1. ✅ Volume turned up?
2. ✅ See "🔊 AGENT AUDIO RECEIVED!" in log?
3. ✅ See "▶️ Audio playing"?
4. ✅ Browser tab not muted? (check icon in tab)

**Try**: Say something to trigger agent response

### Issue: Microphone not working
**Checks**:
1. ✅ Clicked "Allow" for microphone?
2. ✅ Browser shows microphone icon in address bar?
3. ✅ Using Chrome or Edge? (best LiveKit support)

**Fix**: Check System Preferences → Security & Privacy → Microphone

### Issue: Agent doesn't respond
**Wait 2-3 seconds!** Processing takes time:
1. Speech-to-text (STT)
2. GPT-4 response generation
3. Text-to-speech (TTS)
4. Audio streaming

**Also check**:
- Internet connection working?
- All green checkmarks in log?
- Speaking clearly and loudly enough?

---

## 🔧 Quick Verification (No Browser)

Verify all systems without opening browser:

```bash
python3 verify_setup.py
```

Expected output:
```
✅ Config module: OK
✅ API Key: Valid (vb_iHqvM80Ey...)
✅ Endpoint: https://vocalbridgeai.com/api/v1
✅ Client Module: OK
✅ API Connection: OK
✅ LiveKit Credentials: OK

Total: 6 passed, 0 failed
🎉 ALL CHECKS PASSED!
```

---

## ⏹️ Stop the Server:

Press **Ctrl+C** in the terminal window.

To restart:
```bash
python3 working_voice_server.py
```

---

## 📚 Additional Documentation:

- **VOICE_AGENT_READY.md** - Complete testing guide
- **LIVEKIT_SDK_FIX.md** - Technical details of recent fix
- **HOW_TO_TEST.md** - Detailed testing instructions
- **VOCAL_BRIDGE_SUCCESS.md** - Integration documentation

---

## ✅ System Status: ALL GREEN

- ✅ **API**: Connected and working
- ✅ **API Key**: Valid (no quotes issue)
- ✅ **LiveKit SDK**: Loading from local server (v1.15.0, 332KB)
- ✅ **Server**: Running on port 5040
- ✅ **CORS**: Fixed (Flask backend proxy)
- ✅ **Export Name**: Fixed (`LivekitClient` with lowercase 'k')

**Your Agent Configuration:**
- **Name**: Vice Agent
- **Voice**: ElevenLabs Flash v2.5
- **Model**: GPT-4 Realtime
- **Purpose**: Amazon & Walmart returns processing

---

## 🎉 Everything is Working!

Just open your browser:
```
http://localhost:5040
```

Click the two buttons and start talking to your voice agent!

---

**Last Updated**: 2026-01-31 07:42 AM
**Status**: ✅ READY FOR TESTING
**Recent Fix**: LiveKit SDK export name (`LivekitClient`)
