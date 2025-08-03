from abc import ABC, abstractmethod
from datetime import datetime
import sqlite3
from typing import Dict, List, Optional

class BaseAgent(ABC):
    """Foundation class for all life domain agents"""
    
    def __init__(self, domain_name: str, user_id: int, db_path="life_agent.db"):
        self.domain = domain_name
        self.user_id = user_id
        self.db_path = db_path
        self.personality_traits = self.get_personality_traits()
    
    @abstractmethod
    def get_personality_traits(self) -> Dict:
        """Return personality characteristics for this agent"""
        pass
    
    @abstractmethod
    def generate_daily_prompt(self) -> str:
        """Generate domain-specific daily commitment prompt"""
        pass
    
    @abstractmethod  
    def analyze_response(self, user_response: str) -> str:
        """Analyze user's response with agent personality"""
        pass
    
    @abstractmethod
    def get_intervention_message(self, pattern_data: Dict) -> str:
        """Generate intervention when patterns decline"""
        pass
    
    def log_commitment(self, commitment_text: str):
        """Log user's daily commitment to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO daily_checkins (user_id, date, domain, commitment, completed)
        VALUES (?, ?, ?, ?, ?)
        ''', (self.user_id, datetime.now().date(), self.domain, commitment_text, False))
        
        conn.commit()
        conn.close()