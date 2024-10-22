import pandas as pd

def csv_to_txt(csv_file):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Iterate over each column in the DataFrame
    for column in df.columns:
        # Open a new text file named after the column
        with open(f'{column}.txt', 'w') as txt_file:
            # Write each row of the column to the text file
            for item in df[column]:
                txt_file.write(str(item) + '\n')

csv_to_txt('combined_qa_pairs.csv')