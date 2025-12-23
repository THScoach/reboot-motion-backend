"""
Event Detection Module
Detects key swing events: stance, load, launch, contact

Critical for tempo calculations and phase analysis
"""

import numpy as np
from typing import List, Optional, Dict
from dataclasses import dataclass
from physics_calculator import JointAngles, JointVelocities


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
    """
    
    def __init__(self):
        """Initialize event detector"""
        pass
    
    def detect_stance(self, angles: List[JointAngles]) -> Optional[float]:
        """
        Detect stance position (initial ready state)
        Usually the first few frames where movement is minimal
        
        Args:
            angles: List of JointAngles
        
        Returns:
            Timestamp in milliseconds
        """
        if not angles or len(angles) < 5:
            return None
        
        # Stance is typically first frame or when movement is minimal
        # For now, use first valid frame
        return angles[0].timestamp_ms
    
    def detect_load_start(self, angles: List[JointAngles],
                         velocities: List[JointVelocities]) -> Optional[float]:
        """
        Detect when load begins (weight shift, coil starts)
        Look for initial backward movement of pelvis or torso
        
        Args:
            angles: List of JointAngles
            velocities: List of JointVelocities
        
        Returns:
            Timestamp in milliseconds
        """
        if not velocities or len(velocities) < 10:
            return None
        
        # Load typically starts when pelvis begins rotating backward
        # Look for first significant pelvis velocity
        pelvis_vels = [abs(v.pelvis_velocity) for v in velocities]
        
        # Find first frame where velocity exceeds threshold
        threshold = 50  # deg/s
        
        for i, vel in enumerate(pelvis_vels[:len(pelvis_vels)//2]):  # First half
            if vel > threshold:
                return velocities[i].timestamp_ms
        
        # Fallback: 10% into the video
        return velocities[len(velocities)//10].timestamp_ms
    
    def detect_load_peak(self, angles: List[JointAngles]) -> Optional[float]:
        """
        Detect maximum load position (peak coil)
        Look for maximum hip/shoulder separation
        
        Args:
            angles: List of JointAngles
        
        Returns:
            Timestamp in milliseconds
        """
        if not angles or len(angles) < 10:
            return None
        
        # Calculate hip-shoulder separation (X-factor)
        separations = []
        for angle in angles:
            separation = abs(angle.torso_angle - angle.pelvis_angle)
            separations.append(separation)
        
        # Find peak separation (usually in first 60% of swing)
        search_range = int(len(separations) * 0.6)
        peak_idx = np.argmax(separations[:search_range])
        
        return angles[peak_idx].timestamp_ms
    
    def detect_launch(self, velocities: List[JointVelocities],
                     load_peak_ms: float) -> Optional[float]:
        """
        Detect launch point (forward movement begins)
        Look for rapid acceleration after load peak
        
        Args:
            velocities: List of JointVelocities
            load_peak_ms: Timestamp of load peak
        
        Returns:
            Timestamp in milliseconds
        """
        if not velocities:
            return None
        
        # Find velocities after load peak
        post_load = [v for v in velocities if v.timestamp_ms > load_peak_ms]
        
        if not post_load:
            return None
        
        # Look for rapid increase in pelvis velocity (forward rotation)
        pelvis_vels = [v.pelvis_velocity for v in post_load]
        
        # Find first significant positive acceleration
        for i in range(1, len(pelvis_vels)):
            if pelvis_vels[i] > pelvis_vels[i-1] + 100:  # deg/s² threshold
                return post_load[i].timestamp_ms
        
        # Fallback: shortly after load peak
        return post_load[0].timestamp_ms if post_load else load_peak_ms + 50
    
    def detect_contact(self, velocities: List[JointVelocities],
                      launch_ms: float) -> Optional[float]:
        """
        Detect estimated bat-ball contact
        Look for peak bat velocity or hand deceleration
        
        Args:
            velocities: List of JointVelocities
            launch_ms: Timestamp of launch
        
        Returns:
            Timestamp in milliseconds
        """
        if not velocities:
            return None
        
        # Find velocities after launch
        post_launch = [v for v in velocities if v.timestamp_ms > launch_ms]
        
        if not post_launch:
            return None
        
        # Contact typically occurs at peak hand/bat velocity
        bat_vels = [v.bat_velocity for v in post_launch]
        
        if not bat_vels:
            return post_launch[-1].timestamp_ms
        
        peak_idx = np.argmax(bat_vels)
        return post_launch[peak_idx].timestamp_ms
    
    def detect_follow_through(self, angles: List[JointAngles],
                             contact_ms: float) -> Optional[float]:
        """
        Detect follow-through completion
        Typically when rotation stabilizes or video ends
        
        Args:
            angles: List of JointAngles
            contact_ms: Timestamp of contact
        
        Returns:
            Timestamp in milliseconds
        """
        if not angles:
            return None
        
        # Find angles after contact
        post_contact = [a for a in angles if a.timestamp_ms > contact_ms]
        
        if not post_contact:
            return angles[-1].timestamp_ms
        
        # Follow-through is typically 80% through post-contact frames
        follow_idx = int(len(post_contact) * 0.8)
        follow_idx = min(follow_idx, len(post_contact) - 1)
        
        return post_contact[follow_idx].timestamp_ms
    
    def detect_all_events(self, angles: List[JointAngles],
                         velocities: List[JointVelocities]) -> SwingEvents:
        """
        Detect all swing events in sequence
        
        Args:
            angles: List of JointAngles
            velocities: List of JointVelocities
        
        Returns:
            SwingEvents with all timestamps
        """
        # Detect events in order
        stance_ms = self.detect_stance(angles)
        load_start_ms = self.detect_load_start(angles, velocities)
        load_peak_ms = self.detect_load_peak(angles)
        launch_ms = self.detect_launch(velocities, load_peak_ms)
        contact_ms = self.detect_contact(velocities, launch_ms)
        follow_through_ms = self.detect_follow_through(angles, contact_ms)
        
        # Ensure logical ordering (fallback values if detection fails)
        if not stance_ms:
            stance_ms = angles[0].timestamp_ms if angles else 0.0
        
        if not load_start_ms or load_start_ms < stance_ms:
            load_start_ms = stance_ms + 100
        
        if not load_peak_ms or load_peak_ms < load_start_ms:
            load_peak_ms = load_start_ms + 200
        
        if not launch_ms or launch_ms < load_peak_ms:
            launch_ms = load_peak_ms + 50
        
        if not contact_ms or contact_ms < launch_ms:
            contact_ms = launch_ms + 150
        
        if not follow_through_ms or follow_through_ms < contact_ms:
            follow_through_ms = contact_ms + 200
        
        return SwingEvents(
            stance_time_ms=stance_ms,
            load_start_ms=load_start_ms,
            load_peak_ms=load_peak_ms,
            launch_ms=launch_ms,
            contact_ms=contact_ms,
            follow_through_ms=follow_through_ms
        )
    
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
    print("Event Detection Module")
    print("=" * 60)
    print("Detects:")
    print("  - Stance position")
    print("  - Load start and peak")
    print("  - Launch point")
    print("  - Contact timing")
    print("  - Follow-through")
    print("\nCalculates:")
    print("  - Tempo Ratio (Load/Swing)")
    print("=" * 60)
