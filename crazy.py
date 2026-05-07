import pyttsx3
import os
import requests
import wikipedia
import pyautogui
import speech_recognition as sr
import time
import datetime
import webbrowser
import screen_brightness_control as sbc
import psutil
import json
import re
import subprocess
import threading

# ---------------- CONFIG ----------------
WAKE_WORD = "jack"
active = False
OLLAMA_URL = "http://localhost:11434/api/generate"
current_active_app = None  # Track current active app for context
app_context_active = False  # Whether we're in app context mode

# ---------------- TTS ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.9)

def speak(text):
    """Speak text using TTS"""
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------------- APP DICTIONARY WITH SHORTCUTS ----------------
apps = {
    "notepad": {"path": "notepad.exe", "shortcuts": {"new": "ctrl+n", "save": "ctrl+s", "save as": "ctrl+shift+s", "open": "ctrl+o", "find": "ctrl+f", "replace": "ctrl+h", "select all": "ctrl+a", "copy": "ctrl+c", "cut": "ctrl+x", "paste": "ctrl+v", "undo": "ctrl+z", "redo": "ctrl+y", "print": "ctrl+p", "delete": "delete", "backspace": "backspace", "enter": "enter", "tab": "tab"}},
    "paint": {"path": "mspaint.exe", "shortcuts": {"new": "ctrl+n", "save": "ctrl+s", "open": "ctrl+o", "print": "ctrl+p", "undo": "ctrl+z", "redo": "ctrl+y", "select all": "ctrl+a", "copy": "ctrl+c", "paste": "ctrl+v", "crop": "ctrl+shift+x", "resize": "ctrl+w"}},
    "calculator": {"path": "calc.exe", "shortcuts": {"clear": "esc", "backspace": "backspace", "equals": "enter", "add": "+", "subtract": "-", "multiply": "*", "divide": "/"}},
    "cmd": {"path": "cmd.exe", "shortcuts": {"clear": "cls", "copy": "ctrl+c", "paste": "ctrl+v"}},
    "word": {"path": "winword.exe", "shortcuts": {"new": "ctrl+n", "save": "ctrl+s", "save as": "f12", "open": "ctrl+o", "print": "ctrl+p", "bold": "ctrl+b", "italic": "ctrl+i", "underline": "ctrl+u", "center": "ctrl+e", "left align": "ctrl+l", "right align": "ctrl+r", "justify": "ctrl+j", "undo": "ctrl+z", "redo": "ctrl+y", "find": "ctrl+f", "replace": "ctrl+h", "select all": "ctrl+a", "copy": "ctrl+c", "cut": "ctrl+x", "paste": "ctrl+v", "zoom in": "ctrl+]", "zoom out": "ctrl+[", "bullet points": "ctrl+shift+l"}},
    "excel": {"path": "excel.exe", "shortcuts": {"new": "ctrl+n", "save": "ctrl+s", "save as": "f12", "open": "ctrl+o", "print": "ctrl+p", "bold": "ctrl+b", "italic": "ctrl+i", "underline": "ctrl+u", "undo": "ctrl+z", "redo": "ctrl+y", "find": "ctrl+f", "replace": "ctrl+h", "select all": "ctrl+a", "copy": "ctrl+c", "cut": "ctrl+x", "paste": "ctrl+v", "formula": "=", "calculate now": "f9"}},
    "powerpoint": {"path": "powerpnt.exe", "shortcuts": {"new slide": "ctrl+m", "save": "ctrl+s", "open": "ctrl+o", "print": "ctrl+p", "bold": "ctrl+b", "italic": "ctrl+i", "underline": "ctrl+u", "undo": "ctrl+z", "redo": "ctrl+y", "present": "f5"}},
    "chrome": {"path": "chrome.exe", "shortcuts": {"new tab": "ctrl+t", "close tab": "ctrl+w", "reopen tab": "ctrl+shift+t", "new window": "ctrl+n", "incognito": "ctrl+shift+n", "bookmark": "ctrl+d", "find": "ctrl+f", "reload": "f5", "hard reload": "ctrl+f5", "zoom in": "ctrl+plus", "zoom out": "ctrl+minus", "history": "ctrl+h", "downloads": "ctrl+j", "dev tools": "f12", "back": "alt+left", "forward": "alt+right", "address bar": "ctrl+l"}},
    "vs code": {"path": "code.exe", "shortcuts": {"open file": "ctrl+o", "save": "ctrl+s", "save all": "ctrl+k s", "new file": "ctrl+n", "close file": "ctrl+w", "split editor": "ctrl+\\", "find": "ctrl+f", "replace": "ctrl+h", "comment line": "ctrl+/", "copy line": "ctrl+shift+d", "delete line": "ctrl+shift+k", "format document": "ctrl+shift+i", "run": "ctrl+f5", "debug": "f5", "terminal": "ctrl+`", "command palette": "ctrl+shift+p"}},
    "vlc": {"path": "vlc.exe", "shortcuts": {"play pause": "space", "fullscreen": "f", "mute": "m", "volume up": "ctrl+up", "volume down": "ctrl+down", "next": "n", "previous": "p", "stop": "s", "speed up": "]", "slow down": "[", "screenshot": "ctrl+s"}},
    "spotify": {"path": "Spotify.exe", "shortcuts": {"play pause": "space", "next": "ctrl+right", "previous": "ctrl+left", "volume up": "ctrl+up", "volume down": "ctrl+down", "mute": "ctrl+shift+down", "shuffle": "ctrl+s", "repeat": "ctrl+r", "like": "alt+shift+b"}},
    "discord": {"path": "Discord.exe", "shortcuts": {"mute": "ctrl+shift+m", "deafen": "ctrl+shift+d", "start call": "ctrl+`", "end call": "esc"}}
}

