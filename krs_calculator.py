"""
Catching Barrels - KRS Calculator
==================================

KRS™ (Kinetic Realization Score) Calculation Engine

KRS = (Creation Score + Transfer Score) / 2

Creation Score: How much power you generate (Body)
Transfer Score: How efficiently you deliver it (Bat)

Author: Builder 2
Date: 2025-12-25
"""

from typing import Dict, Tuple, Optional
from player_report_schema import KRSLevel, DataSource, Confidence


# ============================================================================
# KRS LEVEL THRESHOLDS
# ============================================================================

KRS_LEVELS = {
    KRSLevel.FOUNDATION: (0, 40, "🌱"),    # 0-39
    KRSLevel.BUILDING: (40, 60, "🔧"),     # 40-59
    KRSLevel.DEVELOPING: (60, 75, "📈"),   # 60-74
    KRSLevel.ADVANCED: (75, 90, "⭐"),     # 75-89
    KRSLevel.ELITE: (90, 100, "🏆"),       # 90-100
}


def get_krs_level(krs: float) -> Tuple[KRSLevel, str, float]:
    """
    Get KRS level, emoji, and points to next level
    
    Args:
        krs: KRS score (0-100)
        
    Returns:
        (level, emoji, points_to_next)
    """
    for level, (min_score, max_score, emoji) in KRS_LEVELS.items():
        if min_score <= krs < max_score:
            points_to_next = max_score - krs
            return level, emoji, points_to_next
    
    # If krs >= 90, it's ELITE
    return KRSLevel.ELITE, "🏆", 0.0


# ============================================================================
# CREATION SCORE CALCULATION
# ============================================================================

def calculate_creation_score(
    ground_flow_score: float,  # 0-10
    engine_flow_score: float,  # 0-10
    bat_speed_mph: Optional[float] = None,
    player_weight_lbs: Optional[float] = None,
    player_height_inches: Optional[float] = None,
) -> float:
    """
    Calculate Creation Score (0-100)
    
    Creation = How much power you generate in your body
    
    Components:
    - Ground Flow (40%): Stance, load, stride, plant
    - Engine Flow (40%): Pelvis, hips, torso, sequencing
    - Physical Capacity (20%): Size, strength, athleticism
    
    Args:
        ground_flow_score: Ground flow score (0-10)
        engine_flow_score: Engine flow score (0-10)
        bat_speed_mph: Actual bat speed (if available)
        player_weight_lbs: Player weight
        player_height_inches: Player height
        
    Returns:
        Creation score (0-100)
    """
    
    # Convert 0-10 scores to 0-100
    ground_contribution = (ground_flow_score / 10) * 100 * 0.4
    engine_contribution = (engine_flow_score / 10) * 100 * 0.4
    
    # Physical capacity estimation (simplified)
    capacity_contribution = 0
    if player_weight_lbs and player_height_inches:
        # Normalize by typical values (72", 185 lbs)
        weight_factor = player_weight_lbs / 185.0
        height_factor = player_height_inches / 72.0
        capacity_factor = (weight_factor + height_factor) / 2
        capacity_contribution = min(capacity_factor * 100, 100) * 0.2
    else:
        # Default to 50% if no physical data
        capacity_contribution = 50 * 0.2
    
    creation_score = ground_contribution + engine_contribution + capacity_contribution
    
    return min(max(creation_score, 0), 100)


# ============================================================================
# TRANSFER SCORE CALCULATION
# ============================================================================

