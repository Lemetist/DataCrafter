import pandas as pd
import requests
import os

def download_file():
    url = 'https://docs.google.com/spreadsheets/d/1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m/export?format=xlsx'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Вызывает ошибку для статусов 4xx и 5xx

        # Сохранение файла на диск
        file_path = 'download_file.xlsx'
        with open(file_path, 'wb') as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f'Ошибка загрузки файла: {e}')

def wb_name():
    file_path = "download_file.xlsx"
    
    # Проверяем, существует ли файл перед его открытием
    if os.path.exists(file_path):
        wb = pd.ExcelFile(file_path)
        return wb.sheet_names
    else:
        print(f'Файл {file_path} не найден.')
        return None

# Пример вызова функций
if __name__ == "__main__":
    download_file()  # Сначала загрузим файл
    sheet_names = wb_name()  # Затем получим имена листов
    if sheet_names:
        print("Имена листов:", sheet_names)
