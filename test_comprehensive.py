"""
COMPREHENSIVE TEST SUITE - Reboot Lite + Coach Rick AI
========================================================

Tests all components:
1. Existing Reboot Lite API (BAT Module, Tempo, Stability, Race Bar)
2. New Coach Rick AI Engine (Motor Profile, Pattern Recognition)
3. Integration tests

Author: Builder 2
Date: 2024-12-24
"""

import requests
import json
from typing import Dict, List

# Test server URLs
BASE_URL_8002 = "http://localhost:8002"  # Priority 13 server
BASE_URL_8003 = "http://localhost:8003"  # Priority 16 server

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def print_test_header(test_name: str):
    """Print test section header"""
    print(f"\n{'=' * 70}")
    print(f"{BLUE}🧪 TEST: {test_name}{RESET}")
    print(f"{'=' * 70}")


def print_success(message: str):
    """Print success message"""
    print(f"{GREEN}✅ {message}{RESET}")


def print_error(message: str):
    """Print error message"""
    print(f"{RED}❌ {message}{RESET}")


def print_info(message: str):
    """Print info message"""
    print(f"{YELLOW}ℹ️  {message}{RESET}")


# ============================================================
# TEST 1: COACH RICK AI - Motor Profile Classifier
# ============================================================

def test_motor_profile_classifier():
    """Test motor profile classification"""
    print_test_header("Motor Profile Classifier")
    
    try:
        import sys
        sys.path.insert(0, '/home/user/webapp')
        from coach_rick.motor_profile_classifier import classify_motor_profile
        
        # Test case 1: Spinner
        spinner_data = {
            "kinematic_sequence": {
                "torso_peak_ms": 145,
                "arms_peak_ms": 165,
                "bat_peak_ms": 180
            },
            "tempo": {"ratio": 2.1},
            "stability": {"score": 92},
            "bat_speed": 82
        }
        
        result = classify_motor_profile(spinner_data)
        
        if result.profile == "Spinner" and result.confidence >= 0.8:
            print_success(f"Spinner classification correct: {result.profile} ({result.confidence:.0%} confidence)")
            print_info(f"Characteristics: {', '.join(result.characteristics[:2])}")
        else:
            print_error(f"Spinner classification failed: {result.profile}")
            return False
        
        # Test case 2: Whipper
        whipper_data = {
            "kinematic_sequence": {
                "torso_peak_ms": 140,
                "arms_peak_ms": 175,
                "bat_peak_ms": 200
            },
            "tempo": {"ratio": 2.8},
            "stability": {"score": 88},
            "bat_speed": 85
        }
        
        result = classify_motor_profile(whipper_data)
        
        if result.profile == "Whipper" and result.confidence >= 0.8:
            print_success(f"Whipper classification correct: {result.profile} ({result.confidence:.0%} confidence)")
        else:
            print_error(f"Whipper classification failed: {result.profile}")
            return False
        
        # Test case 3: Torquer
        torquer_data = {
            "kinematic_sequence": {
                "torso_peak_ms": 150,
                "arms_peak_ms": 160,
                "bat_peak_ms": 170
            },
            "tempo": {"ratio": 1.5},
            "stability": {"score": 94},
            "bat_speed": 80
        }
        
        result = classify_motor_profile(torquer_data)
        
        if result.profile == "Torquer" and result.confidence >= 0.8:
            print_success(f"Torquer classification correct: {result.profile} ({result.confidence:.0%} confidence)")
        else:
            print_error(f"Torquer classification failed: {result.profile}")
            return False
        
        print_success("Motor Profile Classifier: ALL TESTS PASSED ✓")
        return True
        
    except Exception as e:
        print_error(f"Motor Profile Classifier test failed: {str(e)}")
        return False


# ============================================================
# TEST 2: COACH RICK AI - Pattern Recognition
# ============================================================

