import pandas as pd
import json
import math


def split_list(input_list, chunk_size=6):
    chunks = [input_list[i:i + chunk_size] for i in range(0, len(input_list), chunk_size)]
    chunks = {i + 1: {j + 1: chunks[i][j] for j in range(len(chunks[i]))} for i in range(min(len(chunks), math.ceil(len(input_list) / chunk_size)))}

    # Записываем в txt файл построчно
    with open('split_sclud_list.txt', 'w', encoding='utf-8') as file:
        file.write(f"{chunks}\n")

    return chunks

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
    # Загружаем данные из Excel
    df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=5, nrows=36)

    # Искомые предметы
    subject1 = 'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.'
    subject2 = 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
    flag = 0
    # Словарь для результата
    result = {}

    # Получаем информацию о группах
    group_data = filter_excel_group(file_path, sheet_name)

    # Проходим по каждому столбцу в df
    for column in df.columns:
        if subject1 in df[column].values or subject2 in df[column].values:

            # Извлекаем список значений из столбца (начиная со второго элемента)
            sclud_list = df[column].to_list()[1:]

            # Разбиваем список на части
            split_sclud_list = split_list(sclud_list)

            # Обновляем результат для текущего столбца
            if flag < len(group_data) :
                group_name = list(group_data.keys())[flag]
                result[group_name] = split_sclud_list
                flag += 1
    return result

def filter_subjects(data, subjects):
    filtered_data = {}
    for column, rows in data.items():
        for row, cells in rows.items():
            for cell, value in cells.items():
                if value in subjects:
                    if column not in filtered_data:
                        filtered_data[column] = {}
                    if row not in filtered_data[column]:
                        filtered_data[column][row] = {}
                    filtered_data[column][row][cell] = value
    return filtered_data

result = filter_excel('download_file.xlsx')
print(result)
print(filter_subjects(result, ['МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.', 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.']))

# Сохранение результата в JSON файл
with open('result.json', 'w', encoding='utf-8') as json_file:
    json.dump(result, json_file, ensure_ascii=False, indent=4)

