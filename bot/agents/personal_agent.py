from .base_agent import BaseAgent
import random

class PersonalAgent(BaseAgent):
    def __init__(self, user_id, conversation_manager):
        super().__init__("personal", user_id, conversation_manager)
    
    def get_personality_traits(self):
        return {
            "tone": "balanced_and_wise",
            "focus": "sustainable_performance",
            "accountability_level": "supportive_firm",
            "motivation_style": "long_term_optimization"
        }
    
    def generate_daily_prompt(self):
        """Simple daily prompt for personal balance"""
        prompts = [
            "How will you recharge today in a way that enhances rather than detracts from your business and family performance?",
            "Gaming, movie, or social time: What recharge activity optimizes tomorrow's performance?",
            "What guilt-free activity will restore your energy for business and family demands?",
            "Personal time balance: Enough to recharge, not so much you lose drive?",
            "What activity will genuinely restore your capacity for challenges?"
        ]
        return random.choice(prompts)
    
    def generate_crisis_prompt(self, avoidance_data):
        """Crisis intervention for personal balance issues"""
        return """
🎯 **PERSONAL BALANCE CRISIS**

**Pattern Alert:** Your personal time has become either excessive escapism or insufficient recovery.

**Performance Impact:** Poor balance creates either burnout or momentum loss.

**Calibration Required:** Strategic rest that restores energy without killing drive.

**Action Required:** 60-90 minutes of quality leisure that leaves you refreshed and motivated, not dulled and avoidant.
"""
    
    def generate_intervention_prompt(self):
        """Intervention for declining personal balance"""
        return """
⚠️ **PERSONAL BALANCE DECLINING**

**Pattern Alert:** Your rest-to-work ratio is affecting overall performance sustainability.

**Course Correction:** What restorative activity will genuinely enhance your capacity for business and family excellence?
"""
    
    def generate_momentum_prompt(self):
        """Capitalize on positive balance momentum"""
        return """
⚖️ **PERSONAL BALANCE OPTIMIZED**

**Pattern Recognition:** Your strategic rest is enhancing performance across all life domains.

**Momentum Question:** How will you maintain this balance while continuing to challenge yourself in business and family growth?
"""
    
    def analyze_response(self, user_response, conversation_context=None):
        """Enhanced analysis with balance focus"""
        response = user_response.lower()
        
        # Strategic rest recognition
        if any(word in response for word in ["recharge", "restore", "balance", "energy"]):
            return "⚖️ **Strategic rest confirmed.** Recovery that enhances performance rather than detracts from it."
        
        # Social connection recognition
        if any(word in response for word in ["friends", "family", "social", "connection"]):
            return "👥 **Social recharge selected.** Human connection enhances all life domains."
        
        # Escapism indicators
        if any(phrase in response for phrase in ["forget about", "escape from", "avoid thinking", "distract myself"]):
            return "⚠️ **Escapism detected rather than restoration.** Healthy personal time enhances your capacity for challenges."
        
        # Specific activities
        if any(word in response for word in ["gaming", "movie", "beach", "pool", "reading"]):
            return "🎮 **Specific leisure activity selected.** Enjoyment is productivity fuel when balanced properly."
        
        return f"**Personal time commitment analyzed:** {user_response}"
    
    def generate_follow_up(self, user_response, analysis_result):
        """Generate follow-up questions for personal commitments"""
        
        # If escapism detected
        if "escapism detected" in analysis_result:
            return "**Reframe question:** What activity would genuinely restore your energy for business and family excellence?"
        
        # If strategic rest confirmed
        if "strategic rest" in analysis_result or "social recharge" in analysis_result:
            return "**Duration boundaries:** How will you prevent this from becoming excessive or turning into avoidance behavior?"
        
        # If specific activity selected
        if "leisure activity" in analysis_result:
            return "**Quality focus:** How will you ensure this restores rather than drains your motivation for tomorrow's challenges?"
        
        return None
    
    def get_intervention_message(self, pattern_data):
        """Generate personal balance intervention"""
        return """
🎯 **PERSONAL BALANCE ACCOUNTABILITY**

**Balance Principle:** Personal time should restore energy and motivation, not drain them or create avoidance patterns.

**Optimal State:** Strategic rest that makes you excited to tackle business and family challenges.

**Action Required:** What specific activity will optimize your capacity for sustained excellence?

**Quality over Quantity:** 60-90 minutes of genuine restoration beats hours of mindless escapism.
"""