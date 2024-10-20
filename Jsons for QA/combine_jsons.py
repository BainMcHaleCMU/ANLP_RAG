import os
import json

def combine_json_files(input_folder, output_file):
    # Dictionary to store data from each JSON file, keyed by filename
    combined_data = {}
    
    # Iterate through all files in the specified folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.json'):
            # Open and load each JSON file with utf-8 encoding
            with open(os.path.join(input_folder, filename), 'r', encoding='utf-8') as file:
                try:
                    data = json.load(file)
                    # Add the data to the dictionary with the filename (without extension) as key
                    combined_data[filename] = data
                except json.JSONDecodeError as e:
                    print(f"Error decoding {filename}: {e}")
    
    # Write the combined data to a single output JSON file
    with open(output_file, 'w', encoding='utf-8') as output:
        json.dump(combined_data, output, indent=4)

# Define the folder containing the JSON files and the output file name
input_folder = 'Jsons for QA'
output_file = 'johndata.json'

# Combine JSON files
combine_json_files(input_folder, output_file)

print(f"Combined JSON saved to {output_file}")
