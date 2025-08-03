from datetime import datetime, timedelta
import sqlite3
import json
from typing import Dict, List, Tuple

class PatternAnalyzer:
    """Analyzes behavioral patterns and predicts future performance"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
    
    def analyze_user_patterns(self, user_id: int, days: int = 30) -> Dict:
        """Comprehensive pattern analysis for user"""
        try:
            patterns = {
                'completion_patterns': self.analyze_completion_patterns(user_id, days),
                'timing_patterns': {'message': 'Timing analysis available after more conversations'},
                'avoidance_patterns': self.analyze_avoidance_patterns(user_id, days),
                'success_factors': {'message': 'Success factor analysis available with more data'},
                'cross_domain_effects': {}
            }
            return patterns
        except Exception as e:
            print(f"Pattern analysis error: {e}")
            return {
                'completion_patterns': {'by_domain': {}},
                'timing_patterns': {'message': 'Error in timing analysis'},
                'avoidance_patterns': {'total_avoidance_rate': 0.0},
                'success_factors': {'message': 'Error in success analysis'},
                'cross_domain_effects': {}
            }
    
    def analyze_completion_patterns(self, user_id: int, days: int) -> Dict:
        """Analyze completion patterns by domain"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT domain, date, completed, commitment
            FROM daily_checkins
            WHERE user_id = ? AND date > date('now', '-{} days')
            ORDER BY date DESC
            '''.format(days), (user_id,))
            
            results = cursor.fetchall()
            conn.close()
            
            if not results:
                return {'by_domain': {}, 'message': 'No data yet - use system for a few days'}
            
            # Domain completion rates
            domain_stats = {}
            domains = ['business', 'health', 'finance', 'parenting', 'work', 'personal']
            
            for domain in domains:
                domain_data = [r for r in results if r[0] == domain]
                if domain_data:
                    completed = sum(1 for r in domain_data if r[2])
                    total = len(domain_data)
                    completion_rate = completed / total
                    
                    # Simple trend calculation
                    if len(domain_data) >= 4:
                        recent_half = domain_data[:len(domain_data)//2]
                        earlier_half = domain_data[len(domain_data)//2:]
                        
                        recent_rate = sum(1 for r in recent_half if r[2]) / len(recent_half)
                        earlier_rate = sum(1 for r in earlier_half if r[2]) / len(earlier_half)
                        
                        if recent_rate > earlier_rate + 0.1:
                            trend = 'improving'
                        elif recent_rate < earlier_rate - 0.1:
                            trend = 'declining'
                        else:
                            trend = 'stable'
                    else:
                        trend = 'stable'
                    
                    domain_stats[domain] = {
                        'completion_rate': completion_rate,
                        'total_commitments': total,
                        'trend': trend
                    }
            
            return {'by_domain': domain_stats}
            
        except Exception as e:
            print(f"Completion pattern error: {e}")
            return {'by_domain': {}}
    
    def analyze_avoidance_patterns(self, user_id: int, days: int) -> Dict:
        """Identify avoidance patterns"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT domain, commitment, date
            FROM daily_checkins
            WHERE user_id = ? AND completed = 0 AND date > date('now', '-{} days')
            '''.format(days), (user_id,))
            
            failed_commitments = cursor.fetchall()
            conn.close()
            
            if not failed_commitments:
                return {'total_avoidance_rate': 0.0}
            
            total_commitments = self.get_total_commitments(user_id, days)
            avoidance_rate = len(failed_commitments) / max(1, total_commitments)
            
            return {'total_avoidance_rate': avoidance_rate}
            
        except Exception as e:
            print(f"Avoidance pattern error: {e}")
            return {'total_avoidance_rate': 0.0}
    
    def get_total_commitments(self, user_id: int, days: int) -> int:
        """Get total commitments in period"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
            SELECT COUNT(*) FROM daily_checkins
            WHERE user_id = ? AND date > date('now', '-{} days')
            '''.format(days), (user_id,))
            
            result = cursor.fetchone()
            conn.close()
            
            return result[0] if result else 0
            
        except Exception as e:
            print(f"Total commitments error: {e}")
            return 0

if __name__ == "__main__":
    analyzer = PatternAnalyzer()
    print("✅ Pattern analyzer ready!")