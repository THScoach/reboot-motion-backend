#!/usr/bin/env python3
"""
Quick Script to Insert Connor Gray's Report Metrics
Run this to populate the database with Connor's actual rotation data
"""

import requests
import json

# Connor Gray's session
SESSION_ID = "4f1a7010-1324-469d-8e1a-e05a1dc45f2e"
API_BASE = "http://localhost:5000"  # Change to your actual API URL

# Connor's metrics extracted from Reboot report
connor_metrics = {
    "pelvis_rotation_rom_deg": 60.0,  # From "Torso Kinematics" chart (purple line ~10° to ~70°)
    "torso_rotation_rom_deg": 25.0,   # From "Torso Kinematics" chart (orange line ~15° to ~40°)
    
    # Optional kinematic sequence (estimate from chart)
    "pelvis_peak_velocity_deg_per_s": 425,  # Visible in kinematic sequence chart
    "torso_peak_velocity_deg_per_s": 738,   # Visible in kinematic sequence chart
    
    # HitTrax validation
    "bat_speed_mph": 59.4,           # Calculated from exit velocity
    "exit_velocity_mph": 98.0,       # HitTrax measured
    "hittrax_bat_speed_mph": 59.4,
    "hittrax_exit_velocity_mph": 98.0,
    "validated_against_hittrax": True,
    
    # Metadata
    "data_source": "manual_input",
    "created_by": "Coach Rick",
    "notes": """
Extracted from Reboot Motion report dated 12/20/2025.
    
Torso Kinematics Chart Analysis:
- Purple line (Pelvis): Start ~10°, Peak ~70° → ROM = 60°
- Orange line (Torso): Start ~15°, Peak ~40° → ROM = 25°

HitTrax Validation:
- Exit Velocity: 98 mph (vs 50-55 mph pitch)
- Calculated Bat Speed: 59.4 mph
- Physics Check: 59.4 mph requires 35-40° pelvis minimum ✅
- Actual Pelvis: 60° ✅ MATCHES PHYSICS

This is 20x different from CSV pelvis_rot column (3°).
The report data is correct, CSV column is wrong.
"""
}

def insert_connor_metrics():
    """Insert Connor's metrics via API"""
    url = f"{API_BASE}/api/reboot/sessions/{SESSION_ID}/report-metrics"
    
    print("=" * 70)
    print("INSERTING CONNOR GRAY'S REPORT METRICS")
    print("=" * 70)
    print()
    print(f"Session ID: {SESSION_ID}")
    print(f"Player: Connor Gray")
    print()
    print("Metrics:")
    print(f"  Pelvis Rotation ROM: {connor_metrics['pelvis_rotation_rom_deg']}°")
    print(f"  Torso Rotation ROM: {connor_metrics['torso_rotation_rom_deg']}°")
    print(f"  Bat Speed: {connor_metrics['bat_speed_mph']} mph")
    print(f"  Exit Velocity: {connor_metrics['exit_velocity_mph']} mph")
    print()
    
    try:
        response = requests.post(url, json=connor_metrics)
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            print()
            print("Connor's metrics have been saved.")
            print("You can now generate KRS report with accurate rotation data.")
            print()
            print("Next steps:")
            print("1. Run KRS calculation with new metrics")
            print("2. Generate corrected report")
            print("3. Update motor profile (likely SPINNER, not WHIPPER)")
            print()
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to API")
        print(f"Make sure Flask app is running at {API_BASE}")
        print()
        print("Alternative: Insert directly into database")
        print()
        print_sql_insert()

def print_sql_insert():
    """Print SQL INSERT statement as fallback"""
    print("=" * 70)
    print("SQL INSERT (if API not available)")
    print("=" * 70)
    print()
    
    sql = f"""
INSERT INTO reboot_report_metrics (
    session_id,
    org_player_id,
    report_file_path,
    data_source,
    pelvis_rotation_rom_deg,
    torso_rotation_rom_deg,
    pelvis_peak_velocity_deg_per_s,
    torso_peak_velocity_deg_per_s,
    bat_speed_mph,
    exit_velocity_mph,
    validated_against_hittrax,
    hittrax_bat_speed_mph,
    hittrax_exit_velocity_mph,
    created_by,
    notes
) VALUES (
    '{SESSION_ID}',
    '80e77691-d7cc-4ebb-b955-2fd45676f0ca',
    '/home/user/webapp/connor_reboot_report.png',
    'manual_input',
    {connor_metrics['pelvis_rotation_rom_deg']},
    {connor_metrics['torso_rotation_rom_deg']},
    {connor_metrics.get('pelvis_peak_velocity_deg_per_s', 'NULL')},
    {connor_metrics.get('torso_peak_velocity_deg_per_s', 'NULL')},
    {connor_metrics['bat_speed_mph']},
    {connor_metrics['exit_velocity_mph']},
    TRUE,
    {connor_metrics['hittrax_bat_speed_mph']},
    {connor_metrics['hittrax_exit_velocity_mph']},
    '{connor_metrics['created_by']}',
    '{connor_metrics['notes'].replace("'", "''")}'
)
ON CONFLICT (session_id) DO UPDATE SET
    pelvis_rotation_rom_deg = EXCLUDED.pelvis_rotation_rom_deg,
    torso_rotation_rom_deg = EXCLUDED.torso_rotation_rom_deg,
    updated_at = CURRENT_TIMESTAMP;
"""
    
    print(sql)
    print()
    print("Copy the above SQL and run in your database.")

if __name__ == "__main__":
    insert_connor_metrics()
