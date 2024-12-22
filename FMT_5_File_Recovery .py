import os
import shutil
from pathlib import Path

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

# Example usage
if __name__ == "__main__":
    while True:
        print("\nFile Management System")
        print("1. Delete a file")
        print("2. Recover a file")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            file_to_delete = input("Enter the full path of the file to delete: ").strip()
            delete_file_safely(file_to_delete)
        elif choice == "2":
            file_to_recover = input("Enter the name of the file to recover: ").strip()
            recover_file(file_to_recover)
        elif choice == "3":
            print("Exiting the File Management System.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
