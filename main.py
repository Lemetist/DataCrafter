from PyQt5.QtWidgets import QApplication
import sys
from ui import SimpleApp  # Импортируем класс SimpleApp из ui.py
import json
import os
from filter_excel import wb_name, split_list, filter_excel_group, filter_excel, filter_subjects, format_day  # Импортируем функции из filter_excel.py
from download_file import download_file


class MainApp(SimpleApp):  # Наследуемся от SimpleApp
    def __init__(self):
        super().__init__()  # Инициализируем родительский класс
        self.name_sheet = "ОСНОВНОЕ"
        self.download_and_process_file()  # Загружаем файл при запуске

    def download_and_process_file(self):
        self.display_message("Начинаем скачивание файла...")
        download_file()  # Скачиваем файл
        sheet_names = wb_name()
        if sheet_names:
            result = filter_excel('download_file.xlsx', self.name_sheet)
            # Сохраняем результат в JSON файл
            with open('result.json', 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            self.display_message("Результат сохранен в result.json")

    def on_day_selected(self, index):
        selected_day = self.combo_box.itemText(index)
        self.display_message(f"Расписание : {selected_day}")
        self.name_sheet = selected_day
        self.download_and_process_file()

    def handle_button_click(self, text):
        super().handle_button_click(text)  # Вызываем метод родительского класса
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
            'МДК.11.01 КП Технология разработки и защиты баз данных\nДавыдова Л.Б.',
            'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.\n\n',
            'МДК.11.01 КП Технология разработки и защиты баз данных Давыдова Л.Б.',
        ]

        filtered_subjects = filter_subjects(data, subjects)

        # Сохраняем отфильтрованные предметы в filter_subjects.json
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
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
