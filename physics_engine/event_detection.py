"""
Event Detection Module - REWRITTEN with Swing Window Detection
Detects key swing events: stance, load, launch, contact

CRITICAL FIX: Now detects swing window FIRST, then finds events within that window
This prevents finding events in wrong parts of long videos with multiple swings
"""

import numpy as np
from typing import List, Optional, Dict, Tuple
from dataclasses import dataclass
from physics_calculator import JointAngles, JointVelocities


@dataclass
class SwingWindow:
    """Defines the time window containing a single swing"""
    start_ms: float          # First significant movement
    end_ms: float            # End of follow-through
    peak_velocity_ms: float  # Peak bat/hand velocity (likely contact)
    
    def duration_ms(self) -> float:
        return self.end_ms - self.start_ms


@dataclass
class SwingEvents:
    """Key timestamps in the swing"""
    stance_time_ms: float      # Initial ready position
    load_start_ms: float        # Weight shift begins
    load_peak_ms: float         # Maximum load (coil)
    launch_ms: float            # Forward movement begins
    contact_ms: float           # Estimated bat-ball contact
    follow_through_ms: float    # Swing completion
    
    def get_load_duration_ms(self) -> float:
        """Time from load start to launch"""
        return self.launch_ms - self.load_start_ms
    
    def get_swing_duration_ms(self) -> float:
        """Time from launch to contact"""
        return self.contact_ms - self.launch_ms
    
    def get_tempo_ratio(self) -> float:
        """
        Tempo Ratio = Load Duration / Swing Duration
        
        Ideal range: 2.5:1 to 3.5:1
        Younger players: often 2.0:1 to 2.5:1
        Elite MLB: 2.8:1 to 3.2:1
        """
        swing_duration = self.get_swing_duration_ms()
        load_duration = self.get_load_duration_ms()
        
        if swing_duration <= 0:
            return 0.0
        
        return load_duration / swing_duration


