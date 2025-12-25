"""
Coach Rick's Take Generator - Natural coaching insights
Generates personalized coaching commentary based on swing analysis

Author: Coach Rick AI
Date: 2025-12-25
"""

from typing import Dict, Any, List
from dataclasses import dataclass
from .pattern_recognition import PatternDiagnosis


@dataclass
class CoachTake:
    """Coach Rick's personalized take on the swing"""
    opening: str
    diagnosis: str
    good_news: str
    fix_summary: str
    expected_results: str
    motivation: str
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "opening": self.opening,
            "diagnosis": self.diagnosis,
            "good_news": self.good_news,
            "fix_summary": self.fix_summary,
            "expected_results": self.expected_results,
            "motivation": self.motivation
        }
    
    def to_text(self) -> str:
        """Full text version"""
        return f"""
{self.opening}

{self.diagnosis}

{self.good_news}

{self.fix_summary}

{self.expected_results}

{self.motivation}
""".strip()


class CoachRickTakeGenerator:
    """Generates natural coaching commentary"""
    
    # Pattern-specific templates
    PATTERN_OPENINGS = {
        "PATTERN_1_KNEE_LEAK": [
            "I can see you're generating solid ground force, but we're losing it before it gets to the bat.",
            "Your timing and ground forces look great - but there's a leak in the system that's killing your power.",
            "Good athlete here. The issue isn't effort or strength - it's about locking that front side."
        ],
        "PATTERN_2_WEAK_HIPS": [
            "Your timing is on point, which is huge. But we need to get more from your hips.",
            "The sequencing looks good, but your hips are underperforming relative to what they should be doing.",
            "You've got the coordination - now we need to load the hips properly."
        ],
        "PATTERN_3_FAST_FOOT_ROLL": [
            "I'm seeing a spinning pattern here - your foot's rolling way too early.",
            "You're rotating instead of pushing through the ground. Classic spinner profile.",
            "The foot roll is happening before you can build any vertical force. We need to fix that sequence."
        ],
        "PATTERN_4_SHOULDER_COMPENSATION": [
            "Your shoulders are doing all the work here, and they shouldn't have to.",
            "This is a compensation pattern - shoulders working overtime because the hips aren't contributing.",
            "We need to get your hips to do their job so your shoulders can focus on bat speed."
        ]
    }
    
    DIAGNOSIS_TEMPLATES = {
        "PATTERN_1_KNEE_LEAK": "Here's what's happening: Your lead leg is absorbing energy instead of transferring it. When your knee flexes at contact (currently at {lead_knee}°), it acts like a shock absorber. That energy should be bouncing up into your hips and eventually the bat. Instead, it's getting lost in your quad.",
        "PATTERN_2_WEAK_HIPS": "Your hip-shoulder timing is solid at {timing}ms, but your hip angular momentum is only {hip_momentum:.1f} when it should be 2-3x higher. The hips aren't contributing enough rotational power, so your shoulders are compensating.",
        "PATTERN_3_FAST_FOOT_ROLL": "Your lead foot is rolling to the outside edge before you can push through the ground. This kills your vertical ground force (currently {vgrf:.2f}x bodyweight - should be 1.2-1.5x). Without that vertical push, your leg never straightens, hips never lock, and you end up spinning.",
        "PATTERN_4_SHOULDER_COMPENSATION": "Your shoulder angular momentum is {shoulder_momentum:.1f} while your hip angular momentum is only {hip_momentum:.1f} - that's a {shoulder_hip_ratio:.1f}x ratio. Should be 2-3x. Your shoulders are rotating WITH your hips instead of AFTER them, which means no elastic energy and no bat whip."
    }
    
    GOOD_NEWS_TEMPLATES = {
        "PATTERN_1_KNEE_LEAK": "The good news? Your ground force generation is already there. You're athletic. This is purely a coordination issue - we just need to teach your lead leg to extend instead of flex. That's a 2-3 week fix, not a 6-month strength program.",
        "PATTERN_2_WEAK_HIPS": "The good news? Your timing is elite. That's the hardest thing to teach. Now we just need to load the hips properly so they can do what they're supposed to do in that timing window.",
        "PATTERN_3_FAST_FOOT_ROLL": "Here's the good part: Once we fix the foot pattern, everything else will cascade. Your timing and rotation look good - we just need to add that vertical component before the rotation starts.",
        "PATTERN_4_SHOULDER_COMPENSATION": "The good news is your shoulders are strong and coordinated. Once we get your hips contributing, those shoulders will create even more bat speed because they won't be fighting to make up for weak hips."
    }
    
    FIX_SUMMARIES = {
        "PATTERN_1_KNEE_LEAK": "The fix: Single-leg isometric holds to teach your brain what a locked lead leg feels like. Then single-leg vertical jumps to own that position under load. Then rope swings with the cue 'steel rod, not shock absorber.' Simple progression.",
        "PATTERN_2_WEAK_HIPS": "The fix: Force Pedals to build that vertical ground force. Then lead-leg slams to explosive swings - teaching your system to transfer ground force → hip rotation. Then constraint drills to integrate it into live swings.",
        "PATTERN_3_FAST_FOOT_ROLL": "The fix: Ankle dorsiflexion isometrics to strengthen that pattern. Then single-leg pedal work with the cue 'push through the ball of the foot.' Then add rotation AFTER you feel that vertical push. Sequence matters.",
        "PATTERN_4_SHOULDER_COMPENSATION": "The fix: Get your hips loaded first. Hip lock drills. Medicine ball throws to feel that hip brake → shoulder stretch. Then rope swings with the cue 'hips stop, shoulders go.' Feel that elastic energy."
    }
    
    def __init__(self):
        pass
    
    def generate_take(
        self,
        pattern: PatternDiagnosis,
        metrics: Dict[str, float],
        ball_outcomes: Dict[str, Any],
        predictions: Dict[str, Any]
    ) -> CoachTake:
        """
        Generate Coach Rick's personalized take
        
        Args:
            pattern: Diagnosed swing pattern
            metrics: Biomechanical metrics
            ball_outcomes: Current ball outcome stats
            predictions: Predicted improvements
            
        Returns:
            Complete coach take
        """
        pattern_key = pattern.type
        
        # Opening
        opening = self._get_opening(pattern_key)
        
        # Diagnosis with metrics
        diagnosis = self._get_diagnosis(pattern_key, metrics)
        
        # Good news
        good_news = self._get_good_news(pattern_key)
        
        # Fix summary
        fix_summary = self._get_fix_summary(pattern_key)
        
        # Expected results
        expected_results = self._generate_results(ball_outcomes, predictions)
        
        # Motivation
        motivation = self._get_motivation(pattern.severity, predictions)
        
        return CoachTake(
            opening=opening,
            diagnosis=diagnosis,
            good_news=good_news,
            fix_summary=fix_summary,
            expected_results=expected_results,
            motivation=motivation
        )
    
    def _get_opening(self, pattern_key: str) -> str:
        """Get opening statement"""
        templates = self.PATTERN_OPENINGS.get(pattern_key, [
            "Let's talk about what I'm seeing in your swing data."
        ])
        # Use first template (in production, could randomize)
        return templates[0]
    
    def _get_diagnosis(self, pattern_key: str, metrics: Dict[str, float]) -> str:
        """Get diagnosis with metrics filled in"""
        template = self.DIAGNOSIS_TEMPLATES.get(
            pattern_key,
            "Your swing shows some coordination issues we can work on."
        )
        
        # Fill in metrics
        return template.format(
            lead_knee=metrics.get("lead_knee_angle", 0),
            hip_momentum=metrics.get("hip_angular_momentum", 0),
            shoulder_momentum=metrics.get("shoulder_angular_momentum", 0),
            shoulder_hip_ratio=metrics.get("shoulder_hip_ratio", 0),
            timing=metrics.get("timing_gap_ms", 0),
            vgrf=metrics.get("vertical_grf_estimate", 0)
        )
    
    def _get_good_news(self, pattern_key: str) -> str:
        """Get good news statement"""
        return self.GOOD_NEWS_TEMPLATES.get(
            pattern_key,
            "The good news is this is totally fixable with the right drills."
        )
    
    def _get_fix_summary(self, pattern_key: str) -> str:
        """Get fix summary"""
        return self.FIX_SUMMARIES.get(
            pattern_key,
            "We'll use a progressive drill sequence to build the proper pattern."
        )
    
    def _generate_results(
        self,
        current: Dict[str, Any],
        predicted: Dict[str, Any]
    ) -> str:
        """Generate expected results section"""
        ev_current = current.get("exit_velo", 0)
        ev_predicted = predicted.get("exit_velo", 0)
        ev_gain = predicted.get("exit_velo_gain", 0)
        
        la_current = current.get("launch_angle", 0)
        la_predicted = predicted.get("launch_angle", 0)
        
        bb_current = current.get("breaking_ball_avg", 0)
        bb_predicted = predicted.get("breaking_ball_avg", 0)
        
        gb_current = current.get("gb_rate", 0)
        ld_current = current.get("ld_rate", 0)
        gb_predicted = predicted.get("gb_rate", 0)
        ld_predicted = predicted.get("ld_rate", 0)
        
        return f"""Expected results in 6 weeks:
• Exit Velocity: {ev_current:.0f} → {ev_predicted:.0f} mph (+{ev_gain:.0f} mph)
• Launch Angle: {la_current:.0f}° → {la_predicted:.0f}°
• Breaking Ball AVG: {bb_current:.3f} → {bb_predicted:.3f} (+{(bb_predicted-bb_current):.0f} points)
• Ground Ball %: {gb_current:.0f}% → {gb_predicted:.0f}%
• Line Drive %: {ld_current:.0f}% → {ld_predicted:.0f}%

This isn't theory - it's what happens when you fix the energy leak."""
    
    def _get_motivation(self, severity: str, predictions: Dict[str, Any]) -> str:
        """Get motivational closing"""
        ev_gain = predictions.get("exit_velo_gain", 0)
        
        if severity == "CRITICAL":
            return f"Bottom line: You're leaving {ev_gain:.0f} mph on the table right now. This is the single biggest thing holding you back. Fix it, and everything changes. Let's get to work."
        elif severity == "MODERATE":
            return f"You've got {ev_gain:.0f} mph of untapped power here. Clean this up and you'll see it in games immediately. Let's dial it in."
        else:
            return f"Small tweak, big results. {ev_gain:.0f} mph might not sound like much, but it's the difference between a ground ball and a line drive. Worth fixing."


