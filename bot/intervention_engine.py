from datetime import datetime, timedelta
import sqlite3
import json
from typing import Dict, List, Optional
from bot.pattern_analyzer import PatternAnalyzer

class InterventionEngine:
    """Real-time intervention and accountability system"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
        self.pattern_analyzer = PatternAnalyzer(db_path)
        self.init_intervention_tables()
    
    def init_intervention_tables(self):
        """Initialize intervention tracking tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Active interventions table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS active_interventions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        domain TEXT,
        intervention_level INTEGER, -- 1-5 escalation level
        trigger_condition TEXT,
        start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        last_escalation TIMESTAMP,
        response_received BOOLEAN DEFAULT FALSE,
        resolution_status TEXT DEFAULT 'active', -- active, resolved, escalated
        effectiveness_score REAL
        )
        ''')
        
        # Intervention triggers table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS intervention_triggers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        trigger_type TEXT, -- missed_commitment, pattern_decline, avoidance_language
        domain TEXT,
        trigger_data TEXT, -- JSON with specific details
        severity_score REAL, -- 0.0 to 1.0
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        intervention_deployed BOOLEAN DEFAULT FALSE
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def monitor_commitment_deadlines(self, user_id: int):
        """Check for missed commitment deadlines"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get today's uncompleted commitments
        cursor.execute('''
        SELECT id, domain, commitment, created_at
        FROM daily_checkins
        WHERE user_id = ? AND date = date('now') AND completed = 0
        ''', (user_id,))
        
        uncompleted = cursor.fetchall()
        conn.close()
        
        current_time = datetime.now()
        missed_deadlines = []
        
        for commitment_id, domain, commitment, created_at in uncompleted:
            created_time = datetime.fromisoformat(created_at)
            hours_since_commitment = (current_time - created_time).total_seconds() / 3600
            
            # Trigger intervention if commitment is >2 hours old and incomplete
            if hours_since_commitment > 2:
                missed_deadlines.append({
                    'commitment_id': commitment_id,
                    'domain': domain,
                    'commitment': commitment,
                    'hours_overdue': hours_since_commitment
                })
                
                self.log_trigger(user_id, 'missed_deadline', domain, {
                    'commitment': commitment,
                    'hours_overdue': hours_since_commitment
                }, min(hours_since_commitment / 24, 1.0))
        
        return missed_deadlines
    
    def detect_pattern_decline(self, user_id: int):
        """Detect declining performance patterns"""
        patterns = self.pattern_analyzer.analyze_user_patterns(user_id, 14)
        
        declining_domains = []
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        
        for domain, data in domain_patterns.items():
            completion_rate = data['completion_rate']
            trend = data['trend']
            
            # Trigger conditions
            if completion_rate < 0.3:  # Crisis level
                severity = 0.9
                trigger_type = 'crisis_completion_rate'
            elif completion_rate < 0.5 and trend == 'declining':  # Intervention level
                severity = 0.7
                trigger_type = 'declining_performance'
            elif trend == 'declining' and completion_rate < 0.7:  # Warning level
                severity = 0.5
                trigger_type = 'performance_warning'
            else:
                continue
            
            declining_domains.append({
                'domain': domain,
                'completion_rate': completion_rate,
                'trend': trend,
                'severity': severity
            })
            
            self.log_trigger(user_id, trigger_type, domain, {
                'completion_rate': completion_rate,
                'trend': trend,
                'total_commitments': data['total_commitments']
            }, severity)
        
        return declining_domains
    
    def analyze_avoidance_language(self, user_id: int, message_text: str):
        """Analyze user message for avoidance indicators"""
        avoidance_patterns = [
            (['maybe', 'might', 'possibly'], 0.3),
            (['try to', 'hope to', 'plan to'], 0.4),
            (['later', 'eventually', 'sometime'], 0.5),
            (['too tired', 'not feeling', 'overwhelmed'], 0.6),
            (['can\'t', 'impossible', 'no time'], 0.7)
        ]
        
        message_lower = message_text.lower()
        avoidance_score = 0.0
        detected_patterns = []
        
        for patterns, score in avoidance_patterns:
            if any(pattern in message_lower for pattern in patterns):
                avoidance_score = max(avoidance_score, score)
                detected_patterns.extend([p for p in patterns if p in message_lower])
        
        if avoidance_score > 0.3:
            self.log_trigger(user_id, 'avoidance_language', 'general', {
                'message': message_text,
                'detected_patterns': detected_patterns,
                'avoidance_score': avoidance_score
            }, avoidance_score)
            
            return {
                'avoidance_detected': True,
                'score': avoidance_score,
                'patterns': detected_patterns
            }
        
        return {'avoidance_detected': False}
    
    def get_intervention_level(self, user_id: int, domain: str) -> int:
        """Determine appropriate intervention level based on triggers"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get recent triggers for domain
        cursor.execute('''
        SELECT trigger_type, severity_score, timestamp
        FROM intervention_triggers
        WHERE user_id = ? AND domain = ?
        AND timestamp > datetime('now', '-24 hours')
        ORDER BY timestamp DESC
        ''', (user_id, domain))
        
        recent_triggers = cursor.fetchall()
        
        # Check for active interventions
        cursor.execute('''
        SELECT intervention_level, start_time
        FROM active_interventions
        WHERE user_id = ? AND domain = ? AND resolution_status = 'active'
        ORDER BY start_time DESC LIMIT 1
        ''', (user_id, domain))
        
        active_intervention = cursor.fetchone()
        conn.close()
        
        if not recent_triggers:
            return 0  # No intervention needed
        
        # Calculate intervention level
        max_severity = max(trigger[1] for trigger in recent_triggers)
        trigger_count = len(recent_triggers)
        
        if active_intervention:
            current_level = active_intervention[0]
            # Escalate if triggers continue
            if trigger_count > 2:
                return min(current_level + 1, 5)
            return current_level
        
        # Determine initial intervention level
        if max_severity > 0.8 or trigger_count > 3:
            return 4  # Crisis intervention
        elif max_severity > 0.6 or trigger_count > 2:
            return 3  # Firm intervention
        elif max_severity > 0.4 or trigger_count > 1:
            return 2  # Pattern alert
        else:
            return 1  # Gentle reminder
    
    def log_trigger(self, user_id: int, trigger_type: str, domain: str, trigger_data: dict, severity: float):
        """Log intervention trigger"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        INSERT INTO intervention_triggers
        (user_id, trigger_type, domain, trigger_data, severity_score)
        VALUES (?, ?, ?, ?, ?)
        ''', (user_id, trigger_type, domain, json.dumps(trigger_data), severity))
        
        conn.commit()
        conn.close()
    
    def comprehensive_intervention_check(self, user_id: int):
        """Run comprehensive intervention analysis"""
        interventions_needed = {}
        
        # Check all trigger conditions
        missed_deadlines = self.monitor_commitment_deadlines(user_id)
        declining_patterns = self.detect_pattern_decline(user_id)
        cascade_failures = self.check_cross_domain_cascade(user_id)
        
        # Determine interventions needed
        all_domains = ['business', 'health', 'finance', 'parenting', 'work', 'personal']
        
        for domain in all_domains:
            intervention_level = self.get_intervention_level(user_id, domain)
            
            if intervention_level > 0:
                interventions_needed[domain] = {
                    'level': intervention_level,
                    'triggers': self.get_domain_triggers(user_id, domain),
                    'intervention_id': self.deploy_intervention(user_id, domain, intervention_level, {})
                }
        
        return interventions_needed
    
    def check_cross_domain_cascade(self, user_id: int):
        """Detect when failure in one domain is affecting others"""
        patterns = self.pattern_analyzer.analyze_user_patterns(user_id, 7)
        cross_effects = patterns.get('cross_domain_effects', {})
        
        cascading_failures = []
        
        for effect_key, data in cross_effects.items():
            if data['strength'] > 0.6 and data.get('success_correlation', 0) < 0.3:
                # High correlation but low success rate = cascade failure
                if '_affects_' in effect_key:
                    source_domain, target_domain = effect_key.split('_affects_')
                    
                    cascading_failures.append({
                        'source_domain': source_domain,
                        'target_domain': target_domain,
                        'cascade_strength': data['strength']
                    })
                    
                    self.log_trigger(user_id, 'cascade_failure', target_domain, {
                        'source_domain': source_domain,
                        'cascade_strength': data['strength']
                    }, data['strength'])
        
        return cascading_failures
    
    def get_domain_triggers(self, user_id: int, domain: str):
        """Get recent triggers for specific domain"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT trigger_type, trigger_data, severity_score, timestamp
        FROM intervention_triggers
        WHERE user_id = ? AND domain = ?
        AND timestamp > datetime('now', '-48 hours')
        ORDER BY timestamp DESC
        ''', (user_id, domain))
        
        triggers = cursor.fetchall()
        conn.close()
        
        return [{'type': t[0], 'data': json.loads(t[1]), 'severity': t[2], 'time': t[3]}
                for t in triggers]
    
    def deploy_intervention(self, user_id: int, domain: str, intervention_level: int, trigger_data: dict):
        """Deploy intervention and track it"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Record active intervention
        cursor.execute('''
        INSERT INTO active_interventions
        (user_id, domain, intervention_level, trigger_condition)
        VALUES (?, ?, ?, ?)
        ''', (user_id, domain, intervention_level, json.dumps(trigger_data)))
        
        intervention_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return intervention_id

if __name__ == "__main__":
    engine = InterventionEngine()
    print("Intervention engine initialized!")