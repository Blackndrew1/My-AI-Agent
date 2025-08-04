import sqlite3

def fix_missing_tables():
    """Add missing tables to existing database"""
    conn = sqlite3.connect("life_agent.db")
    cursor = conn.cursor()
    
    print("🔧 Adding missing database tables...")
    
    # Add work_tasks table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS work_tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        task_name TEXT,
        task_category TEXT,
        original_duration INTEGER,
        automated_duration INTEGER,
        automation_method TEXT,
        frequency_per_week INTEGER,
        automation_date DATE,
        time_saved_weekly INTEGER,
        automation_status TEXT
    )
    ''')
    
    # Add automation_templates table  
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS automation_templates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        template_name TEXT,
        template_category TEXT,
        template_content TEXT,
        usage_count INTEGER DEFAULT 0,
        effectiveness_score REAL DEFAULT 0.0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_used TIMESTAMP
    )
    ''')
    
    # Add work_efficiency_metrics table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS work_efficiency_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        date DATE,
        total_work_minutes INTEGER,
        automated_minutes INTEGER,
        manual_minutes INTEGER,
        efficiency_score REAL,
        tasks_automated INTEGER,
        new_automations_implemented INTEGER
    )
    ''')
    
    conn.commit()
    conn.close()
    
    print("✅ Database tables fixed!")

if __name__ == "__main__":
    fix_missing_tables()