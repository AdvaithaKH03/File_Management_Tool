import os
import shutil
import string
import re
from sys import argv
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import TerminalFormatter
from docx import Document
from pathlib import Path

def list_drives():
    """
    List all available drives on the computer (Windows only).
    """
    drives = []
    for drive in string.ascii_uppercase:
        if os.path.exists(f"{drive}:\\"):
            drives.append(f"{drive}:\\")
    return drives

def copy_file_dynamic(source_file, destination_file):
    """
    Copies a file from the source location to the destination file path.
    Paths are dynamically constructed for compatibility across operating systems.

    Parameters:
    - source_file: Full path to the file to be copied.
    - destination_file: Full path to the destination file (including the file name).
    """
    try:
        # Validate source file
        if not os.path.isfile(source_file):
            print(f"Source file '{source_file}' does not exist.")
            return

        # Ensure the destination directory exists
        destination_dir = os.path.dirname(destination_file)
        if not os.path.exists(destination_dir):
            print(f"Destination directory '{destination_dir}' does not exist. Creating it.")
            os.makedirs(destination_dir)

        # Perform the file copy
        shutil.copy(source_file, destination_file)
        print(f"File '{source_file}' successfully copied to '{destination_file}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

def read_code(file):
    """
    Reads and highlights code files with syntax highlighting.
    """
    try:
        if not os.path.isfile(file):
            return "File not found. Please check the filename."

        with open(file, 'r') as f:
            code = f.read()

        lexer = guess_lexer_for_filename(file, code)
        highlighted_code = highlight(code, lexer, TerminalFormatter())
        return highlighted_code
    except Exception as e:
        return f"An error occurred while reading the code file: {e}"

def read_docx(file):
    """
    Reads the text content of a .docx file.
    """
    try:
        if not os.path.isfile(file):
            return "File not found. Please check the filename."

        document = Document(file)
        content = "\n".join([paragraph.text for paragraph in document.paragraphs])
        return content if content.strip() else "The document is empty."
    except Exception as e:
        return f"An error occurred while reading the .docx file: {e}"

def open_pdf(file):
    """
    Opens a PDF file in the system's default viewer.
    """
    try:
        if not os.path.isfile(file):
            return "File not found. Please check the filename."

        os.startfile(file)  # Windows
        # For macOS, use: os.system(f"open {file}")
        # For Linux, use: os.system(f"xdg-open {file}")
        return f"Opened {file} in your default PDF viewer."
    except Exception as e:
        return f"An error occurred while opening the PDF file: {e}"

def handle_file(file):
    """
    Determines the file type and processes it accordingly.
    """
    _, extension = os.path.splitext(file)

    if extension.lower() in [".py", ".js", ".java", ".c", ".cpp", ".txt"]:
        print("\n--- Code File Content ---")
        print(read_code(file))
    elif extension.lower() == ".docx":
        print("\n--- Document Content ---")
        print(read_docx(file))
    elif extension.lower() == ".pdf":
        print("\n--- Opening PDF ---")
        print(open_pdf(file))
    else:
        print(f"Unsupported file type: {extension}")

def search_files(base_directory, sub_path, search_term, recursive=True):
    """
    Search for a term in files within a dynamically constructed directory.

    :param base_directory: Base directory to start from.
    :param sub_path: Additional path to navigate dynamically.
    :param search_term: The term or regex pattern to search for.
    :param recursive: Whether to search in subdirectories.
    """
    # Construct the full path
    directory = os.path.join(base_directory, sub_path)

    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    print(f"Searching in: {directory}")
    pattern = re.compile(search_term)
    matches = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line_no, line in enumerate(f, 1):
                        if pattern.search(line):
                            matches.append((file_path, line_no, line.strip()))
            except (UnicodeDecodeError, PermissionError):
                # Skip files that cannot be read
                pass

        if not recursive:
            break

    # Print matches
    if matches:
        print(f"Found {len(matches)} matches:")
        for match in matches:
            print(f"File: {match[0]}, Line: {match[1]}, Content: {match[2]}")
    else:
        print("No matches found.")

# Define paths
RECYCLE_BIN_PATH = Path.home() / ".recycle_bin"
RECYCLE_BIN_PATH.mkdir(exist_ok=True)  # Create recycle bin if not exist

def delete_file_safely(file_path):
    """Move a file to a custom recycle bin."""
    file_path = Path(file_path)
    if not file_path.exists():
        print("File not found!")
        return

    try:
        # Move file to recycle bin
        destination = RECYCLE_BIN_PATH / file_path.name
        shutil.move(str(file_path), str(destination))
        print(f"File moved to recycle bin: {destination}")
    except Exception as e:
        print(f"Error moving file to recycle bin: {e}")

def recover_file(file_name):
    """Recover a file from the recycle bin."""
    file_in_bin = RECYCLE_BIN_PATH / file_name
    if not file_in_bin.exists():
        print("File not found in recycle bin!")
        return

    try:
        destination = Path.cwd() / file_name
        shutil.move(str(file_in_bin), str(destination))
        print(f"File recovered to: {destination}")
    except Exception as e:
        print(f"Error recovering file: {e}")


def command_prompt():
    """
    Mimics a Windows Command Prompt for file navigation with drive access and file copying.
    """
    current_directory = os.getcwd()  # Start in the current working directory

    print("Welcome to the File Navigator (Windows CMD style).")
    print("Type 'help' for a list of commands.\n")

    while True:
        # Display the current directory in a command-prompt style
        prompt = f"{current_directory}> "
        command = input(prompt).strip()

        if not command:
            continue

        # Split the command and arguments
        parts = command.split()
        cmd = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []

        # Handle commands
        if cmd == "dir":
            try:
                print("\n Directory of", current_directory)
                print()
                with os.scandir(current_directory) as entries:
                    for entry in entries:
                        if entry.is_dir():
                            print(f"<DIR>        {entry.name}")
                        elif entry.is_file():
                            print(f"             {entry.name}")
            except PermissionError:
                print("Access denied.")
        elif cmd == "cd":
            if len(args) == 0:
                print(current_directory)
            elif args[0] == "..":
                current_directory = os.path.dirname(current_directory)
            elif len(args) == 1 and args[0].endswith(":"):
                new_drive = args[0].upper() + "\\"
                if os.path.exists(new_drive):
                    current_directory = new_drive
                else:
                    print(f"The system cannot find the drive specified: '{new_drive}'")
            else:
                new_path = os.path.join(current_directory, " ".join(args))
                if os.path.isdir(new_path):
                    current_directory = new_path
                else:
                    print(f"The system cannot find the path specified: '{new_path}'")
        elif cmd == "type":
            if len(args) == 0:
                print("The syntax of the command is incorrect.")
            else:
                file_name = " ".join(args)
                file_path = os.path.join(current_directory, file_name)
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r', encoding='utf-8') as file:
                            print("\n" + "-" * 40)
                            print(file.read())
                            print("-" * 40)
                    except (UnicodeDecodeError, PermissionError):
                        print(f"Could not read the file '{file_name}'.")
                else:
                    print(f"The system cannot find the file specified: '{file_name}'")
        elif cmd == "drives":
            drives = list_drives()
            if drives:
                print("Available drives:")
                for drive in drives:
                    print(f"  {drive}")
            else:
                print("No drives found.")
        elif cmd == "exit":
            print("Exiting File Navigator.")
            break
        elif cmd == "copy":
            # Interactive file copy process
            print("\n--- File Copy ---")
            source_file = input("Enter the full path of the source file: ").strip()
            destination_file = input("Enter the full path of the destination file (including the new name): ").strip()
            copy_file_dynamic(source_file, destination_file)
        elif cmd == "read":
            if len(argv) > 1:
                filename = argv[1]
                filename = input("Enter the file name (with extension): ").strip()

            # Handle the file
            handle_file(filename)
        elif cmd == "search":
            print("\n--- File Search ---")
            base_directory = input("Enter base directory path: ").strip()
            sub_directory = input("Enter subdirectory path (relative to base directory): ").strip()
            term_to_search = input("Enter search term or regex pattern: ").strip()
            is_recursive = input("Search recursively? (yes/no): ").strip().lower() == 'yes'
            search_files(base_directory, sub_directory, term_to_search, is_recursive)

        elif cmd == "delete":
            print("\nFile Management System")
            print("1. Delete a file")
            print("2. Recover a file")
            choice = input("Enter your choice (1/2): ").strip()

            if choice == "1":
                file_to_delete = input("Enter the full path of the file to delete: ").strip()
                delete_file_safely(file_to_delete)
            elif choice == "2":
                file_to_recover = input("Enter the name of the file to recover: ").strip()
                recover_file(file_to_recover)
            else:
                print("Invalid choice. Please enter 1, 2.")

        elif cmd == "help":
            print("\nAvailable Commands:")
            print("  dir             List directory contents")
            print("  cd [path]       Change the current directory or switch drives (e.g., 'cd D:')")
            print("  type [file]     Display the contents of a file")
            print("  drives          List all available drives")
            print("  copy            Copy a file (source -> destination)")
            print("  read            Read or open a file based on type")
            print("  search          Search for a term in files within a directory")
            print("  exit            Exit the program")
            print("  help            Show this help message\n")
            print("  delete          For deletion and recovery of file")
        else:
            print(f"'{cmd}' is not recognized as an internal or external command.")

# Run the command prompt
if __name__ == "__main__":
    command_prompt()
