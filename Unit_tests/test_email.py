import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.email_service import EmailService
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_email_service():
    """Test email functionality directly"""
    try:
        # Create email service instance
        email_service = EmailService()
        
        # Test data
        recipients = ["kobinaaggrey13@gmail.com"]  # Replace with your email
        meeting_name = "Test Meeting Summary"
        summary = "This is a test summary for the meeting. We discussed project progress and next steps."
        action_items = [
            "Complete backend implementation - Assigned to: Dev Team - Due: Friday",
            "Prepare demo for stakeholders - Assigned to: Project Manager - Due: Next Tuesday",
            "Review documentation - Assigned to: Everyone - Due: End of week"
        ]
        
        # Send test email
        result = email_service.send_meeting_summary(
            recipient_emails=recipients,
            meeting_name=meeting_name,
            summary=summary,
            action_items=action_items
        )
        
        if result:
            print("Email sent successfully!")
        else:
            print("Email sending failed")
            
    except Exception as e:
        print(f"Error during email test: {str(e)}")

if __name__ == "__main__":
    test_email_service()