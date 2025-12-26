#!/usr/bin/env python3
"""
Quick script to check available movement types from Reboot Motion API
"""
import os
import requests

# Get credentials from environment
username = os.environ.get('REBOOT_USERNAME')
password = os.environ.get('REBOOT_PASSWORD')

if not username or not password:
    print("❌ REBOOT_USERNAME and REBOOT_PASSWORD must be set")
    exit(1)

# Get OAuth token
token_url = "https://api.rebootmotion.com/oauth/token"
token_data = {
    "username": username,
    "password": password,
    "grant_type": "password"
}

print("🔐 Getting OAuth token...")
token_response = requests.post(token_url, json=token_data)
token_response.raise_for_status()
token = token_response.json()['access_token']
print("✅ Got access token")

# Get movement types
headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
}

print("\n📋 Fetching movement types...")
movement_types_response = requests.get(
    "https://api.rebootmotion.com/movement_types",
    headers=headers
)
movement_types_response.raise_for_status()

import json
movement_types = movement_types_response.json()
print(f"\n✅ Found {len(movement_types)} movement types:")
print(json.dumps(movement_types, indent=2))
