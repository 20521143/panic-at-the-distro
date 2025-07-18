import os
import csv
from collections import Counter
import sys
import re

VALID_FILE_EXTENSIONS = ['.html', '.css', '.js', '.ts', '.php', '.rb', '.py', '.java', '.cs', '.go', 
    '.r', '.pl', '.c', '.cpp', '.h', '.rs', '.swift', '.kt', '.lua', '.sh']

def normalize_file_path(file_path):    
    return re.sub(r'\s∴\s', '', file_path)

def parse_result_file_helper(data):
    '''Parse the  data using regular expresion to parse struct of log
      and return a list of structured tables.'''
     # Define regex patterns to capture sections of each "RISK" table
    table_pattern = re.compile(
        r'(?P<filepath>/[^\[]+) \[(?P<risk_level>[^\]]+)]\n'
        r'-+\n'
        r'RISK\s+KEY.*?\n-+\n(?P<entries>(?:.+\n)+?)(?=\n?-+-+\n|$)',
        re.MULTILINE
    )
    entry_pattern = re.compile(r'(?P<level>LOW|MED|HIG|CRIT)\s+(?P<key>[^\s]+)\s+(?P<description>.+?)\s{2,}(?P<evidence>.+)')
    # Parse the log data
    parsed_tables = []
    for match in table_pattern.finditer(data):
        # Extract table details
        filepath = match.group("filepath").strip()
        risk_level = match.group("risk_level").strip()
        entries_text = match.group("entries")
        
        # Parse each entry in the table
        entries = []
        for entry in entry_pattern.finditer(entries_text):
            entries.append({
                "level": entry.group("level"),
                "key": entry.group("key"),
                "description": entry.group("description"),
                "evidence": entry.group("evidence")
            })
        
        # Append to list as a structured table dictionary
        parsed_tables.append({
            "filepath": normalize_file_path(filepath).replace('/home/lyvd/', ''),
            "risk_level": risk_level,
            "entries": entries
        })
    return parsed_tables
    

def parse_result_file(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return []
    
    package_information = {}
    package_information['dataset'] = file_path.split(os.sep)[-3]
    package_information['package'] = file_path.split(os.sep)[-1]

    results = []

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        log_data = f.read()
        if not log_data.strip():
            return []
    
        parsed_tables = parse_result_file_helper(log_data)
   
    

        for table in parsed_tables:
            if table['filepath'].endswith(tuple(VALID_FILE_EXTENSIONS)):
                results.append({
                    'dataset': package_information['dataset'],
                    'package': package_information['package'],
                    'file': table['filepath'],
                    'number_of_alerts': len(table['entries']),
                })   
    
    return results

                        

def explore_and_parse_logs(root_dir):
    all_results = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.isfile(file_path):
                results = parse_result_file(file_path)
                all_results.extend(results)
    return all_results

def save_results_to_csv(results, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Dataset', 'Package', 'File', 'Number of alerts']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow({
                'Dataset' : result['dataset'],
                'Package' : result['package'],
                'File' : result['file'],
                'Number of alerts' : result['number_of_alerts'],
            })

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = os.path.abspath(os.path.join(script_dir ,'../../scan-results/bincapz'))
    output_file = os.path.abspath(os.path.join(script_dir ,'../../results-csv/bincapz/bincapz.csv'))
    results = explore_and_parse_logs(results_dir)   
    save_results_to_csv(results, output_file)


if __name__ == "__main__":
    main()