import json
import csv
import os
import sys
from collections import Counter
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
]



def parse_bandit_results(file_path):
    package_information = {}
    file_path_parts = file_path.split(os.sep)

    if file_path_parts[-2] == 'python':
        package_information['dataset'] = file_path_parts[-3]
    else:
        package_information['dataset'] = file_path_parts[-2]
    # Extract the package name from the file path
    package_information['package'] = file_path_parts[-1][:-5]
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            results = []
            number_of_alert = Counter()
            for result in data.get('results', []):
               file_path = result.get('filename', 'Unknown')
               if not file_path.endswith(tuple(FILE_TEXT_EXTENSION)):
                     if result.get('issue_severity', '').lower() in ['high', 'critical']:
                        number_of_alert[file_path] += 1
            
            for file, count in number_of_alert.most_common():
                results.append({
                    'dataset': package_information['dataset'],
                    'package': package_information['package'],
                    'file': file,
                    'number_of_alerts': count,
                })

            # check if number_of_alert is empty 
            if not number_of_alert:
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
    all_results = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and not is_empty_file(file_path):
                results = parse_bandit_results(file_path)
                all_results.extend(results)
    return all_results




def main():
    parser = argparse.ArgumentParser(description='Parse bandit results')
    parser.add_argument('results_dir', type=str, help='The directory containing the bandit results')
    parser.add_argument('output_file', type=str, help='The output csv file')
    args = parser.parse_args()
    results_dir = args.results_dir
    output_file = args.output_file



    results = explore_and_parse_files(results_dir)
    
    save_results_to_csv(results, output_file)
    


if __name__ == "__main__":
    main()
