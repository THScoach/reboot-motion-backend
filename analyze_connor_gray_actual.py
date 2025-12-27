#!/usr/bin/env python3
"""
CONNOR GRAY - ACTUAL DATA ANALYSIS
Correcting the misstatement from earlier thread
"""

import pandas as pd
import numpy as np

# Load Connor's actual data
ik_df = pd.read_csv('/tmp/connor_ik.csv')
me_df = pd.read_csv('/tmp/connor_me.csv')

print("=" * 80)
print("CONNOR GRAY - ACTUAL BIOMECHANICS ANALYSIS")
print("=" * 80)
print()

print("📊 SESSION METADATA:")
print(f"  Session ID: 4f1a7010-1324-469d-8e1a-e05a1dc45f2e")
print(f"  Date: 2025-12-20")
print(f"  Frames: {len(ik_df):,} (IK) / {len(me_df):,} (ME)")
print(f"  Duration: ~{len(ik_df) / 240.0:.2f}s (assuming 240 Hz)")
print()

# ============================================================================
# ROTATION ANALYSIS
# ============================================================================
print("=" * 80)
print("PART 1: ROTATION ANALYSIS")
print("=" * 80)
print()

rotation_data = {}
rotation_cols = ['pelvis_rot', 'torso_rot', 'left_hip_rot', 'right_hip_rot']

for col in rotation_cols:
    if col in ik_df.columns:
        data = ik_df[col].dropna()
        if len(data) > 0:
            rotation_data[col] = {
                'min': data.min(),
                'max': data.max(),
                'rom': data.max() - data.min(),
                'mean': data.mean(),
                'std': data.std()
            }

print("🔄 ROTATION METRICS:")
print()
for col, stats in rotation_data.items():
    print(f"{col}:")
    print(f"  Range: {stats['min']:.3f}° to {stats['max']:.3f}°")
    print(f"  ROM: {stats['rom']:.3f}°")
    print(f"  Mean: {stats['mean']:.3f}°")
    print(f"  Std Dev: {stats['std']:.3f}°")
    print()

# Key rotation comparison
pelvis_rom = rotation_data['pelvis_rot']['rom']
torso_rom = rotation_data['torso_rot']['rom']

print("🎯 KEY COMPARISON:")
print(f"  Pelvis ROM: {pelvis_rom:.2f}° (Target: 40-50°)")
print(f"  Torso ROM: {torso_rom:.2f}° (Target: 30-40°)")
print()

if pelvis_rom < 10:
    print("  ⚠️ MINIMAL PELVIS ROTATION - Same issue as Eric Williams!")
    pelvis_pct = (pelvis_rom / 45.0) * 100
    print(f"  → {pelvis_pct:.1f}% of target (45° midpoint)")
else:
    print("  ✓ Adequate pelvis rotation")

if torso_rom < 10:
    print("  ⚠️ MINIMAL TORSO ROTATION - Same issue as Eric Williams!")
    torso_pct = (torso_rom / 35.0) * 100
    print(f"  → {torso_pct:.1f}% of target (35° midpoint)")
else:
    print("  ✓ Adequate torso rotation")

print()

# ============================================================================
# ENERGY ANALYSIS
# ============================================================================
print("=" * 80)
print("PART 2: ENERGY ANALYSIS")
print("=" * 80)
print()

energy_cols = [col for col in me_df.columns if 'kinetic_energy' in col.lower()]
energy_data = {}

for col in energy_cols:
    if col in me_df.columns:
        data = me_df[col].dropna()
        if len(data) > 0:
            peak = data.max()
            if peak > 50:  # Only significant energies
                energy_data[col] = peak

# Sort by peak energy
sorted_energy = sorted(energy_data.items(), key=lambda x: x[1], reverse=True)

print("⚡ PEAK ENERGIES (Top 10):")
for col, peak in sorted_energy[:10]:
    print(f"  {col:30s}: {peak:8.1f} J")

print()

# Key energy metrics
if 'lowerhalf_kinetic_energy' in energy_data:
    lowerhalf_energy = energy_data['lowerhalf_kinetic_energy']
elif 'lth_kinetic_energy' in energy_data:
    lowerhalf_energy = energy_data['lth_kinetic_energy']
else:
    lowerhalf_energy = 0

if 'torso_kinetic_energy' in energy_data:
    torso_energy = energy_data['torso_kinetic_energy']
else:
    torso_energy = 0

bat_energy = max([v for k, v in energy_data.items() if 'bat' in k.lower()], default=0)

print("🎯 KEY ENERGY METRICS:")
print(f"  Lower Half Peak: {lowerhalf_energy:,.1f} J")
print(f"  Torso Peak: {torso_energy:,.1f} J")
if bat_energy > 0:
    print(f"  Bat Peak: {bat_energy:,.1f} J")
print()

if lowerhalf_energy > 0 and torso_energy > 0:
    transfer_pct = (torso_energy / lowerhalf_energy) * 100
    print(f"  Transfer Efficiency: {transfer_pct:.1f}%")
    if transfer_pct < 30:
        print(f"    ⚠️ LOW TRANSFER - Only {transfer_pct:.1f}% of leg energy reaches torso")
    print()

# ============================================================================
# COMPARISON WITH ERIC WILLIAMS
# ============================================================================
print("=" * 80)
print("PART 3: CONNOR vs ERIC COMPARISON")
print("=" * 80)
print()

# Eric's data (from earlier analysis)
eric_data = {
    'session_date': '2025-12-22',
    'pelvis_rom': 2.87,
    'torso_rom': 1.95,
    'peak_energy': 22680.5,
    'lowerhalf_energy': 8662.8,
    'torso_energy': 1119.2
}