def test_pattern_recognition():
    """Test pattern recognition engine"""
    print_test_header("Pattern Recognition Engine")
    
    try:
        import sys
        sys.path.insert(0, '/home/user/webapp')
        from coach_rick.pattern_recognition import PatternRecognitionEngine
        from coach_rick.motor_profile_classifier import classify_motor_profile
        
        # Test case: Spinner with lead arm bent
        spinner_data = {
            "kinematic_sequence": {
                "torso_peak_ms": 145,
                "arms_peak_ms": 160,  # 15ms gap
                "bat_peak_ms": 173,   # 13ms gap
                "grade": "B"
            },
            "tempo": {"ratio": 2.1},
            "stability": {"score": 92},
            "bat_speed": 82
        }
        
        motor_profile_result = classify_motor_profile(spinner_data)
        engine = PatternRecognitionEngine()
        patterns = engine.analyze(spinner_data, motor_profile_result.profile)
        
        if len(patterns) > 0:
            print_success(f"Pattern recognition found {len(patterns)} issues")
            for i, pattern in enumerate(patterns[:2], 1):
                print_info(f"  {i}. [{pattern.priority}] {pattern.diagnosis}")
        else:
            print_error("No patterns detected")
            return False
        
        # Test case 2: Poor stability (universal pattern)
        poor_stability_data = {
            "kinematic_sequence": {
                "torso_peak_ms": 145,
                "arms_peak_ms": 165,
                "bat_peak_ms": 185,
                "grade": "A"
            },
            "tempo": {"ratio": 2.1},
            "stability": {"score": 68},  # Poor
            "bat_speed": 80
        }
        
        motor_profile_result = classify_motor_profile(poor_stability_data)
        patterns = engine.analyze(poor_stability_data, motor_profile_result.profile)
        
        # Should detect stability issue
        stability_pattern = next((p for p in patterns if 'stability' in p.pattern_id), None)
        if stability_pattern:
            print_success("Universal stability pattern detected correctly")
        else:
            print_error("Stability pattern not detected")
            return False
        
        print_success("Pattern Recognition Engine: ALL TESTS PASSED ✓")
        return True
        
    except Exception as e:
        print_error(f"Pattern Recognition test failed: {str(e)}")
        return False


# ============================================================
# TEST 3: BAT MODULE (from Reboot Lite)
# ============================================================

def test_bat_module():
    """Test BAT optimization module"""
    print_test_header("BAT Module (MOI & Optimization)")
    
    try:
        import sys
        sys.path.insert(0, '/home/user/webapp')
        from physics_engine.bat_module import BatModule
        
        # Eric Williams example
        bat_module = BatModule()
        
        # Test MOI calculation
        moi = bat_module.calculate_moi(
            bat_weight_oz=30.0,
            bat_length_inches=33.0,
            bat_type="balanced"
        )
        
        if 0.14 <= moi <= 0.16:
            print_success(f"MOI calculation correct: {moi:.4f} kg·m²")
        else:
            print_error(f"MOI calculation out of range: {moi:.4f}")
            return False
        
        # Test bat optimization
        result = bat_module.analyze_bat_optimization(
            bat_weight_oz=30.0,
            bat_length_inches=33.0,
            bat_speed_mph=82.0,
            body_kinetic_energy=514.0,
            player_height_inches=70,
            player_weight_lbs=185,
            bat_type="balanced"
        )
        
        if result.transfer_efficiency_percent >= 50:
            print_success(f"Transfer efficiency: {result.transfer_efficiency_percent:.1f}%")
        else:
            print_error(f"Transfer efficiency too low: {result.transfer_efficiency_percent:.1f}%")
            return False
        
        if len(result.recommended_weights) > 0:
            print_success(f"Generated {len(result.recommended_weights)} bat weight recommendations")
            print_info(f"  Optimal range: {result.optimal_weight_range_oz[0]}-{result.optimal_weight_range_oz[1]} oz")
        else:
            print_error("No bat weight recommendations generated")
            return False
        
        print_success("BAT Module: ALL TESTS PASSED ✓")
        return True
        
    except Exception as e:
        print_error(f"BAT Module test failed: {str(e)}")
        return False


# ============================================================
# TEST 4: HEALTH CHECKS (API Endpoints)
# ============================================================

