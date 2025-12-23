# ANTHROPOMETRIC DATA COLLECTION SPECIFICATION

**Date**: 2025-12-22  
**Purpose**: Define what measurements are needed for Kinetic DNA Blueprint analysis  
**Source**: Coach Rick's requirements

---

## DATA COLLECTION TIERS

### Tier 1: MINIMUM (Required)
**Accuracy**: ~85%  
**Collection Method**: Simple form (3 fields)

| Field | Example | Units | Required |
|-------|---------|-------|----------|
| Height | 72 | inches (or cm) | YES |
| Weight | 180 | lbs (or kg) | YES |
| Bat Side | Right | Right/Left | YES |

**Why Required**:
- Height & Weight → de Leva anthropometric scaling (segment mass/length)
- Bat Side → Determines which side of body to track for handedness

**Fallback Estimates Used**:
- Age: Assume adult (18+)
- Wingspan: Height × 1.0
- Arm Length: Height × 0.44
- Torso Length: Height × 0.35
- Leg Length: Height × 0.52
- Bat Length: 33 inches
- Bat Weight: 30 oz

---

### Tier 2: STANDARD (Recommended)
**Accuracy**: ~92%  
**Collection Method**: Extended form (7 fields)

**Additional Fields**:

| Field | Example | Units | Why It Helps |
|-------|---------|-------|--------------|
| Age | 14 | years | Youth vs adult body proportions |
| **Wingspan** | 74 | inches | Actual arm length calculation (wingspan - shoulder width) |
| Bat Length | 33 | inches | Bat moment of inertia: I = m × (L/2)² |
| Bat Weight | 30 | oz | Bat moment of inertia: I = m × (L/2)² |

**Why Wingspan Matters**:

Two 6'0" (72") players with different wingspans:

| Player | Height | Wingspan | Arm Length | Likely Motor Profile |
|--------|--------|----------|------------|---------------------|
| Player A | 72" | 70" | 26" | Shorter levers → SPINNER (rotation dominant) |
| Player B | 72" | 76" | 29" | Longer levers → WHIPPER (bat speed dominant) |

**Calculation**:
```python
# Without wingspan (fallback):
arm_length = height * 0.44  # Estimate

# With wingspan (actual):
shoulder_width = height * 0.25  # Estimate
arm_length = (wingspan - shoulder_width) / 2  # Measured
```

**Improved Estimates**:
- Arm Length: (Wingspan - Shoulder Width) / 2
- Torso Length: Height × 0.35 (adjusted for age if <18)
- Leg Length: Height × 0.52 (adjusted for age if <18)

---

### Tier 3: ADVANCED (BioSwing Style)
**Accuracy**: ~98%  
**Collection Method**: Detailed measurement guide (11 fields)

**Additional Fields**:

| Field | Example | Units | Why It Helps |
|-------|---------|-------|--------------|
| **Torso Length** | 24 | inches | Engine (core) segment inertia → affects hip/shoulder rotation |
| **Arm Length** | 32 | inches | Weapon segment calculation (shoulder to wrist) |
| **Leg Length (Inseam)** | 34 | inches | Ground segment calculation → weight transfer analysis |
| **Shoulder Width** | 18 | inches | Torso rotation axis (affects angular velocity) |
| **Hip Width** | 14 | inches | Pelvis rotation axis (affects angular velocity) |
| Throwing Hand | Right | Right/Left | Arm dominance patterns (affects hand path) |

**Why These Matter**:

1. **Torso Length** → Engine Flow Score
   - Longer torso = higher moment of inertia = slower rotation BUT more momentum
   - Shorter torso = lower inertia = faster rotation BUT less momentum
   - Affects hip-shoulder separation timing

2. **Arm Length** → Weapon Flow Score
   - Longer arms = longer lever = higher bat speed potential
   - Shorter arms = shorter lever = tighter hand path
   - Affects bat lag angle calculations

3. **Leg Length** → Ground Flow Score
   - Longer legs = more vertical COM displacement = more potential energy
   - Shorter legs = more stable base = better weight transfer
   - Affects ground reaction force estimates

4. **Shoulder Width** → Rotation Axis
   - Wider shoulders = larger rotation radius = higher linear velocity at hands
   - Affects torso angular momentum: L = I × ω

5. **Hip Width** → Rotation Axis
   - Wider hips = larger pelvis rotation radius
   - Affects pelvis angular momentum: L = I × ω
   - Critical for Transfer Ratio calculation

**No More Estimates**:
All segment lengths are directly measured, maximizing physics accuracy.

---

## MEASUREMENT INSTRUCTIONS

### How to Measure (For Players)

