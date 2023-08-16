import os

folder_path = r"C:\Users\kalma\Desktop\test" #Kad menjas obavezno ostavi 'r', ako ne radi samo ukloni

def replace_in_file(file_path, search_string, replace_string):
    try:
        with open (file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if search_string in content:
            updated_content = content.replace(search_string, replace_string)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Zamena završena za datoteku '{file_path}'.")
        else:
            print(f"String '{search_string}' nije pronađen u datoteci '{file_path}'.")
    except Exception as e:
        print(f"Greška prilikom rukovanja datotekom '{file_path}' : {e}")

search_string = "proba"
replace_string = "podatak"

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"): # Možeš ovde promeniti ekstenziju
        file_path = os.path.join(folder_path, filename)
        try:
            replace_in_file(file_path, search_string, replace_string)
            print(f"Zamena završena za datoteku '{file_path}'.")
        except Exception as e:
            print(f"Greška prilikom zamene za datoteku '{file_path}' : {e}")
