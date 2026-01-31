# 📦 ReturnFlow Voice Agent (V1)

A multi-agent conversational system that allows retail customers to initiate, process, track, and resolve product returns through natural voice conversation.

**Built on:** VocalBridge AI Architecture

## 🎯 Features

- **Voice-First Interface**: Natural conversation flow without complex menus
- **Multi-Agent System**: 6 specialized agents handling different stages
- **Complete Return Workflow**: From initiation to refund processing
- **Smart Classification**: Automatic return reason detection
- **Label Generation**: Mock shipping labels and QR codes
- **Package Tracking**: Real-time status updates
- **Dispute Resolution**: Conversational refund issue handling

## 🏗️ Architecture

```
User Input
    ↓
Intent Router Agent
    ↓
┌─────────────────────────────────┐
│ Purchase Retrieval Agent        │ → Fetches recent orders
│ Return Classification Agent     │ → Classifies return reason
│ Return Processing Agent         │ → Generates labels/QR codes
│ Logistics Agent                 │ → Packaging & drop-off help
│ Tracking & Refund Agent         │ → Status & dispute handling
└─────────────────────────────────┘
    ↓
Mock Retail Database
```

## 📁 Project Structure

```
voice_agent/
├── agents/                    # Specialized agent implementations
│   ├── base_agent.py         # Base agent class
│   ├── intent_router.py      # Routes user intents
│   ├── purchase_retrieval_agent.py
│   ├── return_classification_agent.py
│   ├── return_processing_agent.py
│   ├── logistics_agent.py
│   └── tracking_refund_agent.py
├── models/                    # Data models
│   ├── order.py
│   ├── return_request.py
│   ├── user.py
│   └── tracking.py
├── database/                  # Mock database
│   └── mock_db.py
├── services/                  # Orchestration services
│   └── orchestrator.py       # Main conversation coordinator
├── config.py                  # Environment configuration
├── .env.example              # Environment variables template
├── .env                      # Local environment (git-ignored)
├── main.py                    # CLI entry point
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- uv (Python package manager)

### Installation

1. Clone the repository:
```bash
cd /Users/sankar/projects/voice_agent
```

2. Set up environment (optional - works with defaults):
```bash
cp .env.example .env
# Edit .env to add API keys when needed
```

**Note:** The system works immediately with mock APIs - no API keys needed for development!

3. Install dependencies (if any are added):
```bash
uv sync
```

4. Run the application:
```bash
python main.py
```

Or with uv:
```bash
uv run python main.py
```

For environment setup details, see [ENV_SETUP.md](ENV_SETUP.md)

## 💡 Usage

### Interactive Mode

Start the application and interact naturally:

```
🎤 You: I want to return my headphones
🤖 Agent: I'll help you start a return. Let me look up your recent orders.

🎤 You: It arrived damaged
🤖 Agent: I'm sorry to hear the item arrived damaged...
```

### Available Commands

- `help` - Show help and example phrases
- `demo` - Run the automated demo scenario from the PRD
- `users` - List available test users
- `quit` or `exit` - Exit the application

### Example Conversations

**Starting a Return:**
```
You: I want to return something I bought last week
You: The wireless headphones
You: They're broken
```

**Tracking a Return:**
```
You: Where is my refund?
You: Track my return
```

**Getting Help:**
```
You: How do I pack this item?
You: Where is the nearest UPS?
```

## 🧪 Demo Scenario

Run the complete demo from the PRD:

```bash
python main.py
```

Then type `demo` to run through the full scenario:
1. Start return request
2. Select item
3. Classify reason
4. Generate label/QR
5. Get packaging help
6. Find drop-off location

## 📊 Test Data

The system includes mock data for testing:

### Test Users

- **USER001 - John Doe**
  - Phone: +1-555-0001
  - Email: john.doe@email.com
  - Has 2 recent orders with returns

- **USER002 - Jane Smith**
  - Phone: +1-555-0002
  - Email: jane.smith@email.com
  - Has 1 recent order, no returns

### Sample Orders

- Wireless Headphones - $149.99 (7 days ago)
- Running Shoes - $89.99 (14 days ago)
- Coffee Maker - $79.99 (3 days ago)

## 🎭 Agent Details

### 1. Intent Router
- Classifies user intent
- Routes to appropriate specialist
- Handles ambiguous requests

### 2. Purchase Retrieval Agent
- Fetches recent orders
- Helps user select items
- Validates return eligibility

### 3. Return Classification Agent
- Classifies return reasons
- Calculates fraud risk
- Checks return window

### 4. Return Processing Agent
- Generates return IDs
- Creates shipping labels
- Generates QR codes
- Calculates refunds

### 5. Logistics Agent
- Provides packaging instructions
- Finds drop-off locations
- Offers carrier options

### 6. Tracking & Refund Agent
- Provides tracking status
- Estimates refund timeline
- Handles disputes
- Escalates issues

## 📈 Success Metrics

- Return initiation time: < 90 seconds
- Intent accuracy: > 80%
- Conversation turns to classify: < 3
- Label generation success: > 95%

## 🔧 Development

### Adding New Features

1. Create new agent in `agents/`
2. Inherit from `BaseAgent`
3. Implement `process()` method
4. Register in orchestrator

### Extending the Database

1. Add new models in `models/`
2. Extend `MockDatabase` in `database/mock_db.py`
3. Update seed data as needed

## 🎯 Hackathon Scope (V1)

**Included:**
- ✅ Voice-based return initiation
- ✅ Order retrieval (mock data)
- ✅ Reason classification
- ✅ Mock label + QR generation
- ✅ Tracking status
- ✅ Basic dispute resolution

**Future Enhancements:**
- 🔮 Real carrier integration (UPS, USPS, FedEx)
- 🔮 Payment processing
- 🔮 Advanced ML fraud detection
- 🔮 Photo-based damage validation
- 🔮 Multi-language support
- 🔮 Sentiment detection

## 📝 License

Built for hackathon/educational purposes.

## 🤝 Contributing

This is a V1 hackathon project. Contributions and improvements are welcome!

## 📧 Contact

For questions about this implementation, refer to the PRD document: `ReturnFlow_Voice_Agent_PRD_Summary.md`

---

**Built with ❤️ for seamless voice-powered returns**
