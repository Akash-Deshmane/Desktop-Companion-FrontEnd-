

import pyttsx3 as tts

def onstart(name):
    print("Start to speak")

def onend(name,completed):
    print("done speaking")

engine=tts.init()
engine.connect("started-utterance",onstart)
engine.connect("finished-utterance",onend)

name = input("somthing:")


rate=engine.getProperty('rate')

engine.setProperty('rate',140)

voices=engine.getProperty('voices')

engine.setProperty('voice',voices[1].id)


engine.say(str(name))
engine.runAndWait()