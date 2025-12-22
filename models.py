"""
Database Models for Reboot Motion Athlete App
SQLAlchemy ORM models for PostgreSQL
"""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON, Text
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
    session_id = Column(String(100), unique=True, nullable=False, index=True)
    player_id = Column(Integer, ForeignKey('players.id', ondelete='CASCADE'), nullable=False, index=True)
    session_date = Column(DateTime, index=True)
    movement_type_id = Column(Integer)
    movement_type_name = Column(String(100), index=True)
    data_synced = Column(Boolean, default=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
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
