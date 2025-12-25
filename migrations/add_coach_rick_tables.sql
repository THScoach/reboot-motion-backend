-- ============================================================================
-- COACH RICK AI ENGINE - DATABASE SCHEMA
-- ============================================================================
-- Creates tables for AI coaching analytics, drill tracking, and user progress
-- 
-- Author: Builder 2
-- Date: 2024-12-24
-- Migration: 001_add_coach_rick_tables
-- ============================================================================

-- COACH RICK ANALYSES TABLE
-- Stores complete AI analysis results for each swing video
CREATE TABLE IF NOT EXISTS coach_rick_analyses (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    user_id VARCHAR(255) NOT NULL,
    video_id VARCHAR(255),
    session_id VARCHAR(255) UNIQUE NOT NULL,
    
    -- Motor Profile
    motor_profile VARCHAR(50) NOT NULL, -- Spinner, Whipper, Torquer
    motor_profile_confidence DECIMAL(5,2) NOT NULL,
    motor_characteristics JSONB, -- Detailed profile traits
    
    -- Patterns Detected
    patterns_detected JSONB NOT NULL, -- Array of detected patterns
    primary_issue VARCHAR(255),
    primary_issue_severity VARCHAR(20), -- HIGH, MEDIUM, LOW
    
    -- Drill Prescription
    prescribed_drills JSONB NOT NULL, -- Array of drill IDs
    prescription_duration_weeks INT DEFAULT 3,
    expected_gains TEXT,
    
    -- Metrics
    analysis_metrics JSONB NOT NULL, -- bat_speed, exit_velo, efficiency, etc.
    
    -- AI Messages
    coach_message TEXT, -- Main analysis message from Coach Rick
    drill_intro_message TEXT, -- Drill introduction
    encouragement_message TEXT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_motor_profile (motor_profile),
    INDEX idx_created_at (created_at)
);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_coach_rick_analyses_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER coach_rick_analyses_updated_at
    BEFORE UPDATE ON coach_rick_analyses
    FOR EACH ROW
    EXECUTE FUNCTION update_coach_rick_analyses_updated_at();


-- ============================================================================
-- DRILL COMPLETIONS TABLE
-- Tracks when users complete prescribed drills
-- ============================================================================
CREATE TABLE IF NOT EXISTS drill_completions (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    user_id VARCHAR(255) NOT NULL,
    analysis_id INT REFERENCES coach_rick_analyses(id) ON DELETE CASCADE,
    drill_id VARCHAR(100) NOT NULL, -- rope_swings, lead_arm_one_hand, etc.
    
    -- Completion Details
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reps_completed INT,
    notes TEXT,
    
    -- Quality Tracking (optional, for future)
    quality_score INT CHECK (quality_score BETWEEN 1 AND 5),
    felt_difficulty INT CHECK (felt_difficulty BETWEEN 1 AND 5),
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_analysis_id (analysis_id),
    INDEX idx_drill_id (drill_id),
    INDEX idx_completed_at (completed_at)
);


-- ============================================================================
-- TRAINING ADHERENCE TABLE
-- Weekly tracking of training consistency
-- ============================================================================
CREATE TABLE IF NOT EXISTS training_adherence (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    user_id VARCHAR(255) NOT NULL,
    analysis_id INT REFERENCES coach_rick_analyses(id) ON DELETE CASCADE,
    
    -- Week Tracking
    week_number INT NOT NULL, -- 1, 2, 3 (for 3-week program)
    week_start_date DATE NOT NULL,
    week_end_date DATE NOT NULL,
    
    -- Adherence Metrics
    drills_prescribed INT NOT NULL, -- Total drills for the week
    drills_completed INT DEFAULT 0,
    adherence_percent DECIMAL(5,2) GENERATED ALWAYS AS 
        (CASE WHEN drills_prescribed > 0 
         THEN (drills_completed::DECIMAL / drills_prescribed) * 100 
         ELSE 0 END) STORED,
    
    -- Progress Notes
    progress_notes TEXT,
    coach_feedback TEXT, -- Optional feedback from Coach Rick
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Unique Constraint: One record per user per week per analysis
    UNIQUE (user_id, analysis_id, week_number),
    
    -- Indexes
    INDEX idx_user_id (user_id),
    INDEX idx_analysis_id (analysis_id),
    INDEX idx_week_start (week_start_date)
);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_training_adherence_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER training_adherence_updated_at
    BEFORE UPDATE ON training_adherence
    FOR EACH ROW
    EXECUTE FUNCTION update_training_adherence_updated_at();


