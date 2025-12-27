"""
Test the /api/reboot/generate-krs-report endpoint
"""
import os
import requests
import json

os.environ.setdefault('DATABASE_URL', 'sqlite:///catching_barrels.db')
os.environ['REBOOT_USERNAME'] = 'coachrickpd@gmail.com'
os.environ['REBOOT_PASSWORD'] = 'Train@2025'

# Connor Gray's session
session_id = '4f1a7010-1324-469d-8e1a-e05a1dc45f2e'

print(f"\n🧪 Testing KRS Generation Endpoint")
print("="*60)
print(f"Session ID: {session_id}")
print("="*60)

# Import and test directly (simulating API call)
from session_api import generate_krs_from_reboot

try:
    print("\n📞 Calling generate_krs_from_reboot()...")
    
    # This is the function that the API endpoint calls
    import asyncio
    result = asyncio.run(generate_krs_from_reboot(session_id))
    
    print("\n✅ API Response:")
    print(json.dumps(result, indent=2, default=str))
    
    print("\n" + "="*60)
    print("✅ ENDPOINT TEST SUCCESSFUL")
    print("="*60)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

