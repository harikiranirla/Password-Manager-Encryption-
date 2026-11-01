"""
Desktop Assistant – Jarvis
A beginner-friendly desktop voice assistant that listens to voice commands,
performs common computer tasks, and responds with voice.

Technology:
  - Python
  - SpeechRecognition (voice input)
  - pyttsx3 (text-to-speech)
  - Tkinter (GUI)
  - webbrowser (opening websites)
  - datetime (date and time)
  - os / subprocess (system operations)
"""

import os
import sys
import subprocess
import webbrowser
import datetime
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# These imports may fail if the packages are not installed.
# We catch the error and show a friendly message to the user.
try:
    import pyttsx3
    import speech_recognition as sr
except ImportError:
    print("Missing required packages. Install them with:\n")
    print("  pip install pyttsx3 SpeechRecognition pyaudio")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Website shortcuts — maps a spoken keyword to a URL.
# ---------------------------------------------------------------------------
WEBSITE_MAP = {
    "google": "https://www.google.com",
    "youtube": "https://www.youtube.com",
    "gmail": "https://mail.google.com",
    "github": "https://www.github.com",
    "wikipedia": "https://www.wikipedia.org",
    "stackoverflow": "https://www.stackoverflow.com",
    "facebook": "https://www.facebook.com",
    "twitter": "https://www.twitter.com",
    "instagram": "https://www.instagram.com",
    "linkedin": "https://www.linkedin.com",
    "amazon": "https://www.amazon.com",
    "reddit": "https://www.reddit.com",
}

# ---------------------------------------------------------------------------
# Application shortcuts — maps a spoken keyword to a command that opens
# the app.  We use a list of candidate commands per keyword so the assistant
# works across Windows, macOS, and Linux.
# ---------------------------------------------------------------------------
APP_MAP = {
    "calculator": ["calc", "gnome-calculator", "open -a Calculator"],
    "notepad": ["notepad", "gedit", "open -a TextEdit"],
    "calculator app": ["calc", "gnome-calculator", "open -a Calculator"],
    "text editor": ["notepad", "gedit", "open -a TextEdit"],
    "file explorer": ["explorer", "nautilus", "open -a Finder"],
    "files": ["explorer", "nautilus", "open -a Finder"],
    "browser": ["start chrome", "firefox", "open -a Safari"],
    "chrome": ["start chrome", "google-chrome", "open -a Google Chrome"],
    "firefox": ["start firefox", "firefox", "open -a Firefox"],
    "terminal": ["start cmd", "gnome-terminal", "open -a Terminal"],
    "command prompt": ["start cmd", "gnome-terminal", "open -a Terminal"],
    "settings": ["start ms-settings:", "gnome-control-center", "open -a System Preferences"],
    "task manager": ["taskmgr", "gnome-system-monitor", "open -a Activity Monitor"],
    "paint": ["mspaint", "open -a Preview"],
    "word": ["start winword", "open -a Microsoft Word"],
    "excel": ["start excel", "open -a Microsoft Excel"],
    "powerpoint": ["start powerpnt", "open -a Microsoft PowerPoint"],
    "spotify": ["start spotify", "spotify", "open -a Spotify"],
    "vlc": ["start vlc", "vlc", "open -a VLC"],
}


