import asyncio
import schedule
import time
from datetime import datetime
from bot.intervention_engine import InterventionEngine
from bot.intervention_messages import InterventionMessageGenerator

class InterventionScheduler:
    """Automated monitoring and intervention deployment"""
    
    def __init__(self, telegram_bot, db_path="life_agent.db"):
        self.telegram_bot = telegram_bot
        self.intervention_engine = InterventionEngine(db_path)
        self.message_generator = InterventionMessageGenerator()
        self.active_users = []  # List of user IDs to monitor
    
    def add_monitored_user(self, user_id: int):
        """Add user to monitoring list"""
        if user_id not in self.active_users:
            self.active_users.append(user_id)
    
    async def run_intervention_check(self):
        """Run comprehensive intervention check for all users"""
        for user_id in self.active_users:
            interventions_needed = self.intervention_engine.comprehensive_intervention_check(user_id)
            
            for domain, intervention_data in interventions_needed.items():
                await self.deploy_intervention(user_id, domain, intervention_data)
    
    async def deploy_intervention(self, user_id: int, domain: str, intervention_data: Dict):
        """Deploy intervention message to user"""
        level = intervention_data['level']
        triggers = intervention_data['triggers']
        
        # Generate appropriate intervention message
        intervention_message = self.message_generator.generate_intervention_message(
            domain, level, triggers[0] if triggers else {}, {}
        )
        
        # Send via Telegram
        try:
            await self.telegram_bot.send_message(
                chat_id=user_id,
                text=intervention_message,
                parse_mode='Markdown'
            )
            
            # Log intervention deployment
            self.log_intervention_sent(user_id, domain, level, intervention_message)
            
        except Exception as e:
            print(f"Failed to send intervention to {user_id}: {e}")
    
    def log_intervention_sent(self, user_id: int, domain: str, level: int, message: str):
        """Log that intervention was successfully sent"""
        # Implementation for tracking intervention effectiveness
        pass
    
    def schedule_monitoring_tasks(self):
        """Schedule regular monitoring tasks"""
        # Morning accountability check (9 AM)
        schedule.every().day.at("09:00").do(lambda: asyncio.create_task(self.morning_accountability_check()))
        
        # Midday progress pulse (1 PM) 
        schedule.every().day.at("13:00").do(lambda: asyncio.create_task(self.midday_progress_check()))
        
        # Evening review trigger (8 PM)
        schedule.every().day.at("20:00").do(lambda: asyncio.create_task(self.evening_review_reminder()))
        
        # Real-time monitoring (every 30 minutes)
        schedule.every(30).minutes.do(lambda: asyncio.create_task(self.run_intervention_check()))
    
    async def morning_accountability_check(self):
        """9 AM: Check for missed morning commitments"""
        for user_id in self.active_users:
            missed_deadlines = self.intervention_engine.monitor_commitment_deadlines(user_id)
            
            if missed_deadlines:
                message = f"""
🌅 **Morning Accountability Check**

You have {len(missed_deadlines)} pending commitments from this morning:

{chr(10).join([f"• {item['domain'].title()}: {item['commitment']}" for item in missed_deadlines[:3]])}

Status update: Are these still happening today, or do we need to adjust the plan?
"""
                
                await self.telegram_bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='Markdown'
                )
    
    async def run_scheduler(self):
        """Run the scheduler continuously"""
        self.schedule_monitoring_tasks()
        
        while True:
            schedule.run_pending()
            await asyncio.sleep(60)  # Check every minute

if __name__ == "__main__":
    print("Intervention scheduler ready!")