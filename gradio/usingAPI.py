import gradio as gr
from gtts import gTTS
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
import os,openai

from pymongo import MongoClient

client = MongoClient('mongodb+srv://benaissa:benaissamongodb@youssefcluster.ogkngyi.mongodb.net/') 
db = client['audio_chat_gpt']
collection = db['Historic']

openai.api_key = os.getenv("OPENAI_API_KEY")

messages = [{"role": "system", "content": 'Give me short response.You are a clever english assistant.Your goal is to help users.Answer in 20 words or liss'}
           
            ]

def transcribe(audio):
    global messages
    #make user audio
    audio_filename_with_extension = audio+'.wav'
    os.rename(audio, audio_filename_with_extension)
    audio_file = open(audio_filename_with_extension, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    transcript_content= transcript["text"]
    messages.append({"role": "user", "content": transcript_content})
    #openai messaging
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    system_message = response["choices"][0]["message"]
    messages.append(system_message)  
    # read openai response using google text to speech
    last_message = messages[-1]
    assistant_response = last_message["content"]
    audio = gTTS (text =assistant_response, lang='en',slow=False, tld='us')
    #give name and path to file 
    folder_path = "./responses"
    os.makedirs(folder_path, exist_ok=True)
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M")
    responseName=f"response{dt_string}.mp3"
    file_path = os.path.join(folder_path, responseName)
    audio.save(file_path)
    audio = AudioSegment.from_file(file_path, format="mp3")
    play(audio)

    #collection.insert_one({'question': transcript_content} )
    #collection.insert_one({'answer2': system_message} )
    #append messages to chat history
    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript
ui = gr.Interface(fn=transcribe,title='Voice chatGPT', inputs=gr.Audio(label='Record audio from here',
                  source="microphone", type="filepath",interactive=True,StopIteration=True), outputs="text",allow_flagging='never',
                  live=True,css=".gradio-container {background-color: #a9a9aa}")

ui.launch(favicon_path='./icon/icon.png',show_error=True,auth=("benaissa","benaissa"))