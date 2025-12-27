#!/usr/bin/env python3
"""
Kyle Tucker - KRS Report from Single-Camera Video Analysis
MLB-Level Performance Analysis
"""

import sys
sys.path.insert(0, '/home/user/webapp')

from datetime import datetime
import json

# Load Kyle Tucker's data
with open('/home/user/webapp/kyle_tucker_krs_input.json', 'r') as f:
    tucker_data = json.load(f)

# Kyle Tucker's metrics
kyle_tucker = {
    # Player Info
    'player_name': 'Kyle Tucker',
    'session_id': 'kyle_tucker_mlb_video_001',
    'session_date': '2025-12-27',
    'age': 28,
    'height_inches': 76,  # 6'4"
    'weight_lbs': 212,
    'wingspan_inches': 78,  # Estimated
    'bat_weight_oz': 32,  # MLB standard
    'team': 'Chicago Cubs (Free Agent)',
    
    # Rotation (FROM VIDEO ANALYSIS - Conservative estimates)
    'pelvis_rotation_deg': tucker_data['rotation_metrics']['pelvis_rotation_rom_deg'],
    'torso_rotation_deg': tucker_data['rotation_metrics']['torso_rotation_rom_deg'],
    'x_factor_deg': tucker_data['rotation_metrics']['x_factor_deg'],
    
    # Kinematic Sequence (FROM VIDEO ANALYSIS)
    'pelvis_peak_velocity': tucker_data['kinematic_sequence']['pelvis_peak_velocity_deg_per_s'],
    'torso_peak_velocity': tucker_data['kinematic_sequence']['torso_peak_velocity_deg_per_s'],
    'sequence_gap_ms': tucker_data['kinematic_sequence']['sequence_gap_ms'],
    
    # Performance (FROM VIDEO CONTEXT - MLB standards)
    'estimated_bat_speed_mph': 75.0,  # MLB avg for power hitters
    'estimated_exit_velocity_mph': 95.0,  # Conservative estimate
    'pitch_speed_est_mph': 85.0,  # MLB fastball average
    
    # Exospeed Capacity (calculated from anthropometry)
    'exospeed_capacity_mph': 78.5,  # 6'4", 212 lbs, age 28, +2" ape
}

def calculate_exospeed_capacity(height, weight, wingspan, age, bat_weight):
    """Calculate theoretical bat speed capacity"""
    # Baseline from height/weight
    baseline = 58.0 + (height - 70) * 1.2 + (weight - 180) * 0.05
    
    # Wingspan bonus
    ape_index = wingspan - height
    wingspan_bonus = ape_index * 1.5
    
    # Age factor (peak at 25-30)
    if 25 <= age <= 30:
        age_factor = 1.0
    elif age < 25:
        age_factor = 0.95 + (age - 20) * 0.01
    else:
        age_factor = 1.0 - (age - 30) * 0.01
    
    # Bat weight adjustment
    bat_adj = (31 - bat_weight) * 0.5
    
    capacity = (baseline + wingspan_bonus + bat_adj) * age_factor
    return capacity

# Calculate Kyle Tucker's exospeed capacity
kyle_tucker['exospeed_capacity_mph'] = calculate_exospeed_capacity(
    kyle_tucker['height_inches'],
    kyle_tucker['weight_lbs'],
    kyle_tucker['wingspan_inches'],
    kyle_tucker['age'],
    kyle_tucker['bat_weight_oz']
)

def calculate_krs_creation_score(pelvis_rot, torso_rot, x_factor):
    """
    Creation Score = Body rotation + separation quality
    
    Targets:
    - Pelvis: 45° (50 points max)
    - Torso: 35° (30 points max)
    - X-Factor: 20° (20 points max)
    """
    pelvis_score = (pelvis_rot / 45.0) * 50
    torso_score = (torso_rot / 35.0) * 30
    x_factor_score = (x_factor / 20.0) * 20
    
    creation_score = pelvis_score + torso_score + x_factor_score
    return min(100, creation_score), pelvis_score, torso_score, x_factor_score

