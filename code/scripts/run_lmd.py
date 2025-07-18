import subprocess
import os
from datetime import datetime
import re
import sys

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
    
    # Run the maldet scan command
    try:
        print(f"Scanning directory: {scan_directory}")
        scan_command = f"sudo maldet -a {scan_directory}"
        
        # Run the command and capture the output
        result = subprocess.run(scan_command, shell=True, capture_output=True, text=True)

        # Check if scan was successful
        if result.returncode == 0:
            # Parse the output to find infected filenames
            infected_files = re.findall(r"file hit for malware: (.+)", result.stdout)
            
            if infected_files:
                # Save the infected filenames to a log file in the result directory
                with open(infected_files_log, 'w') as log_file:
                    for file in infected_files:
                        log_file.write(file + '\n')
                print(f"Infected files found and saved to {infected_files_log}")
            else:
                print("No infected files found.")
        else:
            print(f"Error during scan: {result.stderr}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
scan_directory_path = sys.argv[1] 
result_directory_path = sys.argv[2]
scan_with_lmd(scan_directory_path, result_directory_path)

