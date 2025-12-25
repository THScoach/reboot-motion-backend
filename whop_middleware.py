"""
Whop Feature Gate Middleware
============================

Middleware for protecting API endpoints based on subscription tier.

Usage:
    @app.post("/api/endpoint")
    @require_feature("ai_coach")
    async def my_endpoint(user: User = Depends(get_current_user)):
        ...

Author: Builder 2
Date: 2024-12-25
"""

from fastapi import HTTPException, Depends, Header
from typing import Optional, Callable
from functools import wraps

from whop_integration import (
    get_whop_client, 
    SubscriptionTier, 
    WHOP_PRODUCTS,
    WhopMembership
)


# ============================================================================
# USER DEPENDENCY
# ============================================================================

async def get_current_user(
    x_user_id: Optional[str] = Header(None),
    x_membership_id: Optional[str] = Header(None)
) -> dict:
    """
    Get current user from headers
    
    In production, this would validate JWT tokens or session cookies.
    For now, we use simple headers for testing.
    
    Headers:
        X-User-Id: Whop user ID
        X-Membership-Id: Whop membership ID
    
    Returns:
        User dict with tier and membership data
    """
    
    if not x_user_id:
        # No authentication - default to FREE tier
        return {
            "user_id": "anonymous",
            "tier": SubscriptionTier.FREE,
            "membership": None
        }
    
    # Validate membership if provided
    if x_membership_id:
        client = get_whop_client()
        membership = client.validate_membership(x_membership_id)
        
        if membership and membership.valid:
            return {
                "user_id": x_user_id,
                "tier": membership.tier,
                "membership": membership
            }
    
    # User ID provided but no valid membership - FREE tier
    return {
        "user_id": x_user_id,
        "tier": SubscriptionTier.FREE,
        "membership": None
    }


# ============================================================================
# FEATURE GATE DECORATORS
# ============================================================================

