import os
import sys
import subprocess
import multiprocessing

def list_subdirectories(directory):
    try:
        return [(d, os.path.join(directory, d)) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    except Exception as e:
        print(f"Error listing subdirectories in {directory}: {e}")
        return []

python_env = "./env/bin/pipenv"
pwd = os.getcwd()

def process_directory(args):
    name, path, result_base_path = args
    result_path = os.path.join(result_base_path, name)
    if not os.path.exists(result_path):
        command = [python_env, 'run', 'python3', f'{pwd}/javascript_analyzer.py', path, result_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Command executed successfully for {name}!")
                print("Output:\n", result.stdout)
            else:
                print(f"Command failed for {name} with error code {result.returncode}")
                print("Error:\n", result.stderr)
                if os.path.exists(result_path):
                    os.remove(result_path)
        except subprocess.TimeoutExpired:
            print(f"Command timed out for {name}")
            if os.path.exists(result_path):
                os.remove(result_path)
        except subprocess.CalledProcessError as e:
            print(f"Command failed for {name} with error: {e}")
            if os.path.exists(result_path):
                os.remove(result_path)
        except Exception as e:
            print(f"An unexpected error occurred for {name}: {e}")
            if os.path.exists(result_path):
                os.remove(result_path)

if __name__ == "__main__":
    try:
        directory = sys.argv[1]
        result_base_path = sys.argv[2]
    except IndexError:
        print("Usage: python cg_scanner_js.py <directory> <result_base_path>")
        sys.exit(1)

    subdirectories = list_subdirectories(directory)
    if not subdirectories:
        print(f"No subdirectories found in {directory}. Exiting.")
        sys.exit(1)

    args = [(name, path, result_base_path) for name, path in subdirectories]

    try:
        with multiprocessing.Pool() as pool:
            pool.map(process_directory, args)
    except Exception as e:
        print(f"An error occurred during multiprocessing: {e}")