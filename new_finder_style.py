import sys
import csv
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QPushButton, QTextEdit, QLabel, QMessageBox,
    QGroupBox, QSizePolicy
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QPixmap

FAV_FILE = "favorites.json"
HIST_FILE = "history.json"

def load_data():
    items = []
    try:
        with open('items.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                items.append(row)
    except FileNotFoundError:
        pass
    return items

def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class ItemFinder(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Item Finder mit PyQt6")
        self.resize(900, 600)

        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("Hintergrund.png")
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()

        self.items = load_data()
        self.favorites = load_json(FAV_FILE)
        self.history = load_json(HIST_FILE)

        self.title_font = QFont("Arial", 12, QFont.Weight.Bold)
        self.label_font = QFont("Arial", 10, QFont.Weight.Bold)
        self.normal_font = QFont("Arial", 10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Item suchen...")
        self.search_input.textChanged.connect(self.update_search_results)
        self.search_input.setFont(self.normal_font)

        self.search_results_list = QListWidget()
        self.search_results_list.itemClicked.connect(self.on_item_selected)
        self.search_results_list.setFont(self.normal_font)
        self.search_results_list.setMinimumWidth(280)
        self.search_results_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.search_results_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #888;
                padding: 5px;
                background-color: transparent;
                font-weight: bold;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #1f1f1f;
            }
            QListWidget::item:selected {
                background-color: #8c3b26;
                color: white;
            }
        """)

        self.favorites_list = QListWidget()
        self.favorites_list.itemClicked.connect(self.on_favorite_selected)
        self.favorites_list.setFont(self.normal_font)
        self.favorites_list.setMinimumWidth(250)
        self.favorites_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #888;
                padding: 5px;
                background-color: transparent;
                font-weight: bold;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #1f1f1f;
            }
            QListWidget::item:selected {
                background-color: #8c3b26;
                color: white;
            }
        """)

        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_selected)
        self.history_list.setFont(self.normal_font)
        self.history_list.setMinimumWidth(250)
        self.history_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #888;
                padding: 5px;
                background-color: transparent;
                font-weight: bold;
                color: white;
            }
            QListWidget::item:hover {
                background-color: #1f1f1f;
            }
            QListWidget::item:selected {
                background-color: #8c3b26;
                color: white;
            }
        """)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(self.normal_font)
        self.details_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #888;
                padding: 5px;
                background-color: transparent;
                font-weight: bold;
                color: white;
            }
        """)
        self.details_text.setMinimumHeight(120)

        self.add_fav_button = QPushButton("Zu Favoriten hinzufügen")
        self.add_fav_button.clicked.connect(self.add_to_favorites)
        self.add_fav_button.setFont(self.normal_font)
        self.add_fav_button.setStyleSheet("""
            QPushButton {
                background-color: #4caf50;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        self.remove_fav_button = QPushButton("Aus Favoriten entfernen")
        self.remove_fav_button.clicked.connect(self.remove_from_favorites)
        self.remove_fav_button.setFont(self.normal_font)
        self.remove_fav_button.setStyleSheet("""
            QPushButton {
                background-color: #e53935;
                color: white;
                border-radius: 5px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #c62828;
            }
        """)

        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        content_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        fav_header_layout = QHBoxLayout()

        search_label = QLabel("Suche:")
        search_label.setFont(self.label_font)
        search_label.setFixedWidth(50)
        search_label.setStyleSheet("QLabel { color: #8c3b26; }")
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        search_group = QGroupBox("Suchergebnisse")
        search_group.setFont(self.title_font)
        search_group.setLayout(QVBoxLayout())
        search_group.layout().addWidget(self.search_results_list)
        search_group.setMinimumWidth(300)
        search_group.setStyleSheet("QGroupBox { color: #8c3b26; }")

        favorites_group = QGroupBox()
        favorites_group.setFont(self.title_font)
        fav_group_layout = QVBoxLayout()
        favorites_group.setLayout(fav_group_layout)

        fav_title_label = QLabel("Favoriten")
        fav_title_label.setFont(self.title_font)
        fav_title_label.setStyleSheet("QLabel { color: #8c3b26; }")
        fav_header_layout.addWidget(fav_title_label)
        fav_header_layout.addStretch()
        fav_header_layout.addWidget(self.remove_fav_button)

        fav_group_layout.addLayout(fav_header_layout)
        fav_group_layout.addWidget(self.favorites_list)

        history_group = QGroupBox("Historie (letzte 5)")
        history_group.setFont(self.title_font)
        history_group.setStyleSheet("QGroupBox { color: #8c3b26; }")
        history_layout = QVBoxLayout()
        history_group.setLayout(history_layout)
        history_layout.addWidget(self.history_list)

        right_layout.addWidget(favorites_group, 3)
        right_layout.addWidget(history_group, 2)

        content_layout.addWidget(search_group, 3)
        content_layout.addLayout(right_layout, 2)

        details_label = QLabel("Lagerdaten:")
        details_label.setFont(self.label_font)
        details_label.setStyleSheet("QLabel { color: #8c3b26; }")

        main_layout.addLayout(search_layout)
        main_layout.addLayout(content_layout)
        main_layout.addWidget(details_label)
        main_layout.addWidget(self.details_text)
        main_layout.addWidget(self.add_fav_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)

        self.update_search_results()
        self.update_favorites_list()
        self.update_history_list()

    def resizeEvent(self, event):
        scaled_pixmap = self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.background_label.setPixmap(scaled_pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def update_search_results(self):
        term = self.search_input.text().lower()
        filtered = [item for item in self.items if term in item['item_name'].lower()]
        self.search_results_list.clear()
        for item in filtered:
            # Hier kannst du den Text in den Suchergebnissen anpassen:
            anzeige_text = f"{item['item_name']}"
            self.search_results_list.addItem(anzeige_text)

    def show_details(self, item_text):
        # Extrahiere den echten Namen (wenn du oben was hinzugefügt hast)
        item_name = item_text.split(" (")[0]  # nur der Name vor der Klammer
        item = next((it for it in self.items if it['item_name'] == item_name), None)
        if item:
            details = (
                f"Name: {item['item_name']}\n"
                f"Stockwerk: {item['stockwerk']}\n"
                f"Gang: {item['gang_nummer']}\n"
                f"Block: {item['blocknummer']}"
            )
            self.details_text.setPlainText(details)
        else:
            self.details_text.clear()

    def on_item_selected(self, item):
        name = item.text()
        self.show_details(name)
        self.add_to_history(name)

    def on_favorite_selected(self, item):
        self.show_details(item.text())

    def on_history_selected(self, item):
        self.show_details(item.text())

    def add_to_favorites(self):
        current_item = self.search_results_list.currentItem()
        if current_item:
            name = current_item.text()
            if name not in self.favorites:
                self.favorites.insert(0, name)
                self.favorites = self.favorites[:50]
                save_json(FAV_FILE, self.favorites)
                self.update_favorites_list()

    def remove_from_favorites(self):
        current_item = self.favorites_list.currentItem()
        if current_item:
            name = current_item.text()
            if name in self.favorites:
                self.favorites.remove(name)
                save_json(FAV_FILE, self.favorites)
                self.update_favorites_list()

    def update_favorites_list(self):
        self.favorites_list.clear()
        self.favorites_list.addItems(self.favorites)

    def add_to_history(self, name):
        if name in self.history:
            self.history.remove(name)
        self.history.insert(0, name)
        self.history = self.history[:5]
        save_json(HIST_FILE, self.history)
        self.update_history_list()

    def update_history_list(self):
        self.history_list.clear()
        self.history_list.addItems(self.history)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemFinder()
    window.show()
    sys.exit(app.exec())
