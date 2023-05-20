
from flask import Flask, jsonify
from flask_cors import CORS
import openai,config,json
import real
from whisper import load_model

model = load_model("tiny")
openai.api_key = config.OPENAI_API_KEY
app = Flask(__name__)
CORS(app)

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    print(result["text"])
    return (result["text"])


# API Route
@app.route('/')
def get_result():
    audio_path = "./audio.wav"
    data = transcribe_audio(audio_path)
    with open("./audio.json", "w") as file:
        json.dump({"result": data}, file)
    return jsonify({"result": data})


if __name__ == "__main__":
    app.run(debug=True)
