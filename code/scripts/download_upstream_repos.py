import csv
import requests
import os
import sys

def download_github_repo_as_zip(repo_url, output_path):
    # Modify the URL to point to the zip file of the repository's main branch
    zip_url = repo_url.rstrip('/') + '/archive/refs/heads/main.zip'
    
    # Download the zip file
    response = requests.get(zip_url)
    
    # Check if the request was successful
    if response.status_code == 200:
        with open(output_path, 'wb') as file:
            file.write(response.content)
        print(f"Repository downloaded and saved as {output_path}")
    else:
        print(f"Failed to download {repo_url}. Status code: {response.status_code}")

def download_repos_from_csv(csv_file_path, output_dir):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        # Skip the first row (header)
        next(reader)

        for row in reader:
            package_name = row[0]  # First column: Package name
            repo_url = row[-1]     # Last column: GitHub repository URL
            
            # Set the output path for the zip file in the specified output directory
            output_zip = os.path.join(output_dir, f"{package_name}.zip")
            
            # Download the repository as a zip file and save it with the package name in the output directory
            download_github_repo_as_zip(repo_url, output_zip)

# Example usage:
csv_file_path = sys.argv[1]  # Replace with your CSV file path
output_dir = sys.argv[2]  # Directory to store the downloaded zip files
download_repos_from_csv(csv_file_path, output_dir)

