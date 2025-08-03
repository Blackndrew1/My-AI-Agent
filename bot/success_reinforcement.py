class SuccessReinforcementSystem:
    """Recognizes and amplifies positive patterns"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
    
    def detect_success_patterns(self, user_id: int):
        """Detect positive momentum patterns"""
        from bot.pattern_analyzer import PatternAnalyzer
        analyzer = PatternAnalyzer(self.db_path)
        patterns = analyzer.analyze_user_patterns(user_id, 7)
        
        success_patterns = []
        domain_patterns = patterns.get('completion_patterns', {}).get('by_domain', {})
        
        for domain, data in domain_patterns.items():
            completion_rate = data['completion_rate']
            trend = data['trend']
            
            # Detect success patterns
            if completion_rate > 0.8 and trend == 'improving':
                success_patterns.append({
                    'domain': domain,
                    'type': 'momentum_building',
                    'completion_rate': completion_rate,
                    'message': self.generate_momentum_message(domain, completion_rate)
                })
            elif completion_rate > 0.9:
                success_patterns.append({
                    'domain': domain, 
                    'type': 'excellence_achieved',
                    'completion_rate': completion_rate,
                    'message': self.generate_excellence_message(domain, completion_rate)
                })
        
        return success_patterns
    
    def generate_momentum_message(self, domain: str, completion_rate: float) -> str:
        """Generate momentum reinforcement message"""
        
        if domain == 'business':
            return f"""
🚀 **BUSINESS MOMENTUM DETECTED**

**Performance Status:** {completion_rate:.0%} completion rate with improving trend.

**Momentum Opportunity:** You're building the exact habits that create successful consultants.

**Capitalize Now:** What bigger business challenge feels possible now that felt impossible a week ago?

**Acceleration Question:** How can we use this business momentum to land your first $5,000 client?
"""
        
        elif domain == 'health':
            return f"""
💪 **HEALTH MOMENTUM STRONG**

**Energy Optimization:** {completion_rate:.0%} completion rate building physical excellence.

**Cross-Domain Impact:** This health consistency is boosting:
- Business confidence and energy
- Family presence and patience  
- Mental clarity and focus

**Level Up:** What physical challenge will you add while this momentum is strong?
"""
        
        return f"🎯 **{domain.title()} momentum building:** {completion_rate:.0%} completion rate. Time to level up!"
    
    def generate_excellence_message(self, domain: str, completion_rate: float) -> str:
        """Generate excellence recognition message"""
        
        return f"""
⭐ **{domain.title().upper()} EXCELLENCE ACHIEVED**

**Performance Status:** {completion_rate:.0%} completion rate - exceptional consistency.

**Recognition:** You've built a system that works. This level of consistency in {domain} is rare.

**Leverage Opportunity:** How can this {domain} excellence support breakthrough progress in other life domains?

**Mastery Question:** What advanced challenge in {domain} becomes possible with this foundation?
"""

if __name__ == "__main__":
    system = SuccessReinforcementSystem()
    print("Success reinforcement system ready!")