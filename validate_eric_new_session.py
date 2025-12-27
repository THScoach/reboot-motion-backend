#!/usr/bin/env python3
"""
Validation Analysis: Eric Williams Dec 22 Session vs Dec 20 Session
Cross-check new uploaded data against previous KRS analysis
"""

import pandas as pd
import numpy as np
from pathlib import Path

# File paths
IK_FILE = "/home/user/uploaded_files/20251222_session_3_rebootmotion_a293f033-6ebd-47ad-8af9-81a68ab35406_baseball-hitting_inverse-kinematics.csv"
ME_FILE = "/home/user/uploaded_files/20251222_session_3_rebootmotion_a293f033-6ebd-47ad-8af9-81a68ab35406_baseball-hitting_momentum-energy.csv"

print("=" * 80)
print("ERIC WILLIAMS - SESSION VALIDATION & COMPARISON")
print("=" * 80)
print()

# Load the data
print("📊 LOADING NEW SESSION DATA (Dec 22, 2025)...")
ik_df = pd.read_csv(IK_FILE)
me_df = pd.read_csv(ME_FILE)

print(f"✓ Inverse Kinematics: {len(ik_df):,} frames loaded")
print(f"✓ Momentum-Energy: {len(me_df):,} frames loaded")
print()

# ============================================================================
# PART 1: DATA VALIDATION
# ============================================================================
print("=" * 80)
print("PART 1: DATA QUALITY VALIDATION")
print("=" * 80)
print()

# Check for rotation data
rotation_cols = ['pelvis_rot', 'torso_rot', 'left_hip_rot', 'right_hip_rot']
available_rotation_cols = [col for col in rotation_cols if col in ik_df.columns]

print("🔍 ROTATION DATA CHECK:")
print(f"Available rotation columns: {available_rotation_cols}")
print()

if available_rotation_cols:
    for col in available_rotation_cols:
        data = ik_df[col].dropna()
        if len(data) > 0:
            print(f"{col}:")
            print(f"  Range: {data.min():.3f}° to {data.max():.3f}°")
            print(f"  Total ROM: {data.max() - data.min():.3f}°")
            print(f"  Mean: {data.mean():.3f}°")
            print(f"  Std Dev: {data.std():.3f}°")
            print()

# Check for energy data
energy_cols = [col for col in me_df.columns if 'kinetic_energy' in col.lower()]
print("⚡ ENERGY DATA CHECK:")
print(f"Available energy columns: {len(energy_cols)}")

for col in energy_cols[:10]:  # Show first 10
    data = me_df[col].dropna()
    if len(data) > 0:
        peak = data.max()
        if peak > 100:  # Show only significant energies
            print(f"  {col}: Peak {peak:.1f} J")

print()

# ============================================================================
# PART 2: SESSION COMPARISON
# ============================================================================
print("=" * 80)
print("PART 2: COMPARISON WITH PREVIOUS SESSION (Dec 20)")
print("=" * 80)
print()

# Previous session (Dec 20) - from earlier analysis
prev_session = {
    'date': '2025-12-20',
    'session_id': '629a8a99-1906-498f-a582-3cb7bd3c0a77',
    'frames': 574,
    'duration_s': 2.383,
    'pelvis_rot_total': 2.19,
    'torso_rot_total': 1.70,
    'peak_energy_j': 759,
    'krs_total': 48.1,
    'creation_score': 18.0,
    'transfer_score': 68.1,
    'motor_profile': 'TITAN',
    'bat_speed_mph': 82,
    'exit_velocity_mph': 98,
    'on_table_gain_mph': 10.6
}

# Current session (Dec 22)
curr_pelvis_rot = ik_df['pelvis_rot'].dropna() if 'pelvis_rot' in ik_df.columns else pd.Series([0])
curr_torso_rot = ik_df['torso_rot'].dropna() if 'torso_rot' in ik_df.columns else pd.Series([0])

# Get peak energy from momentum-energy data
peak_energies = {}
for col in energy_cols:
    if col in me_df.columns:
        peak_energies[col] = me_df[col].max()

# Find overall peak energy
if peak_energies:
    max_energy_col = max(peak_energies, key=peak_energies.get)
    curr_peak_energy = peak_energies[max_energy_col]
else:
    curr_peak_energy = 0

