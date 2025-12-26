#!/usr/bin/env python3
"""
Analyze Reboot Motion Momentum-Energy CSV
Extract key metrics for physics engine calibration
"""

import pandas as pd
import numpy as np
import sys

# Load the CSV
csv_path = "/home/user/uploaded_files/20251220_session_3_rebootmotion_ad25f0a5-d0d6-48bd-871c-f3d2a78e1576_baseball-hitting_momentum-energy.csv"

print("=" * 80)
print("REBOOT MOTION DATA ANALYSIS")
print("=" * 80)

try:
    df = pd.read_csv(csv_path)
    print(f"\n✅ Loaded CSV: {len(df)} frames, {len(df.columns)} columns")
    
    # Get time column
    if 'time' in df.columns:
        time_col = df['time']
        duration_s = time_col.max() - time_col.min()
        fps = len(df) / duration_s if duration_s > 0 else 0
        print(f"   Duration: {duration_s:.2f} seconds")
        print(f"   Estimated FPS: {fps:.1f}")
    
    # Find peak angular momentum for key segments
    print("\n" + "=" * 80)
    print("PEAK ANGULAR MOMENTUM (Kinetic Chain)")
    print("=" * 80)
    
    segments = {
        'Lower Torso (Pelvis)': 'lowertorso_angular_momentum_mag',
        'Torso': 'torso_angular_momentum_mag',
        'Left Arm': 'larm_angular_momentum_mag',
        'Right Arm': 'rarm_angular_momentum_mag',
        'Bat': 'bat_angular_momentum_mag'
    }
    
    peaks = {}
    for name, col in segments.items():
        if col in df.columns:
            peak_idx = df[col].idxmax()
            peak_value = df[col].max()
            peak_time = df.loc[peak_idx, 'time'] if 'time' in df.columns else peak_idx
            peaks[name] = {
                'value': peak_value,
                'time': peak_time,
                'frame': peak_idx
            }
            print(f"\n{name}:")
            print(f"  Peak: {peak_value:.4f}")
            if 'time' in df.columns:
                print(f"  Time: {peak_time:.3f}s")
            print(f"  Frame: {peak_idx}")
    
    # Calculate kinetic sequence gaps
    if len(peaks) >= 2:
        print("\n" + "=" * 80)
        print("KINETIC SEQUENCE TIMING (Time Between Peaks)")
        print("=" * 80)
        
        sequence = ['Lower Torso (Pelvis)', 'Torso', 'Right Arm', 'Bat']
        for i in range(len(sequence) - 1):
            if sequence[i] in peaks and sequence[i+1] in peaks:
                gap_ms = (peaks[sequence[i+1]]['time'] - peaks[sequence[i]]['time']) * 1000
                print(f"  {sequence[i]} → {sequence[i+1]}: {gap_ms:.1f}ms")
    
    # Bat speed analysis
    print("\n" + "=" * 80)
    print("BAT VELOCITY & ENERGY")
    print("=" * 80)
    
    if 'bat_kinetic_energy' in df.columns:
        peak_bat_energy = df['bat_kinetic_energy'].max()
        peak_bat_idx = df['bat_kinetic_energy'].idxmax()
        
        # Calculate bat velocity from kinetic energy
        # KE = 0.5 * m * v^2
        # Assume bat mass ~ 0.9 kg (32 oz)
        bat_mass_kg = 0.9
        if peak_bat_energy > 0:
            bat_velocity_ms = np.sqrt(2 * peak_bat_energy / bat_mass_kg)
            bat_velocity_mph = bat_velocity_ms * 2.23694
            
            print(f"\nPeak Bat Kinetic Energy: {peak_bat_energy:.4f} Joules")
            print(f"Estimated Bat Velocity: {bat_velocity_ms:.2f} m/s ({bat_velocity_mph:.1f} mph)")
            if 'time' in df.columns:
                print(f"Peak at: {df.loc[peak_bat_idx, 'time']:.3f}s (frame {peak_bat_idx})")
    
    # Total body energy
    if 'total_kinetic_energy' in df.columns:
        peak_total_energy = df['total_kinetic_energy'].max()
        print(f"\nPeak Total Body Energy: {peak_total_energy:.2f} Joules")
    
    # Event detection hints
    print("\n" + "=" * 80)
    print("EVENT DETECTION HINTS")
    print("=" * 80)
    
    # Find where bat angular momentum is near zero (stance)
    if 'bat_angular_momentum_mag' in df.columns:
        bat_angmom = df['bat_angular_momentum_mag']
        threshold = bat_angmom.max() * 0.1
        
        # Find first frame above threshold
        stance_end = None
        for idx in range(len(df)):
            if bat_angmom.iloc[idx] > threshold:
                stance_end = idx
                break
        
        # Find peak
        contact_frame = bat_angmom.idxmax()
        
        # Find when it drops below threshold again
        follow_through = None
        for idx in range(contact_frame, len(df)):
            if bat_angmom.iloc[idx] < threshold:
                follow_through = idx
                break
        
        if 'time' in df.columns:
            if stance_end is not None:
                print(f"\nStance/Load Start: Frame {stance_end}, Time {df.loc[stance_end, 'time']:.3f}s")
            print(f"Contact (Peak): Frame {contact_frame}, Time {df.loc[contact_frame, 'time']:.3f}s")
            if follow_through is not None:
                print(f"Follow-Through: Frame {follow_through}, Time {df.loc[follow_through, 'time']:.3f}s")
                swing_duration_s = df.loc[contact_frame, 'time'] - df.loc[stance_end, 'time'] if stance_end else 0
                print(f"\nSwing Duration: {swing_duration_s * 1000:.1f}ms")
    
    print("\n" + "=" * 80)
    print("KEY COLUMNS FOR CALIBRATION")
    print("=" * 80)
    print("\nAngular Momentum:")
    print("  - bat_angular_momentum_mag")
    print("  - torso_angular_momentum_mag")
    print("  - lowertorso_angular_momentum_mag")
    print("  - larm_angular_momentum_mag / rarm_angular_momentum_mag")
    print("\nEnergy:")
    print("  - bat_kinetic_energy")
    print("  - total_kinetic_energy")
    print("\nTiming:")
    print("  - time (absolute time in seconds)")
    print("  - time_from_max_hand (relative to peak hand velocity)")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
