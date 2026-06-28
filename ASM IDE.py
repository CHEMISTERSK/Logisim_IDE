import subprocess
import os
from customtkinter import *
from pathlib import Path
from PIL import Image
from tkinter import ttk

from virtual_cpu_compiler import compiler

root = CTk()
root.geometry("1920x1080")
root.title("Virtual CPU IDE")
root.after(25, lambda: root.state("zoomed"))

ROOT_DIR = f"{os.path.dirname(os.path.abspath(__file__))}\\projects"
work_dir: list[str] = []

def scale(root):
    dpi_scale  =  root.winfo_fpixels('1i') / 72

    set_window_scaling(dpi_scale)
    set_widget_scaling(dpi_scale)


def refresh_tree():
    tree.delete(*tree.get_children())
    root_node = tree.insert("", "end", text = ROOT_DIR.capitalize() + "\\", open = True)
    insert_files(root_node, ROOT_DIR)



compile_icon_path = Path(__file__).with_name("icons") / "compile_icon.png"
folder_icon_path = Path(__file__).with_name("icons") / "folder.png"
new_file_icon_path = Path(__file__).with_name("icons") / "new_file.png"
new_folder_icon_path = Path(__file__).with_name("icons") / "new_folder.png"
refresh_file_explorer_icon_path = Path(__file__).with_name("icons") / "refresh.png"

compile_icon = CTkImage(light_image = Image.open(compile_icon_path),
                dark_image = Image.open(compile_icon_path),
                size = (25, 25))
folder_icon = CTkImage(light_image = Image.open(folder_icon_path),
                       dark_image = Image.open(folder_icon_path),
                       size = (25, 25))
new_file_icon = CTkImage(light_image = Image.open(new_file_icon_path),
                       dark_image = Image.open(new_file_icon_path),
                       size = (25, 25))
new_folder_icon = CTkImage(light_image = Image.open(new_folder_icon_path),
                           dark_image = Image.open(new_folder_icon_path),
                           size = (25, 25))
refresh_file_explorer_icon = CTkImage(light_image = Image.open(refresh_file_explorer_icon_path),
                                      dark_image = Image.open(refresh_file_explorer_icon_path),
                                      size = (25, 25))


file_explorer = CTkFrame(root,
                         width = 384,
                         height = 785,
                         border_width = 2.5,
                         border_color = "white" )

path_link = CTkButton(file_explorer,
                      text = "Open Projects Folder ",
                      font = ("arial", 15, "bold"),
                      width = 120,
                      height = 30,
                      image = folder_icon,
                      command = lambda: os.startfile(f"{os.path.dirname(os.path.abspath(__file__))}\\projects"))

new_file = CTkButton(file_explorer,
                     text = "",
                     width = 30,
                     height = 30,
                     image = new_file_icon,
                     command = lambda: create_file())

new_folder = CTkButton(file_explorer,
                     text = "",
                     width = 30,
                     height = 30,
                     image = new_folder_icon,
                     command = lambda: create_folder())

refresh_file_explorer = CTkButton(file_explorer,
                                  text = "",
                                  width = 30,
                                  height = 30,
                                  image = refresh_file_explorer_icon,
                                  command = lambda: refresh_tree())


# Prispôsobenie treeview štýlu pre CTk
style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview",
                background = "#212121",
                foreground = "white",
                fieldbackground = "#212121",
                borderwidth = 0,
                font=("arial", 10))
style.configure("Treeview.Heading",
                background = "#2a2a2a",
                foreground = "white",
                borderwidth = 0,
                font = ("arial", 10, "bold"))
style.map('Treeview',
          background = [('selected', '#0078d4')],
          foreground = [('selected', 'white')])

# Treeview pre stromovú štruktúru
tree = ttk.Treeview(file_explorer, style = "Treeview")
tree.grid(row = 1, column = 0, columnspan = 4, sticky = "nsew", padx = 5, pady = (0, 5))


terminal_frame = CTkFrame(root,
                    width = 1135,
                    height = 230,
                    border_width = 2.5,
                    border_color = "white")

terminal_cards = CTkFrame(terminal_frame,
                          width = 1120,
                          height = 30)

terminal = CTkTextbox(terminal_frame,
                      width = 1120,
                      height = 150,
                      state = "disabled",
                      font = ("Consolas", 12))

terminal_input = CTkEntry(terminal_frame,
                          width = 1120,
                          height = 30)


def compilation():
    terminal.configure(state = "normal")
    terminal.insert("end", "@> python virtual_cpu_compiler.py --file pro.txt --cpu 4x8_vn16")
    terminal.insert("end", f"\n{subprocess.run(["python", "virtual_cpu_compiler.py", "--file", "pro", "--cpu", "4x8_vn16"], capture_output = True, text = True).stdout}")
    terminal.configure(state = "disabled")


