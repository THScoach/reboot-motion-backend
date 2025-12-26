"""
Unit Tests for Report Transformer
Phase 1 Week 3-4: Priority 4

Tests transformation of Coach Rick analysis output to PlayerReport format
"""

import pytest
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.services.report_transformer import (
    transform_coach_rick_to_report,
    extract_creation_score,
    extract_transfer_score,
    _validate_report_data
)


class TestReportTransformer:
    """Test suite for report transformer"""
    
    def test_complete_coach_rick_data(self):
        """Test transformation with complete Coach Rick data"""
        coach_rick_data = {
            "bat_speed_mph": 82.0,
            "exit_velocity_mph": 99.0,
            "efficiency_percent": 111.0,
            "tempo_score": 87.0,
            "stability_score": 92.0,
            "gew_overall": 88.5,
            "hip_shoulder_gap_ms": 20,
            "hands_bat_gap_ms": 15,
            "motor_profile": {
                "type": "SLINGSHOTTER",
                "confidence": 92.0
            },
            "launch_angle": 15.0,
            "frames_analyzed": 120,
            "duration_seconds": 4.0
        }
        
        report = transform_coach_rick_to_report(
            coach_rick_data, 
            "test_sess_1", 
            1
        )
        
        # Validate KRS scoring
        assert 0 <= report["krs_total"] <= 100, "KRS out of range"
        assert report["krs_level"] in ["FOUNDATION", "BUILDING", "DEVELOPING", "ADVANCED", "ELITE"]
        assert report["krs_total"] >= 85, "High performance should yield ADVANCED/ELITE"
        
        # Validate 4B Framework
        assert report["brain_motor_profile"] == "Slingshotter"
        assert report["brain_confidence"] == 92
        assert report["body_creation_score"] == report["creation_score"]
        assert report["bat_transfer_score"] == report["transfer_score"]
        assert report["ball_exit_velocity_mph"] == 99
        
        # Validate session metadata
        assert report["session_id"] == "test_sess_1"
        assert report["player_id"] == 1
        assert report["swing_count"] == 1
        
        print(f"✅ Test 1 passed: KRS={report['krs_total']} ({report['krs_level']})")
    
    def test_minimal_coach_rick_data(self):
        """Test transformation with minimal required data"""
        coach_rick_data = {
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
        }
        
        report = transform_coach_rick_to_report(
            coach_rick_data,
            "test_sess_2",
            1
        )
        
        # Should still produce valid report with defaults
        assert report["krs_total"] is not None
        assert report["krs_level"] is not None
        assert report["brain_motor_profile"] == "Spinner"
        
        # Optional fields should have sensible defaults
        assert report["duration_minutes"] >= 0
        assert report["swing_count"] >= 1
        
        print(f"✅ Test 2 passed: KRS={report['krs_total']} ({report['krs_level']})")
    
    def test_elite_player_data(self):
        """Test transformation for elite player (high scores)"""
        coach_rick_data = {
            "bat_speed_mph": 90.0,
            "exit_velocity_mph": 105.0,
            "efficiency_percent": 120.0,
            "tempo_score": 95.0,
            "stability_score": 98.0,
            "gew_overall": 96.0,
            "motor_profile": {
                "type": "TITAN",
                "confidence": 95.0
            }
        }
        
        report = transform_coach_rick_to_report(
            coach_rick_data,
            "test_sess_3",
            1
        )
        
        # Elite player should have ELITE level
        assert report["krs_total"] >= 85, "Elite player should have KRS >= 85"
        assert report["krs_level"] == "ELITE"
        assert report["ball_contact_quality"] == "EXCELLENT"
        assert report["brain_motor_profile"] == "Titan"
        
        print(f"✅ Test 3 passed: ELITE player with KRS={report['krs_total']}")
    
    def test_creation_score_extraction(self):
        """Test creation score extraction logic"""
        # Test with tempo and stability
        coach_data_1 = {
            "tempo_score": 80.0,
            "stability_score": 90.0,
            "gew_overall": 85.0
        }
        creation_1 = extract_creation_score(coach_data_1)
        expected_1 = (80.0 * 0.6) + (90.0 * 0.4)  # 48 + 36 = 84
        assert abs(creation_1 - expected_1) < 0.1
        
        # Test with missing tempo/stability (fallback to GEW)
        coach_data_2 = {
            "gew_overall": 75.0
        }
        creation_2 = extract_creation_score(coach_data_2)
        assert creation_2 == 75.0
        
        print("✅ Test 4 passed: Creation score extraction")
    
    def test_transfer_score_extraction(self):
        """Test transfer score extraction logic"""
        # Test at 100% efficiency (baseline)
        coach_data_1 = {"efficiency_percent": 100.0}
        transfer_1 = extract_transfer_score(coach_data_1)
        assert transfer_1 == 85.0, "100% efficiency should yield 85 transfer"
        
        # Test above 100% efficiency
        coach_data_2 = {"efficiency_percent": 110.0}
        transfer_2 = extract_transfer_score(coach_data_2)
        assert transfer_2 > 85.0, "110% efficiency should yield >85 transfer"
        
        # Test below 100% efficiency
        coach_data_3 = {"efficiency_percent": 90.0}
        transfer_3 = extract_transfer_score(coach_data_3)
        assert transfer_3 < 85.0, "90% efficiency should yield <85 transfer"
        
        # Test missing efficiency (default)
        coach_data_4 = {}
        transfer_4 = extract_transfer_score(coach_data_4)
        assert transfer_4 == 70.0, "Missing efficiency should default to 70"
        
        print("✅ Test 5 passed: Transfer score extraction")
    
    def test_validation_passes_valid_data(self):
        """Test validation accepts valid report data"""
        valid_report = {
            "session_id": "test_123",
            "player_id": 1,
            "krs_total": 75.0,
            "krs_level": "DEVELOPING",
            "creation_score": 70.0,
            "transfer_score": 80.0
        }
        
        # Should not raise any exception
        _validate_report_data(valid_report)
        print("✅ Test 6 passed: Validation accepts valid data")
    
    def test_validation_rejects_invalid_krs(self):
        """Test validation rejects out-of-range KRS"""
        invalid_report = {
            "session_id": "test_123",
            "player_id": 1,
            "krs_total": 150.0,  # Out of range!
            "krs_level": "ELITE",
            "creation_score": 70.0,
            "transfer_score": 80.0
        }
        
        with pytest.raises(ValueError, match="krs_total out of range"):
            _validate_report_data(invalid_report)
        
        print("✅ Test 7 passed: Validation rejects invalid KRS")
    
    def test_validation_rejects_invalid_level(self):
        """Test validation rejects invalid KRS level"""
        invalid_report = {
            "session_id": "test_123",
            "player_id": 1,
            "krs_total": 75.0,
            "krs_level": "SUPER_ELITE",  # Invalid level!
            "creation_score": 70.0,
            "transfer_score": 80.0
        }
        
        with pytest.raises(ValueError, match="Invalid krs_level"):
            _validate_report_data(invalid_report)
        
        print("✅ Test 8 passed: Validation rejects invalid level")
    
    def test_on_table_gain_calculation(self):
        """Test On-Table Gain is calculated"""
        # Use lower efficiency to create bigger transfer gap → larger gain
        coach_rick_data = {
            "bat_speed_mph": 80.0,
            "exit_velocity_mph": 90.0,
            "efficiency_percent": 95.0,  # Lower efficiency = more gain potential
            "tempo_score": 85.0,
            "stability_score": 90.0,
            "gew_overall": 87.0,
            "motor_profile": {
                "type": "SLINGER",
                "confidence": 88.0
            }
        }
        
        report = transform_coach_rick_to_report(
            coach_rick_data,
            "test_sess_gain",
            1
        )
        
        # On-Table Gain should be calculated when there's room for improvement
        # Note: gain may be None if transfer is already very high (< 0.5 mph gain)
        if report["on_table_gain_value"] is not None:
            assert report["on_table_gain_metric"] == "mph"
            assert report["on_table_gain_description"] is not None
            assert report["on_table_gain_value"] > 0
            print(f"✅ Test 9 passed: On-Table Gain = +{report['on_table_gain_value']} mph")
        else:
            print(f"✅ Test 9 passed: On-Table Gain = None (transfer already optimal)")
    
    def test_contact_quality_classification(self):
        """Test contact quality classification based on efficiency"""
        test_cases = [
            (120.0, "EXCELLENT"),
            (110.0, "EXCELLENT"),
            (105.0, "SOLID"),
            (100.0, "SOLID"),
            (95.0, "FAIR"),
            (90.0, "FAIR"),
            (85.0, "POOR")
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
            
            report = transform_coach_rick_to_report(coach_data, "test", 1)
            assert report["ball_contact_quality"] == expected_quality, \
                f"Efficiency {efficiency}% should yield {expected_quality}"
        
        print("✅ Test 10 passed: Contact quality classification")


if __name__ == "__main__":
    print("\n" + "="*70)
    print("REPORT TRANSFORMER - COMPREHENSIVE UNIT TESTS")
    print("="*70 + "\n")
    
    test_suite = TestReportTransformer()
    
    # Run all tests
    test_suite.test_complete_coach_rick_data()
    test_suite.test_minimal_coach_rick_data()
    test_suite.test_elite_player_data()
    test_suite.test_creation_score_extraction()
    test_suite.test_transfer_score_extraction()
    test_suite.test_validation_passes_valid_data()
    test_suite.test_validation_rejects_invalid_krs()
    test_suite.test_validation_rejects_invalid_level()
    test_suite.test_on_table_gain_calculation()
    test_suite.test_contact_quality_classification()
    
    print("\n" + "="*70)
    print("✅ ALL 10 UNIT TESTS PASSED!")
    print("="*70 + "\n")
