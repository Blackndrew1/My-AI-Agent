import sqlite3
from datetime import datetime, timedelta

class AdvancedDatabaseManager:
    """Enhanced database with pattern recognition capabilities"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
        self.init_advanced_tables()
    
    def init_advanced_tables(self):
        """Initialize advanced tables for pattern analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Daily metrics table (for tracking foundational data)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date DATE,
                sleep_quality INTEGER,  -- 1-10 scale
                energy_level INTEGER,   -- 1-10 scale
                stress_level INTEGER,   -- 1-10 scale
                mood_rating INTEGER,    -- 1-10 scale
                external_factors TEXT,  -- JSON: weather, events, etc.
                overall_performance REAL,  -- calculated score
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Performance correlations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_correlations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                factor_1 TEXT,  -- domain or metric
                factor_2 TEXT,  -- domain or metric
                correlation_strength REAL,  -- -1.0 to 1.0
                sample_size INTEGER,
                last_calculated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Success prediction table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS success_predictions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                domain TEXT,
                prediction_date DATE,
                predicted_success_rate REAL,  -- 0.0 to 1.0
                actual_success_rate REAL,  -- filled in later for accuracy tracking
                factors_considered TEXT,  -- JSON array
                confidence_level REAL,  -- 0.0 to 1.0
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        print("✅ Advanced database schema initialized")

if __name__ == "__main__":
    db = AdvancedDatabaseManager()
    print("Advanced database schema complete!")