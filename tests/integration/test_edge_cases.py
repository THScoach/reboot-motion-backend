"""
Integration Tests: Edge Cases
Phase 1 Week 3-4: Priority 5

Tests edge cases, error handling, and boundary conditions
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app.services.report_transformer import transform_coach_rick_to_report
from krs_calculator import calculate_krs


class TestEdgeCases:
    """Test edge cases and error handling"""
    
    def test_missing_optional_fields(self):
        """Test transformer handles missing optional fields"""
        minimal_data = {
            "bat_speed_mph": 75.0,
            "exit_velocity_mph": 85.0,
            "efficiency_percent": 95.0,
            "tempo_score": 75.0,
            "stability_score": 80.0,
            "gew_overall": 77.0,
            "motor_profile": {
                "type": "SPINNER",
                "confidence": 85.0
            }
            # Missing: hip_shoulder_gap_ms, hands_bat_gap_ms, launch_angle, etc.
        }
        
        report = transform_coach_rick_to_report(minimal_data, "edge_001", 1)
        
        # Should still produce valid report with defaults
        assert report["krs_total"] is not None
        assert report["krs_level"] is not None
        assert report["brain_timing"] >= 0  # Should use default timing
        
        print("✅ Test 1: Missing optional fields handled with defaults")
    
    def test_extreme_low_scores(self):
        """Test transformer handles very low performance scores"""
        low_performance_data = {
            "bat_speed_mph": 50.0,
            "exit_velocity_mph": 60.0,
            "efficiency_percent": 80.0,
            "tempo_score": 30.0,
            "stability_score": 40.0,
            "gew_overall": 35.0,
            "motor_profile": {
                "type": "SHAKER",
                "confidence": 60.0
            }
        }
        
        report = transform_coach_rick_to_report(low_performance_data, "edge_002", 1)
        
        # Should produce FOUNDATION or BUILDING level
        assert report["krs_total"] <= 60, "Low performance should yield low KRS"
        assert report["krs_level"] in ["FOUNDATION", "BUILDING"]
        assert report["ball_contact_quality"] == "POOR"
        
        print(f"✅ Test 2: Low performance - KRS {report['krs_total']} ({report['krs_level']})")
    
    def test_extreme_high_scores(self):
        """Test transformer handles exceptionally high scores"""
        elite_data = {
            "bat_speed_mph": 95.0,
            "exit_velocity_mph": 110.0,
            "efficiency_percent": 125.0,
            "tempo_score": 98.0,
            "stability_score": 99.0,
            "gew_overall": 98.0,
            "motor_profile": {
                "type": "TITAN",
                "confidence": 98.0
            }
        }
        
        report = transform_coach_rick_to_report(elite_data, "edge_003", 1)
        
        # Should produce ELITE level with capped KRS at 100
        assert report["krs_total"] <= 100, "KRS should be capped at 100"
        assert report["krs_level"] == "ELITE"
        assert report["ball_contact_quality"] == "EXCELLENT"
        
        print(f"✅ Test 3: Elite performance - KRS {report['krs_total']} ({report['krs_level']})")
    
    def test_zero_confidence_motor_profile(self):
        """Test transformer handles low confidence motor profile"""
        low_confidence_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 95.0,
            "efficiency_percent": 100.0,
            "tempo_score": 85.0,
            "stability_score": 90.0,
            "gew_overall": 87.0,
            "motor_profile": {
                "type": "UNKNOWN",
                "confidence": 0.0
            }
        }
        
        report = transform_coach_rick_to_report(low_confidence_data, "edge_004", 1)
        
        # Should still produce valid report
        assert report["brain_motor_profile"] is not None
        # Confidence rounded to 0 becomes None
        assert report["brain_confidence"] == 0 or report["brain_confidence"] is None
        assert report["krs_total"] is not None
        
        print(f"✅ Test 4: Low confidence motor profile handled")
    
    def test_invalid_motor_profile_type(self):
        """Test transformer handles unknown motor profile types"""
        invalid_profile_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 95.0,
            "efficiency_percent": 100.0,
            "tempo_score": 85.0,
            "stability_score": 90.0,
            "gew_overall": 87.0,
            "motor_profile": {
                "type": "INVALID_TYPE",
                "confidence": 85.0
            }
        }
        
        report = transform_coach_rick_to_report(invalid_profile_data, "edge_005", 1)
        
        # Should capitalize unknown types
        assert report["brain_motor_profile"] == "Invalid_type"
        
        print("✅ Test 5: Invalid motor profile type handled")
    
    def test_missing_tempo_stability_fallback(self):
        """Test fallback to GEW when tempo/stability missing"""
        fallback_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 95.0,
            "efficiency_percent": 100.0,
            # tempo_score and stability_score missing!
            "gew_overall": 85.0,
            "motor_profile": {
                "type": "SPINNER",
                "confidence": 88.0
            }
        }
        
        report = transform_coach_rick_to_report(fallback_data, "edge_006", 1)
        
        # Creation score should fall back to GEW
        assert report["creation_score"] == 85.0
        assert report["krs_total"] is not None
        
        print("✅ Test 6: Tempo/stability fallback to GEW")
    
    def test_missing_efficiency_fallback(self):
        """Test fallback to default when efficiency missing"""
        fallback_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 95.0,
            # efficiency_percent missing!
            "tempo_score": 85.0,
            "stability_score": 90.0,
            "gew_overall": 87.0,
            "motor_profile": {
                "type": "SPINNER",
                "confidence": 88.0
            }
        }
        
        report = transform_coach_rick_to_report(fallback_data, "edge_007", 1)
        
        # Transfer score should use default 70.0
        assert report["transfer_score"] == 70.0
        
        print("✅ Test 7: Efficiency fallback to default 70.0")
    
    def test_krs_boundary_conditions(self):
        """Test KRS level boundaries"""
        test_cases = [
            (0, 0, "FOUNDATION"),      # 0 KRS
            (40, 40, "BUILDING"),      # 40 KRS (boundary)
            (60, 60, "DEVELOPING"),    # 60 KRS (boundary)
            (75, 75, "ADVANCED"),      # 75 KRS (boundary)
            (85, 85, "ELITE"),         # 85 KRS (boundary)
            (100, 100, "ELITE")        # 100 KRS (max)
        ]
        
        for creation, transfer, expected_level in test_cases:
            krs_data = calculate_krs(creation, transfer)
            assert krs_data["krs_level"] == expected_level, \
                f"Creation={creation}, Transfer={transfer} should yield {expected_level}"
        
        print("✅ Test 8: KRS boundary conditions validated")
    
    def test_contact_quality_boundaries(self):
        """Test contact quality classification boundaries"""
        test_cases = [
            (120.0, "EXCELLENT"),
            (110.0, "EXCELLENT"),
            (109.9, "SOLID"),
            (100.0, "SOLID"),
            (99.9, "FAIR"),
            (90.0, "FAIR"),
            (89.9, "POOR"),
            (80.0, "POOR")
        ]
        
        for efficiency, expected_quality in test_cases:
            coach_data = {
                "bat_speed_mph": 80.0,
                "exit_velocity_mph": 95.0,
                "efficiency_percent": efficiency,
                "tempo_score": 85.0,
                "stability_score": 90.0,
                "gew_overall": 87.0,
                "motor_profile": {"type": "TEST", "confidence": 90}
            }
            
            report = transform_coach_rick_to_report(coach_data, f"quality_{efficiency}", 1)
            assert report["ball_contact_quality"] == expected_quality, \
                f"Efficiency {efficiency}% should yield {expected_quality}"
        
        print("✅ Test 9: Contact quality boundaries validated")
    
    def test_on_table_gain_edge_cases(self):
        """Test on-table gain calculation edge cases"""
        from krs_calculator import calculate_on_table_gain
        
        # Case 1: Perfect transfer (100) - should return None or minimal gain
        gain1 = calculate_on_table_gain(95.0, 100.0, 100.0)
        assert gain1 is None or gain1["value"] < 0.5, "Perfect transfer should have no/minimal gain"
        
        # Case 2: Very low transfer - should have significant gain
        gain2 = calculate_on_table_gain(80.0, 100.0, 50.0)
        assert gain2 is not None
        assert gain2["value"] > 5.0, "Low transfer should have significant gain potential"
        
        # Case 3: Missing data - should return None
        gain3 = calculate_on_table_gain(None, 100.0, 85.0)
        assert gain3 is None, "Missing current_exit_velo should return None"
        
        print("✅ Test 10: On-table gain edge cases validated")
    
    def test_empty_dict_error_handling(self):
        """Test error handling for empty or invalid data"""
        # Empty dict will produce a report with default values, not raise error
        # This is by design - transformer is resilient
        report = transform_coach_rick_to_report({}, "error_001", 1)
        # Should have sensible defaults but may have None/0 values
        assert report["session_id"] == "error_001"
        assert report["player_id"] == 1
        
        print("✅ Test 11: Empty dict handled with defaults")
    
    def test_invalid_type_error_handling(self):
        """Test error handling for invalid data types"""
        with pytest.raises(ValueError):
            # String instead of dict should raise ValueError
            transform_coach_rick_to_report("invalid", "error_002", 1)
        
        print("✅ Test 12: Invalid type error handling validated")
    
    def test_duration_calculation_edge_cases(self):
        """Test duration calculation for various inputs"""
        test_cases = [
            (0, 0),      # No duration
            (30, 0),     # 30 seconds → 0 minutes
            (60, 1),     # 60 seconds → 1 minute
            (120, 2),    # 120 seconds → 2 minutes
            (90, 1)      # 90 seconds → 1 minute (integer division)
        ]
        
        for duration_seconds, expected_minutes in test_cases:
            coach_data = {
                "bat_speed_mph": 80.0,
                "exit_velocity_mph": 95.0,
                "efficiency_percent": 100.0,
                "tempo_score": 85.0,
                "stability_score": 90.0,
                "gew_overall": 87.0,
                "motor_profile": {"type": "TEST", "confidence": 90},
                "duration_seconds": duration_seconds
            }
            
            report = transform_coach_rick_to_report(coach_data, f"duration_{duration_seconds}", 1)
            assert report["duration_minutes"] == expected_minutes
        
        print("✅ Test 13: Duration calculation edge cases validated")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("EDGE CASE INTEGRATION TESTS")
    print("="*70 + "\n")
    
    test_suite = TestEdgeCases()
    
    # Run all tests
    test_suite.test_missing_optional_fields()
    test_suite.test_extreme_low_scores()
    test_suite.test_extreme_high_scores()
    test_suite.test_zero_confidence_motor_profile()
    test_suite.test_invalid_motor_profile_type()
    test_suite.test_missing_tempo_stability_fallback()
    test_suite.test_missing_efficiency_fallback()
    test_suite.test_krs_boundary_conditions()
    test_suite.test_contact_quality_boundaries()
    test_suite.test_on_table_gain_edge_cases()
    test_suite.test_empty_dict_error_handling()
    test_suite.test_invalid_type_error_handling()
    test_suite.test_duration_calculation_edge_cases()
    
    print("\n" + "="*70)
    print("✅ ALL 13 EDGE CASE TESTS PASSED!")
    print("="*70 + "\n")
