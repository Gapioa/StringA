import os
import openpyxl
import re
from difflib import SequenceMatcher

# Set folder path where the script is running
folder_path = os.path.dirname(os.path.abspath(__file__))

# Define actual filenames here
excel_filename = 'your_excel_file.xlsx'  # <-- Replace this
text_filename = 'your_text_file.txt'     # <-- Replace this
output_filename = 'missing.txt'

# Full paths
excel_file = os.path.join(folder_path, excel_filename)
text_file = os.path.join(folder_path, text_filename)
output_file = os.path.join(folder_path, output_filename)

# --- Sanity Checks ---
print(f"📄 Excel file: {excel_file}")
print(f"📄 Text file: {text_file}")
if not os.path.exists(excel_file):
    print("❌ Excel file not found!")
    exit(1)
if not os.path.exists(text_file):
    print("❌ Text file not found!")
    exit(1)

# --- Load Excel Data ---
print("🔄 Reading Excel...")
wb = openpyxl.load_workbook(excel_file, read_only=True)
sheet = wb.active
excel_values = set(str(cell.value).strip().lower() for cell in sheet['A'] if cell.value)
print(f"✅ Excel items loaded: {len(excel_values)}")

# --- Extract double-asterisk names from text file ---
print("🔍 Extracting names from text file...")
with open(text_file, 'r', encoding='utf-8') as f:
    text_content = f.read()

pattern = re.compile(r"\*\*(.*?)\*\*")
text_names = [match.lower().strip() for match in pattern.findall(text_content)]
print(f"✅ Found {len(text_names)} names in text.")

# --- Compare using fuzzy matching ---
SIMILARITY_THRESHOLD = 0.7

def is_similar(name, excel_set):
    for excel_name in excel_set:
        if SequenceMatcher(None, name, excel_name).ratio() >= SIMILARITY_THRESHOLD:
            return True
    return False

print("🔁 Comparing for missing items...")
missing = sorted(name for name in text_names if not is_similar(name, excel_values))

# --- Write results ---
if not missing:
    print("✅ All items matched! Nothing is missing.")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Nothing is missing. All items are present.\n")
else:
    print(f"🚨 Missing items found: {len(missing)}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in missing:
            f.write(item + '\n')
    print(f"✅ Missing items written to {output_file}")