def calculate_krs_transfer_score(bat_speed, capacity, sequence_gap_ms):
    """
    Transfer Score = How effectively energy transfers to bat
    
    Components:
    - Utilization: (bat_speed / capacity) * 70 points
    - Sequencing: Timing quality (max 30 points)
    """
    utilization = (bat_speed / capacity) * 70
    
    # Sequencing score based on timing gap
    # Optimal: 50-100ms gap (pelvis peaks, then torso)
    if 40 <= sequence_gap_ms <= 120:
        timing_score = 30
    elif 20 <= sequence_gap_ms < 40 or 120 < sequence_gap_ms <= 150:
        timing_score = 25
    elif 10 <= sequence_gap_ms < 20 or 150 < sequence_gap_ms <= 200:
        timing_score = 15
    else:
        timing_score = 5
    
    transfer_score = utilization + timing_score
    return min(100, transfer_score), utilization, timing_score

def determine_motor_profile(creation_score, transfer_score, pelvis_rot, torso_rot):
    """
    Determine motor profile based on scores and rotation
    """
    total_krs = (creation_score + transfer_score) / 2
    
    # Classify based on rotation quality
    if pelvis_rot >= 50 and torso_rot >= 30:
        profile = 'SYNCER'
        description = 'Elite body rotation with good separation'
        confidence = 0.90
    elif pelvis_rot >= 40 and torso_rot >= 25:
        profile = 'SPINNER'
        description = 'Good rotation, room for optimization'
        confidence = 0.85
    elif pelvis_rot < 30 or torso_rot < 20:
        profile = 'WHIPPER'
        description = 'Arm-dominant, needs body engagement'
        confidence = 0.80
    else:
        profile = 'DEVELOPING'
        description = 'Mixed mechanics, needs refinement'
        confidence = 0.75
    
    return {
        'type': profile,
        'confidence': confidence,
        'description': description
    }

