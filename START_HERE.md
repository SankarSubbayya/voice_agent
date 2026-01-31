# 🎙️ Start Here - Test Your Voice Agent

## ✅ Quick Start (One Command)

```bash
python3 voice_test_server.py
```

That's it! The browser will open automatically.

---

## 📋 What Happens:

1. **Server starts** on `http://localhost:5040`
2. **Browser opens** automatically
3. **Page loads** with:
   - ✅ LiveKit SDK Ready (wait for this!)
   - Button: "Step 1: Get Credentials"

---

## 🎯 Follow These Steps:

### **Step 1:** Wait for SDK
The page will show:
```
✅ LiveKit SDK Ready
```
Once you see this green checkmark, proceed.

### **Step 2:** Click "Get Credentials"
Should immediately show:
```
✅ Ready to Connect
Click "Start Voice Call"
```

### **Step 3:** Click "Start Voice Call"
- Browser will ask for **microphone permission** → Click **Allow**
- Wait for:
  ```
  ✅ Connected to LiveKit room!
  🎤 Microphone enabled!
  🗣️  START SPEAKING NOW!
  ```

### **Step 4:** Start Talking!
Say: **"I want to return my headphones to Amazon"**

The agent should respond within 2-3 seconds!

---

## 🎤 What to Expect:

**Agent will say:**
> "Welcome to Vice Agent. Are you looking to return an item to Amazon or Walmart today?"

**You respond:** "Amazon"

**Agent continues:**
> "I can help with that. What type of item would you like to return?"

**Continue the conversation naturally!**

---

## 📊 Watch the Log

At the bottom of the page, you'll see a black log box showing:

```
[7:24:11 AM] Voice test interface loaded
[7:24:11 AM] Waiting for LiveKit SDK...
[7:24:12 AM] ✅ LiveKit SDK loaded successfully!
[7:24:15 AM] Requesting credentials from backend...
[7:24:16 AM] ✅ Credentials received!
[7:24:16 AM] Room: user-633715bf-agent-953ece37-api-xxxxx
[7:24:20 AM] Connecting to LiveKit room...
[7:24:22 AM] ✅ Connected to LiveKit room!
[7:24:23 AM] 🎤 Microphone enabled!
[7:24:23 AM] 🗣️  START SPEAKING NOW!
[7:24:25 AM] 🔊 Agent audio track received!
[7:24:26 AM] ▶️  Audio playback started
```

Look for:
- ✅ **Green** = Success
- ❌ **Red** = Error
- ⚠️ **Orange** = Warning
- 📡 **Blue** = Info

---

## 🐛 Troubleshooting:

### Issue: "LiveKit SDK not loaded"
**Solution:** Wait a few seconds, it will retry automatically. Or refresh the page.

### Issue: No sound from agent
**Check:**
- ✅ Speaker/headphone volume turned up?
- ✅ See "🔊 Agent audio received!" in log?
- ✅ See "▶️ Audio playback started"?

If yes to all but still no sound:
- Try saying something to trigger a response
- Check browser audio settings

### Issue: Microphone not working
**Check:**
- ✅ Did you click "Allow" when browser asked?
- ✅ Browser shows microphone icon in address bar?
- ✅ Try using Chrome or Edge (best LiveKit support)

### Issue: Agent doesn't respond
**Wait 2-3 seconds** after speaking. The agent needs time to:
1. Process your speech (STT)
2. Generate response (GPT-4)
3. Create audio (TTS)
4. Stream it back

This typically takes 2-3 seconds total.

---

## ⏹️ Stop the Server:

Press **Ctrl+C** in the terminal where you ran the command.

---

## 🔧 Alternative: Quick Verification

To just verify everything is set up (no browser):

```bash
python3 verify_setup.py
```

Should show:
```
Total: 6 passed, 0 failed
🎉 ALL CHECKS PASSED!
```

---

## 📚 More Info:

- **Full Testing Guide:** `HOW_TO_TEST.md`
- **Integration Details:** `VOCAL_BRIDGE_SUCCESS.md`
- **Setup Status:** `VOCALBRIDGE_STATUS.md`

---

## ✅ Current Status:

**Everything is working and ready to test!**

- ✅ API: Working
- ✅ Credentials: Valid
- ✅ Server: Running (port 5040)
- ✅ LiveKit SDK: Fixed and loading properly
- ✅ CORS: No issues (using Flask backend)

**Your Agent:**
- Name: "Vice Agent"
- Voice: ElevenLabs Flash v2.5
- Model: GPT-4 Realtime
- Purpose: Amazon & Walmart returns

---

## 🚀 Ready?

```bash
python3 voice_test_server.py
```

Start testing your voice agent now!
