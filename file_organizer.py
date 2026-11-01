"""
Automated File Organizer
A beginner-friendly desktop application that automatically organizes
files in a selected folder into separate subfolders based on file type.

Technology:
  - Python
  - Tkinter (GUI)
  - os / pathlib (file and folder handling)
  - shutil (moving files)
"""

import os
import shutil
from pathlib import Path
from tkinter import (
    Tk,
    Label,
    Button,
    filedialog,
    messagebox,
    StringVar,
    LEFT,
    RIGHT,
    BOTH,
    X,
    Y,
    TOP,
    BOTTOM,
    END,
    scrolledtext,
)
from tkinter import ttk


# ---------------------------------------------------------------------------
# File-type categories
# Each category maps to a folder name and a set of allowed extensions.
# Extensions are stored in lowercase (without the dot) for easy comparison.
# ---------------------------------------------------------------------------
FILE_CATEGORIES = {
    "Images":       {"jpg", "jpeg", "png", "gif", "webp"},
    "Documents":    {"pdf", "doc", "docx", "txt"},
    "Videos":       {"mp4", "avi", "mkv", "mov"},
    "Audio":        {"mp3", "wav", "aac"},
    "Spreadsheets": {"xls", "xlsx", "csv"},
    "Presentations": {"ppt", "pptx"},
    "Archives":     {"zip", "rar", "7z"},
}

# Folders that the program creates — used to skip them while scanning.
ORGANIZED_FOLDER_NAMES = set(FILE_CATEGORIES.keys()) | {"Others"}


def get_category(extension: str) -> str:
    """Return the category folder name for a given file extension.

    If the extension does not match any known category, 'Others' is returned.
    """
    ext = extension.lower().lstrip(".")
    for category, extensions in FILE_CATEGORIES.items():
        if ext in extensions:
            return category
    return "Others"


def scan_files(folder_path: str) -> list:
    """Scan the given folder and return a list of file paths to organize.

    Subfolders created by this program (Images, Documents, etc.) are skipped
    so that re-running the organizer does not shuffle already-organized files.
    """
    files_to_organize = []
    try:
        for entry in os.listdir(folder_path):
            full_path = os.path.join(folder_path, entry)
            # Only process files, not directories.
            if not os.path.isfile(full_path):
                continue
            # Skip files that are already inside an organized folder.
            if entry in ORGANIZED_FOLDER_NAMES:
                continue
            files_to_organize.append(full_path)
    except PermissionError:
        raise
    return files_to_organize


def create_category_folders(folder_path: str) -> list:
    """Create all category folders inside the selected folder.

    Returns a list of the folder paths that were created (or already existed).
    """
    created_folders = []
    for folder_name in ORGANIZED_FOLDER_NAMES:
        folder = os.path.join(folder_path, folder_name)
        os.makedirs(folder, exist_ok=True)
        created_folders.append(folder)
    return created_folders


def unique_destination(destination_dir: str, filename: str) -> str:
    """Return a destination path that will not overwrite an existing file.

    If a file with the same name already exists in the destination folder,
    a number is appended before the extension (e.g. report_1.pdf).
    """
    destination = os.path.join(destination_dir, filename)
    if not os.path.exists(destination):
        return destination

    stem = Path(filename).stem
    suffix = Path(filename).suffix
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_destination = os.path.join(destination_dir, new_name)
        if not os.path.exists(new_destination):
            return new_destination
        counter += 1


def move_files(files: list) -> dict:
    """Move each file into its category folder.

    Returns a dictionary with:
      - "total":     total number of files scanned
      - "organized": number of files moved into known categories
      - "others":    number of files moved into the 'Others' folder
      - "errors":    list of error messages (if any)
    """
    stats = {"total": len(files), "organized": 0, "others": 0, "errors": []}

    for file_path in files:
        filename = os.path.basename(file_path)
        extension = os.path.splitext(filename)[1]
        category = get_category(extension)

        # The category folder lives in the same directory as the file.
        source_dir = os.path.dirname(file_path)
        category_folder = os.path.join(source_dir, category)

        try:
            destination = unique_destination(category_folder, filename)
            shutil.move(file_path, destination)

            if category == "Others":
                stats["others"] += 1
            else:
                stats["organized"] += 1
        except (PermissionError, OSError) as exc:
            stats["errors"].append(f"Could not move '{filename}': {exc}")

    return stats


