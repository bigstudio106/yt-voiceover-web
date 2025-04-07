
from flask import Flask, render_template, request, send_file
import requests
from pydub import AudioSegment
import os
from io import BytesIO

app = Flask(__name__)

VOICE_OPTIONS = {
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
    "Adam": "pNInz6obpgDQGcFmaJgB"
}

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        api_key = request.form["api_key"]
        voice_name = request.form["voice"]
        script = request.form["script"]
        filename = request.form["filename"] or "voiceover"

        voice_id = VOICE_OPTIONS[voice_name]
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
        data = {
            "text": script,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.8
            }
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                main_audio = AudioSegment.from_file(BytesIO(response.content), format="mp3")

                final_audio = AudioSegment.empty()
                if os.path.exists("intro.mp3"):
                    final_audio += AudioSegment.from_mp3("intro.mp3")
                final_audio += main_audio
                if os.path.exists("outro.mp3"):
                    final_audio += AudioSegment.from_mp3("outro.mp3")

                output = BytesIO()
                final_audio.export(output, format="mp3")
                output.seek(0)

                return send_file(output, as_attachment=True, download_name=f"{filename}.mp3", mimetype="audio/mpeg")
            else:
                return f"API Error: {response.text}", 400
        except Exception as e:
            return f"Error: {str(e)}", 500

    return render_template("index.html", voices=VOICE_OPTIONS.keys())
