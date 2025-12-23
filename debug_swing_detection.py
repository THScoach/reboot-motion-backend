#!/usr/bin/env python3
"""
Debug Swing Window Detection
Analyzes velocity data to understand why swing window detection is failing
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Don't need to import - just analyze the data

def analyze_swing_detection_debug():
    """Analyze the latest swing detection results"""
    
    print("\n" + "="*80)
    print("SWING WINDOW DETECTION DEBUG ANALYSIS")
    print("="*80)
    
    # Sample data from the analysis
    print("\n📊 ANALYSIS RESULTS:")
    print("-" * 80)
    print("Video: 131200-Hitting.mov")
    print("Duration: 19.17 seconds")
    print("FPS: 30")
    print("Frames: 575 total, 279 analyzed (48.5% detection)")
    
    print("\n⏱️ EVENT TIMING (ms):")
    print("-" * 80)
    print(f"Load Start:     1,866.7 ms   (1.87s)  - Frame ~56")
    print(f"Load Peak:     11,066.7 ms  (11.07s)  - Frame ~332")
    print(f"Launch:        16,266.7 ms  (16.27s)  - Frame ~488")
    print(f"Contact:       18,600.0 ms  (18.60s)  - Frame ~558")
    print(f"Follow-Through: 19,066.7 ms (19.07s)  - Frame ~572")
    
    print("\n⚠️ PROBLEMS IDENTIFIED:")
    print("-" * 80)
    print("1. CONTACT TOO LATE:")
    print(f"   Contact at 18.6s in a 19.17s video")
    print(f"   This is only 0.57s before the end!")
    print(f"   Real contact should be ~0.5-1.0s from start for visible swings")
    
    print("\n2. TEMPO RATIO BROKEN:")
    print(f"   Load Duration:  14,400 ms (11.07s - 1.87s)")
    print(f"   Swing Duration:  2,333 ms (18.60s - 16.27s)")
    print(f"   Tempo Ratio:     6.17 (14400 / 2333)")
    print(f"   Expected:        2.0-3.5")
    
    print("\n3. KINETIC SEQUENCE BROKEN:")
    print("-" * 80)
    print(f"   Pelvis Peak:   19,000 ms (19.00s) - LAST")
    print(f"   Torso Peak:    14,133 ms (14.13s) - BEFORE pelvis")
    print(f"   Shoulder Peak: 18,733 ms (18.73s) - LATE")
    print(f"   Hand Peak:     18,600 ms (18.60s) - LATE")
    print(f"   Bat Peak:      18,600 ms (18.60s) - LATE")
    print(f"\n   ❌ Torso peaks 4.87s BEFORE pelvis (should be 20-40ms AFTER)")
    
    print("\n4. BAT SPEED TOO LOW:")
    print("-" * 80)
    print(f"   Reported: 25.9 mph")
    print(f"   Expected: 55-70 mph for 16-year-old")
    print(f"   Difference: 30-44 mph too low")
    
    print("\n🔍 ROOT CAUSE ANALYSIS:")
    print("-" * 80)
    print("The issues suggest:")
    print("1. ❌ Swing window detection is NOT working")
    print("2. ❌ Searching entire 19s video instead of ~400-2000ms window")
    print("3. ❌ Finding random 'peaks' across entire video")
    print("4. ❌ Hand velocity too low (causing low bat speed)")
    
    print("\n💡 HYPOTHESIS:")
    print("-" * 80)
    print("Swing Window Detection is returning None or invalid window")
    print("Reasons could be:")
    print("  - Velocity threshold too high (not detecting movement)")
    print("  - Window too strict (rejecting valid swings)")
    print("  - Peak detection failing (no clear peak)")
    print("  - Scale factor wrong (velocities too low)")
    
    print("\n🔧 RECOMMENDED FIXES:")
    print("-" * 80)
    print("1. Add debug logging to detect_swing_window()")
    print("   - Log all velocity values")
    print("   - Log peak velocity and frame")
    print("   - Log window start/end")
    print("   - Log why window might be rejected")
    print("")
    print("2. Lower velocity thresholds")
    print("   - Current min_peak_velocity might be too high")
    print("   - Adjust for 30 FPS video (vs high-speed)")
    print("")
    print("3. Validate scale factor")
    print("   - Currently using player height (1.829m)")
    print("   - May need adjustment for normalized MediaPipe coords")
    print("")
    print("4. Add fallback swing window")
    print("   - If detection fails, use intelligent fallback")
    print("   - Search middle 20% of video")
    print("   - Or use first clear velocity spike")
    
    print("\n📋 NEXT STEPS:")
    print("-" * 80)
    print("A. Add extensive debug logging to event_detection.py")
    print("B. Re-run analysis to see actual velocity values")
    print("C. Adjust thresholds based on real data")
    print("D. Test with same video to validate fixes")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    analyze_swing_detection_debug()
