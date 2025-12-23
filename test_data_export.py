"""
Test script to fetch biomechanics data from Reboot Motion Data Export API
"""
import requests
import json
import os
from sync_service import RebootMotionSync

def get_data_export(session_id: str, movement_type: str = "baseball-hitting"):
    """
    Fetch biomechanics data from Reboot Motion Data Export API
    
    Args:
        session_id: Reboot Motion session UUID
        movement_type: Type of movement (default: "baseball-hitting")
    
    Returns:
        Biomechanics data dictionary
    """
    # Initialize sync service to get OAuth token
    sync = RebootMotionSync()
    token = sync._get_access_token()
    
    # Data Export endpoint
    base_url = "https://api.rebootmotion.com"
    endpoint = f"{base_url}/data_export"
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    params = {
        'session_id': session_id,
        'movement_type': movement_type
    }
    
    print(f"\n🔍 Fetching biomechanics data...")
    print(f"Session ID: {session_id}")
    print(f"Movement Type: {movement_type}")
    
    response = requests.get(endpoint, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Data retrieved successfully!")
        print(f"Data keys: {list(data.keys())}")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        return None


if __name__ == "__main__":
    # Test with Ronald Acuna session
    session_id = "6764e74b-516d-45eb-a8a9-c50a069ef50d"
    
    print("="*60)
    print("REBOOT MOTION DATA EXPORT TEST")
    print("="*60)
    
    data = get_data_export(session_id)
    
    if data:
        print("\n" + "="*60)
        print("DATA STRUCTURE")
        print("="*60)
        print(json.dumps(data, indent=2)[:2000])  # First 2000 chars
        
        # Check for key biomechanics fields
        print("\n" + "="*60)
        print("KEY FIELDS CHECK")
        print("="*60)
        
        fields_to_check = [
            'angular_velocity',
            'linear_velocity',
            'joint_angles',
            'kinematic_sequence',
            'peak_velocities',
            'timing_events',
            'bat_speed',
            'pelvis',
            'torso',
            'momentum',
            'first_move',
            'foot_plant',
            'contact'
        ]
        
        for field in fields_to_check:
            found = field in str(data).lower()
            status = "✅" if found else "❌"
            print(f"{status} {field}: {'Found' if found else 'Not found'}")
