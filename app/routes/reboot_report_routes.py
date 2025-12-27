"""
API Routes for Reboot Motion Report Metrics
Handles report upload and manual metric input
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from typing import Optional

# This will be integrated into your main Flask app
reboot_reports_bp = Blueprint('reboot_reports', __name__)

# Configuration
UPLOAD_FOLDER = '/home/user/webapp/uploads/reports'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@reboot_reports_bp.route('/api/reboot/sessions/<session_id>/upload-report', methods=['POST'])
def upload_report(session_id):
    """
    Upload Reboot Motion report file (PNG/PDF)
    
    curl -X POST \\
      -F "report=@connor_reboot_report.png" \\
      http://localhost:5000/api/reboot/sessions/4f1a7010-1324-469d-8e1a-e05a1dc45f2e/upload-report
    """
    if 'report' not in request.files:
        return jsonify({'error': 'No report file provided'}), 400
    
    file = request.files['report']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Invalid file type. Allowed: PNG, JPG, PDF'}), 400
    
    # Secure filename and save
    filename = secure_filename(f"{session_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'report_file_path': filepath,
        'filename': filename,
        'message': 'Report uploaded successfully. Please enter metrics manually.'
    }), 200


@reboot_reports_bp.route('/api/reboot/sessions/<session_id>/report-metrics', methods=['GET'])
def get_report_metrics(session_id):
    """
    Get report metrics for a session
    
    Returns metrics extracted from Reboot report (manual or automated)
    """
    # TODO: Query database
    # For now, return structure
    return jsonify({
        'session_id': session_id,
        'metrics': {
            'pelvis_rotation_rom_deg': None,
            'torso_rotation_rom_deg': None,
            'x_factor_deg': None,
            'pelvis_peak_velocity_deg_per_s': None,
            'torso_peak_velocity_deg_per_s': None,
            'bat_speed_mph': None,
            'exit_velocity_mph': None
        },
        'validation': {
            'validated_against_hittrax': False,
            'hittrax_bat_speed_mph': None,
            'hittrax_exit_velocity_mph': None
        },
        'metadata': {
            'data_source': None,
            'report_file_path': None,
            'created_by': None,
            'updated_at': None
        }
    }), 200


@reboot_reports_bp.route('/api/reboot/sessions/<session_id>/report-metrics', methods=['POST'])
def save_report_metrics(session_id):
    """
    Save manually entered report metrics
    
    POST /api/reboot/sessions/4f1a7010.../report-metrics
    {
      "pelvis_rotation_rom_deg": 60.0,
      "torso_rotation_rom_deg": 25.0,
      "pelvis_peak_velocity_deg_per_s": 425,
      "torso_peak_velocity_deg_per_s": 738,
      "data_source": "manual_input",
      "created_by": "Coach Rick",
      "hittrax_bat_speed_mph": 59.4,
      "hittrax_exit_velocity_mph": 98.0,
      "notes": "Extracted from Torso Kinematics chart"
    }
    """
    data = request.json
    
    # Validate required fields
    if 'pelvis_rotation_rom_deg' not in data:
        return jsonify({'error': 'pelvis_rotation_rom_deg is required'}), 400
    
    # TODO: Insert into database
    # For now, return success
    
    metrics = {
        'session_id': session_id,
        'pelvis_rotation_rom_deg': data.get('pelvis_rotation_rom_deg'),
        'torso_rotation_rom_deg': data.get('torso_rotation_rom_deg'),
        'x_factor_deg': data.get('x_factor_deg'),
        'pelvis_peak_velocity_deg_per_s': data.get('pelvis_peak_velocity_deg_per_s'),
        'pelvis_peak_timing_pct': data.get('pelvis_peak_timing_pct'),
        'torso_peak_velocity_deg_per_s': data.get('torso_peak_velocity_deg_per_s'),
        'torso_peak_timing_pct': data.get('torso_peak_timing_pct'),
        'bat_speed_mph': data.get('bat_speed_mph'),
        'exit_velocity_mph': data.get('exit_velocity_mph'),
        'attack_angle_deg': data.get('attack_angle_deg'),
        'contact_frame': data.get('contact_frame'),
        'data_source': data.get('data_source', 'manual_input'),
        'created_by': data.get('created_by'),
        'validated_against_hittrax': data.get('validated_against_hittrax', False),
        'hittrax_bat_speed_mph': data.get('hittrax_bat_speed_mph'),
        'hittrax_exit_velocity_mph': data.get('hittrax_exit_velocity_mph'),
        'notes': data.get('notes')
    }
    
    return jsonify({
        'success': True,
        'session_id': session_id,
        'metrics': metrics,
        'message': 'Metrics saved successfully'
    }), 200


@reboot_reports_bp.route('/api/reboot/sessions/<session_id>/report-metrics/validate', methods=['POST'])
def validate_metrics_with_hittrax(session_id):
    """
    Validate report metrics against HitTrax data
    
    POST /api/reboot/sessions/{session_id}/report-metrics/validate
    {
      "exit_velocity_mph": 98.0,
      "pitch_speed_mph": 52.5,
      "bat_weight_oz": 29
    }
    
    Returns:
    - Calculated bat speed from exit velocity
    - Expected rotation ROM for that bat speed
    - Validation status (PASS/FAIL)
    """
    data = request.json
    
    exit_velocity = data.get('exit_velocity_mph')
    pitch_speed = data.get('pitch_speed_mph', 0)
    bat_weight_oz = data.get('bat_weight_oz', 30)
    
    if not exit_velocity:
        return jsonify({'error': 'exit_velocity_mph is required'}), 400
    
    # Calculate bat speed from exit velocity
    BALL_MASS_OZ = 5.125
    COR_WOOD = 0.50
    q = BALL_MASS_OZ / bat_weight_oz
    
    bat_speed = (exit_velocity * (1 + q) - pitch_speed * COR_WOOD) / (1 + COR_WOOD)
    
    # Estimate required rotation
    # Rule of thumb: 1 mph bat speed ≈ 0.7° pelvis rotation
    # 60 mph → ~35-45° pelvis rotation
    min_pelvis_rotation = bat_speed * 0.6
    max_pelvis_rotation = bat_speed * 0.8
    
    # TODO: Get actual metrics from database
    actual_pelvis_rotation = data.get('actual_pelvis_rotation_rom_deg', 0)
    
    validation_status = 'UNKNOWN'
    if actual_pelvis_rotation > 0:
        if min_pelvis_rotation <= actual_pelvis_rotation <= max_pelvis_rotation * 1.5:
            validation_status = 'PASS'
        elif actual_pelvis_rotation < min_pelvis_rotation * 0.5:
            validation_status = 'FAIL - Rotation too low'
        else:
            validation_status = 'PASS - Above expected'
    
    return jsonify({
        'session_id': session_id,
        'hittrax_data': {
            'exit_velocity_mph': exit_velocity,
            'pitch_speed_mph': pitch_speed,
            'bat_weight_oz': bat_weight_oz
        },
        'calculated': {
            'bat_speed_mph': round(bat_speed, 1),
            'expected_pelvis_rom_range': [round(min_pelvis_rotation, 1), round(max_pelvis_rotation, 1)]
        },
        'actual': {
            'pelvis_rotation_rom_deg': actual_pelvis_rotation
        },
        'validation': {
            'status': validation_status,
            'matches_physics': validation_status == 'PASS'
        }
    }), 200


# Export blueprint to be registered in main app
# app.register_blueprint(reboot_reports_bp)
