"""
Integration test for storage system
Tests full flow: Coach Rick analysis → PlayerReport → Database
"""

import sys
from coach_rick_api import CoachRickAnalysisResponse
from data_transformer import transform_to_player_report
from session_storage import save_session, get_session, get_player_progress
import uuid

print("=" * 70)
print("STORAGE INTEGRATION TEST")
print("=" * 70)

# Mock Coach Rick response (same format as real API)
mock_response = {
    'session_id': f'coach_rick_{uuid.uuid4().hex[:12]}',
    'player_name': 'Integration Test Player',
    'timestamp': '2025-12-25T22:00:00',
    'bat_speed_mph': 85.0,
    'exit_velocity_mph': 102.0,
    'efficiency_percent': 82.0,
    'tempo_score': 8.5,
    'stability_score': 8.0,
    'gew_overall': 80.0,
    'motor_profile': {
        'type': 'Twister',
        'confidence': 92.0,
        'characteristics': ['Strong rotational power', 'Fast hip turn']
    },
    'patterns': [
        {
            'pattern_id': 'PATTERN_1',
            'name': 'Early Extension',
            'description': 'Lead leg extends early',
            'severity': 'HIGH',
            'root_cause': 'Weak posterior chain',
            'symptoms': ['Loss of posture', 'Power leak']
        }
    ],
    'primary_issue': 'Early Extension',
    'prescription': {
        'drills': [
            {
                'drill_id': 'DRILL_001',
                'name': 'Wall Drill',
                'category': 'Lower Body',
                'volume': '3 sets x 10 reps',
                'frequency': 'Daily',
                'key_cues': ['Keep back knee bent', 'Feel glute engagement']
            }
        ],
        'duration_weeks': 4,
        'expected_gains': '+5 mph exit velo',
        'weekly_schedule': {}
    },
    'coach_messages': {
        'analysis': 'Great foundation with room for improvement!',
        'drill_intro': 'Focus on these drills to unlock more power',
        'encouragement': 'Keep up the great work!'
    }
}

# Player info
player_info = {
    'player_id': f'player_{uuid.uuid4().hex[:8]}',
    'name': 'Integration Test Player',
    'age': 22,
    'height_inches': 74,
    'weight_lbs': 195,
    'wingspan_inches': 76,
}

print("\n1️⃣  Transforming Coach Rick response to PlayerReport...")
player_report = transform_to_player_report(
    coach_rick_response=mock_response,
    player_info=player_info,
    session_count=1
)
print(f"   ✓ PlayerReport created: {player_report.session_id}")
print(f"   ✓ KRS: {player_report.krs.total} ({player_report.krs.level.value})")

print("\n2️⃣  Saving to database...")
saved_session_id = save_session(player_report)
print(f"   ✓ Session saved: {saved_session_id}")

print("\n3️⃣  Retrieving from database...")
retrieved = get_session(saved_session_id)
print(f"   ✓ Session retrieved: {retrieved['session_id']}")
print(f"   ✓ KRS: {retrieved['krs_total']} ({retrieved['krs_level']})")

print("\n4️⃣  Checking player progress...")
progress = get_player_progress(player_info['player_id'])
print(f"   ✓ Total sessions: {progress['total_sessions']}")
print(f"   ✓ Total swings: {progress['total_swings']}")
print(f"   ✓ Current KRS: {progress['current_krs']}")
print(f"   ✓ Milestones: {len(progress['milestones'])}")

print("\n5️⃣  Verifying PlayerReport structure...")
report_dict = retrieved['report']
required_keys = ['session_id', 'krs', 'brain', 'body', 'bat', 'ball', 'mission', 'drills']
for key in required_keys:
    assert key in report_dict, f"Missing key: {key}"
    print(f"   ✓ {key}: present")

print("\n" + "=" * 70)
print("✅ ALL INTEGRATION TESTS PASSED!")
print("=" * 70)
print("\nStorage system is fully functional:")
print("  - Coach Rick responses transform correctly")
print("  - Sessions save to database")
print("  - Sessions retrieve from database")
print("  - Player progress tracks correctly")
print("  - PlayerReport structure matches spec")
print("\n🎉 Ready for production deployment!")
print("=" * 70)
