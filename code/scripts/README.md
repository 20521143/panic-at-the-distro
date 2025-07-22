# Automation Scripts for Malware Detection Scanners

This directory contains automation scripts for running various malware detection scanners and related utilities.

## Running Malware Scanners

- [`vt_scan.py`](vt_scan.py): Automatically submits samples to VirusTotal, retrieves reports, and saves them as JSON files.
  - **Usage:**
    ```sh
    python vt_scan.py <Directory_with_files_to_scan> <Directory_to_save_scan_results>
    ```
- [`run_bincapz.py`](run_bincapz.py): Runs the Malcontent tool to scan samples.
  - **Usage:**
    ```sh
    python run_bincapz.py <Directory_with_files_to_scan> <Directory_to_save_scan_results>
    ```
- [`run_odb.py`](run_odb.py): Runs the OSS Detect Backdoor tool to scan sample files.
  - **Usage:**
    ```sh
    python run_odb.py <Directory_with_files_to_scan> <Directory_to_save_scan_results>
    ```
- [`run_bandit4mal.py`](run_bandit4mal.py): Runs the Bandit4Mal tool to scan Python sample files.
  - **Usage:**
    ```sh
    python run_bandit4mal.py <Directory_with_files_to_scan> <Directory_to_save_scan_results>
    ```
- [`run_lmd.py`](run_lmd.py): Runs the [Linux Malware Detect](https://github.com/rfxn/linux-malware-detect) tool.
  - **Usage:**
    ```sh
    python run_lmd.py <Directory_with_files_to_scan> <Directory_to_save_scan_results>
    ```

## Detect Programming Language of Wolfi Upstream Repository

- [`detect_programing_language.py`](detect_programing_language.py): Detects the programming language of a Wolfi APK. This is necessary because the modified Packj project contains three different scripts to scan packages for Python, JavaScript, and Ruby. The script uses the GitHub API and the [github-linguist](https://github.com/github-linguist/linguist) tool.
  - **Usage:**
    ```sh
    python detect_programming_language.py <URL_of_the_project_or_local_file>
    ```

### Modified Packj Tool Language Support

- **Python:** [`cg-packj/cg_scanner.py`](cg-packj/cg_scanner.py) — Script to scan Python samples.
- **JavaScript:** [`cg-packj/cg_scanner_js.py`](cg-packj/cg_scanner_js.py) — Script to scan JavaScript samples.
- **Ruby:** [`cg-packj/cg_scanner_ruby.py`](cg-packj/cg_scanner_ruby.py) — Script to scan Ruby samples.