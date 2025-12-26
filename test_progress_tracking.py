#!/usr/bin/env python3
"""
Test Priority 7: Database & Progress Tracking
Validates progress tracker and session comparison functionality
"""

import sys
from datetime import datetime, timedelta
from typing import List, Dict


# Mock database class for testing
class MockDatabase:
    """
    Mock database connection for testing without actual database
    """
    
    def __init__(self):
        self.base_data: List[tuple] = []
        self.data: List[tuple] = []
        self.columns: List[str] = []
        self.last_query = ""
        self._create_sample_data()
    
    def _create_sample_data(self):
        """
        Create 5 sample sessions for Eric Williams showing improvement
        """
        base_date = datetime.now() - timedelta(days=90)
        
        # Store base data
        self.base_data = [
            # Session 1: Baseline (90 days ago)
            (
                1,  # id
                base_date,  # analysis_date
                57.9,  # bat_speed_actual_mph
                76.0,  # bat_speed_potential_mph
                18.1,  # bat_speed_gap_mph
                76.2,  # pct_potential_achieved
                72.0,  # ground_score
                85.0,  # engine_score
                40.0,  # weapon_score
                65.7,  # overall_efficiency
                'SPINNER',  # motor_profile
                73.6,  # motor_profile_confidence
                'WEAPON',  # weakest_component
                7.2,  # estimated_gain_mph
                10.8,  # total_estimated_gain_mph
                'Eric Williams',  # player_name
                'WEAPON',  # primary_focus_component
            ),
            # Session 2: After 2 weeks
            (
                2, base_date + timedelta(days=14),
                59.2, 76.0, 16.8, 77.9, 74.0, 86.0, 43.0, 67.7,
                'SPINNER', 75.0, 'WEAPON', 6.5, 9.8,
                'Eric Williams', 'WEAPON'
            ),
            # Session 3: After 1 month
            (
                3, base_date + timedelta(days=30),
                60.8, 76.0, 15.2, 80.0, 76.0, 87.0, 47.0, 70.0,
                'SPINNER', 76.5, 'WEAPON', 5.8, 8.9,
                'Eric Williams', 'WEAPON'
            ),
            # Session 4: After 2 months
            (
                4, base_date + timedelta(days=60),
                62.5, 76.0, 13.5, 82.2, 79.0, 88.0, 51.0, 72.7,
                'BALANCED', 68.0, 'WEAPON', 5.0, 7.8,
                'Eric Williams', 'WEAPON'
            ),
            # Session 5: Latest
            (
                5, datetime.now(),
                64.1, 76.0, 11.9, 84.3, 81.0, 89.0, 54.0, 74.7,
                'BALANCED', 70.5, 'WEAPON', 4.2, 6.9,
                'Eric Williams', 'WEAPON'
            )
        ]
        self.data = list(self.base_data)  # Copy
    
    def cursor(self):
        """Return self as cursor"""
        return self
    
    def execute(self, query: str, params: tuple = ()):
        """Mock execute - return relevant data based on query"""
        self.last_query = query.lower()
        
        # Parse query to return appropriate subset
        if 'ground_score' in self.last_query:
            # Return only date and ground_score columns
            self.data = [(row[1], row[6]) for row in self.data]  # date, ground_score
        elif 'engine_score' in self.last_query:
            self.data = [(row[1], row[7]) for row in self.data]  # date, engine_score
        elif 'weapon_score' in self.last_query:
            self.data = [(row[1], row[8]) for row in self.data]  # date, weapon_score
        elif 'bat_speed_gap_mph' in self.last_query:
            self.data = [(row[1], row[4]) for row in self.data]  # date, gap
        elif 'bat_speed_actual_mph' in self.last_query:
            self.data = [(row[1], row[2]) for row in self.data]  # date, actual bat speed
        # Otherwise keep full data for history and comparison queries
        
        return self
    
    def fetchall(self):
        """Return all data"""
        return self.data
    
    def fetchone(self):
        """Return first row"""
        return self.data[0] if self.data else None
    
    @property
    def description(self):
        """Mock column descriptions"""
        # Return appropriate columns based on last query
        if 'SELECT *' in self.last_query.upper() or 'id,' in self.last_query or 'WHERE id IN' in self.last_query:
            # Full columns for comparison query
            return [
                ('id',), ('analysis_date',), ('player_name',),
                ('bat_speed_actual_mph',), ('bat_speed_potential_mph',),
                ('bat_speed_gap_mph',), ('pct_potential_achieved',),
                ('ground_score',), ('engine_score',), ('weapon_score',),
                ('overall_efficiency',), ('motor_profile',),
                ('motor_profile_confidence',), ('weakest_component',),
                ('primary_focus_component',), ('estimated_gain_mph',),
                ('total_estimated_gain_mph',)
            ]
        else:
            # For history query
            return [
                ('id',), ('analysis_date',), ('bat_speed_actual_mph',),
                ('bat_speed_potential_mph',), ('bat_speed_gap_mph',),
                ('pct_potential_achieved',), ('ground_score',),
                ('engine_score',), ('weapon_score',),
                ('overall_efficiency',), ('motor_profile',),
                ('motor_profile_confidence',), ('weakest_component',),
                ('estimated_gain_mph',), ('total_estimated_gain_mph',)
            ]


