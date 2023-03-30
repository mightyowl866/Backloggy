import tkinter as tk
import shelve
from tkinter import *
from tkinter import messagebox
import pandas as pd
import openpyxl




"""
Backloggy, the videogame backlogger

by Ryan Grant/MightyOwl86

"""

"""
-----VERSION----
V0.1 - Current
-Basic functionality for the program.
-User can create, edit, search, and delete entries.
-User can export their database to an excel file, which is store the same folder the program is located.
"""



class UserInput:
    def __init__(self, name, system, status):
        self.name = name
        self.system = system
        self.status = status

def save_user_input(user_input):
    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            for existing_input in inputs:
                if existing_input.name == user_input.name and existing_input.system == user_input.system:
                    messagebox.showwarning("Warning", "Duplicate entry found")
                    return inputs
        else:
            inputs = []
        inputs.append(user_input)
        db['inputs'] = inputs
    return inputs

def edit_user_input():
    name = name_entry.get().upper()
    system = system_entry.get().upper()
    status = status_entry.get().upper()

    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            for item in inputs:
                if item.name == name:
                    item.system = system
                    item.status = status
                    db['inputs'] = inputs
                    console.delete('1.0', tk.END)
                    console.insert(tk.END, "Entry edited.\n")
                    for item in inputs:
                        console.insert(tk.END, f"Name: {item.name:<40}, System: {item.system:<20}, Status: {item.status:<20}\n")
                    return
    messagebox.showwarning("Warning", "Entry not found")

def create_user_input():
    name = name_entry.get().upper()
    system = system_entry.get().upper()
    status = status_entry.get().upper()
    user_input = UserInput(name, system, status)
    inputs = save_user_input(user_input)
    console.delete('1.0', tk.END)
    for item in inputs:
        console.insert(tk.END, f"Name: {item.name: <40} System: {item.system:<20} Status: {item.status:<20}\n")

def remove_user():
    name = name_entry.get()
    system = system_entry.get()
    status = status_entry.get()
    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            for i, item in enumerate(inputs):
                if item.name == name and item.system == system and item.status == status:
                    console.delete('1.0', tk.END)
                    console.insert(tk.END, f"Removing input: {item.name:<40}, {item.system:<20}, {item.status:<20}\n")
                    del inputs[i]
                    db['inputs'] = inputs
                    messagebox.showinfo("Info", "Entry removed.")
                    for item in inputs:
                        console.insert(tk.END, f"Name: {item.name:<40}, System: {item.system:<20}, Status: {item.status:<20}\n")
                    return
            console.delete('1.0', tk.END)
            console.insert(tk.END, "No matching input found.\n")
        else:
            console.delete('1.0', tk.END)
            console.insert(tk.END, "No inputs to remove.\n")

def search():
    name = name_entry.get().upper()
    system = system_entry.get().upper()
    status = status_entry.get().upper()
    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            if name or system or status:
                results = [item for item in inputs if (not name or name in item.name.upper()) and (not system or system in item.system.upper()) and (not status or status in item.status.upper())]
                console.delete('1.0', tk.END)
                if results:
                    for item in results:
                        console.insert(tk.END, f"Name: {item.name:<40}, System: {item.system:<20}, Status: {item.status:<20}\n")
                else:
                    console.insert(tk.END, "No matching input found.\n")
            else:
                console.delete('1.0', tk.END)
                console.insert(tk.END, "Please enter a name, system, or status.\n")
        else:
            console.delete('1.0', tk.END)
            console.insert(tk.END, "No inputs to search.\n")


def sort_by_name():
    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            inputs.sort(key=lambda x: x.name)
            console.delete('1.0', tk.END)
            for item in inputs:
                console.insert(tk.END, f"Name: {item.name: <40} System: {item.system:<20} Status: {item.status:<20}\n")
        else:
            console.delete('1.0', tk.END)
            console.insert(tk.END, "No inputs to sort.\n")

def sort_by_system():
    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            inputs.sort(key=lambda x: x.system)
            console.delete('1.0', tk.END)
            for item in inputs:
                console.insert(tk.END, f"Name: {item.name: <40} System: {item.system:<20} Status: {item.status:<20}\n")
        else:
            console.delete('1.0', tk.END)
            console.insert(tk.END, "No inputs to sort.\n")

