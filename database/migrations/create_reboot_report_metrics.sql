"""
Database schema for storing Reboot Motion report metrics
These metrics are extracted from Reboot's PDF/PNG reports since the API
doesn't expose the actual rotation data shown in their reports.
"""

CREATE_REBOOT_REPORT_METRICS_TABLE = """
CREATE TABLE IF NOT EXISTS reboot_report_metrics (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) NOT NULL,
    org_player_id VARCHAR(255),
    
    -- Report metadata
    report_file_path TEXT,
    report_upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    data_source VARCHAR(50) DEFAULT 'manual_input', -- 'manual_input', 'automated_parser', 'api'
    extraction_confidence FLOAT DEFAULT 1.0,
    
    -- Rotation metrics (from "Torso Kinematics" chart)
    pelvis_rotation_rom_deg FLOAT,  -- Actual swing rotation (e.g., 60°)
    torso_rotation_rom_deg FLOAT,   -- Actual swing rotation (e.g., 25°)
    x_factor_deg FLOAT,              -- Hip-shoulder separation
    
    -- Kinematic sequence metrics (from chart and table)
    pelvis_peak_velocity_deg_per_s FLOAT,
    pelvis_peak_timing_pct FLOAT,   -- % of swing when pelvis peaks
    torso_peak_velocity_deg_per_s FLOAT,
    torso_peak_timing_pct FLOAT,    -- % of swing when torso peaks
    
    -- Additional metrics from report tables
    peak_shoulder_internal_rotation_rear_deg FLOAT,
    peak_shoulder_internal_rotation_lead_deg FLOAT,
    hip_to_torso_peak_angular_velocity FLOAT,
    min_pelvis_torso_separation_deg FLOAT,
    max_shoulder_rotation_at_max_torque_deg_per_s FLOAT,
    rear_elbow_wrist_velocity_ratio FLOAT,
    
    -- Bat metrics (if available in report)
    bat_speed_mph FLOAT,
    exit_velocity_mph FLOAT,
    attack_angle_deg FLOAT,
    
    -- Event frames (if available)
    load_frame INTEGER,
    stride_frame INTEGER,
    contact_frame INTEGER,
    follow_through_frame INTEGER,
    
    -- Validation
    validated_against_hittrax BOOLEAN DEFAULT FALSE,
    hittrax_bat_speed_mph FLOAT,
    hittrax_exit_velocity_mph FLOAT,
    validation_notes TEXT,
    
    -- Audit
    created_by VARCHAR(100),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT,
    
    -- Constraints
    UNIQUE(session_id),
    FOREIGN KEY (session_id) REFERENCES reboot_sessions(session_id) ON DELETE CASCADE
);

-- Index for quick lookups
CREATE INDEX IF NOT EXISTS idx_report_metrics_session ON reboot_report_metrics(session_id);
CREATE INDEX IF NOT EXISTS idx_report_metrics_player ON reboot_report_metrics(org_player_id);

-- Comments
COMMENT ON TABLE reboot_report_metrics IS 'Stores metrics extracted from Reboot Motion reports (not API/CSV)';
COMMENT ON COLUMN reboot_report_metrics.pelvis_rotation_rom_deg IS 'Actual swing rotation from Torso Kinematics chart (e.g., Connor: 60°)';
COMMENT ON COLUMN reboot_report_metrics.data_source IS 'How metrics were obtained: manual_input, automated_parser, or api';
COMMENT ON COLUMN reboot_report_metrics.extraction_confidence IS '0-1 confidence score for automated parsing';
"""

# Sample insert for Connor Gray
INSERT_CONNOR_EXAMPLE = """
INSERT INTO reboot_report_metrics (
    session_id,
    org_player_id,
    report_file_path,
    data_source,
    pelvis_rotation_rom_deg,
    torso_rotation_rom_deg,
    validated_against_hittrax,
    hittrax_bat_speed_mph,
    hittrax_exit_velocity_mph,
    created_by,
    notes
) VALUES (
    '4f1a7010-1324-469d-8e1a-e05a1dc45f2e',
    '80e77691-d7cc-4ebb-b955-2fd45676f0ca',
    '/uploads/reports/connor_reboot_report.png',
    'manual_input',
    60.0,  -- From "Torso Kinematics" chart (purple line: ~10° to ~70°)
    25.0,  -- From "Torso Kinematics" chart (orange line: ~15° to ~40°)
    TRUE,
    59.4,  -- HitTrax derived from 98 mph exit velocity
    98.0,  -- HitTrax measured
    'Coach Rick',
    'Manual extraction from Reboot report. Pelvis ROM ~60° matches HitTrax validation (59.4 mph bat speed requires 35-40° minimum).'
)
ON CONFLICT (session_id) DO UPDATE SET
    pelvis_rotation_rom_deg = EXCLUDED.pelvis_rotation_rom_deg,
    torso_rotation_rom_deg = EXCLUDED.torso_rotation_rom_deg,
    updated_at = CURRENT_TIMESTAMP;
"""
