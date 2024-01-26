from flask import Flask, Response
import requests
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
import os

load_dotenv()

voice_id = os.environ["ELEVENLABS_VOICE_ID"]
xi_api_key = os.environ["ELEVENLABS_XI_API_KEY"]


# ElevenLabs constants
OPTIMIZE_STREAMING_LATENCY = "3"
MODEL_ID = "eleven_monolingual_v1"
STABILITY = 0.5
SIMILARITY_BOOST = 0.5
OUTPUT_FORMAT = "mp3_44100_64"
TEXT = "Thank you for calling Owl Bank! Please choose from one of the following options"

# ElevanLabs API requst data
eleven_labs_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream?optimize_streaming_latency={OPTIMIZE_STREAMING_LATENCY}&output_format={OUTPUT_FORMAT}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": xi_api_key,
}
data = {
    "text": TEXT,
    "model_id": MODEL_ID,
    "voice_settings": {"stability": STABILITY, "similarity_boost": SIMILARITY_BOOST},
}

# Flask
app = Flask(__name__)


@app.route("/twiml", methods=["GET", "POST"])
def twiml_route():
    twiml = VoiceResponse()
    twiml.play("/audio")
    return Response(str(twiml), mimetype="text/xml")


@app.route("/audio", methods=["GET"])
def audio_route():
    elevan_lab_response = requests.post(eleven_labs_url, json=data, headers=headers)
    response = Response(elevan_lab_response.content, content_type="audio/mpeg")
    return response


if __name__ == "__main__":
    app.run(debug=True)
