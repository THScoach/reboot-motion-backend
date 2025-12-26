"""
PRIORITY 13: VIDEO LIBRARY SYSTEM
==================================

Video library management for drill demonstrations, coaching content,
and athlete education. Integrates with Priority 10 recommendations.

Features:
- Video metadata storage (title, description, duration, tags)
- Drill-to-video mapping
- Video search and filtering
- Support for multiple video sources (YouTube, Vimeo, S3, local)
- Thumbnail generation and caching
- View tracking and analytics
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import json


class VideoSource(Enum):
    """Video hosting sources"""
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    S3 = "s3"
    LOCAL = "local"
    CLOUDFLARE_STREAM = "cloudflare_stream"


class VideoCategory(Enum):
    """Video content categories"""
    DRILL = "drill"
    TECHNIQUE = "technique"
    CONCEPT = "concept"
    ASSESSMENT = "assessment"
    EXERCISE = "exercise"
    INTERVIEW = "interview"
    CASE_STUDY = "case_study"


class DrillStage(Enum):
    """Matches Priority 10 drill stages"""
    STAGE_1 = "Stage 1: Foundation/Isolation"
    STAGE_2 = "Stage 2: Integration/Combination"
    STAGE_3 = "Stage 3: Game-Speed Application"


@dataclass
class VideoMetadata:
    """Complete video metadata"""
    video_id: str
    title: str
    description: str
    source: VideoSource
    source_url: str
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    category: VideoCategory = VideoCategory.DRILL
    tags: Set[str] = field(default_factory=set)
    drill_ids: Set[str] = field(default_factory=set)
    drill_stage: Optional[DrillStage] = None
    coaching_points: List[str] = field(default_factory=list)
    equipment: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    view_count: int = 0
    featured: bool = False


class VideoLibrary:
    """
    Central video library management system
    Stores and retrieves drill demonstration videos
    """
    
    def __init__(self):
        """Initialize video library with sample content"""
        self.videos: Dict[str, VideoMetadata] = {}
        self._initialize_sample_library()
    
    
    def _initialize_sample_library(self):
        """
        Initialize library with sample drill videos
        
        NOTE: In production, these should be:
        1. Stored in a database (PostgreSQL, MongoDB)
        2. Managed through an admin interface
        3. Connected to actual video hosting (S3, Cloudflare Stream)
        
        For now, we use YouTube videos as examples
        """
        
        sample_videos = [
            # GROUND FORCE / STRIDE DRILLS (Stage 1)
            VideoMetadata(
                video_id="vid_step_through_001",
                title="Step Through Drill - Foundation",
                description="Learn the fundamental weight shift and ground force pattern. "
                           "This drill teaches proper stride timing and directional force.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",  # Placeholder
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=180,
                category=VideoCategory.DRILL,
                tags={"ground", "stride", "weight_shift", "foundation", "timing"},
                drill_ids={"step_drill_stage1", "drill_step_through"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Start with feet together",
                    "Step forward with front foot, feel weight shift",
                    "Drive off back leg into front leg",
                    "Focus on directional force toward pitcher"
                ],
                equipment=["bat", "none"],
                featured=True
            ),
            
            VideoMetadata(
                video_id="vid_weight_shift_001",
                title="Weight Shift Load Drill",
                description="Isolate and develop the loading phase. Learn to load properly "
                           "into the back hip before initiating rotation.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=240,
                category=VideoCategory.DRILL,
                tags={"ground", "load", "weight_shift", "foundation"},
                drill_ids={"drill_weight_shift_load"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Feel weight shift into back leg",
                    "Maintain balance and control",
                    "Don't over-rotate during load",
                    "Keep head steady"
                ],
                equipment=["bat"]
            ),
            
            # HIP ROTATION DRILLS (Stage 1 & 2)
            VideoMetadata(
                video_id="vid_hip_rotation_001",
                title="Hip-Only Rotation Drill",
                description="Isolate hip rotation without upper body involvement. "
                           "Builds awareness of hip-shoulder separation and sequencing.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=210,
                category=VideoCategory.DRILL,
                tags={"engine", "hip_rotation", "separation", "foundation"},
                drill_ids={"drill_hip_only_rotation"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Hold bat behind shoulders",
                    "Rotate hips only, shoulders stay back",
                    "Feel the stretch in torso",
                    "Back leg drives rotation"
                ],
                equipment=["bat"],
                featured=True
            ),
            
            VideoMetadata(
                video_id="vid_hip_rotation_arm_hold_002",
                title="Hip Rotation with Arm Hold - Integration",
                description="Progress hip rotation drill by adding arm constraint. "
                           "Develops proper sequencing and torso connection.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=195,
                category=VideoCategory.DRILL,
                tags={"engine", "hip_rotation", "separation", "integration"},
                drill_ids={"drill_hip_rotation_arm_hold"},
                drill_stage=DrillStage.STAGE_2,
                coaching_points=[
                    "Cross arms over chest",
                    "Rotate hips first, then torso follows",
                    "Maintain connection through core",
                    "Progressive acceleration"
                ],
                equipment=["bat"]
            ),
            
            # CONNECTION DRILLS
            VideoMetadata(
                video_id="vid_connection_ball_001",
                title="Connection Ball Roll-Back Drill",
                description="Develop and maintain proper connection between body and arms. "
                           "The ball ensures hands stay close to the body during rotation.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=225,
                category=VideoCategory.DRILL,
                tags={"engine", "connection", "hands", "foundation"},
                drill_ids={"drill_connection_ball"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Place ball between forearms and chest",
                    "Don't let ball drop during swing",
                    "Hands stay connected to body rotation",
                    "Feel the torso pulling the arms"
                ],
                equipment=["bat", "medicine_ball", "towel"],
                featured=True
            ),
            
            # TIMING & RHYTHM DRILLS
            VideoMetadata(
                video_id="vid_pause_quality_001",
                title="Pause Quality Emphasis Drill",
                description="Break down swing timing into distinct phases. "
                           "Helps identify and correct rushing or hesitation.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=270,
                category=VideoCategory.DRILL,
                tags={"timing", "rhythm", "foundation", "sequencing"},
                drill_ids={"pause_quality_emphasis", "drill_pause_quality"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Pause at load position (2 seconds)",
                    "Pause at separation (1 second)",
                    "Execute swing with rhythm",
                    "Focus on quality over speed"
                ],
                equipment=["bat", "tee"]
            ),
            
            # BARRIER DRILLS
            VideoMetadata(
                video_id="vid_backside_barrier_001",
                title="Backside Barrier Drill",
                description="Prevent premature weight shift and maintain back-side leverage. "
                           "Critical for spinners and maintaining rotational power.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=240,
                category=VideoCategory.DRILL,
                tags={"ground", "leverage", "spinner", "foundation"},
                drill_ids={"drill_backside_barrier"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Place chair or barrier behind back leg",
                    "Don't drift backward into barrier",
                    "Rotate over stable back leg",
                    "Feel the coil and leverage"
                ],
                equipment=["bat", "chair", "barrier"],
                featured=True
            ),
            
            # DIRECTION / BARREL PATH DRILLS
            VideoMetadata(
                video_id="vid_open_stance_45_001",
                title="Open Stance 45° Drill",
                description="Improve bat path direction and barrel control through the zone. "
                           "Open stance forces proper hand path and connection.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=255,
                category=VideoCategory.DRILL,
                tags={"weapon", "direction", "barrel_path", "foundation"},
                drill_ids={"open_stance_45", "drill_open_stance_45"},
                drill_stage=DrillStage.STAGE_1,
                coaching_points=[
                    "Start with feet at 45° angle",
                    "Focus on barrel staying in zone longer",
                    "Prevent casting or long path",
                    "Feel direct hand path to ball"
                ],
                equipment=["bat", "tee"]
            ),
            
            # GAME-SPEED APPLICATION (Stage 3)
            VideoMetadata(
                video_id="vid_game_speed_flow_001",
                title="Game-Speed Flow Drills",
                description="Apply corrected mechanics at game speed. "
                           "Progressive tempo work from soft toss to live pitching.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=420,
                category=VideoCategory.DRILL,
                tags={"game_speed", "application", "integration", "live"},
                drill_ids={"game_speed_flow", "drill_game_speed_flow"},
                drill_stage=DrillStage.STAGE_3,
                coaching_points=[
                    "Start with soft toss (50% speed)",
                    "Progress to front toss (75% speed)",
                    "Finish with live BP (100% speed)",
                    "Maintain quality mechanics at all speeds"
                ],
                equipment=["bat", "balls", "L-screen"],
                featured=True
            ),
            
            # STRENGTH & CONDITIONING VIDEOS
            VideoMetadata(
                video_id="vid_med_ball_slams_001",
                title="Split-Stance Medicine Ball Slams",
                description="Build explosive rotational power and ground force generation. "
                           "Key exercise for developing bat speed.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=180,
                category=VideoCategory.EXERCISE,
                tags={"strength", "power", "rotation", "ground_force"},
                drill_ids=set(),
                coaching_points=[
                    "Start in hitting stance",
                    "Load into back leg",
                    "Explosively rotate and slam ball",
                    "Follow swing mechanics pattern"
                ],
                equipment=["medicine_ball"]
            ),
            
            # CONCEPTUAL VIDEOS
            VideoMetadata(
                video_id="vid_motor_preference_explained_001",
                title="Understanding Motor Preference - Spinner vs Glider vs Launcher",
                description="Dr. Kwon explains the science behind motor preference detection "
                           "and why fair scoring matters for individual development.",
                source=VideoSource.YOUTUBE,
                source_url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                thumbnail_url="https://img.youtube.com/vi/dQw4w9WgXcQ/mqdefault.jpg",
                duration_seconds=600,
                category=VideoCategory.CONCEPT,
                tags={"motor_preference", "spinner", "glider", "launcher", "science"},
                coaching_points=[
                    "Body structure determines optimal force pattern",
                    "No preference is better than another",
                    "Train to your preference, don't fight it",
                    "Fair scoring adjusts for motor type"
                ],
                featured=True
            ),
        ]
        
        # Add all videos to library
        for video in sample_videos:
            self.videos[video.video_id] = video
    
    
    # ========================================
    # QUERY METHODS
    # ========================================
    
    def get_video(self, video_id: str) -> Optional[VideoMetadata]:
        """Get a specific video by ID"""
        return self.videos.get(video_id)
    
    
    def get_videos_for_drill(self, drill_id: str) -> List[VideoMetadata]:
        """Get all videos associated with a specific drill"""
        return [
            video for video in self.videos.values()
            if drill_id in video.drill_ids
        ]
    
    
    def get_videos_by_stage(self, stage: DrillStage) -> List[VideoMetadata]:
        """Get all videos for a specific drill stage"""
        return [
            video for video in self.videos.values()
            if video.drill_stage == stage
        ]
    
    
    def get_videos_by_category(self, category: VideoCategory) -> List[VideoMetadata]:
        """Get all videos in a category"""
        return [
            video for video in self.videos.values()
            if video.category == category
        ]
    
    
    def search_videos(
        self,
        query: str = None,
        tags: Set[str] = None,
        category: VideoCategory = None,
        drill_stage: DrillStage = None,
        featured_only: bool = False
    ) -> List[VideoMetadata]:
        """
        Search videos with multiple filters
        
        Args:
            query: Text search in title/description
            tags: Filter by tags (any match)
            category: Filter by category
            drill_stage: Filter by drill stage
            featured_only: Only return featured videos
        """
        results = list(self.videos.values())
        
        # Filter by featured
        if featured_only:
            results = [v for v in results if v.featured]
        
        # Filter by category
        if category:
            results = [v for v in results if v.category == category]
        
        # Filter by drill stage
        if drill_stage:
            results = [v for v in results if v.drill_stage == drill_stage]
        
        # Filter by tags (any match)
        if tags:
            results = [
                v for v in results
                if any(tag in v.tags for tag in tags)
            ]
        
        # Text search in title/description
        if query:
            query_lower = query.lower()
            results = [
                v for v in results
                if query_lower in v.title.lower() or
                   query_lower in v.description.lower()
            ]
        
        # Sort by featured, then view count, then created date
        results.sort(key=lambda v: (-v.featured, -v.view_count, v.created_at), reverse=True)
        
        return results
    
    
    def get_featured_videos(self, limit: int = 10) -> List[VideoMetadata]:
        """Get featured videos"""
        featured = [v for v in self.videos.values() if v.featured]
        featured.sort(key=lambda v: -v.view_count)
        return featured[:limit]
    
    
    def get_all_tags(self) -> Set[str]:
        """Get all unique tags in library"""
        all_tags = set()
        for video in self.videos.values():
            all_tags.update(video.tags)
        return all_tags
    
    
    # ========================================
    # VIDEO MANAGEMENT
    # ========================================
    
    def add_video(self, video: VideoMetadata) -> bool:
        """Add a new video to library"""
        if video.video_id in self.videos:
            return False
        self.videos[video.video_id] = video
        return True
    
    
    def update_video(self, video_id: str, updates: Dict) -> bool:
        """Update video metadata"""
        if video_id not in self.videos:
            return False
        
        video = self.videos[video_id]
        for key, value in updates.items():
            if hasattr(video, key):
                setattr(video, key, value)
        
        return True
    
    
    def increment_view_count(self, video_id: str) -> bool:
        """Increment view count for a video"""
        if video_id not in self.videos:
            return False
        self.videos[video_id].view_count += 1
        return True
    
    
    def delete_video(self, video_id: str) -> bool:
        """Remove a video from library"""
        if video_id not in self.videos:
            return False
        del self.videos[video_id]
        return True
    
    
    # ========================================
    # INTEGRATION WITH PRIORITY 10
    # ========================================
    
    def get_videos_for_correction_plan(self, drill_ids: List[str]) -> Dict[str, List[VideoMetadata]]:
        """
        Get videos for all drills in a correction plan
        Returns dict mapping drill_id -> list of videos
        """
        result = {}
        for drill_id in drill_ids:
            videos = self.get_videos_for_drill(drill_id)
            if videos:
                result[drill_id] = videos
        return result
    
    
    def to_dict(self) -> Dict:
        """Convert library to dict for JSON serialization"""
        return {
            "total_videos": len(self.videos),
            "videos": [
                {
                    "video_id": v.video_id,
                    "title": v.title,
                    "description": v.description,
                    "source": v.source.value,
                    "source_url": v.source_url,
                    "thumbnail_url": v.thumbnail_url,
                    "duration_seconds": v.duration_seconds,
                    "category": v.category.value,
                    "tags": list(v.tags),
                    "drill_ids": list(v.drill_ids),
                    "drill_stage": v.drill_stage.value if v.drill_stage else None,
                    "coaching_points": v.coaching_points,
                    "equipment": v.equipment,
                    "view_count": v.view_count,
                    "featured": v.featured
                }
                for v in self.videos.values()
            ]
        }


# Global video library instance
_video_library_instance = None

def get_video_library() -> VideoLibrary:
    """Get or create global video library instance"""
    global _video_library_instance
    if _video_library_instance is None:
        _video_library_instance = VideoLibrary()
    return _video_library_instance


# ========================================
# TESTING & EXAMPLES
# ========================================

if __name__ == "__main__":
    # Test the video library
    library = VideoLibrary()
    
    print("=" * 80)
    print("VIDEO LIBRARY SYSTEM - PRIORITY 13")
    print("=" * 80)
    
    print(f"\n📚 Total Videos: {len(library.videos)}")
    print(f"🏷️  Total Tags: {len(library.get_all_tags())}")
    
    print("\n🌟 Featured Videos:")
    for video in library.get_featured_videos(5):
        print(f"   - {video.title} ({video.category.value})")
    
    print("\n🎓 Stage 1 Drills:")
    for video in library.get_videos_by_stage(DrillStage.STAGE_1):
        print(f"   - {video.title}")
    
    print("\n🔍 Search: 'hip rotation'")
    results = library.search_videos(query="hip rotation")
    for video in results:
        print(f"   - {video.title}")
    
    print("\n🏷️  Videos tagged 'foundation':")
    results = library.search_videos(tags={"foundation"})
    print(f"   Found {len(results)} videos")
    
    print("\n✅ Video Library System Ready!")
