import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
from datetime import datetime
import json

class EmailAutomationGUI:
    """Professional email template automation with GUI interface"""
    
    def __init__(self):
        self.db_path = "life_agent.db"
        self.init_email_tables()
        self.create_gui()
        self.load_template_data()
    
    def init_email_tables(self):
        """Initialize email automation tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS email_templates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            template_name TEXT UNIQUE NOT NULL,
            category TEXT NOT NULL,
            subject_line TEXT NOT NULL,
            template_body TEXT NOT NULL,
            variables_used TEXT,
            usage_count INTEGER DEFAULT 0,
            effectiveness_score REAL DEFAULT 5.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_used TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def load_template_data(self):
        """Load sample email templates"""
        sample_templates = [
            {
                'template_name': 'Technical Support Response',
                'category': 'Customer Support',
                'subject_line': 'Re: {issue_type} - Ticket #{ticket_number}',
                'template_body': '''Hi {customer_name},

Thank you for reaching out about {issue_description}. I understand how {issue_type} problems can be frustrating.

I've reviewed your account and {analysis_summary}.

**Solution:**
{solution_steps}

**Expected Resolution:** {resolution_timeframe}

**Next Steps:**
1. {step_1}
2. {step_2}
3. If you continue experiencing issues, reply to this email with {additional_info_needed}

{follow_up_commitment}

Best regards,
{agent_name}
{company_name} Technical Support

**Ticket #{ticket_number}** | **Priority: {priority_level}** | **ETA: {eta}**''',
                'variables_used': 'customer_name,issue_type,issue_description,analysis_summary,solution_steps,resolution_timeframe,step_1,step_2,additional_info_needed,follow_up_commitment,agent_name,company_name,ticket_number,priority_level,eta'
            },
            {
                'template_name': 'Project Status Update',
                'category': 'Project Management',
                'subject_line': 'Project Update: {project_name} - {status_type}',
                'template_body': '''Hi {client_name},

I wanted to provide you with an update on {project_name}.

**Current Status:** {current_status}
**Completion:** {completion_percentage}%
**Timeline:** {timeline_status}

**Recent Accomplishments:**
• {accomplishment_1}
• {accomplishment_2}
• {accomplishment_3}

**Next Milestones:**
• {milestone_1} - {milestone_1_date}
• {milestone_2} - {milestone_2_date}

**Any Concerns:** {concerns_or_blockers}

Please let me know if you have any questions or need additional details.

Best regards,
{project_manager_name}''',
                'variables_used': 'client_name,project_name,status_type,current_status,completion_percentage,timeline_status,accomplishment_1,accomplishment_2,accomplishment_3,milestone_1,milestone_1_date,milestone_2,milestone_2_date,concerns_or_blockers,project_manager_name'
            },
            {
                'template_name': 'Meeting Follow-up',
                'category': 'Communication',
                'subject_line': 'Follow-up: {meeting_topic} - Action Items',
                'template_body': '''Hi {attendees},

Thank you for joining today's meeting about {meeting_topic}.

**Meeting Summary:**
{meeting_summary}

**Decisions Made:**
• {decision_1}
• {decision_2}
• {decision_3}

**Action Items:**
• {action_item_1} - Owner: {owner_1} - Due: {due_date_1}
• {action_item_2} - Owner: {owner_2} - Due: {due_date_2}
• {action_item_3} - Owner: {owner_3} - Due: {due_date_3}

**Next Meeting:** {next_meeting_date}

Please confirm receipt and let me know if I missed anything important.

Best regards,
{meeting_organizer}''',
                'variables_used': 'attendees,meeting_topic,meeting_summary,decision_1,decision_2,decision_3,action_item_1,owner_1,due_date_1,action_item_2,owner_2,due_date_2,action_item_3,owner_3,due_date_3,next_meeting_date,meeting_organizer'
            }
        ]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        for template in sample_templates:
            cursor.execute('SELECT COUNT(*) FROM email_templates WHERE template_name = ?', 
                         (template['template_name'],))
            if cursor.fetchone()[0] == 0:
                cursor.execute('''
                INSERT INTO email_templates 
                (template_name, category, subject_line, template_body, variables_used)
                VALUES (?, ?, ?, ?, ?)
                ''', (
                    template['template_name'], template['category'], 
                    template['subject_line'], template['template_body'],
                    template['variables_used']
                ))
        
        conn.commit()
        conn.close()
    
    def create_gui(self):
        """Create the main GUI interface"""
        self.root = tk.Tk()
        self.root.title("Email Automation System - Professional Template Generator")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="📧 Email Automation System", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Template selection
        ttk.Label(main_frame, text="Select Template:", font=('Arial', 10, 'bold')).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5))
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(main_frame, textvariable=self.template_var, 
                                          width=50, state="readonly")
        self.template_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=(0, 10))
        self.template_combo.bind('<<ComboboxSelected>>', self.on_template_select)
        
        # Load templates into combobox
        self.load_template_list()
        
        # Template preview area
        preview_frame = ttk.LabelFrame(main_frame, text="Template Preview", padding="10")
        preview_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        preview_frame.columnconfigure(0, weight=1)
        preview_frame.rowconfigure(1, weight=1)
        
        # Subject line
        ttk.Label(preview_frame, text="Subject Line:", font=('Arial', 9, 'bold')).grid(
            row=0, column=0, sticky=tk.W)
        self.subject_text = tk.Text(preview_frame, height=2, wrap=tk.WORD, font=('Arial', 9))
        self.subject_text.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 10))
        
        # Email body
        ttk.Label(preview_frame, text="Email Body:", font=('Arial', 9, 'bold')).grid(
            row=2, column=0, sticky=tk.W)
        self.body_text = scrolledtext.ScrolledText(preview_frame, height=20, wrap=tk.WORD, 
                                                  font=('Arial', 9))
        self.body_text.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(5, 10))
        
        # Variables info
        ttk.Label(preview_frame, text="Available Variables:", font=('Arial', 9, 'bold')).grid(
            row=4, column=0, sticky=tk.W)
        self.variables_text = tk.Text(preview_frame, height=3, wrap=tk.WORD, font=('Arial', 8))
        self.variables_text.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(button_frame, text="📋 Copy Template", 
                  command=self.copy_template).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📊 Show Statistics", 
                  command=self.show_statistics).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="💾 Export Templates", 
                  command=self.export_templates).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="❌ Close", 
                  command=self.root.quit).pack(side=tk.RIGHT)
    
    def load_template_list(self):
        """Load template names into combobox"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT template_name, category FROM email_templates ORDER BY category, template_name')
        templates = cursor.fetchall()
        conn.close()
        
        template_list = [f"{template[1]} - {template[0]}" for template in templates]
        self.template_combo['values'] = template_list
        
        if template_list:
            self.template_combo.set(template_list[0])
            self.on_template_select()
    
    def on_template_select(self, event=None):
        """Handle template selection"""
        selected = self.template_var.get()
        if not selected:
            return
        
        # Extract template name from "Category - Template Name" format
        template_name = selected.split(' - ', 1)[1]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT subject_line, template_body, variables_used 
        FROM email_templates 
        WHERE template_name = ?
        ''', (template_name,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            subject, body, variables = result
            
            # Update display
            self.subject_text.delete(1.0, tk.END)
            self.subject_text.insert(1.0, subject)
            
            self.body_text.delete(1.0, tk.END)
            self.body_text.insert(1.0, body)
            
            # Format variables nicely
            if variables:
                var_list = variables.split(',')
                formatted_vars = ', '.join([f"{{{var.strip()}}}" for var in var_list])
                self.variables_text.delete(1.0, tk.END)
                self.variables_text.insert(1.0, formatted_vars)
    
    def copy_template(self):
        """Copy current template to clipboard"""
        subject = self.subject_text.get(1.0, tk.END).strip()
        body = self.body_text.get(1.0, tk.END).strip()
        
        full_template = f"Subject: {subject}\n\n{body}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(full_template)
        
        messagebox.showinfo("Copied", "Email template copied to clipboard!")
    
    def show_statistics(self):
        """Show email automation statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT 
            COUNT(*) as total_templates,
            AVG(effectiveness_score) as avg_effectiveness,
            SUM(usage_count) as total_usage
        FROM email_templates
        ''')
        
        stats = cursor.fetchone()
        
        cursor.execute('''
        SELECT category, COUNT(*) 
        FROM email_templates 
        GROUP BY category
        ''')
        
        categories = cursor.fetchall()
        conn.close()
        
        # Calculate time savings
        avg_email_time_before = 8  # minutes
        avg_email_time_after = 2   # minutes
        time_saved_per_email = avg_email_time_before - avg_email_time_after
        total_emails = stats[2] if stats[2] else 100  # Default assumption
        total_time_saved = (total_emails * time_saved_per_email) / 60  # hours
        
        stats_message = f"""📊 EMAIL AUTOMATION STATISTICS
        
📧 Template Portfolio:
• Total Templates: {stats[0]}
• Average Effectiveness: {stats[1]:.1f}/10
• Total Usage: {total_emails} emails processed

⏱️ Time Savings Analysis:
• Time per email before: {avg_email_time_before} minutes
• Time per email after: {avg_email_time_after} minutes
• Time saved per email: {time_saved_per_email} minutes
• Total time saved: {total_time_saved:.1f} hours

💰 Business Value:
• Hourly rate assumption: $50
• Total value generated: ${total_time_saved * 50:.0f}
• Monthly value (est): ${(total_time_saved * 50) / 3:.0f}

📁 Template Categories:"""
        
        for category, count in categories:
            stats_message += f"\n• {category}: {count} templates"
        
        messagebox.showinfo("Automation Statistics", stats_message)
    
    def export_templates(self):
        """Export templates summary"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        SELECT template_name, category, subject_line, usage_count, effectiveness_score
        FROM email_templates
        ORDER BY category, template_name
        ''')
        
        templates = cursor.fetchall()
        conn.close()
        
        export_text = "EMAIL TEMPLATE PORTFOLIO EXPORT\n"
        export_text += "=" * 50 + "\n\n"
        
        current_category = ""
        for template in templates:
            name, category, subject, usage, effectiveness = template
            
            if category != current_category:
                export_text += f"\n📁 {category.upper()}\n"
                export_text += "-" * 30 + "\n"
                current_category = category
            
            export_text += f"• {name}\n"
            export_text += f"  Subject: {subject}\n"
            export_text += f"  Usage: {usage} times | Effectiveness: {effectiveness}/10\n\n"
        
        # Copy to clipboard
        self.root.clipboard_clear()
        self.root.clipboard_append(export_text)
        
        messagebox.showinfo("Exported", "Template portfolio exported to clipboard!")
    
    def run(self):
        """Start the GUI application"""
        self.root.mainloop()

def main():
    """Main execution"""
    print("📧 **EMAIL AUTOMATION GUI v1.0**")
    print("Professional email template system")
    print("=" * 50)
    
    try:
        app = EmailAutomationGUI()
        print("✅ Email automation system initialized")
        print("🚀 Opening GUI interface...")
        app.run()
        
    except Exception as e:
        print(f"❌ **Error:** {str(e)}")
        print("🔧 **Resolution:** Check dependencies and database")

if __name__ == "__main__":
    main()