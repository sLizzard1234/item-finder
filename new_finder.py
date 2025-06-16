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

        # Hintergrundbild-Label anlegen
        self.background_label = QLabel(self)
        self.background_pixmap = QPixmap("Hintergrund.png")
        self.background_label.setPixmap(self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation))
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        self.background_label.lower()  # ganz nach hinten

        self.items = load_data()
        self.favorites = load_json(FAV_FILE)
        self.history = load_json(HIST_FILE)

        # Fonts
        self.title_font = QFont("Arial", 12, QFont.Weight.Bold)
        self.label_font = QFont("Arial", 10, QFont.Weight.Bold)
        self.normal_font = QFont("Arial", 10)

        # Sucheingabe
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Item suchen...")
        self.search_input.textChanged.connect(self.update_search_results)
        self.search_input.setFont(self.normal_font)

        # Suchergebnisse Liste
        self.search_results_list = QListWidget()
        self.search_results_list.itemClicked.connect(self.on_item_selected)
        self.search_results_list.setFont(self.normal_font)
        self.search_results_list.setMinimumWidth(280)
        self.search_results_list.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.search_results_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #888;
                padding: 5px;
                background-color: #f9f9f9;
            }
            QListWidget::item:hover {
                background-color: #d6eaff;
            }
            QListWidget::item:selected {
                background-color: #4285f4;
                color: white;
            }
        """)

        # Favoriten Box
        self.favorites_list = QListWidget()
        self.favorites_list.itemClicked.connect(self.on_favorite_selected)
        self.favorites_list.setFont(self.normal_font)
        self.favorites_list.setMinimumWidth(250)
        self.favorites_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #888;
                padding: 5px;
                background-color: #fff7e6;
            }
            QListWidget::item:hover {
                background-color: #ffe4b5;
            }
            QListWidget::item:selected {
                background-color: #f57c00;
                color: white;
            }
        """)

        # Historie Box
        self.history_list = QListWidget()
        self.history_list.itemClicked.connect(self.on_history_selected)
        self.history_list.setFont(self.normal_font)
        self.history_list.setMinimumWidth(250)
        self.history_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #888;
                padding: 5px;
                background-color: #e6f7ff;
            }
            QListWidget::item:hover {
                background-color: #b3e0ff;
            }
            QListWidget::item:selected {
                background-color: #007acc;
                color: white;
            }
        """)

        # Details Textfeld
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(self.normal_font)
        self.details_text.setStyleSheet("""
            QTextEdit {
                background-color: #f4f6f8;
                border: 1px solid #bbb;
                padding: 8px;
            }
        """)
        self.details_text.setMinimumHeight(120)

        # Buttons
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
        self.add_fav_button.setToolTip("Markiertes Item zu Favoriten hinzufügen")

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
        self.remove_fav_button.setToolTip("Ausgewähltes Item aus Favoriten entfernen")

        # Layouts
        main_layout = QVBoxLayout()
        search_layout = QHBoxLayout()
        content_layout = QHBoxLayout()
        right_layout = QVBoxLayout()
        fav_header_layout = QHBoxLayout()

        # Sucheingabe Layout
        search_label = QLabel("Suche:")
        search_label.setFont(self.label_font)
        search_label.setFixedWidth(50)
        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)

        # Linke Seite - Suchergebnisse in GroupBox
        search_group = QGroupBox("Suchergebnisse")
        search_group.setFont(self.title_font)
        search_group.setLayout(QVBoxLayout())
        search_group.layout().addWidget(self.search_results_list)
        search_group.setMinimumWidth(300)

        # Textfarbe der GroupBox-Überschrift auf Rot setzen
        search_group.setStyleSheet("QGroupBox { color: #8c3b26; }")

        # Rechte Seite: Favoriten + Historie
        favorites_group = QGroupBox()
        favorites_group.setFont(self.title_font)
        fav_group_layout = QVBoxLayout()
        favorites_group.setLayout(fav_group_layout)

        fav_title_label = QLabel("Favoriten")
        fav_title_label.setFont(self.title_font)
        fav_header_layout.addWidget(fav_title_label)
        fav_header_layout.addStretch()
        fav_header_layout.addWidget(self.remove_fav_button)
    
        fav_group_layout.addLayout(fav_header_layout)
        fav_group_layout.addWidget(self.favorites_list)

        history_group = QGroupBox("Historie (letzte 5)")
        history_group.setFont(self.title_font)
        history_layout = QVBoxLayout()
        history_group.setLayout(history_layout)
        history_layout.addWidget(self.history_list)

        right_layout.addWidget(favorites_group, 3)
        right_layout.addWidget(history_group, 2)

        content_layout.addWidget(search_group, 3)
        content_layout.addLayout(right_layout, 2)

        # Details und add-favorite button unten
        details_label = QLabel("Lagerdaten:")
        details_label.setFont(self.label_font)

        main_layout.addLayout(search_layout)
        main_layout.addLayout(content_layout)
        main_layout.addWidget(details_label)
        main_layout.addWidget(self.details_text)
        main_layout.addWidget(self.add_fav_button, alignment=Qt.AlignmentFlag.AlignRight)

        self.setLayout(main_layout)

        # Initiale Befüllung
        self.update_search_results()
        self.update_favorites_list()
        self.update_history_list()

    def resizeEvent(self, event):
        # Beim Fenstergrößenwechsel Hintergrund anpassen
        scaled_pixmap = self.background_pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatioByExpanding, Qt.TransformationMode.SmoothTransformation)
        self.background_label.setPixmap(scaled_pixmap)
        self.background_label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

    def update_search_results(self):
        term = self.search_input.text().lower()
        filtered = [item for item in self.items if term in item['item_name'].lower()]
        self.search_results_list.clear()
        for item in filtered:
            self.search_results_list.addItem(item['item_name'])

    def show_details(self, item_name):
        item = next((it for it in self.items if it['item_name'] == item_name), None)
        if item:
            details = (
                f"Item Name: {item['item_name']}\n"
                f"Stockwerk: {item['stockwerk']}\n"
                f"Gang Nummer: {item['gang_nummer']}\n"
                f"Blocknummer: {item['blocknummer']}"
            )
            self.details_text.setPlainText(details)
        else:
            self.details_text.clear()

    def on_item_selected(self, item):
        name = item.text()
        self.show_details(name)
        self.add_to_history(name)

    def on_favorite_selected(self, item):
        name = item.text()
        self.show_details(name)

    def on_history_selected(self, item):
        name = item.text()
        self.show_details(name)

    def add_to_favorites(self):
        text = self.details_text.toPlainText()
        if not text.strip():
            QMessageBox.warning(self, "Warnung", "Kein Item ausgewählt.")
            return
        first_line = text.splitlines()[0]
        if first_line.startswith("Item Name: "):
            item_name = first_line[len("Item Name: "):]
            if item_name not in self.favorites:
                self.favorites.append(item_name)
                self.update_favorites_list()
                save_json(FAV_FILE, self.favorites)
            else:
                QMessageBox.information(self, "Info", f"'{item_name}' ist bereits in den Favoriten.")
        else:
            QMessageBox.warning(self, "Warnung", "Ungültige Itemdetails.")

    def remove_from_favorites(self):
        selected = self.favorites_list.currentItem()
        if selected:
            item_name = selected.text()
            if item_name in self.favorites:
                self.favorites.remove(item_name)
                self.update_favorites_list()
                save_json(FAV_FILE, self.favorites)
        else:
            QMessageBox.warning(self, "Warnung", "Kein Favorit ausgewählt.")

    def add_to_history(self, item_name):
        if item_name in self.history:
            self.history.remove(item_name)
        self.history.insert(0, item_name)
        if len(self.history) > 5:
            self.history = self.history[:5]
        self.update_history_list()
        save_json(HIST_FILE, self.history)

    def update_favorites_list(self):
        self.favorites_list.clear()
        for item in self.favorites:
            self.favorites_list.addItem(item)

    def update_history_list(self):
        self.history_list.clear()
        for item in self.history:
            self.history_list.addItem(item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ItemFinder()
    window.show()
    sys.exit(app.exec())
