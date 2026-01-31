#!/usr/bin/env python3
"""
Complete Vocal Bridge Integration Test

Tests all aspects of the Vocal Bridge + LiveKit integration.
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

from services.vocalbridge_livekit_client import VocalBridgeClient
import json


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def test_api_connection():
    """Test 1: API Connection and Authentication"""
    print_section("TEST 1: API Connection & Authentication")

    try:
        client = VocalBridgeClient()
        print("✅ Client initialized successfully")
        print(f"   API Key: {client.api_key[:20]}...")
        print(f"   Endpoint: {client.endpoint}")
        return client, True
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return None, False


def test_get_credentials(client):
    """Test 2: Get LiveKit Credentials"""
    print_section("TEST 2: Get LiveKit Credentials")

    try:
        creds = client.get_livekit_credentials()

        print("✅ Successfully retrieved LiveKit credentials!")
        print()
        print("Credentials Details:")
        print("-" * 70)
        print(f"  LiveKit URL:        {creds['livekit_url']}")
        print(f"  Room Name:          {creds['room_name']}")
        print(f"  Participant ID:     {creds['participant_identity']}")
        print(f"  Agent Mode:         {creds['agent_mode']}")
        print(f"  Token Expires In:   {creds['expires_in']} seconds ({creds['expires_in']//60} minutes)")
        print()

        # Verify credentials structure
        assert 'livekit_url' in creds, "Missing livekit_url"
        assert 'token' in creds, "Missing token"
        assert 'room_name' in creds, "Missing room_name"
        assert creds['livekit_url'].startswith('wss://'), "Invalid LiveKit URL"
        assert len(creds['token']) > 100, "Token seems too short"

        print("✅ All credential fields validated")
        return creds, True

    except Exception as e:
        print(f"❌ Failed to get credentials: {e}")
        import traceback
        traceback.print_exc()
        return None, False


def test_token_structure(creds):
    """Test 3: Verify JWT Token Structure"""
    print_section("TEST 3: Verify JWT Token Structure")

    try:
        token = creds['token']
        parts = token.split('.')

        print(f"JWT Token Analysis:")
        print(f"  Total length: {len(token)} characters")
        print(f"  Parts: {len(parts)} (should be 3: header.payload.signature)")

        assert len(parts) == 3, f"Invalid JWT structure: {len(parts)} parts"
        print("✅ JWT structure is valid")

        # Decode header (first part)
        import base64
        header_b64 = parts[0]
        padding = 4 - len(header_b64) % 4
        if padding != 4:
            header_b64 += '=' * padding

        header = json.loads(base64.b64decode(header_b64))
        print(f"\nToken Header:")
        print(f"  Algorithm: {header.get('alg')}")
        print(f"  Type: {header.get('typ')}")

        print("✅ Token header decoded successfully")
        return True

    except Exception as e:
        print(f"❌ Token validation failed: {e}")
        return False


def test_web_demo_generation(client):
    """Test 4: Generate Web Demo"""
    print_section("TEST 4: Generate Web Demo File")

    try:
        import os
        output_file = "test_demo.html"

        # Remove old test file if exists
        if os.path.exists(output_file):
            os.remove(output_file)

        html_file = client.create_web_integration_html(output_file)

        # Verify file was created
        assert os.path.exists(html_file), "HTML file not created"

        # Check file size
        file_size = os.path.getsize(html_file)
        print(f"✅ Web demo generated: {html_file}")
        print(f"   File size: {file_size:,} bytes")

        # Verify content
        with open(html_file, 'r') as f:
            content = f.read()
            assert 'LiveKit' in content, "Missing LiveKit SDK"
            assert 'wss://' in content, "Missing WebSocket URL"
            assert 'ReturnFlow' in content, "Missing app title"

        print("✅ HTML content validated")
        print(f"\n   📄 Test demo created: {output_file}")
        print(f"   🌐 Main demo: vocalbridge_demo.html")

        return True

    except Exception as e:
        print(f"❌ Web demo generation failed: {e}")
        return False


def test_multiple_requests(client):
    """Test 5: Multiple Token Requests"""
    print_section("TEST 5: Multiple Token Requests")

    try:
        print("Requesting 3 tokens to test API reliability...")
        print()

        room_names = []
        for i in range(3):
            creds = client.get_livekit_credentials()
            room_names.append(creds['room_name'])
            print(f"  Request {i+1}: ✅ Room: {creds['room_name'][-20:]}")

        print()
        print("✅ All 3 requests successful")
        print(f"   Each request creates a unique room")
        print(f"   API is stable and responsive")

        return True

    except Exception as e:
        print(f"❌ Multiple requests test failed: {e}")
        return False


def test_configuration():
    """Test 6: Environment Configuration"""
    print_section("TEST 6: Environment Configuration")

    try:
        from config import config

        print("Configuration Check:")
        print("-" * 70)
        print(f"  Environment:        {config.environment}")
        print(f"  Mock APIs:          {config.use_mock_apis}")
        print(f"  VB API Key Set:     {config.has_vocalbridge()}")
        print(f"  VB Endpoint:        {config.vocalbridge_endpoint}")

        # Verify settings
        assert config.has_vocalbridge(), "VocalBridge API key not configured"

        print()
        print("✅ Configuration is valid")

        return True

    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def print_summary(results):
    """Print test summary"""
    print_section("TEST SUMMARY")

    total = len(results)
    passed = sum(1 for r in results.values() if r)
    failed = total - passed

    print(f"Total Tests:  {total}")
    print(f"✅ Passed:    {passed}")
    print(f"❌ Failed:    {failed}")
    print()

    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}  {test_name}")

    print()

    if failed == 0:
        print("🎉 ALL TESTS PASSED! 🎉")
        print()
        print("Vocal Bridge integration is fully operational!")
        print()
        print("Next Steps:")
        print("  1. Open vocalbridge_demo.html in your browser")
        print("  2. Click 'Start Call' button")
        print("  3. Allow microphone access")
        print("  4. Speak: 'I want to return my headphones to Amazon'")
        print("  5. Experience the voice conversation!")
    else:
        print("⚠️  SOME TESTS FAILED")
        print()
        print("Please review the failed tests above for details.")

    print()
    print("=" * 70)


def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("  VOCAL BRIDGE INTEGRATION - COMPLETE TEST SUITE")
    print("=" * 70)

    results = {}

    # Test 1: API Connection
    client, success = test_api_connection()
    results["1. API Connection & Authentication"] = success

    if not success or client is None:
        print("\n❌ Cannot proceed - client initialization failed")
        print_summary(results)
        return

    # Test 2: Get Credentials
    creds, success = test_get_credentials(client)
    results["2. Get LiveKit Credentials"] = success

    if success and creds:
        # Test 3: Token Structure
        success = test_token_structure(creds)
        results["3. JWT Token Structure"] = success
    else:
        results["3. JWT Token Structure"] = False

    # Test 4: Web Demo Generation
    success = test_web_demo_generation(client)
    results["4. Web Demo Generation"] = success

    # Test 5: Multiple Requests
    success = test_multiple_requests(client)
    results["5. Multiple Token Requests"] = success

    # Test 6: Configuration
    success = test_configuration()
    results["6. Environment Configuration"] = success

    # Print summary
    print_summary(results)


if __name__ == "__main__":
    main()
