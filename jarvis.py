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

# ---------------- CONFIG ----------------
WAKE_WORD = "tony"
active = False
OLLAMA_URL = "http://localhost:11434/api/generate"

# ---------------- TTS ----------------
engine = pyttsx3.init()
engine.setProperty('rate', 160)
engine.setProperty('volume', 0.9)

def speak(text):
    """Speak text using TTS"""
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# ---------------- APP DICTIONARY ----------------
apps = {
    "notepad": "notepad.exe",
    "paint": "mspaint.exe",
    "calculator": "calc.exe",
    "cmd": "cmd.exe",
    "terminal": "cmd.exe",
    "command prompt": "cmd.exe",
    "task manager": "taskmgr.exe",
    "control panel": "control.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "powerpoint": "powerpnt.exe",
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "firefox": "firefox.exe",
    "vs code": "code.exe",
    "visual studio code": "code.exe",
    "vlc": "vlc.exe",
    "explorer": "explorer.exe",
    "file explorer": "explorer.exe",
    "spotify": "Spotify.exe",
    "discord": "Discord.exe",
    "whatsapp": "WhatsApp.exe",
    "telegram": "Telegram.exe"
}

# ---------------- SYSTEM COMMANDS (DIRECT EXECUTION) ----------------
def set_brightness(level):
    """Set screen brightness"""
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent")
        return True
    except:
        speak("Could not change brightness")
        return False

def change_volume(action):
    """Change system volume"""
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
    """Take screenshot"""
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
    """Lock computer"""
    try:
        os.system("rundll32.exe user32.dll,LockWorkStation")
        speak("Computer locked")
        return True
    except:
        speak("Could not lock computer")
        return False

def shutdown_computer():
    """Shutdown computer"""
    speak("Shutting down in 10 seconds. Say cancel to abort.")
    for i in range(10, 0, -1):
        print(f"Shutdown in {i} seconds...")
        time.sleep(1)
    os.system("shutdown /s /t 1")
    return True

def restart_computer():
    """Restart computer"""
    speak("Restarting in 10 seconds. Say cancel to abort.")
    for i in range(10, 0, -1):
        print(f"Restart in {i} seconds...")
        time.sleep(1)
    os.system("shutdown /r /t 1")
    return True

def get_time():
    """Get current time"""
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The time is {current_time}")

def get_date():
    """Get current date"""
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak(f"Today is {current_date}")

def search_web(query):
    """Search Google"""
    webbrowser.open(f"https://www.google.com/search?q={query}")
    speak(f"Searching Google for {query}")

def minimize_all():
    """Minimize all windows"""
    pyautogui.hotkey('win', 'd')
    speak("Minimized all windows")

def close_window():
    """Close current window"""
    pyautogui.hotkey('alt', 'f4')
    speak("Closed current window")

def open_app(app_name):
    """Open an application"""
    if app_name in apps:
        speak(f"Opening {app_name}")
        try:
            os.system(f'start {apps[app_name]}')
        except:
            os.system(f'start "" "{apps[app_name]}"')
        return True
    return False

def type_text(text):
    """Type text using pyautogui"""
    try:
        pyautogui.write(text, interval=0.05)
        speak(f"Typed: {text[:50]}..." if len(text) > 50 else f"Typed: {text}")
        return True
    except Exception as e:
        speak(f"Could not type text")
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
    """Get system stats"""
    cpu = psutil.cpu_percent()
    memory = psutil.virtual_memory().percent
    speak(f"CPU usage is {cpu} percent, Memory usage is {memory} percent")

def open_website(url):
    """Open a website"""
    if not url.startswith("http"):
        url = "https://" + url
    webbrowser.open(url)
    speak(f"Opening {url}")

def create_file():
    """Create a new file using Notepad"""
    try:
        os.system('start notepad.exe')
        time.sleep(1)
        speak("Opened Notepad. You can now type and save your file.")
        return True
    except:
        speak("Could not open Notepad")
        return False

