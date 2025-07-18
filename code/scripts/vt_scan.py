
import os
import time
import requests
import json
import sys

# Set your VirusTotal API key here
API_KEY = '48a0d48d8f64f4f12a3327a4c3d049061821b602d598a07c410201502b8170f4'

# Define headers for VirusTotal API requests
HEADERS = {
    'x-apikey': API_KEY
}

# Define directories
input_dir = sys.argv[1]  # Directory with files to scan
output_dir = sys.argv[2]  # Directory to save scan results

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

def submit_file_to_virustotal(file_path):
    url = 'https://www.virustotal.com/api/v3/files'
    files = {'file': (os.path.basename(file_path), open(file_path, 'rb'))}
    response = requests.post(url, headers=HEADERS, files=files)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to upload {file_path}. Status code: {response.status_code}")
        return None

def get_scan_results(scan_id):
    url = f'https://www.virustotal.com/api/v3/analyses/{scan_id}'
    while True:
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            result = response.json()
            status = result.get('data', {}).get('attributes', {}).get('status')
            if status == 'completed':
                return result
            else:
                time.sleep(25)  # Wait before polling again
        else:
            print(f"Failed to get scan results for {scan_id}. Status code: {response.status_code}")
            return None

def save_json_results(file_name, results):
    output_file = os.path.join(output_dir, f"{file_name}.json")
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=4)

def main():
    files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]

    for file_name in files:
        output_file = os.path.join(output_dir, f"{file_name}.json")
        if not os.path.exists(output_file):
            file_path = os.path.join(input_dir, file_name)
            print(f"Submitting {file_name} to VirusTotal...")

            response = submit_file_to_virustotal(file_path)

            if response:
                scan_id = response['data']['id']
                print(f"Submitted {file_name}, scan ID: {scan_id}. Waiting for results...")
                results = get_scan_results(scan_id)

                if results:
                    print(f"Scan completed for {file_name}, saving results...")
                    save_json_results(file_name, results)
                else:
                    print(f"Failed to get scan results for {file_name}.")
            else:
                print(f"Failed to submit {file_name}.")

if __name__ == "__main__":
    main()

