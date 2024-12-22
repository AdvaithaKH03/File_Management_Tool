import os
from sys import argv
from pygments import highlight
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import TerminalFormatter
from docx import Document



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


if __name__ == "__main__":
    # Get the file name from the user or arguments
    if len(argv) > 1:
        filename = argv[1]
    else:
        filename = input("Enter the file name (with extension): ").strip()

    # Handle the file
    handle_file(filename)
