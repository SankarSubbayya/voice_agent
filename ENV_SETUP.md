# Environment Setup Guide

## Quick Start (Development)

The system works **out of the box** with mock APIs - no API keys needed!

```bash
python3 main.py
```

The default `.env` file uses mock mode for all external services.

---

## Environment Variables

### Configuration Files

1. **`.env.example`** - Template file (safe to commit to git)
2. **`.env`** - Your actual configuration (git-ignored, already created)
3. **`config.py`** - Python module that loads environment variables

---

## Using Mock vs Real APIs

### Mock Mode (Default - Development)

```env
USE_MOCK_APIS=true
USE_MOCK_DATABASE=true
USE_MOCK_CARRIERS=true
```

**Features:**
- ✅ No API keys needed
- ✅ Works offline
- ✅ Fast for development
- ✅ Deterministic test data
- ❌ No real shipping labels
- ❌ No real payments
- ❌ No real voice recognition

### Production Mode

```env
USE_MOCK_APIS=false
USE_MOCK_DATABASE=false
USE_MOCK_CARRIERS=false
```

**Requirements:**
- Real API keys configured
- Database connection
- External services accessible

---

## API Key Setup

### 1. VocalBridge AI (Voice Platform)

```env
VOCALBRIDGE_API_KEY=your_api_key_here
VOCALBRIDGE_ENDPOINT=https://api.vocalbridge.ai/v1
```

**How to get:**
1. Sign up at vocalbridge.ai
2. Create a new application
3. Copy the API key

### 2. Speech Services (Alternative)

**Google Speech:**
```env
GOOGLE_SPEECH_API_KEY=your_key_here
```

**AWS (Transcribe + Polly):**
```env
AWS_ACCESS_KEY_ID=your_key_id
AWS_SECRET_ACCESS_KEY=your_secret
AWS_REGION=us-east-1
```

### 3. Carrier APIs (Shipping Labels)

**UPS:**
```env
UPS_API_KEY=your_key
UPS_CLIENT_ID=your_client_id
UPS_CLIENT_SECRET=your_secret
UPS_ACCOUNT_NUMBER=your_account
```

**USPS:**
```env
USPS_USER_ID=your_user_id
USPS_PASSWORD=your_password
```

**FedEx:**
```env
FEDEX_API_KEY=your_key
FEDEX_SECRET_KEY=your_secret
FEDEX_ACCOUNT_NUMBER=your_account
```

### 4. Payment Processing

**Stripe:**
```env
STRIPE_API_KEY=sk_test_...
STRIPE_SECRET_KEY=your_secret
```

**PayPal:**
```env
PAYPAL_CLIENT_ID=your_client_id
PAYPAL_CLIENT_SECRET=your_secret
PAYPAL_MODE=sandbox  # or 'live'
```

### 5. Notifications

**Twilio (SMS):**
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=+1234567890
```

**SendGrid (Email):**
```env
SENDGRID_API_KEY=SG.xxxxxxxxxxxx
SENDGRID_FROM_EMAIL=noreply@yourcompany.com
```

---

## Database Configuration

### Development (Mock Database)

```env
USE_MOCK_DATABASE=true
```

Uses in-memory mock database - no setup needed.

### Production (PostgreSQL)

```env
USE_MOCK_DATABASE=false
DATABASE_URL=postgresql://user:password@localhost:5432/returnflow
```

Or individual settings:
```env
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_NAME=returnflow
DATABASE_USER=your_user
DATABASE_PASSWORD=your_password
```

### Redis (Session Storage)

```env
REDIS_URL=redis://localhost:6379/0
```

---

## Using Configuration in Code

```python
from config import config

# Check mode
if config.use_mock_apis:
    print("Using mock APIs")
else:
    print("Using real APIs")

# Get API keys
if config.has_vocalbridge():
    api_key = config.vocalbridge_api_key
    # Initialize VocalBridge

# Business logic settings
return_window = config.default_return_window_days  # 30
fraud_threshold = config.fraud_risk_threshold      # 0.7
```

---

## Environment-Specific Setup

### Development

```env
ENVIRONMENT=development
DEBUG=true
USE_MOCK_APIS=true
LOG_LEVEL=DEBUG
```

### Staging

```env
ENVIRONMENT=staging
DEBUG=true
USE_MOCK_APIS=false
LOG_LEVEL=INFO
```

### Production

```env
ENVIRONMENT=production
DEBUG=false
USE_MOCK_APIS=false
LOG_LEVEL=WARNING
SECRET_KEY=<generate-strong-key>
JWT_SECRET=<generate-strong-key>
```

**⚠️ Security Warning:**
- Never use default `dev-*` secrets in production
- Use secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)
- Rotate keys regularly

---

## Validation

Check your configuration:

```python
from config import config

warnings = config.validate()
for warning in warnings:
    print(warning)
```

---

## Troubleshooting

### Issue: API keys not loading

**Solution:** Check that `.env` file exists and keys have no quotes:
```env
# ✅ Correct
API_KEY=abc123

# ❌ Wrong
API_KEY="abc123"
```

### Issue: Still using mocks in production

**Solution:** Verify environment variable:
```bash
echo $USE_MOCK_APIS
# Should be: false
```

### Issue: Database connection failed

**Solution:** Test database URL:
```bash
psql $DATABASE_URL
```

---

## Best Practices

1. **Never commit `.env`** - It's git-ignored
2. **Use `.env.example`** - Keep it updated as template
3. **One `.env` per environment** - dev, staging, prod
4. **Use secrets manager in production** - Not `.env` files
5. **Validate on startup** - Use `config.validate()`
6. **Rotate keys regularly** - Especially after team changes

---

## Migration Path

### Phase 1: Development (Current)
```
✅ Mock APIs
✅ Mock Database
✅ Text-based CLI
```

### Phase 2: Voice Integration
```
→ Add VocalBridge API key
→ Set USE_MOCK_APIS=false for voice
→ Keep other mocks for faster testing
```

### Phase 3: Carrier Integration
```
→ Add UPS/USPS/FedEx keys
→ Set USE_MOCK_CARRIERS=false
→ Test with real label generation
```

### Phase 4: Full Production
```
→ PostgreSQL database
→ Redis sessions
→ Payment processing
→ All real APIs
```

---

## Quick Reference

| Variable | Default | Purpose |
|----------|---------|---------|
| `ENVIRONMENT` | development | dev/staging/production |
| `USE_MOCK_APIS` | true | Use mock vs real APIs |
| `DEFAULT_RETURN_WINDOW_DAYS` | 30 | Return policy window |
| `FRAUD_RISK_THRESHOLD` | 0.7 | Fraud detection cutoff |
| `LOG_LEVEL` | INFO | Logging verbosity |

---

**Current Status:** ✅ Ready for development with mock APIs
**Next Step:** Add VocalBridge API key when ready for voice