-- ============================================================================
-- SAMPLE DATA (FOR TESTING)
-- ============================================================================

-- Insert sample Coach Rick analysis
INSERT INTO coach_rick_analyses (
    user_id,
    video_id,
    session_id,
    motor_profile,
    motor_profile_confidence,
    motor_characteristics,
    patterns_detected,
    primary_issue,
    primary_issue_severity,
    prescribed_drills,
    prescription_duration_weeks,
    expected_gains,
    analysis_metrics,
    coach_message,
    drill_intro_message
) VALUES (
    'user_eric_williams',
    'video_123',
    'session_abc123',
    'Spinner',
    85.0,
    '{"type": "Spinner", "characteristics": ["Rotational power", "Moderate timing gaps"]}'::jsonb,
    '[
        {
            "pattern_id": "spinner_lead_arm_bent",
            "name": "Lead arm not extending through pitch plane",
            "severity": "HIGH",
            "description": "Lead arm stays bent through contact"
        },
        {
            "pattern_id": "spinner_over_rotation",
            "name": "Shoulders over-compensating for lack of arm extension",
            "severity": "HIGH",
            "description": "Arms not creating momentum on pitch plane"
        }
    ]'::jsonb,
    'Lead arm not extending through pitch plane',
    'HIGH',
    '[
        {"drill_id": "rope_swings", "name": "Rope Swings"},
        {"drill_id": "lead_arm_one_hand", "name": "Lead-Arm One-Hand Swings"},
        {"drill_id": "resistance_band_extension", "name": "Resistance Band Extension Drills"}
    ]'::jsonb,
    3,
    '+3-5 mph exit velocity, better away contact, less ground balls',
    '{
        "bat_speed_mph": 82,
        "exit_velocity_mph": 99,
        "efficiency_percent": 111,
        "tempo_score": 87,
        "stability_score": 92
    }'::jsonb,
    'Great to see you working on your swing, Eric! You''re a classic Spinner - you generate power through rotation. I notice your lead arm isn''t fully extending through contact, which is limiting your reach. With a few targeted drills, I''m confident we can unlock 3-5 mph more exit velo.',
    'I''ve put together a drill plan that''s going to help you extend through the zone and drive the ball to all fields. Let''s get to work!'
) ON CONFLICT (session_id) DO NOTHING;


-- Insert sample drill completions
INSERT INTO drill_completions (user_id, analysis_id, drill_id, reps_completed, notes, quality_score)
VALUES 
    ('user_eric_williams', 1, 'rope_swings', 20, 'Felt good extension on last 5 reps', 4),
    ('user_eric_williams', 1, 'lead_arm_one_hand', 30, 'Tough but getting stronger', 3)
ON CONFLICT DO NOTHING;


-- Insert sample training adherence
INSERT INTO training_adherence (
    user_id,
    analysis_id,
    week_number,
    week_start_date,
    week_end_date,
    drills_prescribed,
    drills_completed,
    progress_notes
) VALUES (
    'user_eric_williams',
    1,
    1,
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '6 days',
    21, -- 3 drills * 7 days
    15, -- Completed 15 so far
    'Strong start, focusing on rope swings daily'
) ON CONFLICT (user_id, analysis_id, week_number) DO NOTHING;


-- ============================================================================
-- QUERIES FOR TESTING
-- ============================================================================

-- Get all analyses for a user
-- SELECT * FROM coach_rick_analyses WHERE user_id = 'user_eric_williams';

-- Get drill completion rate
-- SELECT 
--     ca.session_id,
--     ca.motor_profile,
--     COUNT(dc.id) as drills_completed,
--     ca.created_at
-- FROM coach_rick_analyses ca
-- LEFT JOIN drill_completions dc ON ca.id = dc.analysis_id
-- WHERE ca.user_id = 'user_eric_williams'
-- GROUP BY ca.session_id, ca.motor_profile, ca.created_at;

-- Get weekly adherence
-- SELECT 
--     week_number,
--     adherence_percent,
--     drills_completed,
--     drills_prescribed
-- FROM training_adherence
-- WHERE user_id = 'user_eric_williams'
-- ORDER BY week_number;


-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================
-- Tables created:
--   1. coach_rick_analyses (swing analysis results)
--   2. drill_completions (drill tracking)
--   3. training_adherence (weekly progress)
--
-- Ready for Coach Rick AI Engine integration
-- ============================================================================
