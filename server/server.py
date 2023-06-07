from flask import Flask
from flask_cors import CORS
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os
from fastapi.middleware.cors import CORSMiddleware
from whisper import load_model
import openai,realRecord,db
import speech_recognition as sr

model = load_model('tiny')
r = sr.Recognizer()

openai.api_key = os.getenv("OPENAI_API_KEY")
#system role
messages = [{"role": "system", "content": 'You are a benaissaChatBot .speak only english.you are clever. Respond to all input in 20 words or less.'}]


app = Flask(__name__)
#cors like get method
CORS(app)




def transcribe_audio(audio_path):
    result = model.transcribe(audio_path)
    Question = result["text"]
    return Question

def get_response(Question):
    #make user role
    messages.append({"role": "user", "content": Question})
    #get json response from openai
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    #get string value
    AI_response = response["choices"][0]["message"]["content"]
    return AI_response

def read_response(AI_response):
    #      last_message = messages[-1]
    #      assistant_response = last_message["content"]
    respo=gTTS (text =AI_response, lang='en',slow=False, tld='us')
    answer_path='./cache/answer.wav'
    respo.save(answer_path)
    respo = AudioSegment.from_file(answer_path, format="mp3")
    play(respo)
    return 0


@app.get("/data")
async def get_result():
    audio_path = "./cache/Question.wav"
    ask = transcribe_audio(audio_path)
    respo=get_response(ask)
    read_response(respo)

    db.collection.insert_one({'question': ask} )
    db.collection.insert_one({'answer2': respo} )
    data= 'User:'+ask+'\n'+'Assistante'+respo
    
    return data

#with open("realRecord.py") as record:
  #      exec(record.read())

if (__name__ == "__main__"):
   

    app.run(debug=True,host="127.0.0.1", port=8000)
