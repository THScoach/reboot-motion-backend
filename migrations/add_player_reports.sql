"""
Database Migration: Add PlayerReport table
Phase 1 Week 3-4: Priority 1
Run this script to create the player_reports table
"""

-- Add PlayerReport table for KRS scoring and 4B Framework
CREATE TABLE IF NOT EXISTS player_reports (
    -- Primary Keys
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL REFERENCES sessions(session_id) ON DELETE CASCADE,
    player_id INTEGER NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    
    -- KRS Scores (0-100 scale)
    krs_total FLOAT NOT NULL,  -- (Creation × 0.4) + (Transfer × 0.6)
    krs_level VARCHAR(20) NOT NULL,  -- FOUNDATION/BUILDING/DEVELOPING/ADVANCED/ELITE
    creation_score FLOAT NOT NULL,  -- 0-100
    transfer_score FLOAT NOT NULL,  -- 0-100
    
    -- On-Table Metrics (Exit Velocity Gain)
    on_table_gain_value FLOAT,  -- e.g., 3.1
    on_table_gain_metric VARCHAR(10) DEFAULT 'mph',  -- 'mph', 'degrees', '%'
    on_table_gain_description TEXT,  -- e.g., "Exit velocity improvement with optimal mechanics"
    
    -- 4B Framework - Brain (Motor Profile)
    brain_motor_profile VARCHAR(50),  -- Spinner/Slingshotter/Whipper/Titan
    brain_confidence FLOAT,  -- 0-100%
    brain_timing FLOAT,  -- seconds (e.g., 0.24)
    
    -- 4B Framework - Body (Creation)
    body_creation_score FLOAT,  -- 0-100 (same as creation_score above)
    body_physical_capacity_mph FLOAT,  -- Max exit velocity capacity
    body_peak_force_n FLOAT,  -- Peak force in Newtons
    
    -- 4B Framework - Bat (Transfer)
    bat_transfer_score FLOAT,  -- 0-100 (same as transfer_score above)
    bat_transfer_efficiency FLOAT,  -- 0-100%
    bat_attack_angle_deg FLOAT,  -- Attack angle in degrees
    
    -- 4B Framework - Ball (Outcomes)
    ball_exit_velocity_mph FLOAT,  -- Current exit velocity
    ball_capacity_mph FLOAT,  -- Max capacity (same as body_physical_capacity_mph)
    ball_launch_angle_deg FLOAT,  -- Launch angle in degrees
    ball_contact_quality VARCHAR(20),  -- POOR/FAIR/SOLID/EXCELLENT
    
    -- Additional Metrics
    swing_count INTEGER,  -- Number of swings in session
    duration_minutes INTEGER,  -- Session duration
    
    -- Timestamps
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique constraint: one report per session-player combination
    CONSTRAINT uq_report_session_player UNIQUE (session_id, player_id)
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_player_reports_session_id ON player_reports(session_id);
CREATE INDEX IF NOT EXISTS idx_player_reports_player_id ON player_reports(player_id);
CREATE INDEX IF NOT EXISTS idx_player_reports_krs_total ON player_reports(krs_total);
CREATE INDEX IF NOT EXISTS idx_player_reports_krs_level ON player_reports(krs_level);
CREATE INDEX IF NOT EXISTS idx_player_reports_analyzed_at ON player_reports(analyzed_at);

-- Add comments for documentation
COMMENT ON TABLE player_reports IS 'Player reports with KRS scoring and 4B Framework metrics (Phase 1 Week 3-4)';
COMMENT ON COLUMN player_reports.krs_total IS 'KRS total score: (Creation × 0.4) + (Transfer × 0.6), range 0-100';
COMMENT ON COLUMN player_reports.krs_level IS 'KRS level: FOUNDATION (0-40), BUILDING (40-60), DEVELOPING (60-75), ADVANCED (75-85), ELITE (85-100)';
COMMENT ON COLUMN player_reports.creation_score IS 'Creation score: ability to generate force (0-100)';
COMMENT ON COLUMN player_reports.transfer_score IS 'Transfer score: ability to transfer force to bat (0-100)';
COMMENT ON COLUMN player_reports.on_table_gain_value IS 'Exit velocity improvement potential with optimal mechanics (mph)';

-- Verify table creation
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'player_reports'
ORDER BY ordinal_position;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '✅ Migration complete: player_reports table created successfully';
    RAISE NOTICE '📊 Table supports KRS scoring (0-100 scale) and 4B Framework metrics';
    RAISE NOTICE '🔗 Foreign keys: session_id → sessions, player_id → players';
    RAISE NOTICE '📈 Indexes created for: session_id, player_id, krs_total, krs_level, analyzed_at';
END $$;
