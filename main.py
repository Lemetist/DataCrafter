from PyQt5.QtWidgets import QApplication
import sys
from ui import SimpleApp  # Importing the SimpleApp class from ui.py
import json
import os
from filter_excel import wb_name, split_list, filter_excel_group, filter_excel, filter_subjects,format_day # Import functions from filter_excel.py
from download_file import download_file


class MainApp(SimpleApp):  # Inherit from SimpleApp
    def __init__(self):
        super().__init__()  # Initialize the parent class
        self.download_and_process_file()  # Load file on startup

    def download_and_process_file(self):
        self.display_message("Начинаем скачивание файла...")
        download_file()  # Download the file
        sheet_names = wb_name()  # Get sheet names
        if sheet_names:
            result = filter_excel('download_file.xlsx')
            # Save result to JSON file
            with open('result.json', 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            self.display_message("Результат сохранен в result.json")

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

        filtered_subjects = filter_subjects(data, subjects)

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

        formatted_output = format_day(filtered_subjects, day_mapping)
        self.text_output.append(formatted_output)
        self.status_bar.showMessage("Фильтрованные данные добавлены в текстовое поле и сохранены в filter_subjects.json.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()  # Create an instance of MainApp
    window.show()
    sys.exit(app.exec_())