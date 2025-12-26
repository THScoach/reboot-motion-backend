"""
PRIORITY 18: USER ACCOUNTS & MANUAL PLAYER IMPORT
==================================================

User account management and manual import system for Reboot Motion data

Features:
- User account creation and management
- Manual player import from Reboot Motion data
- Model player designation (pro benchmarks)
- Biomechanics data parsing and analysis
- Player comparison against models

Author: Reboot Motion Development Team
Date: 2025-12-24
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
from datetime import datetime
from enum import Enum
import uuid
import hashlib


# ============================================================================
# ENUMERATIONS
# ============================================================================

class UserRole(Enum):
    """User roles in the system"""
    ADMIN = "admin"
    COACH = "coach"
    ATHLETE = "athlete"
    PARENT = "parent"


class PlayerType(Enum):
    """Type of player in system"""
    ACTIVE_ATHLETE = "active_athlete"  # Current player you're coaching
    MODEL_PLAYER = "model_player"  # Pro benchmark (e.g., Ronald Acuña)
    HISTORICAL = "historical"  # Past player data


class ImportStatus(Enum):
    """Status of data import"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class User:
    """User account in the system"""
    user_id: str
    email: str
    password_hash: str
    role: UserRole
    first_name: str
    last_name: str
    created_date: datetime
    last_login: Optional[datetime] = None
    is_active: bool = True
    organization: Optional[str] = None
    phone: Optional[str] = None
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'role': self.role.value,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'created_date': self.created_date.isoformat(),
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active,
            'organization': self.organization,
            'phone': self.phone
        }


@dataclass
class Player:
    """Player profile (can be active athlete or model player)"""
    player_id: str
    user_id: Optional[str]  # Linked user account (None for model players)
    player_type: PlayerType
    first_name: str
    last_name: str
    created_date: datetime
    
    # Biometrics
    height_inches: Optional[int] = None
    wingspan_inches: Optional[int] = None
    weight_lbs: Optional[int] = None
    age: Optional[int] = None
    
    # Baseball info
    position: Optional[str] = None
    bats: Optional[str] = None  # R, L, S
    throws: Optional[str] = None  # R, L
    team: Optional[str] = None
    level: Optional[str] = None  # MLB, MiLB, College, HS, etc.
    
    # Model player specific
    is_model: bool = False
    model_description: Optional[str] = None
    
    # Reboot Motion data
    reboot_player_id: Optional[str] = None
    has_biomechanics_data: bool = False
    
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'player_id': self.player_id,
            'user_id': self.user_id,
            'player_type': self.player_type.value,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'height_inches': self.height_inches,
            'wingspan_inches': self.wingspan_inches,
            'weight_lbs': self.weight_lbs,
            'age': self.age,
            'position': self.position,
            'bats': self.bats,
            'throws': self.throws,
            'team': self.team,
            'level': self.level,
            'is_model': self.is_model,
            'model_description': self.model_description,
            'reboot_player_id': self.reboot_player_id,
            'has_biomechanics_data': self.has_biomechanics_data,
            'created_date': self.created_date.isoformat()
        }


@dataclass
class BiomechanicsData:
    """Biomechanics data from Reboot Motion"""
    data_id: str
    player_id: str
    session_date: datetime
    
    # Scores
    ground_score: int
    engine_score: int
    weapon_score: int
    
    # Performance metrics
    bat_speed_mph: Optional[float] = None
    exit_velocity_mph: Optional[float] = None
    attack_angle: Optional[float] = None
    
    # Kinetic data
    rotation_ke_joules: Optional[float] = None
    translation_ke_joules: Optional[float] = None
    
    # Angular velocities
    pelvis_angular_velocity: Optional[float] = None
    torso_angular_velocity: Optional[float] = None
    bat_angular_velocity: Optional[float] = None
    
    # Timing data
    time_to_contact_ms: Optional[float] = None
    stride_length_in: Optional[float] = None
    
    # Raw Reboot Motion data
    reboot_session_id: Optional[str] = None
    raw_data: Optional[Dict[str, Any]] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'data_id': self.data_id,
            'player_id': self.player_id,
            'session_date': self.session_date.isoformat(),
            'ground_score': self.ground_score,
            'engine_score': self.engine_score,
            'weapon_score': self.weapon_score,
            'bat_speed_mph': self.bat_speed_mph,
            'exit_velocity_mph': self.exit_velocity_mph,
            'attack_angle': self.attack_angle,
            'rotation_ke_joules': self.rotation_ke_joules,
            'translation_ke_joules': self.translation_ke_joules,
            'pelvis_angular_velocity': self.pelvis_angular_velocity,
            'torso_angular_velocity': self.torso_angular_velocity,
            'bat_angular_velocity': self.bat_angular_velocity,
            'time_to_contact_ms': self.time_to_contact_ms,
            'stride_length_in': self.stride_length_in,
            'reboot_session_id': self.reboot_session_id
        }


