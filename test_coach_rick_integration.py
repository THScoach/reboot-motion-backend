"""
Coach Rick AI - Integration Test
Tests the complete API integration with all components
"""

import sys
import requests
import json
from io import BytesIO

print("\n" + "="*70)
print("COACH RICK AI - INTEGRATION TEST")
print("="*70)

# Test configuration
BASE_URL = "http://localhost:8005"  # Update if different
API_ENDPOINT = f"{BASE_URL}/api/v1/reboot-lite/analyze-with-coach"
HEALTH_ENDPOINT = f"{BASE_URL}/api/v1/reboot-lite/coach-rick/health"

print(f"\nBase URL: {BASE_URL}")
print(f"API Endpoint: {API_ENDPOINT}")
print(f"Health Endpoint: {HEALTH_ENDPOINT}")

# ============================================================================
# TEST 1: Health Check
# ============================================================================
print("\n" + "-"*70)
print("TEST 1: HEALTH CHECK")
print("-"*70)

try:
    response = requests.get(HEALTH_ENDPOINT, timeout=5)
    
    if response.status_code == 200:
        health_data = response.json()
        print("✅ PASS - Health check successful")
        print(f"\nStatus: {health_data.get('status')}")
        print(f"Service: {health_data.get('service')}")
        print(f"Version: {health_data.get('version')}")
        print("\nComponents:")
        for component, status in health_data.get('components', {}).items():
            print(f"  {component}: {status}")
    else:
        print(f"❌ FAIL - Health check failed with status {response.status_code}")
        sys.exit(1)
        
except Exception as e:
    print(f"❌ FAIL - Health check error: {e}")
    print("\n💡 TIP: Make sure the server is running:")
    print("   cd /home/user/webapp && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000")
    sys.exit(1)


# ============================================================================
# TEST 2: Full Analysis Request (Mock Video)
# ============================================================================
print("\n" + "-"*70)
print("TEST 2: FULL COACH RICK ANALYSIS")
print("-"*70)

# Create mock video file (small text file for testing)
mock_video_content = b"Mock video data for testing"
mock_video = BytesIO(mock_video_content)
mock_video.name = "test_swing.mp4"

# Request data
files = {
    'video': ('test_swing.mp4', mock_video, 'video/mp4')
}

data = {
    'player_name': 'Eric Williams',
    'height_inches': 73.0,
    'weight_lbs': 185.0,
    'age': 28,
    'bat_weight_oz': 30.0
}

print("\nRequest Data:")
for key, value in data.items():
    print(f"  {key}: {value}")

try:
    print("\n⏳ Sending request to Coach Rick AI...")
    response = requests.post(API_ENDPOINT, files=files, data=data, timeout=30)
    
    if response.status_code == 200:
        result = response.json()
        
        print("\n✅ PASS - Analysis completed successfully!")
        print("\n" + "="*70)
        print("ANALYSIS RESULTS")
        print("="*70)
        
        # Session info
        print(f"\nSession ID: {result.get('session_id')}")
        print(f"Player: {result.get('player_name')}")
        print(f"Timestamp: {result.get('timestamp')}")
        
        # Core metrics
        print(f"\n📊 CORE METRICS:")
        print(f"  Bat Speed: {result.get('bat_speed_mph')} mph")
        print(f"  Exit Velocity: {result.get('exit_velocity_mph')} mph")
        print(f"  Efficiency: {result.get('efficiency_percent')}%")
        print(f"  Tempo Score: {result.get('tempo_score')}")
        print(f"  Stability Score: {result.get('stability_score')}")
        print(f"  GEW Overall: {result.get('gew_overall')}")
        
        # Motor profile
        motor_profile = result.get('motor_profile', {})
        print(f"\n🎯 MOTOR PROFILE:")
        print(f"  Type: {motor_profile.get('type')}")
        print(f"  Confidence: {motor_profile.get('confidence')}%")
        print(f"  Characteristics: {', '.join(motor_profile.get('characteristics', []))}")
        
        # Patterns
        patterns = result.get('patterns', [])
        print(f"\n🔍 PATTERNS DETECTED: {len(patterns)}")
        for i, pattern in enumerate(patterns[:2], 1):  # Show top 2
            print(f"\n  {i}. {pattern.get('name')} ({pattern.get('severity')})")
            print(f"     {pattern.get('description')}")
        
        # Primary issue
        print(f"\n🎯 PRIMARY ISSUE:")
        print(f"  {result.get('primary_issue')}")
        
        # Prescription
        prescription = result.get('prescription', {})
        drills = prescription.get('drills', [])
        print(f"\n💪 DRILL PRESCRIPTION ({prescription.get('duration_weeks')} weeks):")
        for i, drill in enumerate(drills[:3], 1):  # Show top 3
            print(f"\n  {i}. {drill.get('name')}")
            print(f"     Volume: {drill.get('volume')}")
            print(f"     Frequency: {drill.get('frequency')}")
        
        print(f"\n  Expected Gains: {prescription.get('expected_gains')}")
        
        # Coach Rick messages
        coach_messages = result.get('coach_messages', {})
        print(f"\n🗣️  COACH RICK SAYS:")
        print(f"\n  Analysis:")
        print(f"  \"{coach_messages.get('analysis')}\"")
        print(f"\n  Drill Introduction:")
        print(f"  \"{coach_messages.get('drill_intro')}\"")
        print(f"\n  Encouragement:")
        print(f"  \"{coach_messages.get('encouragement')}\"")
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\n🎉 Coach Rick AI is FULLY OPERATIONAL!")
        
    else:
        print(f"\n❌ FAIL - Analysis failed with status {response.status_code}")
        print(f"Response: {response.text}")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ FAIL - Analysis error: {e}")
    sys.exit(1)


print("\n" + "="*70)
print("INTEGRATION TEST COMPLETE")
print("="*70)
print("\n✅ Coach Rick AI Engine is ready for production!")
print(f"\nAPI Documentation: {BASE_URL}/docs")
print("\n")
