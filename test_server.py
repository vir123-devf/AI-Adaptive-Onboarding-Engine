#!/usr/bin/env python3
"""Test the API endpoint."""
import time
import requests
import json

time.sleep(2)  # Wait for server to start

try:
    response = requests.get("http://localhost:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print("\n✓ Server is running and responding!")
except requests.exceptions.ConnectionError:
    print("✗ Failed to connect to server. Is it running?")
except Exception as e:
    print(f"✗ Error: {e}")
