import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def summarize_transcript(transcript_text):
    """
    Summarize meeting transcript and extract action items using OpenAI GPT
    
    Args:
        transcript_text (str): Transcribed meeting text
        
    Returns:
        dict: Dictionary containing summary and action items
    """
    if not transcript_text:
        return {
            "summary": "No transcript provided.",
            "action_items": []
        }
    
    try:
        # Create system prompt for better structure
        system_prompt = """
        You are an AI assistant specialized in summarizing meetings and extracting action items.
        Provide your response in the following format:
        
        # MEETING SUMMARY
        [Concise meeting summary here]
        
        # ACTION ITEMS
        1. [Action] - Assigned to: [Name] - Deadline: [Date]
        2. [Action] - Assigned to: [Name] - Deadline: [Date]
        ...
        """
        
        # User prompt with the transcript
        user_prompt = f"""
        Please summarize this meeting transcript clearly, and extract all action items, 
        responsible individuals, and deadlines.
        
        TRANSCRIPT:
        {transcript_text}
        """
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o",  # You can use gpt-3.5-turbo for lower cost
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.5,  # Lower temperature for more factual responses
            max_tokens=1000   # Adjust based on your needs
        )
        
        # Extract response
        processed_content = response.choices[0].message.content
        
        # Simple parsing - you can make this more sophisticated
        # Split into summary and action items sections
        parts = processed_content.split("# ACTION ITEMS")
        summary = parts[0].replace("# MEETING SUMMARY", "").strip()
        
        # Extract action items if available
        action_items = []
        if len(parts) > 1:
            action_text = parts[1].strip()
            if action_text:
                # Split by numbered items and filter empty strings
                raw_items = [item.strip() for item in action_text.split("\n") 
                            if item.strip() and any(c.isdigit() for c in item[:2])]
                action_items = [item[item.find(" ")+1:].strip() for item in raw_items]
        
        return {
            "summary": summary,
            "action_items": action_items
        }
        
    except Exception as e:
        print(f"Summarization error: {str(e)}")
        return {
            "summary": f"Error during summarization: {str(e)}",
            "action_items": []
        }

if __name__ == "__main__":
    # Test with a sample transcript
    test_transcript = """
    John: Hi everyone, thanks for joining today's project update.
    Sarah: Thanks John, let's start with the frontend progress.
    John: Sure. We've completed the user authentication module, but we're behind on the dashboard.
    Sarah: I can help with that. I'll take on the dashboard components and aim to finish by Friday.
    Mike: Great. For the API integration, I need Sam to provide the endpoint documentation by Wednesday.
    Sam: I'll send it by tomorrow afternoon.
    John: Perfect. Last thing - we need to schedule the user testing session.
    Mike: I can organize that for next Monday.
    John: Great, let's wrap up. Next meeting is scheduled for Thursday at 2pm.
    """
    
    result = summarize_transcript(test_transcript)
    print("\nSUMMARY:")
    print(result["summary"])
    print("\nACTION ITEMS:")
    for item in result["action_items"]:
        print(f"- {item}")