# ---------------- SYSTEM COMMANDS ----------------
def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent")
        return True
    except:
        speak("Could not change brightness")
        return False

def change_volume(action):
    try:
        if action == "up":
            pyautogui.press('volumeup', presses=5)
            speak("Volume increased")
        elif action == "down":
            pyautogui.press('volumedown', presses=5)
            speak("Volume decreased")
        elif action == "mute":
            pyautogui.press('volumemute')
            speak("Volume muted")
        return True
    except:
        speak("Could not change volume")
        return False

def take_screenshot():
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshot_{timestamp}.png"
        pyautogui.screenshot(filename)
        speak(f"Screenshot saved as {filename}")
        return True
    except:
        speak("Could not take screenshot")
        return False

def lock_screen():
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak("Computer locked")
        return True
    except:
        speak("Could not lock computer")
        return False

def shutdown_computer():
    speak("Shutting down in 10 seconds. Say cancel to abort.")
    for i in range(10, 0, -1):
        print(f"Shutdown in {i} seconds...")
        time.sleep(1)
    os.system("shutdown /s /t 1")
    return True

def restart_computer():
    speak("Restarting in 10 seconds. Say cancel to abort.")
    for i in range(10, 0, -1):
        print(f"Restart in {i} seconds...")
        time.sleep(1)
    os.system("shutdown /r /t 1")
    return True

def get_time():
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def get_date():
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {current_date}")

def search_web(query):
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}")

def minimize_all():
    pyautogui.hotkey('win', 'd')
    speak("Minimized all windows")

def close_window():
    pyautogui.hotkey('alt', 'f4')
    speak("Closed current window")

