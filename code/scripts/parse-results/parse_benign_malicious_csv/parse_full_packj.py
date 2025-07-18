import csv
import os
import json
import argparse
import multiprocessing

def is_empty_file(file_path):
    return os.stat(file_path).st_size == 0

def filter_languages(language):
    allowed_languages = {"python": "Python", "javascript": "Javascript", "ruby": "Ruby"}
    return allowed_languages.get(language.lower(), None)

def get_source_type_full_name(api_result, api_configs):
    for api_config in api_configs:
        if api_config.get('type') == api_result.get('type'):
            if api_config.get('name') == api_result.get('name'):
                if api_config.get('fullName') == api_result.get('fullName'):
                    if api_config.get('baseType', '') == api_result.get('baseType', ''):
                        return api_config.get('sourceType', api_config.get('sourceSink', '')), api_config.get('fullName')
                   
            
    return None, None

def process_single_file(file_path):
    """Processes a single file and extracts relevant package data."""

        
    file_path_parts = file_path.split(os.sep)
    package_information = {}
    
    # Determine the dataset name based on the file path structure
    if file_path_parts[-2] in ['js', 'python', 'ruby']:
        package_information['dataset'] = file_path_parts[-3]
    else:
        package_information['dataset'] = file_path_parts[-2]
    # Extract the package name from the file path
    package_information['package'] = file_path_parts[-1]

    results = []
    try:
        
        with open(file_path, "r") as f:
            data = json.load(f)
            package = data.get('pkgs', [])

            for package_data in package:

                language = package_data.get('language')
                package_name = package_data.get('pkgName')
                config_type_source = {}
                api_configs = package_data.get('config', {}).get('apis', [])

                for api in package_data.get("apiResults", []):  # Safely iterate over 'config'
                        
                        source_type,  full_name = get_source_type_full_name(api, api_configs)

                        if source_type:    
                            results.append({
                                'Dataset': package_information['dataset'],
                                'Package': package_information['package'],
                                'Language': filter_languages(language.lower()),
                                'fullName': full_name,
                                'sourceType': source_type
                            })
                        

        if len(results) == 0:
            results.append({
                'Dataset': package_information['dataset'],
                'Package': package_information['package'],
                'Language': filter_languages(language.lower()),
                'fullName': 'benign',
                'sourceType': 'No sourceType'
            })
        return results
    except json.JSONDecodeError:
        print(f"Error decoding JSON in file: {os.path.basename(file_path)}")
        return []
    except Exception as e:
        print(f"An error occurred with {os.path.basename(file_path)}: {e}")
        return []


def explore_file(directory_path):
    #wakk dir
    all_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if not file.endswith('.json') and not is_empty_file(os.path.join(root, file)):
                all_files.append(os.path.join(root, file))


    if not all_files:
        print("No files found in the directory.")
        return []

    with multiprocessing.Pool() as pool:
        results = pool.map(process_single_file, all_files)
        pool.close()
        pool.join()

    # Flatten the results list
    return [item for sublist in results for item in sublist]


def save_csv(data, output_file):
    """Saves extracted data into a CSV file."""
    if not data:
        print("No data to write to the CSV.")
        return

    try:
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Dataset', 'Package', 'Language', 'fullName', 'sourceType'])
            for row in data:
                writer.writerow([row['Dataset'], row['Package'], row['Language'], row['fullName'], row['sourceType']])
        print(f"Data successfully written to {output_file}")
    except Exception as e:
        print(f"Failed to write data to CSV: {e}")


def main():
    """Main function to parse  files and save results to a CSV file."""
    parser = argparse.ArgumentParser(description="Parse JSON files and save results to a CSV file.")
    parser.add_argument("directory", help="Directory containing JSON files to parse.")
    parser.add_argument("output", help="Output CSV file to save results.")
    args = parser.parse_args()


    # Check if the provided directory exists
    if not os.path.isdir(args.directory):
        print(f"Error: The directory '{args.directory}' does not exist.")
        return

    # Process results
    results = explore_file(args.directory)

    # Save the results to the CSV file
    save_csv(results, args.output)


if __name__ == '__main__':
    main()
