"""
SWING REHAB RECOMMENDATION LOGIC SYSTEM
Based on Dr. Kwon's biomechanical principles
Integrated with Kinetic Capacity Framework

This system:
1. Analyzes video scores (Ground, Engine, Weapon) from the Kinetic Capacity system
2. Identifies root biomechanical issues using Dr. Kwon's assessment logic
3. Generates personalized drill recommendations with progressions
4. Considers motor preference and individual patterns
5. Is fully extensible for adding new drills/corrections
"""

from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class IssueCategory(Enum):
    """Biomechanical issue categories"""
    TIMING_RHYTHM = "timing_rhythm"
    HIP_SHOULDER_SEPARATION = "hip_shoulder_separation"
    CONNECTION = "connection"
    KINETIC_CHAIN = "kinetic_chain"
    DIRECTION_BARREL = "direction_barrel"
    FORCE_GENERATION = "force_generation"
    STRIDE = "stride"
    LOAD = "load"
    TRANSITION = "transition"


class Priority(Enum):
    """Priority levels for recommendations"""
    CRITICAL = "CRITICAL"  # Must fix first - safety or fundamental
    HIGH = "HIGH"          # Major power/performance leak
    MEDIUM = "MEDIUM"      # Refinement needed
    LOW = "LOW"            # Optional enhancement


class DrillStage(Enum):
    """Progressive drill stages"""
    STAGE_1 = "Stage 1: Foundation/Isolation"
    STAGE_2 = "Stage 2: Integration/Combination"
    STAGE_3 = "Stage 3: Game-Speed Application"


@dataclass
class BiomechanicalIssue:
    """Represents an identified biomechanical issue"""
    category: IssueCategory
    name: str
    description: str
    severity: float  # 0.0-1.0, calculated from scores
    priority: Priority
    root_cause: str
    data_evidence: Dict[str, any]
    
    
@dataclass
class DrillRecommendation:
    """Represents a drill recommendation"""
    drill_id: str
    drill_name: str
    stage: DrillStage
    description: str
    how_it_works: str
    addresses: List[IssueCategory]
    equipment_needed: List[str]
    sets_reps: str
    coaching_cues: List[str]
    video_reference: Optional[str] = None
    integration_with_tools: Optional[str] = None
    expected_outcome: Optional[str] = None


@dataclass
class CorrectionPlan:
    """Complete correction plan for an athlete"""
    issues: List[BiomechanicalIssue]
    drill_progression: List[DrillRecommendation]
    strength_work: List[Dict]
    timeline: str
    success_metrics: Dict[str, float]
    motor_preference_notes: str


