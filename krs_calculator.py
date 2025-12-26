"""
KRS Calculator Service
Phase 1 Week 3-4: Priority 2
Formula: KRS = (Creation × 0.4) + (Transfer × 0.6)
Scale: 0-100
Levels: FOUNDATION (0-40), BUILDING (40-60), DEVELOPING (60-75), ADVANCED (75-85), ELITE (85-100)
"""

from typing import Dict, Optional


def calculate_krs(creation: float, transfer: float) -> Dict[str, any]:
    """
    Calculate KRS from Creation and Transfer scores.
    
    Args:
        creation: Creation score (0-100)
        transfer: Transfer score (0-100)
    
    Returns:
        {
            "krs_total": float,
            "krs_level": str,
            "creation": float,
            "transfer": float,
            "level_info": dict
        }
    
    Examples:
        >>> calculate_krs(74.8, 69.5)
        {'krs_total': 71.6, 'krs_level': 'ADVANCED', ...}
        
        >>> calculate_krs(80, 90)
        {'krs_total': 86.0, 'krs_level': 'ELITE', ...}
        
        >>> calculate_krs(50, 60)
        {'krs_total': 56.0, 'krs_level': 'BUILDING', ...}
    """
    # Validate inputs
    if not (0 <= creation <= 100):
        raise ValueError(f"Creation score must be 0-100, got {creation}")
    if not (0 <= transfer <= 100):
        raise ValueError(f"Transfer score must be 0-100, got {transfer}")
    
    # Calculate KRS using weighted formula
    krs_total = (creation * 0.4) + (transfer * 0.6)
    
    # Determine level based on KRS total
    if krs_total >= 85:
        level = "ELITE"
        level_info = {
            "name": "ELITE",
            "range": "85-100",
            "color": "#8B5CF6",  # Purple
            "description": "Elite performer with exceptional mechanics"
        }
    elif krs_total >= 75:
        level = "ADVANCED"
        level_info = {
            "name": "ADVANCED",
            "range": "75-85",
            "color": "#06B6D4",  # Cyan
            "description": "Advanced player with consistent high-quality mechanics"
        }
    elif krs_total >= 60:
        level = "DEVELOPING"
        level_info = {
            "name": "DEVELOPING",
            "range": "60-75",
            "color": "#F59E0B",  # Amber
            "description": "Developing player with solid fundamentals"
        }
    elif krs_total >= 40:
        level = "BUILDING"
        level_info = {
            "name": "BUILDING",
            "range": "40-60",
            "color": "#475569",  # Gray
            "description": "Building foundational movement patterns"
        }
    else:
        level = "FOUNDATION"
        level_info = {
            "name": "FOUNDATION",
            "range": "0-40",
            "color": "#1E293B",  # Dark Slate
            "description": "Establishing fundamental movement patterns"
        }
    
    return {
        "krs_total": round(krs_total, 1),
        "krs_level": level,
        "creation": round(creation, 1),
        "transfer": round(transfer, 1),
        "level_info": level_info
    }


def calculate_on_table_gain(
    current_exit_velo: float,
    physical_capacity: float,
    transfer_score: float
) -> Optional[Dict[str, any]]:
    """
    Calculate On-Table Gain (exit velocity improvement with optimal mechanics).
    
    Args:
        current_exit_velo: Current exit velocity (mph)
        physical_capacity: Max physical capacity (mph)
        transfer_score: Transfer score (0-100)
    
    Returns:
        {
            "value": float,  # e.g., 3.1
            "metric": str,   # "mph"
            "description": str
        }
    
    Formula:
        Potential improvement = (physical_capacity - current_exit_velo) * (1 - transfer_score/100)
        On-table gain shows how much exit velo can be gained by improving transfer efficiency
    """
    if not current_exit_velo or not physical_capacity or not transfer_score:
        return None
    
    # Calculate potential gain based on transfer efficiency gap
    efficiency_gap = 1 - (transfer_score / 100)  # e.g., 0.305 for transfer_score=69.5
    potential_improvement = (physical_capacity - current_exit_velo) * efficiency_gap
    
    # Only show gain if there's meaningful improvement potential
    if potential_improvement < 0.5:
        return None
    
    return {
        "value": round(potential_improvement, 1),
        "metric": "mph",
        "description": "Exit velocity improvement with optimal mechanics"
    }


def get_krs_level_ranges() -> Dict[str, Dict[str, any]]:
    """
    Get KRS level definitions for reference.
    
    Returns:
        Dictionary of level definitions with ranges, colors, and descriptions
    """
    return {
        "FOUNDATION": {
            "min": 0,
            "max": 40,
            "color": "#1E293B",
            "description": "Establishing fundamental movement patterns"
        },
        "BUILDING": {
            "min": 40,
            "max": 60,
            "color": "#475569",
            "description": "Building foundational movement patterns"
        },
        "DEVELOPING": {
            "min": 60,
            "max": 75,
            "color": "#F59E0B",
            "description": "Developing player with solid fundamentals"
        },
        "ADVANCED": {
            "min": 75,
            "max": 85,
            "color": "#06B6D4",
            "description": "Advanced player with consistent high-quality mechanics"
        },
        "ELITE": {
            "min": 85,
            "max": 100,
            "color": "#8B5CF6",
            "description": "Elite performer with exceptional mechanics"
        }
    }


