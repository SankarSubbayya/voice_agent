# LiveKit SDK Loading Debug Instructions

## Current Status

The voice test server is running on **http://localhost:5040** with enhanced debugging.

## What I Changed

Added console debugging to identify what the LiveKit SDK actually exports to the browser's window object.

## What You Need To Do

1. **Open the page** (if not already open):
   ```
   http://localhost:5040
   ```

2. **Open Browser Developer Console**:
   - **Chrome/Edge**: Press `F12` or `Cmd+Option+J` (Mac) / `Ctrl+Shift+J` (Windows)
   - **Firefox**: Press `F12` or `Cmd+Option+K` (Mac) / `Ctrl+Shift+K` (Windows)
   - **Safari**: Enable Developer menu first (Safari > Preferences > Advanced > Show Develop menu), then `Cmd+Option+C`

3. **Look for the debug output**:
   You should see something like:
   ```
   === LiveKit SDK Debug ===
   window.LiveKitClient: undefined
   window.LivekitClient: undefined
   window.LiveKit: object    ← This tells us the actual export name!
   window.livekit: undefined
   Properties containing "live": [...]
   Properties containing "kit": [...]
   ========================
   ```

4. **Copy the debug output and share it with me**

   The key information I need:
   - Which of the checked properties shows `object` or `function` (not `undefined`)
   - What's listed in "Properties containing 'live'" or "Properties containing 'kit'"

## Why This Helps

The LiveKit SDK file (332KB) is loading correctly from the server, but the JavaScript variable name it exports to is not what we expected. Once we see what it actually exports, I can update the code to use the correct variable name.

## Alternative: Screenshot

If copying console output is difficult, just take a screenshot of the browser console showing the debug output.

---

**Server Running**: Port 5040
**SDK File**: /static/livekit-client.js (332,236 bytes)
**Status**: Waiting for browser console debug info
