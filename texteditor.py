import tkinter as tk
from tkinter import filedialog, messagebox

import os

current_file = None
text_undo_stack = []
text_redo_stack = []

root = tk.Tk()
root.title("Untitled.txt" + ' - textpad')
root.geometry('800x600')


def update_title(new_title):
    root.title(new_title + ' - textpad')

def new_file():
    global current_file
    text.delete(1.0, tk.END)
    update_title("Untitled.txt")
    current_file = None

def open_file():
    global current_file
    file_path = filedialog.askopenfilename(defaultextension='.txt', filetypes=[('All Files', '*.*')])
    if file_path:
        current_file = file_path
        with open(file_path, 'r') as file:
            filename = os.path.basename(file.name).split('/')[-1]
            update_title(filename)
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())
            messagebox.showinfo("Info", 'File opened successfully')
            
def save_as_file():
    file_path = filedialog.asksaveasfilename(initialfile = 'Untitled.txt', defaultextension='.txt' , filetypes=[('All Files', '*.*')])
    if file_path:
        global current_file
        current_file = file_path
        with open(file_path, 'w') as file:
            filename = os.path.basename(file.name).split('/')[-1]
            update_title(filename)
            file.write(text.get(1.0, tk.END))
            messagebox.showinfo("Info", "File saved successfully")

def save_file():
    global current_file
    if current_file:
        with open(current_file, "w") as file:
            text_content = text.get("1.0", "end-1c")
            file.write(text_content)
    else:
        save_as_file()
            
def select_all(): # to select all text inside Text box 
    text.tag_add("sel", "1.0","end")
    text.tag_config("sel",background="green",foreground="red")
    
def cut_select(): # Cut the selection of text to clipboard 
    global data 
    if text.selection_get():
        data=text.selection_get()
        text.delete('sel.first','sel.last') 
        
def copy_select(): # copy selected text to clipboard
    global data 
    if text.selection_get():
        data=text.selection_get()
        
def paste_select():
    global data
    text.insert(tk.END,data) # Paste data from clipboard
            

menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='New', command=new_file)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_file)
file_menu.add_command(label='Save as', command=save_as_file)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

file_menu2 = tk.Menu(menu)
menu.add_cascade(label='Edit', menu=file_menu2)
file_menu2.add_command(label='Select All', command=select_all)
file_menu2.add_command(label='Copy', command=copy_select)
file_menu2.add_command(label='Cut', command=cut_select)
file_menu2.add_command(label='Paste', command=paste_select)

text = tk.Text(root, wrap=tk.WORD, font = ('Helvetica', 12), fg='blue')
text.pack(expand=tk.YES, fill=tk.BOTH, side=tk.LEFT, padx=5, pady=10)

yscrollbar = tk.Scrollbar(root, orient='vertical')
yscrollbar.pack(expand=tk.YES, fill=tk.Y)

def on_yscroll(*args):
   text.yview(*args)

yscrollbar.config(command=on_yscroll)

text.config(yscrollcommand=yscrollbar.set)

root.mainloop()