def validate_krs_calculation(krs_data: dict) -> bool:
    """
    Validate KRS calculation results.
    
    Args:
        krs_data: Output from calculate_krs()
    
    Returns:
        True if valid, raises ValueError if invalid
    """
    required_keys = ['krs_total', 'krs_level', 'creation', 'transfer']
    for key in required_keys:
        if key not in krs_data:
            raise ValueError(f"Missing required key: {key}")
    
    # Validate ranges
    if not (0 <= krs_data['krs_total'] <= 100):
        raise ValueError(f"krs_total out of range: {krs_data['krs_total']}")
    if not (0 <= krs_data['creation'] <= 100):
        raise ValueError(f"creation out of range: {krs_data['creation']}")
    if not (0 <= krs_data['transfer'] <= 100):
        raise ValueError(f"transfer out of range: {krs_data['transfer']}")
    
    # Validate level
    valid_levels = ['FOUNDATION', 'BUILDING', 'DEVELOPING', 'ADVANCED', 'ELITE']
    if krs_data['krs_level'] not in valid_levels:
        raise ValueError(f"Invalid krs_level: {krs_data['krs_level']}")
    
    # Verify formula
    expected_krs = round((krs_data['creation'] * 0.4) + (krs_data['transfer'] * 0.6), 1)
    if abs(krs_data['krs_total'] - expected_krs) > 0.1:
        raise ValueError(
            f"KRS calculation mismatch. Expected {expected_krs}, got {krs_data['krs_total']}"
        )
    
    return True


# Test cases for validation
if __name__ == "__main__":
    print("Running KRS Calculator Tests...")
    print("=" * 60)
    
    # Test Case 1: Creation=74.8, Transfer=69.5 → KRS≈71.6, DEVELOPING
    test1 = calculate_krs(74.8, 69.5)
    print(f"\nTest 1: Creation=74.8, Transfer=69.5")
    print(f"  Result: KRS={test1['krs_total']}, Level={test1['krs_level']}")
    assert test1['krs_total'] == 71.6, f"Expected 71.6, got {test1['krs_total']}"
    assert test1['krs_level'] == 'DEVELOPING', f"Expected DEVELOPING, got {test1['krs_level']}"
    print("  ✅ PASS")
    
    # Test Case 2: Creation=80, Transfer=90 → KRS=86, ELITE
    test2 = calculate_krs(80, 90)
    print(f"\nTest 2: Creation=80, Transfer=90")
    print(f"  Result: KRS={test2['krs_total']}, Level={test2['krs_level']}")
    assert test2['krs_total'] == 86.0, f"Expected 86.0, got {test2['krs_total']}"
    assert test2['krs_level'] == 'ELITE', f"Expected ELITE, got {test2['krs_level']}"
    print("  ✅ PASS")
    
    # Test Case 3: Creation=50, Transfer=60 → KRS=56, BUILDING
    test3 = calculate_krs(50, 60)
    print(f"\nTest 3: Creation=50, Transfer=60")
    print(f"  Result: KRS={test3['krs_total']}, Level={test3['krs_level']}")
    assert test3['krs_total'] == 56.0, f"Expected 56.0, got {test3['krs_total']}"
    assert test3['krs_level'] == 'BUILDING', f"Expected BUILDING, got {test3['krs_level']}"
    print("  ✅ PASS")
    
    # Test Case 4: Edge case - ELITE boundary (85)
    test4 = calculate_krs(85, 85)
    print(f"\nTest 4: Creation=85, Transfer=85 (ELITE boundary)")
    print(f"  Result: KRS={test4['krs_total']}, Level={test4['krs_level']}")
    assert test4['krs_total'] == 85.0, f"Expected 85.0, got {test4['krs_total']}"
    assert test4['krs_level'] == 'ELITE', f"Expected ELITE, got {test4['krs_level']}"
    print("  ✅ PASS")
    
    # Test Case 5: Edge case - ADVANCED boundary (75)
    test5 = calculate_krs(75, 75)
    print(f"\nTest 5: Creation=75, Transfer=75 (ADVANCED boundary)")
    print(f"  Result: KRS={test5['krs_total']}, Level={test5['krs_level']}")
    assert test5['krs_total'] == 75.0, f"Expected 75.0, got {test5['krs_total']}"
    assert test5['krs_level'] == 'ADVANCED', f"Expected ADVANCED, got {test5['krs_level']}"
    print("  ✅ PASS")
    
    # Test Case 6: On-Table Gain calculation
    gain = calculate_on_table_gain(82, 95, 69.5)
    print(f"\nTest 6: On-Table Gain")
    print(f"  Current: 82 mph, Capacity: 95 mph, Transfer: 69.5")
    print(f"  Result: +{gain['value']} {gain['metric']}")
    assert gain['metric'] == 'mph', f"Expected 'mph', got {gain['metric']}"
    assert 2.0 <= gain['value'] <= 5.0, f"Expected gain between 2-5 mph, got {gain['value']}"
    print("  ✅ PASS")
    
    # Test Case 7: Validation
    print(f"\nTest 7: Validation")
    validate_krs_calculation(test1)
    print("  ✅ PASS")
    
    print("\n" + "=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
