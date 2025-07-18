import os
import sys
import pandas as pd
import subprocess
import shutil
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def clone_repo(package_name, repo_url, base_dir, attempts=1, timeout=3600):
    package_dir = os.path.join(base_dir, package_name)

    if not os.path.exists(package_dir):
        os.makedirs(package_dir)

        for attempt in range(1, attempts + 1):
            logging.info(f"Attempt {attempt}: Cloning {package_name} from {repo_url} into {package_dir}")
            try:
                subprocess.run(['git', 'clone', '--depth', '1', repo_url, package_dir], timeout=timeout, check=True)
                logging.info(f"Successfully cloned {package_name}.")
                return True
            except subprocess.TimeoutExpired:
                logging.error(f"Attempt {attempt}: Cloning {package_name} failed: operation timed out.")
            except subprocess.CalledProcessError as e:
                logging.error(f"Attempt {attempt}: Cloning {package_name} failed: Git command error: {e}")
            except Exception as e:
                logging.error(f"Attempt {attempt}: Cloning {package_name} failed due to an unexpected error: {e}")

            if os.path.exists(package_dir):
                shutil.rmtree(package_dir)

        logging.error(f"Failed to clone {package_name} after {attempts} attempts.")
        return False
    else:
        logging.info(f"Directory for {package_name} already exists, skipping...")
        return False

def process_repo(row, base_dir):
    package_name = row.iloc[0]
    repo_url = row.iloc[-3]

    if pd.notna(repo_url) and repo_url.strip():
        clone_repo(package_name, repo_url, base_dir)

def main(csv_file, base_dir):
    df = pd.read_csv(csv_file, skiprows=range(1,80), nrows=20)

    with ProcessPoolExecutor() as executor:
        futures = {executor.submit(process_repo, row, base_dir): row for _, row in df.iterrows()}
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"An error occurred: {e}")

    logging.info("All cloning tasks have completed.")

if __name__ == '__main__':
    csv_file = sys.argv[1]
    base_dir = sys.argv[2]

    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    main(csv_file, base_dir)
