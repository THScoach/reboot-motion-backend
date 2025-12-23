#!/bin/bash

# Test script to check if Data Export endpoint is deployed

echo "🔍 Testing Reboot Motion Data Export Endpoint..."
echo ""

SESSION_ID="6764e74b-516d-45eb-a8a9-c50a069ef50d"
ENDPOINT="https://reboot-motion-backend-production.up.railway.app/reboot/data-export/$SESSION_ID"

echo "📡 Endpoint: $ENDPOINT"
echo ""

for i in {1..10}; do
    echo "Attempt $i/10..."
    
    RESPONSE=$(curl -s "$ENDPOINT")
    
    if echo "$RESPONSE" | grep -q '"session_id"'; then
        echo ""
        echo "✅ SUCCESS! Endpoint is live!"
        echo ""
        echo "Sample response:"
        echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"
        exit 0
    elif echo "$RESPONSE" | grep -q '"detail":"Not Found"'; then
        echo "   ❌ Still deploying... (404 Not Found)"
    else
        echo "   ⚠️  Unexpected response:"
        echo "$RESPONSE" | head -3
    fi
    
    if [ $i -lt 10 ]; then
        echo "   Waiting 30 seconds..."
        sleep 30
    fi
    echo ""
done

echo "❌ Deployment not complete after 5 minutes."
echo "Check Railway dashboard or try again later."
exit 1
