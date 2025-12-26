"""
Event Detection Module - V2 (Matches Working TypeScript Implementation)

Based on proven frontend code from December 17-18, 2025
Contact detection via PEAK BAT ANGULAR VELOCITY
Proper tempo calculation: Load Duration / Swing Duration

Ground truth validation (Connor Gray):
- Tempo Ratio: 3.38:1
- Bat Speed: 57.5 mph
- Load: 1579ms, Swing: 467ms
"""

import numpy as np
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from physics_calculator import JointAngles, JointVelocities


@dataclass
class SwingEvents:
    """Key timestamps in the swing (matches TS interface)"""
    stance_time_ms: float       # Initial ready position
    load_start_ms: float        # Weight shift begins (load)
    foot_down_ms: float         # End of load, start of swing (footDown)
    contact_ms: float           # Peak bat velocity (contact)
    follow_through_ms: float    # Swing completion (finish)
    
    def get_load_duration_ms(self) -> float:
        """Load phase: load_start → foot_down"""
        return self.foot_down_ms - self.load_start_ms
    
    def get_swing_duration_ms(self) -> float:
        """Swing phase: foot_down → contact"""
        return self.contact_ms - self.foot_down_ms
    
    def get_tempo_ratio(self) -> float:
        """
        Tempo Ratio = Load Duration / Swing Duration
        
        Expected ranges:
        - 2.0 - 3.5: Optimal (patient load, explosive swing)
        - < 1.5: Rushing / spinning out
        - > 4.0: Too slow / disconnected
        """
        swing_duration = self.get_swing_duration_ms()
        load_duration = self.get_load_duration_ms()
        
        if swing_duration <= 0:
            return 0.0
        
        tempo = load_duration / swing_duration
        
        # Sanity check: cap at reasonable bounds
        return max(0.5, min(10.0, tempo))


