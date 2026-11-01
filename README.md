# Automated File Organizer

A beginner-friendly **Python desktop application** that automatically organizes files in a selected folder into separate subfolders based on their file type.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Project Folder Structure](#project-folder-structure)
3. [Features](#features)
4. [Installation Instructions](#installation-instructions)
5. [How to Run in VS Code](#how-to-run-in-vs-code)
6. [Project Workflow](#project-workflow)
7. [Sample Input and Output](#sample-input-and-output)
8. [Code Explanation](#code-explanation)
9. [Future Enhancements](#future-enhancements)

---

## Project Overview

The **Automated File Organizer** is a desktop GUI application built with Python and Tkinter. When a user selects a folder and clicks **Organize Files**, the program scans every file in that folder, identifies its type by extension, creates the necessary category folders, and moves each file into the correct folder — all automatically.

### Technology Used

| Technology | Purpose |
|---|---|
| **Python** | Core programming language |
| **Tkinter** | GUI (graphical user interface) |
| **os / pathlib** | File and folder handling |
| **shutil** | Moving files safely |

---

## Project Folder Structure

```
automated-file-organizer/
│
├── file_organizer.py      # Main application source code
└── README.md              # This documentation file
```

---

## Features

- Clean and simple GUI built with Tkinter
- **Browse Folder** button to select any folder
- Scans all files in the selected folder
- Identifies files by their extensions
- Automatically creates and organizes files into these folders:

| Folder | Extensions |
|---|---|
| **Images** | JPG, JPEG, PNG, GIF, WEBP |
| **Documents** | PDF, DOC, DOCX, TXT |
| **Videos** | MP4, AVI, MKV, MOV |
| **Audio** | MP3, WAV, AAC |
| **Spreadsheets** | XLS, XLSX, CSV |
| **Presentations** | PPT, PPTX |
| **Archives** | ZIP, RAR, 7Z |
| **Others** | Any unknown file type |

- Moves files into their respective folders automatically
- **Never deletes files**
- Prevents duplicate files from being overwritten by creating unique filenames (e.g., `report_1.pdf`)
- Displays the number of files organized in a summary
- Shows clear success/error messages
- Handles invalid folder paths and permission errors
- **Reset** button to clear the selection and start over
- Simple interface suitable for a college mini-project

---

## Installation Instructions

### Step 1: Install Python

Download and install **Python 3.8 or later** from the official website:

> https://www.python.org/downloads/

During installation on Windows, **check the box** that says **"Add Python to PATH"**.

Verify the installation by opening a terminal and running:

```
python --version
```

### Step 2: Download the Project

Download or clone the project folder to your computer. You only need the file `file_organizer.py`.

### Step 3: No External Libraries Required

This project uses only **built-in Python libraries** (Tkinter, os, pathlib, shutil). You do **not** need to install any external packages with `pip`.

> **Linux users only:** Tkinter may not be included by default. Install it with:
> ```
> sudo apt-get install python3-tk
> ```

---

## How to Run in VS Code

1. **Install VS Code** from https://code.visualstudio.com/ if you don't have it.

2. **Open the project folder** in VS Code:
   - Open VS Code
   - Go to **File → Open Folder**
   - Select the `automated-file-organizer` folder

3. **Open the file** `file_organizer.py` in the editor.

4. **Run the application** using one of these methods:
   - **Method A:** Click the **Run** button (▶) in the top-right corner of the editor.
   - **Method B:** Open the integrated terminal (**Terminal → New Terminal**) and type:
     ```
     python file_organizer.py
     ```

5. The **Automated File Organizer** window will appear.

---

## Project Workflow

Here is a step-by-step explanation of how the application works:

### 1. User Selects a Folder
The user clicks the **Browse Folder** button. A folder-selection dialog opens. The user navigates to and selects the folder they want to organize. The selected path is displayed on screen.

### 2. User Clicks "Organize Files"
The application validates the folder path. If the path is invalid or no folder is selected, an error message is shown.

### 3. Scanning (`scan_files`)
The application scans the selected folder and collects a list of all files (ignoring subdirectories, including previously created category folders so re-running doesn't re-shuffle files).

### 4. Categorizing (`get_category`)
Each file's extension is checked against the `FILE_CATEGORIES` dictionary. The file is assigned to one of the eight categories (Images, Documents, Videos, Audio, Spreadsheets, Presentations, Archives, or Others).

### 5. Creating Folders (`create_category_folders`)
The application creates all eight category folders inside the selected directory (if they don't already exist).

### 6. Moving Files (`move_files` + `unique_destination`)
Each file is moved into its category folder using `shutil.move()`. Before moving, the application checks if a file with the same name already exists in the destination. If it does, a unique name is generated by appending a counter (e.g., `photo_1.jpg`, `photo_2.jpg`) so no file is ever overwritten.

### 7. Displaying the Summary
After all files are moved, a summary is displayed showing:
- Total files found
- Files organized into known categories
- Files placed in the "Others" folder
- Any errors that occurred

A popup message also confirms the result.

---

## Sample Input and Output

### Sample Input

A folder containing these files before organizing:

```
Downloads/
├── report.pdf
├── notes.txt
├── photo.jpg
├── vacation.mp4
├── song.mp3
├── data.csv
├── slides.pptx
├── backup.zip
├── unknown.xyz
└── report.pdf        (duplicate name)
```

### Sample Output

After clicking **Organize Files**, the folder looks like this:

```
Downloads/
├── Images/
│   ├── photo.jpg
├── Documents/
│   ├── report.pdf
│   ├── notes.txt
├── Videos/
│   ├── vacation.mp4
├── Audio/
│   ├── song.mp3
├── Spreadsheets/
│   ├── data.csv
├── Presentations/
│   ├── slides.pptx
├── Archives/
│   ├── backup.zip
├── Others/
│   ├── unknown.xyz
```

### Summary Displayed in the Application

```
Organization Completed Successfully!
------------------------------------
Total Files:     10
Files Organized:  9
Other Files:      1
```

---

## Code Explanation

The code is organized into clean, separate functions, each with a single responsibility:

| Function | Purpose |
|---|---|
| `get_category(extension)` | Takes a file extension and returns the matching category name (or "Others") |
| `scan_files(folder_path)` | Scans a folder and returns a list of file paths to organize |
| `create_category_folders(folder_path)` | Creates all eight category folders inside the selected directory |
| `unique_destination(dir, filename)` | Generates a unique destination path to prevent overwriting existing files |
| `move_files(files)` | Moves each file into its category folder and returns statistics |
| `FileOrganizerApp` | The main GUI class that builds the interface and connects button actions |
| `browse_folder()` | Opens a folder dialog and stores the selected path |
| `organize_files()` | Runs the full organize workflow (scan → create → move → summarize) |
| `reset()` | Clears the selection and resets the status area |
| `main()` | Entry point that creates the Tkinter root window and starts the app |

---

## Future Enhancements

Here are ideas to extend this project further:

1. **Custom Categories** — Let users add their own file types and category names through the GUI.
2. **Recursive Scanning** — Organize files inside subfolders, not just the top level.
3. **Undo Feature** — Reverse the last organization and restore files to their original locations.
4. **Drag and Drop** — Allow dragging a folder onto the window instead of using the browse button.
5. **Progress Bar** — Show a real-time progress bar while files are being moved.
6. **Dark Mode** — Add a toggle for a dark theme.
7. **Schedule Automatic Organizing** — Use a timer or scheduler to organize the Downloads folder automatically every day.
8. **Log File** — Save a text log of every move operation with timestamps.
9. **Preview Before Organizing** — Show the user what will be moved where, and ask for confirmation before executing.
10. **Cross-Platform Packaging** — Package the app as a standalone `.exe` (Windows) or `.app` (macOS) using PyInstaller so non-Python users can run it.
