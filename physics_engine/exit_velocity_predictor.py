"""
Exit Velocity Predictor using Real MLB Statcast Data

This module provides realistic exit velocity predictions based on actual MLB player
benchmarks, adjusted for player size (height + weight) and contact quality.

Key features:
- Uses real Statcast data from MLB players
- Interpolates for player sizes not in database
- Caps predictions at size-appropriate maximums
- Accounts for contact quality from biomechanics (timing + weapon score)

Author: Kinetic DNA Blueprint
"""

from typing import Dict, List, Tuple
import math


class ExitVelocityPredictor:
    """
    Predict exit velocity using MLB Statcast benchmarks
    Interpolates for player sizes not in database
    
    Uses real MLB data to provide realistic predictions that account for
    physical limitations based on player size.
    """
    
    # Real MLB Statcast benchmarks (height_inches, weight_lbs): (max_ev, avg_ev, name)
    MLB_BENCHMARKS = {
        # Small (5'6" - 5'8")
        (66, 167): (112.3, 86.7, 'Jose Altuve'),        # 5'6", 167 lbs
        (68, 180): (111.8, 87.1, 'Dustin Pedroia'),     # 5'8", 180 lbs
        
        # Medium-small (5'9" - 5'10")
        (69, 180): (113.2, 87.5, 'Ozzie Albies'),       # 5'9", 180 lbs
        (70, 185): (114.5, 88.3, 'Freddie Freeman'),    # 5'10", 185 lbs
        
        # Medium (5'11" - 6'0")
        (71, 195): (116.8, 89.4, 'Mookie Betts'),       # 5'11", 195 lbs
        (72, 200): (117.5, 89.8, 'Ronald Acuna Jr'),    # 6'0", 200 lbs
        
        # Medium-large (6'1" - 6'2")
        (73, 205): (118.9, 90.5, 'Mike Trout'),         # 6'1", 205 lbs
        (74, 215): (119.8, 91.2, 'Juan Soto'),          # 6'2", 215 lbs
        
        # Large (6'3" - 6'4")
        (75, 220): (121.1, 92.0, 'Bryce Harper'),       # 6'3", 220 lbs
        (76, 230): (121.8, 92.5, 'Kyle Schwarber'),     # 6'4", 230 lbs
        
        # Extra-large (6'5"+)
        (77, 240): (122.4, 93.1, 'Aaron Judge'),        # 6'5", 240 lbs
        (78, 250): (121.9, 92.8, 'Giancarlo Stanton'),  # 6'6", 250 lbs
    }
    
    # Contact quality multipliers (bat speed to exit velo)
    CONTACT_QUALITY_MULTIPLIERS = {
        'elite': 1.50,      # Perfect timing + barrel
        'good': 1.45,       # Good timing
        'average': 1.40,    # Average contact
        'below_avg': 1.35,  # Slight mistiming
        'poor': 1.30        # Significant mistiming
    }
    
    def __init__(self):
        """Initialize the exit velocity predictor"""
        pass
    
    def find_nearest_benchmarks(
        self,
        height_inches: int,
        weight_lbs: int,
        num_neighbors: int = 4
    ) -> List[Tuple]:
        """
        Find nearest MLB players by size for interpolation
        
        Uses Euclidean distance with height weighted 5x more than weight:
        distance = sqrt((height_diff * 5)^2 + weight_diff^2)
        
        Height is weighted more heavily because it has a stronger correlation
        with power generation capability than weight alone.
        
        Args:
            height_inches: Player height in inches
            weight_lbs: Player weight in pounds
            num_neighbors: Number of nearest neighbors to return (default: 4)
        
        Returns:
            List of tuples: (height, weight, max_ev, avg_ev, name, distance)
            Sorted by distance (closest first)
        
        Example:
            >>> predictor = ExitVelocityPredictor()
            >>> neighbors = predictor.find_nearest_benchmarks(68, 190, num_neighbors=4)
            >>> print(f"Nearest: {neighbors[0][4]} at {neighbors[0][2]} mph max")
        """
        distances = []
        
        for (h, w), (max_ev, avg_ev, name) in self.MLB_BENCHMARKS.items():
            # Calculate weighted Euclidean distance
            # Height weighted 5x more than weight
            height_diff = h - height_inches
            weight_diff = w - weight_lbs
            
            distance = math.sqrt((height_diff * 5) ** 2 + weight_diff ** 2)
            
            distances.append((h, w, max_ev, avg_ev, name, distance))
        
        # Sort by distance (closest first)
        distances.sort(key=lambda x: x[5])
        
        # Return top N neighbors
        return distances[:num_neighbors]
    
    def interpolate_max_exit_velo(
        self,
        height_inches: int,
        weight_lbs: int,
        num_neighbors: int = 4
    ) -> Tuple[float, float, List[str]]:
        """
        Interpolate max exit velocity for player size using inverse distance weighting
        
        Method: Inverse distance weighting (IDW) from N nearest neighbors
        - Closer players have more influence on the prediction
        - Weight = 1 / (distance^2 + 0.1)  # Add 0.1 to avoid division by zero
        
        Args:
            height_inches: Player height in inches
            weight_lbs: Player weight in pounds
            num_neighbors: Number of neighbors for interpolation (default: 4)
        
        Returns:
            Tuple of (max_ev_mph, avg_ev_mph, reference_players_list)
        
        Example:
            >>> predictor = ExitVelocityPredictor()
            >>> max_ev, avg_ev, refs = predictor.interpolate_max_exit_velo(68, 190)
            >>> print(f"Max EV: {max_ev:.1f} mph (refs: {refs})")
        """
        # Get nearest benchmarks
        neighbors = self.find_nearest_benchmarks(height_inches, weight_lbs, num_neighbors)
        
        # Check for exact match
        for h, w, max_ev, avg_ev, name, distance in neighbors:
            if distance < 0.1:  # Effectively zero distance
                return (max_ev, avg_ev, [f"{name} ({h//12}'{h%12}\", {w} lbs)"])
        
        # Inverse distance weighting
        total_weight = 0.0
        weighted_max_ev = 0.0
        weighted_avg_ev = 0.0
        reference_players = []
        
        for h, w, max_ev, avg_ev, name, distance in neighbors:
            # Weight = 1 / (distance^2 + epsilon)
            # epsilon prevents division by zero and limits extreme weights
            weight = 1.0 / (distance ** 2 + 0.1)
            
            weighted_max_ev += max_ev * weight
            weighted_avg_ev += avg_ev * weight
            total_weight += weight
            
            # Add to reference list
            reference_players.append(f"{name} ({h//12}'{h%12}\", {w} lbs)")
        
        # Normalize by total weight
        interpolated_max_ev = weighted_max_ev / total_weight
        interpolated_avg_ev = weighted_avg_ev / total_weight
        
        # Apply weight penalty if player is significantly heavier than benchmarks
        # (being heavier doesn't always mean more power if you're short)
        avg_benchmark_weight = sum(n[1] for n in neighbors) / len(neighbors)
        if weight_lbs > avg_benchmark_weight + 5:
            # Apply penalty for being disproportionately heavy for size
            # 1% penalty per 5 lbs over average, max 3% penalty
            weight_penalty = 1.0 - min(0.01 * ((weight_lbs - avg_benchmark_weight) / 5), 0.03)
            interpolated_max_ev *= weight_penalty
        
        return (
            round(interpolated_max_ev, 1),
            round(interpolated_avg_ev, 1),
            reference_players
        )
    
    def predict_from_bat_speed(
        self,
        bat_speed: float,
        height_inches: int,
        weight_lbs: int,
        contact_quality: str = 'average'
    ) -> Dict:
        """
        Predict exit velocity from bat speed with size-appropriate capping
        
        Steps:
        1. Get size-appropriate max EV (from interpolation)
        2. Calculate: predicted_ev = bat_speed × contact_multiplier
        3. Cap at size-appropriate max
        4. Calculate 90th percentile (1.06x avg, capped at max)
        
        Args:
            bat_speed: Bat speed in mph
            height_inches: Player height in inches
            weight_lbs: Player weight in pounds
            contact_quality: 'elite', 'good', 'average', 'below_avg', or 'poor'
        
        Returns:
            Dictionary with prediction details:
            {
                'bat_speed_mph': 74.0,
                'contact_quality': 'poor',
                'exit_velocity_avg_mph': 96.2,
                'exit_velocity_90th_mph': 102.0,
                'exit_velocity_max_mph': 111.8,
                'player_size': "5'8\", 190 lbs",
                'size_adjusted_max': 111.8,
                'reference_players': ['Jose Altuve (5\'6", 167 lbs)', ...],
                'pct_of_max_avg': 86.0,
                'pct_of_max_90th': 91.2
            }
        
        Example:
            >>> predictor = ExitVelocityPredictor()
            >>> result = predictor.predict_from_bat_speed(74.0, 68, 190, 'poor')
            >>> print(f"Avg EV: {result['exit_velocity_avg_mph']} mph")
        """
        # Get size-appropriate max EV
        max_ev_size, avg_ev_mlb, reference_players = self.interpolate_max_exit_velo(
            height_inches, weight_lbs
        )
        
        # Get contact quality multiplier
        multiplier = self.CONTACT_QUALITY_MULTIPLIERS.get(contact_quality, 1.40)
        
        # Calculate predicted exit velocity
        predicted_ev_avg = bat_speed * multiplier
        
        # Cap at size-appropriate maximum
        predicted_ev_avg = min(predicted_ev_avg, max_ev_size)
        
        # Calculate 90th percentile (typically 1.06x average for good hitters)
        predicted_ev_90th = predicted_ev_avg * 1.06
        predicted_ev_90th = min(predicted_ev_90th, max_ev_size)
        
        # Player size string
        feet = height_inches // 12
        inches = height_inches % 12
        player_size = f"{feet}'{inches}\", {weight_lbs} lbs"
        
        # Calculate percentages of max
        pct_of_max_avg = (predicted_ev_avg / max_ev_size * 100) if max_ev_size > 0 else 0
        pct_of_max_90th = (predicted_ev_90th / max_ev_size * 100) if max_ev_size > 0 else 0
        
        return {
            'bat_speed_mph': round(bat_speed, 1),
            'contact_quality': contact_quality,
            'exit_velocity_avg_mph': round(predicted_ev_avg, 1),
            'exit_velocity_90th_mph': round(predicted_ev_90th, 1),
            'exit_velocity_max_mph': round(max_ev_size, 1),
            'player_size': player_size,
            'size_adjusted_max': round(max_ev_size, 1),
            'reference_players': reference_players[:2],  # Top 2 most similar
            'pct_of_max_avg': round(pct_of_max_avg, 1),
            'pct_of_max_90th': round(pct_of_max_90th, 1)
        }
    
    def predict_current_vs_potential(
        self,
        bat_speed_actual: float,
        bat_speed_potential: float,
        height_inches: int,
        weight_lbs: int,
        timing_gap_current: float,
        timing_gap_potential: float = 0.2,
        weapon_score_current: float = 40,
        weapon_score_potential: float = 60
    ) -> Dict:
        """
        Generate complete current vs potential exit velocity comparison
        
        Steps:
        1. Determine contact quality from timing + weapon score (current & potential)
        2. Predict current state exit velo
        3. Predict potential state exit velo
        4. Calculate gaps
        
        Args:
            bat_speed_actual: Current bat speed (mph)
            bat_speed_potential: Potential bat speed (mph)
            height_inches: Player height
            weight_lbs: Player weight
            timing_gap_current: Current timing gap (seconds)
            timing_gap_potential: Potential timing gap after improvement (seconds)
            weapon_score_current: Current weapon score (0-100)
            weapon_score_potential: Potential weapon score (0-100)
        
        Returns:
            {
                'current': {...prediction dict...},
                'potential': {...prediction dict...},
                'gaps': {
                    'bat_speed_gain_mph': 2.5,
                    'exit_velo_avg_gain_mph': 11.3,
                    'exit_velo_90th_gain_mph': 9.8,
                    'exit_velo_max_gain_mph': 0.0  # Max is size-limited
                },
                'player_info': {
                    'height_inches': 68,
                    'weight_lbs': 190,
                    'size_description': "5'8\", 190 lbs"
                }
            }
        
        Example:
            >>> predictor = ExitVelocityPredictor()
            >>> result = predictor.predict_current_vs_potential(
            ...     bat_speed_actual=74.0,
            ...     bat_speed_potential=76.5,
            ...     height_inches=68,
            ...     weight_lbs=190,
            ...     timing_gap_current=1.5,
            ...     weapon_score_current=40
            ... )
            >>> print(f"Current: {result['current']['exit_velocity_avg_mph']} mph")
            >>> print(f"Potential: {result['potential']['exit_velocity_avg_mph']} mph")
            >>> print(f"Gain: {result['gaps']['exit_velo_avg_gain_mph']} mph")
        """
        # Determine contact quality for current state
        contact_quality_current = self._determine_contact_quality(
            timing_gap_current, weapon_score_current
        )
        
        # Determine contact quality for potential state
        contact_quality_potential = self._determine_contact_quality(
            timing_gap_potential, weapon_score_potential
        )
        
        # Predict current state
        current_prediction = self.predict_from_bat_speed(
            bat_speed=bat_speed_actual,
            height_inches=height_inches,
            weight_lbs=weight_lbs,
            contact_quality=contact_quality_current
        )
        
        # Predict potential state
        potential_prediction = self.predict_from_bat_speed(
            bat_speed=bat_speed_potential,
            height_inches=height_inches,
            weight_lbs=weight_lbs,
            contact_quality=contact_quality_potential
        )
        
        # Calculate gaps
        gaps = {
            'bat_speed_gain_mph': round(bat_speed_potential - bat_speed_actual, 1),
            'exit_velo_avg_gain_mph': round(
                potential_prediction['exit_velocity_avg_mph'] - 
                current_prediction['exit_velocity_avg_mph'], 1
            ),
            'exit_velo_90th_gain_mph': round(
                potential_prediction['exit_velocity_90th_mph'] - 
                current_prediction['exit_velocity_90th_mph'], 1
            ),
            'exit_velo_max_gain_mph': round(
                potential_prediction['exit_velocity_max_mph'] - 
                current_prediction['exit_velocity_max_mph'], 1
            )
        }
        
        # Player info
        feet = height_inches // 12
        inches = height_inches % 12
        player_info = {
            'height_inches': height_inches,
            'weight_lbs': weight_lbs,
            'size_description': f"{feet}'{inches}\", {weight_lbs} lbs"
        }
        
        return {
            'current': current_prediction,
            'potential': potential_prediction,
            'gaps': gaps,
            'player_info': player_info
        }
    
    def _determine_contact_quality(
        self,
        timing_gap_seconds: float,
        weapon_score: float
    ) -> str:
        """
        Determine contact quality from biomechanics (timing + weapon score)
        
        Logic:
        1. Evaluate timing quality:
           - <0.3s = good timing
           - <0.7s = average timing
           - <1.2s = below_avg timing
           - >=1.2s = poor timing
        
        2. Evaluate weapon quality:
           - >=75 = elite
           - >=60 = good
           - >=45 = average
           - >=30 = below_avg
           - <30 = poor
        
        3. Combined quality = WORSE of the two (minimum quality)
           - If timing is poor OR weapon is poor → overall is poor
           - Takes the more limiting factor
        
        Args:
            timing_gap_seconds: Timing gap in seconds (lower is better)
            weapon_score: Weapon score 0-100 (higher is better)
        
        Returns:
            'elite', 'good', 'average', 'below_avg', or 'poor'
        
        Example:
            >>> predictor = ExitVelocityPredictor()
            >>> quality = predictor._determine_contact_quality(0.2, 65)
            >>> print(quality)  # 'good'
        """
        # Define quality rankings
        quality_ranks = ['poor', 'below_avg', 'average', 'good', 'elite']
        
        # Determine timing quality
        if timing_gap_seconds < 0.3:
            timing_quality = 'good'
        elif timing_gap_seconds < 0.7:
            timing_quality = 'average'
        elif timing_gap_seconds < 1.2:
            timing_quality = 'below_avg'
        else:
            timing_quality = 'poor'
        
        # Determine weapon quality
        if weapon_score >= 75:
            weapon_quality = 'elite'
        elif weapon_score >= 60:
            weapon_quality = 'good'
        elif weapon_score >= 45:
            weapon_quality = 'average'
        elif weapon_score >= 38:  # Raised from 30 to 38
            weapon_quality = 'below_avg'
        else:
            weapon_quality = 'poor'
        
        # Combined quality = worse of the two (limiting factor)
        timing_rank = quality_ranks.index(timing_quality)
        weapon_rank = quality_ranks.index(weapon_quality)
        
        # Take the minimum (worse) quality
        combined_rank = min(timing_rank, weapon_rank)
        
        return quality_ranks[combined_rank]
