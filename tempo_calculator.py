#!/usr/bin/env python3
"""
TEMPO CALCULATION SCRIPT
========================
For use with Reboot Motion momentum-energy CSV exports

This script calculates the correct tempo ratio from biomechanics data.
Validated against Connor Gray ground truth: 3.38:1

Author: Catching Barrels
Date: December 2025
"""

import pandas as pd
import numpy as np

# ============================================================================
# CONFIGURATION
# ============================================================================

# File path - update this to your CSV location
CSV_PATH = "/mnt/user-data/uploads/1766451097841_20251220_session_7_rebootmotion_80e77691-d7cc-4ebb-b955-2fd45676f0ca_baseball-hitting_momentum-energy__1_.csv"

# Time windows for phase detection (in seconds, relative to contact at 0)
LOAD_START_WINDOW = (-2.5, -0.5)   # Where to look for load start (min energy)
HIP_PEAK_WINDOW = (-1.0, -0.1)     # Where to look for hip peak (max energy)

# Expected ranges for validation
EXPECTED_TEMPO_RANGE = (2.0, 4.0)  # Optimal tempo ratio
EXPECTED_LOAD_RANGE = (1.0, 2.0)   # Load duration in seconds
EXPECTED_LAUNCH_RANGE = (0.3, 0.6) # Launch duration in seconds

# ============================================================================
# MAIN ANALYSIS
# ============================================================================

