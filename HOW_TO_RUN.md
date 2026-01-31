# 🚀 How to Run ReturnFlow Voice Agent

**Quick reference guide for running the application**

---

## ⚡ Quick Start (30 seconds)

```bash
# Make sure you're in the project directory
cd /Users/sankar/projects/voice_agent

# Run the voice agent server
python3 working_voice_server.py
```

**That's it!** The browser will open automatically at http://localhost:5040

---

## 📋 Prerequisites Check

Before running, ensure:

### 1. Dependencies Installed
```bash
# Check if dependencies are installed
python3 -c "import flask; import requests; from dotenv import load_dotenv; print('✅ Dependencies OK')"
```

**If you get an error**, install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Variables Set
```bash
# Check if .env file exists
ls -la .env

# Verify API key is set
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', os.getenv('VOCALBRIDGE_API_KEY')[:10] + '...' if os.getenv('VOCALBRIDGE_API_KEY') else 'NOT SET')"
```

**If .env doesn't exist**, create it:
```bash
cp .env.example .env
nano .env  # Add your VOCALBRIDGE_API_KEY
```

### 3. LiveKit SDK File Exists
```bash
# Check if SDK file exists
ls -lh static/livekit-client.js
```

**If missing**, it should already be there. If not:
```bash
curl -L "https://cdn.jsdelivr.net/npm/livekit-client@1.15.0/dist/livekit-client.umd.min.js" \
  -o static/livekit-client.js
```

---

## 🎯 Running the Voice Agent (Primary Method)

### Method 1: Voice Server (Recommended)

**This is what you want for voice interactions.**

```bash
python3 working_voice_server.py
```

**What happens:**
1. Flask server starts on port 5040
2. Browser opens automatically to http://localhost:5040
3. You see the voice interface
4. Click "Get Credentials"
5. Click "Start Voice Call"
6. Allow microphone
7. Start talking!

**Output you'll see:**
```
╔═══════════════════════════════════════════════════════════╗
║            RETURNFLOW VOICE AGENT - TEST SERVER           ║
╚═══════════════════════════════════════════════════════════╝

Server Configuration:
  Port: 5040
  URL: http://localhost:5040

VocalBridge Status:
  ✅ API Key configured
  ✅ Endpoint: https://vocalbridgeai.com/api/v1

LiveKit SDK:
  ✅ Local SDK: static/livekit-client.js (332 KB)

Browser will open automatically in 1.5 seconds...

======================================================================
  TESTING STEPS
======================================================================

1️⃣  Click 'Get Credentials'
2️⃣  Click 'Start Voice Call'
3️⃣  Allow microphone
4️⃣  Say: 'I want to return my headphones to Amazon'

======================================================================

Press Ctrl+C to stop

 * Serving Flask app 'working_voice_server'
 * Debug mode: off
 * Running on http://127.0.0.1:5040
```

**To stop:** Press `Ctrl+C`

---

### Method 2: CLI Agent (Text-based)

**For text-based interactions (no voice).**

```bash
python3 main.py
```

**What happens:**
1. Text-based CLI interface starts
2. You type messages
3. Agent responds in text
4. No voice, no browser

**Example interaction:**
```
🎤 You: I want to return my headphones
🤖 Agent: I'll help you start a return. Let me look up your recent orders.

🎤 You: quit
```

**To stop:** Type `quit` or `exit`

---

## 🧪 Testing Before Running

### Quick Verification

```bash
# Run the verification script
python3 tools/testing/verify_setup.py
```

**Expected output:**
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

### Complete Test Suite

```bash
# Run all API tests
python3 tools/testing/test_vocalbridge_complete.py
```

**Expected output:**
```
Running VocalBridge Complete Test Suite
========================================

Test 1: Initialize Client
✅ Passed

Test 2: Get LiveKit Credentials
✅ Passed

...

========================================
RESULTS: 6 passed, 0 failed
🎉 ALL TESTS PASSED!
```

---

## 🔧 Different Running Options

### Run on Different Port

```bash
# Edit working_voice_server.py to change PORT variable
# Or run on different port (if implemented):
PORT=8080 python3 working_voice_server.py
```

### Run in Background

```bash
# Run in background
nohup python3 working_voice_server.py > server.log 2>&1 &

# Check if running
lsof -i :5040

# View logs
tail -f server.log

# Stop background server
pkill -f working_voice_server.py
```

### Run with Gunicorn (Production)

```bash
# Install gunicorn first
pip install gunicorn

# Run with 4 workers
gunicorn -w 4 -b 0.0.0.0:5040 working_voice_server:app
```

---

## 🌐 Accessing from Different Devices

### Local Access Only (Default)
```
http://localhost:5040
```

### Access from Same Network

**Step 1:** Find your IP address
```bash
# On macOS/Linux
ifconfig | grep "inet " | grep -v 127.0.0.1

# On Windows
ipconfig | findstr IPv4
```

**Step 2:** Update server to listen on all interfaces

Edit `working_voice_server.py`, change:
```python
app.run(debug=False, port=PORT, use_reloader=False)
```

To:
```python
app.run(debug=False, port=PORT, host='0.0.0.0', use_reloader=False)
```

**Step 3:** Access from other device
```
http://YOUR_IP_ADDRESS:5040
```

**⚠️ Note:** Microphone access requires HTTPS for remote devices.

---

## 📱 What You Should See

### In Browser

