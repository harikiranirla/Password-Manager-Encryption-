# Desktop Assistant – Jarvis

A beginner-friendly **Python desktop voice assistant** that listens to your voice commands, performs common computer tasks, and responds with speech.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Required Python Packages](#required-python-packages)
3. [Project Folder Structure](#project-folder-structure)
4. [Installation Commands](#installation-commands)
5. [How to Run in VS Code](#how-to-run-in-vs-code)
6. [Features](#features)
7. [Sample Voice Commands and Responses](#sample-voice-commands-and-responses)
8. [Explanation of Major Functions](#explanation-of-major-functions)
9. [Project Workflow](#project-workflow)
10. [Common Errors and Solutions](#common-errors-and-solutions)
11. [Future Enhancements](#future-enhancements)

---

## Project Overview

**Jarvis** is a desktop voice assistant built with Python. It uses your microphone to listen to commands, converts your speech to text, identifies what you asked for, performs the task, and speaks a response back to you — all through a clean Tkinter graphical interface.

### Technology Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **SpeechRecognition** | Converts your voice into text |
| **pyttsx3** | Text-to-speech (Jarvis speaks to you) |
| **Tkinter** | Graphical user interface |
| **webbrowser** | Opens websites in your browser |
| **datetime** | Provides current time, date, and day |
| **os / subprocess** | Opens applications on your computer |

---

## Required Python Packages

This project uses the following **third-party** packages (not built into Python):

| Package | Purpose |
|---|---|
| `SpeechRecognition` | Captures audio and sends it to Google's speech API |
| `pyttsx3` | Offline text-to-speech engine |
| `pyaudio` | Required by SpeechRecognition to access the microphone |

All other libraries (`tkinter`, `webbrowser`, `datetime`, `os`, `subprocess`) are **built into Python** — no installation needed.

---

## Project Folder Structure

```
desktop-assistant-jarvis/
│
├── jarvis.py          # Main application source code
└── JARVIS_README.md   # This documentation file
```

---

## Installation Commands

### Step 1: Install Python

Download and install **Python 3.8 or later** from https://www.python.org/downloads/

On Windows, check the box **"Add Python to PATH"** during installation.

Verify:
```
python --version
```

### Step 2: Install Required Packages

Open a terminal (Command Prompt on Windows, Terminal on macOS/Linux) and run:

```
pip install pyttsx3 SpeechRecognition pyaudio
```

#### Platform-Specific Notes

**Windows:**
```
pip install pyttsx3 SpeechRecognition pyaudio
```
If `pyaudio` fails, install it with:
```
pip install pipwin
pipwin install pyaudio
```

**macOS:**
```
pip install pyttsx3 SpeechRecognition
brew install portaudio
pip install pyaudio
```

**Linux (Ubuntu/Debian):**
```
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyttsx3 SpeechRecognition pyaudio
```

For Tkinter on Linux (if not already installed):
```
sudo apt-get install python3-tk
```

---

## How to Run in VS Code

1. **Install VS Code** from https://code.visualstudio.com/ if you don't have it.

2. **Open the project folder** in VS Code:
   - Open VS Code
   - Go to **File → Open Folder**
   - Select the `desktop-assistant-jarvis` folder

3. **Open the file** `jarvis.py` in the editor.

4. **Make sure you have a microphone connected** to your computer.

5. **Run the application** using one of these methods:
   - **Method A:** Click the **Run** button (▶) in the top-right corner.
   - **Method B:** Open the integrated terminal (**Terminal → New Terminal**) and type:
     ```
     python jarvis.py
     ```

6. The **Desktop Assistant – Jarvis** window will appear.

7. Click **Start Listening** and speak a command clearly into your microphone.

8. Jarvis will process your command, speak a response, and display it on screen.

9. Click **Exit** or say **"Exit Jarvis"** to close the assistant.

---

## Features

1. **Simple GUI** — Clean, modern Tkinter interface with a title, status, buttons, and display areas.
2. **Voice Input** — Uses your microphone to capture voice commands.
3. **Speech to Text** — Converts your spoken words into text using Google's speech recognition.
4. **Voice Response** — Jarvis speaks responses out loud using pyttsx3.
5. **Recognized Command Display** — Shows what you said on screen.
6. **Date and Time** — Tells you the current time, date, and day of the week.
7. **Open Websites** — Opens Google, YouTube, Gmail, and more.
8. **Google Search** — Searches Google for anything you say.
9. **Open Applications** — Opens Calculator, Notepad, and other apps on your computer.
10. **Greeting** — Greets you based on the time of day (Good Morning / Afternoon / Evening).
11. **Exit Command** — Say "exit", "quit", or "goodbye" to stop the assistant.
12. **Unknown Command Handling** — Responds politely when it doesn't understand.
13. **Error Handling** — Shows clear errors if the microphone or speech recognition is unavailable.
14. **Confirmation for Destructive Actions** — Asks for confirmation before shutdown or restart.
15. **Cross-Platform** — Works on Windows, macOS, and Linux.

---

## Sample Voice Commands and Responses

| You Say | Jarvis Responds | Action |
|---|---|---|
| "What is the time?" | "The current time is 3:45 PM." | — |
| "What is today's date?" | "Today's date is September 15, 2026." | — |
| "What day is it?" | "Today is Monday." | — |
| "Open Google" | "Opening Google." | Opens google.com |
| "Open YouTube" | "Opening YouTube." | Opens youtube.com |
| "Open Gmail" | "Opening Gmail." | Opens mail.google.com |
| "Search Python tutorials" | "Searching Google for Python tutorials." | Opens Google search |
| "Play music on YouTube" | "Playing music on YouTube." | Opens YouTube search |
| "Open calculator" | "Opening calculator." | Opens Calculator app |
| "Open notepad" | "Opening notepad." | Opens Notepad / TextEdit |
| "Hello" | "Good Afternoon! How can I help you?" | — |
| "How are you?" | "I am doing great, thank you! How can I assist you?" | — |
| "What is your name?" | "I am Jarvis, your desktop voice assistant." | — |
| "Help" | Lists available commands | — |
| "Exit Jarvis" | "Goodbye! Have a great day." | Closes the assistant |
| *(unrecognized)* | "I'm sorry, I didn't understand that command." | — |

---

## Explanation of Major Functions

### Core Assistant (`JarvisAssistant` class)

| Function | Purpose |
|---|---|
| `__init__()` | Initializes the text-to-speech engine, speech recognizer, and GUI callbacks |
| `speak(text)` | Speaks the given text out loud and sends it to the GUI display |
| `listen()` | Captures audio from the microphone and converts it to text using Google's API |
| `get_greeting()` | Returns a time-appropriate greeting ("Good Morning", "Good Afternoon", etc.) |
| `greet()` | Speaks the initial greeting when Jarvis starts |
| `process_command(command)` | The brain — matches the recognized text against known commands and executes the right action |
| `_open_application(app_name)` | Tries to open an application using platform-appropriate commands (Windows/macOS/Linux) |
| `listen_once()` | Listens for a single command and processes it (triggered by the GUI button) |
| `stop()` | Stops the assistant and cleans up the speech engine |

### GUI (`JarvisGUI` class)

| Function | Purpose |
|---|---|
| `__init__()` | Creates the main window and initializes the assistant |
| `_build_ui()` | Builds all GUI widgets: title, icon, status, buttons, display areas |
| `_init_assistant()` | Creates the `JarvisAssistant` instance with GUI update callbacks |
| `on_command(text)` | Updates the "Recognized Command" display when a command is heard |
| `on_response(text)` | Appends Jarvis's response to the scrollable response area with a timestamp |
| `on_status(text)` | Updates the status label (e.g., "Listening...", "Ready") |
| `on_error(text)` | Displays error messages in the response area |
| `toggle_listening()` | Starts a listening cycle in a background thread (keeps the GUI responsive) |
| `on_exit()` | Stops the assistant and closes the application |
| `run()` | Starts the Tkinter main event loop |

---

## Project Workflow

```
Start Jarvis
    ↓
Click "Start Listening"
    ↓
Jarvis captures audio from microphone
    ↓
Speech is converted to text (Google Speech API)
    ↓
Recognized text is displayed on screen
    ↓
Jarvis identifies the command
    ↓
Jarvis performs the requested task (open website, tell time, etc.)
    ↓
Jarvis speaks a voice response
    ↓
Response is displayed on screen
    ↓
Jarvis waits for the next command
    ↓
(User says "Exit") → Jarvis says goodbye → Application closes
```

---

## Common Errors and Solutions

### 1. `ModuleNotFoundError: No module named 'pyttsx3'`
**Cause:** The pyttsx3 package is not installed.
**Solution:**
```
pip install pyttsx3
```

### 2. `ModuleNotFoundError: No module named 'speech_recognition'`
**Cause:** The SpeechRecognition package is not installed.
**Solution:**
```
pip install SpeechRecognition
```

### 3. `ModuleNotFoundError: No module named 'pyaudio'`
**Cause:** PyAudio (microphone access) is not installed.
**Solution (Windows):**
```
pip install pyaudio
```
If that fails:
```
pip install pipwin
pipwin install pyaudio
```
**Solution (macOS):**
```
brew install portaudio
pip install pyaudio
```
**Solution (Linux):**
```
sudo apt-get install python3-pyaudio portaudio19-dev
pip install pyaudio
```

### 4. `OSError: No Default Input Device Available`
**Cause:** No microphone is connected or the microphone is disabled.
**Solution:** Connect a microphone or enable your built-in microphone in system settings.

### 5. `speech_recognition.UnknownValueError`
**Cause:** Jarvis couldn't understand what you said (background noise, unclear speech).
**Solution:** Speak clearly in a quiet environment. Jarvis handles this automatically and asks you to repeat.

### 6. `speech_recognition.RequestError`
**Cause:** No internet connection (Google Speech API requires internet).
**Solution:** Check your internet connection and try again.

### 7. GUI opens but no sound / Jarvis doesn't speak
**Cause:** Volume is muted or the audio output device is not set correctly.
**Solution:** Check your system volume and audio output settings.

### 8. Tkinter not found (Linux)
**Cause:** Tkinter is not installed on your Linux distribution.
**Solution:**
```
sudo apt-get install python3-tk
```

---

## Future Enhancements

Here are ideas to extend Jarvis further:

1. **Weather Information** — Integrate the OpenWeatherMap API to answer "What's the weather today?"
2. **Reminders and Alarms** — Let the user set voice-activated reminders that trigger a notification at the right time.
3. **Music Control** — Play, pause, skip, and control volume of music playing on the computer.
4. **Email Assistance** — Compose and send emails using voice commands via SMTP.
5. **AI-Based Conversation** — Integrate OpenAI or a similar API so Jarvis can answer general knowledge questions conversationally.
6. **News Headlines** — Fetch and read the latest news using a news API.
7. **Screenshot Capture** — Take a screenshot with a voice command.
8. **System Monitoring** — Report CPU usage, RAM usage, and battery status.
9. **Voice Authentication** — Recognize the owner's voice and only respond to authorized users.
10. **Multi-Language Support** — Understand and respond in multiple languages.
11. **Smart Home Integration** — Control IoT devices like lights and fans.
12. **Custom Wake Word** — Always listen for "Hey Jarvis" instead of requiring a button press.
