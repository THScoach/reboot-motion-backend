"""
Test script to fetch biomechanics data from Reboot Motion Data Export API
Standalone version without database dependency
"""
import requests
import json
import os

def get_oauth_token():
    """Get OAuth token from Reboot Motion"""
    client_id = os.getenv('REBOOT_CLIENT_ID')
    client_secret = os.getenv('REBOOT_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        print("❌ Missing OAuth credentials")
        print("Set REBOOT_CLIENT_ID and REBOOT_CLIENT_SECRET environment variables")
        return None
    
    token_url = 'https://api.rebootmotion.com/oauth/token'
    
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        print(f"❌ OAuth failed: {response.status_code}")
        print(response.text)
        return None


def get_data_export(session_id: str, token: str, movement_type: str = "baseball-hitting"):
    """
    Fetch biomechanics data from Reboot Motion Data Export API
    
    Args:
        session_id: Reboot Motion session UUID
        token: OAuth access token
        movement_type: Type of movement (default: "baseball-hitting")
    
    Returns:
        Biomechanics data dictionary
    """
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
    print(f"Endpoint: {endpoint}")
    
    response = requests.get(endpoint, headers=headers, params=params)
    
    print(f"\nStatus Code: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Data retrieved successfully!")
        return data
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return None


if __name__ == "__main__":
    print("="*60)
    print("REBOOT MOTION DATA EXPORT TEST")
    print("="*60)
    
    # Get OAuth token
    print("\n1. Getting OAuth token...")
    token = get_oauth_token()
    
    if not token:
        print("\n❌ Cannot proceed without OAuth token")
        exit(1)
    
    print("✅ OAuth token obtained")
    
    # Test with Ronald Acuna session
    session_id = "6764e74b-516d-45eb-a8a9-c50a069ef50d"
    
    print("\n2. Fetching Data Export...")
    data = get_data_export(session_id, token)
    
    if data:
        print("\n" + "="*60)
        print("DATA STRUCTURE")
        print("="*60)
        
        # Show top-level keys
        if isinstance(data, dict):
            print(f"\nTop-level keys: {list(data.keys())}")
            
            # Show first 3000 chars
            print("\nData preview:")
            print(json.dumps(data, indent=2)[:3000])
        else:
            print(f"Data type: {type(data)}")
            print(str(data)[:2000])
        
        # Check for key biomechanics fields
        print("\n" + "="*60)
        print("KEY FIELDS CHECK")
        print("="*60)
        
        data_str = str(data).lower()
        
        fields_to_check = [
            ('angular_velocity', 'Angular velocities'),
            ('linear_velocity', 'Linear velocities'),
            ('joint_angles', 'Joint angles'),
            ('kinematic_sequence', 'Kinematic sequence'),
            ('peak_velocities', 'Peak velocities'),
            ('timing_events', 'Timing events'),
            ('bat_speed', 'Bat speed'),
            ('pelvis', 'Pelvis data'),
            ('torso', 'Torso data'),
            ('momentum', 'Momentum'),
            ('first_move', 'First movement'),
            ('foot_plant', 'Foot plant'),
            ('contact', 'Contact timing')
        ]
        
        for field, description in fields_to_check:
            found = field in data_str
            status = "✅" if found else "❌"
            print(f"{status} {description:30s} ({field})")
        
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        
        if isinstance(data, dict):
            print(f"Total keys: {len(data.keys())}")
            print(f"Data size: ~{len(str(data))} chars")
