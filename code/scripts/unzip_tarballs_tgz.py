import os
import tarfile

# Function to extract a .tgz tarball into a directory with the same name
def extract_tgz_to_named_dir(tarball_path, extract_base_dir):
    # Get the base name of the tarball (remove .tgz)
    tarball_name = os.path.basename(tarball_path).replace(".tgz", "")
    # Create a new directory with the same name as the tarball in the target directory
    extract_to_dir = os.path.join(extract_base_dir, tarball_name)
    
    if not os.path.exists(extract_to_dir):
        os.makedirs(extract_to_dir)
    
    # Extract the tarball into the named directory
    if tarfile.is_tarfile(tarball_path):
        with tarfile.open(tarball_path, "r:gz") as tar:
            tar.extractall(path=extract_to_dir)
            print(f"Extracted {tarball_path} to {extract_to_dir}")
    else:
        print(f"{tarball_path} is not a valid tarball")

# Function to extract all .tgz tarballs in a source directory into directories with the same name
def extract_tgz_in_directory(source_dir, target_dir):
    # Check if the source and target directories exist
    if not os.path.exists(source_dir):
        print(f"Source directory {source_dir} does not exist.")
        return

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # Loop through all files in the source directory
    for filename in os.listdir(source_dir):
        if filename.endswith(".tgz"):
            tarball_path = os.path.join(source_dir, filename)
            extract_tgz_to_named_dir(tarball_path, target_dir)

# Example usage
import sys
source_directory = sys.argv[1] 
target_directory = sys.argv[2]
extract_tgz_in_directory(source_directory, target_directory)

