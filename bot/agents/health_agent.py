from .base_agent import BaseAgent
import random

class HealthAgent(BaseAgent):
    def __init__(self, user_id, conversation_manager=None):
        super().__init__("health", user_id, conversation_manager)
    
    def get_personality_traits(self):
        return {
            "tone": "energy_focused",
            "focus": "performance_optimization", 
            "accountability_level": "firm_but_supportive",
            "motivation_style": "performance_correlation"
        }
   
    def generate_daily_prompt(self):
        """Use pattern-based prompting"""
        return self.get_pattern_based_prompt()
    
    def generate_base_prompt(self):
        """Generate base prompt without pattern checking - prevents recursion"""
        prompts = [
            "What's your physical activity plan today? (Morning workout, gym with son, or active recovery)",
            "Your body is your business foundation. What's today's energy investment?",
            "Morning workout plan: Gym, home routine, or outdoor activity?",
            "How will you and your son stay active together today?",
            "What physical activity will optimize your business performance today?"
        ]
        return random.choice(prompts)
    
    def generate_crisis_prompt(self, avoidance_data):
        """Crisis intervention for health avoidance"""
        return """
⚡ **ENERGY CRISIS INTERVENTION**

**Reality Check:** You've consistently avoided physical activity, and it's affecting your business and family energy.

**Energy Physics:** Low energy isn't solved by avoiding exercise - it's CAUSED by it.

**Emergency Action:** 10 minutes of movement RIGHT NOW. Walk, pushups, anything that changes your physical state.

**Choice:** Break the pattern now or accept low energy performance.
"""
    
    def generate_intervention_prompt(self):
        """Intervention for declining health trend"""
        return """
⚠️ **HEALTH MOMENTUM DECLINING**

**Pattern Alert:** Your physical activity consistency is dropping. This typically affects all life domains.

**Course Correction:** What physical activity will you commit to RIGHT NOW to reverse this energy decline?
"""
    
    def generate_momentum_prompt(self):
        """Capitalize on positive health momentum"""
        return """
🏃‍♂️ **HEALTH MOMENTUM STRONG**

**Pattern Recognition:** Your consistent physical activity is boosting all life domains.

**Momentum Question:** What physical challenge will you add today while your health discipline is strong?
"""
    
    def analyze_response(self, user_response, conversation_context=None):
        """Enhanced analysis with energy focus"""
        response = user_response.lower()
        
        # Energy excuse detection
        if any(word in response for word in ["skip", "rest day", "too tired", "later", "maybe"]):
            return "❌ **Energy excuse detected.** 'Too tired' is usually code for 'haven't moved my body.' Low energy is typically CAUSED by inactivity."
        
        # Morning movement recognition
        if "morning" in response:
            return "🌅 **Morning energy investment confirmed.** Early physical activity = sustained energy all day."
        
        # Family fitness integration
        if any(word in response for word in ["son", "basketball", "together", "gym"]):
            return "🏀 **Father-son fitness partnership activated.** Shared physical activity strengthens relationships."
        
        # Specific activity recognition
        if any(word in response for word in ["workout", "run", "walk", "exercise"]):
            return "💪 **Energy investment confirmed.** Physical activity is business fuel and family energy enhancement."
        
        return f"**Health commitment analyzed:** {user_response}"
    
    def generate_follow_up(self, user_response, analysis_result):
        """Generate follow-up questions for health commitments"""
        
        # If energy excuse detected, demand minimum action
        if "energy excuse" in analysis_result:
            return "**Follow-up required:** What's the MINIMUM movement that would change your physical state right now? 10-minute walk? 20 pushups?"
        
        # If good commitment, confirm timing
        if "morning energy" in analysis_result or "father-son fitness" in analysis_result:
            return "**Timing confirmation:** What exact time will this happen, and what's your backup plan if something interferes?"
        
        return None
    
    def get_intervention_message(self, pattern_data):
        """Generate health intervention"""
        return """
⚡ **HEALTH ACCOUNTABILITY CHECK**

**Energy Reality:** Your physical foundation affects everything - business performance, family energy, personal satisfaction.

**Action Required:** What specific physical activity will you commit to today?

**Choice:** Energy investment or energy decline. Choose consciously.
"""