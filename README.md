# patd-results: A Study of Malware Prevention in Linux Distributions

This repository contains the source code and data for the paper titled "A Study of Malware Prevention in Linux Distributions". The primary objective is to evaluate the performance of six open-source malware detection scanners.

## Table of Contents

1. [Dataset](#Dataset)
2. [Setup Malware Scanners](#setup-malware-scanners)
3. [Source Code](#source-code)
4. [Citation](#citation)

## Dataset
- [`Melange files`](./dataset/malicious/melange-files/): This folder contains [melange file](https://github.com/chainguard-dev/melange), which is used to build APK files.
- [`PATD malware datasets`](./dataset/malicious/samples/patd-malware-datasets/): This contains a malware dataset in paper.
- [`Wolfi upstreams repository apks`](./dataset/benign/CSV/upstream_repos_filtered.csv):  This contains a list of Wolfi APKs whose source code is open-source.
- [`scan-results`](https://1drv.ms/u/c/883a8f77a357bed3/EdO-V6N3jzoggIhpKgAAAAABxMjFiK5zEWN7V9PBzC4smw?e=jDHvdE) - Results from malware detection scanners.

| **Dataset** |                                              **Name**                                              |                **Location in Repo**                |
|:-----------:|:--------------------------------------------------------------------------------------------------:|:--------------------------------------------------:|
| Dataset #1  | Historical Samples of Open Source Source Code Malware                                              | [dataset#1](./dataset/malicious/samples/patd-malware-datasets/dataset1/)                 |
| Dataset #2  | Historical Examples of Malicious Linux Binaries                                                    | [dataset#2](./dataset/malicious/samples/patd-malware-datasets/dataset2/)            |
| Dataset #3  | Synthetic Examples of Open Source Source Code Malware                                              | [dataset#3](./dataset/malicious/samples/patd-malware-datasets/dataset3/)      |
| Dataset #4  | Synthetic Examples of Open Source Linux Binaries                                                   | [dataset#4](./dataset/malicious/samples/patd-malware-datasets/dataset4/) |
| Dataset #5  | Synthetic example of Linux malicious source code turned into APKs                                  | [dataset#5](./dataset/malicious/samples/patd-malware-datasets/dataset5/)  |
| Dataset #6  | "Over Time Datasets" For Assessing Capability Analysis Tools (capslock) - Golang only for capslock | [dataset#6](./dataset/malicious/samples/patd-malware-datasets/dataset6)                     |


## Setup Malware Scanners

|            **Tool**           |                                 **Link**                                 |       **Type**      |
|:-----------------------------:|:------------------------------------------------------------------------:|:-------------------:|
| VirusTotal                    | https://www.virustotal.com/                                              | Binary scanner      |
| cg-packj                      | [cg-packj](./code/scripts/cg-packj/)                                     | Source code scanner |
| OSSGadget OSS Detect Backdoor | https://github.com/microsoft/OSSGadget/tree/main/src/oss-detect-backdoor | Source code scanner |
| Malcontent                       | https://github.com/chainguard-dev/malcontent                                | Binary scanner      |
| capslock                      | https://github.com/google/capslock                                       | Source code scanner |
| bandit4mal                    | https://github.com/lyvd/bandit4mal                                       | Source code scanner |



## Source code

- **Jupyter Notebook**: [`/notebook/PATD_data_analysis.ipynb`](./code/notebooks/PATD_data_analysis.ipynb) - Contains code to generate statistical tables for each scanning tool and ROC curves for the paper.
    - Statistical tables and metrics for each tool:
        - [Performance of VirusTotal (VT) on the Wolfi-upstream-repos and Wolfi apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=9PeQqQKnrtyb)
        - [Performance of Malcontent on the Wolfi-upstream-repos and Wolfi apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=x_s5CG7kSeYG)
        - [Performance of Oss-detect-backdoor on the Wolfi-upstream-repos and Wolfi apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=KdhF1lPzhjET)
        - [Performance of Packj on the Wolfi-upstream-repos and Wolfi apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=9Xfi6meT7qP6)
        - [Performance of Bandit4mal on the Wolfi-upstream-repos and Wolfi apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=mSrlqPbrokEI)
    - ROC Curves:
        - [Combined ROC curves](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=7laHuiT4zoVF)
        - [Datset 1 and Wolfi upstream repos](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=lR9xkOJXhOEi&line=1&uniqifier=1)
        - [Dataset 4 and Wolfi  upstream repos](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=WTw80vRBmGFW&line=1&uniqifier=1)
        - [Dataset 2 and Wolfi-apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=wNopHh50njGM&line=1&uniqifier=1)
        - [Dataset 3 and Wolfi-apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=d2KLnPVJJDBy)
        - [Dataset 5 and Wolfi-apks](https://colab.research.google.com/drive/1yymf0-56YQg4lQgg7hk0J1AuocYyTU8X?authuser=2#scrollTo=UqiBNkuNO0ta)

- **Parsed Results format CSV**: [`/results-csv`](./scan-results/CSV/malicious/) - Contains CSV files with parsed results from the [`scan-results`](https://1drv.ms/u/c/883a8f77a357bed3/EdO-V6N3jzoggIhpKgAAAAABxMjFiK5zEWN7V9PBzC4smw?e=PZvejn). These files include only HIGH or CRITICAL alerts, except for [`./scan-results/CSV/benign_malicious`](./scan-results/CSV/benign_malicious/), which contains both benign and malicious.
- **Scripts**: 
    - [`scripts`](./code/scripts/) - Contains automation scripts for running malware detection scanners.
    - [`/parse-results`](./code/scripts/parse-results/) - Script to parse raw scan results into CSV format.
        - [`./code/scripts/parse-results/parse_vt.py`](./code/scripts/parse-results/parse_vt.py) - Parse VirusTotal scan results from JSON to CSV files, including only high or critical alerts from each security vendor.
            - Usage: 
            ```sh
            $ python parse_vt.py -i Directory_for_saving_VirusTotal_scan_results_in_JSON -o csv_filename
            ```
         - [`./code/scripts/parse-results/parse_bincapz.py`](./code/scripts/parse-results/parse_bincapz.py) -  Parse Malcontent scan results from JSON to CSV files, including only high or critical alerts.
             - Usage:
             ```sh
             $ python parse_bincapz.py -i Directory_containing Malcontent_scan_results -o Output_CSV_file
             ```
         - [`./code/scripts/parse-results/parse_oss_detect_backdoor.py`](./code/scripts/parse-results/parse_oss_detect_backdoor.py) - Parse Oss-detect-backdoor scan results from JSON to CSV files, including only high or critical alerts.
             - Usage:
                 ```sh
                 $ python parse_oss_detect_backdoor.py -i Directory_containing_OSS_Detect_Backdoor_scan_results -o Output_CSV_file
                 ```
         - [`./code/scripts/parse-results/parse_packj.py`](./code/scripts/parse-results/parse_packj.py) -  Parse Packj scan results from JSON to CSV files, including only high or critical alerts.
           - Usage:
             ```sh
             $ python parse_packj.py The_path_to_the_directory_contain_JSON_files CSV_files
             ```
         
         - [`./code/scripts/parse-results/parse_bandit4mal.py`](./code/scripts/parse-results/parse_bandit4mal.py) - Parse Bandit4mal scan results from JSON to CSV files, including only high or critical alerts.
          
           - Usage:
             ```sh
             $ python parse_bandit4mal.py directory_contain_JSON_files csv_file
             ```
    - [`./dataset/benign/scripts/wolfi_modified_apk_download.sh`](./dataset/benign/scripts/wolfi_modified_apk_download.sh) - Script to download APK files from Wolfi registries with. Use the following command to execute the script:
        ```sh
        $ wolfi_modified_apk_download.sh --save-path /path-to-save --csv-file ./dataset/benign/CSV/wolfi_parsed.csv
        ```
        - **--csv-file (optional)**: [`./dataset/benign/CSV/wolfi_parsed.csv`](./dataset/benign/CSV/wolfi_parsed.csv) - This file contains a list of APK files with available source code in the Wolfi registry. This option will download only the APKs listed in the CSV.
    - **Running malware scanner**
        - [`/scripts/vt_scan.py`](./code/scripts/vt_scan.py) - script to automatically submit sample in VirusTotal and get report and save as JSON file.
            - Usage: 
            ```sh
            $ python vt_scan.py Directory_with_files_to_scan Directory_to_save_scan_results 
            ```
        - [`./code/scripts/run_bincapz.py`](./code/scripts/run_bincapz.py) - This script is used to run Malcontent tool to scan sample.
            - Usage:
            ```sh
            $ python run_bincapz.py Directory_with_files_to_scan Directory_to_save_scan_results 
            ```
        - [`./code/scripts/run_odb.py`](./code/scripts/run_odb.py) - This script is used to run Oss-detect-backdoor tool to scan sample files.
             - Usage:
            ```sh
            $ python run_odb.py Directory_with_files_to_scan Directory_to_save_scan_results 
            ```
        - [`./code/scripts/run_bandit4mal.py`](./code/scripts/run_bandit4mal.py) - This script is used to run the Bandit4mal tool to scan Python sample files.
             - Usage:
            ```sh
            $ python run_bandit4mal.py Directory_with_files_to_scan Directory_to_save_scan_results 
            ```
        - [`./code/scripts/run_lmd.py`](./code/scripts/run_lmd.py) - This script is used to run [the Linux malware detection](https://github.com/rfxn/linux-malware-detect) tool.
             - Usage:
            ```sh
            $ python run_lmd.py Directory_with_files_to_scan Directory_to_save_scan_results 
            ``` 
    - **Detect programming language of Wolfi Upstream repository**
        - [`./code/scripts/detect_programing_language.py`](./code/scripts/detect_programing_language.py) - The modified Packj project contains three different scripts to scan packages for each programming language (Python, JavaScript, Ruby), so we need to detect programming language of wolfi-apk. In this script, we use GitHub API and [github-linguist](https://github.com/github-linguist/linguist) tool. 
            - Usage:
            ```sh
            $ python detect_programming_language.py URL_of_the_project_or_local_file
            ```
         
        **Modified Packj tool supports three languages:**
        
         - **Python**: [`./code/scripts/cg-packj/cg_scanner.py`](./code/scripts/cg-packj/cg_scanner.py) - Script to scan Python samples.
         - **JavaScript**: [`./code/scripts/cg-packj/cg_scanner_js.py`](./code/scripts/cg-packj/cg_scanner_js.py) - Script to scan JavaScript samples.
         - **Ruby**: [`./code/scripts/cg-packj/cg_scanner_ruby.py`](./code/scripts/cg-packj/cg_scanner_ruby.py) - Script to scan Ruby samples.

    



