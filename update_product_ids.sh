#!/bin/bash
# Update Whop Product IDs in whop_integration.py
# Usage: ./update_product_ids.sh <PRO_ID> <PREMIUM_ID> <ULTIMATE_ID>

set -e

if [ $# -ne 3 ]; then
    echo "Usage: $0 <PRO_ID> <PREMIUM_ID> <ULTIMATE_ID>"
    echo ""
    echo "Example:"
    echo "  $0 prod_ABC123 prod_DEF456 prod_GHI789"
    echo ""
    echo "Current placeholder IDs in whop_integration.py:"
    grep "prod_\[" whop_integration.py || echo "  (none found)"
    exit 1
fi

PRO_ID=$1
PREMIUM_ID=$2
ULTIMATE_ID=$3

echo "🔄 Updating Whop Product IDs..."
echo "================================"
echo "Pro:      $PRO_ID"
echo "Premium:  $PREMIUM_ID"
echo "Ultimate: $ULTIMATE_ID"
echo ""

# Backup original file
cp whop_integration.py whop_integration.py.backup
echo "✓ Backup created: whop_integration.py.backup"

# Update product IDs using sed
sed -i "s/prod_\[PENDING\]/$PRO_ID/g" whop_integration.py
sed -i "s/prod_\[CURRENT PRODUCT - UPDATE ID\]/$PREMIUM_ID/1" whop_integration.py
sed -i "s/prod_\[CURRENT PRODUCT - UPDATE ID\]/$ULTIMATE_ID/1" whop_integration.py

echo "✓ Product IDs updated in whop_integration.py"
echo ""

# Verify changes
echo "📋 Verification:"
echo "----------------"
grep "product_id.*prod_" whop_integration.py | grep -E "(Pro|Premium|Ultimate)" || echo "Could not verify (check manually)"
echo ""

echo "✅ DONE!"
echo ""
echo "Next steps:"
echo "  1. Review changes: diff whop_integration.py.backup whop_integration.py"
echo "  2. Test import: python3 -c 'from whop_integration import WHOP_PRODUCTS; print(WHOP_PRODUCTS)'"
echo "  3. Commit changes: git add whop_integration.py && git commit -m 'chore: Update Whop product IDs'"
echo "  4. Deploy: ./deploy_production.sh"
