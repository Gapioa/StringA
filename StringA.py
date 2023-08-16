import os

folder_path = r"folder_path" #When changing, be sure to leave 'r', if it doesn't work just remove it

def replace_in_file(file_path, search_string, replace_string):
    try:
        with open (file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if search_string in content:
            updated_content = content.replace(search_string, replace_string)

            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(updated_content)
            print(f"Replacement complete '{file_path}'.")
        else:
            print(f"String '{search_string}' not found '{file_path}'.")
    except Exception as e:
        print(f"An error occurred while handling the file '{file_path}' : {e}")

search_string = "test" #What are you looking for
replace_string = "something" #What you want to replace it with

for filename in os.listdir(folder_path):
    if filename.endswith(".txt"): # Change the extension
        file_path = os.path.join(folder_path, filename)
        try:
            replace_in_file(file_path, search_string, replace_string)
            print(f"Replacement complete '{file_path}'.")
        except Exception as e:
            print(f"An error occured while handling the file '{file_path}' : {e}")