class JarvisAssistant:
    """Core assistant logic — speech recognition, command processing, TTS."""

    def __init__(self, on_command=None, on_response=None, on_status=None,
                 on_error=None):
        """Initialize the assistant.

        Callbacks are used to update the GUI without coupling the assistant
        directly to Tkinter widgets.

        Args:
            on_command:  called with the recognized text (str)
            on_response: called with the assistant's text response (str)
            on_status:   called with a status string (str)
            on_error:    called with an error message (str)
        """
        self.on_command = on_command or (lambda text: None)
        self.on_response = on_response or (lambda text: None)
        self.on_status = on_status or (lambda text: None)
        self.on_error = on_error or (lambda text: None)

        # --- Text-to-speech engine -------------------------------------
        self.engine = None
        try:
            self.engine = pyttsx3.init()
            # Slightly slower rate for clarity.
            self.engine.setProperty("rate", 165)
            voices = self.engine.getProperty("voices")
            if voices:
                self.engine.setProperty("voice", voices[0].id)
        except Exception as exc:
            self.on_error(f"Could not initialize text-to-speech: {exc}")

        # --- Speech recognizer -----------------------------------------
        self.recognizer = sr.Recognizer()
        # Adjust for ambient noise tolerance.
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self.running = True

    # ------------------------------------------------------------------
    # Text-to-speech
    # ------------------------------------------------------------------
    def speak(self, text: str):
        """Say the given text out loud and notify the GUI."""
        self.on_response(text)
        if self.engine:
            try:
                self.engine.say(text)
                self.engine.runAndWait()
            except Exception as exc:
                self.on_error(f"Text-to-speech error: {exc}")

    # ------------------------------------------------------------------
    # Speech-to-text
    # ------------------------------------------------------------------
    def listen(self) -> str:
        """Capture audio from the microphone and convert it to text.

        Returns the recognized string (lowercase), or an empty string if
        nothing was understood.
        """
        try:
            with sr.Microphone() as source:
                self.on_status("Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
        except OSError as exc:
            self.on_error(f"Microphone error: {exc}")
            return ""
        except Exception as exc:
            self.on_error(f"Audio capture error: {exc}")
            return ""

        self.on_status("Recognizing...")
        try:
            # Google's free web-based recognizer (requires internet).
            text = self.recognizer.recognize_google(audio)
            return text.lower().strip()
        except sr.UnknownValueError:
            # Speech was unintelligible.
            return ""
        except sr.RequestError as exc:
            self.on_error(f"Speech recognition service error: {exc}")
            return ""
        except Exception as exc:
            self.on_error(f"Recognition error: {exc}")
            return ""

    # ------------------------------------------------------------------
    # Greeting
    # ------------------------------------------------------------------
    def get_greeting(self) -> str:
        """Return a time-appropriate greeting string."""
        hour = datetime.datetime.now().hour
        if 5 <= hour < 12:
            return "Good Morning"
        elif 12 <= hour < 17:
            return "Good Afternoon"
        elif 17 <= hour < 21:
            return "Good Evening"
        else:
            return "Good Night"

    def greet(self):
        """Speak a greeting when the assistant starts."""
        greeting = self.get_greeting()
        self.speak(f"{greeting}! I am Jarvis, your desktop assistant. "
                   f"How can I help you?")

    # ------------------------------------------------------------------
    # Command processing
    # ------------------------------------------------------------------
    def process_command(self, command: str) -> bool:
        """Identify and execute the user's command.

        Returns True if the assistant should keep running, False to exit.
        """
        self.on_command(command)

        if not command:
            self.speak("I didn't catch that. Please try again.")
            return True

        # --- Exit commands ---------------------------------------------
        if any(word in command for word in ("exit", "quit", "stop", "goodbye", "bye")):
            self.speak("Goodbye! Have a great day.")
            self.running = False
            return False

        # --- Greeting --------------------------------------------------
        elif "hello" in command or "hi " in command or command == "hi" \
                or "hey" in command:
            self.speak(f"{self.get_greeting()}! How can I help you?")

        # --- How are you ------------------------------------------------
        elif "how are you" in command:
            self.speak("I am doing great, thank you! How can I assist you?")

        # --- Who are you / your name -----------------------------------
        elif "your name" in command or "who are you" in command:
            self.speak("I am Jarvis, your desktop voice assistant.")

        # --- Time -------------------------------------------------------
        elif "time" in command:
            now = datetime.datetime.now()
            time_str = now.strftime("%I:%M %p")
            self.speak(f"The current time is {time_str}.")

        # --- Date -------------------------------------------------------
        elif "date" in command and "today" in command or command == "what is the date" \
                or "what's the date" in command:
            today = datetime.datetime.now()
            date_str = today.strftime("%B %d, %Y")
            self.speak(f"Today's date is {date_str}.")

        elif "date" in command:
            today = datetime.datetime.now()
            date_str = today.strftime("%B %d, %Y")
            self.speak(f"Today's date is {date_str}.")

        # --- Day of the week -------------------------------------------
        elif "day" in command and "week" in command or "what day is it" in command:
            today = datetime.datetime.now()
            day_str = today.strftime("%A")
            self.speak(f"Today is {day_str}.")

        # --- Open websites ---------------------------------------------
        elif command.startswith("open ") and "search" not in command:
            site = command.replace("open ", "").strip()

            # Check if it's a known website.
            if site in WEBSITE_MAP:
                url = WEBSITE_MAP[site]
                webbrowser.open(url)
                self.speak(f"Opening {site}.")
                return True

            # Check if it's a known application.
            if site in APP_MAP:
                self._open_application(site)
                return True

            # If it looks like a domain, open it directly.
            if "." in site and " " not in site:
                url = f"https://{site}" if not site.startswith("http") else site
                webbrowser.open(url)
                self.speak(f"Opening {site}.")
                return True

            self.speak(f"I'm not sure how to open {site}. Please try another command.")

        # --- Search Google ---------------------------------------------
        elif "search" in command:
            query = command.replace("search", "").replace("for", "", 1).strip()
            if query:
                url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
                webbrowser.open(url)
                self.speak(f"Searching Google for {query}.")
            else:
                self.speak("What would you like me to search for?")

        # --- Play on YouTube -------------------------------------------
        elif "play" in command and "youtube" in command:
            query = command.replace("play", "").replace("on youtube", "").strip()
            if query:
                url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
                webbrowser.open(url)
                self.speak(f"Playing {query} on YouTube.")
            else:
                webbrowser.open("https://www.youtube.com")
                self.speak("Opening YouTube.")

        # --- Wikipedia -------------------------------------------------
        elif "wikipedia" in command:
            query = command.replace("wikipedia", "").replace("search", "").strip()
            if query:
                url = f"https://en.wikipedia.org/wiki/{query.replace(' ', '_')}"
                webbrowser.open(url)
                self.speak(f"Searching Wikipedia for {query}.")
            else:
                webbrowser.open("https://www.wikipedia.org")
                self.speak("Opening Wikipedia.")

        # --- System: shutdown / restart (with confirmation) ------------
        elif "shutdown" in command or "turn off" in command:
            self.speak("Are you sure you want to shut down the computer? "
                       "Please say yes or no.")
            confirm = self.listen()
            if "yes" in confirm:
                self.speak("Shutting down the computer.")
                self.on_status("Shutting down...")
                # Uncomment the line below to actually shut down.
                # os.system("shutdown /s /t 1" if os.name == "nt" else "shutdown -h now")
                self.speak("Shutdown command sent. (Simulated for safety.)")
            else:
                self.speak("Shutdown cancelled.")

        elif "restart" in command:
            self.speak("Are you sure you want to restart the computer? "
                       "Please say yes or no.")
            confirm = self.listen()
            if "yes" in confirm:
                self.speak("Restarting the computer.")
                self.on_status("Restarting...")
                # os.system("shutdown /r /t 1" if os.name == "nt" else "reboot")
                self.speak("Restart command sent. (Simulated for safety.)")
            else:
                self.speak("Restart cancelled.")

        # --- Help -------------------------------------------------------
        elif "help" in command or "what can you do" in command:
            self.speak("I can tell you the time and date, open websites like "
                       "Google, YouTube, and Gmail, search Google, open "
                       "applications like calculator and notepad, and much "
                       "more. Just ask!")

        # --- Unknown command -------------------------------------------
        else:
            self.speak("I'm sorry, I didn't understand that command. "
                       "Say 'help' to hear what I can do.")

        return True

    # ------------------------------------------------------------------
    # Open an application
    # ------------------------------------------------------------------
    def _open_application(self, app_name: str):
        """Try to open an application using platform-appropriate commands."""
        commands = APP_MAP.get(app_name, [])
        for cmd in commands:
            try:
                if os.name == "nt":
                    # Windows: use shell=True so 'start' commands work.
                    subprocess.Popen(cmd, shell=True)
                elif sys.platform == "darwin":
                    # macOS: 'open -a AppName' style commands.
                    subprocess.Popen(cmd, shell=True)
                else:
                    # Linux: try directly, fall back silently.
                    subprocess.Popen(cmd, shell=True,
                                     stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL)
                self.speak(f"Opening {app_name}.")
                return
            except Exception:
                continue
        self.speak(f"Sorry, I couldn't open {app_name}.")

    def listen_once(self):
        """Listen for a single command and process it. Called from GUI."""
        self.on_status("Listening...")
        command = self.listen()
        if command:
            self.process_command(command)
        else:
            self.on_response("(No speech detected or microphone error)")
            self.on_status("Ready")

    def stop(self):
        """Stop the assistant."""
        self.running = False
        if self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass


class JarvisGUI:
    """Tkinter GUI for the Jarvis desktop assistant."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Desktop Assistant – Jarvis")
        self.root.geometry("600x620")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.assistant = None
        self.listening = False

        self._build_ui()
        self._init_assistant()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        """Build the GUI layout."""
        # ---- Title ----------------------------------------------------
        title_frame = tk.Frame(self.root, bg="#1a1a2e")
        title_frame.pack(fill=tk.X, padx=20, pady=(20, 5))

        tk.Label(
            title_frame,
            text="Desktop Assistant – Jarvis",
            font=("Segoe UI", 20, "bold"),
            fg="#e0e0e0",
            bg="#1a1a2e",
        ).pack()

        tk.Label(
            title_frame,
            text="Your voice-controlled desktop helper",
            font=("Segoe UI", 10),
            fg="#888",
            bg="#1a1a2e",
        ).pack(pady=(2, 0))

        # ---- Assistant icon / visual indicator ------------------------
        icon_frame = tk.Frame(self.root, bg="#1a1a2e")
        icon_frame.pack(pady=10)

        self.icon_label = tk.Label(
            icon_frame,
            text="J",
            font=("Segoe UI", 48, "bold"),
            fg="#00d4ff",
            bg="#16213e",
            width=3,
            relief=tk.FLAT,
            padx=20,
            pady=10,
        )
        self.icon_label.pack()

        # ---- Status ---------------------------------------------------
        status_frame = tk.Frame(self.root, bg="#1a1a2e")
        status_frame.pack(fill=tk.X, padx=20)

        self.status_var = tk.StringVar(value="Initializing...")
        self.status_label = tk.Label(
            status_frame,
            textvariable=self.status_var,
            font=("Segoe UI", 11),
            fg="#00d4ff",
            bg="#1a1a2e",
        )
        self.status_label.pack()

        # ---- Buttons --------------------------------------------------
        button_frame = tk.Frame(self.root, bg="#1a1a2e")
        button_frame.pack(fill=tk.X, padx=20, pady=15)

        self.listen_button = tk.Button(
            button_frame,
            text="Start Listening",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#0f3460",
            activebackground="#1a1a2e",
            activeforeground="#00d4ff",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.toggle_listening,
        )
        self.listen_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.exit_button = tk.Button(
            button_frame,
            text="Exit",
            font=("Segoe UI", 12, "bold"),
            fg="white",
            bg="#e94560",
            activebackground="#c2364e",
            activeforeground="white",
            relief=tk.FLAT,
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.on_exit,
        )
        self.exit_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # ---- Recognized command display -------------------------------
        cmd_frame = tk.Frame(self.root, bg="#1a1a2e")
        cmd_frame.pack(fill=tk.X, padx=20, pady=(0, 5))

        tk.Label(
            cmd_frame,
            text="Recognized Command:",
            font=("Segoe UI", 10, "bold"),
            fg="#888",
            bg="#1a1a2e",
            anchor="w",
        ).pack(fill=tk.X)

        self.command_display = tk.Label(
            cmd_frame,
            text="—",
            font=("Segoe UI", 12),
            fg="#e0e0e0",
            bg="#16213e",
            anchor="w",
            padx=10,
            pady=8,
            wraplength=540,
            justify="left",
        )
        self.command_display.pack(fill=tk.X)

        # ---- Assistant response display (scrollable) ------------------
        resp_frame = tk.Frame(self.root, bg="#1a1a2e")
        resp_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=(5, 20))

        tk.Label(
            resp_frame,
            text="Assistant Response:",
            font=("Segoe UI", 10, "bold"),
            fg="#888",
            bg="#1a1a2e",
            anchor="w",
        ).pack(fill=tk.X)

        self.response_text = scrolledtext.ScrolledText(
            resp_frame,
            height=10,
            font=("Consolas", 11),
            bg="#16213e",
            fg="#00d4ff",
            insertbackground="#00d4ff",
            wrap=tk.WORD,
            state=tk.DISABLED,
            relief=tk.FLAT,
            padx=10,
            pady=8,
        )
        self.response_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

    # ------------------------------------------------------------------
    # Assistant initialization
    # ------------------------------------------------------------------
    def _init_assistant(self):
        """Create the assistant instance with GUI callbacks."""
        self.assistant = JarvisAssistant(
            on_command=self.on_command,
            on_response=self.on_response,
            on_status=self.on_status,
            on_error=self.on_error,
        )
        self.status_var.set("Ready — Click 'Start Listening'")

    # ------------------------------------------------------------------
    # Callbacks (called from the assistant, run in worker thread)
    # ------------------------------------------------------------------
    def on_command(self, text: str):
        """Update the recognized-command display."""
        self.root.after(0, lambda: self.command_display.config(
            text=f'"{text}"'))

    def on_response(self, text: str):
        """Append the assistant's response to the text area."""
        def _append():
            self.response_text.config(state=tk.NORMAL)
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.response_text.insert(tk.END, f"[{timestamp}] Jarvis: {text}\n")
            self.response_text.see(tk.END)
            self.response_text.config(state=tk.DISABLED)
        self.root.after(0, _append)

    def on_status(self, text: str):
        """Update the status label."""
        self.root.after(0, lambda: self.status_var.set(text))

    def on_error(self, text: str):
        """Show an error in the response area and as a popup."""
        def _show():
            self.response_text.config(state=tk.NORMAL)
            self.response_text.insert(tk.END, f"[ERROR] {text}\n")
            self.response_text.see(tk.END)
            self.response_text.config(state=tk.DISABLED)
        self.root.after(0, _show)

    # ------------------------------------------------------------------
    # Button actions
    # ------------------------------------------------------------------
    def toggle_listening(self):
        """Start a single listening cycle in a background thread."""
        if self.listening:
            return
        self.listening = True
        self.listen_button.config(text="Listening...", state=tk.DISABLED,
                                  bg="#16213e")
        self.icon_label.config(fg="#e94560")

        def _worker():
            try:
                self.assistant.listen_once()
            except Exception as exc:
                self.root.after(0, lambda: messagebox.showerror(
                    "Error", f"An error occurred: {exc}"))
            finally:
                self.root.after(0, self._reset_button)

        thread = threading.Thread(target=_worker, daemon=True)
        thread.start()

    def _reset_button(self):
        """Restore the listen button to its ready state."""
        self.listening = False
        self.listen_button.config(text="Start Listening", state=tk.NORMAL,
                                  bg="#0f3460")
        self.icon_label.config(fg="#00d4ff")
        self.status_var.set("Ready — Click 'Start Listening'")

    def on_exit(self):
        """Clean up and close the application."""
        if self.assistant:
            self.assistant.stop()
        self.root.destroy()

    def run(self):
        """Start the Tkinter main loop."""
        self.root.mainloop()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    root = tk.Tk()
    app = JarvisGUI(root)
    app.run()


if __name__ == "__main__":
    main()
