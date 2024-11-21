import io
import os

from flask import Flask, render_template, request, jsonify
import openai
from pydub import AudioSegment
import base64

from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPEN_AI_KEY")
openai.organization = os.getenv("OPEN_AI_ORG")


def create_app():
    app = Flask(__name__)

    # Directory to save audio files
    UPLOAD_FOLDER = "uploads"
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/transcribe", methods=["POST"])
    def transcribe():
        file = request.files["audio"]
        buffer = io.BytesIO(file.read())
        buffer.name = "audio.webm"

        audio_file = None

        transcript = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

        return {"output": transcript.text}

    @app.route("/upload", methods=["POST"])
    def upload_audio():
        if "audio" not in request.files:
            return jsonify({"error": "No audio data received"}), 400

        file = request.files["audio"]
        input_path = os.path.join(app.config["UPLOAD_FOLDER"], "temp.webm")
        output_path = os.path.join(app.config["UPLOAD_FOLDER"], "recording.mp3")

        file.save(input_path)


    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
