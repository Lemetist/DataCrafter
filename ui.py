from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QApplication, QHBoxLayout, QDialog, QSlider, QLabel, QGraphicsDropShadowEffect, QFrame, QStatusBar, QColorDialog
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QIcon, QColor
import sys
from datetime import datetime
import locale
import json

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        try:
            locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
        except locale.Error:
            pass  # Если локаль не установлена, используем локаль по умолчанию
        self.light_theme = True 
        self.font_size = 14 
        self.font_color = QColor(255, 255, 255)  # Цвет текста по умолчанию белый 
        self.load_settings()  # Загрузка настроек 
        self.initUI()  # Инициализация интерфейса 

    def initUI(self):
        self.setWindowTitle('SusMan -- Neon_Leonov')
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

        # Инициализация рамки для кнопок 
        self.button_frame = QFrame(self)
        self.button_frame.setStyleSheet("QFrame { border: 2px solid #A77BCA; border-radius: 10px; padding: 10px; }")

        button_layout = QHBoxLayout(self.button_frame)

        button_style = "QPushButton {border: none; border-radius: 10px; padding: 10px; font-size: 14px; background-color: #A77BCA; color: white;} " \
                       "QPushButton:hover {background-color: #9B5B9B;}"

        button_data = [
            ('Добавить', 'plus.png'),
            ('Удалить', 'minus.png'),
            ('Настройки', 'settings.png'),
            ('Очистить', 'clear.png'),
        ]  # Убрали кнопку "Цвет текста" из основного меню 

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

        # Статусная строка 
        self.status_bar = QStatusBar(self)
        layout.addWidget(self.status_bar)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)
        self.update_date()

        self.set_theme()  # Применяем тему после инициализации интерфейса 
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
        else:
            self.display_message(f"Вы нажали кнопку: {text}")

    def display_message(self, message):
        self.text_output.append(message)

    def toggle_theme(self):
        self.light_theme = not self.light_theme 
        self.set_theme()

    def set_theme(self):
        if self.light_theme: # вынести в стили
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

        # Обновляем стиль текстового поля с новым размером шрифта и цветом текста 
        self.text_output.setStyleSheet(f"border: 1px solid #BBBBBB; padding: 10px; font-size: {self.font_size}px; color: {self.font_color.name()};")

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

        color_button = QPushButton("Выбрать цвет текста", self)
        color_button.setStyleSheet("QPushButton {border: none; border-radius: 10px; padding: 10px; font-size: 14px; background-color: #A77BCA; color: white;} " \
                                   "QPushButton:hover {background-color: #9B5B9B;}")
        color_button.clicked.connect(self.select_text_color)
        layout.addWidget(color_button)

        theme_button = QPushButton("Переключить тему", self)
        theme_button.setStyleSheet("QPushButton {border: none; border-radius: 10px; padding: 10px; font-size: 14px; background-color: #A77BCA; color: white;} " \
                                   "QPushButton:hover {background-color: #9B5B9B;}")
        theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def update_font_size(self, value):
        self.font_size = value 
        self.font_size_label.setText(f"Размер шрифта: {self.font_size}px")
        self.set_theme()  # Обновляем тему, чтобы применить новый размер шрифта 
        self.save_settings()  # Сохраняем настройки при изменении 

    def select_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color
            self.set_theme()  # Обновляем цвет текста 
            self.save_settings()  # Сохраняем настройки при изменении 
    def save_settings(self):
        settings = {
            'light_theme': self.light_theme,
            'font_size': self.font_size,
            'font_color': self.font_color.name()  # Сохраняем цвет текста в формате HEX
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.light_theme = settings.get('light_theme', True)
                self.font_size = settings.get('font_size', 14)
                self.font_color = QColor(settings.get('font_color', '#FFFFFF'))  # Загружаем цвет текста 
        except FileNotFoundError:
            pass  # Файл настроек не найден, используем значения по умолчанию

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())