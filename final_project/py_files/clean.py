import os
import zipfile
import pandas as pd

# Unzip folders
def unzip(zip_folder_path):
    for file in os.listdir(zip_folder_path):
        file_path = os.path.join(zip_folder_path, file)

        if zipfile.is_zipfile(file_path):
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                zip_ref.extractall(zip_folder_path)

# Rename the files
def rename(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        new_file_path = file_path.replace('_en', '')
        os.rename(file_path, new_file_path)

# Delete extra characters
def clean_extra(folder_path):
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                data = file.readlines()
            
            clean_data = []

            for line in data:
                line = line.replace(';e', '')
                line = line.replace(';;', ';')

                if line.endswith(';'):
                    line = line[:-1]

                if line.startswith(';'):
                    line = line[1:]

                clean_data.append(line)
            
            # Write the cleaned content back to the file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(clean_data)

# Clean previous years


def since_2020(file_path, headers):

    # Define the extra columns and headers
    cols = []
    for word in headers:
        cols.append(word)

    for i in range(2000, 2024):
        cols.append(str(i))

    # Filter the columns
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8', index_col=None)
    df = df[[col for col in df.columns if col in cols]]
    df.to_csv(file_path, index=False, sep=';')


# unzip('../raw_data')
# rename('../raw_data')
# clean_extra('../clean_data')
# since_2020('../clean_data/12612-0003.csv', ['Country'])
since_2020('../clean_data/12612-0008.csv', ['Age of the mother'])