def open_app(app_name):
    """Open an application and enter app context mode"""
    global current_active_app, app_context_active
    
    if app_name in apps:
        app_info = apps[app_name]
        app_path = app_info["path"] if isinstance(app_info, dict) else app_info
        speak(f"Opening {app_name}")
        try:
            os.system(f'start {app_path}')
            time.sleep(2)
            current_active_app = app_name
            app_context_active = True
            speak(f"{app_name} is now open. I'm in {app_name} mode. You can say things like 'type hello', 'save', 'new file', 'select all', 'copy', 'paste', or say 'close app' to exit.")
            return True
        except:
            try:
                os.system(f'start "" "{app_path}"')
                time.sleep(2)
                current_active_app = app_name
                app_context_active = True
                speak(f"{app_name} is now open. I'm in {app_name} mode. Say 'close app' when you're done.")
                return True
            except:
                speak(f"Could not open {app_name}")
                return False
    return False

def send_app_shortcut(app_name, action):
    """Send keyboard shortcut to specific application"""
    if app_name in apps and isinstance(apps[app_name], dict):
        shortcuts = apps[app_name].get("shortcuts", {})
        if action in shortcuts:
            shortcut = shortcuts[action]
            if '+' in shortcut:
                keys = shortcut.split('+')
                pyautogui.hotkey(*keys)
            else:
                pyautogui.press(shortcut)
            speak(f"{action.capitalize()}")
            return True
    return False

def type_text(text):
    """Type text using pyautogui"""
    try:
        pyautogui.write(text, interval=0.05)
        display_text = text[:50] + "..." if len(text) > 50 else text
        speak(f"Typed: {display_text}")
        return True
    except Exception as e:
        speak("Could not type text")
        return False

def press_keys(keys):
    """Press keyboard shortcuts"""
    try:
        key_list = keys.split('+')
        pyautogui.hotkey(*key_list)
        speak(f"Pressed {keys}")
        return True
    except:
        speak(f"Could not press {keys}")
        return False

def get_system_info():
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    speak(f"CPU usage is {cpu} percent, Memory usage is {memory} percent")

def open_website(url):
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    speak(f"Opening {url}")

def close_active_app():
    """Close the currently active app and exit context mode"""
    global current_active_app, app_context_active
    if current_active_app:
        speak(f"Closing {current_active_app}")
        pyautogui.hotkey('alt', 'f4')
        time.sleep(1)
        current_active_app = None
        app_context_active = False
        speak("Application closed. Returning to normal mode.")
        return True
    return False

# ---------------- OLLAMA AI ----------------
def check_ollama():
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get("models", [])
            if models:
                return models[0]["name"]
    except:
        pass
    return None

