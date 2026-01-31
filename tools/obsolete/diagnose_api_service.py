#!/usr/bin/env python3
"""
API Service Diagnostic Tool

This script attempts to identify which voice API service your API key belongs to
by testing common endpoints and authentication methods.
"""

import requests
from config import config

def test_service(name: str, base_url: str, auth_formats: list, endpoints: list):
    """Test a service with various auth formats and endpoints."""
    print(f"\n{'='*70}")
    print(f"Testing: {name}")
    print(f"Base URL: {base_url}")
    print('='*70)

    api_key = config.vocalbridge_api_key

    for auth_format in auth_formats:
        print(f"\nAuth format: {auth_format}")
        print('-'*70)

        # Build headers based on format
        if auth_format == "Bearer":
            headers = {"Authorization": f"Bearer {api_key}"}
        elif auth_format == "API-Key":
            headers = {"API-Key": api_key}
        elif auth_format == "X-API-Key":
            headers = {"X-API-Key": api_key}
        elif auth_format == "authorization":
            headers = {"authorization": api_key}
        elif auth_format == "X-Vapi-Secret":
            headers = {"X-Vapi-Secret": api_key}
        else:
            headers = {"Authorization": api_key}

        for endpoint in endpoints:
            url = f"{base_url}{endpoint}"
            try:
                response = requests.get(url, headers=headers, timeout=5)

                if response.status_code == 200:
                    print(f"✅ SUCCESS: {endpoint}")
                    print(f"   Status: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
                    return True  # Found it!

                elif response.status_code != 404:  # Not just "not found"
                    print(f"⚠️  RESPONSE: {endpoint}")
                    print(f"   Status: {response.status_code}")
                    print(f"   Message: {response.text[:200]}")

            except requests.exceptions.ConnectionError:
                print(f"❌ Cannot connect: {endpoint}")
            except requests.exceptions.Timeout:
                print(f"⏱️  Timeout: {endpoint}")
            except Exception as e:
                print(f"❌ Error: {endpoint} - {type(e).__name__}")

    return False

def main():
    print("="*70)
    print("API SERVICE DIAGNOSTIC TOOL")
    print("="*70)
    print()
    print(f"API Key: {config.vocalbridge_api_key[:20]}...")
    print(f"Key Prefix: {config.vocalbridge_api_key[:3]}")
    print(f"Key Length: {len(config.vocalbridge_api_key)}")
    print()

    # Test various voice API services
    services = [
        {
            "name": "VAPI",
            "base_url": "https://api.vapi.ai",
            "auth_formats": ["Bearer", "X-Vapi-Secret"],
            "endpoints": ["/assistant", "/call", "/me", "/account"]
        },
        {
            "name": "Bland AI",
            "base_url": "https://api.bland.ai",
            "auth_formats": ["authorization", "Bearer"],
            "endpoints": ["/v1/calls", "/v1/agents", "/v1/account"]
        },
        {
            "name": "Retell AI",
            "base_url": "https://api.retellai.com",
            "auth_formats": ["Bearer", "X-API-Key"],
            "endpoints": ["/v1/get-agent", "/v1/list-calls", "/health"]
        },
        {
            "name": "Play.ht",
            "base_url": "https://api.play.ht",
            "auth_formats": ["X-API-Key", "Bearer"],
            "endpoints": ["/api/v2/voices", "/api/v1/convert", "/health"]
        },
        {
            "name": "ElevenLabs",
            "base_url": "https://api.elevenlabs.io",
            "auth_formats": ["xi-api-key", "Bearer"],
            "endpoints": ["/v1/voices", "/v1/user", "/v1/models"]
        },
        {
            "name": "Deepgram",
            "base_url": "https://api.deepgram.com",
            "auth_formats": ["Bearer", "API-Key"],
            "endpoints": ["/v1/projects", "/v1/keys", "/v1/models"]
        },
        {
            "name": "AssemblyAI",
            "base_url": "https://api.assemblyai.com",
            "auth_formats": ["authorization", "Bearer"],
            "endpoints": ["/v2/transcript", "/v2/realtime/token"]
        },
    ]

    found = False
    for service in services:
        if test_service(**service):
            print(f"\n{'='*70}")
            print(f"🎯 FOUND: Your API key belongs to {service['name']}!")
            print(f"{'='*70}")
            found = True
            break

    if not found:
        print(f"\n{'='*70}")
        print("❓ UNABLE TO IDENTIFY SERVICE")
        print(f"{'='*70}")
        print()
        print("Your API key with prefix 'vb_' doesn't match any known services.")
        print()
        print("Possible reasons:")
        print("1. Custom/internal voice platform")
        print("2. White-label solution")
        print("3. Beta/private service")
        print("4. Service not in our test list")
        print()
        print("NEXT STEPS:")
        print("Please provide:")
        print("  • Dashboard URL where you created the agent")
        print("  • API documentation link")
        print("  • Or screenshot of the dashboard (header/branding)")

if __name__ == "__main__":
    main()
