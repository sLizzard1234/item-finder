import tkinter as tk
from tkinter import ttk
import csv
import json
import os

FAVORITES_FILE = 'favorites.json'
HISTORY_LIMIT = 5

def load_data():
    items = []
    with open('items.csv', mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            items.append(row)
    return items

def save_favorites():
    with open(FAVORITES_FILE, 'w', encoding='utf-8') as f:
        json.dump(favorites, f)

def load_favorites():
    if os.path.exists(FAVORITES_FILE):
        with open(FAVORITES_FILE, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def search_item():
    search_term = search_var.get().lower()
    filtered_items = [item for item in items if search_term in item['item_name'].lower()]
    update_listbox(filtered_items)

def update_listbox(filtered_items):
    item_listbox.delete(0, tk.END)
    for item in filtered_items:
        item_listbox.insert(tk.END, item['item_name'])

def show_item_details_by_name(item_name):
    item_details = next((item for item in items if item['item_name'] == item_name), None)
    if item_details:
        details_text = f"Item Name: {item_details['item_name']}\nStockwerk: {item_details['stockwerk']}\nGang Nummer: {item_details['gang_nummer']}\nBlocknummer: {item_details['blocknummer']}"
        details_text_widget.delete(1.0, tk.END)
        details_text_widget.insert(tk.END, details_text)

        # Update history
        if item_name in history:
            history.remove(item_name)
        history.insert(0, item_name)
        if len(history) > HISTORY_LIMIT:
            history.pop()
        update_history_listbox()

def show_item_details(event):
    selected_index = item_listbox.curselection()
    if selected_index:
        selected_item = item_listbox.get(selected_index)
        show_item_details_by_name(selected_item)

def show_item_from_favorites(event):
    selected_index = favorites_listbox.curselection()
    if selected_index:
        selected_item = favorites_listbox.get(selected_index)
        show_item_details_by_name(selected_item)

def show_item_from_history(event):
    selected_index = history_listbox.curselection()
    if selected_index:
        selected_item = history_listbox.get(selected_index)
        show_item_details_by_name(selected_item)

def on_search_var_change(*args):
    search_item()

def add_to_favorites():
    selected_index = item_listbox.curselection()
    if selected_index:
        selected_item = item_listbox.get(selected_index)
        if selected_item not in favorites:
            favorites.append(selected_item)
            save_favorites()
            update_favorites_listbox()

def remove_from_favorites():
    selected_index = favorites_listbox.curselection()
    if selected_index:
        item_name = favorites_listbox.get(selected_index)
        if item_name in favorites:
            favorites.remove(item_name)
            save_favorites()
            update_favorites_listbox()

def update_favorites_listbox():
    favorites_listbox.delete(0, tk.END)
    for item in favorites:
        favorites_listbox.insert(tk.END, item)

def update_history_listbox():
    history_listbox.delete(0, tk.END)
    for item in history:
        history_listbox.insert(tk.END, item)

# GUI
root = tk.Tk()
root.title("Minecraft Item Finder")

items = load_data()
favorites = load_favorites()
history = []

search_var = tk.StringVar()
search_var.trace_add("write", on_search_var_change)

# Search Frame
search_frame = ttk.Frame(root, padding="10")
search_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

search_label = ttk.Label(search_frame, text="Search Item:")
search_label.grid(row=0, column=0, sticky="w")

search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.grid(row=0, column=1, sticky="ew")

search_button = ttk.Button(search_frame, text="Search", command=search_item)
search_button.grid(row=0, column=2, sticky="e")

search_frame.columnconfigure(1, weight=1)

# Listbox Frame
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

# Details Frame
details_frame = ttk.Frame(root, padding="10")
details_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

details_text_widget = tk.Text(details_frame, height=8, width=50)
details_text_widget.grid(row=0, column=0, sticky="ew")

# Side Frame (Favoriten & Historie)
side_frame = ttk.Frame(root, padding="10")
side_frame.grid(row=1, column=1, sticky="n")

fav_label = ttk.Label(side_frame, text="Favoriten:")
fav_label.pack(anchor="w")

favorites_listbox = tk.Listbox(side_frame, height=6)
favorites_listbox.pack(fill="x")
favorites_listbox.bind("<<ListboxSelect>>", show_item_from_favorites)

remove_fav_button = ttk.Button(side_frame, text="Aus Favoriten entfernen", command=remove_from_favorites)
remove_fav_button.pack(fill="x", pady=(5, 0))

add_fav_button = ttk.Button(side_frame, text="Zu Favoriten hinzufügen", command=add_to_favorites)
add_fav_button.pack(fill="x", pady=(10, 0))

hist_label = ttk.Label(side_frame, text="Historie:")
hist_label.pack(anchor="w", pady=(15, 0))

history_listbox = tk.Listbox(side_frame, height=5)
history_listbox.pack(fill="x")
history_listbox.bind("<<ListboxSelect>>", show_item_from_history)

# Init
update_favorites_listbox()

root.columnconfigure(0, weight=3)
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
