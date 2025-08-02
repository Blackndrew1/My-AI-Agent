import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class LifeAgent:
    def __init__(self):
        self.user_data = {}

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        welcome_message = f"""
🤖 **Life Agent Activated**

Hello {user_name}! I'm your AI accountability agent.

I'm here to enforce discipline across all your life domains:
- Business building (consultant/agency goals)
- Health & fitness (morning workouts, gym with son)
- Financial discipline
- Parenting excellence
- Work automation
- Personal time balance

**I'm clever, analytical, and will hold you firmly accountable.**

Type /help to see what I can do.
Ready to start managing your life?
"""
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown')

    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🛠️ **Available Commands:**

/start - Activate your life agent
/help - Show this help message
/checkin - Start daily life domain check-in
/status - Show current life domain status

**Coming Soon:**
- Morning routine enforcement
- Business action tracking
- Health monitoring
- Work automation
- Pattern analysis

Just type normally and I'll respond intelligently!
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def checkin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle daily check-in"""
        user_name = update.effective_user.first_name
        
        checkin_message = f"""
🎯 **Daily Life Domain Check-In**

{user_name}, time for accountability across all domains:

**Answer each domain with ONE specific commitment:**

1️⃣ **Business**: What's your ONE business action today?
2️⃣ **Health**: Morning workout plan? (gym/home/outdoor)
3️⃣ **Finance**: Any spending plans or money goals?
4️⃣ **Parenting**: Quality time plan with your son?
5️⃣ **Work**: What task will you automate today?
6️⃣ **Personal**: How will you recharge tonight?

Type your commitments and I'll track them!
"""
        
        await update.message.reply_text(checkin_message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user_message = update.message.text
        user_name = update.effective_user.first_name
        
        # Simple intelligent responses
        if "good morning" in user_message.lower():
            response = f"Good morning {user_name}! Ready to dominate today? What's your ONE critical business action?"
        elif "tired" in user_message.lower():
            response = "Tired is a choice. What specific action will you take in the next 10 minutes to change your state?"
        elif "procrastinating" in user_message.lower():
            response = "I see you. Name the exact task you're avoiding. We're breaking it down into 5-minute chunks right now."
        else:
            response = f"I hear you, {user_name}. Tell me specifically what domain needs attention: Business, Health, Finances, Parenting, Work, or Personal time?"
        
        await update.message.reply_text(response)

def main():
    """Main function to run the bot"""
    # Get token from environment
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    # Create Life Agent instance
    agent = LifeAgent()
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", agent.start_command))
    application.add_handler(CommandHandler("help", agent.help_command))
    application.add_handler(CommandHandler("checkin", agent.checkin_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent.handle_message))
    
    # Start the bot
    print("🤖 Life Agent starting...")
    application.run_polling()

if __name__ == '__main__':
    main()