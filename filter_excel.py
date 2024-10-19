import pandas as pd
import json

def split_list(input_list, chunk_size=6):
    chunks = [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
    return {i + 1: {j + 1: chunks[i][j] for j in range(len(chunks[i]))} for i in range(min(len(chunks), 6))}

def filter_excel_group(file_path, sheet_name='ОСНОВНОЕ'):
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=3, nrows=36)
    subject1 = 'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.'
    subject2 = 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
    group_result = {}
    for column in df.columns:
        if subject1 in df[column].values or subject2 in df[column].values:
            group_name = df[column].to_list()[0]
            group_result[group_name] = df[column].to_list()[1:]
    return group_result

def filter_excel(file_path, sheet_name='ОСНОВНОЕ'):
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=5, nrows=36)
    subject1 = 'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.'
    subject2 = 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
    result = []
    group_data = filter_excel_group(file_path, sheet_name)
    for group_name, sclud_list in group_data.items():
        split_sclud_list = split_list(sclud_list)
        result.append({group_name: split_sclud_list})
    return result

result = filter_excel('download_file.xlsx')
print(result)

# Сохранение результата в JSON файл
with open('result.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

print("JSON файл был создан.")

# Преобразование данных в удобный формат для отображения
print(result[0]['ИСП11-322АП'][1])