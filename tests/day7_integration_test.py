import asyncio
import sqlite3
import sys
import os
from datetime import datetime, timedelta
import json

# Add project root to path
sys.path.append('.')

class Day7IntegrationTest:
    """Comprehensive integration testing for complete AI agent system"""
    
    def __init__(self):
        self.test_user_id = 12345
        self.test_results = {}
        self.db_path = "life_agent.db"
        
    def run_all_tests(self):
        """Run complete integration test suite"""
        print("🧪 Day 7 Integration Test Suite Starting...")
        print("=" * 60)
        
        tests = [
            ("Database Connection", self.test_database_connection),
            ("Agent Architecture", self.test_agent_architecture),
            ("Conversation System", self.test_conversation_system),
            ("Pattern Analysis", self.test_pattern_analysis),
            ("Intervention Engine", self.test_intervention_engine),
            ("Work Automation", self.test_work_automation),
            ("Cross-Domain Intelligence", self.test_cross_domain_intelligence),
            ("Performance Metrics", self.test_performance_metrics),
        ]
        
        for test_name, test_func in tests:
            print(f"\n🔍 Testing: {test_name}")
            try:
                result = test_func()
                self.test_results[test_name] = "PASS" if result else "FAIL"
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"   {status}")
            except Exception as e:
                self.test_results[test_name] = f"ERROR: {str(e)}"
                print(f"   ❌ ERROR: {str(e)}")
        
        self.print_test_summary()
        return self.test_results
    
    def test_database_connection(self):
        """Test database connectivity and basic operations"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Test table existence
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            required_tables = [
                'users', 'daily_checkins', 'conversation_sessions', 
                'conversation_messages', 'behavioral_patterns', 
                'work_tasks', 'intervention_triggers'
            ]
            
            missing_tables = [t for t in required_tables if t not in tables]
            if missing_tables:
                print(f"   Missing tables: {missing_tables}")
                return False
            
            # Test data insertion
            cursor.execute("""
                INSERT OR REPLACE INTO users (user_id, username, first_name)
                VALUES (?, ?, ?)
            """, (self.test_user_id, "test_user", "TestUser"))
            
            conn.commit()
            conn.close()
            print(f"   Database has {len(tables)} tables, all required tables present")
            return True
            
        except Exception as e:
            print(f"   Database test failed: {e}")
            return False
    
    def test_agent_architecture(self):
        """Test that all 6 agents are properly implemented"""
        try:
            # Import all agent modules
            from bot.agents.business_agent import BusinessAgent
            from bot.agents.health_agent import HealthAgent
            from bot.agents.finance_agent import FinanceAgent
            from bot.agents.parenting_agent import ParentingAgent
            from bot.agents.work_agent import WorkAgent
            from bot.agents.personal_agent import PersonalAgent
            
            agents = {
                'business': BusinessAgent,
                'health': HealthAgent,
                'finance': FinanceAgent,
                'parenting': ParentingAgent,
                'work': WorkAgent,
                'personal': PersonalAgent
            }
            
            # Test each agent can be instantiated and has required methods
            for domain, agent_class in agents.items():
                agent = agent_class(self.test_user_id)
                
                # Check required methods exist
                required_methods = [
                    'generate_daily_prompt', 
                    'analyze_response', 
                    'get_personality_traits'
                ]
                
                for method in required_methods:
                    if not hasattr(agent, method):
                        print(f"   {domain} agent missing method: {method}")
                        return False
                
                # Test basic functionality
                prompt = agent.generate_daily_prompt()
                if not prompt or len(prompt) < 10:
                    print(f"   {domain} agent prompt too short: {len(prompt)}")
                    return False
            
            print(f"   All 6 agents properly implemented with required methods")
            return True
            
        except ImportError as e:
            print(f"   Agent import failed: {e}")
            return False
        except Exception as e:
            print(f"   Agent architecture test failed: {e}")
            return False
    
    def test_conversation_system(self):
        """Test conversation management and state retention"""
        try:
            from bot.conversation_manager import ConversationManager
            
            conv_manager = ConversationManager(self.db_path)
            
            # Test conversation creation
            session_id = conv_manager.start_conversation(self.test_user_id, "business")
            if not session_id:
                print("   Failed to create conversation session")
                return False
            
            # Test message addition
            success = conv_manager.add_message(
                self.test_user_id, "user", "Test message", "response"
            )
            if not success:
                print("   Failed to add message to conversation")
                return False
            
            # Test context retrieval
            context = conv_manager.get_conversation_context(self.test_user_id)
            if not context or 'session_id' not in context:
                print("   Failed to retrieve conversation context")
                return False
            
            # Test conversation ending
            conv_manager.end_conversation(self.test_user_id, "completed")
            
            print("   Conversation system working: create, message, context, end")
            return True
            
        except Exception as e:
            print(f"   Conversation system test failed: {e}")
            return False
    
    def test_pattern_analysis(self):
        """Test behavioral pattern recognition system"""
        try:
            from bot.pattern_analyzer import PatternAnalyzer
            
            analyzer = PatternAnalyzer(self.db_path)
            
            # Add some test data first
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Insert test checkins for pattern analysis
            test_data = [
                (self.test_user_id, '2024-01-01', 'business', 'Call 3 clients', True),
                (self.test_user_id, '2024-01-02', 'business', 'Write proposal', False),
                (self.test_user_id, '2024-01-03', 'health', 'Morning workout', True),
                (self.test_user_id, '2024-01-04', 'health', 'Gym session', True),
            ]
            
            for data in test_data:
                cursor.execute("""
                    INSERT OR REPLACE INTO daily_checkins 
                    (user_id, date, domain, commitment, completed)
                    VALUES (?, ?, ?, ?, ?)
                """, data)
            
            conn.commit()
            conn.close()
            
            # Test pattern analysis
            patterns = analyzer.analyze_user_patterns(self.test_user_id, 30)
            
            required_pattern_types = [
                'completion_patterns', 'timing_patterns', 
                'avoidance_patterns', 'success_factors'
            ]
            
            for pattern_type in required_pattern_types:
                if pattern_type not in patterns:
                    print(f"   Missing pattern type: {pattern_type}")
                    return False
            
            print("   Pattern analysis working: completion, timing, avoidance, success")
            return True
            
        except Exception as e:
            print(f"   Pattern analysis test failed: {e}")
            return False
    
    def test_intervention_engine(self):
        """Test automated intervention system"""
        try:
            from bot.intervention_engine import InterventionEngine
            
            engine = InterventionEngine(self.db_path)
            
            # Test intervention level calculation  
            level = engine.get_intervention_level(self.test_user_id, "business")
            if not isinstance(level, int) or level < 0 or level > 5:
                print(f"   Invalid intervention level: {level}")
                return False
            
            # Test trigger detection
            triggers = engine.monitor_commitment_deadlines(self.test_user_id)
            if not isinstance(triggers, list):
                print("   Intervention triggers not returning list")
                return False
            
            # Test avoidance language detection
            result = engine.analyze_avoidance_language(
                self.test_user_id, "Maybe I'll try to call clients later"
            )
            if not isinstance(result, dict) or 'avoidance_detected' not in result:
                print("   Avoidance language detection not working")
                return False
            
            print("   Intervention engine working: levels, triggers, avoidance detection")
            return True
            
        except Exception as e:
            print(f"   Intervention engine test failed: {e}")
            return False
    
    def test_work_automation(self):
        """Test work automation systems"""
        try:
            # Test if work automation modules exist and are importable
            work_modules = [
                'work_automation.email_automation',
                'work_automation.report_automation', 
                'work_automation.automation_architecture'
            ]
            
            for module_name in work_modules:
                try:
                    __import__(module_name)
                except ImportError:
                    print(f"   Work automation module missing: {module_name}")
                    return False
            
            # Test work automation database tables
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%work%'")
            work_tables = [row[0] for row in cursor.fetchall()]
            
            if not work_tables:
                print("   No work automation tables found")
                return False
            
            conn.close()
            
            print(f"   Work automation working: {len(work_modules)} modules, {len(work_tables)} tables")
            return True
            
        except Exception as e:
            print(f"   Work automation test failed: {e}")
            return False
    
    def test_cross_domain_intelligence(self):
        """Test cross-domain insights and coordination"""
        try:
            from bot.conversation_manager import ConversationManager
            
            conv_manager = ConversationManager(self.db_path)
            
            # Test cross-domain pattern analysis
            patterns = conv_manager.analyze_cross_domain_patterns(self.test_user_id)
            
            if not isinstance(patterns, dict):
                print("   Cross-domain patterns not returning dictionary")
                return False
            
            # Should have data for multiple domains
            domains = ['business', 'health', 'finance', 'parenting', 'work', 'personal']
            found_domains = [d for d in domains if d in patterns]
            
            if len(found_domains) < 2:
                print(f"   Insufficient cross-domain data: {len(found_domains)} domains")
                return False
            
            print(f"   Cross-domain intelligence working: {len(found_domains)} domains analyzed")
            return True
            
        except Exception as e:
            print(f"   Cross-domain intelligence test failed: {e}")
            return False
    
    def test_performance_metrics(self):
        """Test system performance and response times"""
        try:
            import time
            from bot.pattern_analyzer import PatternAnalyzer
            
            analyzer = PatternAnalyzer(self.db_path)
            
            # Test pattern analysis performance
            start_time = time.time()
            patterns = analyzer.analyze_user_patterns(self.test_user_id, 30)
            analysis_time = time.time() - start_time
            
            if analysis_time > 5.0:  # Should complete in under 5 seconds
                print(f"   Pattern analysis too slow: {analysis_time:.2f}s")
                return False
            
            # Test database query performance
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            start_time = time.time()
            cursor.execute("SELECT COUNT(*) FROM daily_checkins WHERE user_id = ?", (self.test_user_id,))
            result = cursor.fetchone()
            query_time = time.time() - start_time
            
            conn.close()
            
            if query_time > 1.0:  # Should complete in under 1 second
                print(f"   Database query too slow: {query_time:.2f}s")
                return False
            
            print(f"   Performance good: analysis {analysis_time:.2f}s, query {query_time:.3f}s")
            return True
            
        except Exception as e:
            print(f"   Performance test failed: {e}")
            return False
    
    def print_test_summary(self):
        """Print comprehensive test results summary"""
        print("\n" + "=" * 60)
        print("🏁 DAY 7 INTEGRATION TEST RESULTS")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results.values() if result == "PASS")
        total = len(self.test_results)
        
        for test_name, result in self.test_results.items():
            status_emoji = "✅" if result == "PASS" else "❌"
            print(f"{status_emoji} {test_name}: {result}")
        
        print(f"\n📊 OVERALL: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 ALL SYSTEMS OPERATIONAL - Ready for Day 7 completion!")
        else:
            print("⚠️  Some systems need attention before Day 7 completion")
        
        return passed == total

if __name__ == "__main__":
    tester = Day7IntegrationTest()
    success = tester.run_all_tests()
    
    if success:
        print("\n✅ System ready for Day 7 integration and optimization!")
    else:
        print("\n❌ Please address failing tests before proceeding")
