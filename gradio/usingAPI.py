import gradio as gr
from gtts import gTTS
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
import os 
import openai, config
openai.api_key = config.OPENAI_API_KEY

messages = [{"role": "system", "content": 'You are a benaissaChatBot .speak only english.you are a teacher. Respond to all input in 20 words or less.'}]

def transcribe(audio):
    global messages

    audio_filename_with_extension = audio + '.wav'
    os.rename(audio, audio_filename_with_extension)
    
    audio_file = open(audio_filename_with_extension, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    messages.append({"role": "user", "content": transcript["text"]})

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    system_message = response["choices"][0]["message"]
    messages.append(system_message)

    # read openai response using google text to speech
    last_message = messages[-1]
    assistant_response = last_message["content"]
    audio= gTTS (text =assistant_response, lang='fr',slow=False)

    # read openai response using google text to speech
    last_message = messages[-1]
    assistant_response = last_message["content"]
    audio= gTTS (text =assistant_response, lang='en',slow=False)
            
    # read openai response using google text to speech
    last_message = messages[-1]
    assistant_response = last_message["content"]
    audio= gTTS (text =assistant_response, lang='en',slow=False, tld='us')
    
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

    chat_transcript = ""
    for message in messages:
        if message['role'] != 'system':
            chat_transcript += message['role'] + ": " + message['content'] + "\n\n"

    return chat_transcript

ui = gr.Interface(fn=transcribe,title='Voice chatGPT', inputs=gr.Audio(source="microphone", type="filepath"), outputs="text")
ui.launch(share=True , auth=("benaissa","benaissa"))