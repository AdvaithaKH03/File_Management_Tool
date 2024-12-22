import os
import re

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


base_directory = input("Enter base directory path: ")
sub_directory = input("Enter subdirectory path (relative to base directory): ")
term_to_search = input("Enter search term or regex pattern: ")
is_recursive = input("Search recursively? (yes/no): ").strip().lower() == 'yes'

search_files(base_directory, sub_directory, term_to_search, is_recursive)
