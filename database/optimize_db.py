import sqlite3
from datetime import datetime

class DatabaseOptimizer:
    """Optimize database for production-level performance"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
    
    def optimize_database(self):
        """Apply comprehensive database optimizations"""
        print("🔧 Starting database optimization...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Enable performance optimizations
        print("⚡ Enabling performance optimizations...")
        cursor.execute("PRAGMA journal_mode = WAL;")
        cursor.execute("PRAGMA synchronous = NORMAL;")
        cursor.execute("PRAGMA cache_size = 10000;")
        cursor.execute("PRAGMA temp_store = memory;")
        cursor.execute("PRAGMA mmap_size = 268435456;")  # 256MB
        
        # Create performance indexes
        print("📊 Creating performance indexes...")
        
        indexes = [
            "CREATE INDEX IF NOT EXISTS idx_checkins_user_date ON daily_checkins(user_id, date);",
            "CREATE INDEX IF NOT EXISTS idx_checkins_domain ON daily_checkins(domain);",
            "CREATE INDEX IF NOT EXISTS idx_checkins_completed ON daily_checkins(completed);",
            "CREATE INDEX IF NOT EXISTS idx_checkins_date_range ON daily_checkins(date);",
            "CREATE INDEX IF NOT EXISTS idx_conversation_user ON conversation_sessions(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_conversation_agent ON conversation_sessions(agent_domain);",
            "CREATE INDEX IF NOT EXISTS idx_messages_session ON conversation_messages(session_id);",
            "CREATE INDEX IF NOT EXISTS idx_patterns_user ON behavioral_patterns(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_patterns_type ON behavioral_patterns(pattern_type);",
            "CREATE INDEX IF NOT EXISTS idx_interventions_user ON active_interventions(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_interventions_domain ON active_interventions(domain);",
            "CREATE INDEX IF NOT EXISTS idx_triggers_user_domain ON intervention_triggers(user_id, domain);",
            "CREATE INDEX IF NOT EXISTS idx_work_tasks_user ON work_automation_tasks(user_id);",
            "CREATE INDEX IF NOT EXISTS idx_work_tasks_status ON work_automation_tasks(automation_status);"
        ]
        
        for index in indexes:
            try:
                cursor.execute(index)
                print(f"  ✅ Created index: {index.split('idx_')[1].split(' ')[0]}")
            except sqlite3.Error as e:
                print(f"  ⚠️ Index creation warning: {e}")
        
        # Analyze database for query optimization
        print("🔍 Analyzing database for query optimization...")
        cursor.execute("ANALYZE;")
        
        # Vacuum database to reclaim space and optimize
        print("🧹 Optimizing database structure...")
        cursor.execute("VACUUM;")
        
        # Get database statistics
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table';")
        table_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='index';")
        index_count = cursor.fetchone()[0]
        
        cursor.execute("PRAGMA page_count;")
        page_count = cursor.fetchone()[0]
        
        cursor.execute("PRAGMA page_size;")
        page_size = cursor.fetchone()[0]
        
        db_size_mb = (page_count * page_size) / (1024 * 1024)
        
        conn.commit()
        conn.close()
        
        print("\n📈 Database Optimization Complete!")
        print(f"  • Tables: {table_count}")
        print(f"  • Indexes: {index_count}")
        print(f"  • Database size: {db_size_mb:.2f} MB")
        print(f"  • WAL mode enabled for better concurrency")
        print(f"  • Memory cache: 10,000 pages")
        print(f"  • Memory-mapped I/O: 256 MB")
        
        return {
            'table_count': table_count,
            'index_count': index_count,
            'database_size_mb': db_size_mb,
            'optimization_complete': True
        }
    
    def verify_performance(self):
        """Verify database performance optimizations"""
        print("\n🎯 Verifying database performance...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Test query performance
        start_time = datetime.now()
        cursor.execute("""
        SELECT COUNT(*) FROM daily_checkins 
        WHERE user_id = 12345 AND date > date('now', '-30 days')
        """)
        result = cursor.fetchone()[0]
        query_time = (datetime.now() - start_time).total_seconds()
        
        # Check WAL mode
        cursor.execute("PRAGMA journal_mode;")
        journal_mode = cursor.fetchone()[0]
        
        # Check cache size
        cursor.execute("PRAGMA cache_size;")
        cache_size = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"  ✅ Query performance: {query_time:.3f} seconds")
        print(f"  ✅ Journal mode: {journal_mode}")
        print(f"  ✅ Cache size: {cache_size:,} pages")
        print(f"  ✅ Sample query returned {result} records")
        
        performance_good = query_time < 0.1 and journal_mode == 'wal'
        
        if performance_good:
            print("  🚀 Database performance is EXCELLENT!")
        else:
            print("  ⚠️ Database performance needs attention")
        
        return performance_good

if __name__ == "__main__":
    optimizer = DatabaseOptimizer()
    
    # Run optimization
    results = optimizer.optimize_database()
    
    # Verify performance
    performance_ok = optimizer.verify_performance()
    
    if performance_ok:
        print("\n🎉 Database optimization SUCCESSFUL!")
    else:
        print("\n❌ Database optimization needs review")