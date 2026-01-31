#!/usr/bin/env python3
"""
Run a simple web server to test Vocal Bridge integration.

This avoids CORS issues that occur when opening HTML files directly.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

sys.path.insert(0, '/Users/sankar/projects/voice_agent')

PORT = 8000

def main():
    print("\n" + "="*70)
    print("  VOCAL BRIDGE TEST SERVER")
    print("="*70 + "\n")

    # Change to project directory
    os.chdir('/Users/sankar/projects/voice_agent')

    # Create server
    Handler = http.server.SimpleHTTPRequestHandler
    Handler.extensions_map['.html'] = 'text/html'

    print(f"Starting server on http://localhost:{PORT}")
    print()

    try:
        with socketserver.TCPServer(("", PORT), Handler) as httpd:
            print("✅ Server is running!")
            print()
            print(f"Opening browser to test page...")
            print()

            # Open browser
            url = f"http://localhost:{PORT}/test_vocal_bridge_live.html"
            webbrowser.open(url)

            print("="*70)
            print("  TESTING INSTRUCTIONS")
            print("="*70)
            print()
            print("In the browser that just opened:")
            print()
            print("1️⃣  Click 'Step 1: Get Credentials'")
            print("   → Should see: ✅ Credentials Retrieved")
            print()
            print("2️⃣  Click 'Step 2: Start Voice Call'")
            print("   → Allow microphone when prompted")
            print("   → Should see: ✅ Connected to room!")
            print()
            print("3️⃣  Start Speaking!")
            print("   → Say: 'I want to return my headphones to Amazon'")
            print("   → Agent should respond with voice")
            print()
            print("="*70)
            print()
            print("Server is running. Press Ctrl+C to stop.")
            print()

            # Serve forever
            httpd.serve_forever()

    except KeyboardInterrupt:
        print("\n\n✅ Server stopped.")
        print("Test complete!")

if __name__ == "__main__":
    main()
