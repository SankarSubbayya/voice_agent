"""
ReturnFlow Voice Agent - Main Entry Point

A multi-agent conversational system for handling product returns through voice.
Built on VocalBridge AI architecture.
"""

from database.mock_db import MockDatabase
from services.orchestrator import VoiceOrchestrator


def print_banner():
    """Print the application banner."""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         📦 ReturnFlow Voice Agent (V1)                       ║
║         Built on: VocalBridge AI                             ║
║                                                               ║
║         Voice-enabled product returns made simple            ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_help():
    """Print help information."""
    help_text = """
Available Commands:
  - Type your requests naturally (e.g., "I want to return my headphones")
  - 'help' - Show this help message
  - 'demo' - Run the demo scenario from the PRD
  - 'users' - List available test users
  - 'quit' or 'exit' - Exit the application

Example Phrases:
  - "I want to return something I bought last week"
  - "Where is my refund?"
  - "Track my return"
  - "How do I pack this item?"
  - "I need help with a return"
    """
    print(help_text)


def run_demo_scenario(orchestrator: VoiceOrchestrator):
    """Run the hackathon demo script from the PRD."""
    print("\n" + "="*60)
    print("Running Demo Scenario (from PRD)")
    print("="*60 + "\n")

    # Start session for demo user
    session_id = orchestrator.start_conversation("USER001")
    orchestrator.identify_user(session_id, user_id="USER001")

    demo_steps = [
        "I want to return my headphones",
        "first order",
        "headphones",
        "damaged",  # Item selection will trigger, but then we need to give reason again
        "It was broken when it arrived",  # The actual reason
        "yes",  # Accept packaging help
        "Where is the nearest UPS?",
        "no thanks",
    ]

    for i, user_input in enumerate(demo_steps, 1):
        print(f"\n[Step {i}] User: {user_input}")
        success, response, data = orchestrator.process_input(session_id, user_input)
        print(f"Agent: {response}")

        if not success and "Session not found" in response:
            break

    print("\n" + "="*60)
    print("Demo Complete!")
    print("="*60 + "\n")

    orchestrator.end_conversation(session_id)


def list_users(db: MockDatabase):
    """List available test users."""
    print("\n" + "="*60)
    print("Available Test Users")
    print("="*60)

    for user_id, user in db.users.items():
        print(f"\nUser ID: {user_id}")
        print(f"Name: {user.name}")
        print(f"Phone: {user.phone}")
        print(f"Email: {user.email}")
        print(f"Return Count: {user.return_count}")
        print(f"Account Age: {user.account_age_days} days")
        print("-" * 40)

    print()


def interactive_mode():
    """Run the interactive CLI mode."""
    print_banner()
    print("\nWelcome to ReturnFlow Voice Agent!")
    print("Type 'help' for available commands or start talking naturally.\n")

    # Initialize database and orchestrator
    db = MockDatabase()
    orchestrator = VoiceOrchestrator(db)

    session_id = None
    current_user_id = None

    while True:
        try:
            user_input = input("\n🎤 You: ").strip()

            if not user_input:
                continue

            # Handle special commands
            if user_input.lower() in ['quit', 'exit', 'bye']:
                if session_id:
                    orchestrator.end_conversation(session_id)
                print("\n👋 Thanks for using ReturnFlow! Goodbye!\n")
                break

            elif user_input.lower() == 'help':
                print_help()
                continue

            elif user_input.lower() == 'demo':
                if session_id:
                    orchestrator.end_conversation(session_id)
                    session_id = None
                run_demo_scenario(orchestrator)
                continue

            elif user_input.lower() == 'users':
                list_users(db)
                continue

            # Start new session if needed
            if not session_id:
                # For demo purposes, default to USER001
                current_user_id = "USER001"
                session_id = orchestrator.start_conversation(current_user_id)
                orchestrator.identify_user(session_id, user_id=current_user_id)
                print(f"\n[System: Started new session for {db.get_user(current_user_id).name}]")

            # Process input
            success, response, data = orchestrator.process_input(session_id, user_input)

            print(f"\n🤖 Agent: {response}")

            # Check if conversation ended
            context = orchestrator.get_context(session_id)
            if context and context.get("current_agent") == "end":
                print("\n[System: Conversation ended. Starting new session on next input.]")
                orchestrator.end_conversation(session_id)
                session_id = None

        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!\n")
            if session_id:
                orchestrator.end_conversation(session_id)
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            print("Type 'help' for available commands.")


def main():
    """Main entry point."""
    interactive_mode()


if __name__ == "__main__":
    main()
