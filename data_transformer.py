"""
Catching Barrels - Data Transformer
====================================

Transforms Coach Rick API response into PlayerReport schema.

This module bridges the current API with the new Builder 2 spec.

Author: Builder 2
Date: 2025-12-25
"""

from datetime import datetime
from typing import Dict, Any, Optional
import uuid

from player_report_schema import (
    PlayerReport, PlayerInfo, Progress, KRSScore, Brain, Body, Bat, Ball,
    MotorProfile, Tempo, Capacity, Actual, OnTable, SubComponent,
    Flow, KineticChain, LeadLeg, Timing, AttackAngle,
    BallPerformance, Win, Mission, SecondaryIssue, Drill, Projection, Gains,
    CoachMessage, Flags, SpecialInsights, PowerParadox,
    MotorProfileType, KRSLevel, DataSource, Confidence, TempoCategory,
    Status, Priority, MissionCategory
)

from krs_calculator import calculate_full_krs_report


# ============================================================================
# MOTOR PROFILE MAPPING
# ============================================================================

MOTOR_PROFILE_CONFIG = {
    "Spinner": {
        "display_name": "THE SPINNER",
        "tagline": "Quick hands, short path. Let it fly.",
        "color": "#10B981",  # green
        "icon": "🌪️"
    },
    "Whipper": {
        "display_name": "THE WHIPPER",
        "tagline": "Explosive rotation. Stay connected.",
        "color": "#F59E0B",  # amber
        "icon": "⚡"
    },
    "Torquer": {
        "display_name": "THE TORQUER",
        "tagline": "Power from the ground up. Feel the force.",
        "color": "#EF4444",  # red
        "icon": "🔥"
    },
    "Twister": {
        "display_name": "THE TWISTER",
        "tagline": "Rotational power. Stay tight, spin fast.",
        "color": "#8B5CF6",  # purple
        "icon": "🌀"
    },
    "Tilter": {
        "display_name": "THE TILTER",
        "tagline": "Upper body tilt. Attack from above.",
        "color": "#3B82F6",  # blue
        "icon": "📐"
    },
    "Hybrid": {
        "display_name": "THE HYBRID",
        "tagline": "Blend of styles. Adapt and dominate.",
        "color": "#EC4899",  # pink
        "icon": "🎯"
    },
}


def get_status_from_score(score: float, score_type: str = "percentage") -> Status:
    """
    Convert numeric score to Status enum
    
    Args:
        score: Numeric score
        score_type: "percentage" (0-100) or "rating" (0-10)
        
    Returns:
        Status enum
    """
    if score_type == "rating":
        # Convert 0-10 to 0-100
        score = score * 10
    
    if score >= 85:
        return Status.ELITE
    elif score >= 70:
        return Status.GOOD
    elif score >= 50:
        return Status.NEEDS_WORK
    else:
        return Status.CRITICAL


# ============================================================================
# MAIN TRANSFORMER
# ============================================================================

