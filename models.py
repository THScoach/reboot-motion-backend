"""
Database Models for Reboot Motion Athlete App
SQLAlchemy ORM models for PostgreSQL
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Player(Base):
    """Player/Athlete model"""
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    org_player_id = Column(String(100), unique=True, nullable=False, index=True)
    reboot_player_id = Column(String(100), index=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    date_of_birth = Column(String(20))
    height_ft = Column(Float)
    weight_lbs = Column(Float)
    dominant_hand_hitting = Column(String(10))
    dominant_hand_throwing = Column(String(10))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to sessions
    sessions = relationship("Session", back_populates="player", cascade="all, delete-orphan")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'org_player_id': self.org_player_id,
            'reboot_player_id': self.reboot_player_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'date_of_birth': self.date_of_birth,
            'height_ft': self.height_ft,
            'weight_lbs': self.weight_lbs,
            'dominant_hand_hitting': self.dominant_hand_hitting,
            'dominant_hand_throwing': self.dominant_hand_throwing,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Session(Base):
    """Training/Assessment Session model"""
    __tablename__ = 'sessions'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    session_date = Column(DateTime, index=True)
    movement_type_id = Column(Integer)
    movement_type_name = Column(String(100), index=True)
    data_synced = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint: same session can have multiple players
    __table_args__ = (
        UniqueConstraint('session_id', 'player_id', name='uq_session_player'),
    )
    
    # Relationships
    player = relationship("Player", back_populates="sessions")
    biomechanics_data = relationship("BiomechanicsData", back_populates="session", cascade="all, delete-orphan")
    
    def to_dict(self, include_player=True):
        """Convert to dictionary"""
        result = {
            'id': self.id,
            'session_id': self.session_id,
            'player_id': self.player_id,
            'session_date': self.session_date.isoformat() if self.session_date else None,
            'movement_type_id': self.movement_type_id,
            'movement_type_name': self.movement_type_name,
            'data_synced': self.data_synced,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_player and self.player:
            result['player'] = self.player.to_dict()
        
        return result


class BiomechanicsData(Base):
    """Frame-by-frame biomechanics data"""
    __tablename__ = 'biomechanics_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(Integer, ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    timestamp = Column(DateTime)
    frame_number = Column(Integer, index=True)
    joint_angles = Column(JSON)
    joint_positions = Column(JSON)
    joint_velocities = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    session = relationship("Session", back_populates="biomechanics_data")
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'frame_number': self.frame_number,
            'joint_angles': self.joint_angles,
            'joint_positions': self.joint_positions,
            'joint_velocities': self.joint_velocities
        }


class SyncLog(Base):
    """Log of sync operations"""
    __tablename__ = 'sync_log'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    sync_type = Column(String(50), index=True)  # 'players', 'sessions', 'biomechanics', 'full_sync'
    status = Column(String(20), index=True)  # 'success', 'failed', 'in_progress', 'completed'
    records_synced = Column(Integer, default=0)
    players_synced = Column(Integer, default=0)
    sessions_synced = Column(Integer, default=0)
    biomechanics_synced = Column(Integer, default=0)
    error_message = Column(Text)
    started_at = Column(DateTime, default=datetime.utcnow, index=True)
    completed_at = Column(DateTime)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'sync_type': self.sync_type,
            'status': self.status,
            'records_synced': self.records_synced,
            'players_synced': self.players_synced,
            'sessions_synced': self.sessions_synced,
            'biomechanics_synced': self.biomechanics_synced,
            'error_message': self.error_message,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }


class PlayerReport(Base):
    """
    Player Report with KRS Scoring and 4B Framework Metrics
    Phase 1 Week 3-4: Backend API Implementation
    """
    __tablename__ = 'player_reports'
    
    # Primary Keys
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String(100), ForeignKey('sessions.session_id', ondelete='CASCADE'), nullable=False, index=True)
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    
    # KRS Scores (0-100 scale)
    krs_total = Column(Float, nullable=False, index=True)  # (Creation × 0.4) + (Transfer × 0.6)
    krs_level = Column(String(20), nullable=False, index=True)  # FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE
    creation_score = Column(Float, nullable=False)  # 0-100
    transfer_score = Column(Float, nullable=False)  # 0-100
    
    # On-Table Metrics (Exit Velocity Gain)
    on_table_gain_value = Column(Float)  # e.g., 3.1
    on_table_gain_metric = Column(String(10), default='mph')  # 'mph', 'degrees', '%'
    on_table_gain_description = Column(Text)  # e.g., "Exit velocity improvement with optimal mechanics"
    
    # 4B Framework - Brain (Motor Profile)
    brain_motor_profile = Column(String(50))  # Spinner/Slingshotter/Whipper/Titan
    brain_confidence = Column(Float)  # 0-100%
    brain_timing = Column(Float)  # seconds (e.g., 0.24)
    
    # 4B Framework - Body (Creation)
    body_creation_score = Column(Float)  # 0-100 (same as creation_score above)
    body_physical_capacity_mph = Column(Float)  # Max exit velocity capacity
    body_peak_force_n = Column(Float)  # Peak force in Newtons
    
    # 4B Framework - Bat (Transfer)
    bat_transfer_score = Column(Float)  # 0-100 (same as transfer_score above)
    bat_transfer_efficiency = Column(Float)  # 0-100%
    bat_attack_angle_deg = Column(Float)  # Attack angle in degrees
    
    # 4B Framework - Ball (Outcomes)
    ball_exit_velocity_mph = Column(Float)  # Current exit velocity
    ball_capacity_mph = Column(Float)  # Max capacity (same as body_physical_capacity_mph)
    ball_launch_angle_deg = Column(Float)  # Launch angle in degrees
    ball_contact_quality = Column(String(20))  # POOR/FAIR/SOLID/EXCELLENT
    
    # Additional Metrics
    swing_count = Column(Integer)  # Number of swings in session
    duration_minutes = Column(Integer)  # Session duration
    
    # Timestamps
    analyzed_at = Column(DateTime, default=datetime.utcnow, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Unique constraint: one report per session-player combination
    __table_args__ = (
        UniqueConstraint('session_id', 'player_id', name='uq_report_session_player'),
    )
    
    # Relationships
    player = relationship("Player", foreign_keys=[player_id])
    
    def to_dict(self, include_player=False):
        """Convert to dictionary matching UI spec"""
        result = {
            'id': self.id,
            'session_id': self.session_id,
            'player_id': self.player_id,
            
            # KRS Summary
            'krs': {
                'krs_total': round(self.krs_total, 1) if self.krs_total else None,
                'krs_level': self.krs_level,
                'creation_score': round(self.creation_score, 1) if self.creation_score else None,
                'transfer_score': round(self.transfer_score, 1) if self.transfer_score else None,
            },
            
            # On-Table Gain
            'on_table_gain': {
                'value': round(self.on_table_gain_value, 1) if self.on_table_gain_value else None,
                'metric': self.on_table_gain_metric,
                'description': self.on_table_gain_description
            } if self.on_table_gain_value else None,
            
            # 4B Framework
            'framework_metrics': {
                'brain': {
                    'motor_profile': self.brain_motor_profile,
                    'confidence': round(self.brain_confidence, 0) if self.brain_confidence else None,
                    'timing': round(self.brain_timing, 2) if self.brain_timing else None
                },
                'body': {
                    'creation_score': round(self.body_creation_score, 1) if self.body_creation_score else None,
                    'physical_capacity_mph': round(self.body_physical_capacity_mph, 0) if self.body_physical_capacity_mph else None,
                    'peak_force_n': round(self.body_peak_force_n, 0) if self.body_peak_force_n else None
                },
                'bat': {
                    'transfer_score': round(self.bat_transfer_score, 1) if self.bat_transfer_score else None,
                    'transfer_efficiency': round(self.bat_transfer_efficiency, 0) if self.bat_transfer_efficiency else None,
                    'attack_angle_deg': round(self.bat_attack_angle_deg, 0) if self.bat_attack_angle_deg else None
                },
                'ball': {
                    'exit_velocity_mph': round(self.ball_exit_velocity_mph, 0) if self.ball_exit_velocity_mph else None,
                    'capacity_mph': round(self.ball_capacity_mph, 0) if self.ball_capacity_mph else None,
                    'launch_angle_deg': round(self.ball_launch_angle_deg, 0) if self.ball_launch_angle_deg else None,
                    'contact_quality': self.ball_contact_quality
                }
            },
            
            # Session Metadata
            'swing_count': self.swing_count,
            'duration_minutes': self.duration_minutes,
            'analyzed_at': self.analyzed_at.isoformat() if self.analyzed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        # Optionally include player info
        if include_player and self.player:
            result['player'] = self.player.to_dict()
        
        return result
