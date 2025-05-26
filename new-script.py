import os
import openpyxl
import re
from difflib import SequenceMatcher

# Set folder path where both files are located
folder_path = os.path.dirname(os.path.abspath(__file__))

# Define file names (change these to your actual file names)
excel_file = os.path.join(folder_path, 'your_excel_file.xlsx')  # <-- Change filename
text_file = os.path.join(folder_path, 'your_text_file.txt')     # <-- Change filename
output_file = os.path.join(folder_path, 'missing.txt')

# Load data from Column A in the Excel file (to lowercase)
wb = openpyxl.load_workbook(excel_file, read_only=True)
sheet = wb.active
excel_values = set(str(cell.value).strip().lower() for cell in sheet['A'] if cell.value)

# Extract only names between **double asterisks** from the text file
with open(text_file, 'r', encoding='utf-8') as f:
    text_content = f.read()

# Find all **name** patterns using regex
pattern = re.compile(r"\*\*(.*?)\*\*")
text_names = [match.lower().strip() for match in pattern.findall(text_content)]

# Define similarity threshold (0.7 = 70% similarity)
SIMILARITY_THRESHOLD = 0.7

# Helper function to check for fuzzy match
def is_similar(name, excel_set):
    for excel_name in excel_set:
        ratio = SequenceMatcher(None, name, excel_name).ratio()
        if ratio >= SIMILARITY_THRESHOLD:
            return True
    return False

# Determine which names are missing (not similar to any Excel entry)
missing = sorted(name for name in text_names if not is_similar(name, excel_values))

# Write the missing names to output file
with open(output_file, 'w', encoding='utf-8') as f:
    for item in missing:
        f.write(item + '\n')

print(f"Done! Missing values written to {output_file}")
