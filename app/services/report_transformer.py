"""
Data Transformer: Coach Rick Analysis → PlayerReport Format
Phase 1 Week 3-4: Priority 4

Transforms Coach Rick AI analysis output into PlayerReport database format
with KRS scoring (0-100 scale) and 4B Framework metrics.
"""

from typing import Dict, Optional, Any
import logging
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from krs_calculator import calculate_krs, calculate_on_table_gain

logger = logging.getLogger(__name__)


def transform_coach_rick_to_report(
    coach_rick_data: Dict[str, Any],
    session_id: str,
    player_id: int
) -> Dict[str, Any]:
    """
    Transform Coach Rick analysis to PlayerReport format.
    
    Args:
        coach_rick_data: Raw output from Coach Rick API (/api/v1/reboot-lite/analyze-with-coach)
        session_id: Session UUID
        player_id: Player database ID
    
    Returns:
        Dictionary ready for PlayerReport(**data) creation
    
    Raises:
        ValueError: If required fields missing or invalid
        KeyError: If data structure doesn't match expected format
    
    Example:
        >>> coach_data = {
        ...     "bat_speed_mph": 82.0,
        ...     "exit_velocity_mph": 99.0,
        ...     "efficiency_percent": 111.0,
        ...     "motor_profile": {"type": "SLINGSHOTTER", "confidence": 92.0},
        ...     "tempo_score": 87.0,
        ...     "stability_score": 92.0,
        ...     "gew_overall": 88.5
        ... }
        >>> report = transform_coach_rick_to_report(coach_data, "sess_123", 1)
        >>> assert 0 <= report["krs_total"] <= 100
        >>> assert report["krs_level"] in ["FOUNDATION", "BUILDING", "DEVELOPING", "ADVANCED", "ELITE"]
    """
    try:
        # ============================================
        # VALIDATE INPUT DATA
        # ============================================
        if not isinstance(coach_rick_data, dict):
            raise ValueError(f"coach_rick_data must be dict, got {type(coach_rick_data)}")
        
        # ============================================
        # EXTRACT CORE METRICS
        # ============================================
        bat_speed_mph = coach_rick_data.get("bat_speed_mph", 0)
        exit_velocity_mph = coach_rick_data.get("exit_velocity_mph", 0)
        efficiency_percent = coach_rick_data.get("efficiency_percent", 0)
        
        tempo_score = coach_rick_data.get("tempo_score", 0)
        stability_score = coach_rick_data.get("stability_score", 0)
        gew_overall = coach_rick_data.get("gew_overall", 0)
        
        # ============================================
        # CALCULATE CREATION SCORE (0-100)
        # ============================================
        # Creation = ability to generate force/momentum
        # Based on: tempo_score, stability_score, efficiency (lower body mechanics)
        
        # Formula: Weighted average of tempo and stability
        # Higher tempo + stability = better force creation
        if tempo_score and stability_score:
            creation_score = (tempo_score * 0.6) + (stability_score * 0.4)
            creation_score = min(100, max(0, creation_score))  # Clamp 0-100
        else:
            logger.warning(f"Missing tempo/stability scores, using GEW fallback: {gew_overall}")
            creation_score = min(100, max(0, gew_overall))
        
        # ============================================
        # CALCULATE TRANSFER SCORE (0-100)
        # ============================================
        # Transfer = ability to transfer force to bat
        # Based on: efficiency_percent (how well force is converted to bat speed)
        
        # Efficiency is typically 80-120%, normalize to 0-100 scale
        if efficiency_percent:
            # 100% efficiency = 85 transfer score (good baseline)
            # Each 1% above/below 100% = ±0.75 points
            transfer_score = 85 + ((efficiency_percent - 100) * 0.75)
            transfer_score = min(100, max(0, transfer_score))
        else:
            logger.warning("Missing efficiency_percent, using default 70")
            transfer_score = 70.0
        
        # ============================================
        # CALCULATE KRS
        # ============================================
        krs_result = calculate_krs(creation_score, transfer_score)
        
        logger.info(
            f"KRS Calculation: Creation={creation_score:.1f}, Transfer={transfer_score:.1f}, "
            f"KRS={krs_result['krs_total']:.1f} ({krs_result['krs_level']})"
        )
        
        # ============================================
        # EXTRACT MOTOR PROFILE (BRAIN CARD)
        # ============================================
        motor_profile_data = coach_rick_data.get("motor_profile", {})
        
        motor_profile = motor_profile_data.get("type", "UNKNOWN")
        motor_confidence = motor_profile_data.get("confidence", 0)
        
        # Normalize motor profile names (SLINGSHOTTER → Slingshotter)
        motor_profile = motor_profile.capitalize() if motor_profile else "Unknown"
        
        # Calculate timing (load to contact time)
        # Derive from tempo_ratio if available
        hip_shoulder_gap = coach_rick_data.get("hip_shoulder_gap_ms", 20)
        hands_bat_gap = coach_rick_data.get("hands_bat_gap_ms", 15)
        timing = (hip_shoulder_gap + hands_bat_gap) / 1000.0  # Convert ms to seconds
        
        # ============================================
        # CALCULATE PHYSICAL CAPACITY (BODY CARD)
        # ============================================
        # Physical capacity = theoretical max exit velocity based on bat speed
        # Rule of thumb: Exit velo = bat speed × 1.2 (approximate)
        if bat_speed_mph:
            physical_capacity_mph = bat_speed_mph * 1.2
        else:
            physical_capacity_mph = exit_velocity_mph  # Fallback
        
        # Peak force approximation (based on exit velocity)
        # Rough estimate: 1 mph exit velo ~ 8 Newtons of force
        peak_force_n = exit_velocity_mph * 8 if exit_velocity_mph else 0
        
        # ============================================
        # CALCULATE ON-TABLE GAIN
        # ============================================
        gain_data = calculate_on_table_gain(
            current_exit_velo=exit_velocity_mph,
            physical_capacity=physical_capacity_mph,
            transfer_score=transfer_score
        )
        
        # ============================================
        # EXTRACT/CALCULATE BALL CARD METRICS
        # ============================================
        # Launch angle (estimate if not provided)
        launch_angle_deg = coach_rick_data.get("launch_angle", 15.0)
        
        # Contact quality based on efficiency
        if efficiency_percent >= 110:
            contact_quality = "EXCELLENT"
        elif efficiency_percent >= 100:
            contact_quality = "SOLID"
        elif efficiency_percent >= 90:
            contact_quality = "FAIR"
        else:
            contact_quality = "POOR"
        
        # ============================================
        # EXTRACT SESSION METADATA
        # ============================================
        frames_analyzed = coach_rick_data.get("frames_analyzed", 0)
        duration_seconds = coach_rick_data.get("duration_seconds", 0)
        
        # Estimate swing count (typically 1 swing per analysis)
        swing_count = 1
        
        # Session duration in minutes
        duration_minutes = int(duration_seconds / 60) if duration_seconds else 0
        
        # ============================================
        # BUILD PLAYER REPORT DICTIONARY
        # ============================================
        report_data = {
            # Identifiers
            "session_id": session_id,
            "player_id": player_id,
            
            # KRS Scores
            "krs_total": krs_result["krs_total"],
            "krs_level": krs_result["krs_level"],
            "creation_score": round(creation_score, 1),
            "transfer_score": round(transfer_score, 1),
            
            # On-Table Gain
            "on_table_gain_value": gain_data["value"] if gain_data else None,
            "on_table_gain_metric": gain_data["metric"] if gain_data else "mph",
            "on_table_gain_description": gain_data["description"] if gain_data else None,
            
            # 4B Framework - Brain (Motor Profile)
            "brain_motor_profile": motor_profile,
            "brain_confidence": round(motor_confidence, 0) if motor_confidence else None,
            "brain_timing": round(timing, 2),
            
            # 4B Framework - Body (Creation)
            "body_creation_score": round(creation_score, 1),
            "body_physical_capacity_mph": round(physical_capacity_mph, 0) if physical_capacity_mph else None,
            "body_peak_force_n": round(peak_force_n, 0) if peak_force_n else None,
            
            # 4B Framework - Bat (Transfer)
            "bat_transfer_score": round(transfer_score, 1),
            "bat_transfer_efficiency": round(efficiency_percent, 0) if efficiency_percent else None,
            "bat_attack_angle_deg": round(launch_angle_deg, 0) if launch_angle_deg else None,
            
            # 4B Framework - Ball (Outcomes)
            "ball_exit_velocity_mph": round(exit_velocity_mph, 0) if exit_velocity_mph else None,
            "ball_capacity_mph": round(physical_capacity_mph, 0) if physical_capacity_mph else None,
            "ball_launch_angle_deg": round(launch_angle_deg, 0) if launch_angle_deg else None,
            "ball_contact_quality": contact_quality,
            
            # Session Metadata
            "swing_count": swing_count,
            "duration_minutes": duration_minutes,
        }
        
        # Validate critical fields
        _validate_report_data(report_data)
        
        logger.info(
            f"✅ Transformed Coach Rick → PlayerReport: "
            f"KRS {report_data['krs_total']} ({report_data['krs_level']}), "
            f"Motor Profile: {motor_profile}, "
            f"Exit Velo: {exit_velocity_mph} mph"
        )
        
        return report_data
        
    except KeyError as e:
        logger.error(f"Missing required field in Coach Rick data: {e}")
        raise ValueError(f"Invalid Coach Rick data structure: missing {e}")
    except Exception as e:
        logger.error(f"Error transforming Coach Rick data: {e}")
        raise ValueError(f"Failed to transform Coach Rick data: {str(e)}")


