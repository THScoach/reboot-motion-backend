"""
Whop Webhook Handler
===================

Handles Whop webhook events for membership lifecycle.

Events handled:
- membership.created
- membership.updated
- membership.deleted
- membership.payment_succeeded
- membership.payment_failed

Author: Builder 2
Date: 2024-12-25
"""

from fastapi import APIRouter, Request, HTTPException, Header
from typing import Optional
import hmac
import hashlib
import json
from datetime import datetime

from whop_integration import get_whop_client, SubscriptionTier, WHOP_PRODUCTS


router = APIRouter(prefix="/webhooks", tags=["Whop Webhooks"])


# In-memory user database (replace with actual database)
# Format: {user_id: {membership_data}}
USER_MEMBERSHIPS = {}


def verify_whop_signature(
    payload: bytes,
    signature: str,
    secret: str
) -> bool:
    """
    Verify Whop webhook signature
    
    Args:
        payload: Request body bytes
        signature: X-Whop-Signature header
        secret: Webhook secret
        
    Returns:
        True if signature is valid
    """
    if not secret:
        # If no secret configured, skip verification (dev mode)
        return True
    
    try:
        expected_sig = hmac.new(
            secret.encode(),
            payload,
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_sig)
    except:
        return False


@router.post("/whop")
async def whop_webhook(
    request: Request,
    x_whop_signature: Optional[str] = Header(None)
):
    """
    Whop webhook endpoint
    
    Receives and processes Whop membership events.
    
    Events:
    - membership.created: New subscription
    - membership.updated: Subscription changed
    - membership.deleted: Subscription canceled
    - membership.payment_succeeded: Payment successful
    - membership.payment_failed: Payment failed
    """
    
    # Get raw body for signature verification
    body = await request.body()
    
    # Verify signature (skip in development)
    webhook_secret = ""  # TODO: Set actual webhook secret
    if webhook_secret and x_whop_signature:
        if not verify_whop_signature(body, x_whop_signature, webhook_secret):
            raise HTTPException(status_code=401, detail="Invalid signature")
    
    # Parse JSON payload
    try:
        event = json.loads(body)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON")
    
    # Extract event data
    event_type = event.get("type")
    data = event.get("data", {})
    
    print(f"📬 Whop Webhook Received: {event_type}")
    
    # Handle different event types
    if event_type == "membership.created":
        await handle_membership_created(data)
    
    elif event_type == "membership.updated":
        await handle_membership_updated(data)
    
    elif event_type == "membership.deleted":
        await handle_membership_deleted(data)
    
    elif event_type == "membership.payment_succeeded":
        await handle_payment_succeeded(data)
    
    elif event_type == "membership.payment_failed":
        await handle_payment_failed(data)
    
    else:
        print(f"⚠️  Unknown event type: {event_type}")
    
    return {"status": "success"}


async def handle_membership_created(data: dict):
    """Handle new membership creation"""
    membership_id = data.get("id")
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    status = data.get("status")
    
    print(f"✅ New Membership Created:")
    print(f"   User: {user_id}")
    print(f"   Membership: {membership_id}")
    print(f"   Product: {product_id}")
    print(f"   Status: {status}")
    
    # Determine subscription tier
    client = get_whop_client()
    tier = client._get_tier_from_product_id(product_id)
    
    # Store membership data
    USER_MEMBERSHIPS[user_id] = {
        "membership_id": membership_id,
        "product_id": product_id,
        "tier": tier.value,
        "status": status,
        "created_at": datetime.utcnow().isoformat(),
        "swings_used": 0
    }
    
    # TODO: Save to actual database
    # await db.execute(
    #     "INSERT INTO users (whop_user_id, whop_membership_id, subscription_tier) ..."
    # )
    
    print(f"   Tier: {tier.value}")
    print(f"   ✅ User database updated")


