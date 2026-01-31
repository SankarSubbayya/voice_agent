# How to Test Your Vocal Bridge Voice Agent

## ✅ The Problem You Encountered

When you opened `test_vocal_bridge_live.html` directly in your browser, you saw:
```
❌ ERROR: Failed to fetch
```

**Why this happened:**
- Opening HTML files directly (`file://`) causes **CORS (Cross-Origin Resource Sharing)** errors
- Browsers block JavaScript from making API calls from `file://` URLs for security
- This is a browser security feature, not a problem with your code or API

**The Solution:**
Run the HTML through a web server instead of opening it directly.

---

## 🚀 How to Test (3 Methods)

### **Method 1: Flask Server (RECOMMENDED)** ⭐

This method uses a Python Flask server that proxies requests to avoid CORS issues.

```bash
python3 simple_voice_test.py
```

**What happens:**
1. ✅ Flask server starts on `http://localhost:5000`
2. 🌐 Browser opens automatically
3. 📝 Clean interface with no CORS errors
4. 🎤 Click buttons to test voice

**Steps in browser:**
1. Click **"Step 1: Get Credentials"**
   → Should see: ✅ Credentials Retrieved
   → Shows LiveKit URL and room name

2. Click **"Step 2: Start Voice Call"**
   → Allow microphone when prompted
   → Should see: ✅ Connected to room!

3. **Start Speaking!**
   → Say: "I want to return my headphones to Amazon"
   → Agent should respond with voice within 2-3 seconds

4. Watch the **log** at bottom for events

**To stop server:** Press `Ctrl+C` in terminal

---

### **Method 2: Simple HTTP Server**

If you don't want to use Flask, use Python's built-in HTTP server:

```bash
cd /Users/sankar/projects/voice_agent
python3 -m http.server 8000
```

Then open in browser:
```
http://localhost:8000/test_vocal_bridge_live.html
```

**Note:** This method still has CORS issues because the JavaScript makes direct API calls. Use Method 1 instead.

---

### **Method 3: Direct API Test (No Browser)**

Test the API works without a browser:

```bash
python3 verify_setup.py
```

**This verifies:**
- ✅ Config module loaded
- ✅ API key valid
- ✅ Endpoint correct
- ✅ API connection working
- ✅ LiveKit credentials retrieved
- ✅ Demo files present

**Expected output:**
```
Total: 6 passed, 0 failed
🎉 ALL CHECKS PASSED!
```

---

## 🎯 What Success Looks Like

### ✅ When Everything Works:

**Step 1 - Get Credentials:**
```
✅ Credentials Retrieved
LiveKit URL: wss://tutor-j7bhwjbm.livekit.cloud
Room: user-633715bf-agent-953ece37-api-xxxxx
Expires in: 3600 seconds
```

**Step 2 - Start Call:**
```
✅ Connected to room!
🎤 Microphone enabled
🔊 Agent audio track received!
```

**Step 3 - Conversation:**
```
You: "I want to return my headphones to Amazon"
Agent: (speaks) "Welcome to Vice Agent. I can help you with that return..."
```

**Log shows:**
```
[7:15:01 AM] Voice test interface loaded
[7:15:05 AM] Requesting credentials from backend...
[7:15:06 AM] ✅ Credentials received!
[7:15:10 AM] Connecting to LiveKit...
[7:15:12 AM] ✅ Connected to room!
[7:15:13 AM] 🎤 Microphone enabled
[7:15:15 AM] 🔊 Agent audio received!
```

---

## 🐛 Troubleshooting

### Issue: "Failed to fetch"
**Cause:** Opening HTML file directly
**Fix:** Use Method 1 (Flask server)

### Issue: No sound from agent
**Checks:**
- ✅ Is speaker/headphone volume up?
- ✅ Do you see "🔊 Agent audio received!" in log?
- ✅ Try saying something to trigger agent response

### Issue: Microphone not working
**Checks:**
- ✅ Did you allow microphone permission?
- ✅ Check browser shows microphone icon
- ✅ Try Chrome or Edge (best LiveKit support)

### Issue: Agent doesn't respond
**Checks:**
- ✅ Wait 2-3 seconds after speaking
- ✅ Check Vocal Bridge dashboard → Call Logs
- ✅ Verify your agent status is "Active"
- ✅ Speak clearly and wait for response

### Issue: Connection fails
**Checks:**
- ✅ Internet connection working?
- ✅ Run `python3 verify_setup.py` to test API
- ✅ Check `.env` file has correct API key (no quotes)

---

## 📊 Current Status

**API Status:** ✅ WORKING
```bash
$ python3 verify_setup.py
Total: 6 passed, 0 failed
🎉 ALL CHECKS PASSED!
```

**Your Configuration:**
- API Key: `vb_iHqvM80Ey1o8HqNxZn19w4o6o-0h8LDQuRgZQxQ6wcw` ✅
- Endpoint: `https://vocalbridgeai.com/api/v1` ✅
- Agent: "Vice Agent" (return processing) ✅
- Voice: ElevenLabs Flash v2.5 ✅
- Model: GPT-4 Realtime ✅

---

## 🎬 Quick Start Command

```bash
python3 simple_voice_test.py
```

That's it! Browser will open, follow the 3 steps, and start talking to your voice agent.

---

## 📁 Test Files Available

1. **simple_voice_test.py** - Flask server (BEST option)
2. **test_vocal_bridge_live.html** - Web interface
3. **verify_setup.py** - Quick verification
4. **test_voice_agent.py** - Guided test with browser opener

---

## 💡 What Your Agent Will Do

**Your "Vice Agent" is configured to:**
1. Greet you professionally
2. Ask: "Amazon or Walmart?"
3. Request: "What item are you returning?"
4. Ask: "What's your order number?"
5. Ask: "What's the reason for return?"
6. Confirm all details
7. Provide next steps

**Example conversation:**
```
Agent: "Welcome to Vice Agent. Are you looking to return
        an item to Amazon or Walmart today?"

You:   "Amazon"

Agent: "I can help with that. What type of item would you
        like to return?"

You:   "Headphones"

Agent: "May I have the order number for that purchase, please?"

... and so on
```

---

## ✅ Ready to Test!

**Run this now:**
```bash
python3 simple_voice_test.py
```

The browser will open automatically with everything configured and ready to test your voice agent!

---

**Last Updated:** 2026-01-31
**Status:** Fully operational, ready for voice testing
**Method:** Flask server avoids CORS issues