def _validate_report_data(report_data: Dict[str, Any]) -> None:
    """
    Validate transformed report data before database insertion.
    
    Args:
        report_data: Transformed report dictionary
    
    Raises:
        ValueError: If validation fails
    """
    # Required fields
    required_fields = [
        "session_id", "player_id",
        "krs_total", "krs_level",
        "creation_score", "transfer_score"
    ]
    
    for field in required_fields:
        if field not in report_data:
            raise ValueError(f"Missing required field: {field}")
        if report_data[field] is None:
            raise ValueError(f"Field cannot be None: {field}")
    
    # Validate KRS range
    if not (0 <= report_data["krs_total"] <= 100):
        raise ValueError(f"krs_total out of range: {report_data['krs_total']}")
    
    # Validate KRS level
    valid_levels = ["FOUNDATION", "BUILDING", "DEVELOPING", "ADVANCED", "ELITE"]
    if report_data["krs_level"] not in valid_levels:
        raise ValueError(f"Invalid krs_level: {report_data['krs_level']}")
    
    # Validate Creation/Transfer range
    if not (0 <= report_data["creation_score"] <= 100):
        raise ValueError(f"creation_score out of range: {report_data['creation_score']}")
    if not (0 <= report_data["transfer_score"] <= 100):
        raise ValueError(f"transfer_score out of range: {report_data['transfer_score']}")
    
    logger.debug("✅ Report data validation passed")