# ---------------- OLLAMA AI (ONLY FOR CONVERSATION/INFO) ----------------
def check_ollama():
    """Check if Ollama is available"""
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
    """Get conversational response from Ollama"""
    model_name = check_ollama()
    
    if not model_name:
        return None
    
    payload = {
        "model": model_name,
        "prompt": f"""You are a helpful desktop assistant named Jack. Keep responses very brief and conversational (2-3 sentences maximum). 
Just answer the question directly and naturally.

User: {question}
Jack:""",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 150
        }
    }
    
    try:
        print(f"🤔 Asking Ollama ({model_name})...")
        response = requests.post(OLLAMA_URL, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "").strip()
        else:
            return None
    except:
        return None

# ---------------- COMMAND PROCESSING ----------------
def process_command(command):
    """Process voice commands - system commands directly, Ollama for conversation"""
    command = command.lower().strip()
    
    if not command:
        return False
    
    # ===== SYSTEM COMMANDS (Direct execution) =====
    
    # Type text
    if command.startswith("type "):
        text = command[5:].strip()
        type_text(text)
        return True
    
    # Press keys/shortcuts
    if command.startswith("press "):
        keys = command[6:].strip()
        press_keys(keys)
        return True
    
    # Open applications
    for app_name in apps:
        if f"open {app_name}" in command or f"launch {app_name}" in command:
            speak("opening",app_name)
            return open_app(app_name)
            
    
    # Open website
    if "open website" in command or "go to" in command:
        url = command.replace("open website", "").replace("go to", "").strip()
        if url and ("." in url or "localhost" in url):
            open_website(url)
        else:
            speak("What website should I open?")
        return True
    
    # Brightness control
    if "brightness" in command:
        if "up" in command or "increase" in command:
            set_brightness(80)
        elif "down" in command or "decrease" in command:
            set_brightness(30)
        elif "max" in command or "full" in command:
            set_brightness(100)
        elif "minimum" in command or "low" in command:
            set_brightness(10)
        elif "fifty" in command:
            set_brightness(50)
        return True
    
    # Volume control
    if "volume" in command:
        if "up" in command or "increase" in command:
            change_volume("up")
        elif "down" in command or "decrease" in command:
            change_volume("down")
        elif "mute" in command:
            change_volume("mute")
        elif "unmute" in command:
            change_volume("up")
        return True
    
    # Screenshot
    if any(x in command for x in ["screenshot", "take a screenshot", "capture screen"]):
        take_screenshot()
        return True
    
    # Lock screen
    if any(x in command for x in ["lock screen", "lock computer", "lock pc"]):
        lock_screen()
        return True
    
    # Shutdown/Restart
    if "shutdown" in command and "computer" in command:
        shutdown_computer()
        return True
    
    if "restart" in command and "computer" in command:
        restart_computer()
        return True
    
    if "cancel shutdown" in command or "cancel restart" in command:
        os.system("shutdown /a")
        speak("Shutdown cancelled")
        return True
    
    # Time and date
    if any(x in command for x in ["what time", "current time", "tell me the time"]):
        get_time()
        return True
    
    if any(x in command for x in ["what date", "today's date"]):
        get_date()
        return True
    
    # Search web
    if "search" in command or "google" in command:
        query = command.replace("search", "").replace("google", "").replace("for", "").strip()
        if query:
            search_web(query)
        else:
            speak("What would you like to search for?")
        return True
    
    # Window management
    if any(x in command for x in ["minimize all", "show desktop"]):
        minimize_all()
        return True
    
    if "close window" in command:
        close_window()
        return True
    
    # File operations
    if any(x in command for x in ["create file", "new file"]):
        create_file()
        return True
    
    # Wikipedia
    if "wikipedia" in command:
        query = command.replace("wikipedia", "").strip()
        if query:
            speak(f"Searching Wikipedia for {query}")
            try:
                summary = wikipedia.summary(query, sentences=2)
                speak(summary)
            except:
                speak("No Wikipedia article found")
        else:
            speak("What should I search on Wikipedia?")
        return True
    
    # System info
    if any(x in command for x in ["system info", "computer status", "pc info", "system information"]):
        get_system_info()
        return True
    
    # Sleep mode
    if any(x in command for x in ["go to sleep", "sleep now", "deactivate"]):
        return "sleep"
    
    # Exit
    if any(x in command for x in ["exit", "quit", "goodbye", "shut down assistant"]):
        return "exit"
    
    # ===== IF NOT A SYSTEM COMMAND, USE OLLAMA FOR CONVERSATION =====
    print("💭 No system command found - using Ollama for conversation...")
    speak("Let me think about that")
    
    ai_response = ask_ollama(command)
    
    if ai_response:
        speak(ai_response)
        return True
    else:
        # Fallback if Ollama is not available
        speak("I'm not sure how to help with that. Try saying 'open chrome' or 'what time is it'")
        return False

