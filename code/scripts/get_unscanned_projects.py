import os
import pandas as pd
import sys
import argparse
import re

def cleaned_package_name(project):
    filtered_cleaned_packages = {
        "opa-envoy-0.68.0_rc4-r0": "opa-envoy",
        "tzdata-2024b-r0": "tzdata",
        "rstudio-2023.12.1_p402-r1": "rstudio",
        "kpt-1.0.0_beta30-r0": "kpt",
    }

    if project in filtered_cleaned_packages.keys():
        return filtered_cleaned_packages[project]


    pattern = r'(.+)-[0-9]+(?:\.[0-9]+)*(?:_git[0-9]+)?(?:-r[0-9]+)?$'

    # get the matching packages with the pattern, remove not match
    if match := re.search(pattern, project, re.IGNORECASE):
        return match.group(1)

    print(f"Could not find a matching package for {project}")


    return project

def remove_extension(file):
    EXTENSIONS = ('.zip.apk', '.apk', '.zip', '.json',
                   '.zip.json', '.gem', '.tar.gz', '.gz',
                   '.gem', '.tar', '.tgz')
    while True:
        for ext in EXTENSIONS:
            if file.endswith(ext):
                file = file[:-len(ext)]
                break
        else:
            break
    return file

def get_malicious_samples(malicious_dir):
    malicious_dataset = {
    "dataset1": set(),
    "dataset2" : set(),
    "dataset3" : set(),
    "dataset4" : set(),
    "dataset5" : set(),
    }


    for dataset in malicious_dataset.keys():
        for root, _, files in os.walk(os.path.join(malicious_dir, dataset)):
            for file in files:
                malicious_dataset[dataset].add(remove_extension(file))

    return malicious_dataset
        


def  get_scanned_projects(scan_results_dir):

    # Initialize a dictionary to store scanned projects
    scanned_projects = {
        'bincapz': dict(),
        'packj': dict(),
        'vt': dict(),
        'oss-detect-backdoor': dict(),
        'bandit4mal': dict()
    }

    # Loop through the scan-results directory
    for tool in scanned_projects.keys():
        tool_dir = os.path.join(scan_results_dir, tool)
        if os.path.exists(tool_dir):
            for dataset in os.listdir(tool_dir):
                dataset_dir = os.path.join(tool_dir, dataset)
                if os.path.isdir(dataset_dir):
                    scanned_projects[tool][dataset] = set()
                    for root, _, files in os.walk(dataset_dir):
                        for file in files:
                            if dataset == 'wolfi-apks':
                                project_name = cleaned_package_name(remove_extension(file))
                                scanned_projects[tool][dataset].add(project_name)
                            else:
                                project_name = remove_extension(file)
                                scanned_projects[tool][dataset].add(project_name)
    return scanned_projects


def main():
    #get input file csv and scan-result dir from user
    parser = argparse.ArgumentParser()
    parser.add_argument('csv_file_path', help='path to the input file csv')
    parser.add_argument('scan_results_dir', help='path to the scan-results directory')
    parser.add_argument('malicious_dir', help='path to the malicious samples directory')
    args = parser.parse_args()






    data_package = pd.read_csv(args.csv_file_path)

    packages = data_package['package_name'].to_list()

    maliciouse_samples = get_malicious_samples(args.malicious_dir)

    scanned_samples = get_scanned_projects( args.scan_results_dir)

        # Identify un-scanned projects
    unscanned_projects = {tool: {} for tool in scanned_samples.keys()}

    for tool, datasets in scanned_samples.items():
        for dataset, scanned in datasets.items():
            if dataset in ['upstream-repos', 'wolfi-apks']:
                unscanned_projects[tool][dataset] = set(packages) - scanned
            else:
                unscanned_projects[tool][dataset] = maliciouse_samples[dataset] - scanned


    for tool, datasets in unscanned_projects.items():
        for dataset, projects in datasets.items():
            print(f'{tool} - {dataset}: {len(projects)}')






if __name__ == '__main__':
    main()


