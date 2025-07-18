import os
import sys
import subprocess
import multiprocessing

def list_subdirectories(directory):
    return [(d, os.path.join(directory, d)) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

python_env = "./env/bin/pipenv"
pwd = os.getcwd()
def process_directory(args):
    name, path, result_base_path = args
    result_path = os.path.join(result_base_path, name)
    if not os.path.exists(result_path):
        command = [python_env, 'run', 'python3', f'{pwd}/ruby_analyzer.py', '-c', f'{pwd}/config/astgen_ruby_smt.config', path, result_path]
        try:
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Command executed successfully for {name}!")
                print("Output:\n", result.stdout)
            else:
                print(f"Command failed for {name} with error code {result.returncode}")
                print("Error:\n", result.stderr)
                os.remove(result_path)
        except Exception as e:
            print(f"An error occurred for {name}: {e}")

if __name__ == "__main__":
    directory = sys.argv[1]
    result_base_path = sys.argv[2]
    subdirectories = list_subdirectories(directory)
    args = [(name, path, result_base_path) for name, path in subdirectories]

    with multiprocessing.Pool() as pool:
        pool.map(process_directory, args)