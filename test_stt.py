import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")

URL = "https://api.vachana.ai/stt/v3"

AUDIO_FILE = "samples/farmer_question.wav"

if not API_KEY:
    raise ValueError("Gnani API key missing from .env file")

if not os.path.exists(AUDIO_FILE):
    raise FileNotFoundError("Audio file not found!")

headers = {
    "X-API-Key-ID": API_KEY
}

data = {
    "language_code": "te-IN",
    "preferred_language": "te-IN",
    "format": "transcribe",
    "itn_native_numerals": "true"
}

print("Sending farmer's audio to Gnani...")

with open(AUDIO_FILE, "rb") as audio:

    files = {
        "audio_file": ("farmer_question.wav", audio, "audio/wav")
    }

    response = requests.post(
        URL,
        headers=headers,
        data=data,
        files=files,
        timeout=60
    )

print("\nHTTP Status:", response.status_code)

response.raise_for_status()

result = response.json()

print("\nGnani API Response:")
print(result)

if result.get("success"):
    print("\nTELUGU TRANSCRIPTION:")
    print(result.get("transcript"))