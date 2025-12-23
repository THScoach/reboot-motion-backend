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
from typing import Optional

router = APIRouter()


@router.post("/upload-reboot-csv")
async def upload_reboot_csv(
    file: UploadFile = File(...),
    bat_mass_kg: Optional[float] = 0.85,
    athlete_name: Optional[str] = None
):
    """
    Upload and parse Reboot Motion CSV file
    
    Supports:
    - momentum-energy.csv files
    - inverse-kinematics.csv files (future)
    
    Args:
        file: CSV file upload
        bat_mass_kg: Bat mass in kg (default 0.85 for 33"/30oz)
        athlete_name: Optional athlete name
    
    Returns:
        JSON with parsed data and ground truth metrics
    """
    # Validate file type
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    # Validate it's a Reboot Motion file
    if 'rebootmotion' not in file.filename.lower() and 'momentum' not in file.filename.lower():
        raise HTTPException(
            status_code=400, 
            detail="File must be a Reboot Motion export (filename should contain 'rebootmotion' or 'momentum')"
        )
    
    try:
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.csv') as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
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
        
        # Prepare response
        response = {
            "success": True,
            "message": "CSV file processed successfully",
            "session_info": {
                "session_id": swing_data.session_id,
                "athlete_name": swing_data.athlete_name,
                "movement_type": swing_data.movement_type,
                "fps": round(swing_data.fps, 1),
                "duration_s": round(swing_data.duration_s, 2),
                "num_frames": swing_data.num_frames,
                "contact_frame": swing_data.contact_frame,
                "contact_time_s": round(swing_data.contact_time_s, 3)
            },
            "ground_truth_metrics": {
                "bat_speed": {
                    "at_contact_mph": round(metrics['bat_speed_mph'], 1),
                    "peak_mph": round(metrics['peak_bat_speed_mph'], 1)
                },
                "energy_distribution": {
                    "total_j": round(metrics['total_energy_j'], 0),
                    "lowerhalf_pct": round(metrics['lowerhalf_pct'], 1) if metrics['lowerhalf_pct'] else None,
                    "torso_pct": round(metrics['torso_pct'], 1) if metrics['torso_pct'] else None,
                    "arms_pct": round(metrics['arms_pct'], 1) if metrics['arms_pct'] else None
                },
                "kinematic_sequence_ms_before_contact": {
                    k: round(v, 0) for k, v in metrics['kinematic_sequence_ms_before_contact'].items()
                },
                "tempo_estimated": {
                    "ratio": round(metrics['tempo_ratio_estimated'], 2),
                    "load_duration_ms": round(metrics['load_duration_ms_estimated'], 0),
                    "swing_duration_ms": round(metrics['swing_duration_ms_estimated'], 0)
                }
            }
        }
        
        return JSONResponse(content=response)
        
    except Exception as e:
        # Clean up temp file on error
        if 'temp_path' in locals():
            Path(temp_path).unlink(missing_ok=True)
        
        raise HTTPException(
            status_code=500,
            detail=f"Error processing CSV: {str(e)}"
        )


@router.get("/csv-upload-info")
async def csv_upload_info():
    """
    Get information about CSV upload feature
    """
    return {
        "feature": "Reboot Motion CSV Import",
        "description": "Upload momentum-energy or inverse-kinematics CSV files as fallback when API is unavailable",
        "supported_files": [
            "momentum-energy.csv - Energy, momentum, kinetic data",
            "inverse-kinematics.csv - Joint angles, positions (future support)"
        ],
        "endpoint": "/upload-reboot-csv",
        "method": "POST",
        "parameters": {
            "file": "CSV file (required)",
            "bat_mass_kg": "Bat mass in kg (optional, default 0.85)",
            "athlete_name": "Athlete name (optional)"
        },
        "returns": {
            "session_info": "Session metadata from filename",
            "ground_truth_metrics": {
                "bat_speed": "Bat speed at contact and peak",
                "energy_distribution": "Lower half, torso, arms percentages",
                "kinematic_sequence": "Peak times before contact",
                "tempo": "Estimated tempo ratio"
            }
        },
        "example_usage": {
            "curl": "curl -X POST -F 'file=@momentum-energy.csv' -F 'bat_mass_kg=0.85' -F 'athlete_name=Connor Gray' http://localhost:8000/upload-reboot-csv"
        }
    }
