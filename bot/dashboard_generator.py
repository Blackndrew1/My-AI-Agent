from datetime import datetime, timedelta
import sqlite3
from typing import Dict, List
import json

class LifeDashboardGenerator:
    """Generate comprehensive life optimization dashboard"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
    
    def generate_comprehensive_dashboard(self, user_id: int) -> str:
        """Generate complete life optimization dashboard"""
        
        # Get all dashboard components
        performance_summary = self.get_performance_summary(user_id)
        domain_analysis = self.get_domain_analysis(user_id)
        pattern_insights = self.get_pattern_insights(user_id)
        productivity_metrics = self.get_productivity_metrics(user_id)
        intervention_status = self.get_intervention_status(user_id)
        optimization_recommendations = self.get_optimization_recommendations(user_id)
        
        dashboard = f"""
📊 **COMPREHENSIVE LIFE OPTIMIZATION DASHBOARD**

{performance_summary}

{domain_analysis}

{pattern_insights}

{productivity_metrics}

{intervention_status}

{optimization_recommendations}

---
*Dashboard generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}*
*AI Life Agent System - Professional Edition*
"""
        
        return dashboard
    
    def get_performance_summary(self, user_id: int) -> str:
        """Generate overall performance summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get 30-day performance data
        cursor.execute("""
        SELECT 
            domain,
            COUNT(*) as total_commitments,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed_commitments,
            AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as completion_rate
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-30 days')
        GROUP BY domain
        """, (user_id,))
        
        domain_data = cursor.fetchall()
        
        if not domain_data:
            conn.close()
            return "**📈 PERFORMANCE SUMMARY**\n*Insufficient data - complete daily check-ins to generate insights*"
        
        # Calculate overall metrics
        total_commitments = sum(row[1] for row in domain_data)
        total_completed = sum(row[2] for row in domain_data)
        overall_rate = total_completed / total_commitments if total_commitments > 0 else 0
        
        # Find best and worst performing domains
        best_domain = max(domain_data, key=lambda x: x[3])
        worst_domain = min(domain_data, key=lambda x: x[3])
        
        # Get 7-day trend
        cursor.execute("""
        SELECT AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as week_rate
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-7 days')
        """, (user_id,))
        
        week_rate = cursor.fetchone()[0] or 0
        trend = "📈 Improving" if week_rate > overall_rate else "📉 Declining" if week_rate < overall_rate else "➡️ Stable"
        
        conn.close()
        
        return f"""
**📈 PERFORMANCE SUMMARY (30 Days)**

**🎯 Overall Completion Rate:** {overall_rate:.1%}
**📊 Total Commitments:** {total_commitments}
**✅ Successfully Completed:** {total_completed}
**📈 7-Day Trend:** {trend}

**🏆 Best Performing:** {best_domain[0].title()} ({best_domain[3]:.1%})
**⚠️ Needs Attention:** {worst_domain[0].title()} ({worst_domain[3]:.1%})
**🎪 Active Domains:** {len(domain_data)}/6
"""
    
    def get_domain_analysis(self, user_id: int) -> str:
        """Generate detailed domain-by-domain analysis"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
        SELECT 
            domain,
            COUNT(*) as total,
            SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completed,
            AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as rate,
            COUNT(CASE WHEN date > date('now', '-7 days') THEN 1 END) as recent_activity
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-30 days')
        GROUP BY domain
        ORDER BY rate DESC
        """, (user_id,))
        
        domains = cursor.fetchall()
        conn.close()
        
        if not domains:
            return "**🏢 DOMAIN ANALYSIS**\n*No domain data available*"
        
        domain_analysis = "**🏢 DOMAIN ANALYSIS (30 Days)**\n\n"
        
        domain_icons = {
            'business': '💼',
            'health': '⚡',
            'finance': '💰',
            'parenting': '👨‍👦',
            'work': '🤖',
            'personal': '🎮'
        }
        
        for domain, total, completed, rate, recent in domains:
            icon = domain_icons.get(domain, '📋')
            status = "🔥 Excellent" if rate > 0.8 else "✅ Good" if rate > 0.6 else "⚠️ Needs Focus" if rate > 0.4 else "🚨 Critical"
            
            domain_analysis += f"""
{icon} **{domain.title()}:** {rate:.1%} ({completed}/{total})
   Status: {status} | Recent: {recent} check-ins
"""
        
        return domain_analysis
    
    def get_pattern_insights(self, user_id: int) -> str:
        """Generate behavioral pattern insights"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Timing patterns
        cursor.execute("""
        SELECT 
            strftime('%w', created_at) as day_of_week,
            AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as success_rate,
            COUNT(*) as count
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-30 days')
        GROUP BY strftime('%w', created_at)
        HAVING count >= 3
        ORDER BY success_rate DESC
        """, (user_id,))
        
        day_patterns = cursor.fetchall()
        
        # Recent completion streaks
        cursor.execute("""
        SELECT date, completed FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-14 days')
        ORDER BY date DESC
        """, (user_id,))
        
        recent_data = cursor.fetchall()
        conn.close()
        
        # Calculate current streak
        current_streak = 0
        for date, completed in recent_data:
            if completed:
                current_streak += 1
            else:
                break
        
        # Best day analysis
        day_names = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        best_day = ""
        worst_day = ""
        
        if day_patterns:
            best_day_data = max(day_patterns, key=lambda x: x[1])
            worst_day_data = min(day_patterns, key=lambda x: x[1])
            best_day = f"{day_names[int(best_day_data[0])]} ({best_day_data[1]:.1%})"
            worst_day = f"{day_names[int(worst_day_data[0])]} ({worst_day_data[1]:.1%})"
        
        return f"""