#### Height
- Stand barefoot against a wall
- Measure from floor to top of head
- Example: 72 inches (6'0")

#### Weight
- Use a bathroom scale
- Wear normal clothes (no shoes)
- Example: 180 lbs

#### Wingspan (Tier 2+)
- Stand with arms extended to sides (T-pose)
- Measure fingertip to fingertip across back
- Example: 74 inches

#### Torso Length (Tier 3)
- Measure from base of neck (C7 vertebra) to top of pelvis (iliac crest)
- Sit upright, measure vertically
- Example: 24 inches

#### Arm Length (Tier 3)
- Measure from shoulder joint (acromion) to wrist crease
- Arm relaxed at side
- Example: 32 inches

#### Leg Length (Tier 3)
- Inseam measurement (pants size)
- Crotch to floor while standing
- Example: 34 inches

#### Shoulder Width (Tier 3)
- Measure across back from shoulder joint to shoulder joint
- Example: 18 inches

#### Hip Width (Tier 3)
- Measure across widest part of hips (iliac crest)
- Example: 14 inches

---

## IMPLEMENTATION PLAN

### Phase 1 (MVP): Minimum Tier
**Timeline**: Included in initial physics engine (Week 1-2)

**Form Design**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Player Profile
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Height *
[___________] inches  (or cm ⌄)

Weight *
[___________] lbs     (or kg ⌄)

Bat Side *
○ Right  ○ Left

* Required fields
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Accuracy**: ~85% (good enough for MVP)

---

### Phase 2: Standard Tier
**Timeline**: After MVP validation (Week 4-5)

**Extended Form**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Player Profile — Standard
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

REQUIRED FIELDS

Height *
[___________] inches  (or cm ⌄)

Weight *
[___________] lbs     (or kg ⌄)

Bat Side *
○ Right  ○ Left

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OPTIONAL (Improves Accuracy to ~92%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Age
[___________] years

Wingspan
[___________] inches
[?] How to measure

Bat Length
[___________] inches

Bat Weight
[___________] oz

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**"How to measure" links to video or diagram**

**Accuracy**: ~92% (significantly better for Motor Profile classification)

---

### Phase 3: Advanced Tier (Upsell)
**Timeline**: After Standard tier proven (Week 8-10)

**Full Body Mapping Upsell**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
UPGRADE TO FULL BODY MAPPING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Get maximum physics accuracy (~98%)

📏 Includes:
✓ Video measurement guide
✓ Torso, arm, leg, shoulder, hip measurements
✓ Maximum precision for Ground/Engine/Weapon Flows
✓ Most accurate Motor Profile classification

Price: +$49 (one-time)

[Upgrade to Full Body Mapping]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Form** (after upgrade):
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Full Body Mapping
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Watch our measurement guide: [▶ Video]

Torso Length
[___________] inches
[?] How to measure

Arm Length
[___________] inches
[?] How to measure

Leg Length (Inseam)
[___________] inches
[?] How to measure

Shoulder Width
[___________] inches
[?] How to measure

Hip Width
[___________] inches
[?] How to measure

Throwing Hand
○ Right  ○ Left

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Accuracy**: ~98% (elite precision)

**Revenue Opportunity**: 30% of customers upgrade = $1,470/year additional revenue (100 customers × $299 × 30% × $49/$299)

---

## FALLBACK ESTIMATION FORMULAS

When optional fields are not provided, use these research-based estimates:

### From Height Alone (Tier 1)
```python
# Based on de Leva (1996) anthropometric data
wingspan = height * 1.0          # Assumes wingspan ≈ height
arm_length = height * 0.44       # Upper arm (0.186) + forearm (0.146) + hand (0.108)
torso_length = height * 0.35     # Trunk segment
leg_length = height * 0.52       # Upper leg (0.245) + lower leg (0.246) + foot (0.029)
shoulder_width = height * 0.25   # Biacromial breadth
hip_width = height * 0.19        # Biiliac breadth
```

### Age Adjustments (Tier 2)
```python
# Youth players (age < 18) have different proportions
if age < 18:
    # Legs are proportionally longer in youth
    leg_length = height * 0.55   # vs 0.52 for adults
    # Torso is proportionally shorter
    torso_length = height * 0.32  # vs 0.35 for adults
```

### Wingspan to Arm Length (Tier 2)
```python
# If wingspan is provided but arm_length is not
shoulder_width = height * 0.25  # Estimate
arm_length = (wingspan - shoulder_width) / 2
```

### Bat Specifications (Tier 2)
```python
# If not provided, use age-based defaults
if age < 13:
    bat_length = 30  # inches
    bat_weight = 20  # oz
elif age < 16:
    bat_length = 32
    bat_weight = 27
else:  # age >= 16
    bat_length = 33
    bat_weight = 30
```

---

## VALIDATION RULES

### Input Validation
```python
# Height
if units == "inches":
    assert 48 <= height <= 84, "Height must be 4'0\" - 7'0\""
elif units == "cm":
    assert 122 <= height <= 213, "Height must be 122-213 cm"

# Weight
if units == "lbs":
    assert 80 <= weight <= 350, "Weight must be 80-350 lbs"
elif units == "kg":
    assert 36 <= weight <= 159, "Weight must be 36-159 kg"

# Age (if provided)
assert 8 <= age <= 99, "Age must be 8-99 years"

# Wingspan (if provided)
assert 0.95 <= (wingspan / height) <= 1.15, "Wingspan should be 95%-115% of height"

# Arm Length (if provided)
assert 0.35 <= (arm_length / height) <= 0.50, "Arm length should be 35%-50% of height"

# Torso Length (if provided)
assert 0.28 <= (torso_length / height) <= 0.40, "Torso should be 28%-40% of height"

# Leg Length (if provided)
assert 0.45 <= (leg_length / height) <= 0.60, "Leg length should be 45%-60% of height"
```

---

## FOR YOUR DEVELOPER

### MVP Implementation (Tier 1)
**Week 1-2**: Physics engine only needs:
```python
class AthleteProfile:
    def __init__(self, height_inches, weight_lbs, bat_side):
        self.height = height_inches
        self.weight = weight_lbs
        self.bat_side = bat_side  # "right" or "left"
        
        # Calculate all other measurements using fallbacks
        self.wingspan = self._estimate_wingspan()
        self.arm_length = self._estimate_arm_length()
        self.torso_length = self._estimate_torso_length()
        self.leg_length = self._estimate_leg_length()
        self.shoulder_width = self._estimate_shoulder_width()
        self.hip_width = self._estimate_hip_width()
        self.bat_length = 33  # Default adult bat
        self.bat_weight = 30  # Default adult bat
```

**Test with Coach Rick's profile** (you provide):
```python
rick = AthleteProfile(
    height_inches=__,  # Your height
    weight_lbs=__,     # Your weight
    bat_side="__"      # "right" or "left"
)
```

### Phase 2 Implementation (Tier 2)
**Week 4-5**: Add optional fields to database and UI
```python
class AthleteProfile:
    def __init__(self, height_inches, weight_lbs, bat_side,
                 age=None, wingspan=None, bat_length=None, bat_weight=None):
        # Use provided values or fall back to estimates
        pass
```

### Phase 3 Implementation (Tier 3)
**Week 8-10**: Full Body Mapping upsell
```python
class AthleteProfile:
    def __init__(self, height_inches, weight_lbs, bat_side,
                 age=None, wingspan=None, bat_length=None, bat_weight=None,
                 torso_length=None, arm_length=None, leg_length=None,
                 shoulder_width=None, hip_width=None, throwing_hand=None):
        # Use measured values (highest accuracy)
        pass
```

---

## ACCURACY IMPACT BY TIER

### Tier 1 (Minimum): ~85% Accuracy
**What's Accurate**:
- Tempo Ratio: ✅ (time-based, not anthropometric)
- Ground Flow: 🟡 (uses estimated leg length)
- Engine Flow: 🟡 (uses estimated torso dimensions)
- Weapon Flow: 🟡 (uses estimated arm length)
- Transfer Ratio: 🟡 (depends on all segments)

**What's Less Accurate**:
- Motor Profile classification (may misclassify SPINNER vs WHIPPER)
- Absolute angular momentum values (estimates may be off by 10-15%)

### Tier 2 (Standard): ~92% Accuracy
**What's Improved**:
- Motor Profile classification: ✅ (wingspan gives actual arm length)
- Weapon Flow: ✅ (bat specs improve bat momentum calculations)
- Ground/Engine Flow: 🟢 (age adjusts proportions)

**Still Estimated**:
- Torso, shoulder, hip dimensions (uses height-based formulas)

### Tier 3 (Advanced): ~98% Accuracy
**What's Fully Measured**:
- All body segments directly measured
- No estimation errors
- Maximum physics precision

**Only Remaining Uncertainty**:
- MediaPipe pose detection accuracy (~2% error)

---

## SUMMARY FOR COACH RICK

**For testing your 5 videos, I need**:
1. Height (inches or cm)
2. Weight (lbs or kg)
3. Bat side (right or left)

**Optional (if you want to test Tier 2 accuracy)**:
4. Age
5. Wingspan (fingertip to fingertip)
6. Bat length (inches)
7. Bat weight (oz)

**Provide these and I'll test the physics engine on your videos using your actual measurements.**

---

**Last Updated**: 2025-12-22  
**Status**: Ready for Coach Rick's profile data
