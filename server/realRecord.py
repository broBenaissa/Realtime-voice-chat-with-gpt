import pyaudio
import wave
import speech_recognition as sr
from numpy import array, int16
from scipy.io.wavfile import write
import numpy as np
import pyttsx3

CHUNK = 8096
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "./cache/Question.wav"
KEYWORD = 'ok'
ENDWORD = 'ok'
#initalisations
r = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0')
#functions
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def listen_for_startword():
    global KEYWORD
    with sr.Microphone() as source:
        print("Listening for start word...")
        audio = r.listen(source)

        try:
            transcript = r.recognize_google(audio)
            if KEYWORD in transcript:
                speak('yes sir')
                return True
        except sr.UnknownValueError:
            pass

        return False


def listen_for_endword():
    with sr.Microphone() as source:
        print("Listening for end word...")
        audio = r.listen(source)

        try:
            transcript = r.recognize_google(audio)
            if ENDWORD in transcript:
                speak('wait me sir')
                return True
        except sr.UnknownValueError:
            pass

        return False
    


while  True:    
    if (listen_for_startword()):
        print('')
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        #listen_for_endword()
        speak('wait me sir')
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        break
