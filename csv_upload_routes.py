"""
Reboot Motion CSV Upload Endpoint
Allows users to upload momentum-energy or inverse-kinematics CSV files
as a fallback if the API is unavailable
"""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import tempfile
from pathlib import Path
from reboot_csv_importer import RebootCSVImporter, RebootSwingData
from inverse_kinematics_importer import InverseKinematicsImporter, RebootIKData
from typing import Optional, Any, Dict
import numpy as np

router = APIRouter()


def convert_to_native_types(obj: Any) -> Any:
    """
    Convert NumPy/Pandas types to native Python types for JSON serialization.
    
    Handles:
    - numpy.int64 → int
    - numpy.float64 → float
    - numpy.ndarray → list
    - dict → recursively convert values
    - None → None
    """
    if isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, dict):
        return {k: convert_to_native_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_native_types(item) for item in obj]
    else:
        return obj


@router.post("/upload-reboot-csv")
async def upload_reboot_csv(
    file: UploadFile = File(...),
    bat_mass_kg: Optional[float] = 0.85,
    athlete_name: Optional[str] = None
):
    """
    Upload and parse Reboot Motion CSV file
    
    Supports:
    - momentum-energy.csv files ✅
    - inverse-kinematics.csv files ✅
    
    Auto-detects file type from filename.
    
    Args:
        file: CSV file upload
        bat_mass_kg: Bat mass in kg (default 0.85 for 33"/30oz) - for momentum files
        athlete_name: Optional athlete name
    
    Returns:
        JSON with parsed data and calculated metrics
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Validate it's a Reboot Motion file
    if 'rebootmotion' not in file.filename.lower() and \
       'momentum' not in file.filename.lower() and \
       'kinematics' not in file.filename.lower():
        raise HTTPException(
            status_code=400, 
            detail="File must be a Reboot Motion export (filename should contain 'rebootmotion', 'momentum', or 'kinematics')"
        )
    
    try:
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        # Detect file type from filename
        filename_lower = file.filename.lower()
        
        if 'inverse-kinematics' in filename_lower or 'inverse_kinematics' in filename_lower:
            # Process as inverse-kinematics file
            return await process_ik_file(temp_path, athlete_name)
        else:
            # Process as momentum-energy file (default)
            return await process_momentum_file(temp_path, bat_mass_kg, athlete_name)
        
    except Exception as e:
        # Clean up temp file on error
        if 'temp_path' in locals():
            Path(temp_path).unlink(missing_ok=True)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing CSV: {str(e)}"
        )


async def process_momentum_file(temp_path: str, bat_mass_kg: float, athlete_name: Optional[str]) -> JSONResponse:
    """Process momentum-energy CSV file"""
    # Parse CSV
    importer = RebootCSVImporter()
    swing_data = importer.load_momentum_energy_csv(temp_path)
    
    # Add athlete name if provided
    if athlete_name:
        swing_data.athlete_name = athlete_name
    
    # Calculate ground truth metrics
    metrics = importer.calculate_ground_truth_metrics(swing_data, bat_mass_kg)
    
    # Clean up temp file
    Path(temp_path).unlink()
    
    # Prepare response (convert NumPy types to native Python types)
    response = {
        "success": True,
        "data_type": "momentum-energy",
        "message": "Momentum-energy CSV processed successfully",
        "session_info": {
            "session_id": swing_data.session_id,
            "athlete_name": swing_data.athlete_name,
            "movement_type": swing_data.movement_type,
            "fps": float(round(swing_data.fps, 1)),
            "duration_s": float(round(swing_data.duration_s, 2)),
            "num_frames": int(swing_data.num_frames),
            "contact_frame": int(swing_data.contact_frame),
            "contact_time_s": float(round(swing_data.contact_time_s, 3))
        },
        "ground_truth_metrics": {
            "bat_speed": {
                "at_contact_mph": float(round(metrics['bat_speed_mph'], 1)),
                "peak_mph": float(round(metrics['peak_bat_speed_mph'], 1))
            },
            "energy_distribution": {
                "total_j": float(round(metrics['total_energy_j'], 0)),
                "lowerhalf_pct": float(round(metrics['lowerhalf_pct'], 1)) if metrics['lowerhalf_pct'] else None,
                "torso_pct": float(round(metrics['torso_pct'], 1)) if metrics['torso_pct'] else None,
                "arms_pct": float(round(metrics['arms_pct'], 1)) if metrics['arms_pct'] else None
            },
            "kinematic_sequence_ms_before_contact": {
                k: float(round(v, 0)) for k, v in metrics['kinematic_sequence_ms_before_contact'].items()
            },
            "tempo_estimated": {
                "ratio": float(round(metrics['tempo_ratio_estimated'], 2)),
                "load_duration_ms": float(round(metrics['load_duration_ms_estimated'], 0)),
                "swing_duration_ms": float(round(metrics['swing_duration_ms_estimated'], 0))
            }
        }
    }
    
    # Convert any remaining NumPy types
    response = convert_to_native_types(response)
    
    return JSONResponse(content=response)


async def process_ik_file(temp_path: str, athlete_name: Optional[str]) -> JSONResponse:
    """Process inverse-kinematics CSV file"""
    # Parse CSV
    importer = InverseKinematicsImporter()
    ik_data = importer.load_ik_csv(temp_path)
    
    # Add athlete name if provided
    if athlete_name:
        ik_data.athlete_name = athlete_name
    
    # Calculate IK metrics
    metrics = importer.calculate_ik_metrics(ik_data)
    
    # Clean up temp file
    Path(temp_path).unlink()
    
    # Prepare response (convert NumPy types to native Python types)
    response = {
        "success": True,
        "data_type": "inverse-kinematics",
        "message": "Inverse-kinematics CSV processed successfully",
        "session_info": {
            "session_id": ik_data.session_id,
            "athlete_name": ik_data.athlete_name,
            "movement_type": ik_data.movement_type,
            "fps": float(round(ik_data.fps, 1)),
            "duration_s": float(round(ik_data.duration_s, 2)),
            "num_frames": int(ik_data.num_frames),
            "contact_frame": int(ik_data.contact_frame),
            "contact_time_s": float(round(ik_data.contact_time_s, 3))
        },
        "joint_data": {
            "num_joint_angles": int(len(ik_data.joint_angles)),
            "num_joint_positions": int(len(ik_data.joint_positions)),
            "has_angular_velocities": bool(ik_data.angular_velocities is not None),
            "has_segment_orientations": bool(ik_data.segment_orientations is not None)
        },
        "ik_metrics": metrics
    }
    
    # Convert any remaining NumPy types (especially in metrics dict)
    response = convert_to_native_types(response)
    
    return JSONResponse(content=response)


@router.get("/csv-upload-info")
async def csv_upload_info():
    """
    Get information about CSV upload feature
    """
    return {
        "feature": "Reboot Motion CSV Import",
        "description": "Upload momentum-energy or inverse-kinematics CSV files as fallback when API is unavailable",
        "supported_files": [
            {
                "type": "momentum-energy",
                "description": "Energy, momentum, kinetic data",
                "filename_pattern": "*momentum-energy.csv",
                "metrics": ["bat_speed", "energy_distribution", "kinematic_sequence", "tempo"]
            },
            {
                "type": "inverse-kinematics",
                "description": "Joint angles, positions, velocities",
                "filename_pattern": "*inverse-kinematics.csv",
                "metrics": ["joint_angles", "joint_positions", "range_of_motion", "hip_shoulder_separation", "bat_path"]
            }
        ],
        "endpoint": "/upload-reboot-csv",
        "method": "POST",
        "parameters": {
            "file": "CSV file (required)",
            "bat_mass_kg": "Bat mass in kg (optional, default 0.85, for momentum files)",
            "athlete_name": "Athlete name (optional)"
        },
        "auto_detection": "File type is automatically detected from filename",
        "returns": {
            "momentum-energy": {
                "session_info": "Session metadata",
                "ground_truth_metrics": {
                    "bat_speed": "Bat speed at contact and peak",
                    "energy_distribution": "Lower half, torso, arms percentages",
                    "kinematic_sequence": "Peak times before contact",
                    "tempo": "Estimated tempo ratio"
                }
            },
            "inverse-kinematics": {
                "session_info": "Session metadata",
                "joint_data": "Number of joints tracked",
                "ik_metrics": {
                    "range_of_motion": "Min, max, range for each joint",
                    "max_angular_velocities": "Peak velocities for each joint",
                    "hip_shoulder_separation": "Max and at-contact separation",
                    "bat_path_length": "Total bat path distance"
                }
            }
        },
        "example_usage": {
            "curl_momentum": "curl -X POST -F 'file=@momentum-energy.csv' -F 'bat_mass_kg=0.85' http://localhost:8000/upload-reboot-csv",
            "curl_ik": "curl -X POST -F 'file=@inverse-kinematics.csv' -F 'athlete_name=Connor Gray' http://localhost:8000/upload-reboot-csv"
        }
    }
