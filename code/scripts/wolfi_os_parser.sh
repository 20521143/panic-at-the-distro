#!/bin/bash

# Function to display help message
function display_help() {
    echo "This script helps parse the Wolfi OS YAML files and saves the results to a CSV file."
    echo "It parses the following fields: package_name, version, epoch, repository"
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "Options:"
    echo "  -w, --wolfi-dir DIR      Directory containing the Wolfi YAML files (required)"
    echo "  -o, --output-file FILE   Output CSV file name (default: wolfi_os_YYYY-MM-DD.csv)"
    echo "  -h, --help               Display this help message"
}

# Function to display progress bar
function show_progress() {
    local progress=$(( ($1 * 100) / 2 ))
    local done=$((progress * 4 / 10))
    local left=$((40 - done))
    local fill=$(printf "%${done}s")
    local empty=$(printf "%${left}s")

    printf "\rProgress : [${fill// /#}${empty// /-}] ${progress}%% ($1/$2)"
}

# Initialize variables
WOLFI_DIR=""
TODAY=$(date +"%Y-%m-%d")
OUTPUT_FILE="wolfi_os_${TODAY}.csv"

# Parse command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -w|--wolfi-dir) WOLFI_DIR="$2"; shift ;;
        -o|--output-file) OUTPUT_FILE="$2"; shift ;;
        -h|--help) display_help; exit 0 ;;
        *) echo "Unknown parameter passed: $1"; display_help; exit 1 ;;
    esac
    shift
done

# Check if WOLFI_DIR is provided
if [ -z "$WOLFI_DIR" ]; then
    echo "Error: Wolfi directory must be specified."
    display_help
    exit 1
fi

# Create the output directory if it doesn't exist
OUTPUT_DIR=$(dirname "$OUTPUT_FILE")
mkdir -p "$OUTPUT_DIR"

# Write the header to the CSV file
echo "package_name,version,epoch,repository" > "$OUTPUT_FILE"

# Get the total number of YAML files
TOTAL_FILES=$(ls "$WOLFI_DIR"/*.yaml | wc -l)
CURRENT_FILE=0

# Loop through each YAML file in the directory
for FILE in "$WOLFI_DIR"/*.yaml; do
    # Extract the package name, version, epoch, and repository
    PACKAGE_NAME=$(grep -m 1 'name:' "$FILE" | awk '{print $2}')
    VERSION=$(grep -m 1 'version:' "$FILE" | awk '{print $2}')
    EPOCH=$(grep -m 1 'epoch:' "$FILE" | awk '{print $2}')
    REPOSITORY=$(grep -m 1 'repository:' "$FILE" | awk '{print $2}')

    # If the repository field is not found, use "None"
    if [ -z "$REPOSITORY" ]; then
        REPOSITORY="None"
    fi

    # Append the extracted information to the CSV file
    echo "$PACKAGE_NAME,$VERSION,$EPOCH,$REPOSITORY"
    echo "$PACKAGE_NAME,$VERSION,$EPOCH,$REPOSITORY" >> "$OUTPUT_FILE"

    # Update progress bar
    CURRENT_FILE=$((CURRENT_FILE + 1))
    #show_progress "$CURRENT_FILE" "$TOTAL_FILES"
done

# Finish progress bar
echo -e "\nParsing complete. Results saved to $OUTPUT_FILE"
