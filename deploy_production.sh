#!/bin/bash
# CATCHING BARRELS - Production Deployment Script
# Date: 2025-12-25
# Purpose: Deploy Coach Rick AI + Whop Integration to production

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║         CATCHING BARRELS - PRODUCTION DEPLOYMENT                      ║"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo ""

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="${DOMAIN:-api.catchingbarrels.com}"
PORT="${PORT:-8006}"
WEBHOOK_URL="https://${DOMAIN}/webhooks/whop"

echo "📋 DEPLOYMENT CONFIGURATION"
echo "================================"
echo "Domain: ${DOMAIN}"
echo "Port: ${PORT}"
echo "Webhook URL: ${WEBHOOK_URL}"
echo ""

# Step 1: Environment validation
echo "🔍 Step 1: Validating environment..."
echo "------------------------------------"

if [ -z "$WHOP_API_KEY" ]; then
    echo -e "${RED}❌ WHOP_API_KEY not set${NC}"
    echo "   Please set: export WHOP_API_KEY='your_key_here'"
    exit 1
fi

if [ -z "$DATABASE_URL" ]; then
    echo -e "${YELLOW}⚠️  DATABASE_URL not set (will use in-memory storage)${NC}"
else
    echo -e "${GREEN}✓ DATABASE_URL configured${NC}"
fi

echo -e "${GREEN}✓ WHOP_API_KEY configured${NC}"
echo ""

# Step 2: Check product IDs
echo "🏷️  Step 2: Checking Whop product IDs..."
echo "------------------------------------"

PRODUCTS_CONFIGURED=$(grep -c "prod_\[" whop_integration.py || echo "0")

if [ "$PRODUCTS_CONFIGURED" -gt "0" ]; then
    echo -e "${YELLOW}⚠️  Found $PRODUCTS_CONFIGURED placeholder product IDs${NC}"
    echo "   Update these in whop_integration.py:"
    grep "prod_\[" whop_integration.py | head -3
    echo ""
    echo "   Run: ./update_product_ids.sh PRO PREMIUM ULTIMATE"
    echo ""
    read -p "   Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ All product IDs configured${NC}"
fi
echo ""

# Step 3: Install dependencies
echo "📦 Step 3: Installing dependencies..."
echo "------------------------------------"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${YELLOW}⚠️  requirements.txt not found${NC}"
fi
echo ""

# Step 4: Run tests
echo "🧪 Step 4: Running pre-deployment tests..."
echo "------------------------------------"

python3 -c "
import sys
sys.path.insert(0, '.')

# Test 1: Import Whop modules
try:
    from whop_integration import WhopClient, WHOP_PRODUCTS
    print('✓ Whop integration module')
except Exception as e:
    print(f'❌ Whop integration: {e}')
    sys.exit(1)

# Test 2: Import Swing DNA modules
try:
    from swing_dna.csv_parser import parse_momentum_energy, parse_inverse_kinematics
    from swing_dna.pattern_recognition import diagnose_swing_pattern
    print('✓ Swing DNA modules')
except Exception as e:
    print(f'⚠️  Swing DNA: {e} (optional)')

# Test 3: Check API configuration
try:
    client = WhopClient()
    print(f'✓ Whop client (API: {client.base_url})')
except Exception as e:
    print(f'❌ Whop client: {e}')
    sys.exit(1)

print('')
print('✓ All critical tests passed')
"

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Pre-deployment tests failed${NC}"
    exit 1
fi
echo ""

# Step 5: Start production server
echo "🚀 Step 5: Starting production server..."
echo "------------------------------------"

# Kill existing process on port
lsof -ti:${PORT} | xargs kill -9 2>/dev/null || true

# Start server in background
nohup python3 coach_rick_wap_integration.py > logs/production.log 2>&1 &
SERVER_PID=$!

echo "Server PID: $SERVER_PID"
echo "Waiting for server to start..."
sleep 5

# Health check
HEALTH_CHECK=$(curl -s "http://localhost:${PORT}/health" || echo "FAILED")

if echo "$HEALTH_CHECK" | grep -q "healthy"; then
    echo -e "${GREEN}✓ Server is healthy${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
    cat logs/production.log | tail -20
    exit 1
fi
echo ""

# Step 6: Verify endpoints
echo "✅ Step 6: Verifying endpoints..."
echo "------------------------------------"

ENDPOINTS=(
    "/health"
    "/docs"
    "/webhooks/whop/status"
    "/api/subscription/status"
)

for endpoint in "${ENDPOINTS[@]}"; do
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://localhost:${PORT}${endpoint}")
    if [ "$STATUS" = "200" ]; then
        echo -e "${GREEN}✓${NC} ${endpoint} (HTTP ${STATUS})"
    else
        echo -e "${YELLOW}⚠️${NC}  ${endpoint} (HTTP ${STATUS})"
    fi
done
echo ""

# Step 7: Display configuration info
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo "║                    DEPLOYMENT SUCCESSFUL                              ║"
echo "╔══════════════════════════════════════════════════════════════════════╗"
echo ""
echo "🌐 PUBLIC URLs (configure DNS to point to this server):"
echo "   API Docs:    https://${DOMAIN}/docs"
echo "   Health:      https://${DOMAIN}/health"
echo "   Webhook:     https://${DOMAIN}/webhooks/whop"
echo ""
echo "📊 LOCAL URLs (for testing):"
echo "   http://localhost:${PORT}/docs"
echo "   http://localhost:${PORT}/coach-rick-ui"
echo ""
echo "🔧 NEXT STEPS:"
echo ""
echo "1. Configure Whop Webhook:"
echo "   → Go to: https://whop.com/biz/developer"
echo "   → Add webhook: ${WEBHOOK_URL}"
echo "   → Subscribe to events:"
echo "     • membership.created"
echo "     • membership.updated"
echo "     • membership.deleted"
echo "     • membership.payment_succeeded"
echo "     • membership.payment_failed"
echo ""
echo "2. Update Product IDs (if not done):"
echo "   → Run: ./update_product_ids.sh PRO PREMIUM ULTIMATE"
echo ""
echo "3. Test end-to-end flow:"
echo "   → Create test membership in Whop"
echo "   → Check webhook received: curl http://localhost:${PORT}/webhooks/whop/status"
echo "   → Test subscription: curl -H 'X-User-Id: test' http://localhost:${PORT}/api/subscription/status"
echo ""
echo "4. Monitor logs:"
echo "   → tail -f logs/production.log"
echo ""
echo "📝 Server Process: PID ${SERVER_PID}"
echo "🛑 To stop: kill ${SERVER_PID}"
echo ""
echo "════════════════════════════════════════════════════════════════════════"
