import os
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Add project root to imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from conversation_manager import ConversationManager
from enhanced_base_agent import EnhancedBusinessAgent
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
            self.agents[user_id] = {
                'business': EnhancedBusinessAgent(user_id, self.conversation_manager)
            }
        return self.agents[user_id]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_name = update.effective_user.first_name
        message = f"""
🧠 **Enhanced Life Agent**

Hello {user_name}! NEW FEATURES:
- Multi-turn conversations
- Pattern recognition  
- Success prediction

**Commands:**
/business - Intelligent business conversation
/patterns - Behavioral analysis
/insights - Cross-domain correlations
/forecast - Success predictions
/checkin - Original daily check-in

Type /business to test enhanced intelligence!
"""
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def business_conversation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        self.db.add_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        agents = self.get_user_agents(user_id)
        prompt = agents['business'].start_domain_conversation()
        
        await update.message.reply_text(f"🎯 **Business Agent**\n\n{prompt}", parse_mode='Markdown')
    
    async def patterns_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show behavioral pattern analysis"""
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name
        
        from pattern_analyzer import PatternAnalyzer
        analyzer = PatternAnalyzer()
        patterns = analyzer.analyze_user_patterns(user_id, 30)
        
        completion_data = patterns.get('completion_patterns', {}).get('by_domain', {})
        if completion_data:
            completion_text = "\n".join([
                f"**{domain.title()}:** {data['completion_rate']:.0%} ({data['trend']})"
                for domain, data in completion_data.items()
            ])
        else:
            completion_text = "No pattern data yet - use system for a few days"
        
        avoidance_data = patterns.get('avoidance_patterns', {})
        avoidance_rate = avoidance_data.get('total_avoidance_rate', 0)
        
        message = f"""
📊 **{user_name}'s Pattern Analysis**

**📈 COMPLETION RATES:**
{completion_text}

**⚠️ AVOIDANCE RATE:** {avoidance_rate:.0%}

**🔗 CORRELATIONS:** {len(patterns.get('cross_domain_effects', {}))} detected

Use /insights for detailed analysis.
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def insights_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show cross-domain insights"""
        user_id = update.effective_user.id
        
        from pattern_analyzer import PatternAnalyzer
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
            insights_text = "Continue using system to unlock cross-domain insights."
        
        await update.message.reply_text(insights_text, parse_mode='Markdown')
    
    async def forecast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show daily success forecast"""
        user_id = update.effective_user.id
        
        patterns = self.conversation_manager.get_recent_patterns(user_id, 'business', 7)
        
        if patterns:
            completion_rate = sum(1 for p in patterns if p[2]) / len(patterns)
            if completion_rate > 0.7:
                forecast = f"✅ **High Success:** {completion_rate:.0%}"
            elif completion_rate > 0.4:
                forecast = f"⚠️ **Medium Risk:** {completion_rate:.0%}"
            else:
                forecast = f"🚨 **High Risk:** {completion_rate:.0%}"
        else:
            forecast = "📊 **No Data:** Use system for predictions"
        
        message = f"""
🔮 **Daily Forecast**

**Business:** {forecast}

Use /business for coaching.
"""
        
        await update.message.reply_text(message, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_id = update.effective_user.id
        context_data = self.conversation_manager.get_conversation_context(user_id)
        
        if context_data and context_data.get('agent_domain') == 'business':
            agents = self.get_user_agents(user_id)
            response = agents['business'].process_user_response(update.message.text)
            await update.message.reply_text(response, parse_mode='Markdown')
        else:
            await update.message.reply_text("Type /business for intelligent conversation or /start for help")

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    agent = EnhancedLifeAgent()
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", agent.start_command))
    app.add_handler(CommandHandler("business", agent.business_conversation))
    app.add_handler(CommandHandler("patterns", agent.patterns_command))
    app.add_handler(CommandHandler("insights", agent.insights_command))
    app.add_handler(CommandHandler("forecast", agent.forecast_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agent.handle_message))
    
    print("🧠 Enhanced Life Agent starting...")
    app.run_polling()

if __name__ == '__main__':
    main()