#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import re

def check_unar():
    """Finds the unar executable. Checks PATH and typical macOS locations."""
    # First check in PATH
    unar_path = shutil.which("unar")
    if unar_path:
        return unar_path

    # Check common Homebrew installation paths on macOS
    common_paths = [
        "/opt/homebrew/bin/unar",
        "/usr/local/bin/unar",
    ]
    for path in common_paths:
        if os.path.isfile(path) and os.access(path, os.X_OK):
            return path

    return None

def clean_path(path_str):
    """Cleans up paths that might have quotes or backslash-escaped characters from drag-and-drop."""
    path_str = path_str.strip()
    if (path_str.startswith('"') and path_str.endswith('"')) or (path_str.startswith("'") and path_str.endswith("'")):
        path_str = path_str[1:-1]
    else:
        # Replace backslash-escaped characters (like '\ ' with ' ')
        path_str = re.sub(r'\\(.)', r'\1', path_str)
    return path_str

def get_unique_dir(parent_dir, base_name):
    """Generates a unique directory name to prevent overwriting existing folders."""
    output_dir = os.path.join(parent_dir, base_name)
    if not os.path.exists(output_dir):
        return output_dir
    
    counter = 1
    while os.path.exists(os.path.join(parent_dir, f"{base_name}_{counter}")):
        counter += 1
    return os.path.join(parent_dir, f"{base_name}_{counter}")

def extract_rar(rar_path, unar_path):
    """Extracts the archive using unar."""
    # Resolve absolute path and verify file exists
    rar_path = os.path.abspath(rar_path)
    if not os.path.isfile(rar_path):
        print(f"Error: File not found at '{rar_path}'", file=sys.stderr)
        return False

    # Get directory and base filename (without extension)
    dir_name = os.path.dirname(rar_path)
    base_name, ext = os.path.splitext(os.path.basename(rar_path))
    
    # Optional: warn if not a rar file, but proceed anyway since unar supports other formats
    if ext.lower() != '.rar':
        print(f"Note: The file extension is '{ext}', but proceeding to extract using unar.", flush=True)

    # Generate unique output directory
    output_dir = get_unique_dir(dir_name, base_name)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Extracting '{os.path.basename(rar_path)}' to '{os.path.basename(output_dir)}'...", flush=True)
    
    try:
        # Run unar:
        # -o: output directory
        # -D: do not create a containing directory (since we already created a unique output_dir)
        # rar_path: target archive
        # We don't capture stdout/stderr so that any interactive prompt (like passwords) works seamlessly.
        result = subprocess.run([unar_path, "-o", output_dir, "-D", rar_path])
        
        if result.returncode == 0:
            print("\n" + "="*50)
            print("Done! Extraction completed successfully.")
            print(f"Output folder: {output_dir}")
            print("="*50)
            return True
        else:
            print(f"\nError: Extraction failed with return code {result.returncode}.", file=sys.stderr)
            # Clean up the output directory if it is empty
            if os.path.exists(output_dir) and not os.listdir(output_dir):
                os.rmdir(output_dir)
            return False
            
    except Exception as e:
        print(f"\nAn error occurred during extraction: {e}", file=sys.stderr)
        return False

def main():
    print("=== RAR Archive Extractor ===", flush=True)
    
    # 1. Check if unar is installed
    unar_path = check_unar()
    if not unar_path:
        print("Error: 'unar' command-line tool not found.", file=sys.stderr)
        print("Please install it using Homebrew by running:", file=sys.stderr)
        print("    brew install unar", file=sys.stderr)
        sys.exit(1)

    # 2. Get the input file path
    rar_path = None
    if len(sys.argv) > 1:
        rar_path = sys.argv[1]
    else:
        try:
            user_input = input("Drag and drop the .rar file here (or type the path) and press Enter:\n> ")
            rar_path = user_input
        except (KeyboardInterrupt, EOFError):
            print("\nOperation cancelled.")
            sys.exit(0)

    if not rar_path:
        print("Error: No file path provided.", file=sys.stderr)
        sys.exit(1)

    # Clean and resolve path
    rar_path = clean_path(rar_path)
    
    success = extract_rar(rar_path, unar_path)
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
