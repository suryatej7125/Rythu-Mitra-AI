import os
from dotenv import load_dotenv
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

API_KEY = os.getenv("GNANI_API_KEY")

if not API_KEY:
    raise ValueError("Gnani API key missing from .env")

print("\n🌱 RYTHU MITRA AI")
print("Generating Telugu voice...")

# Connect to Gnani TTS
client = GnaniTTSClient(api_key=API_KEY)
# Telugu response
text = """
నమస్కారం రైతు సోదరా!
మీ పంట ఆరోగ్యంగా ఉండాలని కోరుకుంటున్నాము.
మీకు వ్యవసాయంలో సహాయం చేయడానికి రైతు మిత్ర AI సిద్ధంగా ఉంది.
"""

# Generate speech
audio = client.synthesize(
    text,
    voice="Yukti",
    model="timbre-v2.5",
    language="te-IN",
    speed=1.0,
    audio_config=AudioConfig(
        container="wav",
        sample_rate=48000
    )
)

# Save audio
output_file = "rythu_mitra_voice.wav"

with open(output_file, "wb") as file:
    file.write(audio)

print("\nSUCCESS! 🎉")
print("Telugu audio saved:", output_file)
print("Audio size:", len(audio), "bytes")