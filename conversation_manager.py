from datetime import datetime, timedelta
import json
import sqlite3
from typing import Dict, List, Optional

class ConversationManager:
    """Manages conversation state and context for all agents"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
        self.active_conversations = {}
        self.init_conversation_tables()
    
    def init_conversation_tables(self):
        """Initialize database tables for conversation tracking"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            agent_domain TEXT,
            session_start TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            session_end TIMESTAMP,
            session_data TEXT,
            outcome TEXT
        )
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversation_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id INTEGER,
            speaker TEXT,
            message_text TEXT,
            message_type TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (session_id) REFERENCES conversation_sessions (id)
        )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Conversation tables initialized")
    
    def start_conversation(self, user_id: int, agent_domain: str) -> str:
        session_id = self._create_session(user_id, agent_domain)
        self.active_conversations[user_id] = {
            'session_id': session_id,
            'agent_domain': agent_domain,
            'messages': []
        }
        return session_id
    
    def _create_session(self, user_id: int, agent_domain: str) -> str:
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
    manager = ConversationManager()
    print("Conversation Manager ready!")