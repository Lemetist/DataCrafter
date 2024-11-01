# ui.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QApplication, QHBoxLayout, QDialog, QSlider, \
    QLabel, QGraphicsDropShadowEffect, QFrame, QStatusBar, QColorDialog, QComboBox
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QTimer
from PyQt5.QtGui import QIcon, QColor
import sys
import os
from datetime import datetime
import locale
import json

try:
    from filter_excel import wb_name
except ImportError:
    def wb_name():
        return ["Понедельник", "Вторник", "Среда"]  # Моковые данные на случай отсутствия импорта

class SimpleApp(QWidget):
    def __init__(self):
        super().__init__()
        locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8') if locale.getlocale() else None
        self.light_theme = True
        self.font_size = 14
        self.font_color = QColor(255, 255, 255)
        self.load_settings()
        self.initUI()
        self.load_days()

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
        button_style = """
            QPushButton { border: none; border-radius: 10px; padding: 10px; font-size: 14px; background-color: #A77BCA; color: white; }
            QPushButton:hover { background-color: #9B5B9B; }
        """

        button_data = [
            ('Добавить', 'plus.png'),
            ('Удалить', 'minus.png'),
            ('Настройки', 'settings.png'),
            ('Очистить', 'clear.png'),
        ]

        for text, icon in button_data:
            button = QPushButton(text, self)
            button.setStyleSheet(button_style)
            if os.path.exists(icon):
                button.setIcon(QIcon(icon))
            button.clicked.connect(lambda _, t=text: self.handle_button_click(t))
            button_layout.addWidget(button)
            self.add_button_animation(button)

        layout.addWidget(self.button_frame)

        # Статусная строка
        self.status_bar = QStatusBar(self)
        layout.addWidget(self.status_bar)

        # ComboBox для дней недели
        self.combo_box = QComboBox(self)
        self.combo_box.currentIndexChanged.connect(self.on_day_selected)
        h_layout = QHBoxLayout()
        h_layout.addStretch(1)
        h_layout.addWidget(self.combo_box)
        h_layout.addStretch(1)
        layout.addLayout(h_layout)

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_date)
        self.timer.start(1000)
        self.update_date()

        self.set_theme()

    def add_button_animation(self, button):
        animation = QPropertyAnimation(button, b"geometry", button)
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
        self.save_settings()

    def load_days(self):
        days = wb_name()  # Получаем список дней из функции wb_name
        self.combo_box.addItems(days)

    def set_theme(self):
        theme_styles = """
            QWidget {
                background-color: %s;
                color: %s;
                font-family: 'Arial';
                font-size: %dpx;
            }
            QTextEdit {
                background-color: %s;
                border: 1px solid #BBBBBB;
                border-radius: 5px;
                padding: 10px;
                color: %s;
            }
        """ % (
            "#172129" if self.light_theme else "#2E2E2E",
            "#FFFFFF",
            self.font_size,
            "#1E2A36" if self.light_theme else "#3C3C3C",
            self.font_color.name()
        )
        self.setStyleSheet(theme_styles)

    def update_date(self):
        now = datetime.now()
        self.date_label.setText(now.strftime("%d, %B, %A"))

    def open_settings_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Настройки")
        dialog.setFixedSize(300, 200)

        layout = QVBoxLayout(dialog)

        self.font_size_label = QLabel(f"Размер шрифта: {self.font_size}px", self)
        layout.addWidget(self.font_size_label)

        self.font_size_slider = QSlider(Qt.Horizontal, self)
        self.font_size_slider.setRange(8, 30)
        self.font_size_slider.setValue(self.font_size)
        self.font_size_slider.valueChanged.connect(self.update_font_size)
        layout.addWidget(self.font_size_slider)

        color_button = QPushButton("Выбрать цвет текста", self)
        color_button.clicked.connect(self.select_text_color)
        layout.addWidget(color_button)

        theme_button = QPushButton("Переключить тему", self)
        theme_button.clicked.connect(self.toggle_theme)
        layout.addWidget(theme_button)

        dialog.setLayout(layout)
        dialog.exec_()

    def update_font_size(self, value):
        self.font_size = value
        self.font_size_label.setText(f"Размер шрифта: {self.font_size}px")
        self.set_theme()
        self.save_settings()

    def select_text_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color
            self.set_theme()
            self.save_settings()

    def save_settings(self):
        settings = {
            'light_theme': self.light_theme,
            'font_size': self.font_size,
            'font_color': self.font_color.name()
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)

    def load_settings(self):
        try:
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.light_theme = settings.get('light_theme', True)
                self.font_size = settings.get('font_size', 14)
                self.font_color = QColor(settings.get('font_color', '#FFFFFF'))
        except FileNotFoundError:
            pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SimpleApp()
    window.show()
    sys.exit(app.exec_())