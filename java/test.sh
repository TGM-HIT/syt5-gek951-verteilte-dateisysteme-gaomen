
#!/bin/bash

# Base API URL
API_BASE_URL="http://localhost:8080"

# Function to upload a file
upload_file() {
    read -p "Enter the file path to upload: " file_path
    if [[ -f "$file_path" ]]; then
        file_name=$(basename "$file_path")
        echo "Uploading $file_name..."

        curl -X POST -F "file=@${file_path}" "${API_BASE_URL}/upload" -w "\nUpload Status: %{http_code}\n"
    else
        echo "File does not exist! Please check the path and try again. >.<"
    fi
}

# Function to download a file
download_file() {
    read -p "Enter the file name to download: " file_name
    echo "Downloading $file_name..."

    curl -X GET "${API_BASE_URL}/download/${file_name}" -o "$file_name" -w "\nDownload Status: %{http_code}\n"
}

# Function to delete a file
delete_file() {
    read -p "Enter the file name to delete: " file_name
    echo "Deleting $file_name..."

    curl -X DELETE "${API_BASE_URL}/delete/${file_name}" -w "\nDelete Status: %{http_code}\n"
}

# Menu for CRUD operations
while true; do
    echo "Choose an option:"
    echo "1. Upload a file"
    echo "2. Download a file"
    echo "3. Delete a file"
    echo "4. Exit"
    read -p "Option: " option

    case $option in
        1) upload_file ;;
        2) download_file ;;
        3) delete_file ;;
        4) echo "Goodbye! (✿◠‿◠)" ; exit 0 ;;
        *) echo "Invalid option! Please choose 1, 2, 3, or 4. (⁄ ⁄•⁄ω⁄•⁄ ⁄)" ;;
    esac
done