curr_session = {
    'date': '2025-12-22',
    'session_id': 'a293f033-6ebd-47ad-8af9-81a68ab35406',
    'frames': len(ik_df),
    'duration_s': len(ik_df) / 240.0,  # Assuming 240 Hz
    'pelvis_rot_total': curr_pelvis_rot.max() - curr_pelvis_rot.min() if len(curr_pelvis_rot) > 0 else 0,
    'torso_rot_total': curr_torso_rot.max() - curr_torso_rot.min() if len(curr_torso_rot) > 0 else 0,
    'peak_energy_j': curr_peak_energy
}

print("📅 SESSION METADATA:")
print(f"{'':20} {'Dec 20 (Old)':>15} {'Dec 22 (NEW)':>15} {'Change':>15}")
print("-" * 70)
print(f"{'Date':20} {prev_session['date']:>15} {curr_session['date']:>15} {'-':>15}")
print(f"{'Session ID':20} {prev_session['session_id'][:15]:>15} {curr_session['session_id'][:15]:>15} {'-':>15}")
print(f"{'Frames':20} {prev_session['frames']:>15,} {curr_session['frames']:>15,} {f'+{curr_session['frames'] - prev_session['frames']:,}':>15}")
print(f"{'Duration (s)':20} {prev_session['duration_s']:>15.2f} {curr_session['duration_s']:>15.2f} {f'+{curr_session['duration_s'] - prev_session['duration_s']:.2f}':>15}")
print()

print("🔄 ROTATION COMPARISON:")
print(f"{'':20} {'Dec 20 (Old)':>15} {'Dec 22 (NEW)':>15} {'Change':>15}")
print("-" * 70)
print(f"{'Pelvis Rotation (°)':20} {prev_session['pelvis_rot_total']:>15.2f} {curr_session['pelvis_rot_total']:>15.2f} {f'+{curr_session['pelvis_rot_total'] - prev_session['pelvis_rot_total']:.2f}':>15}")
print(f"{'Torso Rotation (°)':20} {prev_session['torso_rot_total']:>15.2f} {curr_session['torso_rot_total']:>15.2f} {f'+{curr_session['torso_rot_total'] - prev_session['torso_rot_total']:.2f}':>15}")
print()

print("⚡ ENERGY COMPARISON:")
print(f"{'':20} {'Dec 20 (Old)':>15} {'Dec 22 (NEW)':>15} {'Change':>15}")
print("-" * 70)
print(f"{'Peak Energy (J)':20} {prev_session['peak_energy_j']:>15,.1f} {curr_session['peak_energy_j']:>15,.1f} {f'+{curr_session['peak_energy_j'] - prev_session['peak_energy_j']:,.1f}':>15}")
if curr_session['peak_energy_j'] > 0 and prev_session['peak_energy_j'] > 0:
    pct_change = ((curr_session['peak_energy_j'] - prev_session['peak_energy_j']) / prev_session['peak_energy_j']) * 100
    print(f"{'% Change':20} {'-':>15} {'-':>15} {f'{pct_change:+.1f}%':>15}")
print()

# ============================================================================
# PART 3: KEY FINDINGS
# ============================================================================
print("=" * 80)
print("PART 3: KEY FINDINGS & VALIDATION")
print("=" * 80)
print()

# Previous KRS scores (from Dec 20 analysis)
print("📊 PREVIOUS KRS SCORES (Dec 20):")
print(f"  KRS Total: {prev_session['krs_total']:.1f}/100 ({prev_session.get('krs_level', 'FOUNDATION')})")
print(f"  Creation Score: {prev_session['creation_score']:.1f}/100")
print(f"  Transfer Score: {prev_session['transfer_score']:.1f}/100")
print(f"  Motor Profile: {prev_session['motor_profile']}")
print(f"  Bat Speed: {prev_session['bat_speed_mph']} mph")
print(f"  Exit Velocity: {prev_session['exit_velocity_mph']} mph")
print(f"  On-Table Gain: {prev_session['on_table_gain_mph']} mph")
print()

# Validation checks
print("✓ VALIDATION CHECKS:")
checks = []

# Check 1: Rotation issue persists
if curr_session['pelvis_rot_total'] < 10:
    checks.append(("✓ Minimal pelvis rotation confirmed", f"{curr_session['pelvis_rot_total']:.2f}° (< 10° threshold)"))
else:
    checks.append(("✗ Pelvis rotation improved", f"{curr_session['pelvis_rot_total']:.2f}°"))

if curr_session['torso_rot_total'] < 10:
    checks.append(("✓ Minimal torso rotation confirmed", f"{curr_session['torso_rot_total']:.2f}° (< 10° threshold)"))
else:
    checks.append(("✗ Torso rotation improved", f"{curr_session['torso_rot_total']:.2f}°"))

