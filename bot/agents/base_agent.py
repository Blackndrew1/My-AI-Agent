from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from typing import Dict, List, Optional
from bot.pattern_analyzer import PatternAnalyzer

class BaseAgent(ABC):
    """Enhanced base class with pattern analysis capabilities"""
    
    def __init__(self, domain_name, user_id, conversation_manager, db_path="life_agent.db"):
        self.domain = domain_name
        self.user_id = user_id
        self.conversation_manager = conversation_manager
        self.db_path = db_path
        self.personality_traits = self.get_personality_traits()
        self.pattern_analyzer = PatternAnalyzer(db_path)
    
    def get_pattern_based_prompt(self):
        """Generate prompt based on user's behavioral patterns"""
        patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 14)
        
        # Get domain-specific patterns
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        avoidance_patterns = patterns.get('avoidance_patterns', {})
        
        if self.domain in domain_patterns:
            completion_rate = domain_patterns[self.domain]['completion_rate']
            trend = domain_patterns[self.domain]['trend']
            
            if completion_rate < 0.3:
                return self.generate_crisis_prompt(avoidance_patterns)
            elif trend == 'declining':
                return self.generate_intervention_prompt()
            elif trend == 'improving':
                return self.generate_momentum_prompt()
        
        return self.generate_daily_prompt()
    
    @abstractmethod
    def generate_crisis_prompt(self, avoidance_data):
        """Generate crisis intervention prompt"""
        pass
    
    @abstractmethod
    def generate_intervention_prompt(self):
        """Generate trend intervention prompt"""
        pass
    
    @abstractmethod
    def generate_momentum_prompt(self):
        """Generate momentum building prompt"""
        pass
    
    def get_predictive_insights(self):
        """Get predictive insights about likely success/failure"""
        patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 30)
        
        insights = []
        
        # Domain completion insights
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        if self.domain in domain_patterns:
            completion_rate = domain_patterns[self.domain]['completion_rate']
            trend = domain_patterns[self.domain]['trend']
            
            if trend == 'improving':
                insights.append(f"📈 **{self.domain.title()} momentum building:** {completion_rate:.0%} completion rate and improving")
            elif trend == 'declining':
                insights.append(f"⚠️ **{self.domain.title()} pattern decline:** {completion_rate:.0%} completion rate and declining")
        
        # Cross-domain insights (simplified for now)
        if self.domain == 'business':
            health_data = domain_patterns.get('health', {})
            if health_data and health_data.get('completion_rate', 0) < 0.5:
                insights.append("⚡ **Energy Alert:** Low health consistency typically reduces business performance")
        
        return insights
    
    def predict_commitment_success(self, commitment_text):
        """Predict likelihood of commitment success"""
        patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 30)
        
        # Base prediction on domain completion rate
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        base_rate = 0.5  # Default 50%
        
        if self.domain in domain_patterns:
            base_rate = domain_patterns[self.domain]['completion_rate']
        
        # Language analysis
        commitment_lower = commitment_text.lower()
        certain_words = ['will', 'going to', 'must', 'committed to', 'definitely']
        uncertain_words = ['maybe', 'try', 'hope', 'might', 'probably']
        
        if any(word in commitment_lower for word in certain_words):
            base_rate += 0.2
        if any(word in commitment_lower for word in uncertain_words):
            base_rate -= 0.3
        
        return min(max(base_rate, 0.1), 0.9)  # Keep between 10% and 90%
    
    @abstractmethod
    def get_personality_traits(self):
        """Return personality traits for this agent"""
        pass
    
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
    
    @abstractmethod
    def get_intervention_message(self, pattern_data):
        """Generate intervention based on patterns"""
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
        """Process user response with full conversation intelligence"""
        context = self.conversation_manager.get_conversation_context(self.user_id)
        
        # Add user message to conversation
        self.conversation_manager.add_message(
            self.user_id, 'user', user_response, 'response'
        )
        
        # Analyze response with context
        analysis = self.analyze_response(user_response, context)
        
        # Add analysis to conversation
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
            # Conversation complete, lock commitment
            self.lock_commitment(user_response)
            self.conversation_manager.end_conversation(self.user_id, 'committed')
            return f"{analysis}\n\n✅ **Commitment locked and tracked.**"
    
    def lock_commitment(self, commitment_text):
        """Lock in final commitment to database"""
        import sqlite3
        from datetime import datetime
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO daily_checkins (user_id, date, domain, commitment, completed)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, datetime.now().date(), self.domain, commitment_text, False))
        
        conn.commit()
        conn.close()