from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
import json
from typing import Dict, List, Optional
from bot.pattern_analyzer import PatternAnalyzer
from bot.intervention_engine import InterventionEngine
from bot.intervention_messages import InterventionMessageGenerator

class BaseAgent(ABC):
    """Enhanced base class with conversation and intervention capabilities"""
    
    def __init__(self, domain_name, user_id, conversation_manager, db_path="life_agent.db"):
        self.domain = domain_name
        self.user_id = user_id
        self.conversation_manager = conversation_manager
        self.db_path = db_path
        self.personality_traits = self.get_personality_traits()
        self.pattern_analyzer = PatternAnalyzer(db_path)
        self.intervention_engine = InterventionEngine(db_path)
        self.intervention_generator = InterventionMessageGenerator()
    
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
    
    def get_pattern_based_prompt(self):
        """Generate prompt based on user's behavioral patterns"""
        patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 14)
        
        # Get domain-specific patterns
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        avoidance_patterns = patterns.get('avoidance_patterns', {}).get('avoidance_by_domain', {})
        
        if self.domain in domain_patterns:
            completion_rate = domain_patterns[self.domain]['completion_rate']
            trend = domain_patterns[self.domain]['trend']
            
            if completion_rate < 0.3:
                return self.generate_crisis_prompt(avoidance_patterns.get(self.domain, {}))
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
    
    def check_intervention_needed(self):
        """Check if intervention is needed for this domain"""
        intervention_level = self.intervention_engine.get_intervention_level(self.user_id, self.domain)
        
        if intervention_level > 0:
            # Get trigger data for context
            trigger_data = self.get_recent_triggers()
            user_patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 14)
            
            # Generate intervention message
            intervention_message = self.intervention_generator.generate_intervention_message(
                self.domain, intervention_level, trigger_data, user_patterns
            )
            
            return {
                'intervention_needed': True,
                'level': intervention_level,
                'message': intervention_message
            }
        
        return {'intervention_needed': False}
    
    def get_recent_triggers(self):
        """Get recent trigger data for this domain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT trigger_type, trigger_data, severity_score, timestamp
        FROM intervention_triggers
        WHERE user_id = ? AND domain = ?
        AND timestamp > datetime('now', '-48 hours')
        ORDER BY timestamp DESC LIMIT 1
        ''', (self.user_id, self.domain))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'trigger_type': result[0],
                'trigger_data': json.loads(result[1]),
                'severity': result[2],
                'timestamp': result[3]
            }
        return {}
    
    def get_predictive_insights(self):
        """Get predictive insights about likely success/failure"""
        patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 30)
        
        insights = []
        
        # Timing insights
        timing_patterns = patterns.get('timing_patterns', {})
        if 'best_commitment_times' in timing_patterns:
            best_times = timing_patterns['best_commitment_times']
            if best_times:
                best_hour = best_times[0][0]
                success_rate = best_times[0][1]['success_rate']
                insights.append(f"🕐 **Optimal timing:** You're {success_rate:.0%} more successful when committing around {best_hour}:00")
        
        # Cross-domain insights
        cross_effects = patterns.get('cross_domain_effects', {})
        for effect, data in cross_effects.items():
            if self.domain in effect and data['strength'] > 0.5:
                insights.append(f"🔗 **Domain correlation:** {effect.replace('_', ' ').title()} (strength: {data['strength']:.0%})")
        
        return insights
    
    def predict_commitment_success(self, commitment_text):
        """Predict likelihood of commitment success"""
        patterns = self.pattern_analyzer.analyze_user_patterns(self.user_id, 30)
        
        score = 0.5  # Base 50% probability
        
        # Domain completion rate
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        if self.domain in domain_patterns:
            domain_rate = domain_patterns[self.domain]['completion_rate']
            score = (score + domain_rate) / 2  # Average with historical performance
        
        # Language analysis
        commitment_lower = commitment_text.lower()
        certain_words = ['will', 'going to', 'must', 'committed to', 'definitely']
        uncertain_words = ['maybe', 'try', 'hope', 'might', 'probably']
        
        if any(word in commitment_lower for word in certain_words):
            score += 0.2
        if any(word in commitment_lower for word in uncertain_words):
            score -= 0.3
        
        return min(max(score, 0.1), 0.9)  # Keep between 10% and 90%