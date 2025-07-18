import os
import sys
import subprocess

# Path to bandit executable
bandit_env = r".\env\Scripts\bandit.exe"

def list_directories(path):
    """List all directories in the specified path."""
    try:
        items = os.listdir(path)
        directories = [(item, os.path.join(path, item)) for item in items if os.path.isdir(os.path.join(path, item))]
        return directories
    except Exception as e:
        print(f"Error listing directories in {path}: {e}")
        sys.exit(1)

# Check that there are enough arguments
if len(sys.argv) < 3:
    print("Usage: script.py <directory_path> <output_directory>")
    sys.exit(1)

# Get directory paths from arguments
directory_path = sys.argv[1] 
output_directory = sys.argv[2]

# Get list of directories in the specified path
directories = list_directories(directory_path)
print("Directories:", directories)

# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Run Bandit for each directory
for directory, path in directories:
    print(f"Processing directory: {directory} at path {path}")
    dest_file = os.path.join(output_directory, f"{directory}.json")
    command = [bandit_env, '-r', path, '-f', 'json', '-o', dest_file]
    
    try:
        # Execute the command and capture output
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Command executed successfully for {directory}!")
        print("Output:\n", result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed for {directory} with error code {e.returncode}")
        print("Error:\n", e.stderr)
    except Exception as e:
        print(f"An unexpected error occurred for {directory}: {e}")
