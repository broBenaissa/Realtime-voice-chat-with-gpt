import gradio as gr
audio= gr.Microphone
import openai, config
from whisper import load_model
my_key=config.OPENAI_API_KEY

model = load_model("tiny")

def transcrib(audio):
    print(audio)
    test_audio='/audio.mp3'
    audio_file=open(audio,'rb')
    result = model.transcribe(test_audio)
   
    return   result['text']

audio_input = gr.inputs.Audio(source='microphone')
text_output = gr.outputs.Textbox()
mydemo = gr.Interface(fn=transcrib, inputs=audio_input, outputs=text_output, capture_session=True)
mydemo.launch(share= True)  