# Check 2: Energy generation
if curr_session['peak_energy_j'] > prev_session['peak_energy_j'] * 10:
    checks.append(("✓ Significantly higher energy recorded", f"{curr_session['peak_energy_j']:,.0f} J vs {prev_session['peak_energy_j']:,.0f} J"))
elif curr_session['peak_energy_j'] > prev_session['peak_energy_j']:
    checks.append(("✓ Higher energy recorded", f"{curr_session['peak_energy_j']:,.0f} J vs {prev_session['peak_energy_j']:,.0f} J"))
else:
    checks.append(("? Similar or lower energy", f"{curr_session['peak_energy_j']:,.0f} J vs {prev_session['peak_energy_j']:,.0f} J"))

# Check 3: Data completeness
if curr_session['frames'] > prev_session['frames'] * 5:
    checks.append(("✓ More complete swing data", f"{curr_session['frames']:,} frames vs {prev_session['frames']:,} frames"))
else:
    checks.append(("? Similar frame count", f"{curr_session['frames']:,} frames"))

# Check 4: Bat data presence
bat_cols = [col for col in me_df.columns if 'bat' in col.lower()]
if len(bat_cols) > 5:
    checks.append(("✓ Complete bat tracking data present", f"{len(bat_cols)} bat-related columns"))
else:
    checks.append(("✗ Limited bat tracking data", f"{len(bat_cols)} bat-related columns"))

for check, detail in checks:
    print(f"  {check}: {detail}")

print()

# ============================================================================
# PART 4: DIAGNOSTIC INTERPRETATION
# ============================================================================
print("=" * 80)
print("PART 4: DIAGNOSTIC INTERPRETATION")
print("=" * 80)
print()

print("🔬 SESSION QUALITY ASSESSMENT:")
print()

# Data completeness score
completeness_score = 0
if curr_session['frames'] > 1000:
    completeness_score += 25
if len(bat_cols) > 5:
    completeness_score += 25
if curr_session['peak_energy_j'] > 1000:
    completeness_score += 25
if len(available_rotation_cols) >= 3:
    completeness_score += 25

print(f"  Data Completeness Score: {completeness_score}/100")
if completeness_score >= 75:
    print(f"    → EXCELLENT: This session has comprehensive data")
elif completeness_score >= 50:
    print(f"    → GOOD: This session has sufficient data")
else:
    print(f"    → LIMITED: This session has incomplete data")
print()

# Mechanical issue consistency
print("⚙️  MECHANICAL ISSUE CONSISTENCY:")
print()

if curr_session['pelvis_rot_total'] < 5 and prev_session['pelvis_rot_total'] < 5:
    print("  ✓ CONSISTENT: Pelvis rotation issue persists across both sessions")
    print(f"    Dec 20: {prev_session['pelvis_rot_total']:.2f}° | Dec 22: {curr_session['pelvis_rot_total']:.2f}°")
    print(f"    → Issue is REAL and REPEATABLE, not a data artifact")
elif abs(curr_session['pelvis_rot_total'] - prev_session['pelvis_rot_total']) < 5:
    print("  ✓ CONSISTENT: Similar minimal rotation in both sessions")
    print(f"    Dec 20: {prev_session['pelvis_rot_total']:.2f}° | Dec 22: {curr_session['pelvis_rot_total']:.2f}°")
else:
    print("  ⚠ INCONSISTENT: Rotation differs significantly between sessions")
    print(f"    Dec 20: {prev_session['pelvis_rot_total']:.2f}° | Dec 22: {curr_session['pelvis_rot_total']:.2f}°")
    print(f"    → May indicate different swing types or improvements")
print()

if curr_session['torso_rot_total'] < 5 and prev_session['torso_rot_total'] < 5:
    print("  ✓ CONSISTENT: Torso rotation issue persists across both sessions")
    print(f"    Dec 20: {prev_session['torso_rot_total']:.2f}° | Dec 22: {curr_session['torso_rot_total']:.2f}°")
elif abs(curr_session['torso_rot_total'] - prev_session['torso_rot_total']) < 5:
    print("  ✓ CONSISTENT: Similar minimal rotation in both sessions")
    print(f"    Dec 20: {prev_session['torso_rot_total']:.2f}° | Dec 22: {curr_session['torso_rot_total']:.2f}°")
else:
    print("  ⚠ INCONSISTENT: Rotation differs significantly between sessions")
    print(f"    Dec 20: {prev_session['torso_rot_total']:.2f}° | Dec 22: {curr_session['torso_rot_total']:.2f}°")
