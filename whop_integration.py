"""
Whop API Integration
===================

Handles Whop payment/subscription integration for Catching Barrels app.

Features:
- Subscription tier management (Free/Pro/Premium/Ultimate)
- Webhook handling for membership events
- Feature access control
- User membership validation

Author: Builder 2
Date: 2024-12-25
"""

import os
import requests
from typing import Dict, Optional, List
from enum import Enum
from dataclasses import dataclass
from datetime import datetime


# Whop API Configuration
WHOP_API_KEY = os.getenv(
    "WHOP_API_KEY", 
    "apik_loM4MlWuGqvp1_C3686518_C_2a4ff33b51fa665398c5ebadf5776a732b3f95a6ceb26c023fa1f39bc"
)
WHOP_COMPANY_ID = os.getenv("WHOP_COMPANY_ID", "biz_4f4wiRWwiEZflF")
WHOP_API_BASE = "https://api.whop.com/api/v2"


# Subscription Tiers
class SubscriptionTier(str, Enum):
    FREE = "free"
    PRO = "pro"
    PREMIUM = "premium"
    ULTIMATE = "ultimate"


# Product IDs and Configuration
WHOP_PRODUCTS = {
    SubscriptionTier.FREE: {
        "id": "prod_Wkwv5hjyghOXC",
        "name": "Free Swing Audit",
        "price": 0,
        "swing_limit": 1,
        "features": [
            "basic_analysis",
            "motor_profile"
        ]
    },
    SubscriptionTier.PRO: {
        "id": "prod_O4CB6y0IzNJLe",
        "name": "Barrels Pro",
        "monthly_price": 19.99,
        "annual_price": 149.99,
        "swing_limit": -1,  # Unlimited
        "features": [
            "basic_analysis",
            "motor_profile",
            "ai_coach",
            "drill_library",
            "progress_tracking"
        ]
    },
    SubscriptionTier.PREMIUM: {
        "id": "prod_7068OOSHrjMvc",
        "name": "Barrels Premium",
        "price": 99.00,
        "swing_limit": -1,  # Unlimited
        "features": [
            "basic_analysis",
            "motor_profile",
            "ai_coach",
            "drill_library",
            "progress_tracking",
            "group_calls",
            "video_analysis"
        ]
    },
    SubscriptionTier.ULTIMATE: {
        "id": "prod_OXEGclGuMyYVd",
        "name": "Barrels Ultimate",
        "price": 299.99,
        "swing_limit": -1,  # Unlimited
        "features": [
            "basic_analysis",
            "motor_profile",
            "ai_coach",
            "drill_library",
            "progress_tracking",
            "group_calls",
            "video_analysis",
            "one_on_one",
            "priority_support"
        ]
    }
}

# Seasonal Products
WHOP_SEASONAL_PRODUCTS = {
    "in_person_assessment": {
        "id": "prod_KKk4VF8oUWKUB",
        "name": "In-Person Assessment",
        "price": 399.00,
        "type": "one_time"
    },
    "90_day_transformation": {
        "id": "prod_zH1wnZs0JKKfd",
        "name": "90-Day Transformation",
        "price": 1299.00,
        "type": "program"
    }
}


@dataclass
class WhopMembership:
    """Whop membership data"""
    membership_id: str
    user_id: str
    product_id: str
    status: str  # active, canceled, expired, etc.
    tier: SubscriptionTier
    valid: bool
    expires_at: Optional[datetime] = None


