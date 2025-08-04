import sqlite3
from datetime import datetime, timedelta

def populate_test_data():
    """Add some test data for cross-domain analysis"""
    conn = sqlite3.connect("life_agent.db")
    cursor = conn.cursor()
    
    print("📊 Adding test data for cross-domain analysis...")
    
    # Add test user
    cursor.execute("INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)",
                   (12345, "test_user", "TestUser"))
    
    # Add sample daily checkins for different domains
    domains = ['business', 'health', 'finance', 'parenting', 'work', 'personal']
    
    for i in range(7):  # Last 7 days
        date = (datetime.now() - timedelta(days=i)).date()
        
        for domain in domains:
            # Simulate realistic completion patterns
            completed = (i + hash(domain)) % 3 != 0  # Varied completion
            
            cursor.execute('''
                INSERT OR IGNORE INTO daily_checkins 
                (user_id, date, domain, commitment, completed)
                VALUES (?, ?, ?, ?, ?)
            ''', (12345, date, domain, f"Test {domain} commitment", completed))
    
    conn.commit()
    conn.close()
    
    print("✅ Test data populated!")

if __name__ == "__main__":
    populate_test_data()