def calculate_transfer_score(
    kinetic_chain_score: float,  # 0-100
    lead_leg_score: float,  # 0-100
    timing_score: float,  # 0-100
    weapon_score: Optional[float] = None,  # 0-100 (if available)
) -> float:
    """
    Calculate Transfer Score (0-100)
    
    Transfer = How efficiently you deliver power to the ball
    
    Components:
    - Kinetic Chain (35%): Hip→shoulder sequencing, ratios
    - Lead Leg (25%): Knee extension, stability, ground force
    - Timing (25%): Pelvis-torso timing, attack angle
    - Weapon (15%): Bat path, barrel control
    
    Args:
        kinetic_chain_score: Kinetic chain efficiency (0-100)
        lead_leg_score: Lead leg quality (0-100)
        timing_score: Timing quality (0-100)
        weapon_score: Weapon/bat path score (0-100, optional)
        
    Returns:
        Transfer score (0-100)
    """
    
    chain_contribution = kinetic_chain_score * 0.35
    lead_leg_contribution = lead_leg_score * 0.25
    timing_contribution = timing_score * 0.25
    
    # Weapon score (use if available, otherwise estimate from other scores)
    if weapon_score is not None:
        weapon_contribution = weapon_score * 0.15
    else:
        # Estimate weapon score from other components
        estimated_weapon = (kinetic_chain_score + timing_score) / 2
        weapon_contribution = estimated_weapon * 0.15
    
    transfer_score = (
        chain_contribution +
        lead_leg_contribution +
        timing_contribution +
        weapon_contribution
    )
    
    return min(max(transfer_score, 0), 100)


# ============================================================================
# KRS CALCULATION
# ============================================================================

def calculate_krs(
    creation_score: float,
    transfer_score: float,
    previous_krs: Optional[float] = None,
    previous_creation: Optional[float] = None,
    previous_transfer: Optional[float] = None,
    data_source: DataSource = DataSource.VIDEO_ANALYSIS,
) -> Dict:
    """
    Calculate complete KRS metrics
    
    Args:
        creation_score: Creation score (0-100)
        transfer_score: Transfer score (0-100)
        previous_krs: Previous session's KRS (for trends)
        previous_creation: Previous creation score
        previous_transfer: Previous transfer score
        data_source: Source of biomechanical data
        
    Returns:
        Dict with KRS metrics
    """
    
    # Calculate KRS total
    krs_total = (creation_score + transfer_score) / 2
    
    # Get level and emoji
    level, emoji, points_to_next = get_krs_level(krs_total)
    
    # Calculate changes (trends)
    krs_change = krs_total - previous_krs if previous_krs is not None else 0
    creation_change = creation_score - previous_creation if previous_creation is not None else 0
    transfer_change = transfer_score - previous_transfer if previous_transfer is not None else 0
    
    # Determine confidence based on data source
    confidence = {
        DataSource.VIDEO_ANALYSIS: Confidence.STANDARD,
        DataSource.ADVANCED_BIOMECHANICS: Confidence.ADVANCED,
        DataSource.ELITE_LAB_SESSION: Confidence.ELITE,
    }.get(data_source, Confidence.STANDARD)
    
    return {
        "total": round(krs_total, 1),
        "level": level,
        "emoji": emoji,
        "points_to_next_level": round(points_to_next, 1),
        "creation_score": round(creation_score, 1),
        "transfer_score": round(transfer_score, 1),
        "krs_change": round(krs_change, 1),
        "creation_change": round(creation_change, 1),
        "transfer_change": round(transfer_change, 1),
        "data_source": data_source,
        "confidence": confidence,
    }


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def estimate_capacity_bat_speed(
    player_height_inches: float,
    player_weight_lbs: float,
    wingspan_inches: Optional[float] = None,
) -> float:
    """
    Estimate capacity bat speed based on anthropometrics
    
    This is a simplified model. In production, use more sophisticated
    biomechanical models.
    
    Args:
        player_height_inches: Player height
        player_weight_lbs: Player weight
        wingspan_inches: Wingspan (optional)
        
    Returns:
        Estimated capacity bat speed (mph)
    """
    
    # Base capacity from weight (strength proxy)
    weight_factor = player_weight_lbs / 185.0  # Normalize to average
    base_capacity = 75 + (weight_factor - 1) * 10  # 75 mph baseline
    
    # Height/leverage adjustment
    height_factor = player_height_inches / 72.0
    leverage_bonus = (height_factor - 1) * 5
    
    # Wingspan bonus (if available)
    wingspan_bonus = 0
    if wingspan_inches:
        ape_index = wingspan_inches - player_height_inches
        if ape_index > 0:
            wingspan_bonus = ape_index * 0.3  # ~0.3 mph per inch of positive ape
    
    capacity = base_capacity + leverage_bonus + wingspan_bonus
    
    return round(capacity, 1)