def extract_creation_score(coach_rick_data: Dict[str, Any]) -> float:
    """
    Extract Creation score from Coach Rick data.
    Returns value 0-100.
    
    Creation = ability to generate force/momentum.
    Based on tempo_score and stability_score.
    """
    tempo_score = coach_rick_data.get("tempo_score", 0)
    stability_score = coach_rick_data.get("stability_score", 0)
    gew_overall = coach_rick_data.get("gew_overall", 0)
    
    if tempo_score and stability_score:
        creation = (tempo_score * 0.6) + (stability_score * 0.4)
        return min(100, max(0, creation))
    else:
        return min(100, max(0, gew_overall))


def extract_transfer_score(coach_rick_data: Dict[str, Any]) -> float:
    """
    Extract Transfer score from Coach Rick data.
    Returns value 0-100.
    
    Transfer = ability to transfer force to bat.
    Based on efficiency_percent.
    """
    efficiency_percent = coach_rick_data.get("efficiency_percent", 0)
    
    if efficiency_percent:
        # 100% efficiency = 85 transfer score
        transfer = 85 + ((efficiency_percent - 100) * 0.75)
        return min(100, max(0, transfer))
    else:
        return 70.0  # Default


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("REPORT TRANSFORMER - UNIT TESTS")
    print("="*70)
    
    # Test Case 1: Complete Coach Rick data
    test_data_complete = {
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
    
    print("\nTest 1: Complete Coach Rick data")
    report1 = transform_coach_rick_to_report(test_data_complete, "test_sess_1", 1)
    print(f"  KRS: {report1['krs_total']} ({report1['krs_level']})")
    print(f"  Creation: {report1['creation_score']}, Transfer: {report1['transfer_score']}")
    print(f"  Motor Profile: {report1['brain_motor_profile']} (confidence: {report1['brain_confidence']}%)")
    print(f"  Exit Velocity: {report1['ball_exit_velocity_mph']} mph")
    assert 0 <= report1["krs_total"] <= 100, "KRS out of range"
    assert report1["krs_level"] in ["FOUNDATION", "BUILDING", "DEVELOPING", "ADVANCED", "ELITE"]
    print("  ✅ PASS")
    
    # Test Case 2: Minimal data (missing optional fields)
    test_data_minimal = {
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
    
    print("\nTest 2: Minimal data (missing optional fields)")
    report2 = transform_coach_rick_to_report(test_data_minimal, "test_sess_2", 1)
    print(f"  KRS: {report2['krs_total']} ({report2['krs_level']})")
    print(f"  Creation: {report2['creation_score']}, Transfer: {report2['transfer_score']}")
    assert report2["krs_total"] is not None
    assert report2["brain_motor_profile"] == "Spinner"
    print("  ✅ PASS")
    
    # Test Case 3: High performance player
    test_data_elite = {
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
    
    print("\nTest 3: Elite player (high scores)")
    report3 = transform_coach_rick_to_report(test_data_elite, "test_sess_3", 1)
    print(f"  KRS: {report3['krs_total']} ({report3['krs_level']})")
    assert report3["krs_total"] >= 85, "Elite player should have KRS >= 85"
    assert report3["krs_level"] == "ELITE"
    assert report3["ball_contact_quality"] == "EXCELLENT"
    print("  ✅ PASS")
    
    print("\n" + "="*70)
    print("✅ ALL TESTS PASSED!")
    print("="*70 + "\n")