def transform_to_player_report(
    coach_rick_response: Dict[str, Any],
    player_info: Dict[str, Any],
    session_count: int = 1,
    previous_session: Optional[Dict] = None,
) -> PlayerReport:
    """
    Transform Coach Rick API response to PlayerReport schema
    
    Args:
        coach_rick_response: Response from /api/v1/reboot-lite/analyze-with-coach
        player_info: Player biographical info
        session_count: Lifetime session count
        previous_session: Previous session data (for trends)
        
    Returns:
        Complete PlayerReport object
    """
    
    # ========================================
    # EXTRACT BASE DATA
    # ========================================
    
    session_id = coach_rick_response.get('session_id', str(uuid.uuid4()))
    player_id = player_info.get('player_id', str(uuid.uuid4()))
    
    # Player info
    player_name = player_info['name']
    age = player_info['age']
    height_inches = player_info['height_inches']
    weight_lbs = player_info['weight_lbs']
    wingspan_inches = player_info.get('wingspan_inches')
    
    # Calculate ape index if wingspan available
    ape_index = wingspan_inches - height_inches if wingspan_inches else None
    
    # Core metrics from response
    bat_speed_mph = coach_rick_response.get('bat_speed_mph', 70.0)
    exit_velocity_mph = coach_rick_response.get('exit_velocity_mph', 85.0)
    efficiency_percent = coach_rick_response.get('efficiency_percent', 75.0)
    tempo_score = coach_rick_response.get('tempo_score', 7.5)
    stability_score = coach_rick_response.get('stability_score', 7.0)
    gew_overall = coach_rick_response.get('gew_overall', 72.0)
    
    # Motor profile
    motor_profile_data = coach_rick_response.get('motor_profile', {})
    motor_type = motor_profile_data.get('type', 'Spinner')
    motor_confidence = motor_profile_data.get('confidence', 85.0)
    
    # Patterns
    patterns = coach_rick_response.get('patterns', [])
    primary_issue = coach_rick_response.get('primary_issue', 'General development')
    
    # Prescription
    prescription = coach_rick_response.get('prescription', {})
    drills_data = prescription.get('drills', [])
    
    # ========================================
    # CALCULATE KRS
    # ========================================
    
    # Estimate component scores from available data
    ground_flow_score = stability_score  # 0-10
    engine_flow_score = tempo_score  # 0-10
    kinetic_chain_score = efficiency_percent  # 0-100
    lead_leg_score = 75.0  # Default estimate
    timing_score = 80.0  # Default estimate
    
    # Get previous KRS if available
    prev_krs = previous_session.get('krs', {}).get('total') if previous_session else None
    prev_creation = previous_session.get('krs', {}).get('creation_score') if previous_session else None
    prev_transfer = previous_session.get('krs', {}).get('transfer_score') if previous_session else None
    
    # Calculate KRS
    krs_result = calculate_full_krs_report(
        ground_flow=ground_flow_score,
        engine_flow=engine_flow_score,
        kinetic_chain=kinetic_chain_score,
        lead_leg=lead_leg_score,
        timing=timing_score,
        bat_speed_mph=bat_speed_mph,
        player_height_inches=height_inches,
        player_weight_lbs=weight_lbs,
        wingspan_inches=wingspan_inches,
        previous_krs=prev_krs,
        previous_creation=prev_creation,
        previous_transfer=prev_transfer,
        data_source=DataSource.VIDEO_ANALYSIS,
    )
    
    # ========================================
    # BUILD PLAYER INFO
    # ========================================
    
    player = PlayerInfo(
        name=player_name,
        age=age,
        height_inches=height_inches,
        weight_lbs=weight_lbs,
        wingspan_inches=wingspan_inches,
        ape_index=ape_index,
    )
    
    # ========================================
    # BUILD PROGRESS
    # ========================================
    
    total_swings = session_count * 10  # Estimate 10 swings per session
    report_unlocked = total_swings >= 50
    swings_to_unlock = max(0, 50 - total_swings)
    
    progress = Progress(
        total_swings=total_swings,
        session_number=session_count,
        last_session_date=datetime.utcnow().isoformat(),
        week_streak=1,  # Default, would track in database
        days_since_last=0,
        report_unlocked=report_unlocked,
        swings_to_unlock=swings_to_unlock,
    )
    
    # ========================================
    # BUILD KRS
    # ========================================
    
    krs = KRSScore(
        total=krs_result['total'],
        level=krs_result['level'],
        emoji=krs_result['emoji'],
        points_to_next_level=krs_result['points_to_next_level'],
        creation_score=krs_result['creation_score'],
        transfer_score=krs_result['transfer_score'],
        krs_change=krs_result['krs_change'],
        creation_change=krs_result['creation_change'],
        transfer_change=krs_result['transfer_change'],
        data_source=krs_result['data_source'],
        confidence=krs_result['confidence'],
    )
    
    # ========================================
    # BUILD BRAIN (MOTOR PROFILE)
    # ========================================
    
    profile_config = MOTOR_PROFILE_CONFIG.get(motor_type, MOTOR_PROFILE_CONFIG['Spinner'])
    
    motor_profile = MotorProfile(
        primary=MotorProfileType(motor_type),
        primary_confidence=motor_confidence,
        secondary=None,
        display_name=profile_config['display_name'],
        tagline=profile_config['tagline'],
        color=profile_config['color'],
        icon=profile_config['icon'],
    )
    
    tempo_ratio = tempo_score / 2.5  # Convert 0-10 to ~0-4 ratio
    tempo_category = TempoCategory.FAST if tempo_ratio > 3.0 else (
        TempoCategory.BALANCED if tempo_ratio > 2.0 else TempoCategory.SLOW
    )
    
    tempo = Tempo(
        ratio=tempo_ratio,
        category=tempo_category,
        message=f"{tempo_category.value} tempo swing",
    )
    
    brain = Brain(
        motor_profile=motor_profile,
        tempo=tempo,
        pitch_watch=None,  # Would need pitch tracking data
    )
    
    # ========================================
    # BUILD BODY (CREATION)
    # ========================================
    
    capacity_speed = krs_result['capacity']['bat_speed_mph']
    on_table_data = krs_result['on_table']
    
    capacity = Capacity(
        capacity_ke_joules=150.0,  # Simplified
        capacity_bat_speed_mph=capacity_speed,
    )
    
    actual = Actual(
        peak_ke_joules=120.0,  # Simplified
        estimated_bat_speed_mph=bat_speed_mph,
    )
    
    on_table = OnTable(
        ke_gap_joules=30.0,  # Simplified
        bat_speed_gap_mph=on_table_data['gap_mph'],
    )
    
    ground_flow = SubComponent(
        score=ground_flow_score,
        status=get_status_from_score(ground_flow_score, "rating"),
    )
    
    engine_flow = SubComponent(
        score=engine_flow_score,
        status=get_status_from_score(engine_flow_score, "rating"),
    )
    
    body = Body(
        creation_score=krs.creation_score,
        capacity=capacity,
        actual=actual,
        on_table=on_table,
        ground_flow=ground_flow,
        engine_flow=engine_flow,
        gap_source=primary_issue if patterns else "General efficiency",
    )
    
    # ========================================
    # BUILD BAT (TRANSFER)
    # ========================================
    
    flow = Flow(
        you_create_mph=capacity_speed,
        reaches_barrel_mph=bat_speed_mph,
        on_table_mph=on_table_data['gap_mph'],
    )
    
    kinetic_chain = KineticChain(
        score=kinetic_chain_score,
        status=get_status_from_score(kinetic_chain_score, "percentage"),
        hip_momentum=None,  # Would need CSV data
        shoulder_momentum=None,
        sh_ratio=None,
        sequence=None,
    )
    
    lead_leg = LeadLeg(
        score=lead_leg_score,
        status=get_status_from_score(lead_leg_score, "percentage"),
        knee_extension_deg=None,  # Would need CSV data
        target_extension_deg=None,
        gap_deg=None,
    )
    
    timing = Timing(
        score=timing_score,
        status=get_status_from_score(timing_score, "percentage"),
    )
    
    attack_angle = AttackAngle(
        current_deg=10.0,  # Default estimate
        capacity_deg=15.0,
    )
    
    bat = Bat(
        transfer_score=krs.transfer_score,
        flow=flow,
        kinetic_chain=kinetic_chain,
        lead_leg=lead_leg,
        timing=timing,
        attack_angle=attack_angle,
        gap_source="Timing and sequencing" if patterns else "General transfer efficiency",
    )
    
    # ========================================
    # BUILD BALL (PROJECTIONS)
    # ========================================
    
    current_ball = BallPerformance(
        exit_velo_mph=exit_velocity_mph,
        launch_angle_deg=10.0,
        contact_quality="Line drive tendency",
    )
    
    capacity_ball = BallPerformance(
        exit_velo_mph=exit_velocity_mph + on_table_data['gap_mph'],
        launch_angle_deg=15.0,
        contact_quality="Consistent hard contact",
    )
    
    ball = Ball(
        current=current_ball,
        capacity=capacity_ball,
        total_on_table_mph=on_table_data['gap_mph'],
    )
    
    # ========================================
    # BUILD WINS
    # ========================================
    
    wins = []
    if bat_speed_mph > 70:
        wins.append(Win(
            metric="Bat Speed",
            score=f"{bat_speed_mph:.1f} mph",
            percentile=None,
            message="Above average bat speed for your age",
            icon="⚡",
        ))
    
    if tempo_score > 7:
        wins.append(Win(
            metric="Tempo",
            score=f"{tempo_score:.1f}/10",
            percentile=None,
            message="Excellent timing and rhythm",
            icon="⏱️",
        ))
    
    if efficiency_percent > 70:
        wins.append(Win(
            metric="Efficiency",
            score=f"{efficiency_percent:.0f}%",
            percentile=None,
            message="Good power transfer efficiency",
            icon="💪",
        ))
    
    # ========================================
    # BUILD MISSION
    # ========================================
    
    mission = Mission(
        title=primary_issue,
        category=MissionCategory.POWER if "power" in primary_issue.lower() else MissionCategory.BODY,
        priority=Priority.CRITICAL if patterns and patterns[0].get('severity') == 'HIGH' else Priority.MEDIUM,
        unlock=f"Unlock +{on_table_data['gap_mph']:.0f} mph bat speed",
        explanation=patterns[0].get('description', 'Focus on general skill development') if patterns else "Focus on general skill development",
        current_value=None,
        target_value=None,
        unit=None,
        gap=None,
        expected_fix_weeks=prescription.get('duration_weeks', 4),
    )
    
    # ========================================
    # BUILD DRILLS
    # ========================================
    
    drills = []
    for drill_data in drills_data[:3]:  # Max 3 drills
        drills.append(Drill(
            name=drill_data.get('name', 'Training Drill'),
            category=drill_data.get('category', 'General'),
            volume=drill_data.get('volume', '3 sets'),
            frequency=drill_data.get('frequency', 'Daily'),
            why_it_works="Addresses mechanical issue and builds proper patterns",
            key_cues=drill_data.get('key_cues', ['Focus', 'Stay connected', 'Feel the sequence']),
            addresses_issue=primary_issue,
            video_url=None,
            thumbnail_url=None,
        ))
    
    # ========================================
    # BUILD PROJECTION
    # ========================================
    
    projection = Projection(
        timeframe=f"{prescription.get('duration_weeks', 4)}-{prescription.get('duration_weeks', 4)+2} weeks",
        gains=Gains(
            bat_speed=f"+{on_table_data['gap_mph']:.0f} mph",
            exit_velocity=f"+{on_table_data['gap_mph']:.0f} mph",
            transfer_efficiency="+10-15%",
            krs_points=f"+{krs.points_to_next_level:.0f} points",
        ),
    )
    
    # ========================================
    # BUILD COACH MESSAGE
    # ========================================
    
    coach_messages_data = coach_rick_response.get('coach_messages', {})
    
    coach_message = CoachMessage(
        what_i_see=coach_messages_data.get('analysis', f"You're a {motor_type} with solid fundamentals.")[:200],
        your_mission=f"Fix {primary_issue.lower()} to unlock more power",
        signature="Trust the work. - Coach Rick",
    )
    
    # ========================================
    # BUILD FLAGS & SPECIAL INSIGHTS
    # ========================================
    
    flags = Flags(
        power_paradox=(on_table_data['gap_mph'] > 10),
        cricket_background=False,  # Would detect from patterns
        anthropometric_advantage=(ape_index > 2 if ape_index else False),
        rapid_improver=False,
    )
    
    special_insights = SpecialInsights()
    
    if flags.power_paradox:
        special_insights.power_paradox = PowerParadox(
            capacity_percentile=85.0,
            delivery_percentile=60.0,
            potential_gain_mph=on_table_data['gap_mph'],
            bottleneck=primary_issue,
        )
    
    # ========================================
    # BUILD COMPLETE REPORT
    # ========================================
    
    report = PlayerReport(
        session_id=session_id,
        player_id=player_id,
        session_date=datetime.utcnow().isoformat(),
        session_number=session_count,
        player=player,
        progress=progress,
        krs=krs,
        brain=brain,
        body=body,
        bat=bat,
        ball=ball,
        mission=mission,
        projection=projection,
        coach_message=coach_message,
        wins=wins,
        drills=drills,
        flags=flags,
        special_insights=special_insights,
    )
    
    return report


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Transform a sample Coach Rick response
    sample_response = {
        'session_id': 'test_123',
        'bat_speed_mph': 72.5,
        'exit_velocity_mph': 88.0,
        'efficiency_percent': 75.0,
        'tempo_score': 7.5,
        'stability_score': 7.0,
        'gew_overall': 72.0,
        'motor_profile': {
            'type': 'Spinner',
            'confidence': 85.0,
        },
        'patterns': [
            {
                'pattern_id': 'P1',
                'name': 'Early Extension',
                'description': 'Hips moving forward too early',
                'severity': 'HIGH',
            }
        ],
        'primary_issue': 'Early Extension',
        'prescription': {
            'duration_weeks': 4,
            'drills': [
                {
                    'name': 'Hip Hinge Drill',
                    'category': 'Hip Mechanics',
                    'volume': '3 sets × 10 reps',
                    'frequency': 'Daily',
                    'key_cues': ['Hinge back', 'Stay tall', 'Feel the load'],
                }
            ],
        },
        'coach_messages': {
            'analysis': 'Great bat speed! Work on staying back in the load.',
        },
    }
    
    player_info = {
        'player_id': 'player_001',
        'name': 'John Smith',
        'age': 24,
        'height_inches': 72,
        'weight_lbs': 185,
        'wingspan_inches': 74,
    }
    
    report = transform_to_player_report(sample_response, player_info, session_count=1)
    
    print("=" * 70)
    print("PLAYER REPORT TRANSFORMATION TEST")
    print("=" * 70)
    print(f"Player: {report.player.name}")
    print(f"Session: {report.session_number}")
    print(f"KRS: {report.krs.total} {report.krs.emoji} ({report.krs.level.value})")
    print(f"  Creation: {report.krs.creation_score}")
    print(f"  Transfer: {report.krs.transfer_score}")
    print(f"Motor Profile: {report.brain.motor_profile.display_name}")
    print(f"Mission: {report.mission.title}")
    print(f"Drills: {len(report.drills)}")
    print(f"Wins: {len(report.wins)}")
    print("=" * 70)
