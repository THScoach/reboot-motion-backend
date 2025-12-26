"""
Add Data Export endpoint to backend API
"""

# Add this to main.py

@app.get("/reboot/data-export/{session_id}")
def get_reboot_data_export(
    session_id: str,
    movement_type: str = Query("baseball-hitting", description="Movement type")
):
    """
    Fetch biomechanics data from Reboot Motion Data Export API
    
    Args:
        session_id: Reboot Motion session UUID
        movement_type: Type of movement (default: "baseball-hitting")
    
    Returns:
        Raw biomechanics data from Reboot Motion
    """
    try:
        sync = RebootMotionSync()
        token = sync._get_access_token()
        
        import requests
        
        endpoint = "https://api.rebootmotion.com/data_export"
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        params = {
            'session_id': session_id,
            'movement_type': movement_type
        }
        
        response = requests.get(endpoint, headers=headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Reboot Motion API error: {response.text}"
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
