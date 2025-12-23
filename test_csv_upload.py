#!/usr/bin/env python3
"""
Test Reboot Motion CSV Import Feature
Demonstrates how to use the CSV upload endpoint
"""

import requests
import json
from pathlib import Path


def test_csv_upload_info():
    """Test the info endpoint"""
    print("\n" + "="*80)
    print("TEST 1: Get CSV Upload Info")
    print("="*80)
    
    url = "http://localhost:8000/csv-upload-info"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Info endpoint working")
        print(f"\nFeature: {data['feature']}")
        print(f"Description: {data['description']}")
        print(f"\nSupported Files:")
        for file_type in data['supported_files']:
            print(f"  - {file_type}")
    else:
        print(f"❌ Failed: {response.status_code}")
        print(response.text)


def test_csv_upload(csv_path: str):
    """Test CSV upload and processing"""
    print("\n" + "="*80)
    print("TEST 2: Upload and Process CSV")
    print("="*80)
    
    if not Path(csv_path).exists():
        print(f"❌ File not found: {csv_path}")
        print("\nTo test this feature:")
        print("1. Export a momentum-energy CSV from Reboot Motion")
        print("2. Save it to the current directory")
        print("3. Run this script with the CSV filename")
        return
    
    url = "http://localhost:8000/upload-reboot-csv"
    
    files = {
        'file': (Path(csv_path).name, open(csv_path, 'rb'), 'text/csv')
    }
    
    data = {
        'bat_mass_kg': 0.85,
        'athlete_name': 'Connor Gray'
    }
    
    print(f"Uploading: {csv_path}")
    print(f"Bat mass: {data['bat_mass_kg']} kg")
    print(f"Athlete: {data['athlete_name']}")
    
    response = requests.post(url, files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print("\n✅ CSV processed successfully!")
        
        # Display session info
        print("\n📋 SESSION INFO:")
        session = result['session_info']
        print(f"  Session ID: {session['session_id']}")
        print(f"  Athlete: {session['athlete_name']}")
        print(f"  Movement: {session['movement_type']}")
        print(f"  FPS: {session['fps']}")
        print(f"  Duration: {session['duration_s']}s")
        print(f"  Frames: {session['num_frames']}")
        print(f"  Contact Frame: {session['contact_frame']} ({session['contact_time_s']}s)")
        
        # Display ground truth metrics
        print("\n📊 GROUND TRUTH METRICS:")
        metrics = result['ground_truth_metrics']
        
        print(f"\n  Bat Speed:")
        print(f"    At Contact: {metrics['bat_speed']['at_contact_mph']} mph")
        print(f"    Peak: {metrics['bat_speed']['peak_mph']} mph")
        
        print(f"\n  Energy Distribution (at contact):")
        energy = metrics['energy_distribution']
        print(f"    Total: {energy['total_j']} J")
        if energy['lowerhalf_pct']:
            print(f"    Lower Half: {energy['lowerhalf_pct']}%")
        if energy['torso_pct']:
            print(f"    Torso: {energy['torso_pct']}%")
        if energy['arms_pct']:
            print(f"    Arms: {energy['arms_pct']}%")
        
        print(f"\n  Kinematic Sequence (ms before contact):")
        kin_seq = metrics['kinematic_sequence_ms_before_contact']
        for segment, time_ms in kin_seq.items():
            print(f"    {segment.capitalize()}: {time_ms} ms")
        
        print(f"\n  Tempo (estimated):")
        tempo = metrics['tempo_estimated']
        print(f"    Ratio: {tempo['ratio']}:1")
        print(f"    Load Duration: {tempo['load_duration_ms']} ms")
        print(f"    Swing Duration: {tempo['swing_duration_ms']} ms")
        
        # Save full response for inspection
        output_file = "csv_upload_result.json"
        with open(output_file, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"\n💾 Full response saved to: {output_file}")
        
    else:
        print(f"\n❌ Upload failed: {response.status_code}")
        print(f"Error: {response.text}")


def test_csv_upload_error_handling():
    """Test error handling with invalid files"""
    print("\n" + "="*80)
    print("TEST 3: Error Handling")
    print("="*80)
    
    url = "http://localhost:8000/upload-reboot-csv"
    
    # Test 1: Non-CSV file
    print("\n📝 Test 3a: Non-CSV file extension")
    try:
        files = {'file': ('test.txt', b'fake data', 'text/plain')}
        response = requests.post(url, files=files)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: CSV without rebootmotion in name
    print("\n📝 Test 3b: Non-Reboot Motion CSV")
    try:
        files = {'file': ('random_data.csv', b'col1,col2\n1,2', 'text/csv')}
        response = requests.post(url, files=files)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Run all tests"""
    print("\n🧪 Testing Reboot Motion CSV Import Feature")
    print("="*80)
    
    # Test 1: Get info
    try:
        test_csv_upload_info()
    except Exception as e:
        print(f"❌ Info test failed: {e}")
    
    # Test 2: Upload CSV (if available)
    csv_files = list(Path('.').glob('*momentum*.csv'))
    if csv_files:
        try:
            test_csv_upload(str(csv_files[0]))
        except Exception as e:
            print(f"❌ Upload test failed: {e}")
    else:
        print("\n" + "="*80)
        print("TEST 2: Upload and Process CSV")
        print("="*80)
        print("ℹ️  No momentum-energy CSV files found in current directory")
        print("\nTo test CSV upload:")
        print("1. Export a momentum-energy CSV from Reboot Motion")
        print("2. Place it in this directory")
        print("3. Run this script again")
    
    # Test 3: Error handling
    try:
        test_csv_upload_error_handling()
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print("\n" + "="*80)
    print("✅ Testing complete!")
    print("="*80)
    print("\nNote: Make sure the backend server is running on http://localhost:8000")


if __name__ == "__main__":
    main()
