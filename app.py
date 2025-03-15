import os
import tempfile
import uvicorn
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from services.transcription import transcribe_audio
from services.summarization import summarize_transcript

app = FastAPI(title="Meeting Summarizer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the directory containing frontend files
frontend_dir = os.path.join(os.getcwd(), "front_end")

# Mount the static files directory
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
app.mount("/css", StaticFiles(directory=os.path.join(frontend_dir, "css")), name="css")
app.mount("/js", StaticFiles(directory=os.path.join(frontend_dir, "js")), name="js")

@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file"""
    return FileResponse(os.path.join(frontend_dir, "index.html"))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Meeting Summarizer API is running"}

@app.post("/process-meeting/")
async def process_meeting(file: UploadFile = File(...)):
    """
    Process meeting audio: transcribe, summarize and extract action items
    """
    # Validate file type
    if not file.filename.endswith(('.mp3', '.wav')):
        raise HTTPException(400, detail="Only MP3 and WAV files are supported")
    
    try:
        # Create temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp:
            temp.write(await file.read())
            temp_path = temp.name
        
        # Process the audio file
        transcript = transcribe_audio(temp_path)
        
        # Clean up temp file
        os.unlink(temp_path)
        
        if not transcript:
            return JSONResponse(
                status_code=500,
                content={"error": "Transcription failed"}
            )
        
        # Get summary and action items
        results = summarize_transcript(transcript)
        
        return {
            "transcript": transcript,
            "summary": results["summary"],
            "action_items": results["action_items"]
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Processing failed: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)