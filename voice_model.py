import speech_recognition as sr
import pyttsx3 as ttx
import time
import os
import wikipedia as w
import time 
import pyautogui as pgui

r = sr.Recognizer()

apps = {
    # System Apps
    "notepad": "notepad",
    "paint": "mspaint",
    "calculator": "calc",
    "cmd": "cmd",
    "task manager": "taskmgr",
    "control panel": "control",

    # Microsoft Office
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "access": "msaccess",
    "outlook": "outlook",

    # Browsers
    "chrome": "chrome",
    "edge": "msedge",
    "firefox": "firefox",
    "brave": "brave",

    # Editors & Dev Tools
    "vs code": "code",
    "notepad++": "notepad++",
    "pycharm": "pycharm64",
    "intellij": "idea64",

    # Media
    "vlc": "vlc",
    "windows media player": "wmplayer",

    # Communication
    "whatsapp": r"wDesktop\WhatsApp.Ink",
    "telegram": "telegram",
    "discord": "discord",
    "zoom": "zoom",

    # Design
    "photoshop": "photoshop",
    "illustrator": "illustrator",
    "canva": "canva",

    # File tools
    "explorer": "explorer",
    "7zip": "7zfm",
    "winrar": "winrar"
}



def speak(text):
    engine = ttx.init()
    engine.stop() 
    engine.setProperty('rate', 145)
    engine.say(text)
    engine.runAndWait()
    time.sleep(0.2)  # small buffer

running = True

while running:
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source, duration=1)
        

        audio = r.listen(source, phrase_time_limit=8)
        text = r.recognize_google(audio).lower()

        print("You said:", text)

        if "open" in text:
            text.replace("open","")
            for app in apps:
                if app in text:
                     speak( text)
                     os.system(f'start "" "{apps[app]}"')  
                     time.sleep(2)  
        elif "typing" in text:
            speak("What should I type?")
    
            with sr.Microphone() as source:
                audio = r.listen(source)
                content = r.recognize_google(audio)
        
            print("Writing:", content)
            speak("Writing now")
        
            pgui.write(content, interval=0.05)   

        elif "wikipedia" in text:
            info=w.summary(text, sentences=2)
            print(info)
            speak(info)
        elif "go back" in text:
            speak("You're welcome")
            running = False
        else:
            print("don't understand")

        
