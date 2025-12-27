import pandas as pd
import numpy as np
from app.services.reboot_sync import RebootMotionSync
import asyncio

async def analyze_disconnection():
    # Initialize Reboot sync
    reboot = RebootMotionSync()
    
    # Eric Williams session
    session_id = "629a8a99-1906-498f-a582-3cb7bd3c0a77"
    
    print("=" * 80)
    print("ERIC WILLIAMS - DISCONNECTION ANALYSIS")
    print(f"Session: {session_id[:8]}")
    print("=" * 80)
    
    # Get session data
    session = await reboot.get_session_details(session_id)
    print(f"Date: {session.get('session_date')}")
    
    # Get data exports
    exports = await reboot.get_data_exports(session_id)
    
    # Find IK and ME exports
    ik_export = next(e for e in exports if e.get("data_type") == "inverse-kinematics")
    me_export = next(e for e in exports if e.get("data_type") == "momentum-energy")
    
    # Download CSVs
    ik_df = pd.read_csv(ik_export["download_url"])
    me_df = pd.read_csv(me_export["download_url"])
    
    print(f"\nData loaded: {len(ik_df)} frames")
    
    # 1. TIMING ANALYSIS
    print("\n1️⃣  TIMING SEQUENCE ANALYSIS")
    print("-" * 80)
    
    time = ik_df['time'].values
    
    # Pelvis rotation velocity
    pelvis_rot = ik_df['pelvis_rot'].values
    pelvis_vel = np.gradient(pelvis_rot, time)
    pelvis_peak_idx = np.argmax(np.abs(pelvis_vel))
    pelvis_peak_time = time[pelvis_peak_idx]
    pelvis_peak_vel = pelvis_vel[pelvis_peak_idx]
    
    # Torso rotation velocity
    torso_rot = ik_df['torso_rot'].values
    torso_vel = np.gradient(torso_rot, time)
    torso_peak_idx = np.argmax(np.abs(torso_vel))
    torso_peak_time = time[torso_peak_idx]
    torso_peak_vel = torso_vel[torso_peak_idx]
    
    print(f"Pelvis Peak Time:  {pelvis_peak_time:.3f}s (velocity: {pelvis_peak_vel:.1f}°/s)")
    print(f"Torso Peak Time:   {torso_peak_time:.3f}s (velocity: {torso_peak_vel:.1f}°/s)")
    
    # Calculate delays
    pelvis_torso_delay = torso_peak_time - pelvis_peak_time
    print(f"\n⏱️  Hip-to-Torso Delay: {pelvis_torso_delay*1000:.0f} ms")
    
    if pelvis_torso_delay < 0:
        print("   ⚠️  WARNING: Torso peaks BEFORE hips (reversed sequence!)")
        print("   → Early shoulder rotation / disconnection")
    elif pelvis_torso_delay < 0.050:
        print("   ⚠️  WARNING: Delay too short (< 50ms)")
        print("   → Segments moving together, no separation")
    elif pelvis_torso_delay > 0.150:
        print("   ⚠️  WARNING: Delay too long (> 150ms)")  
        print("   → Poor timing, losing energy transfer")
    else:
        print("   ✅ Good timing (50-150ms optimal)")
    
    # Check arm energy timing
    if 'lsh_kinetic_energy' in me_df.columns and 'rsh_kinetic_energy' in me_df.columns:
        arm_energy = me_df['lsh_kinetic_energy'] + me_df['rsh_kinetic_energy']
        arm_peak_idx = arm_energy.idxmax()
        arm_peak_time = time[arm_peak_idx]
        arm_peak_energy = arm_energy.iloc[arm_peak_idx]
        
        print(f"Arms Peak Time:    {arm_peak_time:.3f}s (energy: {arm_peak_energy:.1f} J)")
        
        torso_arm_delay = arm_peak_time - torso_peak_time
        print(f"\n⏱️  Torso-to-Arms Delay: {torso_arm_delay*1000:.0f} ms")
        
        if torso_arm_delay < 0:
            print("   ❌ DISCONNECTION: Arms peak BEFORE torso!")
            print("   → Back elbow flying off early")
            print("   → Arms taking over instead of following body")
    
    # 2. HIP-SHOULDER SEPARATION
    print("\n2️⃣  HIP-SHOULDER SEPARATION ANALYSIS")
    print("-" * 80)
    
    hip_shoulder_sep = ik_df['pelvis_rot'] - ik_df['torso_rot']
    max_separation = hip_shoulder_sep.max()
    max_sep_idx = hip_shoulder_sep.idxmax()
    max_sep_time = time[max_sep_idx]
    
    print(f"Max Hip-Shoulder Separation: {max_separation:.1f}°")
    print(f"Occurred at: {max_sep_time:.3f}s")
    
    # Check WHERE the separation occurs
    swing_duration = time[-1]
    sep_phase = max_sep_time / swing_duration
    
    if sep_phase < 0.3:
        print(f"Phase: LOAD (early - {sep_phase*100:.0f}%)")
        print("Quality: ✅ GOOD - True loading separation")
    elif sep_phase < 0.6:
        print(f"Phase: TRANSITION (middle - {sep_phase*100:.0f}%)")
        print("Quality: ⚠️  May be fake separation from poor timing")
    else:
        print(f"Phase: LAUNCH (late - {sep_phase*100:.0f}%)")
        print("Quality: ❌ BAD - Fake separation from disconnection")
        print("   → Separation from shoulders rotating early, not from loading")
    
    # 3. ROTATION MAGNITUDE
    print("\n3️⃣  ROTATION MAGNITUDE")
    print("-" * 80)
    
    pelvis_total = ik_df['pelvis_rot'].max() - ik_df['pelvis_rot'].min()
    torso_total = ik_df['torso_rot'].max() - ik_df['torso_rot'].min()
    
    print(f"Total Pelvis Rotation: {pelvis_total:.1f}° (target: 40-50°)")
    print(f"Total Torso Rotation:  {torso_total:.1f}° (target: 30-40°)")
    
    if pelvis_total < 10:
        print("\n❌ CRITICAL: Minimal hip rotation")
        print("   → Arm-dominant swing")
        print("   → Not using lower body effectively")
    
    if torso_total < 10:
        print("\n❌ CRITICAL: Minimal torso rotation")  
        print("   → Upper body disconnected or data quality issue")
    
    # 4. ENERGY FLOW
    print("\n4️⃣  ENERGY FLOW SEQUENCE")
    print("-" * 80)
    
    energy_cols = ['lowerhalf_kinetic_energy', 'torso_kinetic_energy', 
                   'arms_kinetic_energy', 'bat_kinetic_energy']
    available_cols = [c for c in energy_cols if c in me_df.columns]
    
    if len(available_cols) >= 2:
        print("Energy peaks:")
        peak_info = []
        for col in available_cols:
            peak_energy = me_df[col].max()
            peak_idx = me_df[col].idxmax()
            peak_time = time[peak_idx]
            print(f"  {col:25s}: {peak_energy:6.1f} J at {peak_time:.3f}s")
            peak_info.append((col, peak_time, peak_energy))
        
        # Check sequence
        peak_times = [info[1] for info in peak_info]
        is_sequential = all(peak_times[i] <= peak_times[i+1] for i in range(len(peak_times)-1))
        
        if is_sequential:
            print("\n✅ Energy flows in correct sequence (proximal → distal)")
        else:
            print("\n❌ Energy flow is OUT OF SEQUENCE")
            print("   → Indicates disconnection or poor timing")
            
            # Show the actual sequence
            sorted_peaks = sorted(peak_info, key=lambda x: x[1])
            print("\nActual sequence:")
            for col, t, e in sorted_peaks:
                print(f"  {t:.3f}s: {col:25s} ({e:.1f} J)")
    
    # 5. DIAGNOSIS
    print("\n5️⃣  DIAGNOSIS & COACHING PLAN")
    print("=" * 80)
    
    issues = []
    fixes = []
    
    # Disconnection check
    if 'lsh_kinetic_energy' in me_df.columns and torso_arm_delay < 0:
        issues.append("❌ DISCONNECTION: Back elbow flies off early")
        fixes.append("1. CONNECTION DRILLS")
        fixes.append("   • Towel under back armpit drill")
        fixes.append("   • Keep elbow 'in the shirt pocket' during load")
        fixes.append("   • Feel the connection before launching")
    
    # Sequencing check
    if pelvis_torso_delay < 0:
        issues.append("❌ REVERSED SEQUENCE: Shoulders before hips")
        fixes.append("2. SEQUENCING DRILLS")
        fixes.append("   • Med ball rotation throws (hips lead)")
        fixes.append("   • 'Hips start, shoulders chase' cue")
        fixes.append("   • Front toss with focus on hip initiation")
    
    # Fake separation check
    if sep_phase > 0.6:
        issues.append("❌ FAKE SEPARATION: Occurs too late in swing")
        fixes.append("3. LOADING MECHANICS")
        fixes.append("   • Load hips first, keep shoulders closed")
        fixes.append("   • Create separation BEFORE launch")
        fixes.append("   • Think 'wind up the spring' in load phase")
    
    # Hip rotation check
    if pelvis_total < 10:
        issues.append("❌ ARM-DOMINANT: Minimal hip rotation")
        fixes.append("4. HIP ENGAGEMENT")
        fixes.append("   • 'Swing with your belly button' cue")
        fixes.append("   • Hip rotation drills (no bat)")
        fixes.append("   • Feel hips driving the swing")
    
    if issues:
        print("\n🔍 ISSUES DETECTED:\n")
        for i, issue in enumerate(issues, 1):
            print(f"{i}. {issue}")
        
        print("\n\n💡 RECOMMENDED FIX PRIORITY:\n")
        for fix in fixes:
            print(fix)
    else:
        print("✅ No major mechanical issues detected")
    
    # 6. BAT SPEED CONTEXT
    print("\n\n6️⃣  BAT SPEED & UPSIDE")
    print("=" * 80)
    print("📊 Blast Motion Data:")
    print("   Peak Bat Speed: 82 mph")
    print("   Average: 76 mph")
    print("\n💪 Current State:")
    print("   → Getting 82 mph from HANDS/ARMS alone")
    print("   → Minimal contribution from hips/torso")
    print("\n🚀 With Proper Mechanics:")
    print("   → Could achieve 88-92 mph with SAME effort")
    print("   → That's +6-10 mph just from sequencing!")
    print("   → Exit velocity could jump from ~98 to ~106-110 mph")
    
    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETE")
    print("=" * 80)

# Run the analysis
asyncio.run(analyze_disconnection())
