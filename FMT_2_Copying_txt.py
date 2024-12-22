import os
import shutil


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


# Main program
if __name__ == "__main__":
    print("This script will copy a file from a source folder to a destination folder with a new file name.")
    
    # Prompt the user for the source folder
    source_folder = input("Enter the source folder path (e.g., Documents/Projects): ").strip()
    home_directory = os.path.expanduser("~")
    full_source_folder = os.path.join(home_directory, source_folder)

    # Prompt the user for the file name in the source folder
    source_file_name = input("Enter the name of the file to copy (e.g., example.txt): ").strip()
    source_file = os.path.join(full_source_folder, source_file_name)

    # Prompt the user for the destination folder
    destination_folder = input("Enter the destination folder path (e.g., Documents/Backup): ").strip()
    full_destination_folder = os.path.join(home_directory, destination_folder)

    # Prompt the user for the destination file name
    destination_file_name = input("Enter the name of the destination file (e.g., new_example.txt): ").strip()
    destination_file = os.path.join(full_destination_folder, destination_file_name)

    print(f"\n--- Path Preview ---")
    print(f"Source File: {source_file}")
    print(f"Destination File: {destination_file}\n")

    # Confirm with the user
    confirm = input("Do you want to proceed with copying? (yes/no): ").strip().lower()
    if confirm in ["yes", "y"]:
        # Copy the file
        copy_file_dynamic(source_file, destination_file)
    else:
        print("Operation canceled.")


