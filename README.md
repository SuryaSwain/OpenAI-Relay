# OpenAI API Relay Service

This project is a FastAPI-based relay service for interacting with the OpenAI API. It provides endpoints for audio transcription using OpenAI's Whisper model and for generating responses based on text prompts with OpenAI's GPT-3.5 model.

## Features

- **Audio Transcription**: Accepts `.wav` audio files and returns a transcription of the spoken content.
- **Text Prompt Response Generation**: Accepts a text prompt and returns a generated response using OpenAI's language model.

## Project Structure

```plaintext
.
├── main.py              # FastAPI application and endpoint definitions
├── requirements.txt     # Dependencies for the project
├── keys.py              # Stores OpenAI API key
└── README.md            # Project documentation
```


## Installation (Local)

### Prerequisites

- Python 3.7 or higher
- OpenAI API key (store in `keys.py` file as `OPENAI_API_KEY`)

### Setup

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/OpenAI-API-Relay.git
    cd OpenAI-API-Relay
    ```

2. **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

3. **Configure OpenAI API Key**

    Add your OpenAI API key to a file named `keys.py`:

    ```python
    # keys.py
    OPENAI_API_KEY = "your_openai_api_key_here"
    ```


### Run the FastAPI Server (Local)

Start the server with `uvicorn`:

```bash
uvicorn main:app --reload
```

The service will be available at `http://127.0.0.1:8000`.

## Render.com Settings

1. **Environment**: Python
2. **Build Command**: 
   ```bash
   pip install -r requirements.txt
   ```
3. **Start Command**: 
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   (Replace `main:app` with `<filename>:<app_instance>` if your file or app instance names differ.)

4. **Environment Variables**:
   - **Key**: `OPENAI_API_KEY`
   - **Value**: *(your actual OpenAI API key)*

This configuration will set up your FastAPI app to run on Render.com.


## API Endpoints

### 1. Transcribe Audio

- **Endpoint**: `/transcribe-audio/`
- **Method**: `POST`
- **Content-Type**: `multipart/form-data`
- **Parameter**: `file` (WAV audio file)

Example:

```bash
curl -X POST "http://127.0.0.1:8000/transcribe-audio/" -F "file=@/path/to/audio.wav"
```

**Response**:

```json
{
  "transcription": "Transcribed text from audio file"
}
```

### 2. Generate Response

- **Endpoint**: `/generate-response/`
- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**: JSON with `prompt` field

Example:

```bash
curl -X POST "http://127.0.0.1:8000/generate-response/" -H "Content-Type: application/json" -d '{"prompt": "Your prompt here"}'
```

**Response**:

```json
{
  "response": "Generated response from OpenAI model"
}
```

### Error Handling

The API returns user-friendly error messages and logs errors internally for debugging. Make sure to check the logs for details in case of any issues.


## Using the endpoints in Python code

### Prerequisites

Ensure you have the `requests` library installed:
```bash
pip install requests
```

### Python Code to Use the Endpoints

```python
import requests

# Base URL for your FastAPI server
BASE_URL = "http://127.0.0.1:8000"

# Endpoint 1: Transcribe Audio
def transcribe_audio(file_path):
    url = f"{BASE_URL}/transcribe-audio/"
    with open(file_path, "rb") as audio_file:
        files = {"file": audio_file}
        try:
            response = requests.post(url, files=files)
            response.raise_for_status()  # Check for HTTP errors
            transcription = response.json().get("transcription")
            print("Transcription:", transcription)
            return transcription
        except requests.exceptions.RequestException as e:
            print("Error during transcription:", e)
            return None

# Endpoint 2: Generate Response
def generate_response(prompt):
    url = f"{BASE_URL}/generate-response/"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": prompt}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Check for HTTP errors
        generated_response = response.json().get("response")
        print("Generated Response:", generated_response)
        return generated_response
    except requests.exceptions.RequestException as e:
        print("Error generating response:", e)
        return None

# Example Usage
if __name__ == "__main__":
    # Transcribe audio from a WAV file
    transcription = transcribe_audio("/path/to/audio.wav")

    # Generate response from a prompt
    prompt = "What is the weather today?"
    response = generate_response(prompt)
```

### Explanation of the Code

- **`transcribe_audio` Function**: Opens a WAV audio file, sends it to the `/transcribe-audio/` endpoint using a `POST` request with `multipart/form-data`, and retrieves the transcription.
- **`generate_response` Function**: Sends a `POST` request with a JSON payload to the `/generate-response/` endpoint, including the prompt, and retrieves the generated response.
  
Replace `"/path/to/audio.wav"` with the actual path to your audio file and run the script to test the endpoints. The output will display the transcription and generated responses.


## Acknowledgments

- [OpenAI](https://openai.com/) for the GPT and Whisper models
- [FastAPI](https://fastapi.tiangolo.com/) for the robust API framework


