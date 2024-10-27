from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QApplication, QHBoxLayout, QDialog, QSlider, QLabel, QGraphicsDropShadowEffect, QFrame, QStatusBar
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QIcon
import sys
from datetime import datetime
import locale
import json
import pandas as pd
import requests
import os
import math

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_TIME, 'Russian_Russia.1251')
        self.light_theme = True 
        self.font_size = 14 
        self.load_settings()  
        self.initUI()  

        # Загрузка файла при запуске приложения
        self.download_and_process_file()

    def initUI(self):
        self.setWindowTitle('SusMan -- Lemetist')
        self.resize(400, 300)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.date_label = QLabel(self)
        self.date_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(self.date_label)

        self.text_output = QTextEdit(self)
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        self.button_frame = QFrame(self)
        self.button_frame.setStyleSheet("QFrame { border: 2px solid #A77BCA; border-radius: 10px; padding: 10px; }")

        button_layout = QHBoxLayout(self.button_frame)

        button_style = "QPushButton {border: none; border-radius: 10px; padding: 10px; font-size: 14px; background-color: #A77BCA; color: white;} " \
                       "QPushButton:hover {background-color: #9B5B9B;}"

        button_data = [
            ('Добавить', 'plus.png'),
            ('Удалить', 'minus.png'),
            ('Настройки', 'settings.png'),
            ('Очистить', 'clear.png')
        ]

        for text, icon in button_data:
            button = QPushButton(text, self)
            button.setStyleSheet(button_style)
            button.setIcon(QIcon(icon))
            button.clicked.connect(lambda _, t=text: self.handle_button_click(t))
            button_layout.addWidget(button)

            shadow_effect = QGraphicsDropShadowEffect()
            shadow_effect.setBlurRadius(10)
            shadow_effect.setXOffset(5)
            shadow_effect.setYOffset(5)
            shadow_effect.setColor(Qt.black)
            button.setGraphicsEffect(shadow_effect)

            self.add_button_animation(button)

        layout.addWidget(self.button_frame)

        self.status_bar = QStatusBar(self)
        layout.addWidget(self.status_bar)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)
        self.update_date()

        self.set_theme()  

        self.setLayout(layout)

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
        self.download_file()  # Скачиваем файл
        sheet_names = self.wb_name()  # Получаем имена листов
        if sheet_names:
            self.display_message("Имена листов: " + ", ".join(sheet_names))
            result = self.filter_excel('download_file.xlsx')
            self.display_message(f"Результат фильтрации: {result}")

            # Сохранение результата в JSON файл
            with open('result.json', 'w', encoding='utf-8') as json_file:
                json.dump(result, json_file, ensure_ascii=False, indent=4)
            self.display_message("Результат сохранен в result.json")

    def split_list(self, input_list, chunk_size=6):
        chunks = [input_list[i: i + chunk_size] for i in range(0, len(input_list), chunk_size)]
        chunks = {i + 1: {j + 1: chunks[i][j] for j in range(len(chunks[i]))} for i in range(min(len(chunks), math.ceil(len(input_list) / chunk_size)))}

        with open('split_sclud_list.txt', 'w', encoding='utf-8') as file:
            file.write(f"{chunks}\n")

        return chunks

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

    def filter_subjects(self, data, subjects):
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

    def add_button_animation(self, button):
        animation = QPropertyAnimation(button, b"geometry")
        original_geometry = button.geometry()
        animation.setDuration(300)
        animation.setStartValue(QRect(original_geometry.x(), original_geometry.y() - 50, original_geometry.width(), original_geometry.height()))
        animation.setEndValue(original_geometry)
        animation.start()

    def handle_button_click(self, text):
        if text == 'Очистить':
            self.text_output.clear()
            self.status_bar.showMessage("Текст очищен.")
        elif text == 'Настройки':
            self.open_settings_dialog()
        elif text == 'Добавить':
            # Load data from result.json
            try:
                with open('result.json', 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
            except FileNotFoundError:
                self.display_message("Файл result.json не найден.")
                return
            except json.JSONDecodeError:
                self.display_message("Ошибка при чтении файла result.json.")
                return

            # Define subjects for filtering
            subjects = [
                'МДК.07.01 Управление и автоматизация баз данных\nДавыдова Л.Б.',
                'МДК.11.01 Технология разработки и защиты баз данных\nДавыдова Л.Б.'
            ]

            # Filter the subjects
            filtered_subjects = self.filter_subjects(data, subjects)

            # Save filtered subjects to filter_subjects.json
            with open('filter_subjects.json', 'w', encoding='utf-8') as json_file:
                json.dump(filtered_subjects, json_file, ensure_ascii=False, indent=4)

            # Clear the text output before displaying
            self.text_output.clear()

            # Mapping of numbers to days
            day_mapping = {
                "1": "Понедельник",
                "2": "Вторник",
                "3": "Среда",
                "4": "Четверг",
                "5": "Пятница",
                "6": "Суббота",
                "7": "Воскресенье"
            }

            # Display the filtered subjects with modified values
            for key, value in filtered_subjects.items():
                formatted_output = f"{key}:\n"  # Изменено: добавлен перевод строки
                for day_number, classes in value.items():
                    # Проверяем, является ли classes строкой, если да, то преобразуем
                    if isinstance(classes, str):
                        try:
                            classes_dict = eval(classes)  # Преобразуем строку в словарь
                        except Exception as e:
                            self.display_message(f"Ошибка при обработке классов: {e}")
                            continue
                    elif isinstance(classes, dict):
                        classes_dict = classes  # Если это уже словарь, просто присваиваем

                    # Добавляем день недели в вывод без номера
                    formatted_output += f"{day_mapping[day_number]}:\n"  # Название дня

                    # Добавляем номера классов перед классами
                    for class_key, class_value in classes_dict.items():
                        formatted_output += f"  {class_key}. {class_value}\n"  # Номер класса и класс
                    formatted_output += "\n"  # Добавляем пустую строку после каждого дня для разделения

                self.text_output.append(formatted_output.strip())  # Убираем лишний пробел в конце

            self.status_bar.showMessage("Фильтрованные данные добавлены в текстовое поле и сохранены в filter_subjects.json.")
        else:
            self.display_message(f"Вы нажали кнопку: {text}")

















    def display_message(self, message):
        self.text_output.append(message)

    def toggle_theme(self):
        self.light_theme = not self.light_theme 
        self.set_theme()

    def set_theme(self):
        if self.light_theme:
            self.setStyleSheet("""
            QWidget {
                background-color: #172129;
                color: #FFFFFF;
                font-family: 'Arial';
                font-size: 14px;
            }
            QTextEdit {
                background-color: #1E2A36;
                border: 1px solid #BBBBBB;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            """)
        else:
            self.setStyleSheet("""
            QWidget {
                background-color: #2E2E2E;
                color: white;
                font-family: 'Arial';
                font-size: 14px;
            }
            QTextEdit {
                background-color: #3C3C3C;
                border: 1px solid #555;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            """)

        self.text_output.setStyleSheet(f"border: 1px solid #BBBBBB; padding: 10px; font-size: {self.font_size}px;")

    def update_date(self):
        now = datetime.now()
        self.date_label.setText(now.strftime("%d, %B, %A"))

    def open_settings_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Настройки")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout()

        self.font_size_label = QLabel(f"Размер шрифта: {self.font_size}px", self)
        layout.addWidget(self.font_size_label)

        self.font_size_slider = QSlider(Qt.Horizontal, self)
        self.font_size_slider.setMinimum(8)
        self.font_size_slider.setMaximum(30)
        self.font_size_slider.setValue(self.font_size)
        self.font_size_slider.valueChanged.connect(self.update_font_size)
        layout.addWidget(self.font_size_slider)

        theme_button = QPushButton("Переключить тему", self)
        theme_button.setStyleSheet("QPushButton {border: none; border-radius: 5px; padding: 10px; font-size: 14px; background-color: #A77BCA; color: white;} " \
                                   "QPushButton:hover {background-color: #9B5B9B;}")
        theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def update_font_size(self, value):
        self.font_size = value 
        self.font_size_label.setText(f"Размер шрифта: {self.font_size}px")
        self.set_theme()  
        self.text_output.setStyleSheet(f"border: 1px solid #BBBBBB; padding: 10px; font-size: {self.font_size}px;")
        self.save_settings()  

    def save_settings(self):
        settings = {
            'light_theme': self.light_theme,
            'font_size': self.font_size,
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.light_theme = settings.get('light_theme', True)
                self.font_size = settings.get('font_size', 14)
        except FileNotFoundError:
            pass  

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())
