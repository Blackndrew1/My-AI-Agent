from .base_agent import BaseAgent
import random

class WorkAgent(BaseAgent):
    def __init__(self, user_id, conversation_manager=None):
        super().__init__("work", user_id, conversation_manager)
    
    def get_personality_traits(self):
        return {
            "tone": "efficiency_focused",
            "focus": "automation_opportunities",
            "accountability_level": "strategic",
            "motivation_style": "time_liberation"
        }
    
    def generate_daily_prompt(self):
        """Simple daily prompt for work automation"""
        prompts = [
            "What repetitive work task will you automate today to create more capacity for business building?",
            "Which customer support process can be streamlined or eliminated?",
            "Email templates, report automation, or workflow optimization - pick one to implement.",
            "What manual task takes 30+ minutes that could be reduced to 5 minutes?",
            "How will you demonstrate automation expertise that builds your consultant portfolio?"
        ]
        return random.choice(prompts)
    
    def generate_base_prompt(self):
        """Generate base prompt without pattern checking - prevents recursion"""
        prompts = [
            "What repetitive customer support task will you automate today?",
            "Which administrative process can be streamlined or eliminated?",
            "Email templates, report automation, or workflow optimization - pick one to implement.",
            "What manual task takes 30+ minutes that could be reduced to 5 minutes?",
            "How will you demonstrate automation expertise that impresses colleagues?"
        ]
        import random
        return random.choice(prompts)
    
    def generate_crisis_prompt(self, avoidance_data):
        """Crisis intervention for work efficiency avoidance"""
        return """
💼 **WORK EFFICIENCY CRISIS**

**Pattern Alert:** You're stuck in manual task loops that prevent business development time.

**Opportunity Cost:** Every hour spent on routine work is an hour not building your consultant business.

**Reality Check:** You can't scale a consultant business if you can't automate your own work processes.

**Implementation Question:** What's the simplest automation you could implement today that would save time this week?
"""
    
    def generate_intervention_prompt(self):
        """Intervention for declining work efficiency"""
        return """
⚠️ **WORK EFFICIENCY DECLINING**

**Pattern Alert:** You're avoiding automation opportunities, trading business development time for busy work.

**Course Correction:** What specific automation will you implement today to create capacity for business focus?
"""
    
    def generate_momentum_prompt(self):
        """Capitalize on positive work efficiency momentum"""
        return """
🤖 **WORK AUTOMATION MOMENTUM STRONG**

**Pattern Recognition:** Your automation implementations are creating time and demonstrating expertise.

**Momentum Question:** What advanced automation will you tackle today while your efficiency focus is strong?
"""
    
    def analyze_response(self, user_response, conversation_context=None):
        """Enhanced analysis with efficiency focus"""
        response = user_response.lower()
        
        # Automation opportunity recognition
        if any(word in response for word in ["automate", "template", "system", "process", "script"]):
            return "🤖 **Automation opportunity identified.** This saves time AND builds portfolio credibility."
        
        # Manual process acceptance
        if any(phrase in response for phrase in ["nothing to automate", "no time", "too complex"]):
            return "❌ **Automation avoidance detected.** You're in customer support - automation opportunities are everywhere."
        
        # Efficiency improvement recognition
        if any(word in response for word in ["email", "report", "template", "workflow"]):
            return "⚡ **Efficiency improvement target confirmed.** This type of automation typically saves 60-80% of task time."
        
        return f"**Work automation commitment analyzed:** {user_response}"
    
    def generate_follow_up(self, user_response, analysis_result):
        """Generate follow-up questions for work commitments"""
        
        # If automation opportunity identified
        if "automation opportunity" in analysis_result:
            return "**Implementation timeline:** When specifically will you build this, and how will you document the time savings for your portfolio?"
        
        # If automation avoidance detected
        if "automation avoidance" in analysis_result:
            return "**Reality check:** Start with the most repetitive task you do daily. What's the easiest automation to begin with?"
        
        # If efficiency improvement confirmed
        if "efficiency improvement" in analysis_result:
            return "**Portfolio development:** How will you document this automation for client demonstrations and business development?"
        
        return None
    
    def get_intervention_message(self, pattern_data):
        """Generate work efficiency intervention"""
        return """
💼 **WORK EFFICIENCY ACCOUNTABILITY**

**Current Status:** Manual work tasks are consuming time that could build your consultant business.

**Competitive Advantage:** Automation expertise is exactly what your future clients need.

**Action Required:** Identify ONE 15-minute task you do repeatedly. Automate it this week.

**ROI:** 1 hour investment saves 5+ hours monthly + demonstrates expertise to potential clients.
"""