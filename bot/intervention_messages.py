from typing import Dict, List
import random
from datetime import datetime

class InterventionMessageGenerator:
    """Generates escalating intervention messages based on level and context"""
    
    def __init__(self):
        self.personality_traits = {
            'business': 'direct_challenging',
            'health': 'energy_focused', 
            'finance': 'analytical_sharp',
            'parenting': 'caring_accountable',
            'work': 'efficiency_focused',
            'personal': 'balanced_wise'
        }
    
    def generate_intervention_message(self, domain: str, level: int, trigger_data: Dict, user_patterns: Dict = None) -> str:
        """Generate intervention message based on level and context"""
        
        if level == 1:
            return self.generate_gentle_reminder(domain, trigger_data)
        elif level == 2:
            return self.generate_pattern_alert(domain, trigger_data, user_patterns)
        elif level == 3:
            return self.generate_firm_intervention(domain, trigger_data, user_patterns)
        elif level == 4:
            return self.generate_crisis_intervention(domain, trigger_data, user_patterns)
        elif level == 5:
            return self.generate_emergency_override(domain, trigger_data, user_patterns)
        else:
            return "System error: Invalid intervention level"
    
    def generate_gentle_reminder(self, domain: str, trigger_data: Dict) -> str:
        """Level 1: Gentle accountability reminder"""
        
        if domain == 'business':
            return f"""
🔔 **Business Reminder**

I noticed you haven't completed your business commitment yet today.

**What was planned:** {trigger_data.get('commitment', 'Business action')}
**Time since commitment:** {trigger_data.get('hours_overdue', 0):.1f} hours

Quick check: What's the current status? Still on track to complete this?
"""
        
        elif domain == 'health':
            return f"""
⚡ **Energy Check**

Your health commitment is pending.

**What was planned:** {trigger_data.get('commitment', 'Physical activity')}

Physical momentum affects everything else. What's the current plan for getting this done?
"""
        
        # Add similar gentle reminders for other domains...
        return f"Gentle reminder: Your {domain} commitment needs attention."
    
    def generate_pattern_alert(self, domain: str, trigger_data: Dict, user_patterns: Dict) -> str:
        """Level 2: Pattern recognition alert"""
        
        completion_rate = trigger_data.get('completion_rate', 0)
        
        if domain == 'business':
            return f"""
⚠️ **Business Pattern Alert**

**Pattern Recognition:** You're entering a business avoidance cycle.

**Current completion rate:** {completion_rate:.0%} (down from your baseline)
**Typical outcome:** This pattern usually leads to 2-week business stagnation

**Pattern Break Required:** What specific business action will you complete in the next 2 hours to interrupt this avoidance cycle?

This is the intervention moment. Choose momentum or continue the decline.
"""
        
        elif domain == 'health':
            return f"""
💪 **Health Pattern Alert**

**Energy Decline Detected:** {completion_rate:.0%} completion rate in health domain.

**Correlation Impact:** Your business performance typically drops 40% when health consistency fails.

**Pattern Break:** 15 minutes of movement in the next hour. What specific activity will change your state?

Your physical foundation supports everything else. Fix this first.
"""
        
        # Add pattern alerts for other domains...
        return f"Pattern alert for {domain}: Action required to break negative cycle."
    
    def generate_firm_intervention(self, domain: str, trigger_data: Dict, user_patterns: Dict) -> str:
        """Level 3: Firm intervention with direct confrontation"""
        
        completion_rate = trigger_data.get('completion_rate', 0)
        
        if domain == 'business':
            return f"""
🚨 **BUSINESS INTERVENTION REQUIRED**

**Reality Check:** You're avoiding business actions at a rate that guarantees mediocrity.

**Pattern Analysis:**
- Business completion rate: {completion_rate:.0%}
- Typical avoided tasks: Client outreach, direct sales, uncomfortable conversations

**The Uncomfortable Truth:** Your consultant business exists in the gap between comfort and growth. Every comfort choice keeps you in customer support.

**Intervention Protocol:**
1. Name the ONE business action you're most afraid to do
2. Complete it in the next 2 hours  
3. Report back with results or explain what stopped you

**Choice:** Comfort zone maintenance (stay where you are) or growth actions (build your business).

**Response Required:** Specific action + exact completion timeline. This intervention continues until action is taken.
"""
        
        elif domain == 'health':
            return f"""
⚡ **ENERGY INTERVENTION REQUIRED**

**Physical Foundation Crisis:** {completion_rate:.0%} health completion rate.

**Performance Impact:** Your business and family energy are suffering from physical neglect.

**Reality Check:** You can't build a successful business or be an excellent parent from a declining physical foundation.

**Emergency Action:** Break the inactivity cycle NOW.

**Minimum Viable Movement:** 10 minutes of any physical activity in the next 30 minutes.

Your energy IS your competitive advantage. Protect it.
"""
        
        # Add firm interventions for other domains...
        return f"Firm intervention required for {domain}."
    
    def generate_crisis_intervention(self, domain: str, trigger_data: Dict, user_patterns: Dict) -> str:
        """Level 4: Crisis intervention for severe patterns"""
        
        if domain == 'business':
            return f"""
🚨 **BUSINESS CRISIS - EMERGENCY PROTOCOLS ACTIVATED**

**Crisis Status:** Complete business avoidance mode detected.

**Current Reality:** You've entered the death spiral that kills entrepreneurial dreams. Normal business development has stopped.

**Emergency Simplification:** Forget complex strategies. Focus on survival-level business actions.

**Emergency Actions (Choose ONE):**
1. Send ONE email to ONE potential client
2. Post ONE social media update showcasing your expertise  
3. Make ONE networking call to ONE business contact
4. Update ONE business profile (LinkedIn, website, portfolio)

**Truth:** Every successful consultant started with one uncomfortable action. Your business doesn't need a perfect strategy - it needs momentum.

**Emergency Response:** Pick one action. Do it in the next 30 minutes. Report back. We rebuild from here.
"""
        
        return f"Crisis intervention for {domain}: Emergency action required."
    
    def generate_emergency_override(self, domain: str, trigger_data: Dict, user_patterns: Dict) -> str:
        """Level 5: Emergency override for system breakdown"""
        
        return f"""
🚨 **EMERGENCY OVERRIDE - SYSTEM BREAKDOWN DETECTED**

**Critical Status:** Multiple life domains failing simultaneously.

**Emergency Simplification:** All complex goals suspended. Focus on basic function restoration.

**Emergency Actions:**
1. {domain.title()}: ONE simple action in the next 15 minutes
2. Report completion immediately
3. No planning, no optimization - just basic momentum restoration

**System Restart Protocol:** We're rebuilding from fundamental actions. Complex goals resume once basic momentum is restored.

**Emergency Response Required:** Action + immediate confirmation. External accountability may be activated.
"""

if __name__ == "__main__":
    generator = InterventionMessageGenerator()
    print("Intervention message generator ready!")