def calculate_tempo(df, verbose=True):
    """
    Calculate tempo ratio from Reboot momentum-energy data.
    
    Tempo = Load Duration / Launch Duration
    
    Where:
    - Load Duration: time from load start to hip peak
    - Launch Duration: time from hip peak to contact
    
    Returns dict with all tempo metrics
    """
    
    results = {}
    
    # ----------------------------------------
    # STEP 1: Validate required columns
    # ----------------------------------------
    required_cols = ['time_from_max_hand', 'lowerhalf_kinetic_energy']
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    if verbose:
        print("=" * 70)
        print("TEMPO CALCULATION")
        print("=" * 70)
        print(f"\nData points: {len(df)}")
        print(f"Time range: {df['time_from_max_hand'].min():.3f}s to {df['time_from_max_hand'].max():.3f}s")
    
    # ----------------------------------------
    # STEP 2: Find CONTACT frame (time = 0)
    # ----------------------------------------
    contact_idx = df['time_from_max_hand'].abs().idxmin()
    contact_time = df.loc[contact_idx, 'time_from_max_hand']
    contact_ke = df.loc[contact_idx, 'lowerhalf_kinetic_energy']
    
    results['contact_time'] = contact_time
    results['contact_ke'] = contact_ke
    
    if verbose:
        print(f"\n[CONTACT]")
        print(f"  Frame: {contact_idx}")
        print(f"  Time: {contact_time:.4f}s (should be ~0)")
        print(f"  Lower Half KE: {contact_ke:.1f} J")
    
    # ----------------------------------------
    # STEP 3: Find LOAD START (minimum lower half KE)
    # ----------------------------------------
    # Look in the window before hip rotation begins
    load_window = df[
        (df['time_from_max_hand'] >= LOAD_START_WINDOW[0]) & 
        (df['time_from_max_hand'] <= LOAD_START_WINDOW[1])
    ]
    
    if len(load_window) == 0:
        raise ValueError(f"No data in load start window {LOAD_START_WINDOW}")
    
    load_start_idx = load_window['lowerhalf_kinetic_energy'].idxmin()
    load_start_time = df.loc[load_start_idx, 'time_from_max_hand']
    load_start_ke = df.loc[load_start_idx, 'lowerhalf_kinetic_energy']
    
    results['load_start_time'] = load_start_time
    results['load_start_ke'] = load_start_ke
    
    if verbose:
        print(f"\n[LOAD START] (min KE in window {LOAD_START_WINDOW})")
        print(f"  Frame: {load_start_idx}")
        print(f"  Time: {load_start_time:.3f}s")
        print(f"  Lower Half KE: {load_start_ke:.1f} J")
    
    # ----------------------------------------
    # STEP 4: Find HIP PEAK (maximum lower half KE)
    # ----------------------------------------
    # This is when hip rotation is at maximum speed
    # BEFORE energy transfers to torso
    hip_window = df[
        (df['time_from_max_hand'] >= HIP_PEAK_WINDOW[0]) & 
        (df['time_from_max_hand'] <= HIP_PEAK_WINDOW[1])
    ]
    
    if len(hip_window) == 0:
        raise ValueError(f"No data in hip peak window {HIP_PEAK_WINDOW}")
    
    hip_peak_idx = hip_window['lowerhalf_kinetic_energy'].idxmax()
    hip_peak_time = df.loc[hip_peak_idx, 'time_from_max_hand']
    hip_peak_ke = df.loc[hip_peak_idx, 'lowerhalf_kinetic_energy']
    
    results['hip_peak_time'] = hip_peak_time
    results['hip_peak_ke'] = hip_peak_ke
    
    if verbose:
        print(f"\n[HIP PEAK] (max KE in window {HIP_PEAK_WINDOW})")
        print(f"  Frame: {hip_peak_idx}")
        print(f"  Time: {hip_peak_time:.3f}s")
        print(f"  Lower Half KE: {hip_peak_ke:.1f} J")
    
    # ----------------------------------------
    # STEP 5: Calculate DURATIONS
    # ----------------------------------------
    load_duration = hip_peak_time - load_start_time
    launch_duration = abs(hip_peak_time)  # Time from hip peak to contact (0)
    
    results['load_duration_s'] = load_duration
    results['load_duration_ms'] = load_duration * 1000
    results['launch_duration_s'] = launch_duration
    results['launch_duration_ms'] = launch_duration * 1000
    
    if verbose:
        print(f"\n[DURATIONS]")
        print(f"  Load:   {load_duration:.3f}s ({load_duration*1000:.0f}ms)")
        print(f"  Launch: {launch_duration:.3f}s ({launch_duration*1000:.0f}ms)")
    
    # ----------------------------------------
    # STEP 6: Calculate TEMPO RATIO
    # ----------------------------------------
    if launch_duration > 0:
        tempo_ratio = load_duration / launch_duration
    else:
        tempo_ratio = 0
    
    results['tempo_ratio'] = round(tempo_ratio, 2)
    
    if verbose:
        print(f"\n[TEMPO RATIO]")
        print(f"  {load_duration:.3f}s / {launch_duration:.3f}s = {tempo_ratio:.2f}:1")
    
    # ----------------------------------------
    # STEP 7: Validate against expected ranges
    # ----------------------------------------
    validations = []
    
    if EXPECTED_TEMPO_RANGE[0] <= tempo_ratio <= EXPECTED_TEMPO_RANGE[1]:
        validations.append(("Tempo Ratio", tempo_ratio, "✓ OPTIMAL"))
    elif tempo_ratio < EXPECTED_TEMPO_RANGE[0]:
        validations.append(("Tempo Ratio", tempo_ratio, "⚠ FAST (rushing)"))
    else:
        validations.append(("Tempo Ratio", tempo_ratio, "⚠ SLOW (deliberate)"))
    
    if EXPECTED_LOAD_RANGE[0] <= load_duration <= EXPECTED_LOAD_RANGE[1]:
        validations.append(("Load Duration", f"{load_duration:.2f}s", "✓ NORMAL"))
    else:
        validations.append(("Load Duration", f"{load_duration:.2f}s", "⚠ CHECK"))
    
    if EXPECTED_LAUNCH_RANGE[0] <= launch_duration <= EXPECTED_LAUNCH_RANGE[1]:
        validations.append(("Launch Duration", f"{launch_duration:.2f}s", "✓ NORMAL"))
    else:
        validations.append(("Launch Duration", f"{launch_duration:.2f}s", "⚠ CHECK"))
    
    results['validations'] = validations
    
    if verbose:
        print(f"\n[VALIDATION]")
        for name, value, status in validations:
            print(f"  {name}: {value} {status}")
    
    return results


