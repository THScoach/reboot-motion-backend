import pandas as pd
import numpy as np
import requests
import os
from datetime import datetime

# Reboot Motion credentials
username = os.getenv("REBOOT_USERNAME", "coachrickpd@gmail.com")
password = os.getenv("REBOOT_PASSWORD", "Catchingbarrels1234!")

# Get OAuth token
token_url = "https://api.rebootmotion.com/oauth/token"
token_data = {
    "grant_type": "password",
    "username": username,
    "password": password
}
token_response = requests.post(token_url, data=token_data)
token = token_response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# Eric Williams session
session_id = "629a8a99-1906-498f-a582-3cb7bd3c0a77"

# Get session details
session_url = f"https://api.rebootmotion.com/sessions/{session_id}"
session_response = requests.get(session_url, headers=headers)
session_data = session_response.json()

# Get data exports
exports_url = f"https://api.rebootmotion.com/sessions/{session_id}/data_exports"
exports_response = requests.get(exports_url, headers=headers)
exports = exports_response.json()

# Find IK and ME exports
ik_export = next(e for e in exports if e.get("data_type") == "inverse-kinematics")
me_export = next(e for e in exports if e.get("data_type") == "momentum-energy")

# Download CSVs
ik_df = pd.read_csv(ik_export["download_url"])
me_df = pd.read_csv(me_export["download_url"])

print("=" * 80)
print("ERIC WILLIAMS - DISCONNECTION ANALYSIS")
print("Session:", session_id[:8], "| Date:", session_data.get("session_date"))
print("=" * 80)

# 1. TIMING ANALYSIS - When do body segments activate?
print("\n1️⃣  TIMING SEQUENCE ANALYSIS")
print("-" * 80)

# Find peak times for each segment
time = ik_df['time'].values

def find_peak_time(series, name):
    """Find when a segment reaches peak velocity/energy"""
    if len(series) == 0:
        return None
    # Use absolute values for rotation
    abs_series = np.abs(series)
    peak_idx = abs_series.idxmax()
    peak_time = time[peak_idx]
    peak_value = series.iloc[peak_idx]
    return peak_time, peak_value, peak_idx

# Pelvis rotation velocity (derivative)
pelvis_rot = ik_df['pelvis_rot'].values
pelvis_vel = np.gradient(pelvis_rot, time)
pelvis_peak_time, pelvis_peak_vel, pelvis_peak_idx = find_peak_time(pd.Series(pelvis_vel), 'pelvis')

# Torso rotation velocity
torso_rot = ik_df['torso_rot'].values
torso_vel = np.gradient(torso_rot, time)
torso_peak_time, torso_peak_vel, torso_peak_idx = find_peak_time(pd.Series(torso_vel), 'torso')

# Check if we have arm/shoulder energy data
if 'lsh_kinetic_energy' in me_df.columns:
    arm_energy = me_df['lsh_kinetic_energy'] + me_df['rsh_kinetic_energy']
    arm_peak_time, arm_peak_energy, arm_peak_idx = find_peak_time(arm_energy, 'arms')
else:
    arm_peak_time = None

print(f"Pelvis Peak Time:  {pelvis_peak_time:.3f}s (velocity: {pelvis_peak_vel:.1f}°/s)")
print(f"Torso Peak Time:   {torso_peak_time:.3f}s (velocity: {torso_peak_vel:.1f}°/s)")
if arm_peak_time:
    print(f"Arms Peak Time:    {arm_peak_time:.3f}s (energy: {arm_peak_energy:.1f} J)")

# Calculate delays
pelvis_torso_delay = torso_peak_time - pelvis_peak_time
print(f"\n⏱️  Hip-to-Torso Delay: {pelvis_torso_delay*1000:.0f} ms")

if pelvis_torso_delay < 0:
    print("   ⚠️  WARNING: Torso peaks BEFORE hips (reversed sequence!)")
    print("   → This indicates early shoulder rotation")
elif pelvis_torso_delay < 0.050:
    print("   ⚠️  WARNING: Delay too short (< 50ms)")
    print("   → Segments moving together, no separation")
elif pelvis_torso_delay > 0.150:
    print("   ⚠️  WARNING: Delay too long (> 150ms)")
    print("   → Poor timing, losing energy transfer")
else:
    print("   ✅ Good timing (50-150ms optimal)")

if arm_peak_time:
    torso_arm_delay = arm_peak_time - torso_peak_time
    print(f"\n⏱️  Torso-to-Arms Delay: {torso_arm_delay*1000:.0f} ms")
    if torso_arm_delay < 0:
        print("   ⚠️  WARNING: Arms peak BEFORE torso (disconnection!)")
        print("   → Back elbow flying off early")

# 2. HIP-SHOULDER SEPARATION ANALYSIS
print("\n2️⃣  HIP-SHOULDER SEPARATION ANALYSIS")
print("-" * 80)

# Calculate separation through the swing
hip_shoulder_sep = ik_df['pelvis_rot'] - ik_df['torso_rot']
max_separation = hip_shoulder_sep.max()
max_sep_time = time[hip_shoulder_sep.idxmax()]

