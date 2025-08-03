from datetime import datetime, timedelta
import json
import sqlite3
from typing import Dict, List, Optional

class ConversationManager:
    """Manages conversation state and context for all agents"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
        self.active_conversations = {}  # In-memory conversation state
        self.init_conversation_tables()
    
    def init_conversation_tables(self):
        """Initialize database tables for conversation tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Conversation sessions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            agent_domain TEXT,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_end TIMESTAMP,
            session_data TEXT, -- JSON data
            outcome TEXT -- committed, abandoned, intervened
        )
        ''')
        
        # Conversation messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            speaker TEXT, -- user, agent
            message_text TEXT,
            message_type TEXT, -- prompt, response, analysis, intervention
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES conversation_sessions (id)
        )
        ''')
        
        # Behavioral patterns table for pattern recognition
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS behavioral_patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            pattern_type TEXT, -- avoidance, success, energy, mood
            pattern_description TEXT,
            confidence_score REAL, -- 0.0 to 1.0
            occurrences INTEGER,
            last_occurrence TIMESTAMP,
            triggers TEXT, -- JSON array of trigger conditions
            outcomes TEXT, -- JSON array of typical outcomes
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Conversation and pattern tables initialized")
    
    def start_conversation(self, user_id: int, agent_domain: str) -> str:
        """Start new conversation session with specific agent"""
        session_id = self._create_session(user_id, agent_domain)
        
        self.active_conversations[user_id] = {
            'session_id': session_id,
            'agent_domain': agent_domain,
            'conversation_stage': 'initial_prompt',
            'messages': [],
            'context': {},
            'commitment_pending': False,
            'last_activity': datetime.now()
        }
        
        return session_id
    
    def add_message(self, user_id: int, speaker: str, message: str, message_type: str = 'response'):
        """Add message to active conversation"""
        if user_id not in self.active_conversations:
            return False
        
        conversation = self.active_conversations[user_id]
        session_id = conversation['session_id']
        
        # Add to database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO conversation_messages (session_id, speaker, message_text, message_type)
        VALUES (?, ?, ?, ?)
        ''', (session_id, speaker, message, message_type))
        conn.commit()
        conn.close()
        
        # Add to active conversation
        conversation['messages'].append({
            'speaker': speaker,
            'message': message,
            'type': message_type,
            'timestamp': datetime.now()
        })
        conversation['last_activity'] = datetime.now()
        
        return True
    
    def get_conversation_context(self, user_id: int) -> Dict:
        """Get current conversation context for user"""
        if user_id not in self.active_conversations:
            return {}
        return self.active_conversations[user_id]
    
    def get_recent_patterns(self, user_id: int, agent_domain: str, days: int = 7) -> List:
        """Get recent completion patterns for domain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT date, commitment, completed, notes
        FROM daily_checkins
        WHERE user_id = ? AND domain = ?
        AND date > date('now', '-{} days')
        ORDER BY date DESC
        '''.format(days), (user_id, agent_domain))
        
        results = cursor.fetchall()
        conn.close()
        return results
    
    def analyze_cross_domain_patterns(self, user_id: int) -> Dict:
        """Analyze patterns across all life domains"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get completion rates by domain
        cursor.execute('''
        SELECT domain,
        COUNT(*) as total_commitments,
        SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_commitments,
        AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as completion_rate
        FROM daily_checkins
        WHERE user_id = ? AND date > date('now', '-14 days')
        GROUP BY domain
        ''', (user_id,))
        
        domain_stats = cursor.fetchall()
        conn.close()
        
        patterns = {}
        for domain, total, completed, rate in domain_stats:
            patterns[domain] = {
                'total_commitments': total,
                'completed_commitments': completed,
                'completion_rate': rate,
                'trend': 'improving' if rate > 0.7 else 'concerning' if rate < 0.4 else 'stable'
            }
        
        return patterns
    
    def get_pattern_insights(self, user_id: int, domain: str) -> List[str]:
        """Get behavioral insights for specific domain"""
        patterns = self.analyze_cross_domain_patterns(user_id)
        insights = []
        
        if domain == 'business':
            if 'health' in patterns and patterns['health']['completion_rate'] < 0.5:
                insights.append("⚡ **Energy Pattern:** Low health consistency typically reduces business performance by 40%")
            if 'finance' in patterns and patterns['finance']['completion_rate'] < 0.5:
                insights.append("💳 **Financial Stress:** Money concerns may be reducing business risk-taking")
        
        elif domain == 'health':
            if 'business' in patterns and patterns['business']['completion_rate'] < 0.5:
                insights.append("📈 **Avoidance Correlation:** Business procrastination often correlates with skipped workouts")
            if 'personal' in patterns and patterns['personal']['completion_rate'] > 0.8:
                insights.append("🎮 **Balance Alert:** High leisure time may indicate avoidance of physical challenges")
        
        return insights
    
    def predict_success_likelihood(self, user_id: int, domain: str, commitment_text: str) -> float:
        """Predict likelihood of commitment completion based on patterns"""
        patterns = self.get_recent_patterns(user_id, domain, 14)
        if not patterns:
            return 0.5  # Default 50% if no history
        
        # Calculate base success rate
        completed = sum(1 for p in patterns if p[2])  # p[2] is completed column
        base_rate = completed / len(patterns)
        
        # Adjust based on commitment language
        commitment_lower = commitment_text.lower()
        
        # Negative indicators
        if any(word in commitment_lower for word in ['maybe', 'try', 'hope', 'might']):
            base_rate *= 0.7
        
        # Positive indicators  
        if any(word in commitment_lower for word in ['will', 'committed', 'definitely']):
            base_rate *= 1.2
        
        # Specific action indicators
        if any(word in commitment_lower for word in ['at', 'by', 'before', 'during']):
            base_rate *= 1.1
        
        return min(max(base_rate, 0.1), 0.9)  # Keep between 10% and 90%
    
    def end_conversation(self, user_id: int, outcome: str = 'completed'):
        """End active conversation session"""
        if user_id not in self.active_conversations:
            return
        
        conversation = self.active_conversations[user_id]
        session_id = conversation['session_id']
        
        # Update session in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE conversation_sessions
        SET session_end = CURRENT_TIMESTAMP,
            outcome = ?,
            session_data = ?
        WHERE id = ?
        ''', (outcome, json.dumps(conversation['context']), session_id))
        conn.commit()
        conn.close()
        
        # Remove from active conversations
        del self.active_conversations[user_id]
    
    def _create_session(self, user_id: int, agent_domain: str) -> str:
        """Create new conversation session in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO conversation_sessions (user_id, agent_domain)
        VALUES (?, ?)
        ''', (user_id, agent_domain))
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return session_id

if __name__ == "__main__":
    # Test the conversation manager
    manager = ConversationManager()
    print("Conversation Manager initialized and ready!")