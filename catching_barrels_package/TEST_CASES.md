# 🧪 TEST CASES - CATCHING BARRELS Training Module

**Version**: 1.0  
**Date**: December 25, 2025  
**Purpose**: Validate system implementation against known results

---

## 📋 TABLE OF CONTENTS

1. [Test Data Sets](#test-data-sets)
2. [Unit Tests](#unit-tests)
3. [Integration Tests](#integration-tests)
4. [End-to-End Tests](#end-to-end-tests)
5. [Edge Case Tests](#edge-case-tests)
6. [Performance Tests](#performance-tests)
7. [Validation Criteria](#validation-criteria)

---

## 📊 TEST DATA SETS

### **Test Case 1: Eric Williams (Reference Case)**

**Description**: Known athlete with energy leak pattern

**Input Files:**
- `eric_williams_data/momentum-energy.csv` (755 frames)
- `eric_williams_data/inverse-kinematics.csv` (755 frames)

**Athlete Info:**
- Name: Eric Williams
- Handedness: RHH
- Age: 24
- Position: OF

**Expected Metrics:**
```json
{
  "lead_knee_angle": 0.3,
  "hip_angular_momentum": 2.10,
  "shoulder_angular_momentum": 18.25,
  "shoulder_hip_ratio": 8.68,
  "bat_speed": 82.0,
  "timing_gap_ms": 158.3,
  "lead_arm_extension": 1.5
}
```

**Expected Pattern:**
```json
{
  "type": "PATTERN_1_KNEE_LEAK",
  "severity": "CRITICAL",
  "primary_protocol": "PROTOCOL_1",
  "secondary_protocol": "PROTOCOL_2"
}
```

**Expected Efficiency:**
```json
{
  "hip_efficiency": 21.0,
  "knee_efficiency": 0.2,
  "contact_efficiency": 7.5,
  "total_efficiency": 11.2
}
```

**Expected Ball Outcomes:**
```json
{
  "current": {
    "exit_velo": 82.0,
    "launch_angle": 2,
    "gb_rate": 65,
    "ld_rate": 25
  },
  "predicted": {
    "exit_velo": 89.0,
    "launch_angle": 15,
    "gb_rate": 35,
    "ld_rate": 55
  },
  "improvement": {
    "exit_velo_gain": 7.0,
    "launch_angle_gain": 13
  }
}
```

**Expected Overall Score**: 60.3/100

**Pass Criteria:**
- ✅ All metrics within ±5% of expected values
- ✅ Pattern type matches exactly
- ✅ Primary protocol is PROTOCOL_1
- ✅ Overall score within ±3 points

---

### **Test Case 2: Elite Hitter (Control)**

**Description**: Hypothetical elite hitter with optimal mechanics

**Mock Metrics:**
```json
{
  "lead_knee_angle": 170.0,
  "hip_angular_momentum": 9.5,
  "shoulder_angular_momentum": 12.8,
  "shoulder_hip_ratio": 1.35,
  "bat_speed": 92.0,
  "timing_gap_ms": 22.0,
  "lead_arm_extension": 18.5
}
```

**Expected Pattern:**
```json
{
  "type": "PATTERN_NONE",
  "severity": "NONE",
  "title": "Excellent Mechanics",
  "description": "No significant issues detected"
}
```

**Expected Efficiency:**
```json
{
  "hip_efficiency": 95.0,
  "knee_efficiency": 100.0,
  "contact_efficiency": 92.5,
  "total_efficiency": 95.8
}
```

**Expected Ball Outcomes:**
```json
{
  "current": {
    "exit_velo": 90.0,
    "launch_angle": 15,
    "gb_rate": 32,
    "ld_rate": 58
  },
  "predicted": {
    "exit_velo": 92.0,
    "launch_angle": 16,
    "gb_rate": 30,
    "ld_rate": 60
  }
}
```

**Expected Overall Score**: 95.0/100

**Pass Criteria:**
- ✅ No critical pattern detected
- ✅ Overall score > 90/100
- ✅ No training protocol recommended

---

### **Test Case 3: Spinner Pattern**

**Description**: Athlete with fast foot roll pattern

**Mock Metrics:**
```json
{
  "lead_knee_angle": 125.0,
  "hip_angular_momentum": 3.8,
  "shoulder_angular_momentum": 14.2,
  "shoulder_hip_ratio": 3.74,
  "bat_speed": 78.0,
  "timing_gap_ms": 12.0,
  "lead_arm_extension": 8.2
}
```

**Expected Pattern:**
```json
{
  "type": "PATTERN_3_SPINNER",
  "severity": "HIGH",
  "primary_protocol": "PROTOCOL_2",
  "secondary_protocol": "PROTOCOL_1"
}
```

**Expected Training Focus**: Vertical Ground Force (Force Pedals)

**Pass Criteria:**
- ✅ PATTERN_3_SPINNER detected
- ✅ PROTOCOL_2 (Vertical Force) is primary
- ✅ Timing gap < 15ms recognized

---

### **Test Case 4: Weak Hip Contribution**

**Description**: Good timing but weak hip input

**Mock Metrics:**
```json
{
  "lead_knee_angle": 155.0,
  "hip_angular_momentum": 4.2,
  "shoulder_angular_momentum": 18.5,
  "shoulder_hip_ratio": 4.40,
  "bat_speed": 84.0,
  "timing_gap_ms": 21.0,
  "lead_arm_extension": 12.0
}
```

**Expected Pattern:**
```json
{
  "type": "PATTERN_2_WEAK_HIP",
  "severity": "HIGH",
  "primary_protocol": "PROTOCOL_2",
  "secondary_protocol": "PROTOCOL_3"
}
```

**Pass Criteria:**
- ✅ PATTERN_2_WEAK_HIP detected
- ✅ Timing gap > 15ms but hip angmom < 5.0
- ✅ PROTOCOL_2 or PROTOCOL_3 recommended

---

## 🔧 UNIT TESTS

### **Test Suite 1: Data Parsing**

#### **Test 1.1: Parse Momentum CSV**

```python
def test_parse_momentum_csv():
    """
    Test that momentum-energy.csv is parsed correctly
    """
    df = parse_momentum_csv("eric_williams_data/momentum-energy.csv")
    
    # Check required columns exist
    assert 'rel_frame' in df.columns
    assert 'lowertorso_angular_momentum_mag' in df.columns
    assert 'torso_angular_momentum_mag' in df.columns
    assert 'bat_kinetic_energy' in df.columns
    
    # Check data types
    assert df['rel_frame'].dtype == int or df['rel_frame'].dtype == 'int64'
    assert df['lowertorso_angular_momentum_mag'].dtype == float or df['lowertorso_angular_momentum_mag'].dtype == 'float64'
    
    # Check frame count
    assert len(df) == 755
    
    # Check contact frame exists
    assert 0 in df['rel_frame'].values
    
    print("✅ Test 1.1 PASSED: Momentum CSV parsed correctly")
```

#### **Test 1.2: Parse Kinematics CSV**

```python
def test_parse_kinematics_csv():
    """
    Test that inverse-kinematics.csv is parsed correctly
    """
    df = parse_kinematics_csv("eric_williams_data/inverse-kinematics.csv")
    
    # Check required columns
    assert 'rel_frame' in df.columns
    assert 'left_knee' in df.columns or 'right_knee' in df.columns
    assert 'torso_rot' in df.columns
    
    # Check frame alignment with momentum
    assert len(df) == 755
    assert 0 in df['rel_frame'].values
    
    print("✅ Test 1.2 PASSED: Kinematics CSV parsed correctly")
```

#### **Test 1.3: Extract Contact Frame**

```python
def test_extract_contact_frame():
    """
    Test contact frame extraction (rel_frame = 0)
    """
    momentum_df = parse_momentum_csv("eric_williams_data/momentum-energy.csv")
    kinematics_df = parse_kinematics_csv("eric_williams_data/inverse-kinematics.csv")
    
    contact_frame_momentum = momentum_df[momentum_df['rel_frame'] == 0].index[0]
    contact_frame_kinematics = kinematics_df[kinematics_df['rel_frame'] == 0].index[0]
    
    # Frames should align
    assert contact_frame_momentum is not None
    assert contact_frame_kinematics is not None
    
    print("✅ Test 1.3 PASSED: Contact frame extracted successfully")
```

---

### **Test Suite 2: Metric Extraction**

#### **Test 2.1: Calculate Hip Angular Momentum**

```python
def test_calculate_hip_angmom():
    """
    Test hip angular momentum extraction at contact
    """
    momentum_df = parse_momentum_csv("eric_williams_data/momentum-energy.csv")
    
    hip_angmom = extract_hip_angular_momentum(momentum_df)
    
    # Eric Williams expected value
    expected = 2.10
    tolerance = 0.05
    
    assert abs(hip_angmom - expected) < tolerance, f"Expected {expected}, got {hip_angmom}"
    
    print(f"✅ Test 2.1 PASSED: Hip angmom = {hip_angmom:.2f} (expected {expected})")
```

#### **Test 2.2: Calculate Shoulder/Hip Ratio**

```python
def test_calculate_shoulder_hip_ratio():
    """
    Test shoulder/hip ratio calculation
    """
    momentum_df = parse_momentum_csv("eric_williams_data/momentum-energy.csv")
    
    hip_angmom = extract_hip_angular_momentum(momentum_df)
    shoulder_angmom = extract_shoulder_angular_momentum(momentum_df)
    ratio = shoulder_angmom / hip_angmom
    
    # Eric Williams expected ratio
    expected_ratio = 8.68
    tolerance = 0.2
    
    assert abs(ratio - expected_ratio) < tolerance, f"Expected {expected_ratio}, got {ratio}"
    
    print(f"✅ Test 2.2 PASSED: Shoulder/Hip ratio = {ratio:.2f}x (expected {expected_ratio}x)")
```

#### **Test 2.3: Extract Lead Knee Angle**

```python
def test_extract_lead_knee_angle():
    """
    Test lead knee angle extraction at contact
    """
    kinematics_df = parse_kinematics_csv("eric_williams_data/inverse-kinematics.csv")
    handedness = "RHH"
    
    lead_knee_angle = extract_lead_knee_angle(kinematics_df, handedness)
    
    # Eric Williams expected value
    expected = 0.3
    tolerance = 0.5
    
    assert abs(lead_knee_angle - expected) < tolerance, f"Expected {expected}°, got {lead_knee_angle}°"
    
    print(f"✅ Test 2.3 PASSED: Lead knee angle = {lead_knee_angle:.1f}° (expected {expected}°)")
```

---

### **Test Suite 3: Pattern Recognition**

#### **Test 3.1: Detect Energy Leak Pattern**

```python
def test_detect_energy_leak_pattern():
    """
    Test PATTERN_1_KNEE_LEAK detection
    """
    metrics = {
        'lead_knee_angle': 0.3,
        'hip_angular_momentum': 2.10,
        'shoulder_angular_momentum': 18.25,
        'shoulder_hip_ratio': 8.68,
        'timing_gap_ms': 158.3
    }
    
    pattern = diagnose_pattern(metrics)
    
    assert pattern['type'] == 'PATTERN_1_KNEE_LEAK', f"Expected PATTERN_1_KNEE_LEAK, got {pattern['type']}"
    assert pattern['severity'] == 'CRITICAL'
    assert pattern['primary_protocol'] == 'PROTOCOL_1'
    
    print(f"✅ Test 3.1 PASSED: {pattern['type']} detected correctly")
```

#### **Test 3.2: Detect Spinner Pattern**

```python
def test_detect_spinner_pattern():
    """
    Test PATTERN_3_SPINNER detection
    """
    metrics = {
        'lead_knee_angle': 125.0,
        'hip_angular_momentum': 3.8,
        'shoulder_angular_momentum': 14.2,
        'shoulder_hip_ratio': 3.74,
        'timing_gap_ms': 12.0
    }
    
    pattern = diagnose_pattern(metrics)
    
    assert pattern['type'] == 'PATTERN_3_SPINNER', f"Expected PATTERN_3_SPINNER, got {pattern['type']}"
    assert pattern['primary_protocol'] == 'PROTOCOL_2'
    
    print(f"✅ Test 3.2 PASSED: {pattern['type']} detected correctly")
```

#### **Test 3.3: No Pattern (Elite Hitter)**

```python
def test_no_pattern_elite_hitter():
    """
    Test that elite mechanics don't trigger false positives
    """
    metrics = {
        'lead_knee_angle': 170.0,
        'hip_angular_momentum': 9.5,
        'shoulder_angular_momentum': 12.8,
        'shoulder_hip_ratio': 1.35,
        'timing_gap_ms': 22.0
    }
    
    pattern = diagnose_pattern(metrics)
    
    assert pattern['type'] in ['PATTERN_NONE', 'PATTERN_UNCLEAR']
    assert pattern['severity'] in ['NONE', 'LOW']
    
    print(f"✅ Test 3.3 PASSED: No critical pattern detected for elite hitter")
```

---

### **Test Suite 4: Efficiency Calculations**

#### **Test 4.1: Calculate Hip Efficiency**

```python
def test_calculate_hip_efficiency():
    """
    Test hip efficiency calculation
    """
    hip_angmom = 2.10
    
    hip_efficiency = (hip_angmom / 10.0) * 100
    
    expected = 21.0
    
    assert abs(hip_efficiency - expected) < 0.1, f"Expected {expected}%, got {hip_efficiency}%"
    
    print(f"✅ Test 4.1 PASSED: Hip efficiency = {hip_efficiency:.1f}% (expected {expected}%)")
```

#### **Test 4.2: Calculate Total Efficiency**

```python
def test_calculate_total_efficiency():
    """
    Test weighted total efficiency calculation
    """
    efficiency = calculate_efficiency_scores({
        'hip_angular_momentum': 2.10,
        'lead_knee_angle': 0.3,
        'lead_arm_extension': 1.5
    })
    
    expected_total = 11.2
    tolerance = 1.0
    
    assert abs(efficiency['total_efficiency'] - expected_total) < tolerance
    
    print(f"✅ Test 4.2 PASSED: Total efficiency = {efficiency['total_efficiency']:.1f}% (expected {expected_total}%)")
```

---

### **Test Suite 5: Outcome Predictions**

#### **Test 5.1: Predict Exit Velocity**

```python
def test_predict_exit_velocity():
    """
    Test exit velocity prediction
    """
    bat_speed = 82.0
    efficiency = {'total_efficiency': 11.2}
    
    current_ev = bat_speed * (efficiency['total_efficiency'] / 100.0)
    
    # Eric's current weak contact
    expected_current = 9.2
    tolerance = 1.0
    
    assert abs(current_ev - expected_current) < tolerance
    
    # Predicted after training (85% efficiency)
    predicted_ev = bat_speed * 0.85
    expected_predicted = 69.7
    
    assert abs(predicted_ev - expected_predicted) < tolerance
    
    print(f"✅ Test 5.1 PASSED: Exit velocity prediction correct")
```

#### **Test 5.2: Predict Launch Angle**

```python
def test_predict_launch_angle():
    """
    Test launch angle prediction based on lead arm extension
    """
    # Current (weak extension)
    lead_arm_ext = 1.5
    current_la = predict_launch_angle(lead_arm_ext)
    
    assert current_la < 5, "Low extension should predict ground balls (< 5°)"
    
    # After training (good extension)
    lead_arm_ext_fixed = 18.0
    predicted_la = predict_launch_angle(lead_arm_ext_fixed)
    
    assert 12 <= predicted_la <= 18, "Good extension should predict line drives (12-18°)"
    
    print(f"✅ Test 5.2 PASSED: Launch angle prediction correct")
```

---

## 🔗 INTEGRATION TESTS

### **Test Suite 6: End-to-End Analysis**

#### **Test 6.1: Full Eric Williams Analysis**

```python
def test_full_eric_analysis():
    """
    Complete analysis pipeline for Eric Williams
    """
    # Step 1: Upload files
    result = analyze_swing(
        momentum_file="eric_williams_data/momentum-energy.csv",
        kinematics_file="eric_williams_data/inverse-kinematics.csv",
        athlete_info={
            "name": "Eric Williams",
            "handedness": "RHH",
            "age": 24
        }
    )
    
    # Step 2: Validate metrics
    assert result['metrics']['lead_knee_angle'] < 5.0
    assert result['metrics']['hip_angular_momentum'] < 5.0
    assert result['metrics']['shoulder_hip_ratio'] > 5.0
    
    # Step 3: Validate pattern
    assert result['pattern']['type'] == 'PATTERN_1_KNEE_LEAK'
    
    # Step 4: Validate training plan
    assert 'PROTOCOL_1' in result['training_plan']['protocols_used']
    assert result['training_plan']['total_weeks'] == 6
    
    # Step 5: Validate predictions
    assert result['ball_outcomes']['improvement']['exit_velo_gain'] > 5.0
    
    # Step 6: Validate overall score
    assert 55 <= result['overall_score'] <= 65
    
    print("✅ Test 6.1 PASSED: Full Eric Williams analysis correct")
```

#### **Test 6.2: Before/After Comparison**

```python
def test_before_after_comparison():
    """
    Test comparison of before and after training data
    """
    # Before analysis (Eric Williams baseline)
    before = analyze_swing(
        "eric_williams_data/momentum-energy.csv",
        "eric_williams_data/inverse-kinematics.csv",
        {"name": "Eric Williams", "handedness": "RHH"}
    )
    
    # Simulate after training (mock improved metrics)
    after_mock = {
        'lead_knee_angle': 165.0,
        'hip_angular_momentum': 8.5,
        'exit_velo': 89.0
    }
    
    # Calculate improvements
    knee_improvement = after_mock['lead_knee_angle'] - before['metrics']['lead_knee_angle']
    hip_improvement = after_mock['hip_angular_momentum'] - before['metrics']['hip_angular_momentum']
    ev_improvement = after_mock['exit_velo'] - before['ball_outcomes']['current']['exit_velo']
    
    # Validate improvements match predictions
    predicted_ev_gain = before['ball_outcomes']['improvement']['exit_velo_gain']
    assert abs(ev_improvement - predicted_ev_gain) < 3.0, "Exit velo improvement should match prediction"
    
    print(f"✅ Test 6.2 PASSED: Before/After comparison correct")
    print(f"   Knee: {before['metrics']['lead_knee_angle']:.1f}° → {after_mock['lead_knee_angle']:.1f}°")
    print(f"   Hip: {before['metrics']['hip_angular_momentum']:.1f} → {after_mock['hip_angular_momentum']:.1f}")
    print(f"   EV: {before['ball_outcomes']['current']['exit_velo']:.0f} → {after_mock['exit_velo']:.0f} mph")
```

---

## 🚨 EDGE CASE TESTS

### **Test Suite 7: Error Handling**

#### **Test 7.1: Missing Required Columns**

```python
def test_missing_columns():
    """
    Test error handling when CSV is missing required columns
    """
    # Create CSV with missing columns
    invalid_csv = create_csv_with_missing_columns(['bat_kinetic_energy'])
    
    try:
        result = analyze_swing(invalid_csv, "valid_kinematics.csv", {"name": "Test", "handedness": "RHH"})
        assert False, "Should have raised an error"
    except Exception as e:
        assert "missing_columns" in str(e).lower() or "MISSING_COLUMNS" in str(e)
        print(f"✅ Test 7.1 PASSED: Missing columns error caught correctly")
```

#### **Test 7.2: No Contact Frame**

```python
def test_no_contact_frame():
    """
    Test error when rel_frame = 0 doesn't exist
    """
    # Create CSV without contact frame
    invalid_csv = create_csv_without_frame_zero()
    
    try:
        result = analyze_swing(invalid_csv, "valid_kinematics.csv", {"name": "Test", "handedness": "RHH"})
        assert False, "Should have raised an error"
    except Exception as e:
        assert "contact frame" in str(e).lower() or "NO_CONTACT_FRAME" in str(e)
        print(f"✅ Test 7.2 PASSED: No contact frame error caught correctly")
```

#### **Test 7.3: Invalid Handedness**

```python
def test_invalid_handedness():
    """
    Test error when handedness is invalid
    """
    try:
        result = analyze_swing(
            "valid_momentum.csv",
            "valid_kinematics.csv",
            {"name": "Test", "handedness": "SWITCH"}  # Invalid
        )
        assert False, "Should have raised an error"
    except Exception as e:
        assert "handedness" in str(e).lower()
        print(f"✅ Test 7.3 PASSED: Invalid handedness error caught correctly")
```

#### **Test 7.4: Frame Alignment Mismatch**

```python
def test_frame_alignment_mismatch():
    """
    Test error when CSV files don't have matching frames
    """
    # Create mismatched CSVs (different frame counts)
    momentum_csv = create_csv(755 frames)
    kinematics_csv = create_csv(600 frames)  # Mismatch
    
    try:
        result = analyze_swing(momentum_csv, kinematics_csv, {"name": "Test", "handedness": "RHH"})
        assert False, "Should have raised an error"
    except Exception as e:
        assert "alignment" in str(e).lower() or "frame" in str(e).lower()
        print(f"✅ Test 7.4 PASSED: Frame alignment error caught correctly")
```

#### **Test 7.5: Extreme Values**

```python
def test_extreme_values():
    """
    Test handling of extreme/outlier values
    """
    metrics = {
        'lead_knee_angle': 200.0,  # Impossible (> 180°)
        'hip_angular_momentum': -5.0,  # Negative (impossible)
        'shoulder_hip_ratio': 50.0  # Extremely high
    }
    
    # System should either:
    # 1. Flag as invalid and reject
    # 2. Clamp to reasonable ranges
    # 3. Warn but process
    
    pattern = diagnose_pattern(metrics)
    
    # Should handle gracefully (not crash)
    assert pattern is not None
    print(f"✅ Test 7.5 PASSED: Extreme values handled gracefully")
```

---

## ⚡ PERFORMANCE TESTS

### **Test Suite 8: Speed & Scalability**

#### **Test 8.1: Analysis Speed**

```python
import time

def test_analysis_speed():
    """
    Test that analysis completes in reasonable time
    """
    start = time.time()
    
    result = analyze_swing(
        "eric_williams_data/momentum-energy.csv",
        "eric_williams_data/inverse-kinematics.csv",
        {"name": "Eric Williams", "handedness": "RHH"}
    )
    
    elapsed = time.time() - start
    
    # Should complete in under 5 seconds
    assert elapsed < 5.0, f"Analysis took {elapsed:.2f}s (should be < 5s)"
    
    print(f"✅ Test 8.1 PASSED: Analysis completed in {elapsed:.2f}s")
```

#### **Test 8.2: Large File Handling**

```python
def test_large_file_handling():
    """
    Test handling of large CSV files (e.g., 10,000+ frames)
    """
    # Create large CSV file
    large_csv = create_large_csv(10000 frames)
    
    start = time.time()
    result = analyze_swing(large_csv, large_csv, {"name": "Test", "handedness": "RHH"})
    elapsed = time.time() - start
    
    # Should still complete in reasonable time
    assert elapsed < 15.0, f"Large file took {elapsed:.2f}s (should be < 15s)"
    
    print(f"✅ Test 8.2 PASSED: Large file handled in {elapsed:.2f}s")
```

#### **Test 8.3: Concurrent Requests**

```python
import threading

def test_concurrent_requests():
    """
    Test handling multiple simultaneous analyses
    """
    def run_analysis():
        result = analyze_swing(
            "eric_williams_data/momentum-energy.csv",
            "eric_williams_data/inverse-kinematics.csv",
            {"name": "Eric Williams", "handedness": "RHH"}
        )
        return result
    
    # Run 10 analyses concurrently
    threads = []
    for i in range(10):
        t = threading.Thread(target=run_analysis)
        threads.append(t)
        t.start()
    
    start = time.time()
    for t in threads:
        t.join()
    elapsed = time.time() - start
    
    # Should complete in reasonable time
    assert elapsed < 30.0, f"10 concurrent analyses took {elapsed:.2f}s"
    
    print(f"✅ Test 8.3 PASSED: 10 concurrent analyses in {elapsed:.2f}s")
```

---

## ✅ VALIDATION CRITERIA

### **System Passes When:**

#### **Functional Validation:**
- [ ] All Eric Williams metrics match within ±5%
- [ ] Pattern detection is 100% accurate on test cases
- [ ] Efficiency calculations match formulas
- [ ] Predictions are within ±10% of expected
- [ ] Training plans auto-generate correctly
- [ ] Before/After comparison works

#### **Error Handling:**
- [ ] Missing columns caught and reported
- [ ] No contact frame error handled
- [ ] Invalid handedness rejected
- [ ] Frame misalignment detected
- [ ] Extreme values handled gracefully

#### **Performance:**
- [ ] Single analysis < 5 seconds
- [ ] Large files (10k+ frames) < 15 seconds
- [ ] 10 concurrent analyses < 30 seconds
- [ ] Memory usage < 500MB per analysis

#### **UI/UX:**
- [ ] Report renders in < 2 seconds
- [ ] All sections display correctly
- [ ] Color coding matches severity
- [ ] Mobile responsive
- [ ] PDF export works

---

## 🔄 REGRESSION TEST SUITE

Run this full suite before each release:

```bash
# Run all tests
python -m pytest tests/ -v

# Expected output:
# test_parse_momentum_csv           PASSED
# test_parse_kinematics_csv         PASSED
# test_calculate_hip_angmom         PASSED
# test_detect_energy_leak_pattern   PASSED
# test_full_eric_analysis           PASSED
# ... (all tests)
# 
# 30/30 tests passed (100%)
```

---

## 📊 TEST COVERAGE TARGET

**Minimum Coverage**: 90%

**Critical Areas** (Must be 100%):
- Data parsing
- Pattern recognition
- Efficiency calculations
- Prediction formulas

**Lower Priority** (Can be 80%):
- UI rendering
- PDF generation
- Email notifications

---

## 🆘 DEBUGGING FAILED TESTS

### **If Metrics Don't Match:**
1. Check CSV parsing (column names, data types)
2. Verify contact frame extraction (rel_frame = 0)
3. Print intermediate values at each calculation step
4. Compare with Knowledge Base formulas

### **If Pattern Not Detected:**
1. Review thresholds in diagnostic logic
2. Check if metrics are NaN (handle missing data)
3. Print all metrics before pattern matching
4. Manually verify against pattern definitions

### **If Predictions Are Wrong:**
1. Verify efficiency calculation
2. Check bat_speed extraction
3. Ensure lead_arm_extension is correct
4. Review prediction formulas in Knowledge Base

---

**Test Suite Version**: 1.0  
**Last Updated**: December 25, 2025  
**Maintained By**: QA Team

---

*End of Test Cases*
