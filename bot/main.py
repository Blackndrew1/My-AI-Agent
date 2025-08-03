import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Add project root to imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conversation_manager import ConversationManager
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database'))
from db_setup import LifeDatabase
load_dotenv()

class EnhancedLifeAgent:
    def __init__(self):
        self.db = LifeDatabase()
        self.conversation_manager = ConversationManager()
        self.agents = {}
    
    def get_user_agents(self, user_id):
        if user_id not in self.agents:
            # Import all agents
            from bot.agents.business_agent import BusinessAgent
            from bot.agents.health_agent import HealthAgent
            from bot.agents.finance_agent import FinanceAgent
            from bot.agents.parenting_agent import ParentingAgent
            from bot.agents.work_agent import WorkAgent
            from bot.agents.personal_agent import PersonalAgent
            
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
        user_name = update.effective_user.first_name
        message = f"""
🧠 **Complete Life Agent System - Day 4**

Hello {user_name}! ALL 6 AGENTS WITH PATTERN INTELLIGENCE:

**Individual Agent Commands:**
/business - Business coaching with pattern intelligence
/health - Health & energy optimization
/finance - Financial discipline & investment mindset
/parenting - Quality time & relationship building
/work - Automation & efficiency optimization
/personal - Strategic rest & life balance

**Analysis Commands:**
/patterns - Your behavioral analysis across all domains
/insights - Cross-domain correlations
/forecast - Success predictions
/checkin - Quick check-in across all 6 domains

**Test the intelligence:** Try any agent command above!
"""
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def business_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['business'].start_domain_conversation()
        
        await update.message.reply_text(f"🎯 **Business Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def health_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['health'].start_domain_conversation()
        
        await update.message.reply_text(f"⚡ **Health Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def finance_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['finance'].start_domain_conversation()
        
        await update.message.reply_text(f"💰 **Finance Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def parenting_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['parenting'].start_domain_conversation()
        
        await update.message.reply_text(f"👨‍👦 **Parenting Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def work_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['work'].start_domain_conversation()
        
        await update.message.reply_text(f"💼 **Work Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def personal_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['personal'].start_domain_conversation()
        
        await update.message.reply_text(f"⚖️ **Personal Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def patterns_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show detailed pattern analysis"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        from bot.pattern_analyzer import PatternAnalyzer
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze_user_patterns(user_id, 30)
        
        # Format completion patterns
        completion_data = patterns.get('completion_patterns', {}).get('by_domain', {})
        if completion_data:
            completion_text = "\n".join([
                f"**{domain.title()}:** {data['completion_rate']:.0%} ({data['trend']})"
                for domain, data in completion_data.items()
            ])
        else:
            completion_text = "No completion data yet - use system for a few days"
        
        # Format avoidance patterns
        avoidance_data = patterns.get('avoidance_patterns', {})
        avoidance_rate = avoidance_data.get('total_avoidance_rate', 0)
        
        message = f"""
📊 **{user_name}'s Behavioral Pattern Analysis**

**📈 COMPLETION RATES (30 days):**
{completion_text}

**⚠️ AVOIDANCE RATE:** {avoidance_rate:.0%}

**🎯 CROSS-DOMAIN INSIGHTS:**
{len(patterns.get('cross_domain_effects', {}))} significant correlations detected

Type /insights for detailed predictive analysis.
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def insights_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show cross-domain insights"""
        user_id = update.effective_user.id
        
        from bot.pattern_analyzer import PatternAnalyzer
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze_user_patterns(user_id, 30)
        
        cross_effects = patterns.get('cross_domain_effects', {})
        
        if cross_effects:
            insights_text = "**🧠 CROSS-DOMAIN INTELLIGENCE:**\n\n"
            for effect_key, data in list(cross_effects.items())[:3]:
                source, target = effect_key.split('_affects_')
                strength = data['strength']
                insights_text += f"• **{source.title()} → {target.title()}:** {strength:.0%} correlation\n"
        else:
            insights_text = "Continue using system to unlock cross-domain insights.\n\nNeed 5+ days of data across multiple domains for meaningful correlations."
        
        await update.message.reply_text(insights_text, parse_mode='Markdown')
    
    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show daily success forecast"""
        user_id = update.effective_user.id
        
        from bot.pattern_analyzer import PatternAnalyzer
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze_user_patterns(user_id, 7)
        
        completion_data = patterns.get('completion_patterns', {}).get('by_domain', {})
        
        if completion_data:
            forecast_text = "**🔮 SUCCESS PREDICTIONS:**\n\n"
            for domain, data in completion_data.items():
                rate = data['completion_rate']
                trend = data['trend']
                
                if rate > 0.7:
                    emoji = "✅"
                    status = "High Success"
                elif rate > 0.4:
                    emoji = "⚠️"
                    status = "Medium Risk"
                else:
                    emoji = "🚨"
                    status = "High Risk"
                
                forecast_text += f"{emoji} **{domain.title()}:** {rate:.0%} - {status} ({trend})\n"
        else:
            forecast_text = "📊 **No Data:** Use system for a few days to enable predictions"
        
        message = f"""
🔮 **Daily Success Forecast**

{forecast_text}

Type any agent command for pattern-based coaching.
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def checkin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced check-in with all 6 agents"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        self.db.add_user(user_id, update.effective_user.username, user_name)
        
        # Get all agents
        agents = self.get_user_agents(user_id)
        
        message = f"""
🤖 **Six-Agent Life Coordination - Pattern Intelligence Active**

{user_name}, your AI agents are ready for daily accountability:

**1️⃣ BUSINESS:** {agents['business'].generate_daily_prompt()}

**2️⃣ HEALTH:** {agents['health'].generate_daily_prompt()}

**3️⃣ FINANCE:** {agents['finance'].generate_daily_prompt()}

**4️⃣ PARENTING:** {agents['parenting'].generate_daily_prompt()}

**5️⃣ WORK:** {agents['work'].generate_daily_prompt()}

**6️⃣ PERSONAL:** {agents['personal'].generate_daily_prompt()}

**Use individual commands (/business, /health, etc.) for intelligent conversations!**
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        context_data = self.conversation_manager.get_conversation_context(user_id)
        
        if context_data:
            agent_domain = context_data.get('agent_domain')
            agents = self.get_user_agents(user_id)
            
            if agent_domain in agents:
                response = agents[agent_domain].process_user_response(update.message.text)
                await update.message.reply_text(response, parse_mode='Markdown')
            else:
                await update.message.reply_text("Type any agent command (/business, /health, etc.) for intelligent coaching!")
        else:
            # Simple intelligent responses for general messages
            user_message = update.message.text.lower()
            user_name = update.effective_user.first_name
            
            if "pattern" in user_message or "analysis" in user_message:
                await update.message.reply_text("📊 Type /patterns to see your behavioral analysis!")
            elif "business" in user_message:
                await update.message.reply_text("🎯 Type /business for pattern-based business coaching!")
            elif "health" in user_message or "workout" in user_message:
                await update.message.reply_text("⚡ Type /health for energy optimization coaching!")
            elif "help" in user_message:
                await update.message.reply_text("Try /start to see all available commands!")
            else:
                await update.message.reply_text(f"Hi {user_name}! Try /checkin for all 6 agents or /business, /health, /finance, /parenting, /work, /personal for individual coaching.")

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("ERROR: TELEGRAM_BOT_TOKEN not found in .env file")
        return
    
    agent = EnhancedLifeAgent()
    app = Application.builder().token(token).build()
    
    # Add all command handlers
    app.add_handler(CommandHandler("start", agent.start_command))
    app.add_handler(CommandHandler("business", agent.business_conversation))
    app.add_handler(CommandHandler("health", agent.health_conversation))
    app.add_handler(CommandHandler("finance", agent.finance_conversation))
    app.add_handler(CommandHandler("parenting", agent.parenting_conversation))
    app.add_handler(CommandHandler("work", agent.work_conversation))
    app.add_handler(CommandHandler("personal", agent.personal_conversation))
    app.add_handler(CommandHandler("patterns", agent.patterns_command))
    app.add_handler(CommandHandler("insights", agent.insights_command))
    app.add_handler(CommandHandler("forecast", agent.forecast_command))
    app.add_handler(CommandHandler("checkin", agent.checkin_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent.handle_message))
    
    print("🧠 Complete Life Agent System - All 6 Agents with Pattern Intelligence starting...")
    app.run_polling()

if __name__ == '__main__':
    main()