work_space = CTkFrame(root,
                      width = 1135,
                      height = 550,
                      border_width = 2.5,
                      border_color = "white")

hot_bar = CTkFrame(work_space,
                   width = 1075,
                   height = 30)

compile_button = CTkButton(work_space,
                           image = compile_icon,
                           text = "",
                           width = 25,
                           height = 25,
                           command = lambda: compilation())

editor = CTkTextbox(work_space,
                    width = 1120,
                    height = 495,
                    font = ('Consolas', 13))


# Pridanie root priečinka
root_node = tree.insert("", "end", text = ROOT_DIR.capitalize() + "\\", open = True)

def insert_files(parent, path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            node = tree.insert(parent, "end", text = item, open = False)

            if os.path.isdir(full_path):
                tree.insert(node, "end")
    except PermissionError:
        pass

insert_files(root_node, ROOT_DIR)

def open_node(event):
    node = tree.focus()
    # Odstránenie dummy childov
    children = tree.get_children(node)
    if len(children) ==  1 and tree.item(children[0], "text") == "":
        tree.delete(children[0])
        
        path_parts = []
        current = node
        while current:
            path_parts.insert(0, tree.item(current, "text").rstrip("\\"))
            current = tree.parent(current)
        
        path = os.path.join(ROOT_DIR, *path_parts[1:])
        insert_files(node, path)

tree.bind("<<TreeviewOpen>>", open_node)


def get_selected_path():
    """Zistí cestu vybraného priečinka v strome"""
    selected_node = tree.focus()
    
    if not selected_node:
        return ROOT_DIR
    
    # Rekonstruuj cestu z hierarchie
    path_parts = []
    current = selected_node
    while current:
        item_text = tree.item(current, "text").rstrip("\\")
        if item_text != "projects":  # Preskoči root
            path_parts.insert(0, item_text)
        current = tree.parent(current)
    
    full_path = os.path.join(ROOT_DIR, *path_parts)
    
    # Ak je to súbor, vráť jeho priečinok
    if os.path.isfile(full_path):
        return os.path.dirname(full_path)
    
    return full_path if os.path.isdir(full_path) else ROOT_DIR

def create_file() -> None:
    selected_path = get_selected_path()
    file_path = os.path.join(selected_path, "newfile.txt")
    with open(file_path, "w"):
        pass
    refresh_tree()

def create_folder(folder: str = "new_folder") -> None:
    selected_path = get_selected_path()
    Path(os.path.join(selected_path, folder)).mkdir(parents = True, exist_ok = True)
    refresh_tree()

def explorer(work_dir: list[str]) -> list[str]:
    """Rekurzívne načíta štruktúru priečinkov a súborov"""
    try:
        path = os.path.join(*work_dir) if work_dir else ROOT_DIR
        items = []
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            items.append(item)
            if os.path.isdir(full_path):
                # Rekurzívne načítaj podpriečinky
                sub_items = explorer(work_dir + [item])
                items.extend(sub_items)
        return items
    except PermissionError:
        return []


# root grid init
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 4)

root.grid_rowconfigure(0, weight = 4)
root.grid_rowconfigure(1, weight = 1)


# file explorer
file_explorer.grid(row = 0, column = 0, rowspan = 2, sticky = "nsew", padx = 10, pady = 10)

file_explorer.grid_columnconfigure(0, weight = 1)
file_explorer.grid_rowconfigure(1, weight = 1)

# buttons
path_link.grid(row = 0, column = 0, sticky = "nw", padx = (5, 2.5), pady = (5, 5))

new_file.grid(row = 0, column = 1, sticky = "nw", padx = 2.5, pady = (5, 5))
new_folder.grid(row = 0, column = 2, sticky = "nw", padx = 2.5, pady = (5, 5))
refresh_file_explorer.grid(row = 0, column = 3, sticky = "nw", padx = (2.5, 5), pady = (5, 5))


# codeing workspace
work_space.grid(row = 0, column = 1, sticky = "nsew", padx =  10, pady = 10)

work_space.grid_columnconfigure(0, weight = 1)
work_space.grid_columnconfigure(1, weight = 0)
work_space.grid_rowconfigure(1, weight = 1)

hot_bar.grid(row = 0, column = 0, sticky = "ew", padx =  (10, 2.5), pady = (10, 5))
compile_button.grid(row = 0, column = 1, sticky = "e", padx = (2.5, 10), pady = (10, 5))
editor.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", padx = 10, pady = (5, 10))


# terminal monitor
terminal_frame.grid(row = 1, column = 1, sticky = "nsew", padx =  10, pady = 10)

terminal_frame.grid_columnconfigure(0, weight = 1)
terminal_frame.grid_rowconfigure(1, weight = 1)

terminal_cards.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = (10, 2.5))
terminal.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 5)
terminal_input.grid(row = 2, column = 0, sticky = "ew", padx = 10, pady = (2.5, 10))



root.mainloop()