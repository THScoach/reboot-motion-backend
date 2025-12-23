"""
Track player progress over multiple sessions
Analyze trends and improvements

This module provides progress tracking capabilities for the Kinetic DNA Blueprint system,
allowing coaches and players to monitor improvement over time across multiple analysis sessions.
"""

from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
import statistics


class ProgressTracker:
    """
    Track and analyze player progress over time
    
    Provides methods to:
    - Retrieve player analysis history
    - Calculate progress metrics for specific measurements
    - Track component (Ground/Engine/Weapon) improvements
    - Identify trends and improvement rates
    """
    
    def __init__(self, db_connection: Any):
        """
        Initialize progress tracker with database connection
        
        Args:
            db_connection: Database connection object (SQLAlchemy session, psycopg2, etc.)
        """
        self.db = db_connection
    
    def get_player_history(
        self,
        player_id: int,
        limit: int = 10,
        metrics: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Get player's analysis history
        
        Args:
            player_id: Player ID
            limit: Maximum number of sessions to return (default: 10)
            metrics: Specific metrics to include (None = all standard metrics)
        
        Returns:
            List of analysis results sorted by date (newest first)
            
        Example:
            >>> tracker = ProgressTracker(db)
            >>> history = tracker.get_player_history(player_id=1, limit=5)
            >>> print(f"Player has {len(history)} sessions")
        """
        query = """
            SELECT 
                id,
                analysis_date,
                bat_speed_actual_mph,
                bat_speed_potential_mph,
                bat_speed_gap_mph,
                pct_potential_achieved,
                ground_score,
                engine_score,
                weapon_score,
                overall_efficiency,
                motor_profile,
                motor_profile_confidence,
                weakest_component,
                estimated_gain_mph,
                total_estimated_gain_mph
            FROM analysis_results
            WHERE player_id = %s
            ORDER BY analysis_date DESC
            LIMIT %s
        """
        
        try:
            # Execute query - implementation depends on database library
            cursor = self.db.cursor()
            cursor.execute(query, (player_id, limit))
            results = cursor.fetchall()
            
            history = []
            for row in results:
                history.append({
                    'id': row[0],
                    'date': row[1].isoformat() if hasattr(row[1], 'isoformat') else str(row[1]),
                    'bat_speed_actual': float(row[2]) if row[2] is not None else None,
                    'bat_speed_potential': float(row[3]) if row[3] is not None else None,
                    'bat_speed_gap': float(row[4]) if row[4] is not None else None,
                    'pct_achieved': float(row[5]) if row[5] is not None else None,
                    'ground_score': float(row[6]) if row[6] is not None else None,
                    'engine_score': float(row[7]) if row[7] is not None else None,
                    'weapon_score': float(row[8]) if row[8] is not None else None,
                    'overall_efficiency': float(row[9]) if row[9] is not None else None,
                    'motor_profile': row[10],
                    'motor_profile_confidence': float(row[11]) if row[11] is not None else None,
                    'weakest_component': row[12],
                    'estimated_gain': float(row[13]) if row[13] is not None else None,
                    'total_estimated_gain': float(row[14]) if row[14] is not None else None
                })
            
            return history
            
        except Exception as e:
            print(f"Error retrieving player history: {e}")
            return []
    
    def calculate_progress(
        self,
        player_id: int,
        metric: str = 'bat_speed_actual_mph',
        time_window_days: Optional[int] = None
    ) -> Dict:
        """
        Calculate progress metrics for a specific metric
        
        Args:
            player_id: Player ID
            metric: Metric to track (e.g., 'bat_speed_actual_mph', 'ground_score', 'weapon_score')
            time_window_days: Only consider sessions within this time window (None = all time)
        
        Returns:
            Dictionary with progress metrics:
            {
                'metric_name': 'bat_speed_actual_mph',
                'first_session': {'date': '2024-01-15', 'value': 57.9},
                'latest_session': {'date': '2024-03-20', 'value': 63.2},
                'improvement': 5.3,
                'pct_improvement': 9.15,
                'trend': 'IMPROVING',  # 'IMPROVING', 'DECLINING', 'STABLE'
                'sessions_count': 8,
                'avg_value': 60.5,
                'std_deviation': 2.1,
                'improvement_rate_per_week': 0.8
            }
            
        Example:
            >>> progress = tracker.calculate_progress(1, 'bat_speed_actual_mph')
            >>> print(f"Improved by {progress['improvement']} mph!")
        """
        # Build query with optional time window
        query = f"""
            SELECT 
                analysis_date,
                {metric}
            FROM analysis_results
            WHERE player_id = %s
        """
        
        params: List[Any] = [player_id]
        
        if time_window_days:
            query += " AND analysis_date >= %s"
            cutoff_date = datetime.now() - timedelta(days=time_window_days)
            params.append(cutoff_date)
        
        query += " ORDER BY analysis_date ASC"
        
        try:
            cursor = self.db.cursor()
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            if not results or len(results) < 2:
                return {
                    'error': 'Not enough data for progress calculation',
                    'sessions_count': len(results) if results else 0,
                    'message': 'Need at least 2 sessions to calculate progress'
                }
            
            # Extract values
            dates = [row[0] for row in results]
            values = [float(row[1]) for row in results if row[1] is not None]
            
            if not values:
                return {
                    'error': 'No valid data points',
                    'sessions_count': len(results)
                }
            
            # Calculate metrics
            first_value = values[0]
            latest_value = values[-1]
            improvement = latest_value - first_value
            pct_improvement = (improvement / first_value * 100) if first_value != 0 else 0
            
            # Determine trend
            if len(values) >= 3:
                # Use average of recent vs old to determine trend
                mid_point = len(values) // 2
                old_avg = statistics.mean(values[:mid_point])
                recent_avg = statistics.mean(values[mid_point:])
                
                if recent_avg > old_avg * 1.02:  # 2% threshold
                    trend = 'IMPROVING'
                elif recent_avg < old_avg * 0.98:
                    trend = 'DECLINING'
                else:
                    trend = 'STABLE'
            else:
                trend = 'IMPROVING' if improvement > 0 else ('DECLINING' if improvement < 0 else 'STABLE')
            
            # Calculate time-based improvement rate
            days_elapsed = (dates[-1] - dates[0]).days
            weeks_elapsed = days_elapsed / 7 if days_elapsed > 0 else 1
            improvement_rate_per_week = improvement / weeks_elapsed if weeks_elapsed > 0 else 0
            
            return {
                'metric_name': metric,
                'first_session': {
                    'date': dates[0].isoformat() if hasattr(dates[0], 'isoformat') else str(dates[0]),
                    'value': round(first_value, 2)
                },
                'latest_session': {
                    'date': dates[-1].isoformat() if hasattr(dates[-1], 'isoformat') else str(dates[-1]),
                    'value': round(latest_value, 2)
                },
                'improvement': round(improvement, 2),
                'pct_improvement': round(pct_improvement, 2),
                'trend': trend,
                'sessions_count': len(values),
                'avg_value': round(statistics.mean(values), 2),
                'std_deviation': round(statistics.stdev(values), 2) if len(values) > 1 else 0,
                'improvement_rate_per_week': round(improvement_rate_per_week, 2)
            }
            
        except Exception as e:
            return {
                'error': f'Error calculating progress: {str(e)}',
                'metric_name': metric
            }
    
    def get_component_progress(
        self,
        player_id: int,
        time_window_days: Optional[int] = None
    ) -> Dict:
        """
        Get progress for all three components (Ground, Engine, Weapon)
        
        Args:
            player_id: Player ID
            time_window_days: Optional time window for analysis
        
        Returns:
            {
                'ground': {...progress metrics...},
                'engine': {...progress metrics...},
                'weapon': {...progress metrics...},
                'most_improved': 'GROUND',
                'needs_focus': 'WEAPON',
                'overall_trend': 'IMPROVING'
            }
            
        Example:
            >>> comp_progress = tracker.get_component_progress(1)
            >>> print(f"Focus on {comp_progress['needs_focus']}")
        """
        ground = self.calculate_progress(player_id, 'ground_score', time_window_days)
        engine = self.calculate_progress(player_id, 'engine_score', time_window_days)
        weapon = self.calculate_progress(player_id, 'weapon_score', time_window_days)
        
        # Determine most improved and needs focus
        improvements = {
            'GROUND': ground.get('improvement', 0),
            'ENGINE': engine.get('improvement', 0),
            'WEAPON': weapon.get('improvement', 0)
        }
        
        # Most improved = highest improvement
        most_improved = max(improvements, key=improvements.get)
        
        # Needs focus = lowest current score or declining
        latest_scores = {
            'GROUND': ground.get('latest_session', {}).get('value', 50),
            'ENGINE': engine.get('latest_session', {}).get('value', 50),
            'WEAPON': weapon.get('latest_session', {}).get('value', 50)
        }
        
        needs_focus = min(latest_scores, key=latest_scores.get)
        
        # Overall trend
        trends = [ground.get('trend'), engine.get('trend'), weapon.get('trend')]
        improving_count = trends.count('IMPROVING')
        declining_count = trends.count('DECLINING')
        
        if improving_count > declining_count:
            overall_trend = 'IMPROVING'
        elif declining_count > improving_count:
            overall_trend = 'DECLINING'
        else:
            overall_trend = 'STABLE'
        
        return {
            'ground': ground,
            'engine': engine,
            'weapon': weapon,
            'most_improved': most_improved,
            'most_improved_gain': round(improvements[most_improved], 2),
            'needs_focus': needs_focus,
            'needs_focus_score': round(latest_scores[needs_focus], 2),
            'overall_trend': overall_trend,
            'summary': {
                'improving_components': improving_count,
                'declining_components': declining_count,
                'stable_components': trends.count('STABLE')
            }
        }
    
    def get_bat_speed_progress(
        self,
        player_id: int,
        time_window_days: Optional[int] = None
    ) -> Dict:
        """
        Get comprehensive bat speed progress including actual, potential, and gap
        
        Returns detailed bat speed progress metrics
        """
        actual_progress = self.calculate_progress(player_id, 'bat_speed_actual_mph', time_window_days)
        gap_progress = self.calculate_progress(player_id, 'bat_speed_gap_mph', time_window_days)
        
        # Gap should be decreasing (negative improvement is good!)
        gap_improvement = gap_progress.get('improvement', 0)
        gap_is_closing = gap_improvement < 0
        
        return {
            'actual_bat_speed': actual_progress,
            'gap': gap_progress,
            'gap_is_closing': gap_is_closing,
            'gap_closure_rate': abs(round(gap_improvement, 2)),
            'projected_weeks_to_potential': (
                abs(gap_progress.get('latest_session', {}).get('value', 0)) / 
                abs(gap_progress.get('improvement_rate_per_week', 0.1))
            ) if gap_progress.get('improvement_rate_per_week', 0) != 0 else None
        }
