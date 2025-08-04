from .base_agent import BaseAgent
import random

class ParentingAgent(BaseAgent):
    def __init__(self, user_id: int, conversation_manager=None):
        super().__init__("parenting", user_id, conversation_manager)
    
    def get_personality_traits(self) -> dict:
        return {
            "tone": "caring_but_accountable",
            "focus": "quality_engagement", 
            "accountability_level": "gentle_firm",
            "motivation_style": "legacy_building"
        }
    
    def generate_daily_prompt(self) -> str:
        prompts = [
            "What specific quality time will you have with your son today? Phone away, fully present.",
            "Basketball season starts Aug 11 - how will you prepare for gym time together?", 
            "Dinner engagement plan: What will you discuss with your son tonight?",
            "Weekend family activity ideas: What memory will you create this week?",
            "Gaming balance: How will you enjoy video games together without excess?"
        ]
        return random.choice(prompts)
    
    def generate_base_prompt(self):
        """Generate base prompt without pattern checking - prevents recursion"""
        prompts = [
            "What specific quality time will you have with your son today? Phone away, fully present.",
            "Basketball season starts Aug 11 - how will you prepare for gym time together?",
            "Dinner engagement plan: What will you discuss with your son tonight?",
            "Weekend family activity ideas: What memory will you create this week?",
            "Gaming balance: How will you enjoy video games together without excess?"
        ]
        import random
        return random.choice(prompts)
    
    def analyze_response(self, user_response: str, conversation_context=None) -> str:
        response = user_response.lower()
        
        if any(word in response for word in ["phone away", "present", "focused", "no distractions"]):
            return "✅ **Present parenting commitment.** Quality attention creates lasting impact. Duration planned?"
        
        if any(word in response for word in ["gym", "basketball", "sports", "active"]):
            return "🏀 **Active bonding confirmed.** Physical activities build stronger relationships. Consistency is key."
        
        if any(word in response for word in ["might", "if I can", "depends"]):
            return "⚠️ **Conditional parenting detected.** Your son deserves certainty. What specific time commitment can you guarantee?"
        
        return f"**Parenting commitment logged:** {user_response}\n\nHow will this strengthen your relationship and his development?"
    
    def generate_follow_up(self, user_response: str, analysis_result: str):
        """Generate intelligent follow-up questions"""
        response = user_response.lower()
        
        # If commitment is conditional, demand specificity
        if "conditional parenting" in analysis_result:
            return "**Follow-up required:** Give me the specific time and activity you can guarantee, regardless of work or business demands."
        
        # If it's present parenting, check for obstacles
        if "present parenting" in analysis_result:
            return "**Timing confirmation:** What exact time, and what's your backup plan if work/business thoughts interfere?"
        
        # If it's active bonding, ensure consistency
        if "active bonding" in analysis_result:
            return "**Consistency question:** How does this become a reliable routine rather than occasional occurrence?"
        
        # No follow-up needed
        return None
    
    def generate_crisis_prompt(self, avoidance_data):
        """Crisis intervention based on avoidance patterns"""
        avoided_tasks = avoidance_data.get('common_avoided_tasks', [])
        failure_count = avoidance_data.get('failure_count', 0)
        
        return f"""
🚨 **PARENTING CRISIS ALERT**

**Pattern Recognition:** You've missed {failure_count} quality time commitments with your son recently.

**Reality Check:** These foundational years don't come back. Work stress is stealing present-moment parenting.

**The Truth:** Your business builds your future. Your parenting builds HIS future. Both require intentional attention.

**Override Action:** One hour of completely present time TODAY. Phone away, work thoughts off, full engagement.

What specific activity will you do with your son in the next 2 hours?
"""
    
    def generate_intervention_prompt(self):
        """Intervention for declining trend"""
        insights = self.get_predictive_insights()
        insight_text = "\n".join(insights) if insights else ""
        
        return f"""
⚠️ **PARENTING ATTENTION DECLINING**

**Pattern Alert:** Your quality time consistency is dropping. This affects your relationship foundation.

**Predictive Analysis:**
{insight_text}

**Course Correction:** What specific father-son activity will you commit to RIGHT NOW to reverse this trend?
"""
    
    def generate_momentum_prompt(self):
        """Capitalize on positive momentum"""
        insights = self.get_predictive_insights()
        insight_text = "\n".join(insights) if insights else ""
        
        return f"""
👨‍👦 **PARENTING EXCELLENCE MOMENTUM**

**Pattern Recognition:** You're consistently delivering quality time. Your son is benefiting from your attention.

**Success Analysis:**
{insight_text}

**Momentum Question:** What deeper father-son experience will you create today while your parenting consistency is strong?
"""
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
👨‍👦 **Parenting Excellence Alert**

**Pattern Recognition:** Work stress and business building are reducing your present-moment parenting quality.

**Impact:** Your son notices distracted attention. These years are foundational for your relationship.

**Perspective:** Business success means nothing if you miss building the relationship that matters most.

**Action Required:** One hour of completely present time today. Phone away, work thoughts off, full engagement.

Your business builds your future. Your parenting builds his future. Both require intentional attention.
"""