class FileOrganizerApp:
    """Main application class that builds and controls the Tkinter GUI."""

    def __init__(self, root: Tk):
        self.root = root
        self.root.title("Automated File Organizer")
        self.root.geometry("620x540")
        self.root.resizable(False, False)

        # State variables
        self.selected_folder = StringVar()
        self.selected_folder.set("No folder selected")

        self._build_ui()

    # ------------------------------------------------------------------
    # UI construction
    # ------------------------------------------------------------------
    def _build_ui(self):
        """Build all GUI widgets and lay them out."""
        # ---- Title -----------------------------------------------------
        title_label = Label(
            self.root,
            text="Automated File Organizer",
            font=("Segoe UI", 18, "bold"),
            pady=15,
        )
        title_label.pack(side=TOP, fill=X)

        subtitle_label = Label(
            self.root,
            text="Organize your files automatically by type",
            font=("Segoe UI", 10),
            fg="gray",
        )
        subtitle_label.pack(side=TOP, fill=X)

        # ---- Selected folder display -----------------------------------
        folder_frame = ttk.Frame(self.root, padding=15)
        folder_frame.pack(side=TOP, fill=X)

        ttk.Label(folder_frame, text="Selected Folder:", font=("Segoe UI", 10, "bold")) \
            .pack(anchor="w")

        self.folder_display = Label(
            folder_frame,
            textvariable=self.selected_folder,
            font=("Segoe UI", 10),
            fg="blue",
            wraplength=560,
            anchor="w",
            justify="left",
        )
        self.folder_display.pack(anchor="w", pady=(5, 0))

        # ---- Buttons ---------------------------------------------------
        button_frame = ttk.Frame(self.root, padding=15)
        button_frame.pack(side=TOP, fill=X)

        self.browse_button = ttk.Button(
            button_frame, text="Browse Folder", command=self.browse_folder
        )
        self.browse_button.pack(side=LEFT, padx=5, fill=X, expand=True)

        self.organize_button = ttk.Button(
            button_frame, text="Organize Files", command=self.organize_files
        )
        self.organize_button.pack(side=LEFT, padx=5, fill=X, expand=True)

        self.reset_button = ttk.Button(
            button_frame, text="Reset", command=self.reset
        )
        self.reset_button.pack(side=LEFT, padx=5, fill=X, expand=True)

        # ---- Status / summary text area --------------------------------
        status_frame = ttk.Frame(self.root, padding=15)
        status_frame.pack(side=TOP, fill=BOTH, expand=True)

        ttk.Label(status_frame, text="Status & Summary:", font=("Segoe UI", 10, "bold")) \
            .pack(anchor="w")

        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=12,
            font=("Consolas", 10),
            wrap="word",
            state="disabled",
        )
        self.status_text.pack(side=TOP, fill=BOTH, expand=True, pady=(5, 0))

        # ---- Footer ----------------------------------------------------
        footer_label = Label(
            self.root,
            text="Files are never deleted — only moved into category folders.",
            font=("Segoe UI", 9),
            fg="gray",
        )
        footer_label.pack(side=BOTTOM, fill=X, pady=5)

    # ------------------------------------------------------------------
    # Helper: write text to the status area
    # ------------------------------------------------------------------
    def _set_status(self, message: str):
        """Replace the status text area content with the given message."""
        self.status_text.config(state="normal")
        self.status_text.delete(1.0, END)
        self.status_text.insert(END, message)
        self.status_text.config(state="disabled")

    def _append_status(self, message: str):
        """Append a line to the status text area."""
        self.status_text.config(state="normal")
        self.status_text.insert(END, message + "\n")
        self.status_text.config(state="disabled")

    # ------------------------------------------------------------------
    # Button actions
    # ------------------------------------------------------------------
    def browse_folder(self):
        """Open a folder-selection dialog and store the chosen path."""
        folder = filedialog.askdirectory(title="Select a Folder to Organize")
        if folder:
            self.selected_folder.set(folder)
            self._set_status(f"Folder selected:\n{folder}\n\nClick 'Organize Files' to begin.")

    def organize_files(self):
        """Main workflow: scan, create folders, move files, show summary."""
        folder_path = self.selected_folder.get()

        # --- Validate the selected folder -------------------------------
        if not folder_path or folder_path == "No folder selected":
            messagebox.showwarning("No Folder", "Please select a folder first.")
            return

        if not os.path.isdir(folder_path):
            messagebox.showerror("Invalid Path", "The selected folder path is invalid.")
            return

        try:
            # --- Step 1: Scan files -------------------------------------
            files = scan_files(folder_path)
            if not files:
                self._set_status("No files found to organize in the selected folder.")
                return

            self._set_status(
                f"Scanning '{folder_path}'...\n"
                f"Found {len(files)} file(s) to organize.\n\nOrganizing...\n"
            )
            self.root.update()

            # --- Step 2: Create category folders ------------------------
            create_category_folders(folder_path)

            # --- Step 3: Move files --------------------------------------
            stats = move_files(files)

            # --- Step 4: Display summary ---------------------------------
            summary = (
                "Organization Completed Successfully!\n"
                "------------------------------------\n"
                f"Total Files:    {stats['total']}\n"
                f"Files Organized: {stats['organized']}\n"
                f"Other Files:    {stats['others']}\n"
            )
            if stats["errors"]:
                summary += "\nSome files could not be moved:\n"
                for err in stats["errors"]:
                    summary += f"  - {err}\n"

            self._set_status(summary)

            messagebox.showinfo(
                "Success",
                f"Organization Completed!\nTotal: {stats['total']}\n"
                f"Organized: {stats['organized']}\nOthers: {stats['others']}",
            )

        except PermissionError:
            error_msg = "Permission denied. The selected folder cannot be accessed."
            self._set_status(f"Error: {error_msg}")
            messagebox.showerror("Permission Error", error_msg)
        except Exception as exc:
            error_msg = f"An unexpected error occurred:\n{exc}"
            self._set_status(f"Error: {error_msg}")
            messagebox.showerror("Error", error_msg)

    def reset(self):
        """Clear the selected folder and reset the status area."""
        self.selected_folder.set("No folder selected")
        self._set_status("Ready. Select a folder to begin.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
def main():
    root = Tk()
    app = FileOrganizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