def generate_coach_take(
    pattern: PatternDiagnosis,
    metrics: Dict[str, float],
    ball_outcomes: Dict[str, Any],
    predictions: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convenience function to generate coach take
    
    Args:
        pattern: Diagnosed swing pattern
        metrics: Biomechanical metrics
        ball_outcomes: Current ball outcomes
        predictions: Predicted improvements
        
    Returns:
        Coach take as dictionary with full text
    """
    generator = CoachRickTakeGenerator()
    take = generator.generate_take(pattern, metrics, ball_outcomes, predictions)
    
    return {
        "sections": take.to_dict(),
        "full_text": take.to_text()
    }


# Testing
if __name__ == "__main__":
    print("\n" + "="*70)
    print("COACH RICK'S TAKE GENERATOR - TEST")
    print("="*70 + "\n")
    
    # Mock data for testing
    from .pattern_recognition import PatternDiagnosis
    
    test_pattern = PatternDiagnosis(
        pattern="PATTERN_1_KNEE_LEAK",
        severity="CRITICAL",
        confidence=0.95,
        root_cause="Energy Leak at Lead Knee",
        primary_protocol="PROTOCOL_1",
        secondary_protocol="PROTOCOL_2",
        key_metrics={"lead_knee_angle": 30.5}
    )
    
    test_metrics = {
        "lead_knee_angle": 30.5,
        "hip_angular_momentum": 2.10,
        "shoulder_angular_momentum": 18.25,
        "shoulder_hip_ratio": 8.68,
        "bat_speed": 82.0,
        "timing_gap_ms": 158.3
    }
    
    test_current = {
        "exit_velo": 82.0,
        "launch_angle": 2.0,
        "breaking_ball_avg": 0.180,
        "gb_rate": 65,
        "ld_rate": 25
    }
    
    test_predicted = {
        "exit_velo": 89.0,
        "exit_velo_gain": 7.0,
        "launch_angle": 15.0,
        "breaking_ball_avg": 0.280,
        "gb_rate": 35,
        "ld_rate": 55
    }
    
    # Generate take
    result = generate_coach_take(test_pattern, test_metrics, test_current, test_predicted)
    
    print("✅ Coach Rick's Take Generated\n")
    print("="*70)
    print(result["full_text"])
    print("="*70)
    
    print("\n✅ COACH RICK'S TAKE GENERATOR READY\n")
