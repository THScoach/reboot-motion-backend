#!/usr/bin/env python3
"""
Test the Reboot Motion Data Export endpoint
"""

import requests
import json
import sys

# Test endpoint
BASE_URL = "https://reboot-motion-backend-production.up.railway.app"
SESSION_ID = "6764e74b-516d-45eb-a8a9-c50a069ef50d"

def test_data_export():
    """Test the POST /reboot/data-export endpoint"""
    
    print("🧪 Testing Reboot Motion Data Export Endpoint")
    print(f"   Base URL: {BASE_URL}")
    print(f"   Session ID: {SESSION_ID}")
    print()
    
    # Build request
    url = f"{BASE_URL}/reboot/data-export"
    params = {
        "session_id": SESSION_ID,
        "movement_type_id": 1,  # baseball-hitting
        "data_type": "momentum-energy",
        "data_format": "csv"
    }
    
    print(f"📡 POST {url}")
    print(f"   Params: {json.dumps(params, indent=2)}")
    print()
    
    try:
        response = requests.post(url, params=params, timeout=60)
        
        print(f"📊 Response:")
        print(f"   Status Code: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print()
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS!")
            print(json.dumps(data, indent=2)[:1000])  # First 1000 chars
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

if __name__ == "__main__":
    result = test_data_export()
    sys.exit(0 if result else 1)