def analyze_kinematic_sequence(df, verbose=True):
    """
    Analyze the kinematic sequence (order of peak velocities).
    
    Proper sequence: Lower Half → Torso → Arms → Bat
    Each segment should peak and decelerate before the next.
    """
    
    if verbose:
        print("\n" + "=" * 70)
        print("KINEMATIC SEQUENCE")
        print("=" * 70)
    
    # Columns to check for peak timing
    segments = [
        ('lowerhalf_kinetic_energy', 'Lower Half'),
        ('lowertorso_kinetic_energy', 'Pelvis'),
        ('torso_kinetic_energy', 'Torso'),
        ('arms_kinetic_energy', 'Arms'),
    ]
    
    # Use swing phase only (-1.0s to +0.1s)
    swing = df[(df['time_from_max_hand'] >= -1.0) & (df['time_from_max_hand'] <= 0.1)]
    
    results = []
    for col, name in segments:
        if col in swing.columns:
            peak_idx = swing[col].idxmax()
            peak_time = swing.loc[peak_idx, 'time_from_max_hand']
            peak_val = swing.loc[peak_idx, col]
            results.append({
                'segment': name,
                'column': col,
                'peak_time': peak_time,
                'peak_value': peak_val,
                'ms_before_contact': abs(peak_time) * 1000
            })
    
    # Sort by peak time
    results.sort(key=lambda x: x['peak_time'])
    
    if verbose:
        print(f"\nPeak KE Timing (earliest to latest):")
        for i, r in enumerate(results, 1):
            print(f"  {i}. {r['segment']}: {r['peak_value']:.0f} J at t={r['peak_time']:.3f}s ({r['ms_before_contact']:.0f}ms before contact)")
        
        # Check if sequence is correct
        expected_order = ['Lower Half', 'Pelvis', 'Torso', 'Arms']
        actual_order = [r['segment'] for r in results]
        
        print(f"\n  Expected: {' → '.join(expected_order)}")
        print(f"  Actual:   {' → '.join(actual_order)}")
        
        if actual_order == expected_order:
            print("  Status: ✓ CORRECT SEQUENCE")
        else:
            print("  Status: ⚠ SEQUENCE ISSUE - Check kinetic chain")
    
    return results


def calculate_bat_speed(df, bat_mass_kg=0.85, verbose=True):
    """
    Calculate bat speed from kinetic energy or momentum.
    
    Method 1: From translational KE
      v = √(2 × KE / m)
    
    Method 2: From linear momentum magnitude
      v = |p| / m
    """
    
    if verbose:
        print("\n" + "=" * 70)
        print("BAT SPEED CALCULATION")
        print("=" * 70)
    
    results = {}
    
    # Method 1: From translational energy
    if 'bat_trans_energy' in df.columns:
        df['bat_speed_from_ke'] = np.sqrt(2 * df['bat_trans_energy'] / bat_mass_kg) * 2.237  # to mph
        
        # Filter to reasonable values and swing phase
        swing = df[(df['time_from_max_hand'] >= -0.5) & (df['time_from_max_hand'] <= 0.1)]
        valid = swing[swing['bat_speed_from_ke'].notna() & (swing['bat_speed_from_ke'] < 120)]
        
        if len(valid) > 0:
            peak_speed = valid['bat_speed_from_ke'].max()
            peak_idx = valid['bat_speed_from_ke'].idxmax()
            peak_time = valid.loc[peak_idx, 'time_from_max_hand']
            
            # Speed near contact
            near_contact = valid[abs(valid['time_from_max_hand']) < 0.1]
            if len(near_contact) > 0:
                contact_speed = near_contact.loc[near_contact['time_from_max_hand'].abs().idxmin(), 'bat_speed_from_ke']
            else:
                contact_speed = None
            
            results['peak_bat_speed_mph'] = round(peak_speed, 1)
            results['peak_bat_speed_time'] = round(peak_time, 3)
            results['contact_bat_speed_mph'] = round(contact_speed, 1) if contact_speed else None
            
            if verbose:
                print(f"\n  Method: √(2 × KE_trans / m) × 2.237")
                print(f"  Bat Mass: {bat_mass_kg} kg")
                print(f"\n  Peak Bat Speed: {peak_speed:.1f} mph at t={peak_time:.3f}s")
                if contact_speed:
                    print(f"  Speed at Contact: {contact_speed:.1f} mph")
    
    # Method 2: From momentum (if available)
    if all(c in df.columns for c in ['bat_linear_momentum_x', 'bat_linear_momentum_y', 'bat_linear_momentum_z']):
        df['bat_momentum_mag'] = np.sqrt(
            df['bat_linear_momentum_x']**2 + 
            df['bat_linear_momentum_y']**2 + 
            df['bat_linear_momentum_z']**2
        )
        df['bat_speed_from_p'] = (df['bat_momentum_mag'] / bat_mass_kg) * 2.237
        
        valid_p = df[df['bat_speed_from_p'].notna() & (df['bat_speed_from_p'] < 120)]
        if len(valid_p) > 0:
            peak_from_p = valid_p['bat_speed_from_p'].max()
            results['peak_bat_speed_from_momentum_mph'] = round(peak_from_p, 1)
            
            if verbose:
                print(f"\n  Cross-check from momentum: {peak_from_p:.1f} mph")
    
    return results


