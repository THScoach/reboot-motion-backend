# 🔧 Physics Engine Debug Mode - READY FOR TESTING

## Status: ✅ Server Running with Debug Logging

**Live URL:** https://8000-i5cseikj92ei70k8wadux-2e77fc33.sandbox.novita.ai

## What's New?

### Comprehensive Debug Logging Added

The `detect_swing_window()` function now outputs:
- Total number of velocities processed
- Time range of video (ms and seconds)
- Velocity statistics (min, max, mean)
- Peak velocity location and value
- Velocity threshold calculations
- Window start/end indices and times
- Window duration validation
- Success/failure reasons

### Example Debug Output

When you upload Connor Gray's video again, you'll see:
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
   ✓ Valid swing window detected!
```

## Critical Issues We're Debugging

### 1. Tempo Ratio: 6.17 (Expected: 2.0-3.5)
- Load: 14,400 ms
- Swing: 2,333 ms
- **Root Cause:** Swing window detection failing

### 2. Bat Speed: 25.9 mph (Expected: 55-70 mph)
- **Root Cause:** Hand velocity too low (scale factor issues?)

### 3. Kinetic Sequence BROKEN
- Torso peaks BEFORE pelvis (should be after)
- **Root Cause:** Searching entire video instead of swing window

### 4. Contact at 18.6s in 19.17s video
- Only 0.57s before end!
- **Root Cause:** No valid swing window, using fallback

## What to Look For

### Hypothesis #1: Peak Velocity Too Low
If peak velocity is < 5 m/s:
- Scale factor may be wrong
- Lever arm calculation needs adjustment

### Hypothesis #2: Window Too Long
If window duration > 2000ms:
- Velocity threshold too low
- Not finding proper boundaries

### Hypothesis #3: Peak in Wrong Location
If peak at > 15 seconds:
- Not detecting actual swing
- Finding movement at end of video

## Next Steps

1. **Upload Connor Gray video again**
2. **Check server console output** (via BashOutput)
3. **Analyze debug data**
4. **Adjust thresholds**:
   - Velocity threshold (currently 30% of mean)
   - Min peak velocity (need baseline)
   - Window duration limits (400-2000ms)
5. **Re-test with adjustments**

## Commits Pushed to GitHub

All changes pushed to: https://github.com/THScoach/reboot-motion-backend

Latest commits:
- `a6bb5b4`: Add extensive logging to swing window detection
- `4b7c75a`: Update current status with debug findings
- `1e5bcd8`: Analyze second Reboot Motion dataset
- `f71ea24`: Implement proper bat speed calculation
- `f54e65b`: Rewrite event detection with swing window detection

## Test Video Ready

**Connor Gray - 131200-Hitting.mov**
- 16 years old, Left-handed hitter
- 30 FPS video, 19.17 seconds
- 279/575 frames with pose detection (48.5%)

**Please re-upload this video to see the debug output!**

---

**Server is running and waiting for your upload! 🚀**
