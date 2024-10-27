from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QDialog, QSlider, QLabel, QGraphicsDropShadowEffect, QFrame, QStatusBar, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QIcon
import sys
from ui import SimpleApp  # Importing the SimpleApp class from ui.py
import json
import pandas as pd
import requests
import os
import math

class MainApp(SimpleApp):  # Inherit from SimpleApp
    def __init__(self):
        super().__init__()  # Initialize the parent class
        self.download_and_process_file()  # Load file on startup

    def download_file(self):
        url = 'https://docs.google.com/spreadsheets/d/1S3kj0zo_QDERJu7O2QU1J4gMRx-K381m/export?format=xlsx'
        try:
            response = requests.get(url)
            response.raise_for_status()

            file_path = 'download_file.xlsx'
            with open(file_path, 'wb') as f:
                f.write(response.content)
            self.display_message(f'Файл сохранен как {file_path}')
        except requests.exceptions.RequestException as e:
            self.display_message(f'Ошибка загрузки файла: {e}')

    def wb_name(self):
        file_path = "download_file.xlsx"
        
        if os.path.exists(file_path):
            wb = pd.ExcelFile(file_path)
            return wb.sheet_names
        else:
            self.display_message(f'Файл {file_path} не найден.')
            return None

    def download_and_process_file(self):
        self.display_message("Начинаем скачивание файла...")
        self.download_file()  # Download the file
        sheet_names = self.wb_name()  # Get sheet names
        if sheet_names:
            self.display_message("Имена листов: " + ", ".join(sheet_names))
            result = self.filter_excel('download_file.xlsx')
            self.display_message(f"Результат фильтрации: {result}")

            # Save result to JSON file
            with open('result.json', 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            self.display_message("Результат сохранен в result.json")

    def filter_excel_group(self, file_path, sheet_name='ОСНОВНОЕ'):
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=3, nrows=36)
        subject1 = 'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.'
        subject2 = 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
        group_result = {}
        for column in df.columns:
            if subject1 in df[column].values or subject2 in df[column].values:
                group_name = df[column].to_list()[0]
                group_result[group_name] = df[column].to_list()[1:]
        return group_result

    def filter_excel(self, file_path, sheet_name='ОСНОВНОЕ'):
        df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl', skiprows=5, nrows=36)
        subject1 = 'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.'
        subject2 = 'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
        flag = 0
        result = {}

        group_data = self.filter_excel_group(file_path, sheet_name)

        for column in df.columns:
            if subject1 in df[column].values or subject2 in df[column].values:
                sclud_list = df[column].to_list()[1:]
                split_sclud_list = self.split_list(sclud_list)

                if flag < len(group_data):
                    group_name = list(group_data.keys())[flag]
                    result[group_name] = split_sclud_list
                    flag += 1
        return result

    def split_list(self, input_list, chunk_size=6):
        chunks = [input_list[i: i + chunk_size] for i in range(0, len(input_list), chunk_size)]
        return {i + 1: {j + 1: chunks[i][j] for j in range(len(chunks[i]))} for i in range(len(chunks))}

    def filter_subjects(self, data, subjects):  # Added filter_subjects method
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

    def handle_button_click(self, text):
        super().handle_button_click(text)  # Call the parent class method
        if text == 'Добавить':
            self.load_filtered_data()

    def load_filtered_data(self):
        try:
            with open('result.json', 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            self.display_message("Файл result.json не найден.")
            return
        except json.JSONDecodeError:
            self.display_message("Ошибка при чтении файла result.json.")
            return

        subjects = [
            'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.',
            'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
        ]

        filtered_subjects = self.filter_subjects(data, subjects)

        # Save filtered subjects to filter_subjects.json
        with open('filter_subjects.json', 'w', encoding='utf-8') as json_file:
            json.dump(filtered_subjects, json_file, ensure_ascii=False, indent=4)

        self.text_output.clear()
        day_mapping = {
            "1": "Понедельник",
            "2": "Вторник",
            "3": "Среда",
            "4": "Четверг",
            "5": "Пятница",
            "6": "Суббота",
            "7": "Воскресенье"
        }

        formatted_output = ""
        for key, value in filtered_subjects.items():
            formatted_output += f"{key}:\n"
            for day_number, classes in value.items():
                formatted_output += f"{day_mapping[day_number]}:\n"
                for class_key, class_value in classes.items():
                    formatted_output += f"  {class_key}. {class_value}\n"
                formatted_output += "\n"

            formatted_output += "\n"

        self.text_output.append(formatted_output.strip())
        self.status_bar.showMessage("Фильтрованные данные добавлены в текстовое поле и сохранены в filter_subjects.json.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()  # Create an instance of MainApp
    window.show()
    sys.exit(app.exec_())