**Initial Load:**
```
┌─────────────────────────────────────────┐
│  ReturnFlow Voice Agent                 │
├─────────────────────────────────────────┤
│                                         │
│  ✅ LiveKit SDK Loaded (Local)          │
│                                         │
│  Status: Ready                          │
│  Click "Get Credentials" to start       │
│                                         │
│  [Step 1: Get Credentials]              │
│                                         │
└─────────────────────────────────────────┘
```

**After Clicking "Get Credentials":**
```
┌─────────────────────────────────────────┐
│  Status: ✅ Ready to Connect             │
│  Click "Start Voice Call"               │
│                                         │
│  [Step 2: Start Voice Call]             │
│                                         │
│  Log:                                   │
│  [7:42:15 AM] ✅ Credentials received!   │
│  [7:42:15 AM] Room: user-633715bf...    │
└─────────────────────────────────────────┘
```

**After Starting Call:**
```
┌─────────────────────────────────────────┐
│  Status: ✅ LIVE!                        │
│  🗣️ START SPEAKING NOW!                 │
│                                         │
│  [Stop Call]                            │
│                                         │
│  Log:                                   │
│  [7:42:20 AM] ✅ Connected to LiveKit!   │
│  [7:42:21 AM] 🎤 Microphone enabled!     │
│  [7:42:21 AM] 🗣️ START SPEAKING NOW!    │
└─────────────────────────────────────────┘
```

### In Terminal

```
 * Serving Flask app 'working_voice_server'
 * Running on http://127.0.0.1:5040
127.0.0.1 - - [31/Jan/2026 07:42:15] "GET / HTTP/1.1" 200 -
127.0.0.1 - - [31/Jan/2026 07:42:15] "GET /static/livekit-client.js HTTP/1.1" 200 -
127.0.0.1 - - [31/Jan/2026 07:42:16] "GET /api/credentials HTTP/1.1" 200 -
```

---

## 🐛 Troubleshooting

### Server Won't Start

**Error: "Address already in use"**
```bash
# Find what's using port 5040
lsof -i :5040

# Kill it
kill -9 <PID>
```

**Error: "Module not found"**
```bash
# Install dependencies
pip install -r requirements.txt
```

**Error: "VOCALBRIDGE_API_KEY not found"**
```bash
# Check .env file
cat .env

# Make sure no quotes around the value!
# WRONG: VOCALBRIDGE_API_KEY='vb_...'
# RIGHT: VOCALBRIDGE_API_KEY=vb_...
```

### Browser Shows Errors

**Error: "LiveKit SDK Failed to Load"**
```bash
# Check SDK file exists
ls -lh static/livekit-client.js

# Should be ~332KB
# Hard refresh browser: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
```

**Error: "Failed to fetch"**
- This usually means the server isn't running
- Check terminal for errors
- Restart the server

**Error: "Microphone not working"**
- Click "Allow" when browser asks for microphone permission
- Check System Preferences → Security & Privacy → Microphone
- Try Chrome or Edge (best LiveKit support)

### Agent Not Responding

**Check these:**
1. Wait 2-3 seconds (processing takes time)
2. Speak clearly and loudly
3. Check internet connection
4. Look for errors in browser console (F12)
5. Check terminal for API errors

---

## 📊 Monitoring While Running

### View Logs in Real-Time

**Terminal logs** (automatic):
- Shows HTTP requests
- Shows errors if any
- Shows server status

**Browser console** (F12):
```
[LiveKit] Connected to room
[LiveKit] Track subscribed: audio
[Audio] Agent speech detected
```

### Check API Status

**While server is running:**
```bash
# Test credentials endpoint
curl http://localhost:5040/api/credentials

# Should return JSON with LiveKit credentials
```

### Check System Resources

```bash
# CPU and memory usage
ps aux | grep python3

# Network connections
lsof -i :5040
```

---

## ⏹️ Stopping the Application

### Stop Voice Server

**If running in terminal:**
- Press `Ctrl+C`

**If running in background:**
```bash
# Find process
ps aux | grep working_voice_server

# Kill it
kill -9 <PID>

# Or kill all Python processes (careful!)
pkill -f working_voice_server.py
```

### Verify It Stopped

```bash
# Should return nothing
lsof -i :5040
```

---

## 🔄 Restart After Changes

### If you modified code:

```bash
# Stop server (Ctrl+C)
# Make your changes
# Restart server
python3 working_voice_server.py
```

### If you updated dependencies:

```bash
# Stop server
# Update dependencies
pip install -r requirements.txt

# Restart server
python3 working_voice_server.py
```

### If you changed .env:

```bash
# Stop server
# Edit .env
nano .env

# Restart server (will load new .env)
python3 working_voice_server.py
```

---

## 📝 Summary

**To run the voice agent:**
```bash
python3 working_voice_server.py
```

**To test without browser:**
```bash
python3 tools/testing/verify_setup.py
```

**To use text-based CLI:**
```bash
python3 main.py
```

**To stop:**
- Press `Ctrl+C`

**Default URL:**
- http://localhost:5040

**That's it!** 🚀

---

## 🆘 Quick Help

**Not working?**
1. Run: `python3 tools/testing/verify_setup.py`
2. Check: `cat .env` (no quotes around API key!)
3. Check: `ls static/livekit-client.js` (should exist)
4. Check: `pip list | grep -E "flask|requests|dotenv"` (should show versions)

**Still stuck?**
- Read: DEBUG_INSTRUCTIONS.md
- Read: INSTALLATION.md
- Check: https://github.com/SankarSubbayya/voice_agent

---

**Last Updated:** 2026-01-31
**Version:** 1.0.0
