"""
Athlete Profile Configuration
Used for testing the Kinetic DNA Blueprint physics engine
"""

# Test Athlete 1: Conor Gray (High School)
CONOR_GRAY = {
    "name": "Conor Gray",
    "height_inches": 72,  # 6'0"
    "weight_lbs": 160,
    "wingspan_inches": 76,
    "bat_side": "left",
    "age": 16,  # Estimated high school age
    "level": "High School",
    
    # Videos (30 FPS)
    "videos": [
        "/home/user/uploaded_files/131215-Hitting.mov",
        "/home/user/uploaded_files/131151-Hitting.mov",
        "/home/user/uploaded_files/131233-Hitting.mov",
        "/home/user/uploaded_files/131200-Hitting.mov",
        "/home/user/uploaded_files/131301-Hitting.mov"
    ]
}

# Test Athlete 2: Shohei Ohtani (MLB)
SHOHEI_OHTANI = {
    "name": "Shohei Ohtani",
    "height_inches": 76,  # 6'4"
    "weight_lbs": 210,
    "wingspan_inches": 79,  # Estimated (typically height + 3-4" for elite athletes)
    "bat_side": "left",
    "age": 29,
    "level": "MLB",
    
    # Videos (300 FPS)
    "videos": [
        "/home/user/uploaded_files/340109 (1).mp4",
        "/home/user/uploaded_files/340109 (2).mp4",
        "/home/user/uploaded_files/340109 (3).mp4"
    ]
}

# All test videos
ALL_TEST_VIDEOS = CONOR_GRAY["videos"] + SHOHEI_OHTANI["videos"]
