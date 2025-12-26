"""
Race Bar Formatter
Converts kinetic chain sequence data to Race Bar visualization format

The Race Bar shows the sequential timing of body segments during the swing,
visualizing the kinetic chain from ground up (hips → shoulders → arms → bat).

Grading Scale (based on sequence efficiency):
- A+: 95-100% efficiency, optimal timing gaps (80-120ms between segments)
- A: 90-94% efficiency, very good timing
- B: 80-89% efficiency, acceptable timing
- C: 70-79% efficiency, some inefficiencies
- F: <70% efficiency, significant breakdown

Author: Builder 2 (Backend & Database AI)
Date: 2024-12-24
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class RaceBarSegment:
    """Single segment in the race bar"""
    name: str
    peak_timing_ms: float
    duration_ms: float
    color: str


def format_kinetic_sequence_for_race_bar(kinetic_chain_events: Dict) -> Dict:
    """
    Convert existing kinetic chain data to Race Bar visualization format
    
    Args:
        kinetic_chain_events: Dictionary with kinetic chain timing data:
        {
            'lower_half_peak_ms': 420,
            'torso_peak_ms': 520,
            'arms_peak_ms': 610,
            'tempo_lower_to_torso': 100,
            'tempo_torso_to_arms': 90
        }
    
    Returns:
        Race Bar format dictionary:
        {
            'segments': [
                {'name': 'HIPS', 'peak_timing_ms': 420, 'duration_ms': 80, 'color': '#3B82F6'},
                {'name': 'SHOULDERS', 'peak_timing_ms': 520, 'duration_ms': 80, 'color': '#10B981'},
                {'name': 'ARMS', 'peak_timing_ms': 610, 'duration_ms': 80, 'color': '#F59E0B'},
                {'name': 'BAT', 'peak_timing_ms': 690, 'duration_ms': 80, 'color': '#EF4444'}
            ],
            'sequence_grade': 'A+',
            'timing_gap': 90,
            'energy_transfer': 98
        }
    """
    # Extract peak timings
    hips_peak = kinetic_chain_events.get('lower_half_peak_ms', 0)
    shoulders_peak = kinetic_chain_events.get('torso_peak_ms', 0)
    arms_peak = kinetic_chain_events.get('arms_peak_ms', 0)
    
    # Estimate bat peak (typically 80-100ms after arms peak)
    bat_peak = arms_peak + 80
    
    # Standard segment duration (visual representation)
    # In reality, segments overlap, but for visualization we show fixed duration
    segment_duration = 80  # ms
    
    # Create segments
    segments = [
        {
            'name': 'HIPS',
            'peak_timing_ms': hips_peak,
            'duration_ms': segment_duration,
            'color': '#3B82F6'  # Blue
        },
        {
            'name': 'SHOULDERS',
            'peak_timing_ms': shoulders_peak,
            'duration_ms': segment_duration,
            'color': '#10B981'  # Green
        },
        {
            'name': 'ARMS',
            'peak_timing_ms': arms_peak,
            'duration_ms': segment_duration,
            'color': '#F59E0B'  # Orange
        },
        {
            'name': 'BAT',
            'peak_timing_ms': bat_peak,
            'duration_ms': segment_duration,
            'color': '#EF4444'  # Red
        }
    ]
    
    # Calculate timing gaps between segments
    gap_hips_to_shoulders = shoulders_peak - hips_peak if shoulders_peak > hips_peak else 0
    gap_shoulders_to_arms = arms_peak - shoulders_peak if arms_peak > shoulders_peak else 0
    gap_arms_to_bat = bat_peak - arms_peak if bat_peak > arms_peak else 0
    
    # Average timing gap
    timing_gaps = [gap_hips_to_shoulders, gap_shoulders_to_arms, gap_arms_to_bat]
    valid_gaps = [g for g in timing_gaps if g > 0]
    avg_timing_gap = sum(valid_gaps) / len(valid_gaps) if valid_gaps else 0
    
    # Calculate sequence grade and energy transfer efficiency
    sequence_grade, energy_transfer = _grade_kinetic_sequence(timing_gaps)
    
    return {
        'segments': segments,
        'sequence_grade': sequence_grade,
        'timing_gap': round(avg_timing_gap, 1),
        'energy_transfer': energy_transfer,
        'timing_gaps': {
            'hips_to_shoulders_ms': gap_hips_to_shoulders,
            'shoulders_to_arms_ms': gap_shoulders_to_arms,
            'arms_to_bat_ms': gap_arms_to_bat
        }
    }


def _grade_kinetic_sequence(timing_gaps: List[float]) -> tuple:
    """
    Grade the kinetic sequence based on timing gaps
    
    Optimal timing gaps are 80-120ms between segments.
    Too fast (<60ms) = segments overlapping, energy loss
    Too slow (>150ms) = disconnected, energy loss
    
    Args:
        timing_gaps: List of [hips→shoulders, shoulders→arms, arms→bat] gaps in ms
    
    Returns:
        Tuple of (grade, energy_transfer_percentage)
    """
    if not timing_gaps or all(g == 0 for g in timing_gaps):
        return ('F', 0)
    
    # Optimal range: 80-120ms
    # Calculate how far each gap deviates from optimal
    optimal_min = 80
    optimal_max = 120
    
    deviations = []
    for gap in timing_gaps:
        if gap == 0:
            continue
        
        if optimal_min <= gap <= optimal_max:
            # Perfect timing
            deviation = 0
        elif gap < optimal_min:
            # Too fast - overlapping
            deviation = abs(gap - optimal_min)
        else:  # gap > optimal_max
            # Too slow - disconnected
            deviation = abs(gap - optimal_max)
        
        deviations.append(deviation)
    
    if not deviations:
        return ('F', 0)
    
    # Calculate average deviation
    avg_deviation = sum(deviations) / len(deviations)
    
    # Calculate efficiency score (0-100%)
    # Perfect = 100%, each 10ms deviation reduces efficiency by ~2%
    efficiency = 100 - (avg_deviation * 0.2)
    efficiency = max(0, min(100, efficiency))
    
    # Assign grade based on efficiency
    if efficiency >= 95:
        grade = 'A+'
    elif efficiency >= 90:
        grade = 'A'
    elif efficiency >= 85:
        grade = 'A-'
    elif efficiency >= 80:
        grade = 'B+'
    elif efficiency >= 75:
        grade = 'B'
    elif efficiency >= 70:
        grade = 'B-'
    elif efficiency >= 65:
        grade = 'C+'
    elif efficiency >= 60:
        grade = 'C'
    else:
        grade = 'F'
    
    return (grade, int(round(efficiency)))


def analyze_race_bar_consistency(race_bars: List[Dict]) -> Dict:
    """
    Analyze consistency of kinetic sequence across multiple swings
    
    Args:
        race_bars: List of race bar dictionaries from multiple swings
    
    Returns:
        Consistency analysis:
        {
            'avg_timing_gap': 92.5,
            'std_dev_gap': 8.2,
            'avg_efficiency': 96.3,
            'consistency_rating': 'EXCELLENT'
        }
    """
    if not race_bars:
        return {
            'avg_timing_gap': 0.0,
            'std_dev_gap': 0.0,
            'avg_efficiency': 0.0,
            'consistency_rating': 'N/A'
        }
    
    # Extract metrics
    timing_gaps = [rb['timing_gap'] for rb in race_bars if rb['timing_gap'] > 0]
    efficiencies = [rb['energy_transfer'] for rb in race_bars]
    
    # Calculate averages
    avg_timing_gap = sum(timing_gaps) / len(timing_gaps) if timing_gaps else 0
    avg_efficiency = sum(efficiencies) / len(efficiencies) if efficiencies else 0
    
    # Calculate standard deviation of timing gaps
    if len(timing_gaps) > 1:
        variance = sum((g - avg_timing_gap) ** 2 for g in timing_gaps) / len(timing_gaps)
        std_dev_gap = variance ** 0.5
    else:
        std_dev_gap = 0
    
    # Determine consistency rating based on std dev
    # Lower std dev = more consistent
    if std_dev_gap < 5:
        consistency_rating = 'EXCELLENT'
    elif std_dev_gap < 10:
        consistency_rating = 'VERY GOOD'
    elif std_dev_gap < 15:
        consistency_rating = 'GOOD'
    elif std_dev_gap < 20:
        consistency_rating = 'FAIR'
    else:
        consistency_rating = 'NEEDS IMPROVEMENT'
    
    return {
        'avg_timing_gap': round(avg_timing_gap, 1),
        'std_dev_gap': round(std_dev_gap, 2),
        'avg_efficiency': round(avg_efficiency, 1),
        'consistency_rating': consistency_rating,
        'grade_distribution': _count_grades([rb['sequence_grade'] for rb in race_bars])
    }


def _count_grades(grades: List[str]) -> Dict[str, int]:
    """Count occurrences of each grade"""
    grade_counts = {}
    for grade in grades:
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    return grade_counts


def create_race_bar_from_events(
    stance_start_ms: float,
    load_start_ms: float,
    stride_start_ms: float,
    launch_start_ms: float,
    contact_ms: float
) -> Dict:
    """
    Create race bar directly from event timestamps
    
    Args:
        stance_start_ms: Stance phase start time
        load_start_ms: Load phase start time
        stride_start_ms: Stride phase start time
        launch_start_ms: Launch phase start time
        contact_ms: Contact time
    
    Returns:
        Race bar dictionary
    """
    # Estimate peak velocities for each segment
    # Typically occur at midpoint of each phase
    hips_peak = (load_start_ms + stride_start_ms) / 2
    shoulders_peak = (stride_start_ms + launch_start_ms) / 2
    arms_peak = (launch_start_ms + contact_ms) / 2
    
    kinetic_chain_events = {
        'lower_half_peak_ms': hips_peak,
        'torso_peak_ms': shoulders_peak,
        'arms_peak_ms': arms_peak,
        'tempo_lower_to_torso': shoulders_peak - hips_peak,
        'tempo_torso_to_arms': arms_peak - shoulders_peak
    }
    
    return format_kinetic_sequence_for_race_bar(kinetic_chain_events)


# Example usage
if __name__ == "__main__":
    print("Race Bar Formatter - Example")
    print("=" * 50)
    
    # Example 1: Optimal kinetic sequence
    print("\nExample 1: Optimal Sequence (A+ Grade)")
    kinetic_chain = {
        'lower_half_peak_ms': 400,
        'torso_peak_ms': 490,   # 90ms gap (optimal)
        'arms_peak_ms': 585,    # 95ms gap (optimal)
        'tempo_lower_to_torso': 90,
        'tempo_torso_to_arms': 95
    }
    race_bar = format_kinetic_sequence_for_race_bar(kinetic_chain)
    print(f"  Sequence Grade: {race_bar['sequence_grade']}")
    print(f"  Energy Transfer: {race_bar['energy_transfer']}%")
    print(f"  Average Timing Gap: {race_bar['timing_gap']}ms")
    print(f"  Segments:")
    for seg in race_bar['segments']:
        print(f"    - {seg['name']}: {seg['peak_timing_ms']}ms")
    
    # Example 2: Suboptimal sequence (too fast)
    print("\nExample 2: Too Fast Sequence (B Grade)")
    kinetic_chain = {
        'lower_half_peak_ms': 400,
        'torso_peak_ms': 450,   # 50ms gap (too fast)
        'arms_peak_ms': 505,    # 55ms gap (too fast)
        'tempo_lower_to_torso': 50,
        'tempo_torso_to_arms': 55
    }
    race_bar = format_kinetic_sequence_for_race_bar(kinetic_chain)
    print(f"  Sequence Grade: {race_bar['sequence_grade']}")
    print(f"  Energy Transfer: {race_bar['energy_transfer']}%")
    print(f"  Average Timing Gap: {race_bar['timing_gap']}ms")
    
    # Example 3: Suboptimal sequence (too slow)
    print("\nExample 3: Too Slow Sequence (C Grade)")
    kinetic_chain = {
        'lower_half_peak_ms': 400,
        'torso_peak_ms': 560,   # 160ms gap (too slow)
        'arms_peak_ms': 730,    # 170ms gap (too slow)
        'tempo_lower_to_torso': 160,
        'tempo_torso_to_arms': 170
    }
    race_bar = format_kinetic_sequence_for_race_bar(kinetic_chain)
    print(f"  Sequence Grade: {race_bar['sequence_grade']}")
    print(f"  Energy Transfer: {race_bar['energy_transfer']}%")
    print(f"  Average Timing Gap: {race_bar['timing_gap']}ms")
