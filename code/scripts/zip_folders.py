import os
import zipfile
import sys

def zip_folders_in_directory(directory):
    # Change to the target directory
    os.chdir(directory)

    # Loop through each item in the directory
    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)
        
        # Check if the item is a folder
        if os.path.isdir(folder_path):
            # Create a zip file for the folder
            zip_file_name = f"{folder_name}.zip"
            with zipfile.ZipFile(zip_file_name, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                # Walk through the folder and add files to the zip
                for root, dirs, files in os.walk(folder_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        # Add the file to the zip, preserving the folder structure
                        zip_file.write(file_path, os.path.relpath(file_path, folder_path))
            print(f"Zipped folder: {folder_name}")

# Example usage:
directory_path = sys.argv[1] 
zip_folders_in_directory(directory_path)

