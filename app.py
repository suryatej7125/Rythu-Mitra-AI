import os
import uuid
import subprocess
import requests

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from brain import get_agriculture_answer
from gnani.tts import GnaniTTSClient, AudioConfig

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("GNANI_API_KEY")
STT_URL = "https://api.vachana.ai/stt/v3"

UPLOAD_FOLDER = "samples"
OUTPUT_FOLDER = "static/audio"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

client = GnaniTTSClient(api_key=API_KEY)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/ask", methods=["POST"])
def ask_farmer():

    if "audio" not in request.files:
        return jsonify({"error": "No audio received"}), 400

    uploaded_audio = request.files["audio"]

    if not uploaded_audio.filename:
        return jsonify({"error": "Empty audio file"}), 400

    unique_id = str(uuid.uuid4())

    original_file = os.path.join(
        UPLOAD_FOLDER, unique_id + "_original"
    )

    wav_file = os.path.join(
        UPLOAD_FOLDER, unique_id + ".wav"
    )

    try:
        uploaded_audio.save(original_file)

        # Convert browser audio to WAV
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-i", original_file,
                "-vn",
                "-acodec", "pcm_s16le",
                "-ar", "16000",
                "-ac", "1",
                wav_file
            ],
            check=True,
            capture_output=True
        )

        # STEP 1: Speech to Text
        headers = {
            "X-API-Key-ID": API_KEY
        }

        data = {
            "language_code": "te-IN",
            "preferred_language": "te-IN",
            "format": "transcribe",
            "itn_native_numerals": "true"
        }

        with open(wav_file, "rb") as audio:
            files = {
                "audio_file": (
                    "farmer.wav", audio, "audio/wav"
                )
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
            return jsonify({
                "error": "Speech recognition failed"
            }), 500

        question = stt_result["transcript"]

        # STEP 2: Agricultural Brain
        answer = get_agriculture_answer(question)

        telugu_answer = answer["answer_te"]

        # STEP 3: Text to Speech
        generated_audio = client.synthesize(
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

        audio_filename = unique_id + ".wav"

        audio_path = os.path.join(
            OUTPUT_FOLDER, audio_filename
        )

        with open(audio_path, "wb") as file:
            file.write(generated_audio)

        return jsonify({
            "success": True,
            "question": question,
            "answer": telugu_answer,
            "audio_url": "/static/audio/" + audio_filename,
            "source": answer.get("source", "No source specified"),
            "knowledge_found": answer["success"]
        })

    except Exception as error:
        print("APPLICATION ERROR:", str(error))

        return jsonify({
            "error": "Something went wrong. Please try again."
        }), 500

    finally:
        for path in [original_file, wav_file]:
            if os.path.exists(path):
                os.remove(path)

@app.route("/api/ask-text", methods=["POST"])
def ask_text():

    data = request.get_json()

    if not data or not data.get("question", "").strip():
        return jsonify({
            "error": "Please enter a farming question."
        }), 400

    try:
        question = data["question"].strip()

        # STEP 1: Agricultural Brain
        answer = get_agriculture_answer(question)

        telugu_answer = answer["answer_te"]

        # STEP 2: Generate Telugu Voice
        generated_audio = client.synthesize(
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

        audio_filename = str(uuid.uuid4()) + ".wav"

        audio_path = os.path.join(
            OUTPUT_FOLDER,
            audio_filename
        )

        with open(audio_path, "wb") as file:
            file.write(generated_audio)

        return jsonify({
            "success": True,
            "question": question,
            "answer": telugu_answer,
            "source": answer.get("source", "No source specified"),
            "audio_url": "/static/audio/" + audio_filename,
            "source": answer.get("source", "No source specified"),
            "knowledge_found": answer["success"]
        })

    except Exception as error:

        print("TEXT APPLICATION ERROR:", str(error))

        return jsonify({
            "error": "Unable to process your question. Please try again."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)