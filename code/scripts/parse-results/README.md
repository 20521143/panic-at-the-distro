# Script to parse raw scan results into CSV format. Only alerts with HIGH and CRITICAL severity are included in the CSV.
## The resulting CSV files are located in the folder [scan-results/CSV/malicious/README.md](../../../scan-results/CSV/malicious/README.md)

## Usage:
- [`parse_vt.py`](./parse_vt.py) - Parses VirusTotal scan results from JSON to CSV files, including only high or critical alerts from each security vendor.
    - Usage:
    ```sh
    $ python parse_vt.py -i Directory_with_VirusTotal_JSON_results -o output_csv_filename
    ```
- [`parse_bincapz.py`](parse_bincapz.py) - Parses Malcontent scan results from JSON to CSV files, including only high or critical alerts.
    - Usage:
    ```sh
    $ python parse_bincapz.py -i Directory_with_Malcontent_JSON_results -o output_csv_file
    ```
- [`parse_oss_detect_backdoor.py`](parse_oss_detect_backdoor.py) - Parses Oss-detect-backdoor scan results from JSON to CSV files, including only high or critical alerts.
    - Usage:
    ```sh
    $ python parse_oss_detect_backdoor.py -i Directory_with_OSS_Detect_Backdoor_JSON_results -o output_csv_file
    ```
- [`parse_packj.py`](parse_packj.py) - Parses Packj scan results from JSON to CSV files, including only high or critical alerts.
    - Usage:
    ```sh
    $ python parse_packj.py Directory_with_JSON_files output_csv_file
    ```
- [`parse_bandit4mal.py`](parse_bandit4mal.py) - Parses Bandit4mal scan results from JSON to CSV files, including only high or critical alerts.
    - Usage:
    ```sh
    $ python parse_bandit4mal.py Directory_with_JSON_files output_csv_file
    ```