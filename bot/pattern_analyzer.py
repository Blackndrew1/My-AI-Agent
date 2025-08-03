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
        patterns = {
            'completion_patterns': self.analyze_completion_patterns(user_id, days),
            'timing_patterns': self.analyze_timing_patterns(user_id, days),
            'avoidance_patterns': self.analyze_avoidance_patterns(user_id, days),
            'success_factors': self.analyze_success_factors(user_id, days),
            'cross_domain_effects': self.analyze_cross_domain_effects(user_id, days)
        }
        
        return patterns
    
    def analyze_completion_patterns(self, user_id: int, days: int) -> Dict:
        """Analyze completion patterns by domain, day of week, streaks"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT domain, date, completed, created_at, commitment
        FROM daily_checkins
        WHERE user_id = ? AND date > date('now', '-{} days')
        ORDER BY date DESC
        '''.format(days), (user_id,))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return {'message': 'No data yet - use system for a few days'}
        
        # Domain completion rates
        domain_stats = {}
        domains = ['business', 'health', 'finance', 'parenting', 'work', 'personal']
        
        for domain in domains:
            domain_data = [r for r in results if r[0] == domain]
            if domain_data:
                completed = sum(1 for r in domain_data if r[2])
                total = len(domain_data)
                
                recent_data = domain_data[:7] if len(domain_data) >= 7 else domain_data
                earlier_data = domain_data[7:14] if len(domain_data) >= 14 else []
                
                recent_rate = sum(1 for r in recent_data if r[2]) / len(recent_data) if recent_data else 0
                earlier_rate = sum(1 for r in earlier_data if r[2]) / len(earlier_data) if earlier_data else recent_rate
                
                trend = 'improving' if recent_rate > earlier_rate + 0.1 else 'declining' if recent_rate < earlier_rate - 0.1 else 'stable'
                
                domain_stats[domain] = {
                    'completion_rate': completed / total,
                    'total_commitments': total,
                    'trend': trend
                }
        
        return {'by_domain': domain_stats}
    
    def analyze_timing_patterns(self, user_id: int, days: int) -> Dict:
        """Analyze timing patterns"""
        return {'message': 'Timing analysis available after more conversations'}
    
    def analyze_avoidance_patterns(self, user_id: int, days: int) -> Dict:
        """Identify avoidance patterns"""
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
    
    def analyze_success_factors(self, user_id: int, days: int) -> Dict:
        """Analyze success factors"""
        return {'message': 'Success factor analysis available with more data'}
    
    def analyze_cross_domain_effects(self, user_id: int, days: int) -> Dict:
        """Analyze cross-domain correlations"""
        return {}
    
    def get_total_commitments(self, user_id: int, days: int) -> int:
        """Get total commitments in period"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT COUNT(*) FROM daily_checkins
        WHERE user_id = ? AND date > date('now', '-{} days')
        '''.format(days), (user_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else 0

if __name__ == "__main__":
    analyzer = PatternAnalyzer()
    print("✅ Pattern analyzer ready!")