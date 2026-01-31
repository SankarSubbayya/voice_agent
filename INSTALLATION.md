# 🚀 ReturnFlow Voice Agent - Installation Guide

**Complete setup instructions for development and production**

---

## 📋 Prerequisites

- **Python 3.12+** (required)
- **Git** (for cloning the repository)
- **A VocalBridge API key** (get one at https://vocalbridgeai.com)

---

## ⚡ Quick Install (5 minutes)

### Step 1: Clone the Repository

```bash
git clone https://github.com/SankarSubbayya/voice_agent.git
cd voice_agent
```

### Step 2: Install Dependencies

**Option A: Using pip (recommended)**
```bash
pip install -r requirements.txt
```

**Option B: Using uv (faster)**
```bash
uv pip install -r requirements.txt
```

**Option C: Using the project file**
```bash
pip install -e .
```

### Step 3: Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys
nano .env
```

**Add your credentials:**
```env
# VocalBridge Configuration
VOCALBRIDGE_API_KEY=vb_your_api_key_here
VOCALBRIDGE_ENDPOINT=https://vocalbridgeai.com/api/v1

# OpenAI Configuration (for agents)
OPENAI_API_KEY=sk-your_openai_key_here
```

**⚠️ Important:** Do NOT use quotes around values in .env file!

### Step 4: Verify Installation

```bash
python3 tools/testing/verify_setup.py
```

**Expected output:**
```
✅ Config module: OK
✅ API Key: Valid (vb_...)
✅ Endpoint: https://vocalbridgeai.com/api/v1
✅ Client Module: OK
✅ API Connection: OK
✅ LiveKit Credentials: OK

Total: 6 passed, 0 failed
🎉 ALL CHECKS PASSED!
```

### Step 5: Start the Server

```bash
python3 working_voice_server.py
```

**Server will start on:** http://localhost:5040

Open your browser and start talking to your voice agent!

---

## 📦 Dependencies Explained

### Core Dependencies

**flask (>=3.0.0)**
- Web framework for the backend server
- Handles HTTP requests and static file serving
- Used for: API proxy, credential endpoint, HTML interface

**requests (>=2.31.0)**
- HTTP client library
- Used for: VocalBridge API calls
- Handles authentication and error responses

**python-dotenv (>=1.0.0)**
- Environment variable management
- Loads API keys from .env file
- Keeps secrets out of code

### Optional Dependencies

**gunicorn (>=21.2.0)**
- Production WSGI server
- Use instead of Flask's development server
- Required for production deployment

**pytest (>=7.4.0)**
- Testing framework
- Run test suite: `pytest tools/testing/`

**black (>=23.0.0)**
- Code formatter
- Format code: `black .`

**flake8 (>=6.0.0)**
- Code linter
- Check code: `flake8 .`

---

## 🔧 Installation Methods

### Method 1: pip install (Standard)

```bash
# Install core dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep -E "flask|requests|python-dotenv"
```

### Method 2: uv install (Fast)

```bash
# Install uv first (if not installed)
pip install uv

# Install dependencies (much faster than pip)
uv pip install -r requirements.txt
```

### Method 3: Virtual Environment (Recommended for Development)

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# OR
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt

# Deactivate when done
deactivate
```

### Method 4: Development Install (Editable)

```bash
# Install in editable mode (for development)
pip install -e .

# This allows you to modify code and see changes immediately
```

---

## 🐳 Docker Installation (Optional)

### Using Docker Compose (Easiest)

```bash
# Build and run
docker-compose up

# Server available at http://localhost:5040
```

### Using Dockerfile

```bash
# Build image
docker build -t voice-agent .

# Run container
docker run -p 5040:5040 --env-file .env voice-agent
```

**Note:** Docker files are not included yet but can be added.

---

## 🌐 Production Installation

### Step 1: Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3.12 python3-pip git nginx

# CentOS/RHEL
sudo yum install python3.12 python3-pip git nginx
```

### Step 2: Clone and Install

```bash
# Clone repository
cd /var/www
sudo git clone https://github.com/SankarSubbayya/voice_agent.git
cd voice_agent

# Install dependencies
sudo pip install -r requirements.txt
sudo pip install gunicorn
```

### Step 3: Configure Environment

```bash
# Create .env file
sudo nano .env

# Add production credentials
VOCALBRIDGE_API_KEY=vb_production_key_here
VOCALBRIDGE_ENDPOINT=https://vocalbridgeai.com/api/v1
```

### Step 4: Run with Gunicorn

```bash
# Production server (4 workers)
gunicorn -w 4 -b 0.0.0.0:5040 working_voice_server:app
```

### Step 5: Configure nginx (Optional)

```nginx
# /etc/nginx/sites-available/voice-agent
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5040;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static {
        alias /var/www/voice_agent/static;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/voice-agent /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🧪 Testing Installation

### Run Test Suite

```bash
# Quick verification (6 checks)
python3 tools/testing/verify_setup.py

# Complete API test suite (6 tests)
python3 tools/testing/test_vocalbridge_complete.py

# All tests (if pytest installed)
pytest tools/testing/
```

### Manual Testing

```bash
# Start server
python3 working_voice_server.py

# In another terminal, test API
curl http://localhost:5040/api/credentials

# Expected: JSON response with LiveKit credentials
```

---

## 🔍 Troubleshooting

### Issue: "Module not found" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Or with uv
uv pip install -r requirements.txt --reinstall
```

### Issue: "VOCALBRIDGE_API_KEY not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check .env file content (no quotes!)
cat .env

# Verify environment loading
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('VOCALBRIDGE_API_KEY'))"
```

### Issue: Port 5040 already in use

**Solution:**
```bash
# Find process using port 5040
lsof -i :5040

# Kill the process
kill -9 <PID>

# Or use a different port
python3 working_voice_server.py --port 5041
```

### Issue: 401 Unauthorized from VocalBridge

**Solution:**
```bash
# Check API key format (NO QUOTES!)
# WRONG: VOCALBRIDGE_API_KEY='vb_...'
# RIGHT: VOCALBRIDGE_API_KEY=vb_...

# Test API key directly
curl -H "X-API-Key: vb_your_key_here" https://vocalbridgeai.com/api/v1/token
```

### Issue: LiveKit SDK not loading

**Solution:**
```bash
# Verify SDK file exists
ls -lh static/livekit-client.js

# Should be ~332KB
# If missing, download it:
curl -L "https://cdn.jsdelivr.net/npm/livekit-client@1.15.0/dist/livekit-client.umd.min.js" \
  -o static/livekit-client.js
```

---

## 📊 Verify Everything Works

### Checklist

- [ ] Python 3.12+ installed
- [ ] Dependencies installed (pip list shows flask, requests, python-dotenv)
- [ ] .env file created with API keys (no quotes!)
- [ ] Verification script passes (6/6)
- [ ] Server starts on port 5040
- [ ] Browser opens to http://localhost:5040
- [ ] SDK status shows green "✅ LiveKit SDK Loaded"
- [ ] "Get Credentials" button works
- [ ] "Start Voice Call" button works
- [ ] Microphone permission granted
- [ ] Can hear agent speaking

---

## 🆘 Getting Help

**Check Documentation:**
- README.md - Project overview
- START_HERE.md - Quick start guide
- DEBUG_INSTRUCTIONS.md - Debugging help

**Run Diagnostics:**
```bash
python3 tools/testing/verify_setup.py
```

**Check Logs:**
```bash
# Server logs show in terminal where you ran working_voice_server.py
```

**GitHub Issues:**
https://github.com/SankarSubbayya/voice_agent/issues

---

## ✅ Installation Complete!

If all checks pass, you're ready to use ReturnFlow Voice Agent.

**Next Steps:**
1. Read START_HERE.md for usage guide
2. Try the demo: http://localhost:5040
3. Review VOICE_AGENT_READY.md for detailed testing

**Enjoy your voice agent!** 🎉

---

**Last Updated:** 2026-01-31
**Version:** 1.0.0
