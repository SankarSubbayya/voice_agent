#!/usr/bin/env python3
"""
Quick verification that everything is set up correctly
"""

import sys
sys.path.insert(0, '/Users/sankar/projects/voice_agent')

def verify():
    print("\n" + "="*70)
    print("  VOCAL BRIDGE SETUP VERIFICATION")
    print("="*70 + "\n")

    checks = []

    # Check 1: Config module
    print("✓ Checking configuration...")
    try:
        from config import config
        checks.append(("Config module", True, None))
    except Exception as e:
        checks.append(("Config module", False, str(e)))

    # Check 2: API key
    print("✓ Checking API key...")
    try:
        from config import config
        has_key = config.has_vocalbridge()
        key = config.vocalbridge_api_key
        if has_key and key.startswith('vb_') and len(key) > 40:
            checks.append(("API Key", True, f"{key[:20]}..."))
        else:
            checks.append(("API Key", False, f"Invalid format: {key[:20]}..."))
    except Exception as e:
        checks.append(("API Key", False, str(e)))

    # Check 3: Endpoint
    print("✓ Checking endpoint...")
    try:
        endpoint = config.vocalbridge_endpoint
        if 'vocalbridgeai.com' in endpoint:
            checks.append(("Endpoint", True, endpoint))
        else:
            checks.append(("Endpoint", False, f"Wrong endpoint: {endpoint}"))
    except Exception as e:
        checks.append(("Endpoint", False, str(e)))

    # Check 4: Client module
    print("✓ Checking client module...")
    try:
        from services.vocalbridge_livekit_client import VocalBridgeClient
        checks.append(("Client Module", True, "vocalbridge_livekit_client.py"))
    except Exception as e:
        checks.append(("Client Module", False, str(e)))

    # Check 5: API connection
    print("✓ Testing API connection...")
    try:
        from services.vocalbridge_livekit_client import VocalBridgeClient
        client = VocalBridgeClient()
        creds = client.get_livekit_credentials()
        checks.append(("API Connection", True, f"Room: {creds['room_name'][:30]}..."))
    except Exception as e:
        checks.append(("API Connection", False, str(e)[:60]))

    # Check 6: HTML demo file
    print("✓ Checking demo files...")
    try:
        import os
        html_file = 'test_vocal_bridge_live.html'
        if os.path.exists(html_file):
            size = os.path.getsize(html_file)
            checks.append(("HTML Demo", True, f"{html_file} ({size} bytes)"))
        else:
            checks.append(("HTML Demo", False, "File not found"))
    except Exception as e:
        checks.append(("HTML Demo", False, str(e)))

    # Print results
    print("\n" + "="*70)
    print("  RESULTS")
    print("="*70 + "\n")

    passed = 0
    failed = 0

    for name, success, detail in checks:
        if success:
            passed += 1
            print(f"✅ {name:<20} PASS")
            if detail:
                print(f"   {detail}")
        else:
            failed += 1
            print(f"❌ {name:<20} FAIL")
            if detail:
                print(f"   {detail}")
        print()

    # Summary
    print("="*70)
    print(f"\nTotal: {passed} passed, {failed} failed\n")

    if failed == 0:
        print("🎉 ALL CHECKS PASSED!")
        print()
        print("Your Vocal Bridge integration is ready to test.")
        print()
        print("To test the voice agent:")
        print("  1. Run: python3 test_voice_agent.py")
        print("  2. Or open: test_vocal_bridge_live.html in your browser")
        print()
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before testing.")
        print()

    return failed == 0

if __name__ == "__main__":
    success = verify()
    sys.exit(0 if success else 1)
