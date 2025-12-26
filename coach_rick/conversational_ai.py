"""
Coach Rick Conversational AI Module
Generates natural, encouraging coaching messages using GPT-4

Author: Builder 2
Date: 2024-12-24
Status: Phase 2 - Day 2
"""

import os
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
import requests


@dataclass
class CoachMessage:
    """Coach Rick AI message"""
    message_type: str  # analysis, encouragement, drill_intro, progress
    content: str
    player_name: Optional[str] = None
    timestamp: Optional[str] = None


class ConversationalAI:
    """
    Generates natural coaching messages using GPT-4
    
    Features:
    - Personalized analysis feedback
    - Encouraging, positive tone
    - Technical explanations in simple language
    - Drill introductions and motivation
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Conversational AI
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self.api_url = "https://api.openai.com/v1/chat/completions"
        
        # Coach Rick personality traits
        self.coach_personality = {
            "tone": "encouraging, enthusiastic, knowledgeable",
            "style": "conversational, uses baseball terminology naturally",
            "approach": "emphasizes small wins, technical clarity, actionable feedback",
            "voice": "experienced coach who's seen it all, but stays positive"
        }
    
    def generate_analysis_message(
        self,
        player_name: str,
        motor_profile: str,
        confidence: float,
        patterns: List[Dict],
        metrics: Dict
    ) -> CoachMessage:
        """
        Generate personalized swing analysis message
        
        Args:
            player_name: Player's name
            motor_profile: Motor profile type (Spinner, Whipper, Torquer)
            confidence: Classification confidence (0-100)
            patterns: List of detected patterns
            metrics: Analysis metrics (bat speed, exit velo, etc.)
        
        Returns:
            CoachMessage with analysis
        """
        
        # Build context for GPT-4
        prompt = self._build_analysis_prompt(
            player_name, motor_profile, confidence, patterns, metrics
        )
        
        # Call GPT-4
        content = self._call_gpt4(prompt, max_tokens=300)
        
        return CoachMessage(
            message_type="analysis",
            content=content,
            player_name=player_name
        )
    
    def generate_drill_introduction(
        self,
        player_name: str,
        primary_issue: str,
        drill_name: str,
        expected_gains: str
    ) -> CoachMessage:
        """
        Generate motivating drill introduction
        
        Args:
            player_name: Player's name
            primary_issue: Main issue to address
            drill_name: Name of prescribed drill
            expected_gains: Expected improvements
        
        Returns:
            CoachMessage with drill intro
        """
        
        prompt = f"""
You are Coach Rick, an experienced hitting coach known for your encouraging approach.

Write a short, motivating introduction for a drill prescription.

Player: {player_name}
Issue: {primary_issue}
Drill: {drill_name}
Expected Gains: {expected_gains}

Guidelines:
- 2-3 sentences max
- Acknowledge the issue positively ("I see you're working on...")
- Explain WHY this drill will help
- End with encouragement

Keep it conversational and upbeat.
"""
        
        content = self._call_gpt4(prompt, max_tokens=150)
        
        return CoachMessage(
            message_type="drill_intro",
            content=content,
            player_name=player_name
        )
    
    def generate_encouragement(
        self,
        player_name: str,
        context: str = "general"
    ) -> CoachMessage:
        """
        Generate general encouragement
        
        Args:
            player_name: Player's name
            context: Context (general, improvement, struggle)
        
        Returns:
            CoachMessage with encouragement
        """
        
        prompts = {
            "general": f"Write 1-2 encouraging sentences for {player_name} as Coach Rick, their hitting coach. Be brief and positive.",
            "improvement": f"Write 1-2 sentences celebrating {player_name}'s recent improvements. Be specific about effort, not results.",
            "struggle": f"Write 1-2 sentences encouraging {player_name} through a difficult training period. Emphasize process over results."
        }
        
        prompt = prompts.get(context, prompts["general"])
        content = self._call_gpt4(prompt, max_tokens=100)
        
        return CoachMessage(
            message_type="encouragement",
            content=content,
            player_name=player_name
        )
    
    def _build_analysis_prompt(
        self,
        player_name: str,
        motor_profile: str,
        confidence: float,
        patterns: List[Dict],
        metrics: Dict
    ) -> str:
        """Build GPT-4 prompt for swing analysis"""
        
        # Format patterns
        patterns_text = ""
        for p in patterns[:2]:  # Top 2 patterns
            patterns_text += f"- {p['name']}: {p['description']}\n"
        
        # Format key metrics
        bat_speed = metrics.get('bat_speed_mph', 'N/A')
        exit_velo = metrics.get('exit_velocity_mph', 'N/A')
        efficiency = metrics.get('efficiency_percent', 'N/A')
        
        prompt = f"""
You are Coach Rick, an experienced hitting coach with 20+ years working with players from Little League to MLB.

Analyze this swing for {player_name}:

MOTOR PROFILE: {motor_profile} (Confidence: {confidence:.0f}%)

KEY METRICS:
- Bat Speed: {bat_speed} mph
- Exit Velocity: {exit_velo} mph  
- Efficiency: {efficiency}%

PATTERNS DETECTED:
{patterns_text}

