# Add to BaseAgent class
from bot.intervention_engine import InterventionEngine
from bot.intervention_messages import InterventionMessageGenerator

class BaseAgent(ABC):
    def __init__(self, domain_name, user_id, conversation_manager, db_path="life_agent.db"):
        self.domain = domain_name
        self.user_id = user_id
        self.conversation_manager = conversation_manager
        self.db_path = db_path
        self.personality_traits = self.get_personality_traits()
        self.pattern_analyzer = PatternAnalyzer(db_path)
        self.intervention_engine = InterventionEngine(db_path)
        self.intervention_generator = InterventionMessageGenerator()
    
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