class EventDetector:
    """
    Detect key swing events from joint angles and velocities
    
    NEW APPROACH:
    1. First detect swing window (where the actual swing happens)
    2. Then find events ONLY within that window
    3. This prevents finding events in wrong parts of multi-swing videos
    """
    
    def __init__(self, debug=False):
        """Initialize event detector"""
        self.debug = debug
    
    def detect_swing_window(self, velocities: List[JointVelocities],
                           min_duration_ms: float = 400,
                           max_duration_ms: float = 2000) -> Optional[SwingWindow]:
        """
        Detect the time window containing a single swing
        
        Strategy:
        1. Find peak bat/hand velocity (likely contact point)
        2. Look backward ~300-600ms for load phase
        3. Look forward ~200-400ms for follow-through
        4. Validate the window makes sense (duration, velocity profile)
        
        Args:
            velocities: List of JointVelocities
            min_duration_ms: Minimum valid swing duration (default 400ms)
            max_duration_ms: Maximum valid swing duration (default 2000ms)
        
        Returns:
            SwingWindow or None if no valid swing found
        """
        if not velocities or len(velocities) < 20:
            return None
        
        # Calculate combined velocity metric (bat + hand velocities)
        combined_vels = []
        for v in velocities:
            # Use bat velocity primarily, fall back to hand velocity
            vel = abs(v.bat_velocity) if hasattr(v, 'bat_velocity') and v.bat_velocity else 0
            if hasattr(v, 'lead_hand_velocity'):
                vel = max(vel, abs(v.lead_hand_velocity))
            if hasattr(v, 'rear_hand_velocity'):
                vel = max(vel, abs(v.rear_hand_velocity))
            combined_vels.append(vel)
        
        if not combined_vels:
            return None
        
        # Find peak velocity (likely contact point)
        peak_idx = np.argmax(combined_vels)
        peak_velocity_ms = velocities[peak_idx].timestamp_ms
        
        if self.debug:
            print(f"  Peak velocity at index {peak_idx}, time {peak_velocity_ms}ms")
        
        # Look backward for swing start (load phase begins)
        # Typically 300-600ms before contact
        search_start_idx = max(0, peak_idx - 100)  # Search ~100 frames back
        
        # Find where velocity was low (stance/early load)
        velocity_threshold = np.mean(combined_vels) * 0.3  # 30% of mean
        
        start_idx = peak_idx
        for i in range(peak_idx - 1, search_start_idx, -1):
            if combined_vels[i] < velocity_threshold:
                start_idx = i
                break
        
        # Look forward for follow-through end
        # Typically 200-400ms after contact
        search_end_idx = min(len(velocities) - 1, peak_idx + 80)  # Search ~80 frames forward
        
        end_idx = peak_idx
        for i in range(peak_idx + 1, search_end_idx):
            # Follow-through ends when velocity drops significantly
            if combined_vels[i] < velocity_threshold:
                end_idx = i
                break
        else:
            # Didn't find low velocity, use search end
            end_idx = search_end_idx
        
        # Create swing window
        window = SwingWindow(
            start_ms=velocities[start_idx].timestamp_ms,
            end_ms=velocities[end_idx].timestamp_ms,
            peak_velocity_ms=peak_velocity_ms
        )
        
        # Validate window duration
        duration = window.duration_ms()
        
        if self.debug:
            print(f"  Window: {window.start_ms:.0f}ms to {window.end_ms:.0f}ms")
            print(f"  Duration: {duration:.0f}ms")
        
        if duration < min_duration_ms or duration > max_duration_ms:
            if self.debug:
                print(f"  ❌ Invalid duration: {duration:.0f}ms")
            return None
        
        return window
    
    def detect_stance(self, angles: List[JointAngles],
                     window: SwingWindow) -> Optional[float]:
        """
        Detect stance position within swing window
        
        Args:
            angles: List of JointAngles
            window: SwingWindow
        
        Returns:
            Timestamp in milliseconds
        """
        # Filter to window
        window_angles = [a for a in angles 
                        if window.start_ms <= a.timestamp_ms <= window.end_ms]
        
        if not window_angles:
            return window.start_ms
        
        # Stance is at the beginning of the window
        return window_angles[0].timestamp_ms
    
    def detect_load_start(self, velocities: List[JointVelocities],
                         window: SwingWindow) -> Optional[float]:
        """
        Detect load start within swing window
        Look for initial pelvis/torso movement
        
        Args:
            velocities: List of JointVelocities
            window: SwingWindow
        
        Returns:
            Timestamp in milliseconds
        """
        # Filter to window
        window_vels = [v for v in velocities 
                      if window.start_ms <= v.timestamp_ms <= window.end_ms]
        
        if not window_vels:
            return window.start_ms + 50
        
        # Load starts when pelvis begins rotating
        pelvis_vels = [abs(v.pelvis_velocity) if hasattr(v, 'pelvis_velocity') else 0 
                      for v in window_vels]
        
        # Find first significant pelvis velocity
        threshold = max(10, np.mean(pelvis_vels) * 0.5)
        
        for i, vel in enumerate(pelvis_vels):
            if vel > threshold:
                return window_vels[i].timestamp_ms
        
        # Fallback: 10% into window
        idx = len(window_vels) // 10
        return window_vels[idx].timestamp_ms if idx < len(window_vels) else window.start_ms
    
    def detect_load_peak(self, angles: List[JointAngles],
                        window: SwingWindow,
                        load_start_ms: float) -> Optional[float]:
        """
        Detect maximum load (peak coil) within swing window
        Look for maximum hip-shoulder separation
        
        Args:
            angles: List of JointAngles
            window: SwingWindow
            load_start_ms: When load started
        
        Returns:
            Timestamp in milliseconds
        """
        # Filter to window, after load start
        window_angles = [a for a in angles 
                        if load_start_ms <= a.timestamp_ms <= window.end_ms]
        
        if not window_angles:
            return load_start_ms + 100
        
        # Calculate hip-shoulder separation
        separations = []
        for angle in window_angles:
            sep = abs(angle.torso_angle - angle.pelvis_angle) if hasattr(angle, 'torso_angle') and hasattr(angle, 'pelvis_angle') else 0
            separations.append(sep)
        
        if not separations:
            return load_start_ms + 100
        
        # Find peak separation (before contact)
        contact_idx = len(window_angles) // 2  # Rough estimate
        peak_idx = np.argmax(separations[:contact_idx]) if contact_idx > 0 else 0
        
        return window_angles[peak_idx].timestamp_ms
    
    def detect_launch(self, window: SwingWindow,
                     load_peak_ms: float) -> float:
        """
        Detect launch point (forward movement begins)
        Typically 20-50ms after load peak
        
        Args:
            window: SwingWindow
            load_peak_ms: When load peaked
        
        Returns:
            Timestamp in milliseconds
        """
        # Launch happens shortly after load peak
        # Typical range: 20-50ms
        launch_ms = load_peak_ms + 30
        
        # Ensure it's before contact
        if launch_ms > window.peak_velocity_ms:
            launch_ms = load_peak_ms + (window.peak_velocity_ms - load_peak_ms) * 0.2
        
        return launch_ms
    
    def detect_contact(self, window: SwingWindow) -> float:
        """
        Detect bat-ball contact
        Use peak velocity from swing window
        
        Args:
            window: SwingWindow
        
        Returns:
            Timestamp in milliseconds
        """
        # Contact is at peak velocity (already detected in swing window)
        return window.peak_velocity_ms
    
    def detect_follow_through(self, window: SwingWindow,
                              contact_ms: float) -> float:
        """
        Detect follow-through completion
        
        Args:
            window: SwingWindow
            contact_ms: When contact occurred
        
        Returns:
            Timestamp in milliseconds
        """
        # Follow-through extends from contact to end of window
        # Typically 200-400ms after contact
        follow_through_ms = contact_ms + (window.end_ms - contact_ms) * 0.7
        
        # Ensure it's within window
        follow_through_ms = min(follow_through_ms, window.end_ms)
        
        return follow_through_ms
    
    def detect_all_events(self, angles: List[JointAngles],
                         velocities: List[JointVelocities]) -> Optional[SwingEvents]:
        """
        Detect all swing events in sequence
        
        NEW APPROACH:
        1. First detect swing window
        2. Then find events within that window only
        
        Args:
            angles: List of JointAngles
            velocities: List of JointVelocities
        
        Returns:
            SwingEvents with all timestamps, or None if no swing detected
        """
        if self.debug:
            print("\n🔍 Detecting Swing Window...")
        
        # Step 1: Detect swing window
        window = self.detect_swing_window(velocities)
        
        if not window:
            if self.debug:
                print("❌ No valid swing window detected")
            return None
        
        if self.debug:
            print(f"✅ Swing window: {window.start_ms:.0f}ms - {window.end_ms:.0f}ms")
            print(f"   Duration: {window.duration_ms():.0f}ms")
            print(f"   Peak velocity at: {window.peak_velocity_ms:.0f}ms")
        
        # Step 2: Detect events within window
        stance_ms = self.detect_stance(angles, window)
        load_start_ms = self.detect_load_start(velocities, window)
        load_peak_ms = self.detect_load_peak(angles, window, load_start_ms)
        launch_ms = self.detect_launch(window, load_peak_ms)
        contact_ms = self.detect_contact(window)
        follow_through_ms = self.detect_follow_through(window, contact_ms)
        
        if self.debug:
            print(f"\n📊 Events Detected:")
            print(f"   Stance: {stance_ms:.0f}ms")
            print(f"   Load Start: {load_start_ms:.0f}ms")
            print(f"   Load Peak: {load_peak_ms:.0f}ms")
            print(f"   Launch: {launch_ms:.0f}ms")
            print(f"   Contact: {contact_ms:.0f}ms")
            print(f"   Follow-through: {follow_through_ms:.0f}ms")
        
        events = SwingEvents(
            stance_time_ms=stance_ms,
            load_start_ms=load_start_ms,
            load_peak_ms=load_peak_ms,
            launch_ms=launch_ms,
            contact_ms=contact_ms,
            follow_through_ms=follow_through_ms
        )
        
        if self.debug:
            print(f"\n⏱️  Durations:")
            print(f"   Load: {events.get_load_duration_ms():.0f}ms")
            print(f"   Swing: {events.get_swing_duration_ms():.0f}ms")
            print(f"   Tempo Ratio: {events.get_tempo_ratio():.2f}")
        
        return events
    
    def get_event_summary(self, events: SwingEvents) -> Dict:
        """
        Get human-readable summary of events
        
        Args:
            events: SwingEvents
        
        Returns:
            Dictionary with timing breakdown
        """
        return {
            "stance_ms": round(events.stance_time_ms, 1),
            "load_start_ms": round(events.load_start_ms, 1),
            "load_peak_ms": round(events.load_peak_ms, 1),
            "launch_ms": round(events.launch_ms, 1),
            "contact_ms": round(events.contact_ms, 1),
            "follow_through_ms": round(events.follow_through_ms, 1),
            "load_duration_ms": round(events.get_load_duration_ms(), 1),
            "swing_duration_ms": round(events.get_swing_duration_ms(), 1),
            "tempo_ratio": round(events.get_tempo_ratio(), 2),
            "total_swing_time_ms": round(
                events.follow_through_ms - events.stance_time_ms, 1
            )
        }


if __name__ == "__main__":
    print("Event Detection Module - REWRITTEN")
    print("=" * 60)
    print("NEW FEATURES:")
    print("  ✅ Swing window detection (finds actual swing in video)")
    print("  ✅ Peak velocity detection (accurate contact timing)")
    print("  ✅ Window-constrained event detection")
    print("\nDetects:")
    print("  - Swing window (start/end of actual swing)")
    print("  - Stance position")
    print("  - Load start and peak")
    print("  - Launch point")
    print("  - Contact timing (at peak velocity)")
    print("  - Follow-through")
    print("\nCalculates:")
    print("  - Tempo Ratio (Load/Swing)")
    print("  - Expected range: 2.0-3.5 for good swings")
    print("=" * 60)
