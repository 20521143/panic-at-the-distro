import sys
import os
from os import listdir
from os.path import isfile, join
import subprocess
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor, as_completed

mypath = sys.argv[1]
output_dir = sys.argv[2]
onlyfiles = [(f, join(mypath, f)) for f in listdir(mypath) if isfile(join(mypath, f))]
odb_binary = './OSSGadget/src/oss-detect-backdoor/bin/Debug/net6.0/oss-detect-backdoor'

def run_linux_command(command, file_saved):
    try:
        # Run the command and capture the output
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=3600)

        # Check if the command was successful
        if result.returncode == 0:
            print("Command executed successfully!")
            print("Output:\n", result.stdout)
        else:
            print(f"Command failed with error code {result.returncode}")
            print("Error:\n", result.stderr)

    except Exception as e:
        print("Not to process project", file_saved.split(os.sep)[-1])
        print(f"An error occurred: {e}")
        if os.path.exists(file_saved):
            os.remove(file_saved)

def process_file(file_info):
    f, path = file_info
    print(f)
    filename_wo_ext = Path(path).with_suffix('').name
    file_saved = os.path.join(output_dir, filename_wo_ext)
    if not  os.path.exists(file_saved):
       
        command = odb_binary + ' {} -f sarifv2 -o {}'.format(path, file_saved)
        run_linux_command(command, file_saved)
    else:
         print(f"{file_saved} already exists. Skipping...")




# Use ProcessPoolExecutor to run commands concurrently
with ProcessPoolExecutor(max_workers=4) as executor:
    futures = [executor.submit(process_file, file_info) for file_info in onlyfiles]
    for future in as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"An error occurred: {e}")