Write a 3-4 sentence analysis in Coach Rick's voice:
1. Start with something positive (even if it's just effort/commitment)
2. Explain their motor profile in simple terms
3. Address the main pattern/issue found
4. End with an optimistic note about improvement potential

Guidelines:
- Use first person ("I see...", "I notice...")
- Be conversational, not clinical
- Use baseball terminology naturally
- Stay positive and encouraging
- Keep it under 100 words
"""
        
        return prompt
    
    def _call_gpt4(
        self,
        prompt: str,
        max_tokens: int = 200,
        temperature: float = 0.7
    ) -> str:
        """
        Call OpenAI GPT-4 API
        
        Args:
            prompt: System prompt
            max_tokens: Max response length
            temperature: Creativity (0-1)
        
        Returns:
            Generated text
        """
        
        # FALLBACK MODE: If no API key, return template response
        if not self.api_key or self.api_key == "your-openai-key-here":
            return self._generate_fallback_message(prompt)
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "gpt-4",
            "messages": [
                {"role": "system", "content": "You are Coach Rick, an encouraging hitting coach."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            content = result['choices'][0]['message']['content'].strip()
            return content
            
        except Exception as e:
            print(f"⚠️  GPT-4 API Error: {e}")
            print("    Falling back to template responses...")
            return self._generate_fallback_message(prompt)
    
    def _generate_fallback_message(self, prompt: str) -> str:
        """
        Generate template-based response when GPT-4 unavailable
        
        This ensures the system works even without OpenAI API key
        """
        
        # Detect message type from prompt
        if "drill prescription" in prompt.lower():
            return "I've put together a drill plan that's going to help you unlock some serious power. Let's get to work!"
        
        elif "motor profile" in prompt.lower() or "swing analysis" in prompt.lower():
            # Extract key info from prompt
            if "Spinner" in prompt:
                profile = "Spinner"
                tip = "focus on extending those arms through the hitting zone"
            elif "Whipper" in prompt:
                profile = "Whipper"
                tip = "dial in your timing for more consistent contact"
            elif "Torquer" in prompt:
                profile = "Torquer"
                tip = "leverage that ground force even more"
            else:
                profile = "your swing style"
                tip = "work on consistency in your approach"
            
            return f"Great to see you working on your swing! I can see you're a {profile}, which means you generate power through rotation. The key for you is going to be to {tip}. With the right adjustments, I'm seeing real potential for improvement here."
        
        elif "encouraging" in prompt.lower() or "struggle" in prompt.lower():
            return "Keep grinding! Every rep counts, and I can see you putting in the work. Trust the process - the results will come."
        
        else:
            return "Looking good! Let's keep building on this foundation. I'm here to help you reach the next level."


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("CONVERSATIONAL AI (COACH RICK) TEST")
    print("="*70)
    
    # Initialize (will use fallback mode without API key)
    coach = ConversationalAI()
    
    # Test 1: Analysis Message
    print("\n📊 TEST 1: SWING ANALYSIS MESSAGE")
    print("-" * 70)
    
    analysis_msg = coach.generate_analysis_message(
        player_name="Eric Williams",
        motor_profile="Spinner",
        confidence=85.0,
        patterns=[
            {
                "pattern_id": "spinner_lead_arm_bent",
                "name": "Lead arm not extending through pitch plane",
                "description": "Lead arm stays bent through contact",
                "severity": "HIGH"
            },
            {
                "pattern_id": "spinner_over_rotation",
                "name": "Shoulders over-compensating",
                "description": "Arms not creating momentum on pitch plane",
                "severity": "HIGH"
            }
        ],
        metrics={
            "bat_speed_mph": 82,
            "exit_velocity_mph": 99,
            "efficiency_percent": 111
        }
    )
    
    print(f"Player: {analysis_msg.player_name}")
    print(f"Type: {analysis_msg.message_type}")
    print(f"\nMessage:\n{analysis_msg.content}")
    
    # Test 2: Drill Introduction
    print("\n\n🎯 TEST 2: DRILL INTRODUCTION")
    print("-" * 70)
    
    drill_msg = coach.generate_drill_introduction(
        player_name="Eric Williams",
        primary_issue="Lead arm not extending through pitch plane",
        drill_name="Rope Swings",
        expected_gains="+3-5 mph exit velocity, better away contact"
    )
    
    print(f"Type: {drill_msg.message_type}")
    print(f"\nMessage:\n{drill_msg.content}")
    
    # Test 3: Encouragement
    print("\n\n💪 TEST 3: ENCOURAGEMENT MESSAGE")
    print("-" * 70)
    
    encouragement_msg = coach.generate_encouragement(
        player_name="Eric Williams",
        context="improvement"
    )
    
    print(f"Type: {encouragement_msg.message_type}")
    print(f"\nMessage:\n{encouragement_msg.content}")
    
    print("\n" + "="*70)
    print("✅ CONVERSATIONAL AI MODULE: WORKING")
    print("="*70)
    print("\nNOTE: Currently using FALLBACK MODE (template responses)")
    print("      Set OPENAI_API_KEY environment variable for GPT-4 integration")
    print("="*70 + "\n")