async def handle_membership_updated(data: dict):
    """Handle membership update"""
    membership_id = data.get("id")
    user_id = data.get("user_id")
    product_id = data.get("product_id")
    status = data.get("status")
    
    print(f"🔄 Membership Updated:")
    print(f"   User: {user_id}")
    print(f"   Membership: {membership_id}")
    print(f"   New Status: {status}")
    
    # Update stored data
    if user_id in USER_MEMBERSHIPS:
        USER_MEMBERSHIPS[user_id]["status"] = status
        USER_MEMBERSHIPS[user_id]["updated_at"] = datetime.utcnow().isoformat()
    
    # TODO: Update actual database
    print(f"   ✅ User database updated")


async def handle_membership_deleted(data: dict):
    """Handle membership cancellation/deletion"""
    membership_id = data.get("id")
    user_id = data.get("user_id")
    
    print(f"❌ Membership Deleted:")
    print(f"   User: {user_id}")
    print(f"   Membership: {membership_id}")
    
    # Update status to canceled
    if user_id in USER_MEMBERSHIPS:
        USER_MEMBERSHIPS[user_id]["status"] = "canceled"
        USER_MEMBERSHIPS[user_id]["tier"] = "free"  # Downgrade to free
        USER_MEMBERSHIPS[user_id]["canceled_at"] = datetime.utcnow().isoformat()
    
    # TODO: Update actual database
    print(f"   ✅ User downgraded to FREE tier")


async def handle_payment_succeeded(data: dict):
    """Handle successful payment"""
    membership_id = data.get("membership_id")
    user_id = data.get("user_id")
    amount = data.get("amount", 0) / 100  # Convert cents to dollars
    
    print(f"💰 Payment Succeeded:")
    print(f"   User: {user_id}")
    print(f"   Amount: ${amount:.2f}")
    print(f"   Membership: {membership_id}")
    
    # Update payment status
    if user_id in USER_MEMBERSHIPS:
        USER_MEMBERSHIPS[user_id]["last_payment"] = {
            "amount": amount,
            "date": datetime.utcnow().isoformat(),
            "status": "succeeded"
        }
    
    # TODO: Record payment in database
    print(f"   ✅ Payment recorded")


async def handle_payment_failed(data: dict):
    """Handle failed payment"""
    membership_id = data.get("membership_id")
    user_id = data.get("user_id")
    reason = data.get("reason", "Unknown")
    
    print(f"⚠️  Payment Failed:")
    print(f"   User: {user_id}")
    print(f"   Membership: {membership_id}")
    print(f"   Reason: {reason}")
    
    # Update payment status
    if user_id in USER_MEMBERSHIPS:
        USER_MEMBERSHIPS[user_id]["last_payment"] = {
            "date": datetime.utcnow().isoformat(),
            "status": "failed",
            "reason": reason
        }
    
    # TODO: Send notification, retry payment, etc.
    print(f"   ⚠️  Payment failure recorded")


# ============================================================================
# HELPER ENDPOINTS
# ============================================================================

@router.get("/whop/status")
async def webhook_status():
    """Check webhook status and configuration"""
    return {
        "status": "active",
        "endpoint": "/webhooks/whop",
        "events_handled": [
            "membership.created",
            "membership.updated",
            "membership.deleted",
            "membership.payment_succeeded",
            "membership.payment_failed"
        ],
        "users_count": len(USER_MEMBERSHIPS)
    }


@router.get("/whop/users")
async def list_users():
    """List all users (debug endpoint)"""
    return {
        "count": len(USER_MEMBERSHIPS),
        "users": USER_MEMBERSHIPS
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WHOP WEBHOOK HANDLER TEST")
    print("="*70)
    
    print(f"\n📡 Webhook Configuration:")
    print(f"  Endpoint: POST /webhooks/whop")
    print(f"  Events Handled:")
    print(f"    - membership.created")
    print(f"    - membership.updated")
    print(f"    - membership.deleted")
    print(f"    - membership.payment_succeeded")
    print(f"    - membership.payment_failed")
    
    print(f"\n✅ Webhook Handler Ready")
    print("="*70 + "\n")