def generate_report(df, athlete_name="Athlete", verbose=True):
    """
    Generate complete tempo and biomechanics report.
    """
    
    print("\n")
    print("█" * 70)
    print(f"  BIOMECHANICS REPORT: {athlete_name.upper()}")
    print("█" * 70)
    
    # Run all analyses
    tempo_results = calculate_tempo(df, verbose=verbose)
    sequence_results = analyze_kinematic_sequence(df, verbose=verbose)
    bat_results = calculate_bat_speed(df, verbose=verbose)
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    print(f"""
┌────────────────────────────────────────────────────────────────────┐
│  {athlete_name.upper():<64} │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  TEMPO                                                             │
│    Ratio:         {tempo_results['tempo_ratio']:>6.2f}:1                                   │
│    Load:          {tempo_results['load_duration_ms']:>6.0f} ms                                   │
│    Launch:        {tempo_results['launch_duration_ms']:>6.0f} ms                                   │
│                                                                    │
│  BAT SPEED                                                         │
│    Peak:          {bat_results.get('peak_bat_speed_mph', 'N/A'):>6} mph                                   │
│    At Contact:    {bat_results.get('contact_bat_speed_mph', 'N/A'):>6} mph                                   │
│                                                                    │
│  KEY EVENTS                                                        │
│    Load Start:    {tempo_results['load_start_time']:>6.3f}s                                   │
│    Hip Peak:      {tempo_results['hip_peak_time']:>6.3f}s                                   │
│    Contact:       {tempo_results['contact_time']:>6.3f}s                                   │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
""")
    
    return {
        'tempo': tempo_results,
        'sequence': sequence_results,
        'bat_speed': bat_results
    }


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    print("\nLoading data...")
    
    try:
        df = pd.read_csv(CSV_PATH)
        print(f"✓ Loaded {len(df)} rows from {CSV_PATH.split('/')[-1]}")
        
        # Run full report
        results = generate_report(df, athlete_name="Connor Gray", verbose=True)
        
        # Ground truth comparison
        print("\n" + "=" * 70)
        print("GROUND TRUTH VALIDATION")
        print("=" * 70)
        print("""
Expected values for Connor Gray:
  Tempo Ratio:    3.38:1
  Load Duration:  1579 ms
  Launch Duration: 467 ms
  Bat Speed:      57.5 mph

If your values don't match, check:
  1. Window boundaries for load start detection
  2. Window boundaries for hip peak detection
  3. That you're using 'lowerhalf_kinetic_energy' column
  4. That time is relative to contact (time_from_max_hand)
""")
        
    except FileNotFoundError:
        print(f"✗ File not found: {CSV_PATH}")
        print("  Update CSV_PATH variable to point to your momentum-energy file")
    except Exception as e:
        print(f"✗ Error: {e}")
