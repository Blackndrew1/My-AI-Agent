import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all agents (now we can use relative imports)
from agents.business_agent import BusinessAgent, HealthAgent, FinanceAgent
from agents.parenting_agent import ParentingAgent, WorkAgent, PersonalAgent

# Import database - let's create a simple version if needed
try:
    from database.db_setup import LifeDatabase
except ImportError:
    # Simple fallback database class
    import sqlite3
    from datetime import datetime
    
    class LifeDatabase:
        def __init__(self, db_path="life_agent.db"):
            self.db_path = db_path
            self.init_database()
        
        def init_database(self):
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                date DATE,
                domain TEXT,
                commitment TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            ''')
            conn.commit()
            conn.close()
        
        def add_user(self, user_id, username, first_name):
            pass  # Simple version - just skip user tracking for now

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class LifeAgent:
    def __init__(self):
        self.user_data = {}
        self.db = LifeDatabase()
        self.agents = {}  # Will store agent instances per user
    
    def get_user_agents(self, user_id: int):
        """Get or create agent instances for user"""
        if user_id not in self.agents:
            self.agents[user_id] = {
                'business': BusinessAgent(user_id),
                'health': HealthAgent(user_id), 
                'finance': FinanceAgent(user_id),
                'parenting': ParentingAgent(user_id),
                'work': WorkAgent(user_id),
                'personal': PersonalAgent(user_id)
            }
        return self.agents[user_id]

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
/checkin - Start daily life domain check-in with all 6 agents
/status - Show current life domain status

**NEW: Six Specialized Agents:**
- BusinessAgent: Revenue-focused accountability
- HealthAgent: Energy optimization & fitness
- FinanceAgent: Investment vs consumption tracking
- ParentingAgent: Quality time with your son
- WorkAgent: Automation & efficiency building
- PersonalAgent: Strategic rest & balance

Just type normally and I'll respond intelligently!
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def checkin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced check-in with all 6 agents"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        username = update.effective_user.username
        
        # Add user to database
        self.db.add_user(user_id, username, user_name)
        
        # Get user's agents
        user_agents = self.get_user_agents(user_id)
        
        checkin_message = f"""
🤖 **Six-Agent Life Coordination**

{user_name}, your AI agents are ready for daily accountability:

**1️⃣ BUSINESS AGENT:**
{user_agents['business'].generate_daily_prompt()}

**2️⃣ HEALTH AGENT:** 
{user_agents['health'].generate_daily_prompt()}

**3️⃣ FINANCE AGENT:**
{user_agents['finance'].generate_daily_prompt()}

**4️⃣ PARENTING AGENT:**
{user_agents['parenting'].generate_daily_prompt()}

**5️⃣ WORK AGENT:**
{user_agents['work'].generate_daily_prompt()}

**6️⃣ PERSONAL AGENT:**
{user_agents['personal'].generate_daily_prompt()}

**Respond with your commitments for each domain. Each agent will analyze and provide targeted accountability.**
"""
        
        await update.message.reply_text(checkin_message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages with agent personality"""
        user_message = update.message.text
        user_name = update.effective_user.first_name
        user_id = update.effective_user.id
        
        # Get user's agents for intelligent responses
        user_agents = self.get_user_agents(user_id)
        
        # Enhanced intelligent responses based on message content
        if "good morning" in user_message.lower():
            # Use BusinessAgent's direct style
            response = f"Good morning {user_name}! Ready to dominate today? What's your ONE uncomfortable business action that will actually move the needle?"
        elif "tired" in user_message.lower():
            # Use HealthAgent's energy-focused approach
            response = "Tired is usually code for 'haven't moved my body.' Low energy is CAUSED by inactivity, not solved by avoiding it. 10-minute walk NOW?"
        elif "procrastinating" in user_message.lower():
            # Use BusinessAgent's firm accountability
            response = "I see you. Name the exact task you're avoiding. We're breaking it down into 5-minute chunks and you're starting in the next 60 seconds."
        elif any(word in user_message.lower() for word in ["money", "spending", "buy", "purchase"]):
            # Use FinanceAgent's investment mindset
            response = "Money question detected. Is this business investment or comfort consumption? Every dollar spent is a strategic choice. Justify it."
        elif any(word in user_message.lower() for word in ["son", "family", "parenting"]):
            # Use ParentingAgent's caring accountability
            response = f"Family focus, {user_name}. Quality time isn't about duration - it's about presence. Phone away, fully engaged. What's the plan?"
        elif any(word in user_message.lower() for word in ["work", "automate", "efficiency"]):
            # Use WorkAgent's efficiency focus
            response = "Work optimization opportunity. What manual task are you doing repeatedly that could be automated in 1 hour of development?"
        elif any(word in user_message.lower() for word in ["gaming", "rest", "recharge", "leisure"]):
            # Use PersonalAgent's balance wisdom
            response = "Personal time question. Strategic rest or escapism? Recovery should make you excited to return to challenges, not avoid them."
        else:
            response = f"I hear you, {user_name}. Tell me specifically what domain needs attention: Business, Health, Finances, Parenting, Work, or Personal time? Each has a specialized agent ready to help."
        
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
    # Quick agent test
    print("Testing agents...")
    try:
        test_agent = BusinessAgent(12345)
        print("✅ BusinessAgent works!")
        test_agent = ParentingAgent(12345)
        print("✅ ParentingAgent works!")
        print("All agents loaded successfully!")
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
    
    main()