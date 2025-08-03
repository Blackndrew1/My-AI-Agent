from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from typing import Dict, List, Optional

class BaseAgent(ABC):
    """Enhanced base class with conversation capabilities"""
    
    def __init__(self, domain_name, user_id, conversation_manager, db_path="life_agent.db"):
        self.domain = domain_name
        self.user_id = user_id
        self.conversation_manager = conversation_manager
        self.db_path = db_path
    
    @abstractmethod
    def generate_daily_prompt(self):
        """Generate daily commitment prompt"""
        pass
    
    @abstractmethod
    def analyze_response(self, user_response, conversation_context=None):
        """Analyze response with conversation context"""
        pass
    
    @abstractmethod
    def generate_follow_up(self, user_response, analysis_result):
        """Generate intelligent follow-up questions"""
        pass
    
    def start_domain_conversation(self):
        """Start focused conversation for this domain"""
        session_id = self.conversation_manager.start_conversation(self.user_id, self.domain)
        initial_prompt = self.generate_daily_prompt()
        
        self.conversation_manager.add_message(
            self.user_id, 'agent', initial_prompt, 'initial_prompt'
        )
        
        return initial_prompt
    
    def process_user_response(self, user_response):
        """Process user response with conversation intelligence"""
        context = self.conversation_manager.get_conversation_context(self.user_id)
        
        # Add user message
        self.conversation_manager.add_message(
            self.user_id, 'user', user_response, 'response'
        )
        
        # Analyze response
        analysis = self.analyze_response(user_response, context)
        
        # Add analysis
        self.conversation_manager.add_message(
            self.user_id, 'agent', analysis, 'analysis'
        )
        
        # Generate follow-up if needed
        follow_up = self.generate_follow_up(user_response, analysis)
        
        if follow_up:
            self.conversation_manager.add_message(
                self.user_id, 'agent', follow_up, 'follow_up'
            )
            return f"{analysis}\n\n{follow_up}"
        else:
            # Conversation complete
            self.lock_commitment(user_response)
            self.conversation_manager.end_conversation(self.user_id, 'committed')
            return f"{analysis}\n\n✅ **Commitment locked and tracked.**"
    
    def lock_commitment(self, commitment_text):
        """Lock commitment to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO daily_checkins (user_id, date, domain, commitment, completed)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, datetime.now().date(), self.domain, commitment_text, False))
        
        conn.commit()
        conn.close()
    
    def get_domain_patterns(self, days=7):
        """Get recent patterns for this domain"""
        return self.conversation_manager.get_recent_patterns(self.user_id, self.domain, days)

class EnhancedBusinessAgent(BaseAgent):
    def __init__(self, user_id, conversation_manager):
        super().__init__("business", user_id, conversation_manager)
    
    def generate_daily_prompt(self):
        patterns = self.get_domain_patterns(7)
        
        if len(patterns) == 0:
            return "**First business check-in.** What's your ONE specific business action today that moves your consultant goals forward?"
        
        completion_rate = sum(1 for p in patterns if p[2]) / len(patterns) if patterns else 0
        
        if completion_rate < 0.3:
            return "**Business crisis.** You've avoided business actions 70%+ recently. What uncomfortable action will you do TODAY?"
        elif completion_rate < 0.6:
            return "**Inconsistent progress.** What specific client outreach or content creation will you complete today?"
        else:
            return "**Strong momentum.** What's today's action that builds on your wins?"
    
    def analyze_response(self, user_response, conversation_context=None):
        response = user_response.lower()
        
        if any(word in response for word in ["maybe", "try to", "hope", "think about"]):
            return "❌ **Vague commitment detected.** 'Maybe' and 'try' are failure words. I need specific, measurable action."
        
        if any(word in response for word in ["research", "learn", "study", "read"]):
            return "⚠️ **Learning procrastination alert.** Research without action is avoidance. What ACTION follows this learning TODAY?"
        
        if any(word in response for word in ["client", "customer", "proposal", "outreach", "content"]):
            return "✅ **Revenue-generating action identified.** This advances your consultant goals."
        
        return f"**Business commitment analyzed:** {user_response}"
    
    def generate_follow_up(self, user_response, analysis_result):
        if "vague commitment" in analysis_result:
            return "**Follow-up required:** Give me specific action, exact time, and how you'll measure completion."
        
        if "learning procrastination" in analysis_result:
            return "**Follow-up required:** What SPECIFIC action follows this learning today? Client call? Content creation?"
        
        if "revenue-generating action" in analysis_result:
            return "**Strong commitment confirmed.** What's the most likely obstacle that will stop you? How will you override it?"
        
        return None

if __name__ == "__main__":
    print("✅ Enhanced Business Agent ready!")