"""
Profile Comparison System
Compare player metrics to age-appropriate benchmarks

Part of Priority 4: Motor Profile Classification Refinement
"""

from typing import Dict, List
import logging

logger = logging.getLogger(__name__)


class ProfileComparison:
    """
    Compare player performance to age-appropriate benchmarks
    Provides percentile rankings and rating classifications
    """
    
    # Age-based benchmarks (from research, MLB data, and Reboot Motion insights)
    BENCHMARKS = {
        'youth': {  # Ages 10-13
            'age_range': (10, 13),
            'bat_speed_mph': {
                'elite': 55,
                'above_avg': 50,
                'avg': 45,
                'below_avg': 40
            },
            'exit_velocity_mph': {
                'elite': 75,
                'above_avg': 70,
                'avg': 65,
                'below_avg': 60
            },
            'ground_score': {
                'elite': 80,
                'above_avg': 70,
                'avg': 60,
                'below_avg': 50
            },
            'engine_score': {
                'elite': 80,
                'above_avg': 70,
                'avg': 60,
                'below_avg': 50
            },
            'weapon_score': {
                'elite': 75,
                'above_avg': 65,
                'avg': 55,
                'below_avg': 45
            }
        },
        'high_school': {  # Ages 14-18
            'age_range': (14, 18),
            'bat_speed_mph': {
                'elite': 70,
                'above_avg': 65,
                'avg': 60,
                'below_avg': 55
            },
            'exit_velocity_mph': {
                'elite': 95,
                'above_avg': 88,
                'avg': 82,
                'below_avg': 76
            },
            'ground_score': {
                'elite': 85,
                'above_avg': 75,
                'avg': 65,
                'below_avg': 55
            },
            'engine_score': {
                'elite': 85,
                'above_avg': 75,
                'avg': 65,
                'below_avg': 55
            },
            'weapon_score': {
                'elite': 80,
                'above_avg': 70,
                'avg': 60,
                'below_avg': 50
            }
        },
        'college': {  # Ages 18-23
            'age_range': (18, 23),
            'bat_speed_mph': {
                'elite': 75,
                'above_avg': 72,
                'avg': 68,
                'below_avg': 64
            },
            'exit_velocity_mph': {
                'elite': 102,
                'above_avg': 96,
                'avg': 90,
                'below_avg': 84
            },
            'ground_score': {
                'elite': 88,
                'above_avg': 78,
                'avg': 70,
                'below_avg': 60
            },
            'engine_score': {
                'elite': 88,
                'above_avg': 78,
                'avg': 70,
                'below_avg': 60
            },
            'weapon_score': {
                'elite': 85,
                'above_avg': 75,
                'avg': 65,
                'below_avg': 55
            }
        },
        'adult': {  # Ages 23-35
            'age_range': (23, 35),
            'bat_speed_mph': {
                'elite': 80,
                'above_avg': 75,
                'avg': 70,
                'below_avg': 65
            },
            'exit_velocity_mph': {
                'elite': 108,
                'above_avg': 100,
                'avg': 93,
                'below_avg': 86
            },
            'ground_score': {
                'elite': 90,
                'above_avg': 80,
                'avg': 70,
                'below_avg': 60
            },
            'engine_score': {
                'elite': 90,
                'above_avg': 80,
                'avg': 70,
                'below_avg': 60
            },
            'weapon_score': {
                'elite': 88,
                'above_avg': 78,
                'avg': 68,
                'below_avg': 58
            }
        },
        'pro': {  # MLB/Professional level
            'age_range': (23, 40),
            'bat_speed_mph': {
                'elite': 85,
                'above_avg': 80,
                'avg': 75,
                'below_avg': 72
            },
            'exit_velocity_mph': {
                'elite': 115,
                'above_avg': 108,
                'avg': 100,
                'below_avg': 94
            },
            'ground_score': {
                'elite': 92,
                'above_avg': 85,
                'avg': 78,
                'below_avg': 70
            },
            'engine_score': {
                'elite': 92,
                'above_avg': 85,
                'avg': 78,
                'below_avg': 70
            },
            'weapon_score': {
                'elite': 90,
                'above_avg': 83,
                'avg': 75,
                'below_avg': 68
            }
        }
    }
    
    def __init__(self):
        pass
    
    def _determine_age_group(self, age: int) -> str:
        """
        Determine age group from age
        
        Args:
            age: Player age in years
            
        Returns:
            Age group key ('youth', 'high_school', 'college', 'adult', 'pro')
        """
        if age <= 13:
            return 'youth'
        elif age <= 18:
            return 'high_school'
        elif age <= 23:
            return 'college'
        elif age <= 35:
            return 'adult'
        else:
            return 'adult'  # Masters/veteran
    
    def _get_rating(self, value: float, benchmarks: Dict) -> str:
        """
        Get rating classification for a metric
        
        Args:
            value: Metric value
            benchmarks: Dictionary with elite/above_avg/avg/below_avg thresholds
            
        Returns:
            Rating: 'ELITE', 'ABOVE_AVERAGE', 'AVERAGE', 'BELOW_AVERAGE'
        """
        if value >= benchmarks['elite']:
            return 'ELITE'
        elif value >= benchmarks['above_avg']:
            return 'ABOVE_AVERAGE'
        elif value >= benchmarks['avg']:
            return 'AVERAGE'
        else:
            return 'BELOW_AVERAGE'
    
    def _estimate_percentile(self, value: float, benchmarks: Dict) -> int:
        """
        Estimate percentile rank within age group
        
        Simplified model:
        - Elite (90th percentile) and above: 90-100
        - Above Average to Elite: 70-90
        - Average to Above Average: 40-70
        - Below Average to Average: 20-40
        - Below Below Average: 0-20
        
        Args:
            value: Metric value
            benchmarks: Dictionary with thresholds
            
        Returns:
            Estimated percentile (0-100)
        """
        elite = benchmarks['elite']
        above_avg = benchmarks['above_avg']
        avg = benchmarks['avg']
        below_avg = benchmarks['below_avg']
        
        if value >= elite:
            # 90-100 percentile
            excess = value - elite
            range_size = elite - above_avg
            pct = 90 + min((excess / range_size) * 10, 10)
            return int(min(pct, 99))
        elif value >= above_avg:
            # 70-90 percentile
            progress = (value - above_avg) / (elite - above_avg)
            pct = 70 + (progress * 20)
            return int(pct)
        elif value >= avg:
            # 40-70 percentile
            progress = (value - avg) / (above_avg - avg)
            pct = 40 + (progress * 30)
            return int(pct)
        elif value >= below_avg:
            # 20-40 percentile
            progress = (value - below_avg) / (avg - below_avg)
            pct = 20 + (progress * 20)
            return int(pct)
        else:
            # 0-20 percentile
            deficit = below_avg - value
            range_size = avg - below_avg
            pct = 20 - min((deficit / range_size) * 20, 20)
            return int(max(pct, 1))
    
    def compare_metric(
        self,
        metric_name: str,
        value: float,
        age_group: str
    ) -> Dict:
        """
        Compare a single metric to benchmarks
        
        Args:
            metric_name: Name of metric (e.g., 'bat_speed_mph')
            value: Metric value
            age_group: Age group key
            
        Returns:
            Comparison dictionary
        """
        if age_group not in self.BENCHMARKS:
            age_group = 'adult'
        
        if metric_name not in self.BENCHMARKS[age_group]:
            return {
                'value': round(value, 1),
                'rating': 'UNKNOWN',
                'percentile': 50,
                'error': f'Metric {metric_name} not found in benchmarks'
            }
        
        benchmarks = self.BENCHMARKS[age_group][metric_name]
        rating = self._get_rating(value, benchmarks)
        percentile = self._estimate_percentile(value, benchmarks)
        
        return {
            'value': round(value, 1),
            'rating': rating,
            'percentile': percentile,
            'benchmark_elite': benchmarks['elite'],
            'benchmark_avg': benchmarks['avg'],
            'vs_elite': round(value - benchmarks['elite'], 1),
            'vs_avg': round(value - benchmarks['avg'], 1)
        }
    
    def compare_to_benchmarks(
        self,
        player_metrics: Dict,
        age: int
    ) -> Dict:
        """
        Compare player metrics to age-appropriate benchmarks
        
        Args:
            player_metrics: Dictionary with player metrics
                {
                    'bat_speed_mph': 76.0,
                    'exit_velocity_mph': 100.0,
                    'ground_score': 72,
                    'engine_score': 85,
                    'weapon_score': 40
                }
            age: Player age in years
            
        Returns:
            Complete comparison dictionary
        """
        age_group = self._determine_age_group(age)
        
        comparisons = {
            'age': age,
            'age_group': age_group,
            'age_range': f"{self.BENCHMARKS[age_group]['age_range'][0]}-{self.BENCHMARKS[age_group]['age_range'][1]}"
        }
        
        # Compare each metric
        metrics_to_compare = [
            'bat_speed_mph',
            'exit_velocity_mph',
            'ground_score',
            'engine_score',
            'weapon_score'
        ]
        
        for metric in metrics_to_compare:
            if metric in player_metrics:
                comparisons[metric] = self.compare_metric(
                    metric,
                    player_metrics[metric],
                    age_group
                )
        
        # Calculate overall rating (average of all ratings)
        ratings = []
        for metric in metrics_to_compare:
            if metric in comparisons and isinstance(comparisons[metric], dict):
                rating = comparisons[metric].get('rating')
                if rating == 'ELITE':
                    ratings.append(4)
                elif rating == 'ABOVE_AVERAGE':
                    ratings.append(3)
                elif rating == 'AVERAGE':
                    ratings.append(2)
                elif rating == 'BELOW_AVERAGE':
                    ratings.append(1)
        
        if ratings:
            avg_rating_score = sum(ratings) / len(ratings)
            if avg_rating_score >= 3.5:
                overall_rating = 'ELITE'
            elif avg_rating_score >= 2.5:
                overall_rating = 'ABOVE_AVERAGE'
            elif avg_rating_score >= 1.5:
                overall_rating = 'AVERAGE'
            else:
                overall_rating = 'BELOW_AVERAGE'
        else:
            overall_rating = 'UNKNOWN'
        
        comparisons['overall_rating'] = overall_rating
        
        return comparisons
    
    def get_age_group_benchmarks(self, age: int) -> Dict:
        """
        Get all benchmarks for a specific age group
        
        Args:
            age: Player age
            
        Returns:
            Dictionary of benchmarks for that age group
        """
        age_group = self._determine_age_group(age)
        return self.BENCHMARKS[age_group].copy()


