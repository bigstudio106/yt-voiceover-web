import os
import requests
from flask import Flask, render_template, request, send_file, make_response
from io import BytesIO
from dotenv import load_dotenv

load_dotenv()  # Optional: agar local .env file use kar rahe ho

app = Flask(__name__)

ELEVENLABS_API_KEY = os.environ.get('ELEVENLABS_API_KEY')
VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # You can change to your desired voice ID

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        audio = generate_voice(text)
        if audio:
            return send_file(audio, as_attachment=True, download_name="voiceover.mp3")
    response = make_response(render_template('index.html'))
    response.headers['X-Frame-Options'] = 'ALLOWALL'
    return response

def generate_voice(text):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }

    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        print("Error:", response.text)
        return None

if __name__ == '__main__':
    app.run(debug=True)
