import pandas as pd

def filter_excel_file(input_file, output_file, filter_value):
    # Чтение Excel файла
    df = pd.read_excel(input_file)

    # Фильтрация строк, содержащих "Давыдова Л.Б."
    filtered_df = df[df.apply(lambda row: row.astype(str).str.contains(filter_value).any(), axis=1)]

    # Сохранение отфильтрованных данных в новый Excel файл
    filtered_df.to_excel(output_file, index=False)
    print(f'Отфильтрованный файл сохранен как {output_file}')

# Пример использования
input_file = 'download_file.xlsx'
output_file = 'filtered_file.xlsx'
filter_value = 'Давыдова Л.Б.'

filter_excel_file(input_file, output_file, filter_value)