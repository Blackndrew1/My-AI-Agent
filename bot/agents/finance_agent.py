from .base_agent import BaseAgent
import random

class FinanceAgent(BaseAgent):
    def __init__(self, user_id, conversation_manager):
        super().__init__("finance", user_id, conversation_manager)
    
    def get_personality_traits(self):
        return {
            "tone": "analytical_and_direct",
            "focus": "business_investment_mindset",
            "accountability_level": "sharp",
            "motivation_style": "wealth_building"
        }
    
    def generate_daily_prompt(self):
        """Simple daily prompt for financial discipline"""
        prompts = [
            "Any planned purchases today? Distinguish between business investment and impulse spending.",
            "What money action advances your consultant business: expense tracking, revenue planning, or investment decisions?",
            "Spending patterns when stressed: What's your awareness plan today?",
            "Business expense vs. personal expense: How will you categorize today's spending?",
            "What financial discipline supports your business building goals today?"
        ]
        return random.choice(prompts)
    
    def generate_crisis_prompt(self, avoidance_data):
        """Crisis intervention for financial avoidance"""
        return """
💳 **FINANCIAL DISCIPLINE CRISIS**

**Pattern Alert:** You're avoiding financial awareness and discipline, which undermines business confidence.

**Reality Check:** Every dollar spent on comfort reduces capital available for business investment.

**Business Impact:** Poor financial discipline = reduced business risk-taking = slower consultant growth.

**Override Action:** Name one business investment that would generate more value than any comfort purchase you're considering.
"""
    
    def generate_intervention_prompt(self):
        """Intervention for declining financial discipline"""
        return """
⚠️ **FINANCIAL DISCIPLINE DECLINING**

**Pattern Alert:** Your money awareness and discipline are slipping. This typically affects business confidence.

**Course Correction:** What specific financial action will demonstrate discipline and support business goals?
"""
    
    def generate_momentum_prompt(self):
        """Capitalize on positive financial momentum"""
        return """
💰 **FINANCIAL DISCIPLINE STRONG**

**Pattern Recognition:** Your financial awareness is supporting business confidence and growth.

**Momentum Question:** What financial goal or investment will you pursue while your discipline is strong?
"""
    
    def analyze_response(self, user_response, conversation_context=None):
        """Enhanced analysis with financial focus"""
        response = user_response.lower()
        
        # Impulse spending rationalization
        if any(phrase in response for phrase in ["deserve", "treat myself", "just this once", "earned it"]):
            return "❌ **Impulse spending rationalization detected.** 'Deserve' is expensive. What business goal does this purchase support?"
        
        # Business investment recognition
        if any(word in response for word in ["business", "investment", "tools", "education", "networking"]):
            return "✅ **Business investment mindset activated.** This spending creates future earning capacity."
        
        # Savings and planning recognition
        if any(word in response for word in ["save", "budget", "plan", "track"]):
            return "💰 **Financial discipline engaged.** Delayed gratification creates business opportunity freedom."
        
        return f"**Financial commitment analyzed:** {user_response}"
    
    def generate_follow_up(self, user_response, analysis_result):
        """Generate follow-up questions for financial commitments"""
        
        # If impulse spending detected
        if "impulse spending" in analysis_result:
            return "**Follow-up required:** What business investment would generate more value than this purchase?"
        
        # If business investment recognized
        if "business investment" in analysis_result:
            return "**ROI question:** How will you measure the return on this investment? What specific business outcome will it enable?"
        
        # If financial discipline engaged
        if "financial discipline" in analysis_result:
            return "**Correlation tracking:** How does financial discipline in personal life correlate with discipline in business development?"
        
        return None
    
    def get_intervention_message(self, pattern_data):
        """Generate financial intervention"""
        return """
💳 **FINANCIAL ACCOUNTABILITY CHECK**

**Money Reality:** Every spending decision is a strategic choice between building your consultant business or maintaining current lifestyle.

**Action Required:** What financial discipline supports your business building today?

**Choice:** Business investment or comfort consumption. Choose consciously.
"""