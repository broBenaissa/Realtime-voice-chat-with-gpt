import pyaudio
import wave
import speech_recognition as sr

CHUNK = 8096
FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
WAVE_OUTPUT_FILENAME = "audio.wav"


r = sr.Recognizer()

def listen_for_keyword():
    with sr.Microphone() as source:
        print("Listening for keyword...")
        audio = r.listen(source)
        print(audio)

    try:
        transcript = r.recognize_google(audio)
        print("Heard:", transcript)
        if "g" in transcript:
            print('Start recording')
            return True
        else:
            return False
    except sr.UnknownValueError:
        return False
    except sr.RequestError:
        print("Speech recognition service is unavailable.")
        return False

def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    frames = []

    print("Recording...")

    recording = True
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
        if listen_for_keyword():
            recording = False

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

record_audio()