def export_to_excel():
    with shelve.open('database') as db:
        if 'inputs' in db:
            inputs = db['inputs']
            df = pd.DataFrame([(item.name, item.system, item.status) for item in inputs], columns=['Name', 'System', 'Status'])
            df.to_excel('backloggy_database.xlsx', index=False)
            console.delete('1.0', tk.END)
            console.insert(tk.END, "Database exported to Excel file in program directory.\n")
        else:
            console.delete('1.0', tk.END)
            console.insert(tk.END, "No inputs to export.\n")




root = tk.Tk()
root.title("Backloggy V0.1")
root.resizable(False, False)

root['bg'] ='#36393f'

input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT)
input_frame.config(bg='#36393f')

title_label = tk.Label(input_frame, text="Backloggy V0.1", fg='white')
title_label.pack()
title_label.config(bg='#36393f')

name_label = tk.Label(input_frame, text="Name", fg='white')
name_label.pack()
name_label.config(bg='#36393f')
name_entry = tk.Entry(input_frame, width=30)
name_entry.pack()

system_label = tk.Label(input_frame, text="System", fg='white', bg='#36393f')
system_label.pack()
system_entry = tk.StringVar(value='     ')
system_dropdown = tk.OptionMenu(input_frame, system_entry,'     ', 'NES', 'SNES','GB','GBC', 'N64', 'GCN','GBA','NDS', 'WII','3DS', 'WII U', 'SWITCH', 'Master System', 'Genesis','Saturn', 'Dreamcast','PS1','PS2','PSP','PS3','PSVITA','PS4','PS5','Xbox','Xbox 360', 'Xbox One', 'Xbox Series X/S', 'PC', 'Other')
system_dropdown.pack()

status_label = tk.Label(input_frame, text="Status", fg='white', bg='#36393f')
status_label.pack()
status_entry = tk.StringVar(value='')
status_dropdown = tk.OptionMenu(input_frame, status_entry,'', 'Unplayed', 'Played', 'Completed')
status_dropdown.pack()

save_button = tk.Button(input_frame, text="Save", command=create_user_input, fg='white', width=20)
save_button.pack()
save_button.config(bg='#36393f')

remove_button = tk.Button(input_frame, text='Remove Entry', command=remove_user, fg='white', width=20)
remove_button.pack()
remove_button.config(bg='#36393f')

edit_button = tk.Button(input_frame, text='Edit Entry', command=edit_user_input, fg='white', width=20)
edit_button.pack()
edit_button.config(bg='#36393f')

search_button = tk.Button(input_frame, text="Search", command=search, fg='white', width=20)
search_button.pack()
search_button.config(bg='#36393f')

button_frame = tk.Frame(root)
button_frame.pack()

sort_by_name_button = tk.Button(button_frame, text="Sort by Name", command=sort_by_name, fg='white', width=20)
sort_by_name_button.pack(side=tk.LEFT)
sort_by_name_button.config(bg='#36393f')

sort_by_sys_button = tk.Button(button_frame, text="Sort by System", command=sort_by_system, fg='white', width=20)
sort_by_sys_button.pack(side=tk.LEFT)
sort_by_sys_button.config(bg='#36393f')

export_button = tk.Button(button_frame, text="Export to Excel", command=export_to_excel,fg='white', width=20)
export_button.pack(side=tk.LEFT)
export_button.config(bg='#36393f')

console_frame = tk.Frame(root)
console_frame.pack(side=tk.RIGHT)
console_frame.config(bg='#36393f')

console_label = tk.Label(console_frame, text="--Game Database--",fg='white')
console_label.pack()
console_label.config(bg='#36393f')


#The actual console for the program. This is where entries are displayed.
console = tk.Text(console_frame, height=20, width=100, fg='white')
console.pack()
console.config(bg='#484c54')


credits_label = tk.Label(console_frame, text="Program by MightyOwl86",fg='white')
credits_label.pack()
credits_label.config(bg='#36393f')


# initialize console with current entries
with shelve.open('database') as db:
    if 'inputs' in db:
        inputs = db['inputs']
        for item in inputs:
            console.insert(tk.END, f"Name: {item.name: <40} System: {item.system:<20} Status: {item.status:<20}\n")

root.mainloop()
