from .base_agent import BaseAgent
import random

class BusinessAgent(BaseAgent):
    def __init__(self, user_id, conversation_manager=None):
        super().__init__("business", user_id, conversation_manager)

    def get_personality_traits(self):
        return {
            "tone": "direct_and_challenging",
            "focus": "revenue_generating_actions",
            "accountability_level": "firm",
            "motivation_style": "results_oriented"
        }

    def generate_daily_prompt(self):
        """Use pattern-based prompting"""
        return self.get_pattern_based_prompt()

    def generate_base_prompt(self):
        """Generate base prompt without pattern checking - prevents recursion"""
        prompts = [
            "What's your ONE specific business action today that directly advances your consultant goals?",
            "Name the specific client outreach or content creation task you'll complete today.",
            "What business-building action are you most likely to avoid today? Do it first.",
            "Which consultant skill will you demonstrate or improve today?",
            "What specific step moves you closer to your first AI automation client?"
        ]
        return random.choice(prompts)

    def generate_crisis_prompt(self, avoidance_data):
        """Crisis intervention based on avoidance patterns"""
        avoided_tasks = avoidance_data.get('common_avoided_tasks', [])
        failure_count = avoidance_data.get('failure_count', 0)
        
        avoided_text = f" (You consistently avoid: {', '.join(avoided_tasks[:2])})" if avoided_tasks else ""

        return f"""
🚨 **BUSINESS CRISIS ALERT**

**Pattern Recognition:** You've failed {failure_count} business commitments recently{avoided_text}.

**Reality Check:** At this avoidance rate, you'll still be in customer support in 2 years.

**The Uncomfortable Truth:** What specific business action are you most afraid to do? That's exactly what you must do TODAY.

**Override Question:** What's the ONE client-facing action that makes you uncomfortable but would directly advance your consultant goals?
"""

    def generate_intervention_prompt(self):
        """Intervention for declining trend"""
        insights = self.get_predictive_insights()
        insight_text = "\n".join(insights) if insights else ""

        return f"""
⚠️ **BUSINESS MOMENTUM DECLINING**

**Pattern Alert:** Your business action consistency is dropping. This is the critical intervention moment.

**Predictive Analysis:**
{insight_text}

**Course Correction:** What business action will you commit to RIGHT NOW to reverse this trend?
"""

    def generate_momentum_prompt(self):
        """Capitalize on positive momentum"""
        insights = self.get_predictive_insights()
        insight_text = "\n".join(insights) if insights else ""

        return f"""
🚀 **BUSINESS MOMENTUM BUILDING**

**Pattern Recognition:** You're on an upward trend. Time to capitalize.

**Success Analysis:**
{insight_text}

**Momentum Question:** What bigger business challenge will you tackle today while your execution momentum is strong?
"""

    def analyze_response(self, user_response, conversation_context=None):
        """Enhanced analysis with success prediction"""
        response = user_response.lower()

        # Check for specificity
        if any(word in response for word in ["maybe", "try to", "hope", "think about", "probably"]):
            return "❌ **Vague commitment detected.** 'Maybe' and 'try' are failure words. I need a specific, measurable action with a timeline."

        # Check for avoidance disguised as learning
        if any(word in response for word in ["research", "learn", "study", "read", "course"]):
            return "⚠️ **Learning procrastination alert.** Research without action is sophisticated avoidance. What ACTION follows this learning TODAY?"

        # Check for revenue focus
        if any(word in response for word in ["client", "customer", "proposal", "outreach", "networking", "content"]):
            return "✅ **Revenue-generating action identified.** This directly advances your consultant goals."

        # Check for business building vs. maintenance
        if any(word in response for word in ["organize", "plan", "setup", "prepare"]):
            return "📋 **Preparation task noted.** Preparation is valuable, but what CLIENT-FACING action follows this prep work?"

        return f"**Business commitment analyzed:** {user_response}"

    def generate_follow_up(self, user_response, analysis_result):
        """Generate intelligent follow-up questions"""
        response = user_response.lower()

        # If commitment is too vague, demand specificity
        if "vague commitment" in analysis_result:
            return "**Follow-up required:** Give me the specific action, the exact time you'll do it, and how you'll measure completion. No escape words."

        # If it's learning/research, demand the action component
        if "learning procrastination" in analysis_result:
            return "**Follow-up required:** After you complete this learning, what SPECIFIC action will you take with that knowledge today? Client call? Content creation? Outreach message?"

        # If it's preparation, ensure there's client-facing follow-through
        if "preparation task" in analysis_result:
            return "**Follow-up required:** Preparation is step 1. What's step 2 that involves actual client interaction or market visibility?"

        # If commitment is strong, check for obstacles
        if "revenue-generating action" in analysis_result:
            success_probability = self.predict_commitment_success(user_response)
            return f"**Strong commitment confirmed.** Success prediction: {success_probability:.0%}. What's the most likely obstacle that will try to stop you today?"

        # No follow-up needed
        return None

    def get_intervention_message(self, pattern_data):
        """Generate intervention based on patterns"""
        try:
            patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 14)
            domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})

            if self.domain in domain_patterns:
                completion_rate = domain_patterns[self.domain]['completion_rate']

                if completion_rate < 0.3:
                    return """
🚨 **BUSINESS CRISIS INTERVENTION**

**Brutal Reality:** You've avoided business actions 70%+ of the time. At this pace, you'll still be in customer support in 2 years.

**Pattern Recognition:** You consistently avoid client-facing actions. Every avoidance keeps you exactly where you are.

**Reality Check:** Your consultant business requires doing things that make you uncomfortable. There's no comfortable path to business success.

**Non-Negotiable Action:** Name the ONE business action you're most afraid to do. You have 2 hours to complete it.

No "maybe" or "I'll try." Give me the specific action and exact timeline.
"""

            return "**Business accountability check:** What specific business action will you commit to today?"
        except Exception:
            return "**Business accountability check:** What specific business action will you commit to today?"