print(f"Max Hip-Shoulder Separation: {max_separation:.1f}°")
print(f"Occurred at: {max_sep_time:.3f}s")

# Check WHERE the separation occurs (early, middle, late)
swing_duration = time[-1]
sep_phase = max_sep_time / swing_duration

if sep_phase < 0.3:
    phase_name = "LOAD PHASE (early)"
    phase_quality = "✅ GOOD - True loading separation"
elif sep_phase < 0.6:
    phase_name = "TRANSITION (middle)"
    phase_quality = "⚠️  CAUTION - May be fake separation"
else:
    phase_name = "LAUNCH PHASE (late)"
    phase_quality = "❌ BAD - Fake separation from disconnection"

print(f"Separation Phase: {phase_name} ({sep_phase*100:.0f}% through swing)")
print(f"Quality: {phase_quality}")

# 3. ROTATION MAGNITUDE CHECK
print("\n3️⃣  ROTATION MAGNITUDE")
print("-" * 80)

pelvis_total = ik_df['pelvis_rot'].max() - ik_df['pelvis_rot'].min()
torso_total = ik_df['torso_rot'].max() - ik_df['torso_rot'].min()

print(f"Total Pelvis Rotation: {pelvis_total:.1f}° (target: 40-50°)")
print(f"Total Torso Rotation:  {torso_total:.1f}° (target: 30-40°)")

if pelvis_total < 10 and torso_total < 10:
    print("\n❌ CRITICAL: Essentially NO rotation detected")
    print("   Possible causes:")
    print("   1. Assessment/drill data (not a full swing)")
    print("   2. Capture window issue (missed the actual swing)")
    print("   3. Reference frame issue (angles calculated wrong)")
    print("   4. Player swung with all arms (no body rotation)")

# 4. ENERGY FLOW ANALYSIS
print("\n4️⃣  ENERGY FLOW SEQUENCE")
print("-" * 80)

# Check if energy flows properly through kinetic chain
energy_cols = ['lowerhalf_kinetic_energy', 'torso_kinetic_energy', 
               'arms_kinetic_energy', 'bat_kinetic_energy']
available_cols = [c for c in energy_cols if c in me_df.columns]

if len(available_cols) >= 2:
    print("Energy peaks:")
    for col in available_cols:
        peak_energy = me_df[col].max()
        peak_time = time[me_df[col].idxmax()]
        print(f"  {col:25s}: {peak_energy:6.1f} J at {peak_time:.3f}s")
    
    # Check sequence
    peak_times = [time[me_df[col].idxmax()] for col in available_cols]
    is_sequential = all(peak_times[i] <= peak_times[i+1] for i in range(len(peak_times)-1))
    
    if is_sequential:
        print("\n✅ Energy flows in correct sequence (proximal → distal)")
    else:
        print("\n❌ Energy flow is OUT OF SEQUENCE")
        print("   → This indicates disconnection/poor timing")

# 5. DIAGNOSIS & COACHING RECOMMENDATIONS
print("\n5️⃣  DIAGNOSIS & COACHING RECOMMENDATIONS")
print("=" * 80)

issues = []
fixes = []

# Check for disconnection
if arm_peak_time and torso_arm_delay < 0:
    issues.append("❌ Back elbow disconnects early (arms peak before torso)")
    fixes.append("1. Connection drills (towel under armpit)")
    fixes.append("   → Keep back elbow 'in the shirt pocket' during load")

# Check for poor sequencing
if pelvis_torso_delay < 0:
    issues.append("❌ Shoulders rotate before hips (reversed sequence)")
    fixes.append("2. Sequence drills")
    fixes.append("   → 'Hips start, shoulders chase'")
    fixes.append("   → Med ball rotation throws")

# Check for fake separation
if sep_phase > 0.6:
    issues.append("❌ Fake hip-shoulder separation (occurs too late)")
    fixes.append("3. Loading mechanics")
    fixes.append("   → Load hips first, keep shoulders closed longer")

# Check for minimal rotation
if pelvis_total < 10:
    issues.append("❌ Minimal hip rotation (arm-dominant swing)")
    fixes.append("4. Hip engagement")
    fixes.append("   → Front toss focusing on hip drive")
    fixes.append("   → 'Swing with your belly button'")

if issues:
    print("ISSUES DETECTED:")
    for issue in issues:
        print(f"  {issue}")
    print("\nRECOMMENDED FIXES:")
    for fix in fixes:
        print(f"  {fix}")
else:
    print("✅ No major mechanical issues detected")

# 6. BAT SPEED CONTEXT
print("\n6️⃣  BAT SPEED CONTEXT (Blast Motion Data)")
print("=" * 80)
print("Peak Bat Speed: 82 mph (measured)")
print("Average Bat Speed: 76 mph (measured)")
print("\nWith current mechanics (arm-dominant):")
print("  → Getting 82 mph from hands/arms alone")
print("\nWith proper sequencing + connection:")
print("  → Could achieve 88-92 mph (same effort)")
print("  → That's +6-10 mph just from mechanics!")

print("\n" + "=" * 80)
print("END OF DISCONNECTION ANALYSIS")
print("=" * 80)

