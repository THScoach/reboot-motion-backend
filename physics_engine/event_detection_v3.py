"""
Event Detection Module - V3 (WITH PROPER SWING ISOLATION)

CRITICAL FIX: Find the actual swing FIRST (~2 seconds), then detect events within it
This prevents treating 19-second videos as one swing

Ground truth validation (Connor Gray):
- Video: 19.17 seconds
- Swing window: ~2 seconds around peak velocity
- Tempo: 3.38, Bat Speed: 57.5 mph
"""

import numpy as np
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from physics_calculator import JointAngles, JointVelocities


@dataclass
class SwingWindow:
    """The isolated time window containing one swing"""
    start_ms: float
    end_ms: float
    peak_velocity_ms: float
    peak_velocity_value: float
    
    def duration_ms(self) -> float:
        return self.end_ms - self.start_ms


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
    Detect key swing events with PROPER SWING ISOLATION
    
    CRITICAL APPROACH:
    1. FIRST: Isolate swing window (~2 sec around peak bat velocity)
    2. THEN: Detect events within that isolated window only
    3. This prevents 19-sec videos from being treated as one swing
    """
    
    def __init__(self, debug=False):
        """Initialize event detector"""
        self.debug = debug
    
    def detect_all_events(self, angles: List[JointAngles],
                         velocities: List[JointVelocities]) -> Optional[SwingEvents]:
        """
        Detect all swing events with proper swing isolation
        
        Args:
            angles: List of joint angles (for COM/pelvis position)
            velocities: List of joint velocities (for bat velocity)
        
        Returns:
            SwingEvents or None if detection fails
        """
        if not angles or not velocities or len(angles) < 5:
            print("❌ Not enough data for event detection")
            return None
        
        video_duration_s = (angles[-1].timestamp_ms - angles[0].timestamp_ms) / 1000
        print(f"\n🔍 EVENT DETECTION (V3 - with swing isolation)")
        print(f"   Total frames: {len(angles)}")
        print(f"   Video duration: {video_duration_s:.2f} seconds")
        print(f"   Time range: {angles[0].timestamp_ms:.0f}ms to {angles[-1].timestamp_ms:.0f}ms")
        
        try:
            # STEP 1: ISOLATE THE SWING WINDOW (critical!)
            swing_window = self.isolate_swing_window(velocities)
            
            if not swing_window:
                print("❌ Could not isolate swing window")
                return None
            
            print(f"\n   ✅ SWING WINDOW ISOLATED:")
            print(f"      Window: {swing_window.start_ms:.0f}ms to {swing_window.end_ms:.0f}ms")
            print(f"      Duration: {swing_window.duration_ms():.0f}ms ({swing_window.duration_ms()/1000:.2f}s)")
            print(f"      Peak velocity: {swing_window.peak_velocity_value:.1f} m/s at {swing_window.peak_velocity_ms:.0f}ms")
            
            # Filter angles and velocities to swing window only
            window_angles = [a for a in angles 
                           if swing_window.start_ms <= a.timestamp_ms <= swing_window.end_ms]
            window_velocities = [v for v in velocities 
                               if swing_window.start_ms <= v.timestamp_ms <= swing_window.end_ms]
            
            print(f"      Frames in window: {len(window_angles)} angles, {len(window_velocities)} velocities")
            
            if len(window_angles) < 5 or len(window_velocities) < 5:
                print("❌ Not enough frames in swing window")
                return None
            
            # STEP 2: DETECT EVENTS WITHIN THE ISOLATED WINDOW
            
            # 1. STANCE - first frame of window
            stance_ms = window_angles[0].timestamp_ms
            print(f"\n   ✓ Stance: {stance_ms:.0f}ms (window start)")
            
            # 2. LOAD - max backward pelvis movement
            load_ms = self.detect_load(window_angles)
            print(f"   ✓ Load: {load_ms:.0f}ms")
            
            # 3. FOOT DOWN - forward COM movement starts
            foot_down_ms = self.detect_foot_down(window_angles, load_ms)
            print(f"   ✓ Foot Down: {foot_down_ms:.0f}ms")
            
            # 4. CONTACT - use the peak velocity we already found
            contact_ms = swing_window.peak_velocity_ms
            print(f"   ✓ Contact: {contact_ms:.0f}ms (peak bat velocity)")
            
            # 5. FOLLOW THROUGH - last frame of window
            finish_ms = window_angles[-1].timestamp_ms
            print(f"   ✓ Follow Through: {finish_ms:.0f}ms (window end)")
            
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
            
            # Validation
            if tempo < 1.0 or tempo > 5.0:
                print(f"      ⚠️  Tempo {tempo:.2f} outside normal range (1.0-5.0)")
            elif 2.0 <= tempo <= 3.5:
                print(f"      ✅ Tempo {tempo:.2f} in optimal range (2.0-3.5)")
            
            return events
            
        except Exception as e:
            print(f"❌ Event detection failed: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def isolate_swing_window(self, velocities: List[JointVelocities],
                            window_size_ms: float = 2000) -> Optional[SwingWindow]:
        """
        CRITICAL: Isolate the actual swing window within the full video
        
        Strategy:
        1. Find peak bat velocity (likely contact point)
        2. Take ±1 second around peak (creates ~2 second window)
        3. This isolates the actual swing from dead time, setup, multiple takes
        
        Args:
            velocities: All velocities from full video
            window_size_ms: Window size around peak (default 2000ms = 2 seconds)
        
        Returns:
            SwingWindow with isolated time range
        """
        if not velocities or len(velocities) < 10:
            return None
        
        # Find peak bat velocity
        max_bat_vel = 0
        peak_idx = 0
        
        for i, v in enumerate(velocities):
            bat_vel = abs(v.bat_velocity) if hasattr(v, 'bat_velocity') else 0
            if bat_vel > max_bat_vel:
                max_bat_vel = bat_vel
                peak_idx = i
        
        if max_bat_vel < 1.0:  # No clear swing detected
            print(f"   ⚠️  Peak bat velocity too low: {max_bat_vel:.2f} m/s")
            return None
        
        peak_ms = velocities[peak_idx].timestamp_ms
        
        # Create window: ±1 second around peak
        half_window = window_size_ms / 2
        start_ms = peak_ms - half_window
        end_ms = peak_ms + half_window
        
        # Clamp to actual data range
        start_ms = max(start_ms, velocities[0].timestamp_ms)
        end_ms = min(end_ms, velocities[-1].timestamp_ms)
        
        return SwingWindow(
            start_ms=start_ms,
            end_ms=end_ms,
            peak_velocity_ms=peak_ms,
            peak_velocity_value=max_bat_vel
        )
    
    def detect_load(self, angles: List[JointAngles]) -> float:
        """
        Detect load (max backward pelvis movement) in FIRST HALF of swing window
        
        Note: This now searches within the 2-second swing window, not the full 19-second video!
        """
        half_len = len(angles) // 2
        
        # Get pelvis X positions
        max_backward = 0
        load_idx = 0
        initial_x = angles[0].pelvis_angle if hasattr(angles[0], 'pelvis_angle') else 0
        
        for i in range(1, half_len):
            current_x = angles[i].pelvis_angle if hasattr(angles[i], 'pelvis_angle') else 0
            backward_move = initial_x - current_x
            
            if backward_move > max_backward:
                max_backward = backward_move
                load_idx = i
        
        # If no significant backward movement, use 15% mark
        if load_idx == 0 or max_backward < 5:
            load_idx = max(1, int(len(angles) * 0.15))
        
        return angles[load_idx].timestamp_ms
    
    def detect_foot_down(self, angles: List[JointAngles], load_ms: float) -> float:
        """
        Detect foot down (forward COM movement) after load
        
        Note: Searches within swing window only
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
        
        # Fallback: 40% mark of window
        fallback_idx = min(load_idx + int(len(angles) * 0.25), len(angles) - 1)
        return angles[fallback_idx].timestamp_ms
    
    def validate_phases(self, stance_ms: float, load_ms: float, 
                       foot_down_ms: float, contact_ms: float, 
                       finish_ms: float) -> Tuple[float, float, float]:
        """
        Validate phases are in order with minimum duration
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