# ---------------- SPEECH RECOGNITION ----------------
def listen_for_wake_word():
    """Listen for wake word"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening for wake word 'tony'...")
        
        while True:
            try:
                audio = recognizer.listen(source, timeout=2, phrase_time_limit=5)
                text = recognizer.recognize_google(audio).lower()
                
                if WAKE_WORD in text:
                    print(f"🔊 Wake word detected")
                    return True
                    
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                time.sleep(1)
                continue

def listen_for_command():
    """Listen for command"""
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("🎤 Listening for command...")
        
        try:
            audio = recognizer.listen(source, timeout=8, phrase_time_limit=15)
            print("⏳ Processing...")
            command = recognizer.recognize_google(audio).lower()
            print(f"✅ Command: '{command}'")
            return command
            
        except sr.WaitTimeoutError:
            print("⏰ No command detected")
            return ""
        except sr.UnknownValueError:
            print("❌ Could not understand")
            return ""
        except sr.RequestError:
            print("❌ Recognition service error")
            return ""
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""

# ---------------- MAIN FUNCTION ----------------
def main():
    """Main assistant loop"""
    global active
    
    print("=" * 60)
    print("🎤 Desktop Assistant v2.0")
    print("=" * 60)
    print("💡 Say 'Jack' to activate")
    print("\n📝 SYSTEM COMMANDS:")
    print("   • 'type hello world' - Type text")
    print("   • 'press ctrl+c' - Press keyboard shortcuts")
    print("   • 'open chrome' - Open applications")
    print("   • 'volume up' - Control volume")
    print("   • 'brightness max' - Control brightness")
    print("   • 'take screenshot' - Capture screen")
    print("   • 'what time is it' - Get time/date")
    print("   • 'search for cats' - Google search")
    print("\n💬 CONVERSATION (Ollama):")
    print("   • Ask questions, have conversations")
    print("   • Ollama handles all non-command queries")
    print("\n💡 Say 'go to sleep' to deactivate")
    print("💡 Say 'goodbye' to quit")
    print("=" * 60)
    
    # Check Ollama status
    print("\n🔍 Checking Ollama...")
    model = check_ollama()
    if model:
        print(f"✅ Ollama ready ({model}) - Will handle conversations")
    else:
        print("⚠️ Ollama not running - Only system commands will work")
        print("   To enable conversations: Run 'ollama serve' and 'ollama pull llama3.2'")
    
    speak("Hello! I'm Jack. Say my name when you need me.")
    
    while True:
        # Listen for wake word when inactive
        if not active:
            if listen_for_wake_word():
                active = True
                speak("I'm listening. How can I help?")
        
        # Process commands when active
        while active:
            command = listen_for_command()
            
            if not command:
                speak("Sorry, I didn't catch that. Can you repeat?")
                time.sleep(1)
                continue
            
            # Process the command
            result = process_command(command)
            
            # Handle special returns
            if result == "sleep":
                active = False
                speak("Going to sleep. Say Jack to wake me.")
                break
            elif result == "exit":
                speak("Goodbye!")
                return
            
            # Brief pause before next command
            time.sleep(0.5)

# ---------------- RUN ----------------
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Assistant stopped")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()