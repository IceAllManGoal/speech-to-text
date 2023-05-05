from gtts import gTTS
import os

def speach(text: str):
    audio = gTTS(text=text, lang="ru", slow=False)
    audio.save("test.mp3")
