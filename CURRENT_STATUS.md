# Current Status - Physics Engine Debugging

## Date: December 22, 2025

## Issues Found

### Connor Gray Video Analysis (16yo, LHH, 30 FPS video)

**Critical Issues:**
1. **Tempo Ratio: 6.17** (Expected: 2.0-3.5)
   - Load Duration: 14,400 ms (14.4 seconds!)
   - Swing Duration: 2,333 ms (2.3 seconds)
   
2. **Bat Speed: 25.9 mph** (Expected: 55-70 mph for 16yo)

3. **Kinetic Sequence BROKEN:**
   - Pelvis Peak: 19,000 ms (19.0s) - LAST
   - Torso Peak: 14,133 ms (14.1s) - BEFORE pelvis (❌)
   - Shoulder/Hand/Bat: 18,600 ms (18.6s) - Too late
   - Torso peaks 4.87s BEFORE pelvis (should be 20-40ms AFTER)

4. **Contact Time: 18.6s in 19.17s video**
   - Contact is only 0.57s before end
   - Should be around 0.5-1.0s from start for visible swings

## Root Cause

**Swing Window Detection is NOT working!**

The system is:
- Searching entire 19-second video
- Finding random peaks throughout video
- Not restricting search to actual swing window (400-2000ms)

## Debug Steps Taken

1. ✅ Added extensive debug logging to `detect_swing_window()`
2. ✅ Committed changes (`a6bb5b4`)
3. 🔄 Attempting to restart server to see debug output
4. ⚠️  Port 8000 conflicts preventing clean restart

## What We Need

**From next video upload, we should see:**
```
🔍 SWING WINDOW DETECTION (debug mode)
   Total velocities: 279
   Time range: 0ms to 19167ms (19.17s)
   Velocity stats: min=X m/s, max=Y m/s, mean=Z m/s
   ✓ Peak velocity: A m/s at index B, time Cms (Cs)
   Velocity threshold: D m/s (30% of mean)
   Window start: index E, time Fms
   Window end: index G, time Hms
   Window duration: Ims
   Validation: min=400ms, max=2000ms
   [PASS or FAIL message]
```

## Expected Findings

We expect to discover:
1. **Peak velocity is too low** - causing bat speed issues
2. **Window duration is too long** - causing tempo issues  
3. **Velocity threshold is wrong** - not finding proper window boundaries
4. **Scale factor issues** - MediaPipe coords not converting properly to m/s

## Completed Fixes

✅ Event Detection Rewrite (swing window first)
✅ Bat Speed Calculator (lever arm physics)
✅ Contact Detection (peak bat angular velocity)
✅ Tempo Ratio Calculation
✅ Reboot Data Analysis (2 CSV files)

## Pending Fixes

🔄 Debug and fix swing window detection (IN PROGRESS)
⏳ Fix kinetic sequence tracking
⏳ Remove hardcoded Ground/Engine scores
⏳ Test with Shohei Ohtani videos
⏳ Create pull request for all fixes

## Next Actions

1. Get server running with debug mode
2. Re-upload Connor Gray video
3. Analyze debug output
4. Fix thresholds/scale factors
5. Validate with fresh analysis
