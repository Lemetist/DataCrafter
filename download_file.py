import requests

def download_file():
    url =f'https://docs.google.com/spreadsheets/d/1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m/export?format=xlsx'
    response = requests.get(url)
    if response.status_code == 200:
        # Сохранение файла на диск
        file_path = f'download_file.xlsx'
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f'Файл сохранен как {file_path}')
    else:
        print(f'Ошибка загрузки файла: {response.status_code}')