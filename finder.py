import tkinter as tk
from tkinter import ttk
import csv
import json
import os

FAVORITES_FILE = 'favorites.json'

def load_data():
    items = []
    with open('items.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    return items

def search_item():
    search_term = search_var.get().lower()
    filtered_items = [item for item in items if search_term in item['item_name'].lower()]
    update_listbox(filtered_items)

def update_listbox(filtered_items):
    item_listbox.delete(0, tk.END)
    for item in filtered_items:
        item_listbox.insert(tk.END, item['item_name'])

def show_item_details(event):
    selected_index = item_listbox.curselection()
    if selected_index:
        selected_item = item_listbox.get(selected_index)
        item_details = next(item for item in items if item['item_name'] == selected_item)
        details_text = f"Item Name: {item_details['item_name']}\nStockwerk: {item_details['stockwerk']}\nGang Nummer: {item_details['gang_nummer']}\nBlocknummer: {item_details['blocknummer']}"
        details_text_widget.delete(1.0, tk.END)
        details_text_widget.insert(tk.END, details_text)
    else:
        details_text_widget.delete(1.0, tk.END)

def on_search_var_change(*args):
    search_item()

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        try:
            with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if not content:
                    return []
                return json.loads(content)
        except json.JSONDecodeError:
            print("Warnung: favorites.json ist ungültig. Datei wird ignoriert.")
            return []
    return []

def save_favorites():
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f, ensure_ascii=False, indent=2)

def add_to_favorites():
    selected_index = item_listbox.curselection()
    if selected_index:
        selected_item = item_listbox.get(selected_index)
        if selected_item not in favorites:
            favorites.append(selected_item)
            save_favorites()
            update_favorites_listbox()

def update_favorites_listbox():
    favorites_listbox.delete(0, tk.END)
    for fav in favorites:
        favorites_listbox.insert(tk.END, fav)

def show_favorite_details(event):
    selected_index = favorites_listbox.curselection()
    if selected_index:
        selected_item = favorites_listbox.get(selected_index)
        item = next((i for i in items if i['item_name'] == selected_item), None)
        if item:
            details_text = f"Item Name: {item['item_name']}\nStockwerk: {item['stockwerk']}\nGang Nummer: {item['gang_nummer']}\nBlocknummer: {item['blocknummer']}"
            details_text_widget.delete(1.0, tk.END)
            details_text_widget.insert(tk.END, details_text)

root = tk.Tk()
root.title("Item Search App")

# Daten laden
items = load_data()
favorites = load_favorites()

# Suchvariable
search_var = tk.StringVar()
search_var.trace_add("write", on_search_var_change)

# Layout-Konfiguration
root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

# Suchleiste
search_frame = ttk.Frame(root, padding="10")
search_frame.grid(row=0, column=0, sticky="ew")

search_label = ttk.Label(search_frame, text="Search Item:")
search_label.grid(row=0, column=0, sticky="w")

search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.grid(row=0, column=1, sticky="ew")

search_button = ttk.Button(search_frame, text="Search", command=search_item)
search_button.grid(row=0, column=2, sticky="e")

search_frame.columnconfigure(1, weight=1)

# Linke Seite: Suchergebnisse
listbox_frame = ttk.Frame(root, padding="10")
listbox_frame.grid(row=1, column=0, sticky="nsew")

item_listbox = tk.Listbox(listbox_frame, height=15)
item_listbox.grid(row=0, column=0, sticky="nsew")

item_listbox.bind("<<ListboxSelect>>", show_item_details)

scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=item_listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

item_listbox.configure(yscrollcommand=scrollbar.set)

listbox_frame.rowconfigure(0, weight=1)
listbox_frame.columnconfigure(0, weight=1)

# Details + Button
details_frame = ttk.Frame(root, padding="10")
details_frame.grid(row=2, column=0, sticky="ew")

details_text_widget = tk.Text(details_frame, height=10, width=50)
details_text_widget.grid(row=0, column=0, sticky="ew")

add_fav_button = ttk.Button(details_frame, text="Zu Favoriten hinzufügen", command=add_to_favorites)
add_fav_button.grid(row=1, column=0, pady=5, sticky="w")

# Rechte Seite: Favoritenliste
favorites_frame = ttk.LabelFrame(root, text="Favoriten", padding="10")
favorites_frame.grid(row=0, column=1, rowspan=3, sticky="nsew")

favorites_listbox = tk.Listbox(favorites_frame, height=25)
favorites_listbox.grid(row=0, column=0, sticky="nsew")

favorites_listbox.bind("<<ListboxSelect>>", show_favorite_details)

favorites_frame.rowconfigure(0, weight=1)
favorites_frame.columnconfigure(0, weight=1)

# Startliste aktualisieren
update_favorites_listbox()

root.mainloop()
