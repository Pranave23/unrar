# macOS RAR Extractor

A simple, user-friendly script for macOS to automatically extract `.rar` files into folders with the same name. It uses `unar` (via Homebrew) under the hood to handle extraction.

## Features
- **Auto-creation of folders**: Automatically creates a destination folder with the same name as the archive inside the same directory (no double nested folders!).
- **Safe naming**: Automatically appends a number suffix (e.g., `_1`, `_2`) if a folder with the same name already exists, preventing accidental overwriting.
- **Drag and Drop**: You can drag and drop your `.rar` archive directly into the Terminal window to extract.
- **Double-Click Executable**: Includes a `.command` wrapper so you can run it just by double-clicking it in Finder.

---

## How to Use

### Method 1: Double-Click in Finder (Easiest)
1. Double-click the file named [extract.command](file:///Users/pranavekl/projects/unrar/extract.command).
2. A macOS Terminal window will open and prompt you to drag and drop the archive.
3. Drag your `.rar` file from Finder, drop it into the Terminal window, and press **Enter**.
4. Once it prints the success message, press **Enter** again to close the window.

### Method 2: Command Line Argument
Run the Python script directly from your terminal by passing the `.rar` file path as an argument:
```bash
python3 extract.py /path/to/your/archive.rar
```
Or use the wrapper:
```bash
./extract.command /path/to/your/archive.rar
```

---

## Technical Details & Environment
- **Virtual Environment**: A Python virtual environment (`venv`) has been initialized in this folder.
- **Dependencies**: The script utilizes standard Python libraries (`os`, `sys`, `subprocess`, `re`, `shutil`), so no external `pip` packages are required!
- **Unar installation**: The command-line utility `unar` has been verified and installed at `/opt/homebrew/bin/unar`. If needed in the future, it can be re-installed using Homebrew via:
  ```bash
  brew install unar
  ```
# unrar
# unrar
# unrar