def require_feature(feature: str):
    """
    Decorator to require a specific feature for an endpoint
    
    Args:
        feature: Feature name (e.g., "ai_coach", "drill_library")
    
    Raises:
        HTTPException 403 if user doesn't have access
    
    Usage:
        @router.post("/analyze")
        @require_feature("ai_coach")
        async def analyze(user = Depends(get_current_user)):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, user: dict = Depends(get_current_user), **kwargs):
            # Check feature access
            client = get_whop_client()
            tier = user.get("tier", SubscriptionTier.FREE)
            
            if not client.check_feature_access(tier, feature):
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "feature_not_available",
                        "message": f"Your {tier.value} plan doesn't include '{feature}'",
                        "feature": feature,
                        "current_tier": tier.value,
                        "upgrade_tiers": _get_tiers_with_feature(feature)
                    }
                )
            
            # User has access - proceed
            return await func(*args, user=user, **kwargs)
        
        return wrapper
    return decorator


def require_tier(min_tier: SubscriptionTier):
    """
    Decorator to require a minimum subscription tier
    
    Args:
        min_tier: Minimum tier required
    
    Raises:
        HTTPException 403 if user's tier is below minimum
    """
    # Tier hierarchy
    tier_levels = {
        SubscriptionTier.FREE: 0,
        SubscriptionTier.PRO: 1,
        SubscriptionTier.PREMIUM: 2,
        SubscriptionTier.ULTIMATE: 3
    }
    
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, user: dict = Depends(get_current_user), **kwargs):
            user_tier = user.get("tier", SubscriptionTier.FREE)
            
            if tier_levels.get(user_tier, 0) < tier_levels.get(min_tier, 0):
                raise HTTPException(
                    status_code=403,
                    detail={
                        "error": "insufficient_tier",
                        "message": f"This feature requires {min_tier.value} or higher",
                        "current_tier": user_tier.value,
                        "required_tier": min_tier.value
                    }
                )
            
            return await func(*args, user=user, **kwargs)
        
        return wrapper
    return decorator


def check_swing_limit(func: Callable):
    """
    Decorator to check if user has remaining swings
    
    Raises:
        HTTPException 429 if swing limit exceeded
    """
    @wraps(func)
    async def wrapper(*args, user: dict = Depends(get_current_user), **kwargs):
        tier = user.get("tier", SubscriptionTier.FREE)
        client = get_whop_client()
        
        swing_limit = client.get_swing_limit(tier)
        
        # -1 means unlimited
        if swing_limit == -1:
            return await func(*args, user=user, **kwargs)
        
        # Check usage (this would come from database)
        swings_used = _get_swings_used(user.get("user_id"))
        
        if swings_used >= swing_limit:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "swing_limit_exceeded",
                    "message": f"You've used all {swing_limit} swings on your {tier.value} plan",
                    "swings_used": swings_used,
                    "swing_limit": swing_limit,
                    "upgrade_message": "Upgrade to Pro for unlimited swings!"
                }
            )
        
        # Increment usage (this would update database)
        _increment_swings_used(user.get("user_id"))
        
        return await func(*args, user=user, **kwargs)
    
    return wrapper


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _get_tiers_with_feature(feature: str) -> list:
    """Get list of tiers that include a feature"""
    tiers = []
    for tier, config in WHOP_PRODUCTS.items():
        if feature in config.get("features", []):
            tiers.append(tier.value)
    return tiers


# In-memory swing usage tracking (replace with database)
_swing_usage = {}

def _get_swings_used(user_id: str) -> int:
    """Get number of swings used by user this month"""
    return _swing_usage.get(user_id, 0)

def _increment_swings_used(user_id: str):
    """Increment swing count for user"""
    _swing_usage[user_id] = _swing_usage.get(user_id, 0) + 1


# ============================================================================
# USAGE CHECK ENDPOINTS
# ============================================================================

from fastapi import APIRouter

router = APIRouter(prefix="/api/subscription", tags=["Subscription"])


@router.get("/status")
async def get_subscription_status(user: dict = Depends(get_current_user)):
    """Get user's subscription status and usage"""
    tier = user.get("tier")
    client = get_whop_client()
    
    swing_limit = client.get_swing_limit(tier)
    swings_used = _get_swings_used(user.get("user_id"))
    
    # Get available features
    features = WHOP_PRODUCTS[tier]["features"]
    
    return {
        "user_id": user.get("user_id"),
        "tier": tier.value,
        "membership": {
            "id": user.get("membership").membership_id if user.get("membership") else None,
            "status": user.get("membership").status if user.get("membership") else "none",
            "valid": user.get("membership").valid if user.get("membership") else False
        },
        "usage": {
            "swings_used": swings_used,
            "swing_limit": swing_limit if swing_limit != -1 else "unlimited",
            "swings_remaining": "unlimited" if swing_limit == -1 else max(0, swing_limit - swings_used)
        },
        "features": features
    }


@router.get("/features/{feature}")
async def check_feature(
    feature: str,
    user: dict = Depends(get_current_user)
):
    """Check if user has access to a specific feature"""
    tier = user.get("tier")
    client = get_whop_client()
    
    has_access = client.check_feature_access(tier, feature)
    
    return {
        "feature": feature,
        "has_access": has_access,
        "current_tier": tier.value,
        "available_in_tiers": _get_tiers_with_feature(feature) if not has_access else None
    }


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WHOP FEATURE GATE MIDDLEWARE TEST")
    print("="*70)
    
    print(f"\n🔒 Feature Gating:")
    print(f"  - @require_feature('ai_coach') - Requires ai_coach feature")
    print(f"  - @require_tier(SubscriptionTier.PRO) - Requires Pro+ tier")
    print(f"  - @check_swing_limit - Enforces swing limit")
    
    print(f"\n👤 User Authentication:")
    print(f"  - Header: X-User-Id")
    print(f"  - Header: X-Membership-Id")
    
    print(f"\n✅ Endpoints:")
    print(f"  - GET /api/subscription/status - Get user subscription info")
    print(f"  - GET /api/subscription/features/{{feature}} - Check feature access")
    
    print("\n" + "="*70)
    print("✅ FEATURE GATE MIDDLEWARE READY")
    print("="*70 + "\n")