def calculate_on_table_power(
    capacity_bat_speed: float,
    actual_bat_speed: float,
) -> Dict:
    """
    Calculate power left "on the table"
    
    Args:
        capacity_bat_speed: Theoretical max bat speed
        actual_bat_speed: Actual bat speed
        
    Returns:
        Dict with capacity, actual, and gap metrics
    """
    
    gap_mph = capacity_bat_speed - actual_bat_speed
    gap_percentage = (gap_mph / capacity_bat_speed) * 100 if capacity_bat_speed > 0 else 0
    
    return {
        "capacity_mph": round(capacity_bat_speed, 1),
        "actual_mph": round(actual_bat_speed, 1),
        "gap_mph": round(gap_mph, 1),
        "gap_percentage": round(gap_percentage, 1),
    }


# ============================================================================
# MAIN CALCULATOR
# ============================================================================

def calculate_full_krs_report(
    # Current session metrics
    ground_flow: float,
    engine_flow: float,
    kinetic_chain: float,
    lead_leg: float,
    timing: float,
    bat_speed_mph: float,
    
    # Player info
    player_height_inches: float,
    player_weight_lbs: float,
    wingspan_inches: Optional[float] = None,
    
    # Previous session (for trends)
    previous_krs: Optional[float] = None,
    previous_creation: Optional[float] = None,
    previous_transfer: Optional[float] = None,
    
    # Data quality
    data_source: DataSource = DataSource.VIDEO_ANALYSIS,
) -> Dict:
    """
    Calculate complete KRS report with all metrics
    
    This is the main function to call for full KRS calculation.
    
    Returns:
        Complete KRS metrics dict
    """
    
    # Calculate Creation Score
    creation = calculate_creation_score(
        ground_flow_score=ground_flow,
        engine_flow_score=engine_flow,
        bat_speed_mph=bat_speed_mph,
        player_weight_lbs=player_weight_lbs,
        player_height_inches=player_height_inches,
    )
    
    # Calculate Transfer Score
    transfer = calculate_transfer_score(
        kinetic_chain_score=kinetic_chain,
        lead_leg_score=lead_leg,
        timing_score=timing,
    )
    
    # Calculate KRS
    krs_metrics = calculate_krs(
        creation_score=creation,
        transfer_score=transfer,
        previous_krs=previous_krs,
        previous_creation=previous_creation,
        previous_transfer=previous_transfer,
        data_source=data_source,
    )
    
    # Calculate capacity and gaps
    capacity_speed = estimate_capacity_bat_speed(
        player_height_inches=player_height_inches,
        player_weight_lbs=player_weight_lbs,
        wingspan_inches=wingspan_inches,
    )
    
    on_table = calculate_on_table_power(
        capacity_bat_speed=capacity_speed,
        actual_bat_speed=bat_speed_mph,
    )
    
    return {
        **krs_metrics,
        "capacity": {
            "bat_speed_mph": capacity_speed,
        },
        "on_table": on_table,
    }


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == "__main__":
    # Example: Calculate KRS for a player
    result = calculate_full_krs_report(
        ground_flow=7.2,
        engine_flow=6.5,
        kinetic_chain=65,
        lead_leg=70,
        timing=75,
        bat_speed_mph=72.5,
        player_height_inches=72,
        player_weight_lbs=185,
        wingspan_inches=74,
    )
    
    print("KRS Calculation Result:")
    print(f"  KRS Total: {result['total']} {result['emoji']}")
    print(f"  Level: {result['level'].value}")
    print(f"  Creation: {result['creation_score']}")
    print(f"  Transfer: {result['transfer_score']}")
    print(f"  Capacity: {result['capacity']['bat_speed_mph']} mph")
    print(f"  On Table: {result['on_table']['gap_mph']} mph")
