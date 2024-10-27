from fastapi import FastAPI, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai

# Fetch the OpenAI API key from environment variables
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
import logging
logging.basicConfig(level=logging.INFO)


# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific domains if necessary
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

def get_transcription(wav_file_path):
    """Transcribe audio from a WAV file using OpenAI's Whisper model."""
    try:
        with open(wav_file_path, "rb") as audio_file:
            result = openai.Audio.transcribe(model="whisper-1", file=audio_file, language='en')
        return result['text'].strip()
    except Exception as e:
        logging.error(f"Transcription error: {str(e)}")
        return ''

def get_response(prompt: str) -> str:
    """Generate a response from the OpenAI API using the provided transcript."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": prompt}],
            temperature=0.0
        )
        return response.choices[0].message.content
    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API error: {str(e)}")
    except KeyError as e:
        logging.error(f"Key error: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
    return ''


@app.post("/transcribe-audio/")
async def transcribe_audio(file: UploadFile):
    """API endpoint for transcribing audio files."""
    if file.content_type != "audio/wav":
        raise HTTPException(status_code=400, detail="Only WAV files are supported.")
    
    try:
        file_path = f"/tmp/{file.filename}"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Here you may also want to log that the file was written successfully
        logging.info(f"File saved to {file_path}")

        transcription = get_transcription(file_path)
        return {"transcription": transcription}
    except Exception as e:
        logging.error(f"Failed to transcribe audio: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to transcribe audio.")


@app.post("/generate-response/")
async def generate_response(request: PromptRequest):
    """API endpoint for generating a response based on a prompt."""
    prompt = request.prompt
    response_text = get_response(prompt)
    if response_text:
        return {"response": response_text}
    else:
        raise HTTPException(status_code=500, detail="Failed to generate response.")