@dataclass
class ImportRecord:
    """Record of manual data import"""
    import_id: str
    imported_by_user_id: str
    import_date: datetime
    status: ImportStatus
    player_id: str
    player_name: str
    data_source: str  # "reboot_motion_manual"
    records_imported: int
    notes: Optional[str] = None
    error_message: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'import_id': self.import_id,
            'imported_by_user_id': self.imported_by_user_id,
            'import_date': self.import_date.isoformat(),
            'status': self.status.value,
            'player_id': self.player_id,
            'player_name': self.player_name,
            'data_source': self.data_source,
            'records_imported': self.records_imported,
            'notes': self.notes,
            'error_message': self.error_message
        }


# ============================================================================
# USER ACCOUNT MANAGEMENT
# ============================================================================

class UserAccountManager:
    """
    User account management system
    
    Features:
    - User registration
    - Authentication
    - Profile management
    - Role-based access
    """
    
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.email_index: Dict[str, str] = {}  # email -> user_id
    
    def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create new user account"""
        # Check if email already exists
        email = user_data['email'].lower()
        if email in self.email_index:
            raise ValueError(f"Email {email} already exists")
        
        user_id = str(uuid.uuid4())
        
        # Hash password (in production, use bcrypt or similar)
        password_hash = hashlib.sha256(user_data['password'].encode()).hexdigest()
        
        user = User(
            user_id=user_id,
            email=email,
            password_hash=password_hash,
            role=UserRole(user_data.get('role', 'athlete')),
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            created_date=datetime.now(),
            organization=user_data.get('organization'),
            phone=user_data.get('phone')
        )
        
        self.users[user_id] = user
        self.email_index[email] = user_id
        
        return user_id
    
    def authenticate(self, email: str, password: str) -> Optional[User]:
        """Authenticate user"""
        email = email.lower()
        user_id = self.email_index.get(email)
        
        if not user_id:
            return None
        
        user = self.users[user_id]
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        if user.password_hash == password_hash and user.is_active:
            user.last_login = datetime.now()
            return user
        
        return None
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID"""
        return self.users.get(user_id)
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> bool:
        """Update user profile"""
        user = self.users.get(user_id)
        if not user:
            return False
        
        for key, value in updates.items():
            if hasattr(user, key) and key not in ['user_id', 'password_hash', 'created_date']:
                setattr(user, key, value)
        
        return True
    
    def list_users(self, role: Optional[str] = None) -> List[User]:
        """List all users, optionally filtered by role"""
        users = list(self.users.values())
        
        if role:
            role_enum = UserRole(role)
            users = [u for u in users if u.role == role_enum]
        
        return users


# ============================================================================
# PLAYER IMPORT SYSTEM
# ============================================================================

