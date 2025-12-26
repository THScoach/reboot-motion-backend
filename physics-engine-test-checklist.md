# PHYSICS ENGINE — QUICK TEST CHECKLIST

Print this. Check each box as you test.

---

## VIDEO 1: Shohei Ohtani (340109.mp4) — 300 FPS

**Expected:** Elite pro, scores 80+, Whipper or Slingshotter

### Event Detection
| Check | Expected | Actual | Pass? |
|-------|----------|--------|-------|
| First Movement | > 0 ms | _____ ms | ☐ |
| Foot Plant | 200-400ms after first move | _____ ms | ☐ |
| Contact | 100-200ms after foot plant | _____ ms | ☐ |
| Load Duration | 200-600 ms | _____ ms | ☐ |
| Launch Duration | 100-250 ms | _____ ms | ☐ |

### Scores
| Metric | Expected | Actual | Pass? |
|--------|----------|--------|-------|
| Tempo Ratio | 2.0 - 3.5 | _____ | ☐ |
| Ground Score | 75 - 95 | _____ | ☐ |
| Engine Score | 75 - 95 | _____ | ☐ |
| Weapon Score | 80 - 95 | _____ | ☐ |
| Transfer Ratio | 75 - 95% | _____ | ☐ |
| Bat Speed | 70 - 85 mph | _____ mph | ☐ |

### Classification
| Check | Expected | Actual | Pass? |
|-------|----------|--------|-------|
| Motor Profile | Whipper or Slingshotter | _________ | ☐ |
| Uses correct names? | Spinner/Slingshotter/Whipper/Titan | Yes / No | ☐ |
| Confidence % shown? | 60-95% | _____ % | ☐ |

### Kinetic Sequence (order should be Pelvis → Torso → Arms → Bat)
| Segment | Peak Time | Order Correct? |
|---------|-----------|----------------|
| Pelvis | _____ ms | ☐ |
| Torso | _____ ms | ☐ |
| Arms | _____ ms | ☐ |
| Bat | _____ ms | ☐ |

---

## VIDEO 2: Your Swing — 30 FPS

**Expected:** Good amateur, scores 50-80, Weapon capped at 85

### Event Detection
| Check | Expected | Actual | Pass? |
|-------|----------|--------|-------|
| First Movement | > 0 ms | _____ ms | ☐ |
| Foot Plant | 200-400ms after first move | _____ ms | ☐ |
| Contact | 100-200ms after foot plant | _____ ms | ☐ |
| Load Duration | 200-600 ms | _____ ms | ☐ |
| Launch Duration | 100-250 ms | _____ ms | ☐ |

### Scores
| Metric | Expected | Actual | Pass? |
|--------|----------|--------|-------|
| Tempo Ratio | 1.8 - 4.0 | _____ | ☐ |
| Ground Score | 50 - 85 | _____ | ☐ |
| Engine Score | 50 - 85 | _____ | ☐ |
| Weapon Score | 45 - 85 (capped) | _____ | ☐ |
| Transfer Ratio | 55 - 85% | _____ | ☐ |
| Bat Speed | 45 - 75 mph | _____ mph | ☐ |

### Classification
| Check | Expected | Actual | Pass? |
|-------|----------|--------|-------|
| Motor Profile | Any valid profile | _________ | ☐ |
| Uses correct names? | Spinner/Slingshotter/Whipper/Titan | Yes / No | ☐ |
| Confidence % shown? | 60-95% | _____ % | ☐ |

---

## COMPARISON CHECK

| Metric | Shohei | You | Shohei > You? |
|--------|--------|-----|---------------|
| Ground | _____ | _____ | ☐ Yes ☐ No |
| Engine | _____ | _____ | ☐ Yes ☐ No |
| Weapon | _____ | _____ | ☐ Yes ☐ No |
| Bat Speed | _____ | _____ | ☐ Yes ☐ No |
| Transfer | _____ | _____ | ☐ Yes ☐ No |

**Shohei should score higher on most metrics.** If you score higher than an MLB player, something's wrong.

---

## CONSISTENCY CHECK

Upload the same Shohei video 3 times:

| Run | Tempo | Ground | Engine | Weapon | Same? |
|-----|-------|--------|--------|--------|-------|
| 1 | _____ | _____ | _____ | _____ | — |
| 2 | _____ | _____ | _____ | _____ | ☐ |
| 3 | _____ | _____ | _____ | _____ | ☐ |

**All three runs should be identical.**

---

## RED FLAGS — STOP IF YOU SEE THESE

| Red Flag | What It Means |
|----------|---------------|
| ☐ Tempo < 1.0 | Events detected wrong |
| ☐ Tempo > 5.0 | Contact in follow-through |
| ☐ Any score = 0 | Calculation not running |
| ☐ Any score = 100 | Hardcoded / no ceiling |
| ☐ Any score = exactly 50 | Default placeholder |
| ☐ Bat speed > 100 mph | Impossible, calculation error |
| ☐ Bat speed < 30 mph | Tracking lost |
| ☐ Motor Profile = "Rotational/Linear/Hybrid" | Wrong terminology |
| ☐ Your scores > Shohei's scores | Calibration broken |
| ☐ Results change on same video | Non-deterministic bug |

---

## FINAL VERDICT

**Count your checks:**

- Event Detection: ___/5 passed
- Shohei Scores: ___/6 passed  
- Your Scores: ___/6 passed
- Classification: ___/3 passed
- Comparison: ___/5 Shohei higher
- Consistency: ___/3 identical
- Red Flags: ___/0 (should be ZERO)

**Pass Threshold:** All sections pass, zero red flags

---

## RESULT

☐ **PASS** — Ready for Lab Report integration

☐ **FAIL** — Send issues to developer:

```
Issues found:
1. ________________________________
2. ________________________________
3. ________________________________

Expected: ____________
Actual: ______________
Video: _______________
```