class SwingRehabRecommendationEngine:
    """
    Main recommendation engine that analyzes swing data and generates
    personalized correction plans based on Dr. Kwon's principles
    """
    
    def __init__(self):
        """Initialize the recommendation engine with drill database"""
        self.drill_database = self._initialize_drill_database()
        self.issue_assessment_rules = self._initialize_assessment_rules()
        self.strength_exercises = self._initialize_strength_database()
        
    def generate_recommendations(
        self,
        ground_score: int,
        engine_score: int,
        weapon_score: int,
        capacity_data: Dict,
        gap_analysis: Dict,
        motor_preference: Optional[str] = None
    ) -> CorrectionPlan:
        """
        Main entry point: Generate complete correction plan
        
        Args:
            ground_score: Ground efficiency score (0-100)
            engine_score: Engine efficiency score (0-100)
            weapon_score: Weapon efficiency score (0-100)
            capacity_data: Kinetic capacity calculation results
            gap_analysis: Gap analysis results
            motor_preference: Optional motor preference identifier
            
        Returns:
            CorrectionPlan with issues, drills, and timeline
        """
        # Step 1: Identify biomechanical issues
        issues = self._assess_issues(
            ground_score, engine_score, weapon_score, 
            capacity_data, gap_analysis
        )
        
        # Step 2: Prioritize issues
        prioritized_issues = self._prioritize_issues(issues)
        
        # Step 3: Generate drill progression
        drill_progression = self._generate_drill_progression(
            prioritized_issues, motor_preference
        )
        
        # Step 4: Add strength/conditioning work
        strength_work = self._generate_strength_recommendations(
            prioritized_issues
        )
        
        # Step 5: Create timeline
        timeline = self._generate_timeline(prioritized_issues, drill_progression)
        
        # Step 6: Define success metrics
        success_metrics = self._define_success_metrics(
            ground_score, engine_score, weapon_score, prioritized_issues
        )
        
        # Step 7: Motor preference notes
        motor_notes = self._generate_motor_preference_notes(
            prioritized_issues, motor_preference
        )
        
        return CorrectionPlan(
            issues=prioritized_issues,
            drill_progression=drill_progression,
            strength_work=strength_work,
            timeline=timeline,
            success_metrics=success_metrics,
            motor_preference_notes=motor_notes
        )
    
    def _assess_issues(
        self, 
        ground_score: int,
        engine_score: int, 
        weapon_score: int,
        capacity_data: Dict,
        gap_analysis: Dict
    ) -> List[BiomechanicalIssue]:
        """
        Assess biomechanical issues based on scores and data
        
        Uses Dr. Kwon's assessment logic to identify root causes
        """
        issues = []
        
        # GROUND SCORE ANALYSIS (0-100)
        # Ground = Force Generation, Load, Stride mechanics
        if ground_score < 50:
            # CRITICAL: Ground force generation issues
            issues.append(BiomechanicalIssue(
                category=IssueCategory.FORCE_GENERATION,
                name="Weak Ground Force Generation",
                description="Force plate analysis would show late front foot contact or insufficient pressure. Unable to generate proper ground reaction forces.",
                severity=1.0 - (ground_score / 100),
                priority=Priority.CRITICAL,
                root_cause="Front foot lands late or light, can't produce ground forces",
                data_evidence={
                    'ground_score': ground_score,
                    'efficiency_percent': ground_score
                }
            ))
            
            # Load issues often accompany ground issues
            issues.append(BiomechanicalIssue(
                category=IssueCategory.LOAD,
                name="Shallow Load/No Coil",
                description="Back hip not loading deeply, scapular not stretching. No elastic tension being created.",
                severity=1.0 - (ground_score / 100),
                priority=Priority.HIGH,
                root_cause="Back hip not loading, scapular not stretching, no elastic tension",
                data_evidence={
                    'ground_score': ground_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('GROUND', {}).get('gain_mph', 0)
                }
            ))
            
        elif ground_score < 70:
            # HIGH: Stride or load issues
            issues.append(BiomechanicalIssue(
                category=IssueCategory.STRIDE,
                name="Stride Mechanics Problem",
                description="Stride length, direction, or timing is misaligned. May be over-striding, crossing, or poor timing.",
                severity=1.0 - (ground_score / 100),
                priority=Priority.HIGH,
                root_cause="Stride mechanics misaligned with motor preference or pitch recognition",
                data_evidence={
                    'ground_score': ground_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('GROUND', {}).get('gain_mph', 0)
                }
            ))
        
        # ENGINE SCORE ANALYSIS (0-100)
        # Engine = Hip-Shoulder Separation, Kinetic Chain, Transition
        if engine_score < 50:
            # CRITICAL: Broken kinetic chain
            issues.append(BiomechanicalIssue(
                category=IssueCategory.KINETIC_CHAIN,
                name="Broken Kinetic Chain Sequencing",
                description="Energy loss between body segments. Upper body compensating for lower body. Peak angular velocities not in proper order (hip→torso→arm→hand).",
                severity=1.0 - (engine_score / 100),
                priority=Priority.CRITICAL,
                root_cause="Energy loss between segments, upper body compensates",
                data_evidence={
                    'engine_score': engine_score,
                    'efficiency_percent': engine_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('ENGINE', {}).get('gain_mph', 0)
                }
            ))
            
            # No hip-shoulder separation
            issues.append(BiomechanicalIssue(
                category=IssueCategory.HIP_SHOULDER_SEPARATION,
                name="No Hip-Shoulder Separation",
                description="Hip doesn't reach max velocity before shoulder. Body moving together as one unit instead of sequential acceleration.",
                severity=1.0 - (engine_score / 100),
                priority=Priority.HIGH,
                root_cause="Hip doesn't reach max velocity before shoulder, body moves together",
                data_evidence={
                    'engine_score': engine_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('ENGINE', {}).get('gain_mph', 0)
                }
            ))
            
        elif engine_score < 70:
            # HIGH: Transition or timing issues
            issues.append(BiomechanicalIssue(
                category=IssueCategory.TRANSITION,
                name="Abrupt Transition/Lost Rhythm",
                description="Rhythm breaks between load and drive. Loss of flow. Pause quality insufficient.",
                severity=1.0 - (engine_score / 100),
                priority=Priority.HIGH,
                root_cause="Rhythm breaks between load and drive, loss of flow",
                data_evidence={
                    'engine_score': engine_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('ENGINE', {}).get('gain_mph', 0)
                }
            ))
        
        # WEAPON SCORE ANALYSIS (0-100)
        # Weapon = Connection, Direction/Barrel Control, Hand Path
        if weapon_score < 50:
            # CRITICAL: Connection issues
            issues.append(BiomechanicalIssue(
                category=IssueCategory.CONNECTION,
                name="Disconnected Swing",
                description="Barrel drops below hands. Arms disconnect from torso rotation. Flying elbows. Loose angles.",
                severity=1.0 - (weapon_score / 100),
                priority=Priority.CRITICAL,
                root_cause="Barrel drops below hand, arms disconnect from torso rotation",
                data_evidence={
                    'weapon_score': weapon_score,
                    'efficiency_percent': weapon_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('WEAPON', {}).get('gain_mph', 0)
                }
            ))
            
        elif weapon_score < 70:
            # HIGH: Direction/barrel control issues
            issues.append(BiomechanicalIssue(
                category=IssueCategory.DIRECTION_BARREL,
                name="Poor Direction/Zone Time",
                description="Barrel path too vertical or horizontal. Exits zone early. Limited contact window. Struggles with pitch adjustment.",
                severity=1.0 - (weapon_score / 100),
                priority=Priority.HIGH,
                root_cause="Barrel path too vertical or too horizontal, exits zone early",
                data_evidence={
                    'weapon_score': weapon_score,
                    'expected_gain_mph': gap_analysis.get('leaks', {}).get('WEAPON', {}).get('gain_mph', 0)
                }
            ))
        
        # TIMING/RHYTHM (affects all categories)
        overall_efficiency = (ground_score + engine_score + weapon_score) / 3
        if overall_efficiency < 60:
            issues.append(BiomechanicalIssue(
                category=IssueCategory.TIMING_RHYTHM,
                name="Timing & Rhythm Problems",
                description="Mismatch with pitcher rhythm. Load-to-stride sync problem. Early or late load, rushed transition.",
                severity=1.0 - (overall_efficiency / 100),
                priority=Priority.HIGH,
                root_cause="Mismatch with pitcher rhythm, load-to-stride sync problem",
                data_evidence={
                    'overall_efficiency': overall_efficiency,
                    'ground_score': ground_score,
                    'engine_score': engine_score,
                    'weapon_score': weapon_score
                }
            ))
        
        return issues
    
    def _prioritize_issues(self, issues: List[BiomechanicalIssue]) -> List[BiomechanicalIssue]:
        """
        Sort issues by priority and severity
        
        Dr. Kwon's principle: Fix foundation first (Ground → Engine → Weapon)
        But also consider severity within each category
        """
        # Priority order for foundation-first approach
        priority_order = {
            Priority.CRITICAL: 0,
            Priority.HIGH: 1,
            Priority.MEDIUM: 2,
            Priority.LOW: 3
        }
        
        # Category order (foundation first)
        category_order = {
            IssueCategory.TIMING_RHYTHM: 0,      # Rhythm is foundation
            IssueCategory.FORCE_GENERATION: 1,   # Ground forces = power source
            IssueCategory.LOAD: 2,               # Can't drive what you don't load
            IssueCategory.STRIDE: 3,             # Stride bridges load to go
            IssueCategory.KINETIC_CHAIN: 4,      # Sequence before refining parts
            IssueCategory.HIP_SHOULDER_SEPARATION: 5,
            IssueCategory.TRANSITION: 6,
            IssueCategory.CONNECTION: 7,         # Connection before direction
            IssueCategory.DIRECTION_BARREL: 8    # Final refinement
        }
        
        # Sort by: priority → category order → severity
        return sorted(
            issues,
            key=lambda x: (
                priority_order[x.priority],
                category_order[x.category],
                -x.severity  # Higher severity first within same priority/category
            )
        )
    
    def _generate_drill_progression(
        self, 
        issues: List[BiomechanicalIssue],
        motor_preference: Optional[str]
    ) -> List[DrillRecommendation]:
        """
        Generate progressive drill sequence based on identified issues
        
        Follows 3-stage progression: Isolation → Integration → Game Speed
        """
        drill_progression = []
        
        # For each issue, add stage-appropriate drills
        for issue in issues:
            drills_for_issue = self._get_drills_for_issue(issue.category, motor_preference)
            drill_progression.extend(drills_for_issue)
        
        # Remove duplicates (same drill may address multiple issues)
        seen_drill_ids = set()
        unique_drills = []
        for drill in drill_progression:
            if drill.drill_id not in seen_drill_ids:
                seen_drill_ids.add(drill.drill_id)
                unique_drills.append(drill)
        
        # Sort by stage (Stage 1 → Stage 2 → Stage 3)
        stage_order = {
            DrillStage.STAGE_1: 1,
            DrillStage.STAGE_2: 2,
            DrillStage.STAGE_3: 3
        }
        
        return sorted(unique_drills, key=lambda x: stage_order[x.stage])
    
    def _get_drills_for_issue(
        self, 
        category: IssueCategory,
        motor_preference: Optional[str]
    ) -> List[DrillRecommendation]:
        """Get specific drills that address an issue category"""
        drills = []
        
        for drill in self.drill_database:
            if category in drill.addresses:
                drills.append(drill)
        
        return drills
    
    def _generate_strength_recommendations(
        self, 
        issues: List[BiomechanicalIssue]
    ) -> List[Dict]:
        """Generate strength/conditioning work based on issues"""
        strength_recommendations = []
        
        for issue in issues:
            # Map issue to strength work
            strength_work = self.strength_exercises.get(issue.category, [])
            strength_recommendations.extend(strength_work)
        
        # Remove duplicates
        seen = set()
        unique_strength = []
        for item in strength_recommendations:
            item_id = item['exercise']
            if item_id not in seen:
                seen.add(item_id)
                unique_strength.append(item)
        
        return unique_strength
    
    def _generate_timeline(
        self, 
        issues: List[BiomechanicalIssue],
        drills: List[DrillRecommendation]
    ) -> str:
        """Generate training timeline based on issue severity"""
        num_critical = sum(1 for i in issues if i.priority == Priority.CRITICAL)
        num_high = sum(1 for i in issues if i.priority == Priority.HIGH)
        
        if num_critical >= 2:
            return "8-12 weeks: Multiple critical issues require foundation rebuild"
        elif num_critical == 1:
            return "6-8 weeks: Critical issue + secondary corrections"
        elif num_high >= 2:
            return "4-6 weeks: Multiple high-priority refinements"
        else:
            return "2-4 weeks: Minor adjustments and optimization"
    
    def _define_success_metrics(
        self,
        ground_score: int,
        engine_score: int,
        weapon_score: int,
        issues: List[BiomechanicalIssue]
    ) -> Dict[str, float]:
        """Define target improvements for success"""
        return {
            'target_ground_score': min(ground_score + 20, 90),
            'target_engine_score': min(engine_score + 20, 90),
            'target_weapon_score': min(weapon_score + 20, 90),
            'target_overall_efficiency': min((ground_score + engine_score + weapon_score)/3 + 15, 85),
            'expected_bat_speed_gain_mph': sum(i.data_evidence.get('expected_gain_mph', 0) for i in issues[:3])  # Top 3 issues
        }
    
    def _generate_motor_preference_notes(
        self,
        issues: List[BiomechanicalIssue],
        motor_preference: Optional[str]
    ) -> str:
        """Generate notes about respecting motor preference"""
        if motor_preference:
            return f"Motor Preference: {motor_preference} - All drills should be adapted to respect this natural pattern. Don't force generic 'ideal' mechanics."
        else:
            return "Motor preference not yet identified. Observe natural movement patterns during initial drills. Adapt subsequent drills to match individual preference."
    
    def _initialize_drill_database(self) -> List[DrillRecommendation]:
        """
        Initialize comprehensive drill database
        
        This is EXTENSIBLE - you can add new drills by appending to this list
        """
        drills = []
        
        # ===== TIMING & RHYTHM DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="step_drill_stage1",
            drill_name="Step Through Drill (Stage 1)",
            stage=DrillStage.STAGE_1,
            description="Break swing into: step forward (load), pause, step back (swing). Emphasizes load-stride separation.",
            how_it_works="Isolates rhythm components. Load phase (step forward), pause for timing, drive phase (step back or no step).",
            addresses=[IssueCategory.TIMING_RHYTHM, IssueCategory.STRIDE, IssueCategory.TRANSITION],
            equipment_needed=["Bat", "Tee or soft toss"],
            sets_reps="3 sets of 10 reps, focusing on consistent rhythm",
            coaching_cues=[
                "Step forward = load",
                "Pause for pitcher's release",
                "Step back = trigger",
                "Rhythm first, power later"
            ],
            integration_with_tools="Use Erickson Bell after establishing rhythm to add light resistance",
            expected_outcome="Consistent load-to-swing timing, better pitcher synchronization"
        ))
        
        drills.append(DrillRecommendation(
            drill_id="step_drill_stage2",
            drill_name="Narrow Stance Trigger (Stage 2)",
            stage=DrillStage.STAGE_2,
            description="Start in narrow stance, use small step or leg kick as trigger while maintaining rhythm from Stage 1.",
            how_it_works="Reduces stride length, emphasizes trigger quality and rhythm maintenance.",
            addresses=[IssueCategory.TIMING_RHYTHM, IssueCategory.STRIDE],
            equipment_needed=["Bat", "Live or machine pitches"],
            sets_reps="3 sets of 8 reps off machine or live BP",
            coaching_cues=[
                "Small step, big turn",
                "Maintain Stage 1 rhythm",
                "Trigger on pitcher's release"
            ],
            expected_outcome="Improved timing consistency with reduced stride variability"
        ))
        
        # ===== FORCE GENERATION DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="weight_shift_load",
            drill_name="Weight Shift Load Drill",
            stage=DrillStage.STAGE_1,
            description="Isolate weight transfer to back hip, then shift to front foot with significant pressure.",
            how_it_works="Teaches proper load sequence: load back hip FIRST, then drive forward into front foot.",
            addresses=[IssueCategory.FORCE_GENERATION, IssueCategory.LOAD],
            equipment_needed=["Bat", "Force plates (optional but ideal)"],
            sets_reps="3 sets of 12 reps, hold load position 2 seconds",
            coaching_cues=[
                "Feel pressure on back inside hip",
                "Front foot contacts EARLY",
                "Drive ground through front foot",
                "Ground is the power source"
            ],
            integration_with_tools="Use force plate data to validate pressure timing and magnitude",
            expected_outcome="Earlier front foot contact, higher ground reaction forces"
        ))
        
        # ===== HIP-SHOULDER SEPARATION DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="hip_only_rotation",
            drill_name="Hip-Only Rotation Drill",
            stage=DrillStage.STAGE_1,
            description="Rotate hips independently while holding upper body still. Forces hip velocity FIRST before shoulder.",
            how_it_works="Isolates hip rotation, prevents early upper body. Establishes proximal-to-distal sequence.",
            addresses=[IssueCategory.HIP_SHOULDER_SEPARATION, IssueCategory.KINETIC_CHAIN],
            equipment_needed=["Bat held across chest", "Mirror or video feedback"],
            sets_reps="3 sets of 15 reps, pause at hip rotation peak",
            coaching_cues=[
                "Hips turn, shoulders stay",
                "Feel stretch in core",
                "Hip velocity FIRST",
                "Create separation"
            ],
            expected_outcome="Hip reaches max velocity before shoulder initiates rotation"
        ))
        
        drills.append(DrillRecommendation(
            drill_id="hip_rotation_arm_hold",
            drill_name="Hip Rotation with Arm Hold (Stage 2)",
            stage=DrillStage.STAGE_2,
            description="Rotate hips while holding arm in slot position, then release arms to follow hip rotation.",
            how_it_works="Integrates hip-first sequence into swing motion with controlled arm lag.",
            addresses=[IssueCategory.HIP_SHOULDER_SEPARATION, IssueCategory.KINETIC_CHAIN],
            equipment_needed=["Bat", "Tee or soft toss"],
            sets_reps="3 sets of 10 reps",
            coaching_cues=[
                "Hips lead, arms follow",
                "Feel lag in bat",
                "Sequential acceleration"
            ],
            expected_outcome="Improved energy transfer through kinetic chain"
        ))
        
        # ===== CONNECTION DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="connection_ball_rollback",
            drill_name="Connection Ball Roll-Back Drill",
            stage=DrillStage.STAGE_1,
            description="Roll ball across chest during load phase to teach scapular position and front-side stretch.",
            how_it_works="Physical cue creates scapular stretch sensation and proper coil position.",
            addresses=[IssueCategory.CONNECTION, IssueCategory.LOAD],
            equipment_needed=["Connection ball or small basketball", "Bat"],
            sets_reps="3 sets of 12 reps, hold stretch position 2 seconds",
            coaching_cues=[
                "Roll ball back across chest",
                "Feel front shoulder stretch",
                "Maintain ball pressure through swing",
                "Connection = speed + control"
            ],
            integration_with_tools="Alternate with Stack Bat to strengthen coil muscles",
            expected_outcome="Proper scapular loading, maintained connection through swing"
        ))
        
        drills.append(DrillRecommendation(
            drill_id="backside_barrier",
            drill_name="Backside Barrier Drill",
            stage=DrillStage.STAGE_1,
            description="Physical barrier (L-screen, net, coach) prevents early upper body rotation.",
            how_it_works="Barrier forces proper sequence: hips first, delayed shoulder/arm.",
            addresses=[IssueCategory.CONNECTION, IssueCategory.HIP_SHOULDER_SEPARATION],
            equipment_needed=["Bat", "L-screen or net barrier", "Tee"],
            sets_reps="3 sets of 10 reps",
            coaching_cues=[
                "Don't hit the barrier",
                "Hips turn first",
                "Hands stay back",
                "Feel separation"
            ],
            expected_outcome="Elimination of early upper body rotation, proper connection"
        ))
        
        # ===== DIRECTION/BARREL CONTROL DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="open_stance_45",
            drill_name="Open Stance 45° Drill",
            stage=DrillStage.STAGE_2,
            description="45° open stance extends barrel path in zone, improves outside pitch coverage.",
            how_it_works="Open stance forces barrel to stay in zone longer, teaches direction cues.",
            addresses=[IssueCategory.DIRECTION_BARREL],
            equipment_needed=["Bat", "Tee or pitching machine", "Targets for outside pitch location"],
            sets_reps="3 sets of 10 reps, all outside location",
            coaching_cues=[
                "Right hip → Right hand → Right center",
                "Extend barrel through zone",
                "Stay inside ball",
                "Zone time = contact quality"
            ],
            integration_with_tools="Use Stack Bat (light) for high-rep direction training",
            expected_outcome="Improved barrel control, better opposite field contact"
        ))
        
        # ===== KINETIC CHAIN FLOW DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="rope_swing",
            drill_name="Rope Swing Drill",
            stage=DrillStage.STAGE_2,
            description="Flexible rope requires full body control, teaches proximal-to-distal energy flow.",
            how_it_works="Can't 'arm' a rope swing - forces proper sequence and energy transfer.",
            addresses=[IssueCategory.KINETIC_CHAIN, IssueCategory.CONNECTION],
            equipment_needed=["Rope bat or heavy rope"],
            sets_reps="3 sets of 15 reps, focus on flow not speed",
            coaching_cues=[
                "Body guides rope, not arms",
                "Feel energy transfer",
                "Smooth acceleration",
                "Legs → hips → torso → arms"
            ],
            integration_with_tools="Combine with Synapse CCR for CNS activation after rope work",
            expected_outcome="Improved kinetic chain flow, better energy transfer"
        ))
        
        # ===== LOAD DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="deep_hip_load_holds",
            drill_name="Deep Back Hip Load Holds",
            stage=DrillStage.STAGE_1,
            description="Load back hip deeply, hold position to feel stretch and build position awareness.",
            how_it_works="Isometric holds teach proper depth and create proprioceptive awareness.",
            addresses=[IssueCategory.LOAD],
            equipment_needed=["Bat", "Mirror for feedback"],
            sets_reps="3 sets of 8 reps, hold 3-5 seconds each",
            coaching_cues=[
                "Back hip deep",
                "Feel front side stretch",
                "Maintain posture",
                "Load creates power"
            ],
            integration_with_tools="Use BOSU balance work to strengthen stabilizers for deeper loading",
            expected_outcome="Deeper, more consistent load position"
        ))
        
        # ===== STRIDE DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="step_back_stride_control",
            drill_name="Step Back Stride Control Drill",
            stage=DrillStage.STAGE_1,
            description="Control stride mechanics by stepping back into athletic position before stride forward.",
            how_it_works="Breaking stride into components allows focus on length, direction, timing independently.",
            addresses=[IssueCategory.STRIDE],
            equipment_needed=["Bat", "Stride markers or tape"],
            sets_reps="3 sets of 10 reps, measure stride consistency",
            coaching_cues=[
                "Step back to load",
                "Step forward = stride",
                "Land soft, land early",
                "Stride bridges load to drive"
            ],
            expected_outcome="Consistent stride length and direction, better timing"
        ))
        
        # ===== GAME-SPEED INTEGRATION DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="game_speed_flow",
            drill_name="Game-Speed Flow Drills (Stage 3)",
            stage=DrillStage.STAGE_3,
            description="Integrate all mechanics into game rhythm without mechanical thought. Live pitches or high-quality machine work.",
            how_it_works="Apply all learned mechanics at game speed, shift focus to pitch recognition.",
            addresses=[
                IssueCategory.TIMING_RHYTHM,
                IssueCategory.HIP_SHOULDER_SEPARATION,
                IssueCategory.CONNECTION,
                IssueCategory.KINETIC_CHAIN,
                IssueCategory.DIRECTION_BARREL
            ],
            equipment_needed=["Bat", "Live pitching or quality machine"],
            sets_reps="Multiple rounds of game-speed ABs",
            coaching_cues=[
                "See ball, hit ball",
                "Trust your work",
                "Rhythm and timing",
                "Let it happen"
            ],
            integration_with_tools="Use all tools as final validation before live competition",
            expected_outcome="Mechanics become automatic, focus shifts to pitch recognition"
        ))
        
        # ===== TRANSITION DRILLS =====
        drills.append(DrillRecommendation(
            drill_id="pause_quality_emphasis",
            drill_name="Pause Quality Emphasis Drill",
            stage=DrillStage.STAGE_1,
            description="Deliberate pause between load and drive phases to establish rhythm control.",
            how_it_works="Exaggerate pause to feel difference between load completion and drive initiation.",
            addresses=[IssueCategory.TRANSITION, IssueCategory.TIMING_RHYTHM],
            equipment_needed=["Bat", "Tee or soft toss"],
            sets_reps="3 sets of 10 reps, vary pause length",
            coaching_cues=[
                "Load - pause - go",
                "Feel the moment",
                "Smooth not abrupt",
                "Rhythm in transition"
            ],
            expected_outcome="Smoother transitions, better flow, improved rhythm"
        ))
        
        return drills
    
    def _initialize_assessment_rules(self) -> Dict:
        """Initialize Dr. Kwon's assessment flowchart rules"""
        # This maps scores to likely issues
        # Used by _assess_issues() method
        return {
            'ground_critical_threshold': 50,
            'ground_high_threshold': 70,
            'engine_critical_threshold': 50,
            'engine_high_threshold': 70,
            'weapon_critical_threshold': 50,
            'weapon_high_threshold': 70,
            'overall_rhythm_threshold': 60
        }
    
    def _initialize_strength_database(self) -> Dict[IssueCategory, List[Dict]]:
        """
        Initialize strength/conditioning exercise database
        
        Maps biomechanical issues to appropriate strength work
        """
        return {
            IssueCategory.FORCE_GENERATION: [
                {
                    'exercise': 'Split-Stance Medicine Ball Slams',
                    'target': 'Leg/glute power, rate of force development',
                    'equipment': 'Medicine ball (8-12 lbs)',
                    'sets_reps': '4 sets of 8 reps',
                    'timing': 'Pre-season power phase'
                },
                {
                    'exercise': 'Rear Foot Elevated Split Squats',
                    'target': 'Single-leg strength, front leg stability',
                    'equipment': 'Dumbbells or kettlebells, bench',
                    'sets_reps': '3 sets of 10 reps each leg',
                    'timing': 'Foundational strength phase'
                }
            ],
            IssueCategory.LOAD: [
                {
                    'exercise': 'Glute Activation (Clamshells, Monster Walks)',
                    'target': 'Glute max/med for deeper hip loading',
                    'equipment': 'Resistance bands',
                    'sets_reps': '2 sets of 15 reps each',
                    'timing': 'Dynamic warm-up daily'
                },
                {
                    'exercise': 'Deep Split-Stance Holds',
                    'target': 'Hip mobility and load depth',
                    'equipment': 'Bodyweight or light dumbbells',
                    'sets_reps': '3 sets of 30-second holds',
                    'timing': 'Corrective work 3x/week'
                }
            ],
            IssueCategory.HIP_SHOULDER_SEPARATION: [
                {
                    'exercise': 'Banded Hip Rotation Holds',
                    'target': 'Hip internal/external rotation strength',
                    'equipment': 'Resistance bands, 90/90 position',
                    'sets_reps': '3 sets of 10 holds (5-sec each)',
                    'timing': 'Pre-season foundation'
                },
                {
                    'exercise': 'Thoracic Spine Rotations (Quadruped)',
                    'target': 'T-spine rotation ROM for separation',
                    'equipment': 'Bodyweight, mat',
                    'sets_reps': '3 sets of 12 reps each side',
                    'timing': 'Mobility warm-up daily'
                }
            ],
            IssueCategory.KINETIC_CHAIN: [
                {
                    'exercise': 'Scapular Wall Slides',
                    'target': 'Scapular stability for upper chain link',
                    'equipment': 'Wall',
                    'sets_reps': '3 sets of 15 reps',
                    'timing': 'Daily corrective work'
                },
                {
                    'exercise': 'Prone I-Y-T Holds',
                    'target': 'Upper back strength, scapular control',
                    'equipment': 'Mat, light dumbbells (2-5 lbs)',
                    'sets_reps': '3 sets of 10-second holds each position',
                    'timing': '3x/week upper body work'
                }
            ],
            IssueCategory.CONNECTION: [
                {
                    'exercise': 'Band Pull-Aparts with Pause',
                    'target': 'Rear delt and scapular strength for connection',
                    'equipment': 'Resistance band',
                    'sets_reps': '3 sets of 15 reps (2-sec pause)',
                    'timing': 'Upper body days or warm-up'
                }
            ],
            IssueCategory.DIRECTION_BARREL: [
                {
                    'exercise': 'Wrist Curls (Flexion/Extension)',
                    'target': 'Forearm strength for barrel control',
                    'equipment': 'Dumbbells',
                    'sets_reps': '3 sets of 15 reps each direction',
                    'timing': 'Maintenance 2x/week'
                }
            ],
            IssueCategory.STRIDE: [
                {
                    'exercise': 'Lateral Lunges with Resistance',
                    'target': 'Hip stability and stride control',
                    'equipment': 'Kettlebell or dumbbell',
                    'sets_reps': '3 sets of 10 reps each leg',
                    'timing': 'Lower body strength days'
                }
            ],
            IssueCategory.TIMING_RHYTHM: [
                {
                    'exercise': 'Synapse CCR Protocol',
                    'target': 'CNS activation, explosive rotational power',
                    'equipment': 'Synapse CCR device',
                    'sets_reps': 'Per device protocol (typically 3-5 sets)',
                    'timing': 'Pre-game activation or CNS phase'
                }
            ],
            IssueCategory.TRANSITION: [
                {
                    'exercise': 'Stack Bat CNS Training',
                    'target': 'Fast movement patterns, reduced load for speed',
                    'equipment': 'Stack Bat (light option)',
                    'sets_reps': '3 sets of 10 fast swings',
                    'timing': 'Mid-practice during fatigue, 2-3x/week'
                }
            ]
        }
    
    def add_custom_drill(self, drill: DrillRecommendation):
        """
        Add a new drill to the database
        
        This makes the system extensible - you can add drills dynamically
        
        Args:
            drill: DrillRecommendation object with complete drill information
        """
        # Validate drill has required fields
        if not drill.drill_id or not drill.drill_name:
            raise ValueError("Drill must have drill_id and drill_name")
        
        # Check for duplicate drill_id
        if any(d.drill_id == drill.drill_id for d in self.drill_database):
            raise ValueError(f"Drill with ID '{drill.drill_id}' already exists")
        
        # Add to database
        self.drill_database.append(drill)
        print(f"✅ Added drill: {drill.drill_name} (ID: {drill.drill_id})")
    
    def add_strength_exercise(
        self, 
        issue_category: IssueCategory,
        exercise_info: Dict
    ):
        """
        Add a new strength exercise for a specific issue category
        
        Args:
            issue_category: Which biomechanical issue this addresses
            exercise_info: Dict with 'exercise', 'target', 'equipment', 'sets_reps', 'timing'
        """
        if issue_category not in self.strength_exercises:
            self.strength_exercises[issue_category] = []
        
        self.strength_exercises[issue_category].append(exercise_info)
        print(f"✅ Added strength exercise: {exercise_info['exercise']} for {issue_category.value}")


