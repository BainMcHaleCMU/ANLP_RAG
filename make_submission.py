import os
import zipfile

# Define the directory structure
structure = {
    "johnbern/report.pdf": "report.pdf",
    "johnbern/github_url.txt": "github_url.txt",
    "johnbern/contributions.md": "contributions.md",
    "johnbern/data/test/questions.txt": "data/test/questions.txt",
    "johnbern/data/test/reference_answers.txt": "data/test/reference_answers.txt",
    "johnbern/data/train/questions.txt": "data/train/questions.txt",
    "johnbern/data/train/reference_answers.txt": "data/train/reference_answers.txt",
    "johnbern/system_outputs/system_output_1.txt": "system_outputs/system_output_1.txt",
    "johnbern/system_outputs/system_output_2.txt": "system_outputs/system_output_2.txt",
    "johnbern/system_outputs/system_output_3.txt": "system_outputs/system_output_3.txt",
    "johnbern/README.md": "README.md"
}

# Set the name of the output zip file
zip_filename = "johnbern.zip"

# Get the directory where the script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Create a zip file
with zipfile.ZipFile(zip_filename, 'w') as zipf:
    for internal_path, relative_path in structure.items():
        # Create the full path to the file
        file_path = os.path.join(base_dir, relative_path)
        
        # Only add the file if it exists (for optional files)
        if os.path.exists(file_path):
            zipf.write(file_path, arcname=internal_path)
            print(f"Added {relative_path} as {internal_path}")
        else:
            print(f"File {relative_path} not found and will not be added.")

print(f"Zip file '{zip_filename}' created successfully with the specified structure.")
