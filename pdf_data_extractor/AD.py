r"""import pandas as pd

def truncate_text(text, max_words=5000):
    words = str(text).split()
    return " ".join(words[:max_words]) if len(words) > max_words else text

file_path = r"D:\ML_WORK\DATA_GENERATOR\pdf_data_extractor\formatted_text.csv"  # Replace with your actual file path
df = pd.read_csv(file_path)

# Print column names for debugging
print("Available columns:", df.columns.tolist())

# Dynamically process only text columns if available
for column in df.columns:
    df[column] = df[column].apply(truncate_text)

output_path = "shortened_file.csv"
df.to_csv(output_path, index=False)

print(f"Processed file saved as {output_path}")"""
import pandas as pd

def truncate_text(text, max_chars=5000):
    text = str(text)  # Ensure text is a string
    return text[:max_chars] if len(text) > max_chars else text

file_path = r"D:\ML_WORK\DATA_GENERATOR\pdf_data_extractor\formatted_text.csv" # Replace with your actual file path
df = pd.read_csv(file_path)

# Print column names for debugging
print("Available columns:", df.columns.tolist())

# Dynamically truncate text in all columns if needed
for column in df.columns:
    if df[column].dtype == object:  # Apply only to text columns
        df[column] = df[column].apply(truncate_text)

output_path = "shortened_file.csv"
df.to_csv(output_path, index=False)

print(f"Processed file saved as {output_path}")

