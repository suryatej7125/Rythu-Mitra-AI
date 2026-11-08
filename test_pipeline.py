import os
import requests
from dotenv import load_dotenv
from brain import get_agriculture_answer

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")
URL = "https://api.vachana.ai/stt/v3"
AUDIO_FILE = "samples/farmer_question.wav"

headers = {
    "X-API-Key-ID": API_KEY
}

data = {
    "language_code": "te-IN",
    "preferred_language": "te-IN",
    "format": "transcribe",
    "itn_native_numerals": "true"
}

print("\n🌱 RYTHU MITRA AI")
print("Your Farm. Your Language. Your AI Assistant.")
print("\nListening to farmer's question...")

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

response.raise_for_status()

result = response.json()

if result.get("success"):
    farmer_question = result.get("transcript", "")

    print("\n👨‍🌾 FARMER'S QUESTION:")
    print(farmer_question)

    print("\n🧠 RYTHU MITRA AI IS THINKING...")

    answer = get_agriculture_answer(farmer_question)

    print("\n🌾 RYTHU MITRA AI RESPONSE:")
    print(answer["answer_te"])

else:
    print("\nSpeech recognition failed.")
    print(result)