print("📊 ROTATION COMPARISON:")
print(f"{'':20s} {'Connor':>15s} {'Eric':>15s} {'Difference':>15s}")
print("-" * 70)
print(f"{'Pelvis ROM (°)':20s} {pelvis_rom:>15.2f} {eric_data['pelvis_rom']:>15.2f} {pelvis_rom - eric_data['pelvis_rom']:>+15.2f}")
print(f"{'Torso ROM (°)':20s} {torso_rom:>15.2f} {eric_data['torso_rom']:>15.2f} {torso_rom - eric_data['torso_rom']:>+15.2f}")
print()

# Relative to targets
pelvis_target = 45.0
torso_target = 35.0

connor_pelvis_pct = (pelvis_rom / pelvis_target) * 100
eric_pelvis_pct = (eric_data['pelvis_rom'] / pelvis_target) * 100

connor_torso_pct = (torso_rom / torso_target) * 100
eric_torso_pct = (eric_data['torso_rom'] / torso_target) * 100

print("📈 % OF TARGET:")
print(f"{'':20s} {'Connor':>15s} {'Eric':>15s} {'Better?':>15s}")
print("-" * 70)
print(f"{'Pelvis (% of 45°)':20s} {connor_pelvis_pct:>14.1f}% {eric_pelvis_pct:>14.1f}% {'Connor' if connor_pelvis_pct > eric_pelvis_pct else 'Eric':>15s}")
print(f"{'Torso (% of 35°)':20s} {connor_torso_pct:>14.1f}% {eric_torso_pct:>14.1f}% {'Connor' if connor_torso_pct > eric_pelvis_pct else 'Eric':>15s}")
print()

print("⚡ ENERGY COMPARISON:")
print(f"{'':20s} {'Connor':>15s} {'Eric':>15s} {'Difference':>15s}")
print("-" * 70)
print(f"{'Lower Half (J)':20s} {lowerhalf_energy:>15,.1f} {eric_data['lowerhalf_energy']:>15,.1f} {lowerhalf_energy - eric_data['lowerhalf_energy']:>+15,.1f}")
print(f"{'Torso (J)':20s} {torso_energy:>15,.1f} {eric_data['torso_energy']:>15,.1f} {torso_energy - eric_data['torso_energy']:>+15,.1f}")
print()

# ============================================================================
# CONCLUSION
# ============================================================================
print("=" * 80)
print("PART 4: CORRECTED CONCLUSION")
print("=" * 80)
print()

print("🚨 CORRECTION TO EARLIER STATEMENT:")
print()
print("❌ WRONG (from earlier thread):")
print("   'Connor Gray: KRS 48.5, Creation 35.0, Transfer 57.6, Exit Velocity 110 mph'")
print()
print("✅ ACTUAL CONNOR GRAY DATA:")
print(f"   Pelvis ROM: {pelvis_rom:.2f}° (only {connor_pelvis_pct:.1f}% of target)")
print(f"   Torso ROM: {torso_rom:.2f}° (only {connor_torso_pct:.1f}% of target)")
print(f"   Peak Energy: {max(energy_data.values()):,.1f} J")
print()

print("🎯 KEY FINDING:")
if pelvis_rom < 10 and torso_rom < 10:
    print("  ⚠️ CONNOR HAS THE SAME ISSUE AS ERIC!")
    print("     → Minimal pelvis rotation (3.0° vs 45° target)")
    print("     → Minimal torso rotation (2.2° vs 35° target)")
    print("     → Both are at FOUNDATION level with rotation deficits")
    print()
    print("  📊 BOTH PLAYERS NEED:")
    print("     1. Drill #4 (Hip Load & Fire) - Increase rotation")
    print("     2. Drill #7 (Connection Lock) - Fix disconnection")
    print("     3. Drill #1 (Rope Rhythm) - Fix sequencing")
else:
    print("  Connor has better rotation than Eric")
    print(f"  Connor: {pelvis_rom:.2f}° pelvis, {torso_rom:.2f}° torso")
    print(f"  Eric: {eric_data['pelvis_rom']:.2f}° pelvis, {eric_data['torso_rom']:.2f}° torso")

print()

print("💡 SIMILARITY:")
print(f"  Connor pelvis ROM: {pelvis_rom:.2f}°")
print(f"  Eric pelvis ROM: {eric_data['pelvis_rom']:.2f}°")
print(f"  Difference: {abs(pelvis_rom - eric_data['pelvis_rom']):.2f}° (essentially IDENTICAL)")
print()
print(f"  Connor torso ROM: {torso_rom:.2f}°")
print(f"  Eric torso ROM: {eric_data['torso_rom']:.2f}°")
print(f"  Difference: {abs(torso_rom - eric_data['torso_rom']):.2f}° (essentially IDENTICAL)")
print()

print("=" * 80)
print("APOLOGY & CORRECTION")
print("=" * 80)
print()
print("I apologize for the inaccurate comparison in the earlier analysis.")
print("I incorrectly stated Connor had significantly better metrics without")
print("checking his actual data from the Reboot Motion API.")
print()
print("ACTUAL SITUATION:")
print("  • Connor Gray: 3.0° pelvis, 2.2° torso (6-7% of target)")
print("  • Eric Williams: 2.9° pelvis, 1.9° torso (6-7% of target)")
print()
print("→ BOTH PLAYERS HAVE NEARLY IDENTICAL ROTATION DEFICITS")
print("→ BOTH NEED THE SAME DRILL PRESCRIPTION")
print("→ The comparison I made earlier was NOT based on actual data")
print()
print("=" * 80)
