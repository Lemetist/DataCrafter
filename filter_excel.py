import pandas as pd
import json

def split_list(input_list, chunk_size=6):
    chunks = [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
    return {i + 1: {j + 1: chunks[i][j] for j in range(len(chunks[i]))} for i in range(min(len(chunks), 6))}

def filter_excel(file_path, sheet_name='28.10-02.11 нечетная неделя'):
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=5, nrows=36)
    subject1 = 'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.'
    subject2 = 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
    result = []
    for column in df.columns:
        if subject1 in df[column].values or subject2 in df[column].values:
            sclud_list = df[column].to_list()
            sclud_list = sclud_list[1:]
            split_sclud_list = split_list(sclud_list)
            result.append(split_sclud_list)
    return result

result = filter_excel('download_file.xlsx')
print(result)
# Save the result to a JSON file
with open('result.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

print("JSON file has been created.")