**🧠 BEHAVIORAL PATTERN INSIGHTS**

**📅 Performance by Day:**
• Best Day: {best_day or 'Insufficient data'}
• Challenging Day: {worst_day or 'Insufficient data'}

**🔥 Current Streak:** {current_streak} days
**📊 Weekly Patterns:** {len(day_patterns)} days analyzed

**🎯 Pattern Recognition:**
• Consistency Score: {(current_streak / 7) * 100:.0f}%
• Weekly Engagement: {len(day_patterns)}/7 days active
"""
    
    def get_productivity_metrics(self, user_id: int) -> str:
        """Generate productivity and efficiency metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check if work automation data exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='work_automation_tasks'")
        has_work_table = cursor.fetchone() is not None
        
        if has_work_table:
            cursor.execute("""
            SELECT 
                COUNT(*) as total_automations,
                SUM(CASE WHEN automation_status = 'implemented' THEN weekly_time_saved ELSE 0 END) as time_saved,
                AVG(CASE WHEN automation_status = 'implemented' THEN automation_effectiveness ELSE NULL END) as avg_effectiveness
            FROM work_automation_tasks 
            WHERE user_id = ?
            """, (user_id,))
            
            work_data = cursor.fetchone()
            total_automations, time_saved, avg_effectiveness = work_data or (0, 0, 0)
        else:
            total_automations, time_saved, avg_effectiveness = 0, 0, 0
        
        # Calculate commitment velocity (commitments per day)
        cursor.execute("""
        SELECT COUNT(DISTINCT date) as active_days,
               COUNT(*) as total_commitments
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-14 days')
        """, (user_id,))
        
        velocity_data = cursor.fetchone()
        active_days, total_commitments = velocity_data or (0, 0)
        daily_velocity = total_commitments / max(active_days, 1)
        
        conn.close()
        
        return f"""
**⚡ PRODUCTIVITY METRICS**

**🤖 Work Automation:**
• Total Automations: {total_automations}
• Weekly Time Saved: {time_saved or 0} minutes
• Automation Effectiveness: {(avg_effectiveness or 0) * 100:.0f}%

**📊 Commitment Velocity:**
• Daily Average: {daily_velocity:.1f} commitments/day
• Active Days (14d): {active_days}/14
• Total Commitments: {total_commitments}

**🎯 Efficiency Score:** {min(100, (daily_velocity * 20)):.0f}%
"""
    
    def get_intervention_status(self, user_id: int) -> str:
        """Generate intervention system status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for recent interventions
        cursor.execute("""
        SELECT COUNT(*) as intervention_count
        FROM intervention_triggers 
        WHERE user_id = ? AND timestamp > datetime('now', '-7 days')
        """, (user_id,))
        
        recent_interventions = cursor.fetchone()[0] or 0
        
        # Check completion rates for intervention assessment
        cursor.execute("""
        SELECT 
            domain,
            AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as rate
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-7 days')
        GROUP BY domain
        """, (user_id,))
        
        domain_rates = cursor.fetchall()
        conn.close()
        
        # Determine intervention risk
        critical_domains = [d for d, r in domain_rates if r < 0.3]
        warning_domains = [d for d, r in domain_rates if 0.3 <= r < 0.6]
        
        if critical_domains:
            status = f"🚨 HIGH RISK - {len(critical_domains)} domains critical"
            color = "🔴"
        elif warning_domains:
            status = f"⚠️ MODERATE RISK - {len(warning_domains)} domains need attention"
            color = "🟡"
        else:
            status = "✅ LOW RISK - All domains performing well"
            color = "🟢"
        
        return f"""