# ===== USAGE EXAMPLE =====
if __name__ == "__main__":
    # Example: Generate recommendations for Eric Williams
    
    # Initialize engine
    engine = SwingRehabRecommendationEngine()
    
    # Eric's data
    ground_score = 38
    engine_score = 58
    weapon_score = 55
    
    capacity_data = {
        'bat_speed_capacity_midpoint_mph': 76.1,
        'exit_velo_capacity_max_mph': 102.9
    }
    
    gap_analysis = {
        'leaks': {
            'GROUND': {'leak_percent': 32, 'gain_mph': 4.3, 'priority': 'HIGH'},
            'ENGINE': {'leak_percent': 44, 'gain_mph': 5.9, 'priority': 'HIGH'},
            'WEAPON': {'leak_percent': 24, 'gain_mph': 3.1, 'priority': 'MEDIUM'}
        }
    }
    
    # Generate recommendations
    plan = engine.generate_recommendations(
        ground_score=ground_score,
        engine_score=engine_score,
        weapon_score=weapon_score,
        capacity_data=capacity_data,
        gap_analysis=gap_analysis,
        motor_preference="hip-dominant"
    )
    
    # Print results
    print("=" * 80)
    print("SWING REHAB RECOMMENDATION PLAN")
    print("=" * 80)
    print(f"\n📊 IDENTIFIED ISSUES: {len(plan.issues)}")
    for i, issue in enumerate(plan.issues, 1):
        print(f"\n{i}. {issue.name} [{issue.priority.value}]")
        print(f"   Category: {issue.category.value}")
        print(f"   Severity: {issue.severity:.1%}")
        print(f"   Root Cause: {issue.root_cause}")
        if 'expected_gain_mph' in issue.data_evidence:
            print(f"   Potential Gain: +{issue.data_evidence['expected_gain_mph']:.1f} mph")
    
    print(f"\n\n🏋️ DRILL PROGRESSION: {len(plan.drill_progression)} drills")
    for drill in plan.drill_progression:
        print(f"\n📍 {drill.drill_name}")
        print(f"   {drill.stage.value}")
        print(f"   {drill.description}")
        print(f"   Sets/Reps: {drill.sets_reps}")
        print(f"   Cues: {', '.join(drill.coaching_cues[:2])}")
    
    print(f"\n\n💪 STRENGTH WORK: {len(plan.strength_work)} exercises")
    for exercise in plan.strength_work[:5]:  # Show first 5
        print(f"   • {exercise['exercise']} - {exercise['sets_reps']}")
    
    print(f"\n\n📅 TIMELINE: {plan.timeline}")
    
    print(f"\n\n🎯 SUCCESS METRICS:")
    for metric, value in plan.success_metrics.items():
        print(f"   • {metric}: {value:.1f}")
    
    print(f"\n\n🧠 {plan.motor_preference_notes}")
    
    print("\n" + "=" * 80)
