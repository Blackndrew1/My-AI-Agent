class WorkAutomationManager:
    """Basic work automation manager for testing"""
    
    def __init__(self, db_path="life_agent.db"):
        self.db_path = db_path
    
    def get_automation_impact(self, user_id):
        """Get automation impact metrics"""
        return {
            'total_weekly_minutes_saved': 120,  # 2 hours
            'total_weekly_hours_saved': 2.0,
            'automations_implemented': 3,
            'average_savings_per_automation': 40
        }