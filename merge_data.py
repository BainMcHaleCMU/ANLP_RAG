import pandas as pd
import json

# Load CSV data
csv_file_path = 'General Info and History Scraper/general_info.csv'
csv_data = pd.read_csv(csv_file_path)

# Load JSON data
json_file_path = 'johndata.json'
with open(json_file_path, 'r') as f:
    json_data = json.load(f)

# Initialize lists to store new data
link_column = []
text_column = []

# Dynamically handle each section
for section_name, section_entries in json_data.items():
    # Convert entire section content into JSON and store it in the 'text' column
    link_column.append(section_name)  # Use the section/event name as the link
    text_column.append(json.dumps(section_entries))  # Store the entire section content as JSON in the 'text' field

# Create a DataFrame for the JSON data
json_df = pd.DataFrame({
    "source": link_column,
    "text": text_column
})

# Ensure that the CSV has 'link' and 'text' columns for merging
if 'source' not in csv_data.columns:
    csv_data['source'] = None  # Add an empty link column if it doesn't exist
if 'text' not in csv_data.columns:
    csv_data['text'] = None  # Add an empty text column if it doesn't exist

# Combine the CSV and JSON data by concatenating rows
combined_data = pd.concat([csv_data, json_df], ignore_index=True)

# Save the merged data back to a CSV file
combined_csv_file_path = 'data.csv'
combined_data.to_csv(combined_csv_file_path, index=False)

print(f'Combined data saved to {combined_csv_file_path}')
