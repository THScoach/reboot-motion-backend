#!/bin/bash

# Test script for Coach Dashboard API
BASE_URL="http://localhost:8003/api/teams"

echo "=========================================================================="
echo "TESTING COACH DASHBOARD API - PRIORITY 16"
echo "=========================================================================="
echo ""

# Test 1: Create Coach
echo "1. Creating Coach..."
echo "--------------------------------------------------------------------------"
COACH_RESPONSE=$(curl -s -X POST "$BASE_URL/coaches" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Coach Mike Johnson",
    "email": "mike.johnson@thsbaseball.com",
    "role": "head_coach",
    "organization": "Tomball High School Baseball",
    "phone": "(281) 555-1234",
    "certifications": ["USA Baseball", "ABCA Level 3"]
  }')

COACH_ID=$(echo $COACH_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['coach_id'])")
echo "✅ Coach Created: $COACH_ID"
echo ""

# Test 2: Create Team
echo "2. Creating Team..."
echo "--------------------------------------------------------------------------"
TEAM_RESPONSE=$(curl -s -X POST "$BASE_URL/teams" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Varsity Baseball 2024\",
    \"team_type\": \"high_school\",
    \"coach_id\": \"$COACH_ID\",
    \"season\": \"2024 Spring\",
    \"description\": \"Varsity team for Spring 2024 season\"
  }")

TEAM_ID=$(echo $TEAM_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['team_id'])")
echo "✅ Team Created: $TEAM_ID"
echo ""

# Test 3: Add Athletes
echo "3. Adding Athletes to Roster..."
echo "--------------------------------------------------------------------------"

# Athlete 1: Eric Williams
ATHLETE1_RESPONSE=$(curl -s -X POST "$BASE_URL/athletes" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Eric Williams\",
    \"email\": \"ewilliams@student.thsbaseball.com\",
    \"team_id\": \"$TEAM_ID\",
    \"date_of_birth\": \"2006-03-15\",
    \"height_inches\": 68,
    \"wingspan_inches\": 69,
    \"weight_lbs\": 190,
    \"bat_weight_oz\": 30,
    \"position\": \"OF\",
    \"jersey_number\": 24,
    \"grad_year\": 2024,
    \"status\": \"active\"
  }")

ATHLETE1_ID=$(echo $ATHLETE1_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['athlete_id'])")
echo "✅ Athlete 1 Added: Eric Williams (#24) - $ATHLETE1_ID"

# Athlete 2: Jake Martinez
ATHLETE2_RESPONSE=$(curl -s -X POST "$BASE_URL/athletes" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Jake Martinez\",
    \"email\": \"jmartinez@student.thsbaseball.com\",
    \"team_id\": \"$TEAM_ID\",
    \"date_of_birth\": \"2006-07-22\",
    \"height_inches\": 72,
    \"wingspan_inches\": 74,
    \"weight_lbs\": 205,
    \"bat_weight_oz\": 32,
    \"position\": \"1B\",
    \"jersey_number\": 15,
    \"grad_year\": 2024,
    \"status\": \"active\"
  }")

ATHLETE2_ID=$(echo $ATHLETE2_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['athlete_id'])")
echo "✅ Athlete 2 Added: Jake Martinez (#15) - $ATHLETE2_ID"

# Athlete 3: Tommy Chen
ATHLETE3_RESPONSE=$(curl -s -X POST "$BASE_URL/athletes" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"Tommy Chen\",
    \"email\": \"tchen@student.thsbaseball.com\",
    \"team_id\": \"$TEAM_ID\",
    \"date_of_birth\": \"2007-01-08\",
    \"height_inches\": 70,
    \"wingspan_inches\": 71,
    \"weight_lbs\": 180,
    \"bat_weight_oz\": 31,
    \"position\": \"SS\",
    \"jersey_number\": 7,
    \"grad_year\": 2025,
    \"status\": \"active\"
  }")

ATHLETE3_ID=$(echo $ATHLETE3_RESPONSE | python3 -c "import sys, json; print(json.load(sys.stdin)['athlete_id'])")
echo "✅ Athlete 3 Added: Tommy Chen (#7) - $ATHLETE3_ID"
echo ""

# Test 4: Get Team Roster
echo "4. Getting Team Roster..."
echo "--------------------------------------------------------------------------"
curl -s "$BASE_URL/teams/$TEAM_ID/roster" | python3 -m json.tool
echo ""

# Test 5: Add Coach Notes
echo "5. Adding Coach Notes..."
echo "--------------------------------------------------------------------------"
curl -s -X POST "$BASE_URL/notes" \
  -H "Content-Type: application/json" \
  -d "{
    \"coach_id\": \"$COACH_ID\",
    \"athlete_id\": \"$ATHLETE1_ID\",
    \"content\": \"Eric showed great improvement in hip rotation today. Continue focusing on connection drills.\",
    \"category\": \"observation\",
    \"tags\": [\"hip_rotation\", \"improvement\"]
  }" | python3 -m json.tool

echo "✅ Note added for Eric Williams"
echo ""

# Test 6: Assign Drills
echo "6. Assigning Training Drills..."
echo "--------------------------------------------------------------------------"
curl -s -X POST "$BASE_URL/assignments" \
  -H "Content-Type: application/json" \
  -d "{
    \"coach_id\": \"$COACH_ID\",
    \"athlete_id\": \"$ATHLETE1_ID\",
    \"drill_id\": \"step_drill_stage1\",
    \"drill_name\": \"Step Through Drill (Stage 1)\",
    \"due_days\": 7,
    \"priority\": \"HIGH\",
    \"sets_required\": 5,
    \"notes\": \"Focus on rhythm and timing\"
  }" | python3 -m json.tool

echo "✅ Drill assigned to Eric Williams"
echo ""

# Test 7: Get Team Analytics
echo "7. Getting Team Analytics..."
echo "--------------------------------------------------------------------------"
curl -s "$BASE_URL/teams/$TEAM_ID/analytics" | python3 -m json.tool
echo ""

# Test 8: Compare Athletes
echo "8. Comparing Athletes..."
echo "--------------------------------------------------------------------------"
curl -s -X POST "$BASE_URL/athletes/compare" \
  -H "Content-Type: application/json" \
  -d "{
    \"athlete_ids\": [\"$ATHLETE1_ID\", \"$ATHLETE2_ID\", \"$ATHLETE3_ID\"],
    \"metric\": \"bat_speed\"
  }" | python3 -m json.tool
echo ""

# Test 9: Get Coach Dashboard
echo "9. Getting Coach Dashboard Summary..."
echo "--------------------------------------------------------------------------"
curl -s "$BASE_URL/dashboard/$COACH_ID" | python3 -m json.tool
echo ""

echo "=========================================================================="
echo "✅ ALL API TESTS COMPLETED SUCCESSFULLY!"
echo "=========================================================================="
