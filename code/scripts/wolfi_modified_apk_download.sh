#!/bin/bash



# Function to display usage information
usage() {
    echo "This script downloads APK packages from the Wolfi repository found at https://apk.dag.dev"
    echo "Currently it targets x86_64 APK packages"
    echo
    echo "Usage: $0 --save-path <path> [--number-of-packages <number>] [--csv-file <file>]"
    echo "  --save-path           Required path to store the downloaded APKs"
    echo "  --number-of-packages  The number of packages to process (optional)"
    echo "  --csv-file            Path to the CSV file for filtering packages (optional)"
    exit 1
}

# Parse the named arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --save-path)
            SAVE_PATH="$2"
            shift
            ;;
        --number-of-packages)
            NUM_PACKAGES="$2"
            shift
            ;;
        --csv-file)
            CSV_FILE="$2"
            shift
            ;;
        --help)
            usage
            ;;
        *)
            echo "Unknown parameter passed: $1"
            usage
            ;;
    esac
    shift
done

# Validate required arguments
if [ -z "$SAVE_PATH" ]; then
    echo "Error: --save-path is required."
    usage
fi


# Set default value for NUM_PACKAGES if not provided
NUM_PACKAGES=${NUM_PACKAGES:-}

# Create the save path directory if it doesn't exist
mkdir -p "$SAVE_PATH"

# Fetch the list of available packages and remove .apk suffix
raw_package_list=$(cat <(curl -sL https://apk.dag.dev/https/packages.wolfi.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX) \
                        <(curl -sL https://apk.dag.dev/https/packages.cgr.dev/os/x86_64/APKINDEX.tar.gz/APKINDEX) \
                        <(curl -sL https://apk.dag.dev/https/packages.cgr.dev/extras/x86_64/APKINDEX.tar.gz/APKINDEX))

# Extract package names and remove .apk suffix
if [ -n "$NUM_PACKAGES" ]; then
    package_repo_names=$(echo "$raw_package_list" | sed 's/\.apk$//' | head -n "$NUM_PACKAGES")
else
    package_repo_names=$(echo "$raw_package_list" | sed 's/\.apk$//')
fi

echo "Packages loaded: $(echo "$package_repo_names" | wc -l)"

# Define function to filter packages based on a CSV file, removing version info
function filter_packages_with_repo() {
    local csv_file="$1"
    local raw_package_list="$2"
    
    # 1. Extract unique package names from the CSV (first column)
    local csv_package_names=$(awk -F, 'NR > 1 {print $1}' "$csv_file" | sort -u)

    # 2. Create an associative array (set) of package names from the CSV for quick lookup
    declare -A csv_package_set
    while IFS= read -r package; do
        csv_package_set["$package"]=1
    done <<< "$csv_package_names"
    
    # 3. Define a regex pattern to strip version information from package names
    local version_pattern='-[0-9]+(\.[0-9]+)*(_git[0-9]+)?(-r[0-9]+)?$'
    
    # 4. Filter and clean the package names if they are in the CSV package set
    local filtered_cleaned_packages=()
    while IFS= read -r package; do
        # Remove version information from package names
        local cleaned_package=$(echo "$package" | sed -E "s/$version_pattern//")
        
        # Check if the cleaned package exists in the CSV package set
        if [[ -v csv_package_set["$cleaned_package"] ]]; then
            filtered_cleaned_packages+=("$package")
        fi  
    done <<< "$raw_package_list"

    #Some files were not included in the pattern, so we added them manually.
    filtered_cleaned_packages+=("opa-envoy-0.68.0_rc4-r0")
    filtered_cleaned_packages+=("tzdata-2024b-r0")
    filtered_cleaned_packages+=("rstudio-2023.12.1_p402-r1")
    filtered_cleaned_packages+=("kpt-1.0.0_beta30-r0")

    # 5. Output the filtered package names
    echo "${filtered_cleaned_packages[@]}"
}

# Filter the package names based on the CSV file

if [ -n "$CSV_FILE" ]; then
    if [ ! -f "$CSV_FILE" ]; then
        echo "Error: CSV file '$CSV_FILE' does not exist."
        exit 1
    fi
    filtered_package_repo_names=$(filter_packages_with_repo "$CSV_FILE" "$package_repo_names")
    package_repo_names=$(echo "$filtered_package_repo_names" | tr ' ' '\n')
    echo "Packages loaded after filter: $(echo "$package_repo_names" | wc -l)"
fi

# Total number of packages to process
total_packages=$(echo "$package_repo_names" | wc -l)
completed_packages=0

# Loop through each package-repo-name
echo "$package_repo_names" | while read -r package_repo_name; do
    # Define the package URL and output directory
    ARCH="x86_64"  # Replace with your architecture if different
    PACKAGE_URL="https://packages.wolfi.dev/os/$ARCH/$package_repo_name.apk"

    if [ ! -e $SAVE_PATH/$package_repo_name.apk ]; then
	# Download the APK package to the specified output directory
	wget -q $PACKAGE_URL -O $SAVE_PATH/$package_repo_name.apk


	echo "Downloaded $package_repo_name.apk to $SAVE_PATH"

	# Update progress
	completed_packages=$((completed_packages + 1))
	remaining_packages=$((total_packages - completed_packages))

	echo "Completed: $completed_packages, Remaining: $remaining_packages"
    else
        echo "File exist"
fi
done