def generate_krs_report(player):
    """Generate full KRS report"""
    
    print("=" * 70)
    print(f"⚾ KINEMATIC ROTATION SCORE (KRS) REPORT")
    print("=" * 70)
    print()
    print(f"Player: {player['player_name']}")
    print(f"Team: {player.get('team', 'N/A')}")
    print(f"Age: {player['age']}")
    print(f"Height: {player['height_inches']}\" ({player['height_inches'] / 12:.1f}')") 
    print(f"Weight: {player['weight_lbs']} lbs")
    print(f"Wingspan: {player['wingspan_inches']}\" (+{player['wingspan_inches'] - player['height_inches']}\" ape)")
    print(f"Session Date: {player['session_date']}")
    print()
    
    # Calculate scores
    creation_score, pelvis_pts, torso_pts, x_factor_pts = calculate_krs_creation_score(
        player['pelvis_rotation_deg'],
        player['torso_rotation_deg'],
        player['x_factor_deg']
    )
    
    transfer_score, util_pts, seq_pts = calculate_krs_transfer_score(
        player['estimated_bat_speed_mph'],
        player['exospeed_capacity_mph'],
        player['sequence_gap_ms']
    )
    
    total_krs = (creation_score + transfer_score) / 2
    
    motor_profile = determine_motor_profile(
        creation_score,
        transfer_score,
        player['pelvis_rotation_deg'],
        player['torso_rotation_deg']
    )
    
    # Print Rotation Metrics
    print("─" * 70)
    print("🔄 ROTATION METRICS")
    print("─" * 70)
    print()
    print(f"{'Metric':<30} {'Value':<15} {'Target':<15} {'% of Target':<15}")
    print("-" * 70)
    print(f"{'Pelvis Rotation':<30} {player['pelvis_rotation_deg']:.1f}° {'':<8} {'40-50°':<15} {(player['pelvis_rotation_deg']/45*100):.1f}%")
    print(f"{'Torso Rotation':<30} {player['torso_rotation_deg']:.1f}° {'':<8} {'30-40°':<15} {(player['torso_rotation_deg']/35*100):.1f}%")
    print(f"{'X-Factor (Separation)':<30} {player['x_factor_deg']:.1f}° {'':<8} {'15-25°':<15} {(player['x_factor_deg']/20*100):.1f}%")
    print()
    
    # Print Kinematic Sequence
    print("─" * 70)
    print("⚡ KINEMATIC SEQUENCE")
    print("─" * 70)
    print()
    print(f"Pelvis Peak Velocity: {player['pelvis_peak_velocity']:.0f}°/s")
    print(f"Torso Peak Velocity: {player['torso_peak_velocity']:.0f}°/s")
    print(f"Sequence Gap: {player['sequence_gap_ms']:.1f}ms")
    print(f"Sequence Quality: {'✅ EXCELLENT' if 40 <= player['sequence_gap_ms'] <= 120 else '⚠️ NEEDS WORK'}")
    print()
    
    # Print KRS Scores
    print("─" * 70)
    print("📊 KRS SCORES")
    print("─" * 70)
    print()
    print(f"CREATION SCORE: {creation_score:.1f}/100")
    print(f"  ├─ Pelvis Contribution: {pelvis_pts:.1f}/50")
    print(f"  ├─ Torso Contribution: {torso_pts:.1f}/30")
    print(f"  └─ X-Factor Bonus: {x_factor_pts:.1f}/20")
    print()
    print(f"TRANSFER SCORE: {transfer_score:.1f}/100")
    print(f"  ├─ Utilization: {util_pts:.1f}/70 ({player['estimated_bat_speed_mph']:.1f}/{player['exospeed_capacity_mph']:.1f} mph)")
    print(f"  └─ Sequencing: {seq_pts:.1f}/30")
    print()
    print(f"{'TOTAL KRS:':<20} {total_krs:.1f}/100")
    print()
    
    # Determine level
    if total_krs >= 90:
        level = "ELITE (Top 1%)"
    elif total_krs >= 80:
        level = "ADVANCED (Top 5%)"
    elif total_krs >= 70:
        level = "PROFICIENT (Top 15%)"
    elif total_krs >= 60:
        level = "DEVELOPING (Top 30%)"
    elif total_krs >= 50:
        level = "FOUNDATION (Top 50%)"
    else:
        level = "BEGINNER (Needs Development)"
    
    print(f"{'KRS Level:':<20} {level}")
    print()
    
    # Print Motor Profile
    print("─" * 70)
    print("🎯 MOTOR PROFILE")
    print("─" * 70)
    print()
    print(f"Classification: {motor_profile['type']}")
    print(f"Confidence: {motor_profile['confidence']*100:.0f}%")
    print(f"Description: {motor_profile['description']}")
    print()
    
    # Print Analysis Notes
    print("─" * 70)
    print("📝 ANALYSIS NOTES")
    print("─" * 70)
    print()
    print("Data Source: Single-camera video analysis (300fps)")
    print("Method: MediaPipe Pose Estimation + MLB estimation models")
    print("Limitation: Single-camera cannot measure precise 3D rotation")
    print("Confidence: Moderate to High (estimates conservative)")
    print("Recommendation: Values may be 5-10° higher with multi-camera system")
    print()
    print("Context:")
    print(f"  • MLB-level hitter (Chicago Cubs)")
    print(f"  • Estimated pitch speed: {player['pitch_speed_est_mph']} mph")
    print(f"  • Estimated bat speed: {player['estimated_bat_speed_mph']} mph")
    print(f"  • Estimated exit velocity: {player['estimated_exit_velocity_mph']} mph")
    print()
    
    print("=" * 70)
    print("✅ ANALYSIS COMPLETE")
    print("=" * 70)
    
    return {
        'creation_score': creation_score,
        'transfer_score': transfer_score,
        'total_krs': total_krs,
        'motor_profile': motor_profile,
        'level': level
    }

if __name__ == "__main__":
    results = generate_krs_report(kyle_tucker)
    
    # Save results
    output = {
        **kyle_tucker,
        **results
    }
    
    with open('/home/user/webapp/kyle_tucker_krs_report.json', 'w') as f:
        json.dump(output, f, indent=2)
    
    print()
    print("💾 Full report saved to: kyle_tucker_krs_report.json")
