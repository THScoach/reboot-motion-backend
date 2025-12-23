-- Create analysis_results table for storing session data
CREATE TABLE IF NOT EXISTS analysis_results (
    id SERIAL PRIMARY KEY,
    
    -- Foreign keys
    player_id INTEGER NOT NULL,
    session_id INTEGER UNIQUE,  -- Optional: Link to sessions table if exists
    
    -- Player info snapshot (for historical reference)
    player_name VARCHAR(255),
    height_inches INTEGER,
    weight_lbs INTEGER,
    wingspan_inches INTEGER,
    age_years INTEGER,
    bat_length_inches INTEGER,
    bat_weight_oz INTEGER,
    
    -- Potential metrics
    bat_speed_potential_mph FLOAT NOT NULL,
    exit_velo_potential_tee_mph FLOAT,
    exit_velo_potential_pitched_mph FLOAT,
    
    -- Actual performance metrics
    bat_speed_actual_mph FLOAT NOT NULL,
    exit_velo_actual_mph FLOAT,
    
    -- Gap metrics
    bat_speed_gap_mph FLOAT NOT NULL,
    exit_velo_gap_mph FLOAT,
    pct_potential_achieved FLOAT NOT NULL,
    pct_potential_untapped FLOAT NOT NULL,
    gap_status VARCHAR(50),  -- 'BELOW_POTENTIAL', 'AT_POTENTIAL', 'ABOVE_POTENTIAL'
    
    -- Component scores (0-100 scale)
    ground_score FLOAT NOT NULL,
    engine_score FLOAT NOT NULL,
    weapon_score FLOAT NOT NULL,
    overall_efficiency FLOAT NOT NULL,
    
    -- Motor profile classification
    motor_profile VARCHAR(50) NOT NULL,  -- 'TITAN', 'SPINNER', 'SLINGSHOTTER', 'WHIPPER', 'BALANCED'
    motor_profile_confidence FLOAT,
    motor_profile_secondary VARCHAR(50),
    
    -- Weakest component analysis
    weakest_component VARCHAR(50),  -- 'GROUND', 'ENGINE', 'WEAPON'
    weakest_component_score FLOAT,
    weakest_component_priority VARCHAR(50),  -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW'
    
    -- Recommendations
    primary_focus_component VARCHAR(50),
    estimated_gain_mph FLOAT,
    total_estimated_gain_mph FLOAT,
    recommended_drills JSONB,  -- Array of drill objects
    training_frequency VARCHAR(255),
    
    -- Kinematic sequence data
    kinematic_sequence JSONB,  -- {pelvis_ms, torso_ms, arm_ms, hand_ms}
    tempo_ratio FLOAT,
    
    -- Energy distribution
    energy_distribution JSONB,  -- {lowerhalf_pct, torso_pct, arms_pct}
    
    -- Biomechanics metrics
    hip_shoulder_separation_deg FLOAT,
    peak_pelvis_velocity_ms FLOAT,
    peak_torso_velocity_ms FLOAT,
    peak_hand_velocity_ms FLOAT,
    
    -- Metadata
    analysis_date TIMESTAMP NOT NULL DEFAULT NOW(),
    video_url TEXT,
    video_filename VARCHAR(255),
    csv_filename VARCHAR(255),
    notes TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for efficient queries
CREATE INDEX IF NOT EXISTS idx_analysis_player_date 
    ON analysis_results(player_id, analysis_date DESC);

CREATE INDEX IF NOT EXISTS idx_analysis_session 
    ON analysis_results(session_id);

CREATE INDEX IF NOT EXISTS idx_analysis_motor_profile 
    ON analysis_results(motor_profile);

CREATE INDEX IF NOT EXISTS idx_analysis_date 
    ON analysis_results(analysis_date DESC);

-- Create trigger for updated_at timestamp
CREATE OR REPLACE FUNCTION update_analysis_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_analysis_updated_at
    BEFORE UPDATE ON analysis_results
    FOR EACH ROW
    EXECUTE FUNCTION update_analysis_updated_at();

-- Optional: Create view for latest analysis per player
CREATE OR REPLACE VIEW player_latest_analysis AS
SELECT DISTINCT ON (player_id)
    *
FROM analysis_results
ORDER BY player_id, analysis_date DESC;

-- Add comments for documentation
COMMENT ON TABLE analysis_results IS 'Stores complete analysis results for each player session';
COMMENT ON COLUMN analysis_results.player_id IS 'Reference to player (no FK constraint for flexibility)';
COMMENT ON COLUMN analysis_results.bat_speed_potential_mph IS 'Calculated potential bat speed based on anthropometrics';
COMMENT ON COLUMN analysis_results.gap_status IS 'BELOW_POTENTIAL, AT_POTENTIAL, or ABOVE_POTENTIAL';
COMMENT ON COLUMN analysis_results.motor_profile IS 'TITAN, SPINNER, SLINGSHOTTER, WHIPPER, or BALANCED';
COMMENT ON COLUMN analysis_results.recommended_drills IS 'JSON array of drill recommendations';
COMMENT ON COLUMN analysis_results.kinematic_sequence IS 'JSON object with timing data (ms) for pelvis, torso, arm, hand';
COMMENT ON COLUMN analysis_results.energy_distribution IS 'JSON object with percentage distribution';