def test_files_exist():
    """Test 1: Verify all required files exist"""
    print("=" * 80)
    print("TEST 1: FILE EXISTENCE")
    print("=" * 80)
    
    import os
    from pathlib import Path
    
    files = {
        'Database Migration': 'migrations/add_analysis_tracking.sql',
        'Progress Tracker': 'physics_engine/progress_tracker.py',
        'Session Comparison': 'physics_engine/session_comparison.py',
    }
    
    all_exist = True
    for name, path in files.items():
        full_path = Path(path)
        exists = full_path.exists()
        size = full_path.stat().st_size if exists else 0
        print(f"✓ {name}: {path}")
        print(f"  - Exists: {'YES ✓' if exists else 'NO ✗'}")
        print(f"  - Size: {size:,} bytes ({size/1024:.1f} KB)")
        if not exists:
            all_exist = False
    
    return all_exist


def test_import_modules():
    """Test 2: Import and instantiate modules"""
    print("\n" + "=" * 80)
    print("TEST 2: MODULE IMPORTS")
    print("=" * 80)
    
    try:
        from physics_engine.progress_tracker import ProgressTracker
        from physics_engine.session_comparison import SessionComparison
        
        print("✓ ProgressTracker imported successfully")
        print("✓ SessionComparison imported successfully")
        
        # Test instantiation
        db = MockDatabase()
        tracker = ProgressTracker(db)
        comparison = SessionComparison(db)
        
        print("✓ ProgressTracker instantiated successfully")
        print("✓ SessionComparison instantiated successfully")
        
        return True, tracker, comparison, db
        
    except Exception as e:
        print(f"✗ Import failed: {e}")
        return False, None, None, None


def test_get_history(tracker, db):
    """Test 3: Get player history"""
    print("\n" + "=" * 80)
    print("TEST 3: PLAYER HISTORY")
    print("=" * 80)
    
    try:
        history = tracker.get_player_history(player_id=1, limit=5)
        
        print(f"✓ Retrieved {len(history)} sessions")
        
        if len(history) > 0:
            print(f"\n  Session 1 (Oldest):")
            print(f"    Date: {history[-1]['date']}")
            print(f"    Bat Speed: {history[-1]['bat_speed_actual']} mph")
            print(f"    Ground: {history[-1]['ground_score']}, Engine: {history[-1]['engine_score']}, Weapon: {history[-1]['weapon_score']}")
            
            print(f"\n  Session {len(history)} (Latest):")
            print(f"    Date: {history[0]['date']}")
            print(f"    Bat Speed: {history[0]['bat_speed_actual']} mph")
            print(f"    Ground: {history[0]['ground_score']}, Engine: {history[0]['engine_score']}, Weapon: {history[0]['weapon_score']}")
        
        return len(history) == 5
        
    except Exception as e:
        print(f"✗ History test failed: {e}")
        return False


