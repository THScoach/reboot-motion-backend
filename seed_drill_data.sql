-- ============================================================================
-- SEED DATA: ALL 10 CATCHING BARRELS DRILLS
-- ============================================================================

-- ===========================================
-- DRILL #1: ROPE RHYTHM CONTROL
-- ===========================================
INSERT INTO drills (drill_number, drill_name, tool_required, dr_kwon_issue, krs_primary_target, krs_secondary_target, motor_profile_fit, description, purpose, video_url, thumbnail_url)
VALUES (
    1,
    'Rope Rhythm Control',
    'Quan Ropes',
    '#1 Timing & Rhythm',
    'Brain',
    NULL,
    '["Spinner", "Slingshotter", "Stacker", "Titan"]',
    'Teach proper load → fire sequencing without bat weight interference. Uses Quan Ropes to develop rhythm, timing, and hand speed while eliminating early hip rotation.',
    'CNS Activation, Rhythm Development, Sequencing Training',
    '/static/videos/drills/drill_01_rope_rhythm.mp4',
    '/static/images/drills/drill_01_thumb.jpg'
);

INSERT INTO drill_setup (drill_id, anchor_point, handle_position, body_position, resistance_angle, resistance_level)
VALUES (1, 'N/A (handheld tool)', 'Hitting grip on rope handles', 'Athletic stance, soft knees, weight centered', 'N/A', 'N/A (bodyweight)');

INSERT INTO drill_progression (drill_id, stage_number, stage_name, description, sets, reps, tempo)
VALUES 
    (1, 1, 'Slow Rhythm', 'Slow controlled swings (5-second cycle): Load 2 counts, Pause 1 count, Fire 1 count', 2, 10, 'Slow'),
    (1, 2, 'Game Tempo', 'Game-speed swings (2-second cycle): Load, Fire, Follow-through', 3, 15, 'Normal'),
    (1, 3, 'Pause Holds', 'Add 3-second pause at load position to feel coil', 3, 12, 'Controlled'),
    (1, 4, 'Max Speed', 'Maximum speed while maintaining proper sequence', 3, 20, 'Fast');

INSERT INTO drill_cues (drill_id, cue_text, cue_order)
VALUES 
    (1, '2... 2... BANG!', 1),
    (1, 'Hips wait for hands', 2),
    (1, 'Feel the stretch before you swing', 3),
    (1, 'Don''t let your lower half outrun your upper half', 4);

-- ===========================================
-- DRILL #2: SYNAPSE STRIDE DELAY
-- ===========================================
INSERT INTO drills (drill_number, drill_name, tool_required, dr_kwon_issue, krs_primary_target, krs_secondary_target, motor_profile_fit, description, purpose, video_url, thumbnail_url)
VALUES (
    2,
    'Synapse Stride Delay',
    'Synapse CCR',
    '#1 Timing & Rhythm',
    'Brain',
    'Body',
    '["Spinner", "Slingshotter"]',
    'Force proper timing by resisting premature hip rotation. Synapse pulls hips backward, preventing early firing while teaching proper load retention and hip-shoulder separation.',
    'Control Early Hip Rotation, Improve Sequencing, Build Separation',
    '/static/videos/drills/drill_02_synapse_stride.mp4',
    '/static/images/drills/drill_02_thumb.jpg'
);

INSERT INTO drill_setup (drill_id, anchor_point, handle_position, body_position, resistance_angle, resistance_level)
VALUES (2, 'Low floor anchor directly behind back hip', 'Strap around back hip/belt area', 'Athletic stance, hands loaded', 'Pulling hips backward (preventing early rotation)', 'Medium (8 clean reps)');

INSERT INTO drill_progression (drill_id, stage_number, stage_name, description, sets, reps, tempo)
VALUES 
    (2, 1, 'Pause Drill', '3-second holds at stride position before firing', 3, 6, 'Controlled'),
    (2, 2, 'Normal Tempo', 'Game-speed stride with resistance', 3, 8, 'Normal'),
    (2, 3, 'Eccentric Overload', 'Increase Synapse tension (heavy load)', 4, 6, 'Controlled'),
    (2, 4, 'Game Speed', 'Full-speed swings with light resistance', 3, 10, 'Fast');

INSERT INTO drill_cues (drill_id, cue_text, cue_order)
VALUES 
    (2, 'Feel Synapse trying to hold you back', 1),
    (2, 'Stride... WAIT... NOW!', 2),
    (2, 'Hips don''t go until hands are ready', 3),
    (2, 'Fight through the resistance together', 4);

-- ===========================================
-- DRILL #3: STACK BAT REACTION FIRE
-- ===========================================
INSERT INTO drills (drill_number, drill_name, tool_required, dr_kwon_issue, krs_primary_target, krs_secondary_target, motor_profile_fit, description, purpose, video_url, thumbnail_url)
VALUES (
    3,
    'Stack Bat Reaction Fire',
    'Stack Bat',
    '#1 Timing & Rhythm',
    'Brain',
    'Ball',
    '["Spinner", "Slingshotter", "Stacker", "Titan"]',
    'Train reactive timing and decision-making under speed stress. Coach drops colored balls; hitter must identify color and swing through. Improves pitch recognition and reaction time.',
    'Reactive Timing, Decision-Making, Pitch Recognition',
    '/static/videos/drills/drill_03_stack_reaction.mp4',
    '/static/images/drills/drill_03_thumb.jpg'
);

