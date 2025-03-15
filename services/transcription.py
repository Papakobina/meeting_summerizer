import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()

def transcribe_audio(file_path):
    """
    Transcribe an audio file using OpenAI's Whisper model.
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        str: Transcribed text
    """
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
            
        return transcription.text
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Transcription error: {str(e)}")
        return None

def transcribe_uploaded_file(uploaded_file_path):
    """
    Wrapper function to handle files uploaded through the web interface
    
    Args:
        uploaded_file_path (str): Path where the uploaded file is saved
        
    Returns:
        str: Transcribed text
    """
    return transcribe_audio(uploaded_file_path)

if __name__ == '__main__':
    
    sample_file = "./audio_files/audio.mp3"
    if os.path.exists(sample_file):
        result = transcribe_audio(sample_file)
        print(result)
    else:
        print(f"Test file not found at {sample_file}")