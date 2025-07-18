for file in *.tar.gz; do
  dir="${file%.tar.gz}"   # Remove the .tar.gz extension to get the directory name
  mkdir -p "$dir"         # Create the directory with the same name
  tar -xzf "$file" -C "$dir"  # Extract the tarball into the directory
done