def ask_ollama(question):
    model_name = check_ollama()
    if not model_name:
        return None
    
    payload = {
        "model": model_name,
        "prompt": f"""You are a helpful desktop assistant named Jack. Keep responses very brief and conversational (2-3 sentences maximum). 

User: {question}
Jack:""",
        "stream": False,
        "options": {"temperature": 0.7, "num_predict": 150}
    }
    
    try:
        print(f"🤔 Asking Ollama...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
    except:
        return None
    return None

# ---------------- ENHANCED COMMAND PROCESSING WITH APP CONTEXT ----------------
def process_command(command):
    """Process voice commands with app context awareness"""
    global current_active_app, app_context_active
    
    command = command.lower().strip()
    
    if not command:
        return False
    
    # ===== ALWAYS AVAILABLE COMMANDS (even in app context) =====
    
    # Exit app context mode
    if any(x in command for x in ["close app", "close this app", "exit app", "stop app mode"]):
        if app_context_active:
            return close_active_app()
        else:
            speak("No active application to close")
            return True
    
    # Exit assistant
    if any(x in command for x in ["exit", "quit", "goodbye", "shut down assistant"]):
        if app_context_active:
            close_active_app()
        return "exit"
    
    # Sleep mode
    if any(x in command for x in ["go to sleep", "sleep now", "deactivate"]):
        if app_context_active:
            close_active_app()
        return "sleep"
    
    # ===== APP CONTEXT MODE (Focused on one app) =====
    if app_context_active and current_active_app:
        print(f"🎯 In {current_active_app} context mode")
        
        # Text editing commands (work in any app)
        if command == "select all" or command == "select everything":
            send_app_shortcut(current_active_app, "select all")
            return True
        
        elif command == "copy" or command == "copy this":
            send_app_shortcut(current_active_app, "copy")
            return True
        
        elif command == "cut" or command == "cut this":
            send_app_shortcut(current_active_app, "cut")
            return True
        
        elif command == "paste" or command == "paste it":
            send_app_shortcut(current_active_app, "paste")
            return True
        
        elif command == "undo" or command == "undo that":
            send_app_shortcut(current_active_app, "undo")
            return True
        
        elif command == "redo":
            send_app_shortcut(current_active_app, "redo")
            return True
        
        elif command == "delete" or command == "delete that":
            pyautogui.press('delete')
            speak("Deleted")
            return True
        
        elif command == "backspace":
            pyautogui.press('backspace')
            speak("Backspace")
            return True
        
        elif command == "enter" or command == "press enter":
            pyautogui.press('enter')
            speak("Enter pressed")
            return True
        
        elif command == "tab":
            pyautogui.press('tab')
            speak("Tab pressed")
            return True
        
        # File operations
        elif command == "save" or command == "save file":
            send_app_shortcut(current_active_app, "save")
            return True
        
        elif command.startswith("save as "):
            filename = command.replace("save as ", "").strip()
            if send_app_shortcut(current_active_app, "save as"):
                time.sleep(1)
                type_text(filename)
                time.sleep(0.5)
                pyautogui.press('enter')
                speak(f"Saved as {filename}")
            return True
        
        elif command == "new file" or command == "new document":
            send_app_shortcut(current_active_app, "new")
            return True
        
        elif command == "open file":
            send_app_shortcut(current_active_app, "open")
            return True
        
        elif command == "print":
            send_app_shortcut(current_active_app, "print")
            return True
        
        # Find/Replace
        elif command == "find" or command.startswith("find "):
            send_app_shortcut(current_active_app, "find")
            if "find " in command:
                text = command.replace("find ", "").strip()
                time.sleep(0.5)
                type_text(text)
                time.sleep(0.5)
                pyautogui.press('enter')
            return True
        
        elif command == "replace":
            send_app_shortcut(current_active_app, "replace")
            return True
        
        # Typing command
        elif command.startswith("type "):
            text = command[5:].strip()
            type_text(text)
            return True
        
        # App-specific commands (bold, italic, etc.)
        elif current_active_app in apps:
            shortcuts = apps[current_active_app].get("shortcuts", {})
            for action in shortcuts.keys():
                if action in command and len(action) > 3:  # Avoid single letter matches
                    send_app_shortcut(current_active_app, action)
                    return True
        
        # If in app context but command not recognized
        else:
            speak(f"In {current_active_app} mode. Try commands like 'type something', 'save', 'copy', 'paste', 'select all', or say 'close app' to exit.")
            return True
    
    # ===== NORMAL MODE (No active app context) =====
    
    # Open applications (enters app context mode)
    for app_name in apps:
        if f"open {app_name}" in command or f"launch {app_name}" in command or f"start {app_name}" in command:
            return open_app(app_name)
    
    # Typing in normal mode (temporary, no context)
    if command.startswith("type "):
        text = command[5:].strip()
        type_text(text)
        return True
    
    # Keyboard shortcuts
    if command.startswith("press "):
        keys = command[6:].strip()
        press_keys(keys)
        return True
    
    # Open website
    if "open website" in command or "go to" in command:
        url = command.replace("open website", "").replace("go to", "").strip()
        if url and ("." in url or "localhost" in url):
            open_website(url)
        else:
            speak("What website should I open?")
        return True
    
    # System commands
    if "brightness" in command:
        if "up" in command or "increase" in command:
            set_brightness(80)
        elif "down" in command or "decrease" in command:
            set_brightness(30)
        elif "max" in command:
            set_brightness(100)
        return True
    
    if "volume" in command:
        if "up" in command:
            change_volume("up")
        elif "down" in command:
            change_volume("down")
        elif "mute" in command:
            change_volume("mute")
        return True
    
    if any(x in command for x in ["screenshot", "take a screenshot"]):
        take_screenshot()
        return True
    
    if any(x in command for x in ["lock screen", "lock computer"]):
        lock_screen()
        return True
    
    if "shutdown" in command and "computer" in command:
        shutdown_computer()
        return True
    
    if "restart" in command and "computer" in command:
        restart_computer()
        return True
    
    if any(x in command for x in ["what time", "current time"]):
        get_time()
        return True
    
    if any(x in command for x in ["what date", "today's date"]):
        get_date()
        return True
    
    if "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").replace("for", "").strip()
        if query:
            search_web(query)
        return True
    
    if any(x in command for x in ["minimize all", "show desktop"]):
        minimize_all()
        return True
    
    if "close window" in command:
        close_window()
        return True
    
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        if query:
            speak(f"Searching Wikipedia for {query}")
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak(summary)
            except:
                speak("No Wikipedia article found")
        return True
    
    if any(x in command for x in ["system info", "computer status"]):
        get_system_info()
        return True
    
    # ===== CONVERSATION (OLLAMA) =====
    print("💭 Using Ollama for conversation...")
    speak("Let me think about that")
    
    ai_response = ask_ollama(command)
    if ai_response:
        speak(ai_response)
        return True
    else:
        speak("Try saying 'open notepad', 'type hello', or 'what time is it'")
        return False

