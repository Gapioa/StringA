import os
import openpyxl
import re
from difflib import SequenceMatcher

# Set folder path
folder_path = os.path.dirname(os.path.abspath(__file__))

# Set actual file names
excel_filename = 'fileHere.xlsx'  # <-- Change as needed
text_filename = 'fileHere.txt'  # <-- Change as needed
output_filename = 'missing.txt'

# Full paths
excel_file = os.path.join(folder_path, excel_filename)
text_file = os.path.join(folder_path, text_filename)
output_file = os.path.join(folder_path, output_filename)

# File checks
print(f"📄 Excel file: {excel_file}")
print(f"📄 Text file: {text_file}")
if not os.path.exists(excel_file):
    print("❌ Excel file not found!")
    exit(1)
if not os.path.exists(text_file):
    print("❌ Text file not found!")
    exit(1)

# Load Excel values (column A)
print("🔄 Reading Excel...")
wb = openpyxl.load_workbook(excel_file, read_only=True)
sheet = wb.active
excel_values = set(
    str(row[0].value).strip().lower()
    for row in sheet.iter_rows(values_only=False)
    if row[0].value
)
print(f"✅ Excel items loaded: {len(excel_values)}")

# Extract **...** from .txt
print("🔍 Extracting names from text file...")
with open(text_file, 'r', encoding='utf-8') as f:
    text_content = f.read()

pattern = re.compile(r"\*\*(.*?)\*\*")
text_names = [match.lower().strip() for match in pattern.findall(text_content)]
print(f"✅ Found {len(text_names)} names in .txt")

# Fuzzy matcher
SIMILARITY_THRESHOLD = 0.7

def is_similar(name, text_set):
    for txt in text_set:
        if SequenceMatcher(None, name, txt).ratio() >= SIMILARITY_THRESHOLD:
            return True
    return False

# Find values in Excel that aren't similar to any in .txt
print("🔁 Comparing...")
missing = sorted(name for name in excel_values if not is_similar(name, text_names))

# Output
if not missing:
    print("✅ All Excel items have matches in .txt!")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Nothing is missing. All items are present.\n")
else:
    print(f"🚨 Missing Excel items not found in .txt: {len(missing)}")
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in missing:
            f.write(item + '\n')
    print(f"✅ Missing items written to: {output_file}")