def test_calculate_progress(tracker):
    """Test 4: Calculate progress for bat speed"""
    print("\n" + "=" * 80)
    print("TEST 4: PROGRESS CALCULATION")
    print("=" * 80)
    
    try:
        progress = tracker.calculate_progress(player_id=1, metric='bat_speed_actual_mph')
        
        if 'error' in progress:
            print(f"✗ Progress calculation error: {progress['error']}")
            return False
        
        print(f"✓ Progress calculated successfully")
        print(f"\n  Metric: {progress['metric_name']}")
        print(f"  First Session:")
        print(f"    Date: {progress['first_session']['date']}")
        print(f"    Value: {progress['first_session']['value']} mph")
        print(f"  Latest Session:")
        print(f"    Date: {progress['latest_session']['date']}")
        print(f"    Value: {progress['latest_session']['value']} mph")
        print(f"\n  📈 Improvement: {progress['improvement']:+.1f} mph ({progress['pct_improvement']:+.1f}%)")
        print(f"  📊 Trend: {progress['trend']}")
        print(f"  🔄 Sessions: {progress['sessions_count']}")
        print(f"  📅 Rate: {progress['improvement_rate_per_week']:+.2f} mph/week")
        
        # Verify improvement
        assert progress['improvement'] > 0, "Should show improvement"
        assert progress['trend'] == 'IMPROVING', "Trend should be IMPROVING"
        assert progress['sessions_count'] == 5, "Should have 5 sessions"
        
        return True
        
    except Exception as e:
        print(f"✗ Progress calculation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_component_progress(tracker):
    """Test 5: Get component progress (Ground/Engine/Weapon)"""
    print("\n" + "=" * 80)
    print("TEST 5: COMPONENT PROGRESS")
    print("=" * 80)
    
    try:
        comp_progress = tracker.get_component_progress(player_id=1)
        
        print(f"✓ Component progress calculated")
        print(f"\n  📊 GROUND:")
        print(f"    Improvement: {comp_progress['ground']['improvement']:+.1f} points")
        print(f"    Trend: {comp_progress['ground']['trend']}")
        
        print(f"\n  ⚙️  ENGINE:")
        print(f"    Improvement: {comp_progress['engine']['improvement']:+.1f} points")
        print(f"    Trend: {comp_progress['engine']['trend']}")
        
        print(f"\n  🔫 WEAPON:")
        print(f"    Improvement: {comp_progress['weapon']['improvement']:+.1f} points")
        print(f"    Trend: {comp_progress['weapon']['trend']}")
        
        print(f"\n  🌟 Most Improved: {comp_progress['most_improved']} ({comp_progress['most_improved_gain']:+.1f} points)")
        print(f"  🎯 Needs Focus: {comp_progress['needs_focus']} (score: {comp_progress['needs_focus_score']})")
        print(f"  📈 Overall Trend: {comp_progress['overall_trend']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Component progress failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_session_comparison(comparison):
    """Test 6: Compare multiple sessions"""
    print("\n" + "=" * 80)
    print("TEST 6: SESSION COMPARISON")
    print("=" * 80)
    
    try:
        # Compare session 1, 3, and 5 (baseline, midpoint, latest)
        result = comparison.compare_sessions([1, 3, 5])
        
        if 'error' in result:
            print(f"✗ Comparison error: {result['error']}")
            return False
        
        print(f"✓ Compared {result['summary']['total_sessions']} sessions")
        print(f"\n  Player: {result['summary']['player_name']}")
        print(f"  Date Range: {result['summary']['date_range']}")
        print(f"  Days Elapsed: {result['summary']['days_elapsed']}")
        print(f"  Overall Trend: {result['summary']['overall_trend']}")
        
        print(f"\n  📊 KEY CHANGES:")
        for metric_key, data in result['changes'].items():
            if abs(data['change']) > 0.1:  # Only show significant changes
                direction_icon = "📈" if data['direction'] == 'IMPROVED' else "📉" if data['direction'] == 'DECLINED' else "➡️"
                print(f"    {direction_icon} {data['label']}: {data['first']} → {data['latest']} ({data['change']:+.1f}, {data['pct_change']:+.1f}%)")
        
        print(f"\n  🌟 Biggest Improvement: {result['summary']['biggest_improvement']}")
        if result['summary']['biggest_decline']:
            print(f"  ⚠️  Biggest Decline: {result['summary']['biggest_decline']}")
        
        return True
        
    except Exception as e:
        print(f"✗ Session comparison failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_bat_speed_progress(tracker):
    """Test 7: Comprehensive bat speed progress"""
    print("\n" + "=" * 80)
    print("TEST 7: BAT SPEED PROGRESS (COMPREHENSIVE)")
    print("=" * 80)
    
    try:
        bat_speed = tracker.get_bat_speed_progress(player_id=1)
        
        print(f"✓ Bat speed progress calculated")
        print(f"\n  🎯 ACTUAL BAT SPEED:")
        print(f"    Improvement: {bat_speed['actual_bat_speed']['improvement']:+.1f} mph")
        print(f"    Trend: {bat_speed['actual_bat_speed']['trend']}")
        
        print(f"\n  📏 GAP TO POTENTIAL:")
        print(f"    Gap Change: {bat_speed['gap']['improvement']:+.1f} mph")
        print(f"    Gap is Closing: {'YES ✓' if bat_speed['gap_is_closing'] else 'NO ✗'}")
        print(f"    Closure Rate: {bat_speed['gap_closure_rate']} mph")
        
        if bat_speed['projected_weeks_to_potential']:
            print(f"    Projected Weeks to Reach Potential: {bat_speed['projected_weeks_to_potential']:.1f} weeks")
        
        return bat_speed['gap_is_closing']
        
    except Exception as e:
        print(f"✗ Bat speed progress failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 80)
    print("🧪 PRIORITY 7: DATABASE & PROGRESS TRACKING TEST SUITE")
    print("=" * 80)
    print()
    
    tests = []
    
    # Test 1: Files exist
    tests.append(("File Existence", test_files_exist()))
    
    # Test 2: Import modules
    import_success, tracker, comparison, db = test_import_modules()
    tests.append(("Module Imports", import_success))
    
    if not import_success:
        print("\n✗ Cannot proceed with remaining tests - imports failed")
        return False
    
    # Test 3-7: Functionality tests
    tests.append(("Player History", test_get_history(tracker, db)))
    tests.append(("Progress Calculation", test_calculate_progress(tracker)))
    tests.append(("Component Progress", test_component_progress(tracker)))
    tests.append(("Session Comparison", test_session_comparison(comparison)))
    tests.append(("Bat Speed Progress", test_bat_speed_progress(tracker)))
    
    # Summary
    print("\n" + "=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    
    passed = sum(1 for _, result in tests if result)
    total = len(tests)
    
    for name, result in tests:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    print(f"\n{'=' * 80}")
    print(f"TOTAL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED - PRIORITY 7 COMPLETE!")
    else:
        print(f"⚠️  {total - passed} test(s) failed")
    
    print("=" * 80)
    
    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