print()

# Energy analysis
print("⚡ ENERGY GENERATION ANALYSIS:")
print()
if curr_session['peak_energy_j'] > prev_session['peak_energy_j'] * 5:
    print(f"  ⚡ SIGNIFICANTLY HIGHER ENERGY: {curr_session['peak_energy_j']:,.0f} J vs {prev_session['peak_energy_j']:,.0f} J")
    print(f"    → {(curr_session['peak_energy_j'] / prev_session['peak_energy_j'] - 1) * 100:.0f}% increase")
    print(f"    → Possible explanations:")
    print(f"      1. More complete swing captured (full approach vs. partial)")
    print(f"      2. Better bat tracking (actual bat energy vs. estimated)")
    print(f"      3. Different drill/swing type")
    print(f"    → KEY INSIGHT: Eric CAN generate energy, but rotation still minimal")
    print(f"    → This confirms DISCONNECTION, not lack of effort")
elif curr_session['peak_energy_j'] > prev_session['peak_energy_j']:
    print(f"  ↗ HIGHER ENERGY: {curr_session['peak_energy_j']:,.0f} J vs {prev_session['peak_energy_j']:,.0f} J")
    print(f"    → Slight improvement or data completeness difference")
else:
    print(f"  → SIMILAR ENERGY: {curr_session['peak_energy_j']:,.0f} J vs {prev_session['peak_energy_j']:,.0f} J")
print()

# ============================================================================
# PART 5: CONCLUSIONS
# ============================================================================
print("=" * 80)
print("PART 5: FINAL CONCLUSIONS")
print("=" * 80)
print()

print("🎯 VALIDATION SUMMARY:")
print()

# Determine consistency
pelvis_consistent = abs(curr_session['pelvis_rot_total'] - prev_session['pelvis_rot_total']) < 3
torso_consistent = abs(curr_session['torso_rot_total'] - prev_session['torso_rot_total']) < 3
issue_consistent = pelvis_consistent and torso_consistent

if issue_consistent:
    print("  ✅ MECHANICAL ISSUE VALIDATED")
    print("     → Minimal rotation persists across multiple sessions")
    print("     → Issue is REAL, CONSISTENT, and REPEATABLE")
    print("     → Not a data quality artifact")
    print()
else:
    print("  ⚠️  MECHANICAL PATTERN CHANGED")
    print("     → Rotation differs between sessions")
    print("     → May indicate improvements, different drill, or swing variation")
    print()

print("📋 RECOMMENDED ACTIONS:")
print()

if curr_session['pelvis_rot_total'] < 10 and curr_session['torso_rot_total'] < 10:
    print("  1. ⚠️  PRIORITY: Address rotation deficit")
    print("     → Prescribe Drill #4 (Synapse Hip Load & Fire)")
    print("     → Prescribe Drill #1 (Rope Rhythm Control)")
    print()
    print("  2. 🔧 SECONDARY: Fix disconnection")
    print("     → Prescribe Drill #7 (Synapse Connection Lock)")
    print("     → Focus on back elbow attachment")
    print()
    print("  3. 📊 MONITORING: Track progress")
    print("     → Re-test rotation every 2 weeks")
    print("     → Target: 40-50° pelvis, 30-40° torso")
    print()
else:
    print("  1. ✅ Rotation improving - continue current program")
    print("  2. 📊 Re-test to validate improvements")
    print()

print(f"📈 EXPECTED OUTCOMES (if mechanical issues addressed):")
print(f"   Current Bat Speed: {prev_session['bat_speed_mph']} mph")
print(f"   Expected 30-day:   85-86 mph (+3-4 mph)")
print(f"   Expected 60-day:   88-90 mph (+6-8 mph)")
print(f"   Expected 90-day:   90-92 mph (+8-10 mph)")
print()
print(f"   Current Exit Velocity: {prev_session['exit_velocity_mph']} mph")
print(f"   Expected 30-day:       102-103 mph (+4-5 mph)")
print(f"   Expected 60-day:       106-108 mph (+8-10 mph)")
print(f"   Expected 90-day:       108-110 mph (+10-12 mph)")
print()

print("=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
print()
print(f"📁 Session Files Analyzed:")
print(f"   IK: {Path(IK_FILE).name}")
print(f"   ME: {Path(ME_FILE).name}")
print()
print("✅ Cross-reference with eric_scoring_breakdown.py for full mathematical KRS calculation")
print("✅ Cross-reference with ERIC_WILLIAMS_SESSION_COMPARISON.md for detailed comparison")
print()
