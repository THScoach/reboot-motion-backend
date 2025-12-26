"""
Tempo Score Calculator
Calculates Load:Launch:Contact tempo ratios for swing analysis

Tempo Categories:
- Hair Trigger (<0.75): Very quick trigger
- Quick Trigger (0.75-1.5): Fast reaction to pitch
- Balanced (1.5-2.5): Optimal for all pitch types
- Long Load (>2.5): Patient, high power potential

Author: Builder 2 (Backend & Database AI)
Date: 2024-12-24
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class TempoScore:
    """Tempo score result"""
    load_frames: int
    launch_frames: int
    contact_frames: int
    ratio: float
    category: str
    description: str
    load_duration_ms: float
    launch_duration_ms: float
    contact_duration_ms: float


def calculate_tempo_score(
    load_duration_ms: float,
    launch_duration_ms: float,
    contact_duration_ms: float
) -> Dict:
    """
    Calculate Load:Launch:Contact tempo ratio
    
    Args:
        load_duration_ms: Duration of load phase in milliseconds
        launch_duration_ms: Duration of launch phase in milliseconds
        contact_duration_ms: Duration of contact phase in milliseconds
    
    Returns:
        Dictionary with tempo analysis:
        {
            'load_frames': 76,  # At 120 FPS
            'launch_frames': 38,
            'contact_frames': 30,
            'ratio': 2.1,
            'category': 'Balanced',
            'description': 'Optimal for all pitch types'
        }
    
    Tempo Categories:
    - Hair Trigger: ratio < 0.75 (Very quick trigger)
    - Quick Trigger: 0.75 <= ratio < 1.5 (Fast reaction)
    - Balanced: 1.5 <= ratio < 2.5 (Optimal)
    - Long Load: ratio >= 2.5 (Patient, high power)
    """
    # Assume 120 FPS for frame calculation (standard for high-speed cameras)
    FPS = 120.0
    ms_per_frame = 1000.0 / FPS
    
    # Convert milliseconds to frames
    load_frames = int(round(load_duration_ms / ms_per_frame))
    launch_frames = int(round(launch_duration_ms / ms_per_frame))
    contact_frames = int(round(contact_duration_ms / ms_per_frame))
    
    # Calculate tempo ratio (Load / Launch)
    # This represents how long the load phase is relative to the launch phase
    if launch_duration_ms > 0:
        ratio = load_duration_ms / launch_duration_ms
    else:
        ratio = 0.0
    
    # Determine tempo category and description
    category, description = _categorize_tempo(ratio)
    
    return {
        'load_frames': load_frames,
        'launch_frames': launch_frames,
        'contact_frames': contact_frames,
        'load_duration_ms': load_duration_ms,
        'launch_duration_ms': launch_duration_ms,
        'contact_duration_ms': contact_duration_ms,
        'ratio': round(ratio, 2),
        'category': category,
        'description': description
    }


def _categorize_tempo(ratio: float) -> tuple:
    """
    Categorize tempo ratio into performance categories
    
    Args:
        ratio: Load/Launch tempo ratio
    
    Returns:
        Tuple of (category, description)
    """
    if ratio < 0.75:
        return (
            'Hair Trigger',
            'Very quick trigger - May struggle with off-speed pitches'
        )
    elif ratio < 1.5:
        return (
            'Quick Trigger',
            'Fast reaction to pitch - Good for fastballs'
        )
    elif ratio < 2.5:
        return (
            'Balanced',
            'Optimal timing - Can handle all pitch types'
        )
    else:  # ratio >= 2.5
        return (
            'Long Load',
            'Patient approach - High power potential, watch for timing on fastballs'
        )


def calculate_tempo_from_events(events: Dict) -> Dict:
    """
    Calculate tempo score from event detection results
    
    Args:
        events: Dictionary with kinetic chain events containing:
            - stance_start_ms
            - load_start_ms
            - stride_start_ms
            - launch_start_ms
            - contact_ms
            - follow_through_end_ms
    
    Returns:
        Tempo score dictionary
    """
    # Extract phase durations
    stance_start = events.get('stance_start_ms', 0)
    load_start = events.get('load_start_ms', 0)
    stride_start = events.get('stride_start_ms', 0)
    launch_start = events.get('launch_start_ms', 0)
    contact = events.get('contact_ms', 0)
    
    # Calculate phase durations
    load_duration = stride_start - load_start if stride_start > load_start else 0
    launch_duration = contact - launch_start if contact > launch_start else 0
    contact_duration = 50  # Assume ~50ms for contact phase (typical)
    
    return calculate_tempo_score(
        load_duration_ms=load_duration,
        launch_duration_ms=launch_duration,
        contact_duration_ms=contact_duration
    )


def analyze_tempo_consistency(tempo_scores: List[Dict]) -> Dict:
    """
    Analyze tempo consistency across multiple swings
    
    Args:
        tempo_scores: List of tempo score dictionaries from multiple swings
    
    Returns:
        Dictionary with consistency metrics:
        {
            'avg_ratio': 2.15,
            'std_dev': 0.18,
            'cv_percent': 8.4,
            'consistency_rating': 'EXCELLENT',
            'category_distribution': {'Balanced': 4, 'Quick Trigger': 1}
        }
    """
    if not tempo_scores:
        return {
            'avg_ratio': 0.0,
            'std_dev': 0.0,
            'cv_percent': 0.0,
            'consistency_rating': 'N/A',
            'category_distribution': {}
        }
    
    # Extract ratios
    ratios = [score['ratio'] for score in tempo_scores]
    
    # Calculate statistics
    avg_ratio = sum(ratios) / len(ratios)
    variance = sum((r - avg_ratio) ** 2 for r in ratios) / len(ratios)
    std_dev = variance ** 0.5
    cv_percent = (std_dev / avg_ratio * 100) if avg_ratio > 0 else 0
    
    # Determine consistency rating
    if cv_percent < 5:
        consistency_rating = 'EXCELLENT'
    elif cv_percent < 10:
        consistency_rating = 'VERY GOOD'
    elif cv_percent < 15:
        consistency_rating = 'GOOD'
    elif cv_percent < 20:
        consistency_rating = 'FAIR'
    else:
        consistency_rating = 'NEEDS IMPROVEMENT'
    
    # Count category distribution
    category_distribution = {}
    for score in tempo_scores:
        category = score['category']
        category_distribution[category] = category_distribution.get(category, 0) + 1
    
    return {
        'avg_ratio': round(avg_ratio, 2),
        'std_dev': round(std_dev, 3),
        'cv_percent': round(cv_percent, 1),
        'consistency_rating': consistency_rating,
        'category_distribution': category_distribution
    }


# Example usage
if __name__ == "__main__":
    # Example: Calculate tempo for a balanced swing
    tempo = calculate_tempo_score(
        load_duration_ms=633,  # 76 frames at 120 FPS
        launch_duration_ms=317,  # 38 frames at 120 FPS
        contact_duration_ms=250   # 30 frames at 120 FPS
    )
    
    print("Tempo Score Example:")
    print(f"  Load: {tempo['load_frames']} frames ({tempo['load_duration_ms']}ms)")
    print(f"  Launch: {tempo['launch_frames']} frames ({tempo['launch_duration_ms']}ms)")
    print(f"  Contact: {tempo['contact_frames']} frames ({tempo['contact_duration_ms']}ms)")
    print(f"  Ratio: {tempo['ratio']}")
    print(f"  Category: {tempo['category']}")
    print(f"  Description: {tempo['description']}")
