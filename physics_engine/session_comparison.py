"""
Compare analysis results between multiple sessions
Provides side-by-side comparison and change tracking

This module enables detailed comparison of player sessions to identify
improvements, declines, and patterns across multiple analysis sessions.
"""

from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


class SessionComparison:
    """
    Compare two or more sessions side-by-side
    
    Provides methods to:
    - Compare multiple sessions with detailed metrics
    - Calculate changes between sessions
    - Identify biggest improvements and declines
    - Generate summary statistics
    """
    
    def __init__(self, db_connection: Any):
        """
        Initialize session comparison with database connection
        
        Args:
            db_connection: Database connection object
        """
        self.db = db_connection
    
    def compare_sessions(
        self,
        session_ids: List[int]
    ) -> Dict:
        """
        Compare multiple sessions side-by-side
        
        Args:
            session_ids: List of analysis_results IDs to compare (minimum 2)
        
        Returns:
            {
                'sessions': [
                    {
                        'id': 1,
                        'date': '2024-01-15',
                        'bat_speed_actual': 57.9,
                        'bat_speed_potential': 76.0,
                        'ground_score': 72,
                        'engine_score': 85,
                        'weapon_score': 40,
                        'motor_profile': 'SPINNER',
                        ...
                    },
                    {...}
                ],
                'changes': {
                    'bat_speed_actual': {
                        'first': 57.9,
                        'latest': 61.5,
                        'change': +3.6,
                        'pct_change': +6.22
                    },
                    'ground_score': {...},
                    ...
                },
                'summary': {
                    'total_sessions': 3,
                    'date_range': '2024-01-15 to 2024-03-20',
                    'days_elapsed': 65,
                    'overall_trend': 'IMPROVING',
                    'biggest_improvement': 'WEAPON (+12 points)',
                    'biggest_decline': None
                }
            }
            
        Example:
            >>> comparison = SessionComparison(db)
            >>> result = comparison.compare_sessions([1, 3, 5])
            >>> print(result['summary']['overall_trend'])
        """
        if len(session_ids) < 2:
            return {
                'error': 'Need at least 2 sessions to compare',
                'provided': len(session_ids)
            }
        
        # Fetch sessions
        placeholders = ','.join(['%s'] * len(session_ids))
        query = f"""
            SELECT 
                id,
                analysis_date,
                player_name,
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
                primary_focus_component,
                estimated_gain_mph,
                total_estimated_gain_mph
            FROM analysis_results
            WHERE id IN ({placeholders})
            ORDER BY analysis_date ASC
        """
        
        try:
            cursor = self.db.cursor()
            cursor.execute(query, tuple(session_ids))
            results = cursor.fetchall()
            
            if len(results) < 2:
                return {
                    'error': 'Could not find enough sessions',
                    'requested': len(session_ids),
                    'found': len(results)
                }
            
            # Build session objects
            sessions = []
            for row in results:
                sessions.append({
                    'id': row[0],
                    'date': row[1].isoformat() if hasattr(row[1], 'isoformat') else str(row[1]),
                    'player_name': row[2],
                    'bat_speed_actual': float(row[3]) if row[3] is not None else None,
                    'bat_speed_potential': float(row[4]) if row[4] is not None else None,
                    'bat_speed_gap': float(row[5]) if row[5] is not None else None,
                    'pct_achieved': float(row[6]) if row[6] is not None else None,
                    'ground_score': float(row[7]) if row[7] is not None else None,
                    'engine_score': float(row[8]) if row[8] is not None else None,
                    'weapon_score': float(row[9]) if row[9] is not None else None,
                    'overall_efficiency': float(row[10]) if row[10] is not None else None,
                    'motor_profile': row[11],
                    'motor_profile_confidence': float(row[12]) if row[12] is not None else None,
                    'weakest_component': row[13],
                    'primary_focus': row[14],
                    'estimated_gain': float(row[15]) if row[15] is not None else None,
                    'total_estimated_gain': float(row[16]) if row[16] is not None else None
                })
            
            # Calculate changes between first and last session
            metrics = [
                ('bat_speed_actual', 'Bat Speed (Actual)'),
                ('bat_speed_gap', 'Bat Speed Gap'),
                ('pct_achieved', '% Potential Achieved'),
                ('ground_score', 'Ground Score'),
                ('engine_score', 'Engine Score'),
                ('weapon_score', 'Weapon Score'),
                ('overall_efficiency', 'Overall Efficiency')
            ]
            
            changes = {}
            for metric_key, metric_label in metrics:
                first_val = sessions[0].get(metric_key)
                latest_val = sessions[-1].get(metric_key)
                
                if first_val is not None and latest_val is not None:
                    change = latest_val - first_val
                    pct_change = (change / first_val * 100) if first_val != 0 else 0
                    
                    changes[metric_key] = {
                        'label': metric_label,
                        'first': round(first_val, 2),
                        'latest': round(latest_val, 2),
                        'change': round(change, 2),
                        'pct_change': round(pct_change, 2),
                        'direction': 'IMPROVED' if change > 0 else ('DECLINED' if change < 0 else 'STABLE')
                    }
                    
                    # Special case: bat_speed_gap should decrease (lower is better)
                    if metric_key == 'bat_speed_gap':
                        changes[metric_key]['direction'] = 'IMPROVED' if change < 0 else ('DECLINED' if change > 0 else 'STABLE')
            
            # Determine biggest changes
            # For improvements: positive change (except bat_speed_gap)
            improvements = {}
            declines = {}
            
            for key, data in changes.items():
                if key == 'bat_speed_gap':
                    # Gap: negative change is improvement
                    if data['change'] < 0:
                        improvements[key] = abs(data['change'])
                    elif data['change'] > 0:
                        declines[key] = data['change']
                else:
                    # Other metrics: positive change is improvement
                    if data['change'] > 0:
                        improvements[key] = data['change']
                    elif data['change'] < 0:
                        declines[key] = abs(data['change'])
            
            biggest_improvement = None
            if improvements:
                best_key = max(improvements.items(), key=lambda x: x[1])
                biggest_improvement = f"{changes[best_key[0]]['label']} ({changes[best_key[0]]['change']:+.1f})"
            
            biggest_decline = None
            if declines:
                worst_key = max(declines.items(), key=lambda x: x[1])
                biggest_decline = f"{changes[worst_key[0]]['label']} ({changes[worst_key[0]]['change']:+.1f})"
            
            # Calculate summary
            date_range = f"{sessions[0]['date']} to {sessions[-1]['date']}"
            
            # Parse dates for day calculation
            try:
                if isinstance(sessions[0]['date'], str):
                    date_start = datetime.fromisoformat(sessions[0]['date'].replace('Z', '+00:00'))
                    date_end = datetime.fromisoformat(sessions[-1]['date'].replace('Z', '+00:00'))
                else:
                    date_start = sessions[0]['date']
                    date_end = sessions[-1]['date']
                
                days_elapsed = (date_end - date_start).days
            except:
                days_elapsed = 0
            
            # Overall trend: more improvements than declines?
            overall_trend = 'IMPROVING' if len(improvements) > len(declines) else (
                'DECLINING' if len(declines) > len(improvements) else 'STABLE'
            )
            
            return {
                'sessions': sessions,
                'changes': changes,
                'summary': {
                    'total_sessions': len(sessions),
                    'player_name': sessions[0]['player_name'],
                    'date_range': date_range,
                    'days_elapsed': days_elapsed,
                    'weeks_elapsed': round(days_elapsed / 7, 1),
                    'overall_trend': overall_trend,
                    'improvements_count': len(improvements),
                    'declines_count': len(declines),
                    'biggest_improvement': biggest_improvement,
                    'biggest_decline': biggest_decline,
                    'motor_profile_changes': self._track_motor_profile_changes(sessions)
                }
            }
            
        except Exception as e:
            return {
                'error': f'Error comparing sessions: {str(e)}',
                'session_ids': session_ids
            }
    
    def _track_motor_profile_changes(self, sessions: List[Dict]) -> Dict:
        """
        Track motor profile changes across sessions
        
        Args:
            sessions: List of session dictionaries
        
        Returns:
            {
                'first': 'SPINNER',
                'latest': 'BALANCED',
                'changed': True,
                'history': ['SPINNER', 'SPINNER', 'BALANCED']
            }
        """
        profiles = [s['motor_profile'] for s in sessions if s.get('motor_profile')]
        
        if not profiles:
            return {'changed': False, 'history': []}
        
        first_profile = profiles[0]
        latest_profile = profiles[-1]
        changed = first_profile != latest_profile
        
        return {
            'first': first_profile,
            'latest': latest_profile,
            'changed': changed,
            'history': profiles,
            'stability': 'STABLE' if len(set(profiles)) == 1 else 'EVOLVING'
        }
    
    def compare_two_sessions(
        self,
        session_id_1: int,
        session_id_2: int
    ) -> Dict:
        """
        Quick comparison between exactly two sessions
        
        Args:
            session_id_1: First session ID (earlier)
            session_id_2: Second session ID (later)
        
        Returns:
            Simplified comparison focused on key changes
        """
        result = self.compare_sessions([session_id_1, session_id_2])
        
        if 'error' in result:
            return result
        
        # Simplify for 2-session comparison
        return {
            'session_1': result['sessions'][0],
            'session_2': result['sessions'][1],
            'changes': result['changes'],
            'summary': {
                'days_between': result['summary']['days_elapsed'],
                'overall_trend': result['summary']['overall_trend'],
                'biggest_improvement': result['summary']['biggest_improvement'],
                'biggest_decline': result['summary']['biggest_decline']
            }
        }
    
    def get_session_details(
        self,
        session_id: int
    ) -> Optional[Dict]:
        """
        Get full details for a single session
        
        Args:
            session_id: Analysis result ID
        
        Returns:
            Complete session data or None if not found
        """
        query = """
            SELECT *
            FROM analysis_results
            WHERE id = %s
        """
        
        try:
            cursor = self.db.cursor()
            cursor.execute(query, (session_id,))
            row = cursor.fetchone()
            
            if not row:
                return None
            
            # Get column names
            columns = [desc[0] for desc in cursor.description]
            
            # Build dictionary
            session = {}
            for i, col in enumerate(columns):
                value = row[i]
                
                # Convert datetime objects
                if hasattr(value, 'isoformat'):
                    value = value.isoformat()
                
                # Convert decimals/floats
                elif isinstance(value, (float, int)):
                    value = float(value) if isinstance(value, float) else value
                
                session[col] = value
            
            return session
            
        except Exception as e:
            print(f"Error getting session details: {e}")
            return None
