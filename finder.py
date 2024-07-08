import tkinter as tk
from tkinter import ttk
import csv

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

root = tk.Tk()
root.title("Item Search App")

items = load_data()

search_var = tk.StringVar()
search_var.trace_add("write", on_search_var_change)

# Search Frame
search_frame = ttk.Frame(root, padding="10")
search_frame.grid(row=0, column=0, sticky="ew")

search_label = ttk.Label(search_frame, text="Search Item:")
search_label.grid(row=0, column=0, sticky="w")

search_entry = ttk.Entry(search_frame, textvariable=search_var)
search_entry.grid(row=0, column=1, sticky="ew")

search_button = ttk.Button(search_frame, text="Search", command=search_item)
search_button.grid(row=0, column=2, sticky="e")

# Listbox Frame
listbox_frame = ttk.Frame(root, padding="10")
listbox_frame.grid(row=1, column=0, sticky="nsew")

item_listbox = tk.Listbox(listbox_frame, height=15)
item_listbox.grid(row=0, column=0, sticky="nsew")

item_listbox.bind("<<ListboxSelect>>", show_item_details)

scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=item_listbox.yview)
scrollbar.grid(row=0, column=1, sticky="ns")

item_listbox.configure(yscrollcommand=scrollbar.set)

# Details Frame
details_frame = ttk.Frame(root, padding="10")
details_frame.grid(row=2, column=0, sticky="ew")

details_text_widget = tk.Text(details_frame, height=10, width=50)
details_text_widget.grid(row=0, column=0, sticky="ew")

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

root.mainloop()