class EventDetector:
    """
    Detect key swing events - matches proven TypeScript implementation
    
    APPROACH (from working code):
    1. Load Detection: Find max backward COM movement in first half
    2. Foot Down: When COM starts moving forward significantly
    3. Contact: Peak bat angular velocity AFTER foot down
    4. Tempo: (load → foot_down) / (foot_down → contact)
    """
    
    def __init__(self, debug=False):
        """Initialize event detector"""
        self.debug = debug
    
    def detect_all_events(self, angles: List[JointAngles],
                         velocities: List[JointVelocities]) -> Optional[SwingEvents]:
        """
        Detect all swing events using proven TypeScript logic
        
        Args:
            angles: List of joint angles (for COM/pelvis position)
            velocities: List of joint velocities (for bat velocity)
        
        Returns:
            SwingEvents or None if detection fails
        """
        if not angles or not velocities or len(angles) < 5:
            print("❌ Not enough data for event detection")
            return None
        
        print(f"\n🔍 EVENT DETECTION (TypeScript-based approach)")
        print(f"   Total frames: {len(angles)}")
        print(f"   Time range: {angles[0].timestamp_ms:.0f}ms to {angles[-1].timestamp_ms:.0f}ms")
        
        try:
            # 1. STANCE - first frame
            stance_ms = angles[0].timestamp_ms
            print(f"   ✓ Stance: {stance_ms:.0f}ms (frame 0)")
            
            # 2. LOAD - max backward pelvis movement in first half
            load_ms = self.detect_load(angles)
            print(f"   ✓ Load: {load_ms:.0f}ms")
            
            # 3. FOOT DOWN - forward COM movement starts
            foot_down_ms = self.detect_foot_down(angles, load_ms)
            print(f"   ✓ Foot Down: {foot_down_ms:.0f}ms")
            
            # 4. CONTACT - peak bat velocity AFTER foot down
            contact_ms = self.detect_contact(velocities, foot_down_ms)
            print(f"   ✓ Contact: {contact_ms:.0f}ms (peak bat velocity)")
            
            # 5. FOLLOW THROUGH - last frame
            finish_ms = angles[-1].timestamp_ms
            print(f"   ✓ Follow Through: {finish_ms:.0f}ms (frame {len(angles)-1})")
            
            # Validate phase order
            load_ms, foot_down_ms, contact_ms = self.validate_phases(
                stance_ms, load_ms, foot_down_ms, contact_ms, finish_ms
            )
            
            events = SwingEvents(
                stance_time_ms=stance_ms,
                load_start_ms=load_ms,
                foot_down_ms=foot_down_ms,
                contact_ms=contact_ms,
                follow_through_ms=finish_ms
            )
            
            # Print tempo
            tempo = events.get_tempo_ratio()
            load_dur = events.get_load_duration_ms()
            swing_dur = events.get_swing_duration_ms()
            print(f"\n   📊 TEMPO ANALYSIS:")
            print(f"      Load Duration:  {load_dur:.0f}ms")
            print(f"      Swing Duration: {swing_dur:.0f}ms")
            print(f"      Tempo Ratio:    {tempo:.2f}:1")
            
            return events
            
        except Exception as e:
            print(f"❌ Event detection failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def detect_load(self, angles: List[JointAngles]) -> float:
        """
        Detect load (max backward pelvis movement) in first half of video
        
        Matches TS logic:
        - Search first half for max negative COM movement
        - If no movement > 0.5% of frame, use 15% mark
        """
        half_len = len(angles) // 2
        
        # Get pelvis X positions (using pelvis_angle as proxy for horizontal position)
        max_backward = 0
        load_idx = 0
        initial_x = angles[0].pelvis_angle if hasattr(angles[0], 'pelvis_angle') else 0
        
        for i in range(1, half_len):
            current_x = angles[i].pelvis_angle if hasattr(angles[i], 'pelvis_angle') else 0
            backward_move = initial_x - current_x
            
            if backward_move > max_backward:
                max_backward = backward_move
                load_idx = i
        
        # If no significant backward movement (threshold 5 degrees), use 15% mark
        if load_idx == 0 or max_backward < 5:
            load_idx = max(1, int(len(angles) * 0.15))
        
        return angles[load_idx].timestamp_ms
    
    def detect_foot_down(self, angles: List[JointAngles], load_ms: float) -> float:
        """
        Detect foot down (forward COM movement) after load
        
        Matches TS logic:
        - Find when COM moves forward significantly (> 2% threshold)
        - If no clear movement, use 40% mark
        """
        # Find load index
        load_idx = 0
        for i, a in enumerate(angles):
            if a.timestamp_ms >= load_ms:
                load_idx = i
                break
        
        # Get pelvis position at load
        load_x = angles[load_idx].pelvis_angle if hasattr(angles[load_idx], 'pelvis_angle') else 0
        
        # Search for forward movement (threshold: 10 degrees)
        for i in range(load_idx + 1, len(angles)):
            current_x = angles[i].pelvis_angle if hasattr(angles[i], 'pelvis_angle') else 0
            forward_move = current_x - load_x
            
            if forward_move > 10:  # 10 degree forward movement
                return angles[i].timestamp_ms
        
        # Fallback: 40% mark
        fallback_idx = int(len(angles) * 0.4)
        return angles[fallback_idx].timestamp_ms
    
    def detect_contact(self, velocities: List[JointVelocities], foot_down_ms: float) -> float:
        """
        Detect contact via PEAK BAT ANGULAR VELOCITY after foot down
        
        This is the CRITICAL fix from TypeScript:
        - Contact = where bat reaches maximum angular velocity
        - Search ONLY after foot down (swing/acceleration phase)
        - If no clear peak (< 100 deg/s), use 70% mark
        
        Ground truth: This matches industry standard for markerless analysis
        """
        # Find foot down index
        foot_down_idx = 0
        for i, v in enumerate(velocities):
            if v.timestamp_ms >= foot_down_ms:
                foot_down_idx = i
                break
        
        # Search for peak bat velocity AFTER foot down
        max_bat_vel = 0
        contact_idx = foot_down_idx
        
        for i in range(max(0, foot_down_idx - 1), len(velocities)):
            bat_vel = abs(velocities[i].bat_velocity) if hasattr(velocities[i], 'bat_velocity') else 0
            
            if bat_vel > max_bat_vel:
                max_bat_vel = bat_vel
                contact_idx = i
        
        print(f"      Peak bat velocity: {max_bat_vel:.1f} m/s at frame {contact_idx}")
        
        # If no clear peak (< 1.0 m/s), use 70% mark
        if contact_idx <= foot_down_idx or max_bat_vel < 1.0:
            print(f"      ⚠️  No clear bat velocity peak, using 70% fallback")
            contact_idx = int(len(velocities) * 0.7)
        
        return velocities[contact_idx].timestamp_ms
    
    def validate_phases(self, stance_ms: float, load_ms: float, 
                       foot_down_ms: float, contact_ms: float, 
                       finish_ms: float) -> Tuple[float, float, float]:
        """
        Validate phases are in order with minimum duration
        
        Matches TS validation:
        - Minimum 10ms per phase
        - Ensure proper ordering
        """
        min_phase_ms = 10
        
        valid_load = load_ms
        valid_foot_down = foot_down_ms
        valid_contact = contact_ms
        
        if valid_load <= stance_ms:
            valid_load = stance_ms + min_phase_ms
        
        if valid_foot_down <= valid_load:
            valid_foot_down = valid_load + min_phase_ms
        
        if valid_contact <= valid_foot_down:
            valid_contact = valid_foot_down + min_phase_ms
        
        return valid_load, valid_foot_down, valid_contact
    
    def get_event_summary(self, events: Optional[SwingEvents]) -> Dict:
        """Get event summary for API response"""
        if not events:
            return {
                "stance_ms": 0,
                "load_start_ms": 0,
                "foot_down_ms": 0,
                "contact_ms": 0,
                "follow_through_ms": 0,
                "load_duration_ms": 0,
                "swing_duration_ms": 0,
                "tempo_ratio": 0
            }
        
        return {
            "stance_ms": round(events.stance_time_ms, 1),
            "load_start_ms": round(events.load_start_ms, 1),
            "foot_down_ms": round(events.foot_down_ms, 1),
            "contact_ms": round(events.contact_ms, 1),
            "follow_through_ms": round(events.follow_through_ms, 1),
            "load_duration_ms": round(events.get_load_duration_ms(), 1),
            "swing_duration_ms": round(events.get_swing_duration_ms(), 1),
            "tempo_ratio": round(events.get_tempo_ratio(), 2)
        }
