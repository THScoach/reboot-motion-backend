"""
PRIORITY 13: VIDEO-ENHANCED ANALYSIS API
=========================================

Extends Priority 12 API to include video recommendations for each drill
Integrates video library with correction plans
"""

import sys
from pathlib import Path

# Add physics_engine to path
sys.path.insert(0, str(Path(__file__).parent / "physics_engine"))

from priority_12_api_enhancement import enhance_analysis_with_priority_10_11
from video_library import get_video_library


def enhance_analysis_with_videos(
    # Existing analysis data
    ground_score: int,
    engine_score: int,
    weapon_score: int,
    
    # Athlete data
    height_inches: float,
    wingspan_inches: float,
    weight_lbs: float,
    age: int,
    bat_weight_oz: int = 30,
    
    # Optional actual bat speed from sensor
    actual_bat_speed_mph: float = None,
    
    # Optional energy data from video analysis
    rotation_ke_joules: float = None,
    translation_ke_joules: float = None,
    
    # Video options
    include_videos: bool = True,
    max_videos_per_drill: int = 3
):
    """
    Enhanced analysis with Priority 9 + 10 + 11 + 13 (Video Library)
    
    Returns complete analysis dict with:
    - Motor preference detection (Priority 11)
    - Adjusted scores (Priority 11)
    - Kinetic capacity (Priority 9)
    - Gap analysis (Priority 9)
    - Personalized recommendations (Priority 10)
    - Video demonstrations for each drill (Priority 13) ⭐ NEW
    """
    
    # Get base analysis from Priority 12
    result = enhance_analysis_with_priority_10_11(
        ground_score=ground_score,
        engine_score=engine_score,
        weapon_score=weapon_score,
        height_inches=height_inches,
        wingspan_inches=wingspan_inches,
        weight_lbs=weight_lbs,
        age=age,
        bat_weight_oz=bat_weight_oz,
        actual_bat_speed_mph=actual_bat_speed_mph,
        rotation_ke_joules=rotation_ke_joules,
        translation_ke_joules=translation_ke_joules
    )
    
    # Add video recommendations if requested
    if include_videos:
        library = get_video_library()
        
        # Enhance each drill with video recommendations
        drills_with_videos = []
        for drill in result['correction_plan']['drills']:
            drill_dict = dict(drill)  # Convert to dict if needed
            
            # Get videos for this drill
            drill_id = drill_dict['drill_id']
            videos = library.get_videos_for_drill(drill_id)
            
            # Limit number of videos
            videos = videos[:max_videos_per_drill]
            
            # Add video data to drill
            drill_dict['videos'] = [
                {
                    'video_id': v.video_id,
                    'title': v.title,
                    'description': v.description,
                    'source': v.source.value,
                    'source_url': v.source_url,
                    'thumbnail_url': v.thumbnail_url,
                    'duration_seconds': v.duration_seconds,
                    'coaching_points': v.coaching_points,
                    'view_count': v.view_count
                }
                for v in videos
            ]
            
            drills_with_videos.append(drill_dict)
        
        # Replace drills with video-enhanced version
        result['correction_plan']['drills'] = drills_with_videos
        
        # Add featured videos for general education
        featured_videos = library.get_featured_videos(limit=5)
        result['featured_videos'] = [
            {
                'video_id': v.video_id,
                'title': v.title,
                'description': v.description,
                'source': v.source.value,
                'source_url': v.source_url,
                'thumbnail_url': v.thumbnail_url,
                'duration_seconds': v.duration_seconds,
                'category': v.category.value,
                'tags': list(v.tags),
                'featured': v.featured
            }
            for v in featured_videos
        ]
        
        # Add motor-preference specific video recommendations
        motor_pref = result['motor_preference']['preference']
        motor_tags = {motor_pref.lower()}  # e.g., {'spinner'}
        
        motor_videos = library.search_videos(tags=motor_tags, featured_only=False)[:3]
        result['motor_preference_videos'] = [
            {
                'video_id': v.video_id,
                'title': v.title,
                'description': v.description,
                'source': v.source.value,
                'source_url': v.source_url,
                'thumbnail_url': v.thumbnail_url,
                'duration_seconds': v.duration_seconds
            }
            for v in motor_videos
        ]
    
    return result


# Test function
if __name__ == "__main__":
    # Test with Eric Williams data
    result = enhance_analysis_with_videos(
        ground_score=38,
        engine_score=58,
        weapon_score=55,
        height_inches=68,
        wingspan_inches=69,
        weight_lbs=190,
        age=33,
        bat_weight_oz=30,
        actual_bat_speed_mph=67.0,
        rotation_ke_joules=3743,
        translation_ke_joules=421,
        include_videos=True,
        max_videos_per_drill=2
    )
    
    print("=" * 80)
    print("PRIORITY 13: VIDEO-ENHANCED ANALYSIS TEST")
    print("=" * 80)
    
    print(f"\n🧬 Motor Preference: {result['motor_preference']['preference'].upper()}")
    
    print(f"\n🎯 Correction Plan with Videos:")
    for drill in result['correction_plan']['drills']:
        print(f"\n   📚 {drill['drill_name']} ({drill['stage']})")
        if drill.get('videos'):
            print(f"      Videos: {len(drill['videos'])}")
            for video in drill['videos']:
                print(f"         - {video['title']} ({video['duration_seconds']}s)")
        else:
            print(f"      Videos: None available")
    
    print(f"\n🌟 Featured Videos: {len(result.get('featured_videos', []))}")
    for video in result.get('featured_videos', [])[:3]:
        print(f"   - {video['title']}")
    
    print(f"\n🎓 Motor Preference Videos: {len(result.get('motor_preference_videos', []))}")
    for video in result.get('motor_preference_videos', []):
        print(f"   - {video['title']}")
    
    print("\n✅ Video-Enhanced Analysis Working!")
