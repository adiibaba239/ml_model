import csv
import random
from transformers import pipeline

# Load the LLM pipeline for text generation (you can replace this with any preferred model)
generator = pipeline("text-generation", model="gpt2")  # Replace 'gpt2' with your preferred open-source LLM

def read_csv(file_path):
    """Reads a CSV file and returns its content as a list of dictionaries."""
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader), reader.fieldnames

def augment_text(value, column_name):
    """Generates a high-quality variation for a given text value using LLM."""
    prompt = f"Generate a realistic and high-quality variation for the following {column_name}: {value}"
    generated = generator(prompt, max_length=500, num_return_sequences=10)[0]['generated_text']
    return generated.replace(prompt, '').strip()  # Clean up the generated text

def augment_data(row, fieldnames, num_variations=5):
    """Generates synthetic variations for a given row using an LLM."""
    augmented_rows = []

    for _ in range(num_variations):
        augmented_row = {}
        for column in fieldnames:
            value = row[column]
            augmented_row[column] = augment_text(value, column)
        augmented_rows.append(augmented_row)

    return augmented_rows

def write_csv(file_path, data, fieldnames):
    """Writes data to a CSV file."""
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def generate_dataset(input_csv, output_csv, num_variations=100, augment_columns=None):
    """Generates a large dataset from an input CSV."""
    data, fieldnames = read_csv(input_csv)

    if augment_columns:
        # Ensure only specified columns are augmented
        fieldnames = [col for col in fieldnames if col in augment_columns]

    augmented_data = []
    for row in data:
        augmented_data.extend(augment_data(row, fieldnames, num_variations=num_variations))

    write_csv(output_csv, augmented_data, fieldnames)

if __name__ == "__main__":
    # Input CSV file path (replace with your file path)
    input_csv = "input_data.csv"

    # Output CSV file path (where augmented data will be stored)
    output_csv = "augmented_data.csv"

    # Number of variations per row in the input CSV
    num_variations = 10

    # Specify columns to augment (if None, all columns will be augmented)
    augment_columns = None  # Example: ['Column1', 'Column2']

    # Generate the dataset
    generate_dataset(input_csv, output_csv, num_variations=num_variations, augment_columns=augment_columns)

    print(f"Augmented dataset generated and saved to {output_csv}")