**⚡ INTERVENTION SYSTEM STATUS**

**🎯 Current Status:** {status}
**📊 Risk Level:** {color}
**🔄 Recent Interventions (7d):** {recent_interventions}

**📋 Domain Risk Assessment:**
• Critical (>70% failure): {len(critical_domains)} domains
• Warning (40-70% failure): {len(warning_domains)} domains
• Healthy (<40% failure): {len(domain_rates) - len(critical_domains) - len(warning_domains)} domains

**🤖 AI Response:** {'Active monitoring with interventions deployed' if recent_interventions > 0 else 'Passive monitoring - performance within acceptable ranges'}
"""
    
    def get_optimization_recommendations(self, user_id: int) -> str:
        """Generate personalized optimization recommendations"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find lowest performing domain
        cursor.execute("""
        SELECT 
            domain,
            AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as rate,
            COUNT(*) as count
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-14 days')
        GROUP BY domain
        HAVING count >= 3
        ORDER BY rate ASC
        LIMIT 1
        """, (user_id,))
        
        worst_domain = cursor.fetchone()
        
        # Find best performing domain for leverage
        cursor.execute("""
        SELECT 
            domain,
            AVG(CASE WHEN completed = 1 THEN 1.0 ELSE 0.0 END) as rate,
            COUNT(*) as count
        FROM daily_checkins 
        WHERE user_id = ? AND date > date('now', '-14 days')
        GROUP BY domain
        HAVING count >= 3
        ORDER BY rate DESC
        LIMIT 1
        """, (user_id,))
        
        best_domain = cursor.fetchone()
        
        conn.close()
        
        recommendations = ["**🎯 OPTIMIZATION RECOMMENDATIONS**\n"]
        
        if worst_domain:
            domain_name = worst_domain[0].title()
            rate = worst_domain[1]
            
            if rate < 0.4:
                recommendations.append(f"🚨 **CRITICAL:** Focus on {domain_name} ({rate:.1%} completion)")
                recommendations.append(f"   • Break {domain_name.lower()} commitments into smaller, easier actions")
                recommendations.append(f"   • Set minimum viable daily {domain_name.lower()} goal")
                recommendations.append(f"   • Use {domain_name}Agent intervention protocols")
            elif rate < 0.7:
                recommendations.append(f"⚠️ **MODERATE:** Improve {domain_name} consistency ({rate:.1%})")
                recommendations.append(f"   • Identify {domain_name.lower()} avoidance patterns")
                recommendations.append(f"   • Link {domain_name.lower()} actions to existing strong habits")
        
        if best_domain and worst_domain and best_domain[0] != worst_domain[0]:
            best_name = best_domain[0].title()
            best_rate = best_domain[1]
            recommendations.append(f"✅ **LEVERAGE:** Use {best_name} success ({best_rate:.1%}) to boost other domains")
            recommendations.append(f"   • Apply {best_name.lower()} commitment strategies to struggling areas")
        
        # General optimization tips
        recommendations.extend([
            "",
            "**💡 GENERAL OPTIMIZATIONS:**",
            "• Commit to specific actions, not vague intentions",
            "• Use pattern-based prompting from your AI agents",
            "• Address interventions immediately when triggered",
            "• Leverage cross-domain correlations for efficiency"
        ])
        
        return "\n".join(recommendations)

if __name__ == "__main__":
    # Test dashboard generation
    generator = LifeDashboardGenerator()
    dashboard = generator.generate_comprehensive_dashboard(12345)
    print(dashboard)