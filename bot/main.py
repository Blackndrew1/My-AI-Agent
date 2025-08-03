import os
import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import your modules
from database.db_setup import LifeDatabase
from conversation_manager import ConversationManager
from agents.business_agent import BusinessAgent
from agents.health_agent import HealthAgent
from agents.finance_agent import FinanceAgent
from agents.parenting_agent import ParentingAgent
from agents.work_agent import WorkAgent
from agents.personal_agent import PersonalAgent
from intervention_engine import InterventionEngine
from intervention_messages import InterventionMessageGenerator

# Load environment variables
load_dotenv()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

class LifeAgent:
    def __init__(self):
        self.user_data = {}
        self.db = LifeDatabase()
        self.conversation_manager = ConversationManager()
        self.agents = {}
        self.intervention_engine = InterventionEngine()
        self.intervention_scheduler = None  # Will be set after bot initialization

    def get_user_agents(self, user_id):
        """Get or create agent instances with conversation manager"""
        if user_id not in self.agents:
            self.agents[user_id] = {
                'business': BusinessAgent(user_id, self.conversation_manager),
                'health': HealthAgent(user_id, self.conversation_manager),
                'finance': FinanceAgent(user_id, self.conversation_manager),
                'parenting': ParentingAgent(user_id, self.conversation_manager),
                'work': WorkAgent(user_id, self.conversation_manager),
                'personal': PersonalAgent(user_id, self.conversation_manager)
            }
        return self.agents[user_id]

    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        welcome_message = f"""
🤖 **Life Agent Activated**

Hello {user_name}! I'm your AI accountability agent with advanced intervention capabilities.

I'm here to enforce discipline across all your life domains:
• Business building (consultant/agency goals)
• Health & fitness (morning workouts, gym with son)
• Financial discipline
• Parenting excellence
• Work automation
• Personal time balance

**I'm clever, analytical, and will hold you firmly accountable with real-time intervention capabilities.**

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
/patterns - Show behavioral pattern analysis
/interventions - Check current intervention status
/intervene [domain] - Deploy specific intervention

**Real-Time Features:**
- Automatic intervention deployment
- Pattern decline detection
- Avoidance language analysis
- Cross-domain correlation tracking

Just type normally and I'll respond intelligently!
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')

    async def domain_checkin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
{user_agents['business'].get_pattern_based_prompt()}

**2️⃣ HEALTH AGENT:**
{user_agents['health'].get_pattern_based_prompt()}

**3️⃣ FINANCE AGENT:**
{user_agents['finance'].get_pattern_based_prompt()}

**4️⃣ PARENTING AGENT:**
{user_agents['parenting'].get_pattern_based_prompt()}

**5️⃣ WORK AGENT:**
{user_agents['work'].get_pattern_based_prompt()}

**6️⃣ PERSONAL AGENT:**
{user_agents['personal'].get_pattern_based_prompt()}

**Respond with your commitments for each domain. Each agent will analyze and provide targeted accountability.**
"""

        await update.message.reply_text(checkin_message, parse_mode='Markdown')

    async def patterns_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show detailed pattern analysis"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name

        from pattern_analyzer import PatternAnalyzer
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze_user_patterns(user_id, 30)

        # Format completion patterns
        completion_data = patterns.get('completion_patterns', {}).get('by_domain', {})
        completion_text = "\n".join([
            f"**{domain.title()}:** {data['completion_rate']:.0%} ({data['trend']})"
            for domain, data in completion_data.items()
        ]) if completion_data else "No completion data yet"

        # Format timing insights
        timing_data = patterns.get('timing_patterns', {})
        timing_text = ""
        if 'best_commitment_times' in timing_data and timing_data['best_commitment_times']:
            best_hour = timing_data['best_commitment_times'][0][0]
            best_rate = timing_data['best_commitment_times'][0][1]['success_rate']
            timing_text = f"**Best commitment time:** {best_hour}:00 ({best_rate:.0%} success)"

        # Format avoidance patterns
        avoidance_data = patterns.get('avoidance_patterns', {})
        avoidance_rate = avoidance_data.get('total_avoidance_rate', 0)

        message = f"""
📊 **{user_name}'s Behavioral Pattern Analysis**

**📈 COMPLETION RATES (30 days):**
{completion_text}

**⏰ TIMING PATTERNS:**
{timing_text}

**⚠️ AVOIDANCE RATE:** {avoidance_rate:.0%}

**🎯 CROSS-DOMAIN INSIGHTS:**
{len(patterns.get('cross_domain_effects', {}))} significant correlations detected

Type /interventions to check if any accountability measures are needed.
"""

        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def check_interventions_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manual intervention check command"""
        user_id = update.effective_user.id
        
        interventions = self.intervention_engine.comprehensive_intervention_check(user_id)
        
        if not interventions:
            await update.message.reply_text("✅ No interventions needed. All domains performing well!")
            return
        
        intervention_summary = "🚨 **Active Interventions Needed:**\n\n"
        
        for domain, data in interventions.items():
            level = data['level']
            level_text = ['', 'Gentle', 'Pattern Alert', 'Firm', 'Crisis', 'Emergency'][level]
            intervention_summary += f"**{domain.title()}:** Level {level} ({level_text})\n"
        
        intervention_summary += "\nType `/intervene [domain]` for specific intervention details."
        
        await update.message.reply_text(intervention_summary, parse_mode='Markdown')
    
    async def intervene_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Deploy specific domain intervention"""
        user_id = update.effective_user.id
        
        if not context.args:
            await update.message.reply_text("Specify domain: `/intervene business` or `/intervene health` etc.")
            return
        
        domain = context.args[0].lower()
        
        if domain not in ['business', 'health', 'finance', 'parenting', 'work', 'personal']:
            await update.message.reply_text("Invalid domain. Use: business, health, finance, parenting, work, personal")
            return
        
        # Get intervention level for domain
        level = self.intervention_engine.get_intervention_level(user_id, domain)
        
        if level == 0:
            await update.message.reply_text(f"✅ No intervention needed for {domain}. Performance is acceptable.")
            return
        
        # Generate and send intervention
        generator = InterventionMessageGenerator()
        trigger_data = {'completion_rate': 0.3}  # Sample data - would get from real patterns
        
        intervention_message = generator.generate_intervention_message(domain, level, trigger_data)
        
        await update.message.reply_text(intervention_message, parse_mode='Markdown')

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user_message = update.message.text
        user_name = update.effective_user.first_name
        user_id = update.effective_user.id

        # Check for avoidance language in real-time
        avoidance_result = self.intervention_engine.analyze_avoidance_language(user_id, user_message)
        
        if avoidance_result['avoidance_detected']:
            avoidance_response = f"""
⚠️ **Avoidance Language Detected**

Patterns found: {', '.join(avoidance_result['patterns'])}
Avoidance score: {avoidance_result['score']:.0%}

Let's be more specific. What exact action will you take and when?
"""
            await update.message.reply_text(avoidance_response, parse_mode='Markdown')
            return

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
    application.add_handler(CommandHandler("checkin", agent.domain_checkin))
    application.add_handler(CommandHandler("patterns", agent.patterns_command))
    application.add_handler(CommandHandler("interventions", agent.check_interventions_command))
    application.add_handler(CommandHandler("intervene", agent.intervene_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent.handle_message))
    
    # Start the bot
    print("🤖 Life Agent with Intervention System starting...")
    application.run_polling()

if __name__ == '__main__':
    main()