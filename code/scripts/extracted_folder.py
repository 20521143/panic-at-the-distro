import os
import tarfile
import multiprocessing
import sys

# Function to extract a single .tar.gz file
def extract_tar(file_path):

    file_name = file_path.split('\\')[-1][:-4]
    # file_dir = os.path.dirname(file_path)
    # print(f'Extracting: {file_name} from {file_dir}')
    
    try:
        with tarfile.open(file_path, 'r:gz') as tar:
            extract_path = os.path.join(os.path.dirname(file_path), file_name)  # Extract in a folder named after the file
            os.makedirs(extract_path, exist_ok=True)
            tar.extractall(path=extract_path)
            print(f'Extracted: {file_path} to {extract_path}')
    except Exception as e:
        print(f'Failed to extract {file_path}: {e}')

# Function to find all .tar.gz files in a directory (including subdirectories)
def find_tar_files(folder_path):
    tar_files = []
    for root, _, files in os.walk(folder_path):
        for filename in files:
            valid_extensions = ('.tar.gz', '.tgz', '.tar', '.gz', '.zip', '.rar', '.7z')
            if filename.endswith(valid_extensions):
                # print(os.path.join(root, filename))
                tar_files.append(os.path.join(root, filename))
    return tar_files

def main():
    folder_path = sys.argv[1]
    
    # Find all .tar.gz files
    tar_files = find_tar_files(folder_path)

    # print(len(tar_files))
    
    # Create a pool of processes
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        # Extract each .tar.gz file in parallel
        pool.map(extract_tar, tar_files)

if __name__ == '__main__':
    main()
