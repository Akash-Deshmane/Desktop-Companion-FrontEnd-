import speech_recognition as sr
import pyttsx3
import os
import pyautogui
import subprocess

# volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# brightness
import screen_brightness_control as sbc

engine = pyttsx3.init()

def speak(text):
    print(text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except:
        return ""

# 🔊 Volume Control
def set_volume(level):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(level, None)

# 🔁 MAIN LOOP
while True:
    command = take_command()

    # 📂 OPEN APPS
    if "open notepad" in command:
        os.system("notepad")
      
        speak("Opening Notepad")

    elif "open word" in command:
        os.system("start winword")
        speak("Opening Word")

    elif "open chrome" in command:
        os.system("start chrome")
        speak("Opening Chrome")

    # ✍️ TYPE TEXT IN WORD / ANY APP
    elif "typing" in command:
        text = command.replace("typing", "")
        pyautogui.write(text, interval=0.05)
        speak("Writing text")

    # 🔊 VOLUME
    elif "volume up"in front of my friends  in command:
        set_volume(1.0)
        speak("Volume max")

    elif "volume down" in command:
        set_volume(0.2)
        speak("Volume low")

    # 💡 BRIGHTNESS
    elif "brightness up" in command:
        sbc.set_brightness(100)
        speak("Brightness max")

    elif "brightness down" in command:
        sbc.set_brightness(30)
        speak("Brightness low")

    # 🪟 WINDOW CONTROL
    elif "minimize window" in command:
        pyautogui.hotkey("win", "down")

    elif "maximize window" in command:
        pyautogui.hotkey("win", "up")

    elif "close window" in command:
        pyautogui.hotkey("alt", "f4")

    # 🖱️ MOUSE CONTROL (basic)
    elif "move mouse up" in command:
        pyautogui.moveRel(0, -100)

    # ❌ EXIT
    elif "exit" in command:
        speak("Goodbye")
        break

    else:
        speak("Command not recognized")