class PlayerImportSystem:
    """
    Manual player import system for Reboot Motion data
    
    Features:
    - Manual player selection and import
    - Model player designation
    - Biomechanics data parsing
    - Import tracking
    """
    
    def __init__(self):
        self.players: Dict[str, Player] = {}
        self.biomechanics_data: Dict[str, List[BiomechanicsData]] = {}  # player_id -> data
        self.import_records: List[ImportRecord] = []
        self.model_players: List[str] = []  # player_ids of model players
    
    # ========================================================================
    # PLAYER MANAGEMENT
    # ========================================================================
    
    def create_player(self, player_data: Dict[str, Any]) -> str:
        """Create player profile"""
        player_id = str(uuid.uuid4())
        
        player = Player(
            player_id=player_id,
            user_id=player_data.get('user_id'),
            player_type=PlayerType(player_data.get('player_type', 'active_athlete')),
            first_name=player_data['first_name'],
            last_name=player_data['last_name'],
            created_date=datetime.now(),
            height_inches=player_data.get('height_inches'),
            wingspan_inches=player_data.get('wingspan_inches'),
            weight_lbs=player_data.get('weight_lbs'),
            age=player_data.get('age'),
            position=player_data.get('position'),
            bats=player_data.get('bats'),
            throws=player_data.get('throws'),
            team=player_data.get('team'),
            level=player_data.get('level'),
            reboot_player_id=player_data.get('reboot_player_id')
        )
        
        self.players[player_id] = player
        self.biomechanics_data[player_id] = []
        
        return player_id
    
    def get_player(self, player_id: str) -> Optional[Player]:
        """Get player by ID"""
        return self.players.get(player_id)
    
    def list_players(self, player_type: Optional[str] = None, 
                     include_models_only: bool = False) -> List[Player]:
        """List players with optional filters"""
        players = list(self.players.values())
        
        if player_type:
            type_enum = PlayerType(player_type)
            players = [p for p in players if p.player_type == type_enum]
        
        if include_models_only:
            players = [p for p in players if p.is_model]
        
        return players
    
    # ========================================================================
    # MODEL PLAYER DESIGNATION
    # ========================================================================
    
    def designate_as_model(self, player_id: str, description: str) -> bool:
        """
        Designate a player as a model (benchmark player)
        
        Example: Ronald Acuña as power/speed model
        """
        player = self.players.get(player_id)
        if not player:
            return False
        
        player.is_model = True
        player.model_description = description
        player.player_type = PlayerType.MODEL_PLAYER
        
        if player_id not in self.model_players:
            self.model_players.append(player_id)
        
        return True
    
    def remove_model_designation(self, player_id: str) -> bool:
        """Remove model player designation"""
        player = self.players.get(player_id)
        if not player:
            return False
        
        player.is_model = False
        player.model_description = None
        
        if player_id in self.model_players:
            self.model_players.remove(player_id)
        
        return True
    
    def get_model_players(self) -> List[Player]:
        """Get all model players"""
        return [self.players[pid] for pid in self.model_players if pid in self.players]
    
    # ========================================================================
    # BIOMECHANICS DATA IMPORT
    # ========================================================================
    
    def import_biomechanics_data(self, player_id: str, data: Dict[str, Any], 
                                  imported_by: str) -> str:
        """
        Manually import biomechanics data for a player
        
        This is the manual process you mentioned - you select which
        players to import from Reboot Motion data
        """
        player = self.players.get(player_id)
        if not player:
            raise ValueError(f"Player {player_id} not found")
        
        # Create import record
        import_id = str(uuid.uuid4())
        import_record = ImportRecord(
            import_id=import_id,
            imported_by_user_id=imported_by,
            import_date=datetime.now(),
            status=ImportStatus.PROCESSING,
            player_id=player_id,
            player_name=player.full_name,
            data_source="reboot_motion_manual",
            records_imported=0
        )
        
        try:
            # Parse and store biomechanics data
            data_id = str(uuid.uuid4())
            
            biomech_data = BiomechanicsData(
                data_id=data_id,
                player_id=player_id,
                session_date=datetime.fromisoformat(data['session_date']) if isinstance(data['session_date'], str) else data['session_date'],
                ground_score=data['ground_score'],
                engine_score=data['engine_score'],
                weapon_score=data['weapon_score'],
                bat_speed_mph=data.get('bat_speed_mph'),
                exit_velocity_mph=data.get('exit_velocity_mph'),
                attack_angle=data.get('attack_angle'),
                rotation_ke_joules=data.get('rotation_ke_joules'),
                translation_ke_joules=data.get('translation_ke_joules'),
                pelvis_angular_velocity=data.get('pelvis_angular_velocity'),
                torso_angular_velocity=data.get('torso_angular_velocity'),
                bat_angular_velocity=data.get('bat_angular_velocity'),
                time_to_contact_ms=data.get('time_to_contact_ms'),
                stride_length_in=data.get('stride_length_in'),
                reboot_session_id=data.get('reboot_session_id'),
                raw_data=data.get('raw_data')
            )
            
            self.biomechanics_data[player_id].append(biomech_data)
            player.has_biomechanics_data = True
            
            # Update import record
            import_record.status = ImportStatus.COMPLETED
            import_record.records_imported = 1
            
        except Exception as e:
            import_record.status = ImportStatus.FAILED
            import_record.error_message = str(e)
        
        self.import_records.append(import_record)
        return import_id
    
    def get_player_biomechanics(self, player_id: str) -> List[BiomechanicsData]:
        """Get all biomechanics data for a player"""
        return self.biomechanics_data.get(player_id, [])
    
    def get_latest_biomechanics(self, player_id: str) -> Optional[BiomechanicsData]:
        """Get most recent biomechanics data for a player"""
        data_list = self.biomechanics_data.get(player_id, [])
        if not data_list:
            return None
        
        return sorted(data_list, key=lambda x: x.session_date, reverse=True)[0]
    
    # ========================================================================
    # PLAYER COMPARISON
    # ========================================================================
    
    def compare_to_model(self, player_id: str, model_player_id: str) -> Dict[str, Any]:
        """
        Compare a player's biomechanics to a model player
        
        Example: Compare your athlete to Ronald Acuña
        """
        player = self.players.get(player_id)
        model = self.players.get(model_player_id)
        
        if not player or not model:
            raise ValueError("Player or model not found")
        
        if not model.is_model:
            raise ValueError(f"{model.full_name} is not designated as a model player")
        
        player_data = self.get_latest_biomechanics(player_id)
        model_data = self.get_latest_biomechanics(model_player_id)
        
        if not player_data or not model_data:
            raise ValueError("Missing biomechanics data for comparison")
        
        comparison = {
            'player': player.to_dict(),
            'model': model.to_dict(),
            'comparison_date': datetime.now().isoformat(),
            'metrics': {
                'ground_score': {
                    'player': player_data.ground_score,
                    'model': model_data.ground_score,
                    'difference': player_data.ground_score - model_data.ground_score,
                    'percent_of_model': (player_data.ground_score / model_data.ground_score * 100) if model_data.ground_score > 0 else 0
                },
                'engine_score': {
                    'player': player_data.engine_score,
                    'model': model_data.engine_score,
                    'difference': player_data.engine_score - model_data.engine_score,
                    'percent_of_model': (player_data.engine_score / model_data.engine_score * 100) if model_data.engine_score > 0 else 0
                },
                'weapon_score': {
                    'player': player_data.weapon_score,
                    'model': model_data.weapon_score,
                    'difference': player_data.weapon_score - model_data.weapon_score,
                    'percent_of_model': (player_data.weapon_score / model_data.weapon_score * 100) if model_data.weapon_score > 0 else 0
                }
            }
        }
        
        # Add bat speed comparison if available
        if player_data.bat_speed_mph and model_data.bat_speed_mph:
            comparison['metrics']['bat_speed'] = {
                'player': player_data.bat_speed_mph,
                'model': model_data.bat_speed_mph,
                'difference': player_data.bat_speed_mph - model_data.bat_speed_mph,
                'percent_of_model': (player_data.bat_speed_mph / model_data.bat_speed_mph * 100)
            }
        
        return comparison


