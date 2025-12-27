-- ============================================================================
-- CATCHING BARRELS DRILL LIBRARY DATABASE SCHEMA
-- ============================================================================

-- Table 1: Drills (Master drill information)
CREATE TABLE IF NOT EXISTS drills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drill_number INTEGER NOT NULL UNIQUE,
    drill_name VARCHAR(255) NOT NULL,
    tool_required VARCHAR(100),
    dr_kwon_issue VARCHAR(255),
    krs_primary_target VARCHAR(50),
    krs_secondary_target VARCHAR(50),
    motor_profile_fit TEXT,
    description TEXT,
    purpose TEXT,
    video_url VARCHAR(500),
    thumbnail_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Drill Setup (Synapse CCR setup instructions)
CREATE TABLE IF NOT EXISTS drill_setup (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drill_id INTEGER NOT NULL,
    anchor_point TEXT,
    handle_position TEXT,
    body_position TEXT,
    resistance_angle TEXT,
    resistance_level VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drill_id) REFERENCES drills(id)
);

-- Table 3: Drill Progression (4-stage progression)
CREATE TABLE IF NOT EXISTS drill_progression (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drill_id INTEGER NOT NULL,
    stage_number INTEGER NOT NULL,
    stage_name VARCHAR(100),
    description TEXT,
    sets INTEGER,
    reps INTEGER,
    tempo VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drill_id) REFERENCES drills(id)
);

-- Table 4: Drill Cues (Coaching cues)
CREATE TABLE IF NOT EXISTS drill_cues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    drill_id INTEGER NOT NULL,
    cue_text VARCHAR(255),
    cue_order INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drill_id) REFERENCES drills(id)
);

-- Table 5: Player Drill Prescriptions
CREATE TABLE IF NOT EXISTS player_drill_prescriptions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id VARCHAR(255),
    session_id VARCHAR(255),
    drill_id INTEGER NOT NULL,
    prescription_reason TEXT,
    priority INTEGER,
    weeks_assigned INTEGER,
    frequency VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (drill_id) REFERENCES drills(id)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_drills_number ON drills(drill_number);
CREATE INDEX IF NOT EXISTS idx_drill_setup_drill_id ON drill_setup(drill_id);
CREATE INDEX IF NOT EXISTS idx_drill_progression_drill_id ON drill_progression(drill_id);
CREATE INDEX IF NOT EXISTS idx_drill_cues_drill_id ON drill_cues(drill_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_player_id ON player_drill_prescriptions(player_id);
CREATE INDEX IF NOT EXISTS idx_prescriptions_session_id ON player_drill_prescriptions(session_id);