if __name__ == "__main__":
    # Test the comparison system
    print("="*70)
    print("PROFILE COMPARISON SYSTEM TEST")
    print("="*70)
    
    comparison = ProfileComparison()
    
    # Test Case 1: Eric Williams (age 33, adult)
    print("\nTest 1: Eric Williams (33 years old, Adult)")
    print("-" * 70)
    eric_metrics = {
        'bat_speed_mph': 76.0,
        'exit_velocity_mph': 100.0,
        'ground_score': 72,
        'engine_score': 85,
        'weapon_score': 40
    }
    result = comparison.compare_to_benchmarks(eric_metrics, 33)
    
    print(f"Age Group: {result['age_group']} ({result['age_range']} years)")
    print(f"\nBat Speed: {result['bat_speed_mph']['value']} mph")
    print(f"  Rating: {result['bat_speed_mph']['rating']}")
    print(f"  Percentile: {result['bat_speed_mph']['percentile']}th")
    print(f"  vs Elite: {result['bat_speed_mph']['vs_elite']:+.1f} mph")
    print(f"  vs Average: {result['bat_speed_mph']['vs_avg']:+.1f} mph")
    
    print(f"\nGround Score: {result['ground_score']['value']}/100")
    print(f"  Rating: {result['ground_score']['rating']}")
    print(f"  Percentile: {result['ground_score']['percentile']}th")
    
    print(f"\nEngine Score: {result['engine_score']['value']}/100")
    print(f"  Rating: {result['engine_score']['rating']}")
    print(f"  Percentile: {result['engine_score']['percentile']}th")
    
    print(f"\nWeapon Score: {result['weapon_score']['value']}/100")
    print(f"  Rating: {result['weapon_score']['rating']}")
    print(f"  Percentile: {result['weapon_score']['percentile']}th")
    
    print(f"\nOverall Rating: {result['overall_rating']}")
    
    # Test Case 2: Connor Gray (age 16, high school)
    print("\n\nTest 2: Connor Gray (16 years old, High School)")
    print("-" * 70)
    connor_metrics = {
        'bat_speed_mph': 57.5,
        'ground_score': 65,
        'engine_score': 70,
        'weapon_score': 55
    }
    result = comparison.compare_to_benchmarks(connor_metrics, 16)
    
    print(f"Age Group: {result['age_group']} ({result['age_range']} years)")
    print(f"\nBat Speed: {result['bat_speed_mph']['value']} mph")
    print(f"  Rating: {result['bat_speed_mph']['rating']}")
    print(f"  Percentile: {result['bat_speed_mph']['percentile']}th")
    
    print(f"\nOverall Rating: {result['overall_rating']}")
    
    # Test Case 3: Elite MLB player
    print("\n\nTest 3: Elite MLB Player (28 years old)")
    print("-" * 70)
    elite_metrics = {
        'bat_speed_mph': 82.0,
        'exit_velocity_mph': 110.0,
        'ground_score': 91,
        'engine_score': 93,
        'weapon_score': 89
    }
    result = comparison.compare_to_benchmarks(elite_metrics, 28)
    
    print(f"Age Group: {result['age_group']}")
    print(f"Bat Speed: {result['bat_speed_mph']['rating']} ({result['bat_speed_mph']['percentile']}th percentile)")
    print(f"Overall Rating: {result['overall_rating']}")
    
    print("\n" + "="*70)
