"""
Catching Barrels - PlayerReport Schema
======================================

Complete data schema for player session reports as defined in Builder 2 Master Spec.
This schema is the contract between backend and frontend.

DO NOT MODIFY WITHOUT UPDATING FRONTEND.

Author: Builder 2
Date: 2025-12-25
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict, Literal
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS & TYPE DEFINITIONS
# ============================================================================

class MotorProfileType(str, Enum):
    TWISTER = "Twister"
    TILTER = "Tilter"
    HYBRID = "Hybrid"
    SPINNER = "Spinner"


class KRSLevel(str, Enum):
    FOUNDATION = "FOUNDATION"
    BUILDING = "BUILDING"
    DEVELOPING = "DEVELOPING"
    ADVANCED = "ADVANCED"
    ELITE = "ELITE"


class DataSource(str, Enum):
    VIDEO_ANALYSIS = "Video Analysis"
    ADVANCED_BIOMECHANICS = "Advanced Biomechanics"
    ELITE_LAB_SESSION = "Elite Lab Session"


class Confidence(str, Enum):
    STANDARD = "Standard"
    ADVANCED = "Advanced"
    ELITE = "Elite"


class TempoCategory(str, Enum):
    FAST = "Fast"
    BALANCED = "Balanced"
    SLOW = "Slow"


class Status(str, Enum):
    ELITE = "elite"
    GOOD = "good"
    NEEDS_WORK = "needs_work"
    CRITICAL = "critical"


class Sequence(str, Enum):
    PROPER = "proper"
    REVERSED = "reversed"
    COMPRESSED = "compressed"


class Priority(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class MissionCategory(str, Enum):
    BODY = "body"
    BAT = "bat"
    TIMING = "timing"
    POWER = "power"


# ============================================================================
# SUB-SCHEMAS
# ============================================================================

@dataclass
class PlayerInfo:
    """Player biographical information"""
    name: str
    age: int
    height_inches: float
    weight_lbs: float
    wingspan_inches: Optional[float] = None
    ape_index: Optional[float] = None  # wingspan - height


@dataclass
class Progress:
    """Progress tracking"""
    total_swings: int
    session_number: int
    last_session_date: str  # ISO 8601
    week_streak: int
    days_since_last: int
    report_unlocked: bool  # true if >= 50 swings
    swings_to_unlock: int  # Remaining until 50


@dataclass
class KRSScore:
    """KRS™ (Kinetic Realization Score) - Hero Metric"""
    total: float  # 0-100
    level: KRSLevel
    emoji: str  # 🌱, 🔧, 📈, ⭐, 🏆
    points_to_next_level: float
    
    # Components
    creation_score: float  # 0-100
    transfer_score: float  # 0-100
    
    # Trends (vs last session)
    krs_change: float  # +/- points
    creation_change: float
    transfer_change: float
    
    # Data source
    data_source: DataSource
    confidence: Confidence


@dataclass
class MotorProfile:
    """Motor profile classification"""
    primary: MotorProfileType
    primary_confidence: float  # 0-100
    secondary: Optional[str] = None
    
    # Display
    display_name: str = ""  # "THE TWISTER"
    tagline: str = ""  # "Rotational power. Stay tight, spin fast."
    color: str = "#3B82F6"  # Hex color for theming
    icon: str = "🌀"  # Emoji


@dataclass
class Tempo:
    """Tempo analysis"""
    ratio: float  # e.g., 2.8
    category: TempoCategory
    message: str


@dataclass
class Brain:
    """🧠 BRAIN (Motor Profile)"""
    motor_profile: MotorProfile
    tempo: Tempo
    pitch_watch: Optional[str] = None  # "Breaking balls down"


@dataclass
class Capacity:
    """Physical capacity metrics"""
    capacity_ke_joules: float
    capacity_bat_speed_mph: float


@dataclass
class Actual:
    """Actual performance metrics"""
    peak_ke_joules: float
    estimated_bat_speed_mph: float


@dataclass
class OnTable:
    """Gap between capacity and actual"""
    ke_gap_joules: float
    bat_speed_gap_mph: float


@dataclass
class SubComponent:
    """Generic sub-component score"""
    score: float  # 0-10 or 0-100 depending on context
    status: Status


@dataclass
class Body:
    """🏋️ BODY (Creation Score - Power Engine)"""
    creation_score: float  # 0-100
    
    capacity: Capacity
    actual: Actual
    on_table: OnTable
    
    # Sub-components
    ground_flow: SubComponent
    engine_flow: SubComponent
    
    # Gap source (what's limiting creation)
    gap_source: str  # "Early hip rotation"


@dataclass
class Flow:
    """Power flow through kinetic chain"""
    you_create_mph: float  # From body
    reaches_barrel_mph: float  # Output
    on_table_mph: float  # Lost in transfer


@dataclass
class KineticChain:
    """Kinetic chain sub-component"""
    score: float  # 0-100
    status: Status
    
    # Details (if available)
    hip_momentum: Optional[float] = None
    shoulder_momentum: Optional[float] = None
    sh_ratio: Optional[float] = None
    sequence: Optional[Sequence] = None


@dataclass
class LeadLeg:
    """Lead leg sub-component"""
    score: float  # 0-100
    status: Status
    
    # Details (if available)
    knee_extension_deg: Optional[float] = None
    target_extension_deg: Optional[float] = None
    gap_deg: Optional[float] = None


@dataclass
class Timing:
    """Timing sub-component"""
    score: float  # 0-100
    status: Status


@dataclass
class AttackAngle:
    """Attack angle metrics"""
    current_deg: float
    capacity_deg: float  # Optimal range


@dataclass
class Bat:
    """⚔️ BAT (Transfer Score - Power Delivery)"""
    transfer_score: float  # 0-100
    
    flow: Flow
    
    # Sub-components
    kinetic_chain: KineticChain
    lead_leg: LeadLeg
    timing: Timing
    
    # Attack angle
    attack_angle: AttackAngle
    
    # Gap source (what's limiting transfer)
    gap_source: str  # "Pelvis-torso timing"


@dataclass
class BallPerformance:
    """Ball outcome metrics"""
    exit_velo_mph: float
    launch_angle_deg: float
    contact_quality: str  # "Ground ball tendency"


@dataclass
class Ball:
    """⚾ BALL (Projections)"""
    current: BallPerformance
    capacity: BallPerformance
    total_on_table_mph: float  # Body gap + Bat gap


@dataclass
class Win:
    """Individual win/strength"""
    metric: str  # "Hip Angular Momentum"
    score: str  # Can be number or string
    percentile: Optional[float] = None  # Age-normalized
    message: str = ""
    icon: str = "💪"


@dataclass
class Mission:
    """🎯 MISSION (Primary Focus)"""
    title: str  # "Fix Lead Knee Extension"
    category: MissionCategory
    priority: Priority
    
    unlock: str  # "Unlock +20 mph bat speed"
    explanation: str  # 2-3 sentences
    
    current_value: Optional[float] = None
    target_value: Optional[float] = None
    unit: Optional[str] = None
    gap: Optional[float] = None
    
    expected_fix_weeks: int = 6


@dataclass
class SecondaryIssue:
    """Secondary issue"""
    title: str
    priority: Priority
    brief: str


@dataclass
class Drill:
    """Individual drill"""
    name: str
    category: str
    
    volume: str  # "3 sets × 30 seconds"
    frequency: str  # "Daily"
    
    why_it_works: str
    key_cues: List[str]  # Max 3
    addresses_issue: str  # Links to mission
    
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


@dataclass
class Gains:
    """Projected gains"""
    bat_speed: str  # "+15-20 mph"
    exit_velocity: str
    transfer_efficiency: str
    krs_points: str  # "+23 points"


@dataclass
class Projection:
    """Projection if drills followed"""
    timeframe: str  # "4-6 weeks"
    gains: Gains


@dataclass
class CoachMessage:
    """💬 Coach Rick Message"""
    what_i_see: str  # One sentence
    your_mission: str  # One sentence
    signature: str  # "Trust the work."


@dataclass
class PowerParadox:
    """Power paradox insight"""
    capacity_percentile: float
    delivery_percentile: float
    potential_gain_mph: float
    bottleneck: str


@dataclass
class CricketBackground:
    """Cricket background insight"""
    detected_patterns: List[str]
    conversion_timeline: str
    priority_focus: str


@dataclass
class AnthropometricAdvantage:
    """Anthropometric advantage insight"""
    ape_index: float
    leverage_advantage: str
    ceiling_estimate: str


@dataclass
class SpecialInsights:
    """Special insights (conditional)"""
    power_paradox: Optional[PowerParadox] = None
    cricket_background: Optional[CricketBackground] = None
    anthropometric_advantage: Optional[AnthropometricAdvantage] = None


@dataclass
class Flags:
    """🚩 Special flags"""
    power_paradox: bool = False
    cricket_background: bool = False
    anthropometric_advantage: bool = False
    rapid_improver: bool = False


# ============================================================================
# MAIN SCHEMA: PLAYER REPORT
# ============================================================================

@dataclass
class PlayerReport:
    """
    Complete Player Report Schema
    
    This is THE contract between backend and frontend.
    DO NOT MODIFY without updating both sides.
    """
    
    # ========================================
    # METADATA
    # ========================================
    session_id: str
    player_id: str
    session_date: str  # ISO 8601
    session_number: int  # Lifetime session count
    
    # ========================================
    # PLAYER INFO
    # ========================================
    player: PlayerInfo
    
    # ========================================
    # PROGRESS TRACKING
    # ========================================
    progress: Progress
    
    # ========================================
    # KRS™ (HERO METRIC)
    # ========================================
    krs: KRSScore
    
    # ========================================
    # 🧠 BRAIN (MOTOR PROFILE)
    # ========================================
    brain: Brain
    
    # ========================================
    # 🏋️ BODY (CREATION - POWER ENGINE)
    # ========================================
    body: Body
    
    # ========================================
    # ⚔️ BAT (TRANSFER - POWER DELIVERY)
    # ========================================
    bat: Bat
    
    # ========================================
    # ⚾ BALL (PROJECTIONS)
    # ========================================
    ball: Ball
    
    # ========================================
    # 🎯 MISSION (PRIMARY FOCUS)
    # ========================================
    mission: Mission
    
    # Projection if drills followed
    projection: Projection
    
    # ========================================
    # 💬 COACH RICK MESSAGE
    # ========================================
    coach_message: CoachMessage
    
    # ========================================
    # 💪 WINS (WHAT'S WORKING)
    # ========================================
    wins: List[Win] = field(default_factory=list)
    
    # Secondary issues (collapsed by default)
    secondary_issues: List[SecondaryIssue] = field(default_factory=list)
    
    # ========================================
    # 🏋️ DRILLS (TRAINING PLAN)
    # ========================================
    drills: List[Drill] = field(default_factory=list)
    
    # ========================================
    # 🚩 SPECIAL FLAGS
    # ========================================
    flags: Flags = field(default_factory=Flags)
    
    # Special insights (if flags true)
    special_insights: SpecialInsights = field(default_factory=SpecialInsights)
    
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        import dataclasses
        return dataclasses.asdict(self)
