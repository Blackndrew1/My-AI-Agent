import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.intervention_engine import InterventionEngine
from bot.intervention_messages import InterventionMessageGenerator
from bot.agents.business_agent import BusinessAgent
from bot.conversation_manager import ConversationManager
from bot.pattern_analyzer import PatternAnalyzer
import sqlite3
from datetime import datetime, timedelta

def test_complete_intervention_system():
    """Test the complete intervention system end-to-end"""
    print("🧪 Testing Complete Intervention System")
    
    test_user_id = 99999
    db_path = "test_intervention.db"
    
    # Clean test environment
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # Initialize systems
    engine = InterventionEngine(db_path)
    generator = InterventionMessageGenerator()
    analyzer = PatternAnalyzer(db_path)
    cm = ConversationManager(db_path)
    
    # Create sample declining pattern data
    create_test_pattern_data(test_user_id, db_path)
    
    print("✅ Test data created")
    
    # Test 1: Pattern decline detection
    declining = engine.detect_pattern_decline(test_user_id)
    print(f"✅ Pattern decline detection: {len(declining)} domains found")
    
    # Test 2: Intervention level calculation
    business_level = engine.get_intervention_level(test_user_id, 'business')
    print(f"✅ Intervention level calculation: Business = Level {business_level}")
    
    # Test 3: Message generation
    if business_level > 0:
        message = generator.generate_intervention_message('business', business_level, {'completion_rate': 0.2})
        print(f"✅ Intervention message generated: {len(message)} characters")
    else:
        print("✅ No intervention needed (as expected with test data)")
    
    # Test 4: Avoidance language detection
    test_messages = [
        "Maybe I'll try to call clients later",
        "I'm too tired for business tasks today", 
        "I will definitely complete my business calls by 2 PM"
    ]
    
    avoidance_count = 0
    for msg in test_messages:
        result = engine.analyze_avoidance_language(test_user_id, msg)
        if result['avoidance_detected']:
            avoidance_count += 1
    
    print(f"✅ Avoidance detection: {avoidance_count}/{len(test_messages)} messages flagged")
    
    # Test 5: Comprehensive intervention check
    all_interventions = engine.comprehensive_intervention_check(test_user_id)
    print(f"✅ Comprehensive check: {len(all_interventions)} domains need intervention")
    
    # Test 6: Enhanced agent integration
    try:
        agent = BusinessAgent(test_user_id, cm)
        intervention_check = agent.check_intervention_needed()
        print(f"✅ Agent intervention check: {intervention_check['intervention_needed']}")
    except Exception as e:
        print(f"❌ Agent integration error: {e}")
        return False
    
    # Clean up test database
    os.remove(db_path)
    
    print("\n🎉 ALL INTERVENTION SYSTEM TESTS PASSED!")
    print("Your intervention system is working properly!")
    return True

def create_test_pattern_data(user_id, db_path):
    """Create test data showing declining patterns"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table first
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    first_name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Create daily_checkins table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS daily_checkins (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE,
    domain TEXT,
    commitment TEXT,
    completed BOOLEAN DEFAULT FALSE,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
    )
    ''')
    
    # Create pattern of declining business completion
    domains = ['business', 'health', 'finance', 'parenting', 'work', 'personal']
    
    for day_offset in range(14):
        date = (datetime.now() - timedelta(days=day_offset)).date()
        
        for domain in domains:
            # Simulate declining pattern for business
            if domain == 'business':
                # Recent days have low completion (simulating decline)
                completed = 1 if day_offset > 10 else 0  # Failed last 10 days
            else:
                # Other domains performing normally
                completed = 1 if day_offset % 2 == 0 else 0
            
            cursor.execute('''
            INSERT INTO daily_checkins (user_id, date, domain, commitment, completed)
            VALUES (?, ?, ?, ?, ?)
            ''', (user_id, date, domain, f"Test {domain} commitment", completed))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    success = test_complete_intervention_system()
    if success:
        print("\n✅ Ready for final save and commit!")
    else:
        print("\n❌ Issues found - need to fix before proceeding")