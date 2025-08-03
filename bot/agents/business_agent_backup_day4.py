from .base_agent import BaseAgent
import random

class BusinessAgent(BaseAgent):
    def __init__(self, user_id: int):
        super().__init__("business", user_id)
    
    def get_personality_traits(self) -> dict:
        return {
            "tone": "direct_and_challenging",
            "focus": "revenue_generating_actions", 
            "accountability_level": "firm",
            "motivation_style": "results_oriented"
        }
    
    def generate_daily_prompt(self) -> str:
        prompts = [
            "What's your ONE business action today that directly advances your consultant/agency goals?",
            "Name the specific client outreach or content creation task you'll complete today.",
            "What business-building action are you most likely to avoid today? Do it first.",
            "Which consultant skill will you demonstrate or improve today?",
            "What specific step moves you closer to your first AI automation client?"
        ]
        return random.choice(prompts)
    
    def analyze_response(self, user_response: str) -> str:
        response = user_response.lower()
        
        # Check for vague language
        if any(word in response for word in ["maybe", "try to", "hope", "think about"]):
            return "❌ **Too vague.** 'Maybe' and 'try' are failure words. Give me a specific, measurable action."
        
        # Check for revenue focus
        if any(word in response for word in ["client", "customer", "proposal", "outreach", "content"]):
            return "✅ **Revenue-focused action identified.** Time blocked for this? What's your accountability check?"
        
        # Check for disguised procrastination
        if any(word in response for word in ["research", "learn", "study", "read"]):
            return "⚠️ **Learning or research?** That's often disguised procrastination. What ACTION follows this learning?"
        
        return f"**Business commitment logged:** {user_response}\n\nWhat specific obstacle will try to stop you, and how will you override it?"
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
🚨 **Business Discipline Alert**

You're in your typical business avoidance pattern. I see it clearly:

**Pattern:** You commit to business actions but avoid the uncomfortable ones (cold outreach, direct sales, putting yourself out there).

**Reality Check:** Your consultant/agency won't build itself. Every day you avoid direct business action, you stay in customer support instead of building your future.

**Override Command:** Name ONE uncomfortable business action you'll complete in the next 2 hours. Not tomorrow. Not later. Now.

This is your success or failure moment. Choose.
"""


class HealthAgent(BaseAgent):
    def __init__(self, user_id: int):
        super().__init__("health", user_id)
    
    def get_personality_traits(self) -> dict:
        return {
            "tone": "energy_focused",
            "focus": "performance_optimization",
            "accountability_level": "firm_but_supportive", 
            "motivation_style": "performance_correlation"
        }
    
    def generate_daily_prompt(self) -> str:
        prompts = [
            "Morning workout plan: Gym, home routine, or outdoor activity? Your energy depends on this choice.",
            "What physical activity will optimize your business performance today?",
            "How will you and your son stay active together today? (Gym session after Aug 11?)",
            "Your body fuels your mind. What's the fitness commitment that ensures peak performance?",
            "Rate your energy 1-10. What physical action raises that number today?"
        ]
        return random.choice(prompts)
    
    def analyze_response(self, user_response: str) -> str:
        response = user_response.lower()
        
        if any(word in response for word in ["skip", "rest day", "too tired", "later"]):
            return "❌ **Energy excuses detected.** Low energy is often caused by skipping exercise, not fixed by avoiding it. 10-minute walk minimum?"
        
        if any(word in response for word in ["gym", "workout", "run", "basketball", "son"]):
            return "✅ **Energy investment confirmed.** This typically correlates with 40% better business performance. Track that connection."
        
        if "morning" in response:
            return "🎯 **Morning routine locked in.** Early physical activity = sustained energy all day. What time specifically?"
        
        return f"**Health commitment logged:** {user_response}\n\nHow will this affect your business energy and focus today?"
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
⚡ **Energy Performance Alert**

**Data Pattern:** Your business productivity drops 60% on days you skip morning movement.

**Current Status:** You're entering a low-energy spiral that typically lasts 3-5 days and kills business momentum.

**Intervention:** 15-minute movement NOW. Walk, pushups, stretching - anything that changes your physical state.

**Truth:** You can't build a successful business from a declining physical foundation. Your energy IS your business advantage.

Move your body in the next 10 minutes or accept mediocre business results today.
"""


class FinanceAgent(BaseAgent):
    def __init__(self, user_id: int):
        super().__init__("finance", user_id)
    
    def get_personality_traits(self) -> dict:
        return {
            "tone": "analytical_and_direct",
            "focus": "business_investment_mindset",
            "accountability_level": "sharp",
            "motivation_style": "wealth_building"
        }
    
    def generate_daily_prompt(self) -> str:
        prompts = [
            "Any planned purchases today? Distinguish between business investment and impulse spending.",
            "What money action advances your consultant business: expense cutting, revenue tracking, or client pricing?",
            "Spending patterns when stressed: What's your awareness plan today?",
            "Business expense vs. personal expense: How will you categorize today's spending?",
            "What financial discipline supports your business building goals today?"
        ]
        return random.choice(prompts)
    
    def analyze_response(self, user_response: str) -> str:
        response = user_response.lower()
        
        if any(word in response for word in ["deserve", "treat myself", "just this once"]):
            return "❌ **Impulse spending rationalization detected.** 'Deserve' is expensive. What business goal does this purchase support?"
        
        if any(word in response for word in ["business", "investment", "tools", "education"]):
            return "✅ **Business investment mindset.** How will you measure ROI on this expense?"
        
        if any(word in response for word in ["save", "budget", "track"]):
            return "💰 **Financial discipline engaged.** Savings create business opportunity freedom. Track the correlation."
        
        return f"**Financial commitment logged:** {user_response}\n\nBusiness building or consumption? Every dollar spent is a strategic choice."
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
💳 **Financial Discipline Alert**

**Pattern Recognition:** You typically overspend when business stress increases - avoiding revenue actions while spending comfort money.

**Current Trajectory:** This pattern delays business growth by 2-3 months each time it happens.

**Reality:** Every dollar spent on comfort could be business investment capital.

**Override Action:** Name one business expense that would generate more value than whatever you're considering buying.

Money follows discipline. Discipline creates business success. Choose wisely.
"""