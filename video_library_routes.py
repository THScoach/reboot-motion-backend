"""
PRIORITY 13: VIDEO LIBRARY API ROUTES
======================================

RESTful API endpoints for video library management
Integrates with Priority 10 drill recommendations
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Set
from enum import Enum
import sys
from pathlib import Path

# Add physics_engine to path
sys.path.insert(0, str(Path(__file__).parent / "physics_engine"))

from video_library import (
    VideoLibrary,
    VideoMetadata,
    VideoSource,
    VideoCategory,
    DrillStage,
    get_video_library
)


# Create router
router = APIRouter(prefix="/videos", tags=["Video Library"])


# Pydantic models for API
class VideoSourceEnum(str, Enum):
    YOUTUBE = "youtube"
    VIMEO = "vimeo"
    S3 = "s3"
    LOCAL = "local"
    CLOUDFLARE_STREAM = "cloudflare_stream"


class VideoCategoryEnum(str, Enum):
    DRILL = "drill"
    TECHNIQUE = "technique"
    CONCEPT = "concept"
    ASSESSMENT = "assessment"
    EXERCISE = "exercise"
    INTERVIEW = "interview"
    CASE_STUDY = "case_study"


class DrillStageEnum(str, Enum):
    STAGE_1 = "Stage 1: Foundation/Isolation"
    STAGE_2 = "Stage 2: Integration/Combination"
    STAGE_3 = "Stage 3: Game-Speed Application"


class VideoResponse(BaseModel):
    """API response model for video data"""
    video_id: str
    title: str
    description: str
    source: str
    source_url: str
    thumbnail_url: Optional[str] = None
    duration_seconds: Optional[int] = None
    category: str
    tags: List[str]
    drill_ids: List[str]
    drill_stage: Optional[str] = None
    coaching_points: List[str]
    equipment: List[str]
    view_count: int
    featured: bool


class VideoListResponse(BaseModel):
    """API response for list of videos"""
    total: int
    videos: List[VideoResponse]


# ========================================
# API ENDPOINTS
# ========================================

@router.get("/", response_model=VideoListResponse)
def get_all_videos(
    limit: int = Query(100, description="Maximum number of videos to return"),
    offset: int = Query(0, description="Number of videos to skip")
):
    """
    Get all videos in the library
    Supports pagination with limit and offset
    """
    library = get_video_library()
    all_videos = list(library.videos.values())
    
    # Sort by featured, view count, then created date
    all_videos.sort(key=lambda v: (-v.featured, -v.view_count, v.created_at), reverse=True)
    
    # Paginate
    paginated = all_videos[offset:offset + limit]
    
    return VideoListResponse(
        total=len(all_videos),
        videos=[_video_to_response(v) for v in paginated]
    )


@router.get("/featured", response_model=VideoListResponse)
def get_featured_videos(
    limit: int = Query(10, description="Maximum number of featured videos")
):
    """Get featured videos"""
    library = get_video_library()
    featured = library.get_featured_videos(limit=limit)
    
    return VideoListResponse(
        total=len(featured),
        videos=[_video_to_response(v) for v in featured]
    )


@router.get("/search", response_model=VideoListResponse)
def search_videos(
    q: Optional[str] = Query(None, description="Search query (title/description)"),
    tags: Optional[str] = Query(None, description="Comma-separated tags to filter by"),
    category: Optional[VideoCategoryEnum] = Query(None, description="Filter by category"),
    stage: Optional[DrillStageEnum] = Query(None, description="Filter by drill stage"),
    featured_only: bool = Query(False, description="Only return featured videos")
):
    """
    Search videos with multiple filters
    
    Examples:
    - /videos/search?q=hip
    - /videos/search?tags=foundation,ground
    - /videos/search?category=drill&stage=Stage%201
    - /videos/search?featured_only=true
    """
    library = get_video_library()
    
    # Parse tags
    tag_set = None
    if tags:
        tag_set = set(tag.strip() for tag in tags.split(","))
    
    # Convert enums
    category_filter = VideoCategory(category.value) if category else None
    stage_filter = DrillStage(stage.value) if stage else None
    
    # Search
    results = library.search_videos(
        query=q,
        tags=tag_set,
        category=category_filter,
        drill_stage=stage_filter,
        featured_only=featured_only
    )
    
    return VideoListResponse(
        total=len(results),
        videos=[_video_to_response(v) for v in results]
    )


@router.get("/by-category/{category}", response_model=VideoListResponse)
def get_videos_by_category(category: VideoCategoryEnum):
    """Get all videos in a specific category"""
    library = get_video_library()
    results = library.get_videos_by_category(VideoCategory(category.value))
    
    return VideoListResponse(
        total=len(results),
        videos=[_video_to_response(v) for v in results]
    )


@router.get("/by-stage/{stage}", response_model=VideoListResponse)
def get_videos_by_stage(stage: DrillStageEnum):
    """Get all videos for a specific drill stage"""
    library = get_video_library()
    results = library.get_videos_by_stage(DrillStage(stage.value))
    
    return VideoListResponse(
        total=len(results),
        videos=[_video_to_response(v) for v in results]
    )


@router.get("/for-drill/{drill_id}", response_model=VideoListResponse)
def get_videos_for_drill(drill_id: str):
    """
    Get all videos associated with a specific drill
    
    Example: /videos/for-drill/drill_step_through
    """
    library = get_video_library()
    results = library.get_videos_for_drill(drill_id)
    
    if not results:
        raise HTTPException(
            status_code=404,
            detail=f"No videos found for drill: {drill_id}"
        )
    
    return VideoListResponse(
        total=len(results),
        videos=[_video_to_response(v) for v in results]
    )


@router.get("/for-correction-plan", response_model=dict)
def get_videos_for_correction_plan(
    drill_ids: str = Query(..., description="Comma-separated list of drill IDs")
):
    """
    Get videos for multiple drills in a correction plan
    Returns a dict mapping drill_id -> list of videos
    
    Example: /videos/for-correction-plan?drill_ids=drill_step_through,drill_hip_only_rotation
    """
    library = get_video_library()
    
    # Parse drill IDs
    drill_id_list = [did.strip() for did in drill_ids.split(",")]
    
    # Get videos for each drill
    result = library.get_videos_for_correction_plan(drill_id_list)
    
    # Convert to response format
    response = {}
    for drill_id, videos in result.items():
        response[drill_id] = [_video_to_response(v) for v in videos]
    
    return {
        "drill_ids": drill_id_list,
        "videos_by_drill": response,
        "total_videos": sum(len(v) for v in result.values())
    }


@router.get("/tags")
def get_all_tags():
    """Get all unique tags in the video library"""
    library = get_video_library()
    tags = library.get_all_tags()
    
    return {
        "total": len(tags),
        "tags": sorted(list(tags))
    }


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: str):
    """Get a specific video by ID"""
    library = get_video_library()
    video = library.get_video(video_id)
    
    if not video:
        raise HTTPException(
            status_code=404,
            detail=f"Video not found: {video_id}"
        )
    
    # Increment view count
    library.increment_view_count(video_id)
    
    return _video_to_response(video)


@router.post("/{video_id}/view")
def increment_video_view(video_id: str):
    """Increment view count for a video (for analytics)"""
    library = get_video_library()
    
    if not library.increment_view_count(video_id):
        raise HTTPException(
            status_code=404,
            detail=f"Video not found: {video_id}"
        )
    
    return {
        "video_id": video_id,
        "message": "View count incremented",
        "new_view_count": library.get_video(video_id).view_count
    }


# ========================================
# HELPER FUNCTIONS
# ========================================

def _video_to_response(video: VideoMetadata) -> VideoResponse:
    """Convert VideoMetadata to API response model"""
    return VideoResponse(
        video_id=video.video_id,
        title=video.title,
        description=video.description,
        source=video.source.value,
        source_url=video.source_url,
        thumbnail_url=video.thumbnail_url,
        duration_seconds=video.duration_seconds,
        category=video.category.value,
        tags=list(video.tags),
        drill_ids=list(video.drill_ids),
        drill_stage=video.drill_stage.value if video.drill_stage else None,
        coaching_points=video.coaching_points,
        equipment=video.equipment,
        view_count=video.view_count,
        featured=video.featured
    )
