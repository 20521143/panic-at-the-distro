# Malicious Scan Results

This directory contains extracted alerts from various security scanner results, focusing exclusively on **HIGH** and **CRITICAL** severity alerts. The data is organized by tool and, for some tools, further categorized by programming language.

## Summary of Files

| File/Folder                                   | Description                                                                                 |
|-----------------------------------------------|---------------------------------------------------------------------------------------------|
| [bandit4mal.csv](./bandit4mal.csv)            | Alerts from the Bandit4Mal scanner.                                                         |
| [oss-detect-backdoor.csv](./oss-detect-backdoor.csv) | Alerts from the OSS Detect Backdoor tool.                                             |
| [packj.csv](./packj.csv)                      | Alerts from the Packj scanner.                                                              |
| [vt.csv](./vt.csv)                            | Alerts from VirusTotal scans.                                                               |
| [bincapz.csv](./bincapz.csv)                  | Alerts from the Malcontent (BinCapz) scanner.                                               |
| [bincapz_language/](./bincapz_language/README.md)      | Language-specific Malcontent alerts (C, JavaScript, Python, Ruby).                             |

## Tools Overview

- **Bandit4Mal**: Static analysis tool for detecting security issues in Python code.
- **OSS Detect Backdoor**: Tool for identifying potential backdoors in open-source software.
- **Packj**: Security scanner for open-source packages, focusing on supply chain risks.
- **VirusTotal**: Aggregates results from multiple antivirus engines and tools.
- **Malcontent (BinCapz)**: Binary analysis tool for extracting security alerts from compiled code.

## Language-Specific Alerts

For deeper analysis, BinCapz alerts are also extracted and grouped by the main programming language of each sample. The following languages are included:

- [C](./bincapz_language/bincapz_c.csv)
- [JavaScript](./bincapz_language/bincapz_js.csv)
- [Python](./bincapz_language/bincapz_python.csv)
- [Ruby](./bincapz_language/bincapz_ruby.csv)


