from gtts import gTTS

audio = gTTS (text ='yes', lang='en',slow=False, tld='us')
audio.save('yesSir.mp3')