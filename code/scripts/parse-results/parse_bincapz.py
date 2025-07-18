import csv
import os
import json
import argparse

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

def parse_bincapz_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []
    
    file_path_parts = file_path.split(os.sep)
    package_information = {}
    
    # Determine the dataset name based on the file path structure
    if file_path_parts[-2] in ['js', 'python', 'ruby']:
        package_information['dataset'] = file_path_parts[-3]
    else:
        package_information['dataset'] = file_path_parts[-2]
    # Extract the package name from the file path
    package_information['package'] = file_path_parts[-1][:-5]

    # Parse the json file

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data_json = json.load(f)

            data = data_json.get('Files', {})

            results = []

            for dataPath in data:
                risk_level = data[dataPath].get('RiskLevel', '')
                if not dataPath.endswith(tuple(FILE_TEXT_EXTENSION)):
                    
                    if risk_level.lower() in ['high', 'critical']:
                        results.append({
                            'package': package_information['package'],
                            'dataset': package_information['dataset'],
                            'file': dataPath,
                            'risk_level': data[dataPath].get('RiskLevel', '')
                        })
                elif risk_level in ['high', 'critical']:
                    print(f"Skipping file {dataPath} as it is not a valid file type.")
            return results
        
    except Exception as e:
        print(f"Error parsing JSON file {file_path}: {e}")
        return []


def explore_and_parse_logs(root_dir):
    all_results = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path) and file_path.endswith('.json'):
                results = parse_bincapz_file(file_path)
                all_results.extend(results)
    return all_results


def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Package name', 'Dataset', 'File path', 'Risk level (high/critical)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Package name' : result['package'],
                'Dataset' : result['dataset'],
                'File path' : result['file'],
                'Risk level (high/critical)' : result['risk_level']
            })

def main():
    parser = argparse.ArgumentParser(description="Parse bincapz scan results and save to CSV.")
    parser.add_argument('-i', '--input', type=str, required=True, help='Directory containing bincapz scan results.')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output CSV file path.')
    
    args = parser.parse_args()
    
    results_dir = os.path.abspath(args.input)
    output_file = os.path.abspath(args.output)
    
    results = explore_and_parse_logs(results_dir)
    save_results_to_csv(results, output_file)

if __name__ == "__main__":
    main()
