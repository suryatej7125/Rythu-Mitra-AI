import os
import requests

from dotenv import load_dotenv
from brain import get_agriculture_answer
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")

STT_URL = "https://api.vachana.ai/stt/v3"

AUDIO_FILE = "samples/farmer_question.wav"

if not API_KEY:
    raise ValueError("Gnani API key missing!")

print("\n================================")
print("       🌱 RYTHU MITRA AI")
print(" Your Farm. Your Language. AI")
print("================================")

# STEP 1: SPEECH TO TEXT

print("\n🎙️ Processing farmer's voice...")

headers = {
    "X-API-Key-ID": API_KEY
}

data = {
    "language_code": "te-IN",
    "preferred_language": "te-IN",
    "format": "transcribe",
    "itn_native_numerals": "true"
}

with open(AUDIO_FILE, "rb") as audio:
    files = {
        "audio_file": ("farmer_question.wav", audio, "audio/wav")
    }

    response = requests.post(
        STT_URL,
        headers=headers,
        data=data,
        files=files,
        timeout=60
    )

response.raise_for_status()

stt_result = response.json()

if not stt_result.get("success"):
    raise Exception("Speech recognition failed!")

farmer_question = stt_result["transcript"]

print("\n👨‍🌾 FARMER ASKED:")
print(farmer_question)


# STEP 2: AGRICULTURAL INTELLIGENCE

print("\n🧠 RYTHU MITRA AI IS THINKING...")

answer = get_agriculture_answer(farmer_question)

telugu_answer = answer["answer_te"]

print("\n🌾 AGRICULTURAL RESPONSE:")
print(telugu_answer)


# STEP 3: TEXT TO SPEECH

print("\n🗣️ GENERATING TELUGU VOICE...")

client = GnaniTTSClient(api_key=API_KEY)

audio_output = client.synthesize(
    telugu_answer,
    voice="Yukti",
    model="timbre-v2.5",
    language="te-IN",
    speed=1.0,
    audio_config=AudioConfig(
        container="wav",
        sample_rate=48000
    )
)

output_file = "rythu_mitra_response.wav"

with open(output_file, "wb") as file:
    file.write(audio_output)

print("\n================================")
print("       SUCCESS! 🎉")
print("================================")

print("\n🔊 Telugu voice response saved!")
print("File:", output_file)

print("\n🌱 RYTHU MITRA AI COMPLETED ITS TASK!")