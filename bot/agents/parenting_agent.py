from .base_agent import BaseAgent
import random

class ParentingAgent(BaseAgent):
    def __init__(self, user_id: int):
        super().__init__("parenting", user_id)
    
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
    
    def analyze_response(self, user_response: str) -> str:
        response = user_response.lower()
        
        if any(word in response for word in ["phone away", "present", "focused", "no distractions"]):
            return "✅ **Present parenting commitment.** Quality attention creates lasting impact. Duration planned?"
        
        if any(word in response for word in ["gym", "basketball", "sports", "active"]):
            return "🏀 **Active bonding confirmed.** Physical activities build stronger relationships. Consistency is key."
        
        if any(word in response for word in ["might", "if I can", "depends"]):
            return "⚠️ **Conditional parenting detected.** Your son deserves certainty. What specific time commitment can you guarantee?"
        
        return f"**Parenting commitment logged:** {user_response}\n\nHow will this strengthen your relationship and his development?"
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
👨‍👦 **Parenting Excellence Alert**

**Pattern Recognition:** Work stress and business building are reducing your present-moment parenting quality.

**Impact:** Your son notices distracted attention. These years are foundational for your relationship.

**Perspective:** Business success means nothing if you miss building the relationship that matters most.

**Action Required:** One hour of completely present time today. Phone away, work thoughts off, full engagement.

Your business builds your future. Your parenting builds his future. Both require intentional attention.
"""

class WorkAgent(BaseAgent):
    def __init__(self, user_id: int):
        super().__init__("work", user_id)
    
    def get_personality_traits(self) -> dict:
        return {
            "tone": "efficiency_focused",
            "focus": "automation_opportunities",
            "accountability_level": "strategic", 
            "motivation_style": "time_liberation"
        }
    
    def generate_daily_prompt(self) -> str:
        prompts = [
            "What repetitive customer support task will you automate today?",
            "Which administrative process can be streamlined or eliminated?", 
            "Email templates, report automation, or workflow optimization - pick one to implement.",
            "What manual task takes 30+ minutes that could be reduced to 5 minutes?",
            "How will you demonstrate automation expertise that impresses colleagues?"
        ]
        return random.choice(prompts)
    
    def analyze_response(self, user_response: str) -> str:
        response = user_response.lower()
        
        if any(word in response for word in ["automate", "template", "script", "system"]):
            return "🤖 **Automation mindset activated.** This saves time AND builds your AI expertise portfolio. Implementation timeline?"
        
        if any(word in response for word in ["email", "report", "process", "workflow"]):
            return "⚡ **Efficiency target identified.** Time saved here = more business development opportunity. Quantify the impact."
        
        if any(word in response for word in ["nothing", "can't", "no time"]):
            return "❌ **Automation avoidance.** You're in customer support - there are dozens of automation opportunities. Pick the easiest one."
        
        return f"**Work automation commitment logged:** {user_response}\n\nHow will this demonstration of efficiency build your consultant reputation?"
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
💼 **Work Efficiency Alert**

**Current Status:** You're stuck in manual task loops that prevent business development time.

**Opportunity Cost:** Every hour spent on routine work tasks is an hour not building your consultant business.

**Skill Building:** Automation implementations become portfolio pieces for client presentations.

**Action Required:** Identify ONE 15-minute task you do repeatedly. Spend 1 hour automating it this week.

**ROI:** 1 hour investment saves 5+ hours monthly + demonstrates expertise to potential clients.

Stop being busy. Start being efficient. Your business depends on this transition.
"""

class PersonalAgent(BaseAgent):
    def __init__(self, user_id: int):
        super().__init__("personal", user_id)
    
    def get_personality_traits(self) -> dict:
        return {
            "tone": "balanced_and_wise",
            "focus": "sustainable_performance",
            "accountability_level": "supportive_firm",
            "motivation_style": "long_term_optimization"
        }
    
    def generate_daily_prompt(self) -> str:
        prompts = [
            "Gaming, movie, or social time: What recharge activity optimizes tomorrow's performance?",
            "Beach, pool, or leisure plans: How will you enjoy life while maintaining momentum?",
            "Personal time balance: Enough to recharge, not so much you lose drive?", 
            "What guilt-free activity will restore your energy for business and family demands?",
            "Social connections or solo recharge: What does your energy level need today?"
        ]
        return random.choice(prompts)
    
    def analyze_response(self, user_response: str) -> str:
        response = user_response.lower()
        
        if any(word in response for word in ["balance", "recharge", "restore", "energy"]):
            return "⚖️ **Strategic rest identified.** Recovery enables peak performance. Duration limits planned?"
        
        if any(word in response for word in ["gaming", "movie", "beach", "pool"]):
            return "🎮 **Specific leisure activity.** Enjoyment is productivity fuel. How will you prevent this from becoming escapism?"
        
        if any(word in response for word in ["social", "friends", "family", "connection"]):
            return "👥 **Social recharge selected.** Human connection enhances all life domains. Quality over quantity."
        
        return f"**Personal time commitment logged:** {user_response}\n\nHow will this leisure time enhance your business and family performance?"
    
    def get_intervention_message(self, pattern_data: dict) -> str:
        return """
🎯 **Personal Balance Alert**

**Pattern Detection:** You're either working too much (burnout risk) or recharging too much (momentum loss).

**Optimal State:** Strategic rest that restores energy without killing drive.

**Current Need:** Based on your recent pattern, you need [more focused rest / less escape time].

**Balance Principle:** Personal time should make you excited to return to business and family, not avoid them.

**Calibration:** 60-90 minutes of quality leisure that leaves you refreshed, not dulled.

Your personal time quality directly affects your business and parenting performance. Choose wisely.
"""