INSERT INTO drill_setup (drill_id, anchor_point, handle_position, body_position, resistance_angle, resistance_level)
VALUES (3, 'N/A (reaction drill)', 'Hitting grip on lightest Stack Bat or PVC', 'Ready position, partner 10-15 feet away', 'N/A', 'Light bat (overspeed)');

INSERT INTO drill_progression (drill_id, stage_number, stage_name, description, sets, reps, tempo)
VALUES 
    (3, 1, 'Single Ball', 'Coach drops one ball, hitter swings (no color call)', 2, 10, 'Reactive'),
    (3, 2, 'Two-Ball Color Call', 'Coach holds 2 colors, hitter calls color mid-swing', 3, 15, 'Reactive'),
    (3, 3, 'Fake & Delay', 'Coach fakes drops, delays timing', 3, 15, 'Reactive'),
    (3, 4, 'Trajectory Simulation', 'Coach varies drop angles (high/low/away)', 3, 20, 'Game Speed');

INSERT INTO drill_cues (drill_id, cue_text, cue_order)
VALUES 
    (3, 'See it, say it, swing it', 1),
    (3, 'Don''t wait - react and fire', 2),
    (3, 'Eyes stay on the drop point', 3),
    (3, 'Fast hands, calm eyes', 4);


-- ===========================================
-- DRILL #4: SYNAPSE HIP LOAD & FIRE
-- ===========================================
INSERT INTO drills (drill_number, drill_name, tool_required, dr_kwon_issue, krs_primary_target, krs_secondary_target, motor_profile_fit, description, purpose, video_url, thumbnail_url)
VALUES (
    4,
    'Synapse Hip Load & Fire',
    'Synapse CCR',
    '#7 Force Generation',
    'Body',
    NULL,
    '["Spinner", "Slingshotter", "Stacker", "Titan"]',
    'Build explosive hip rotation strength and ground force production. Synapse creates eccentric overload on load phase and resistance on rotation, forcing maximum hip drive.',
    'Hip Rotation Strength, Ground Force, Rotational Power',
    '/static/videos/drills/drill_04_synapse_hip.mp4',
    '/static/images/drills/drill_04_thumb.jpg'
);

INSERT INTO drill_setup (drill_id, anchor_point, handle_position, body_position, resistance_angle, resistance_level)
VALUES (4, 'Floor anchor at 45° to back hip', 'Both handles at chest height (like holding bat)', 'Athletic stance, knees bent, sideways to anchor', 'Pulling hips INTO rotation (eccentric on load, resistance on fire)', 'Heavy (6-8 rep max)');

INSERT INTO drill_progression (drill_id, stage_number, stage_name, description, sets, reps, tempo)
VALUES 
    (4, 1, 'Bodyweight Tempo', 'No Synapse, focus on pattern', 2, 10, 'Controlled'),
    (4, 2, 'Medium Resistance', 'Add Synapse at medium tension', 3, 8, 'Normal'),
    (4, 3, 'Eccentric Overload', 'Heavy load with 3-second eccentric load phase', 4, 6, 'Slow Eccentric'),
    (4, 4, 'Explosive Concentric', 'Focus on explosive rotation (fast concentric)', 3, 8, 'Fast');

INSERT INTO drill_cues (drill_id, cue_text, cue_order)
VALUES 
    (4, 'Load against the pull', 1),
    (4, 'Explode from your back foot', 2),
    (4, 'Drive through the resistance', 3),
    (4, 'Feel your hips do the work, not your arms', 4);

-- ===========================================
-- DRILL #5: SYNAPSE BACK LEG DRIVE
-- ===========================================
INSERT INTO drills (drill_number, drill_name, tool_required, dr_kwon_issue, krs_primary_target, krs_secondary_target, motor_profile_fit, description, purpose, video_url, thumbnail_url)
VALUES (
    5,
    'Synapse Back Leg Drive',
    'Synapse CCR',
    '#7 Force Generation, #4 Kinetic Chain',
    'Body',
    NULL,
    '["Slingshotter", "Stacker"]',
    'Isolate and strengthen back leg drive and hip extension power. Synapse resists forward knee drive, forcing maximum ground force production from back leg.',
    'Back Leg Power, Hip Extension, Ground Force Production',
    '/static/videos/drills/drill_05_synapse_backleg.mp4',
    '/static/images/drills/drill_05_thumb.jpg'
);

INSERT INTO drill_setup (drill_id, anchor_point, handle_position, body_position, resistance_angle, resistance_level)
VALUES (5, 'Low floor anchor behind hitter', 'Strap around back knee/lower thigh', 'Split stance (stride position), front foot planted', 'Pulling back leg backward (preventing forward drive)', 'Medium-Heavy');

INSERT INTO drill_progression (drill_id, stage_number, stage_name, description, sets, reps, tempo)
VALUES 
    (5, 1, 'Slow Controlled', 'Focus on pattern, slow drives', 3, 8, 'Slow'),
    (5, 2, 'Explosive Pop', 'Add explosive knee drive', 4, 6, 'Fast'),
    (5, 3, 'Heavy Resistance', 'Increase Synapse tension (eccentric overload)', 4, 6, 'Controlled'),
    (5, 4, 'Full Swing Integration', 'Add bat, combine with full swing', 3, 10, 'Game Speed');

INSERT INTO drill_cues (drill_id, cue_text, cue_order)
VALUES 
    (5, 'Drive your knee to your front leg', 1),
    (5, 'Back foot pushes, don''t pull with front side', 2),
    (5, 'Feel the ground under your back foot', 3),
    (5, 'Knee leads, hips follow', 4);