# ============================================================================
# TEST & DEMONSTRATION
# ============================================================================

def test_priority_18():
    """Test user accounts, player import, and model players"""
    print("=" * 70)
    print("PRIORITY 18: USER ACCOUNTS & MANUAL IMPORT")
    print("=" * 70)
    print()
    
    # Initialize systems
    user_manager = UserAccountManager()
    player_system = PlayerImportSystem()
    
    # Test 1: Create User Accounts
    print("1. CREATING USER ACCOUNTS")
    print("-" * 70)
    
    # Coach account
    coach_id = user_manager.create_user({
        'email': 'coach@thsbaseball.com',
        'password': 'secure_password_123',
        'role': 'coach',
        'first_name': 'Mike',
        'last_name': 'Johnson',
        'organization': 'Tomball High School Baseball'
    })
    print(f"✅ Coach account created: {coach_id}")
    
    # Athlete accounts
    athlete1_id = user_manager.create_user({
        'email': 'eric.williams@student.com',
        'password': 'athlete_pass',
        'role': 'athlete',
        'first_name': 'Eric',
        'last_name': 'Williams'
    })
    print(f"✅ Athlete account created: {athlete1_id}")
    print()
    
    # Test 2: Authenticate
    print("2. USER AUTHENTICATION")
    print("-" * 70)
    coach = user_manager.authenticate('coach@thsbaseball.com', 'secure_password_123')
    if coach:
        print(f"✅ Coach authenticated: {coach.full_name}")
    print()
    
    # Test 3: Manual Player Import
    print("3. MANUAL PLAYER IMPORT (from Reboot Motion)")
    print("-" * 70)
    
    # Import Eric Williams
    eric_player_id = player_system.create_player({
        'user_id': athlete1_id,
        'player_type': 'active_athlete',
        'first_name': 'Eric',
        'last_name': 'Williams',
        'height_inches': 68,
        'wingspan_inches': 69,
        'weight_lbs': 190,
        'age': 19,
        'position': 'OF',
        'bats': 'R',
        'throws': 'R',
        'team': 'Tomball High School',
        'level': 'High School',
        'reboot_player_id': 'reboot_eric_123'
    })
    print(f"✅ Player imported: Eric Williams ({eric_player_id})")
    
    # Import biomechanics data
    import_id = player_system.import_biomechanics_data(
        eric_player_id,
        {
            'session_date': datetime.now(),
            'ground_score': 72,
            'engine_score': 58,
            'weapon_score': 55,
            'bat_speed_mph': 67.0,
            'exit_velocity_mph': 85.0,
            'rotation_ke_joules': 3743,
            'translation_ke_joules': 421,
            'reboot_session_id': 'session_123'
        },
        coach_id
    )
    print(f"✅ Biomechanics data imported: {import_id}")
    print()
    
    # Test 4: Add Model Player (Ronald Acuña)
    print("4. ADDING MODEL PLAYER - Ronald Acuña Jr.")
    print("-" * 70)
    
    acuna_player_id = player_system.create_player({
        'player_type': 'model_player',
        'first_name': 'Ronald',
        'last_name': 'Acuña Jr.',
        'height_inches': 72,
        'wingspan_inches': 74,
        'weight_lbs': 205,
        'age': 26,
        'position': 'OF',
        'bats': 'R',
        'throws': 'R',
        'team': 'Atlanta Braves',
        'level': 'MLB',
        'reboot_player_id': 'reboot_acuna_mlb'
    })
    
    # Designate as model
    player_system.designate_as_model(
        acuna_player_id,
        "Elite power/speed combination. Premium athleticism with explosive rotation."
    )
    print(f"✅ Model player added: Ronald Acuña Jr. ({acuna_player_id})")
    
    # Import Acuña's biomechanics (example data)
    player_system.import_biomechanics_data(
        acuna_player_id,
        {
            'session_date': datetime.now(),
            'ground_score': 95,
            'engine_score': 92,
            'weapon_score': 88,
            'bat_speed_mph': 78.5,
            'exit_velocity_mph': 105.0,
            'rotation_ke_joules': 5200,
            'translation_ke_joules': 580,
            'reboot_session_id': 'session_acuna_mlb'
        },
        coach_id
    )
    print(f"✅ Acuña biomechanics data imported")
    print()
    
    # Test 5: Compare Player to Model
    print("5. COMPARING ERIC WILLIAMS TO RONALD ACUÑA")
    print("-" * 70)
    
    comparison = player_system.compare_to_model(eric_player_id, acuna_player_id)
    
    print(f"Player: {comparison['player']['full_name']}")
    print(f"Model:  {comparison['model']['full_name']}")
    print(f"Model Description: {comparison['model']['model_description']}")
    print()
    print("METRIC COMPARISON:")
    
    for metric, data in comparison['metrics'].items():
        print(f"\n  {metric.upper()}:")
        print(f"    Player: {data['player']}")
        print(f"    Model:  {data['model']}")
        print(f"    Difference: {data['difference']:+}")
        print(f"    % of Model: {data['percent_of_model']:.1f}%")
    
    print()
    
    # Test 6: List Model Players
    print("6. MODEL PLAYERS IN SYSTEM")
    print("-" * 70)
    model_players = player_system.get_model_players()
    for model in model_players:
        print(f"✅ {model.full_name} ({model.team}, {model.level})")
        print(f"   Description: {model.model_description}")
    print()
    
    print("=" * 70)
    print("✅ PRIORITY 18 SYSTEM READY!")
    print("=" * 70)
    print()
    print("FEATURES AVAILABLE:")
    print("  ✅ User account creation and authentication")
    print("  ✅ Manual player import from Reboot Motion")
    print("  ✅ Model player designation (pro benchmarks)")
    print("  ✅ Biomechanics data import and storage")
    print("  ✅ Player-to-model comparison")
    print()


if __name__ == '__main__':
    test_priority_18()
