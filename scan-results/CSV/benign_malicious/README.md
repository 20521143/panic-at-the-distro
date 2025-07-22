# Benign and Malicious Scan Results

This directory contains CSV files with extracted alerts from various security scanners, covering both **benign** and **malicious** samples. The results are organized by tool and, for some tools, further categorized by programming language.

## Summary of Files

| File Name                              | Description                                                      |
|----------------------------------------|------------------------------------------------------------------|
| bandit4mal_mal_benign.csv              | Alerts from Bandit4Mal for both benign and malicious samples.    |
| bincapz_mal_benign.csv                 | Alerts from BinCapz (Malcontent) for all samples.                |
| bincapz_mal_benign_c.csv               | BinCapz alerts for C language samples.                           |
| bincapz_mal_benign_js.csv              | BinCapz alerts for JavaScript samples.                           |
| bincapz_mal_benign_python.csv          | BinCapz alerts for Python samples.                               |
| bincapz_mal_benign_ruby.csv            | BinCapz alerts for Ruby samples.                                 |
| oss_detect_backdoor_mal_benign.csv     | Alerts from OSS Detect Backdoor for all samples.                 |
| packj_mal_benign.csv                   | Alerts from Packj for all samples.                               |

## Data Organization

- **Benign and Malicious**: Each file contains results for both benign and malicious datasets, enabling comparative analysis.
- **Language-Specific**: For Malcontant(BinCapz), alerts are further split by programming language for more granular insights.
- **Tools**: Results are provided for multiple security scanners, including Bandit4Mal, BinCapz (Malcontent), OSS Detect Backdoor, and Packj.