class WhopClient:
    """
    Whop API Client
    
    Handles all Whop API interactions including:
    - Fetching membership data
    - Validating subscriptions
    - Checking feature access
    """
    
    def __init__(self, api_key: str = WHOP_API_KEY):
        """Initialize Whop client"""
        self.api_key = api_key
        self.base_url = WHOP_API_BASE
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def get_membership(self, membership_id: str) -> Optional[Dict]:
        """
        Get membership by ID
        
        Args:
            membership_id: Whop membership ID
            
        Returns:
            Membership data or None
        """
        try:
            response = requests.get(
                f"{self.base_url}/memberships/{membership_id}",
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Failed to get membership: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching membership: {e}")
            return None
    
    def get_user_memberships(self, user_id: str) -> List[Dict]:
        """
        Get all memberships for a user
        
        Args:
            user_id: Whop user ID
            
        Returns:
            List of membership data
        """
        try:
            response = requests.get(
                f"{self.base_url}/memberships",
                headers=self.headers,
                params={"user_id": user_id},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
            else:
                print(f"Failed to get user memberships: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error fetching user memberships: {e}")
            return []
    
    def validate_membership(self, membership_id: str) -> Optional[WhopMembership]:
        """
        Validate membership and return subscription tier
        
        Args:
            membership_id: Whop membership ID
            
        Returns:
            WhopMembership object or None
        """
        membership_data = self.get_membership(membership_id)
        
        if not membership_data:
            return None
        
        # Extract key fields
        product_id = membership_data.get("product_id")
        status = membership_data.get("status")
        user_id = membership_data.get("user_id")
        
        # Determine tier from product ID
        tier = self._get_tier_from_product_id(product_id)
        
        # Check if membership is valid
        valid = status == "active"
        
        # Parse expiration date
        expires_at = None
        if "expires_at" in membership_data:
            try:
                expires_at = datetime.fromisoformat(
                    membership_data["expires_at"].replace("Z", "+00:00")
                )
            except:
                pass
        
        return WhopMembership(
            membership_id=membership_id,
            user_id=user_id,
            product_id=product_id,
            status=status,
            tier=tier,
            valid=valid,
            expires_at=expires_at
        )
    
    def _get_tier_from_product_id(self, product_id: str) -> SubscriptionTier:
        """Map product ID to subscription tier"""
        for tier, config in WHOP_PRODUCTS.items():
            if config["id"] == product_id:
                return tier
        
        # Default to FREE if product not found
        return SubscriptionTier.FREE
    
    def check_feature_access(
        self, 
        tier: SubscriptionTier, 
        feature: str
    ) -> bool:
        """
        Check if a subscription tier has access to a feature
        
        Args:
            tier: User's subscription tier
            feature: Feature to check
            
        Returns:
            True if user has access, False otherwise
        """
        if tier not in WHOP_PRODUCTS:
            return False
        
        features = WHOP_PRODUCTS[tier]["features"]
        return feature in features
    
    def get_swing_limit(self, tier: SubscriptionTier) -> int:
        """
        Get swing analysis limit for a tier
        
        Args:
            tier: Subscription tier
            
        Returns:
            Swing limit (-1 for unlimited)
        """
        if tier not in WHOP_PRODUCTS:
            return 0
        
        return WHOP_PRODUCTS[tier]["swing_limit"]
    
    def create_checkout_session(
        self, 
        product_id: str, 
        success_url: str,
        cancel_url: str
    ) -> Optional[str]:
        """
        Create a Whop checkout session
        
        Args:
            product_id: Whop product ID
            success_url: URL to redirect on success
            cancel_url: URL to redirect on cancel
            
        Returns:
            Checkout session URL or None
        """
        try:
            response = requests.post(
                f"{self.base_url}/checkout_sessions",
                headers=self.headers,
                json={
                    "product_id": product_id,
                    "success_url": success_url,
                    "cancel_url": cancel_url
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("url")
            else:
                print(f"Failed to create checkout: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error creating checkout: {e}")
            return None


# Singleton instance
_whop_client = None

def get_whop_client() -> WhopClient:
    """Get singleton Whop client instance"""
    global _whop_client
    if _whop_client is None:
        _whop_client = WhopClient()
    return _whop_client


# ============================================================================
# FEATURE ACCESS HELPERS
# ============================================================================

def can_use_ai_coach(tier: SubscriptionTier) -> bool:
    """Check if tier can use AI coach"""
    return get_whop_client().check_feature_access(tier, "ai_coach")

def can_access_drill_library(tier: SubscriptionTier) -> bool:
    """Check if tier can access drill library"""
    return get_whop_client().check_feature_access(tier, "drill_library")

def can_join_group_calls(tier: SubscriptionTier) -> bool:
    """Check if tier can join group calls"""
    return get_whop_client().check_feature_access(tier, "group_calls")

def can_schedule_one_on_one(tier: SubscriptionTier) -> bool:
    """Check if tier can schedule 1-on-1 sessions"""
    return get_whop_client().check_feature_access(tier, "one_on_one")


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("WHOP INTEGRATION TEST")
    print("="*70)
    
    client = get_whop_client()
    
    print(f"\n📡 Whop API Configuration:")
    print(f"  Base URL: {WHOP_API_BASE}")
    print(f"  Company ID: {WHOP_COMPANY_ID}")
    print(f"  API Key: {WHOP_API_KEY[:20]}...")
    
    print(f"\n🎯 Subscription Tiers:")
    for tier, config in WHOP_PRODUCTS.items():
        print(f"\n  {tier.upper()}:")
        print(f"    Product ID: {config['id']}")
        print(f"    Swing Limit: {config['swing_limit']}")
        print(f"    Features: {', '.join(config['features'])}")
    
    print(f"\n✅ Feature Access Matrix:")
    features = ["ai_coach", "drill_library", "group_calls", "one_on_one"]
    print(f"\n{'Tier':<12} | " + " | ".join(f"{f:<15}" for f in features))
    print("-" * 70)
    
    for tier in SubscriptionTier:
        access = [
            "✅" if client.check_feature_access(tier, f) else "❌" 
            for f in features
        ]
        print(f"{tier.value:<12} | " + " | ".join(f"{a:<15}" for a in access))
    
    print("\n" + "="*70)
    print("✅ WHOP INTEGRATION MODULE LOADED")
    print("="*70 + "\n")
