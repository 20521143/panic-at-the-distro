import subprocess
import os
from datetime import datetime
import re

def scan_with_lmd(scan_directory, result_directory):
    # Check if the scan directory exists
    if not os.path.exists(scan_directory):
        print(f"Error: Directory {scan_directory} does not exist.")
        return
    
    # Create the result directory if it doesn't exist
    if not os.path.exists(result_directory):
        os.makedirs(result_directory)
        print(f"Created result directory: {result_directory}")

    # Get the current timestamp for unique log files
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Define the output log file for infected filenames (inside result directory)
    infected_files_log = os.path.join(result_directory, f"infections_{timestamp}.txt")

    # Find all files (not directories) in the scan directory
    files_to_scan = [f for f in os.listdir(scan_directory) if os.path.isfile(os.path.join(scan_directory, f))]

    # If no files are found, exit
    if not files_to_scan:
        print("No files found in the directory.")
        return

    try:
        with open(infected_files_log, 'w') as log_file:
            for file in files_to_scan:
                file_path = os.path.join(scan_directory, file)
                print(f"Scanning file: {file_path}")

                # Run maldet scan for each file
                scan_command = f"sudo maldet -a {file_path}"
                
                # Run the command and capture the output
                result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)

                # Check if scan was successful
                if result.returncode == 0:
                    # Parse the output to find infected filenames
                    infected_files = re.findall(r"file hit for malware: (.+)", result.stdout)

                    if infected_files:
                        # Save the infected filenames to the log file
                        for infected_file in infected_files:
                            log_file.write(infected_file + '\n')
                        print(f"Infected files found in {file_path} and saved to {infected_files_log}")
                    else:
                        print(f"No infected files found in {file_path}.")
                else:
                    print(f"Error during scan of {file_path}: {result.stderr}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
import sys
scan_directory_path = sys.argv[1]   # Update this path
result_directory_path = sys.argv[2]  # Update this path
scan_with_lmd(scan_directory_path, result_directory_path)