def test_api_health_checks():
    """Test API endpoint health checks"""
    print_test_header("API Health Checks")
    
    test_results = []
    
    # Test port 8002 (Priority 13)
    try:
        response = requests.get(f"{BASE_URL_8002}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"Port 8002 health check: OK")
            test_results.append(True)
        else:
            print_error(f"Port 8002 health check failed: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print_error(f"Port 8002 health check failed: {str(e)}")
        test_results.append(False)
    
    # Test port 8003 (Priority 16)
    try:
        response = requests.get(f"{BASE_URL_8003}/health", timeout=5)
        if response.status_code == 200:
            print_success(f"Port 8003 health check: OK")
            test_results.append(True)
        else:
            print_error(f"Port 8003 health check failed: {response.status_code}")
            test_results.append(False)
    except Exception as e:
        print_error(f"Port 8003 health check failed: {str(e)}")
        test_results.append(False)
    
    if all(test_results):
        print_success("API Health Checks: ALL TESTS PASSED ✓")
        return True
    else:
        print_error("Some API health checks failed")
        return False


# ============================================================
# TEST 5: KNOWLEDGE BASE
# ============================================================

def test_knowledge_base():
    """Test knowledge base (drills, patterns, rules)"""
    print_test_header("Knowledge Base (Drills & Rules)")
    
    try:
        import sys
        sys.path.insert(0, '/home/user/webapp')
        from coach_rick.knowledge_base import DRILL_LIBRARY, PATTERN_RULES, PRESCRIPTION_RULES
        
        # Test drill library
        if len(DRILL_LIBRARY) >= 10:
            print_success(f"Drill library loaded: {len(DRILL_LIBRARY)} drills")
        else:
            print_error(f"Drill library incomplete: {len(DRILL_LIBRARY)} drills")
            return False
        
        # Test pattern rules
        if len(PATTERN_RULES) >= 10:
            print_success(f"Pattern rules loaded: {len(PATTERN_RULES)} patterns")
        else:
            print_error(f"Pattern rules incomplete: {len(PATTERN_RULES)} patterns")
            return False
        
        # Test prescription rules
        if len(PRESCRIPTION_RULES) >= 8:
            print_success(f"Prescription rules loaded: {len(PRESCRIPTION_RULES)} prescriptions")
        else:
            print_error(f"Prescription rules incomplete: {len(PRESCRIPTION_RULES)} prescriptions")
            return False
        
        # Test specific drill
        rope_swings = DRILL_LIBRARY.get('rope_swings')
        if rope_swings and 'drill_name' in rope_swings:
            print_success(f"Sample drill verified: {rope_swings['drill_name']}")
        else:
            print_error("Sample drill not found or malformed")
            return False
        
        print_success("Knowledge Base: ALL TESTS PASSED ✓")
        return True
        
    except Exception as e:
        print_error(f"Knowledge Base test failed: {str(e)}")
        return False


# ============================================================
# RUN ALL TESTS
# ============================================================

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 70)
    print(f"{BLUE}🚀 STARTING COMPREHENSIVE TEST SUITE{RESET}")
    print("=" * 70)
    print(f"{YELLOW}Testing: Reboot Lite + Coach Rick AI Engine{RESET}")
    print(f"{YELLOW}Date: 2024-12-24{RESET}")
    print("=" * 70)
    
    results = {
        "Motor Profile Classifier": test_motor_profile_classifier(),
        "Pattern Recognition Engine": test_pattern_recognition(),
        "BAT Module": test_bat_module(),
        "API Health Checks": test_api_health_checks(),
        "Knowledge Base": test_knowledge_base()
    }
    
    # Summary
    print("\n" + "=" * 70)
    print(f"{BLUE}📊 TEST SUMMARY{RESET}")
    print("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}✅ PASS{RESET}" if result else f"{RED}❌ FAIL{RESET}"
        print(f"{test_name:.<50} {status}")
    
    print("=" * 70)
    print(f"Total: {passed}/{total} tests passed ({passed/total*100:.0f}%)")
    
    if passed == total:
        print(f"\n{GREEN}🎉 ALL TESTS PASSED! System is working correctly.{RESET}")
        return True
    else:
        print(f"\n{RED}⚠️  SOME TESTS FAILED. Review errors above.{RESET}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
