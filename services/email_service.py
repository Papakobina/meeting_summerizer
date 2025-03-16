import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailService:
    def __init__(self):
        # Get email configuration from environment variables
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("EMAIL_PASSWORD")
        
        # Validate configuration
        if not all([self.smtp_server, self.smtp_port, self.sender_email, self.sender_password]):
            raise ValueError("Missing email configuration. Check your .env file.")
    
    def send_meeting_summary(self, recipient_emails, meeting_name, summary, action_items):
        """
        Send meeting summary and action items via email
        
        Args:
            recipient_emails (list): List of email addresses to send to
            meeting_name (str): Name/subject of the meeting
            summary (str): Meeting summary text
            action_items (list): List of action items
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        if not recipient_emails:
            return False
            
        try:
            # Create message
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = ", ".join(recipient_emails)
            message["Subject"] = f"Meeting Summary: {meeting_name}"
            
            # Create HTML content
            html_content = f"""
            <html>
              <head>
                <style>
                  body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; color: #333; }}
                  .container {{ max-width: 600px; margin: 0 auto; }}
                  h1 {{ color: #2c3e50; font-size: 24px; }}
                  h2 {{ color: #3498db; font-size: 20px; margin-top: 20px; }}
                  ul {{ padding-left: 20px; }}
                  li {{ margin-bottom: 8px; }}
                  .footer {{ margin-top: 30px; font-size: 12px; color: #7f8c8d; }}
                </style>
              </head>
              <body>
                <div class="container">
                  <h1>Meeting Summary: {meeting_name}</h1>
                  <hr>
                  <h2>Summary</h2>
                  <p>{summary}</p>
                  
                  <h2>Action Items</h2>
                  <ul>
            """
            
            # Add action items to HTML content
            if action_items and len(action_items) > 0:
                for item in action_items:
                    html_content += f"<li>{item}</li>"
            else:
                html_content += "<li>No action items identified</li>"
                
            # Add footer
            html_content += """
                  </ul>
                  <div class="footer">
                    <p>This summary was automatically generated using AI.</p>
                  </div>
                </div>
              </body>
            </html>
            """
            
            # Attach HTML content
            message.attach(MIMEText(html_content, "html"))
            
            # Connect to server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
                
            return True
            
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return False