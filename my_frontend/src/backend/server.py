from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from whisper import load_model
import openai, config, json,real
import speech_recognition as sr

model = load_model("tiny")
r = sr.Recognizer()

openai.api_key = config.OPENAI_API_KEY

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    print(audio_path)
    #result = r.recognize_google(audio_path)
    
    return (result["text"])


@app.get("/")
async def get_result():
    audio_path = "./audio.wav"
    data = transcribe_audio(audio_path)
    with open("./audio.json", "w") as file:
        json.dump({"result": data}, file)
        
    return {"result": data}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
