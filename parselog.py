import re
import os
import shutil
import argparse
import sys

def process_files(ip_list_file, file_directory, regex_pattern):
    # Read the IP addresses from the provided file
    with open(ip_list_file, 'r') as ip_file:
        ip_addresses = ip_file.read().splitlines()

    # Iterate over the files in the specified directory
    for file_name in os.listdir(file_directory):
        file_path = os.path.join(file_directory, file_name)

        # Skip directories and non-regular files
        if not os.path.isfile(file_path):
            continue

        # Read the contents of the file
        with open(file_path, 'r') as file:
            file_content = file.readlines()

        # Use regex to find matching lines
        matches = re.findall(regex_pattern, ''.join(file_content), re.MULTILINE)

        # Create a new file with a suffix for each matching line
        for match in matches:
            transaction_id = match[0]
            ip_address = match[1]

            if ip_address in ip_addresses:
                # Extract the part of the input filename before the dash character
                file_basename = os.path.basename(file_name)
                output_filename = file_basename.split('-')[0]

                # Create a new file with the extracted name and a suffix if it doesn't exist
                new_file_path = os.path.join(file_directory, f"{output_filename}.new")
                if not os.path.exists(new_file_path):
                    shutil.copy2(file_path, new_file_path)

                # Append the matching line to the new file
                with open(new_file_path, 'a') as new_file:
                    new_file.write(''.join([line for line in file_content if transaction_id in line]))

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Script to process files based on IP address matching")

    # Define the command-line arguments
    parser.add_argument("--ip-list-file", help="Path to the file containing newline-delimited IP addresses")
    parser.add_argument("--file-directory", help="Path to the directory where the files are located")
    parser.add_argument("--regex-pattern", help="Regular expression pattern to match the desired lines in the files")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract the arguments
    ip_list_file = args.ip_list_file
    file_directory = args.file_directory
    regex_pattern = args.regex_pattern

    # Check if any argument is missing
    if not all([ip_list_file, file_directory, regex_pattern]):
        parser.print_help()
        sys.exit(1)

    # Call the function to process the files
    process_files(ip_list_file, file_directory, regex_pattern)
