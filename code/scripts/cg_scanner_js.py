import os
import sys
import subprocess


def list_subdirectories(directory):
    return [(d, os.path.join(directory, d)) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

# Example usage
directory = sys.argv[1] 
subdirectories = list_subdirectories(directory)
print(subdirectories)

def run_linux_command(command, result_path):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if the command was successful
        if result.returncode == 0:
            print("Command executed successfully!")
            print("Output:\n", result.stdout)
        else:
            print(f"Command failed with error code {result.returncode}")
            print("Error:\n", result.stderr)
            os.remove(result_path)

    except Exception as e:
        print(f"An error occurred: {e}")

for name, path in subdirectories:
    result_path = os.path.join(sys.argv[2], name)
    if not os.path.exists(result_path):
        command = 'python3 javascript_analyzer.py {} {}'.format(path, result_path)
        run_linux_command(command, result_path)


