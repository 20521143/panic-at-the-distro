import requests
import os
import subprocess
import json
import sys
import argparse
import re
import tempfile
import zipfile

# GitHub personal access token
GITHUB_TOKEN = ""
GITHUB_API_URL = "https://api.github.com"


# Headers for GitHub API requests
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def fetch_repo_languages(repo_name):
    """Fetch the programming languages used in the repository using GitHub API."""
    try:
        url = f"{GITHUB_API_URL}/repos/{repo_name}/languages"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors
        languages = response.json()
        return languages
    except requests.RequestException as e:
        print(f"Error fetching languages for {repo_name}: {e}")
        return {}

def clone_repo(package_name, repo_url, base_dir):
    package_dir = os.path.join(base_dir, package_name)
    
    # Check if directory already exists
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)
        print(f"Cloning {package_name} from {repo_url} into {package_dir}")
        
        try:
            # Run the git clone command with a timeout of 1 minute
            subprocess.run(['git', 'clone', repo_url, package_dir], timeout=120, check=True)
            return True
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            print(f"Cloning {package_name} from {repo_url} failed or timed out. Deleting directory and moving to the next.")
            # shutil.rmtree(package_dir)
            return False
    else:
        print(f"Directory {package_name} already exists, skipping...")
        return False

def detect_language_locally(project_path):
    result = subprocess.run(['github-linguist', project_path, '--json'], capture_output=True, text=True)
    if result.returncode == 0:
        try:
          languages = json.loads(result.stdout)
          #normalize languages like github API language
          new = {}
          for key in languages:
            new[key] = languages[key]['size']
            return new
        except json.JSONDecodeError as e:
          print("Failed to decode JSON:", e)
    return None

def is_repository_in_github(url):
    if re.search(r'^https?://github\.com/.*', url):
        return True
    return False

def get_repo_name_from_url(url):
    """Extract the repository name from the GitHub URL using regex and remove .git extension if present."""
    match = re.search(r'^https?://github\.com/(.*)$', url)
    if match:
        repo_name = match.group(1)
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        if repo_name.endswith('/'):
            repo_name = repo_name[:-1]
        return repo_name
    return None

def handle_local_file(file_path):
    if os.path.isdir(file_path):
        # If it's a directory, detect language directly
        language = detect_language_locally(file_path)
        if language:
            print(f"The programming language of the project is: {language}")
        else:
            print("Failed to detect the programming language locally.")
    elif zipfile.is_zipfile(file_path):
        # If it's a zip file, unzip it to a temporary directory and detect language
        with tempfile.TemporaryDirectory() as temp_dir:
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            language = detect_language_locally(temp_dir)
            if language:
                print(f"The programming language of the project is: {language}")
            else:
                print("Failed to detect the programming language locally.")
    else:
        print("The provided file is neither a directory nor a zip file.")

# Using  github-linguist tool to detect the programming language of local repository
def main():
    parser = argparse.ArgumentParser("Detect the programming language of a project using GitHub API or Linguist tool.")
    parser.add_argument("URL_or_Path", help="URL of the project or local file path")
    args = parser.parse_args()
    input_path = args.URL_or_Path
    if is_repository_in_github(input_path):
        repo_name = get_repo_name_from_url(input_path)
        language = fetch_repo_languages(repo_name)
        if language:
            print(f"The programming language of the project is: {language}")
        else:
            print("Failed to get the programming language from GitHub API.")
    elif os.path.exists(input_path):
        handle_local_file(input_path)

    else:    
        with tempfile.TemporaryDirectory() as temp_dir:
            if clone_repo("temp_project", input_path, temp_dir):
                language = detect_language_locally(os.path.join(temp_dir, "temp_project"))
                if language:
                    print(f"The programming language of the project is: {language}")
                else:
                    print("Failed to detect the programming language locally.")
            else:
                print("Failed to clone the repository.")

if __name__ == "__main__":
    main()
