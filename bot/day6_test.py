#!/usr/bin/env python3
"""
Day 6 System Test - Simple Version
"""

import os
import sys
import sqlite3

def main():
    print("🚀 DAY 6 SYSTEM TEST")
    print("=" * 40)
    
    # Test 1: Check directories exist
    print("\n📁 Test 1: Project Structure")
    required_dirs = ['bot', 'database', 'work_automation', 'tests', 'docs']
    structure_ok = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"   ✅ {dir_name}/ directory exists")
        else:
            print(f"   ❌ {dir_name}/ directory missing")
            structure_ok = False
    
    # Test 2: Check database
    print("\n💾 Test 2: Database")
    if os.path.exists('life_agent.db'):
        db_size = os.path.getsize('life_agent.db')
        print(f"   ✅ Database exists ({db_size:,} bytes)")
        
        # Check tables
        try:
            conn = sqlite3.connect('life_agent.db')
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            print(f"   ✅ Found {len(tables)} tables: {', '.join(tables[:3])}...")
            conn.close()
        except Exception as e:
            print(f"   ⚠️ Database error: {e}")
    else:
        print("   ❌ Database file missing")
    
    # Test 3: Check environment file
    print("\n🔑 Test 3: Environment")
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'TELEGRAM_BOT_TOKEN' in content:
                print("   ✅ Telegram token configured")
            if 'OPENAI_API_KEY' in content:
                print("   ✅ OpenAI key configured")
    else:
        print("   ❌ .env file missing")
    
    # Test 4: Check key files in bot directory
    print("\n🤖 Test 4: Bot Components")
    bot_files = ['main.py', 'agents']
    for item in bot_files:
        path = os.path.join('bot', item)
        if os.path.exists(path):
            print(f"   ✅ bot/{item} exists")
        else:
            print(f"   ❌ bot/{item} missing")
    
    # Test 5: Check work automation
    print("\n⚙️ Test 5: Work Automation")
    work_files = ['email_automation.py', 'report_automation.py']
    for file in work_files:
        path = os.path.join('work_automation', file)
        if os.path.exists(path):
            print(f"   ✅ work_automation/{file} exists")
        else:
            print(f"   ❌ work_automation/{file} missing")
    
    # Summary
    print("\n" + "=" * 40)
    print("📊 SUMMARY")
    
    if structure_ok and os.path.exists('life_agent.db') and os.path.exists('.env'):
        print("🎉 SYSTEM LOOKS GOOD! Ready for Day 7")
        return True
    else:
        print("⚠️ Some components need attention")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\nTest result: {'PASS' if success else 'NEEDS WORK'}")