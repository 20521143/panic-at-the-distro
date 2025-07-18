import os
import json
import csv
from collections import Counter
import re
import argparse

def is_empty_file(file_path):
    return os.stat(file_path).st_size == 0

FILE_TEXT_EXTENSION = [
    '.txt',    # Plain text file
    '.md',     # Markdown file
    '.rtf',    # Rich Text Format
    '.csv',    # Comma-Separated Values
    '.log',    # Log file
    '.xml',    # XML file
    '.yaml',   # YAML Ain't Markup Language
    '.yml',    # YAML Ain't Markup Language
    '.ini',    # Initialization file
    '.conf',   # Configuration file
    '.cfg',    # Configuration file
    '.sql',    # SQL file
    '.tex',    # LaTeX file
    '.html',   # Hypertext Markup Language
    '.htm',    # Hypertext Markup Language
    '.srt',    # SubRip Subtitle
    'README',  # README file
]

def parse_oss_detect_backdoor_file(file_path):
    file_parts = file_path.split(os.sep)
    package_information = {}
    if file_parts[-2] in ['js', 'python', 'ruby']:
        package_information['dataset'] = file_parts[-3]
    else:
        package_information['dataset'] = file_parts[-2]

    package_information['package'] = file_path.split(os.sep)[-1]

    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)           
            results = []
            isbenign = True
            for run in data.get('runs', []):
                number_of_alert = Counter()
                for result in run.get('results', []):
                    # Extract the physical location
                    for location in result.get('locations', []):
                        physical_location = location.get('physicalLocation', {})
                        file_path = physical_location.get('address', {}).get('fullyQualifiedName', 'Unknown')
                        
                        # Check if file path does not end with specified extensions
                        if not file_path.endswith(tuple(FILE_TEXT_EXTENSION)):
                            number_of_alert[file_path] += 1
                    
                for file, count in number_of_alert.most_common():
                    isbenign = False
                    results.append({
                        'dataset': package_information['dataset'],
                        'package': package_information['package'],
                        'file': file,
                        'number_of_alerts': count,
                    })

            if isbenign:
                results.append({
                    'dataset': package_information['dataset'],
                    'package': package_information['package'],
                    'file': 'No file',
                    'number_of_alerts': 0,
                })
            
            return results
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error processing file {file_path}: {e}")
        return []
    

def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Dataset', 'Package', 'File', 'Number of alerts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Dataset': result['dataset'],
                'Package': result['package'],
                'File': result['file'],
                'Number of alerts': result['number_of_alerts'],
            })


def explore_and_parse_files(root_dir):
    """return a list of results from parsing JSON files in the root directory."""
    all_results = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and not is_empty_file(file_path):
                results = parse_oss_detect_backdoor_file(file_path)
                all_results.extend(results)
    return all_results

def main():
    parser = argparse.ArgumentParser(description='Parse OSS Detect Backdoor results and save to CSV.')
    parser.add_argument('root_dir', type=str, help='Root directory containing JSON files to parse')
    parser.add_argument('output_file', type=str, help='Output CSV file path')
    args = parser.parse_args()

    results = explore_and_parse_files(args.root_dir)
    save_results_to_csv(results, args.output_file)
    


if __name__ == "__main__":
    main()
