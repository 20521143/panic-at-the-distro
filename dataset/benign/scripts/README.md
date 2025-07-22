- [`wolfi_modified_apk_download.sh`](./wolfi_modified_apk_download.sh) — Script to download APK files from Wolfi registries. Use the following command to execute the script:
    ```sh
    wolfi_modified_apk_download.sh --save-path /path-to-save --csv-file ./dataset/benign/CSV/wolfi_parsed.csv
    ```
    - **--csv-file (optional):** [`./dataset/benign/CSV/wolfi_parsed.csv`](../CSV/wolfi_parsed.csv) — This file contains a list of APK files with available source code in the Wolfi registry. If provided, only the APKs listed in the CSV will be downloaded.