# ---------------- SPEECH RECOGNITION ----------------
def listen_for_wake_word():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Listening for 'Jack'...")
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=3)
                text = recognizer.recognize_google(audio).lower()
                if WAKE_WORD in text:
                    print(f"🔊 Wake word detected")
                    return True
            except:
                continue

def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("🎤 Listening...")
        
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            print("⏳ Processing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"✅ Command: '{command}'")
            return command
        except:
            return ""

# ---------------- MAIN FUNCTION ----------------
def main():
    global active
    
    print("=" * 60)
    print("🎤 Desktop Assistant v4.0 - Persistent App Control")
    print("=" * 60)
    print("💡 Say 'Jack' to activate")
    print("\n🎯 NEW FEATURE - APP CONTEXT MODE:")
    print("   • Say 'open notepad' - Enters Notepad mode")
    print("   • Then just say 'type Hello', 'save', 'new file'")
    print("   • Say 'close app' to exit app mode")
    print("\n📝 COMMANDS IN APP MODE:")
    print("   • 'type something' - Type text")
    print("   • 'select all', 'copy', 'cut', 'paste'")
    print("   • 'undo', 'redo', 'delete', 'backspace'")
    print("   • 'save', 'save as filename.txt'")
    print("   • 'new file', 'open file', 'print'")
    print("   • 'find word', 'replace'")
    print("   • 'bold', 'italic', 'underline' (in Word)")
    print("\n💡 Say 'close app' to exit app mode")
    print("💡 Say 'goodbye' to quit")
    print("=" * 60)
    
    model = check_ollama()
    if model:
        print(f"✅ Ollama ready - Conversations enabled")
    else:
        print("⚠️ Ollama not running - Only commands work")
    
    speak("Hello! I'm Jack")
    
    while True:
        if not active:
            if listen_for_wake_word():
                active = True
                speak("Ready. ")
        
        while active:
            command = listen_for_command()
            
            if not command:
                speak("Could you repeat that?")
                time.sleep(1)
                continue
            
            result = process_command(command)
            
            if result == "sleep":
                active = False
                speak("Going to sleep. Say Jack to wake me.")
                break
            elif result == "exit":
                speak("Goodbye!")
                return
            
            time.sleep(0.3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Assistant stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()