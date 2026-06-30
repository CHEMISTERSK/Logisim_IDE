import os, shutil, subprocess
from customtkinter import *
from pathlib import Path
from PIL import Image
from tkinter import ttk
from tkinter import Event

# Init
root = CTk()
root.geometry("1920x1080")
root.title("Virtual CPU IDE")
root.iconbitmap(f"{os.path.dirname(os.path.abspath(__file__))}\\icons\\icon.ico")
root.after(25, lambda: root.state("zoomed"))

ROOT_DIR = f"{os.path.dirname(os.path.abspath(__file__))}".capitalize()
work_dir = ROOT_DIR
imbeded_commands = {"clr", "cls"}
command_history = []
command_history_index: int = None
active_file = None

# Icon loading
compile_icon_path = Path(__file__).with_name("icons") / "compile_icon.png"
folder_icon_path = Path(__file__).with_name("icons") / "folder.png"
new_file_icon_path = Path(__file__).with_name("icons") / "new_file.png"
new_folder_icon_path = Path(__file__).with_name("icons") / "new_folder.png"
delete_file_icon_path = Path(__file__).with_name("icons") / "delete_file.png"
refresh_file_explorer_icon_path = Path(__file__).with_name("icons") / "refresh.png"

# Icon compiling
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
delete_file_icon = CTkImage(light_image = Image.open(delete_file_icon_path),
                            dark_image = Image.open(delete_file_icon_path),
                            size = (25, 25))
refresh_file_explorer_icon = CTkImage(light_image = Image.open(refresh_file_explorer_icon_path),
                                      dark_image = Image.open(refresh_file_explorer_icon_path),
                                      size = (25, 25))

# Definition of file explorer 
file_explorer: CTkFrame = CTkFrame(root,
                         width = 384,
                         height = 785,
                         border_width = 2.5,
                         border_color = "white")

root_path_link = CTkButton(file_explorer,
                           text = "Open Projects Folder ",
                           font = ("arial", 15, "bold"),
                           width = 120,
                           height = 30,
                           image = folder_icon,
                           command = lambda: os.startfile(f"{os.path.dirname(os.path.abspath(__file__))}\\projects"))

delete_file = CTkButton(file_explorer,
                        text = "",
                        width = 30,
                        height = 30,
                        image = delete_file_icon,
                        command = lambda: del_file())

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

# Definition of embedded terminal
terminal_frame = CTkFrame(root,
                          width = 1135,
                          height = 230,
                          border_width = 2.5,
                          border_color = "white")

terminal_working_path = CTkFrame(terminal_frame,
                                 width = 1120,
                                 height = 30)

working_dir_label = CTkLabel(terminal_working_path,
                             text = f"Working Directory: {work_dir}>",
                             font = ("Consolas", 14, "bold"))

terminal = CTkTextbox(terminal_frame,
                      width = 1120,
                      height = 150,
                      state = "disabled",
                      font = ("Consolas", 12))

terminal_input = CTkEntry(terminal_frame,
                          width = 1120,
                          height = 30)

# Definition of workspace
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

# Customizing treeview style for CTk
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

# Functions
def command_execution(command: str = None) -> None:
    global work_dir
    global command_history
    global command_history_index

    if command:
        try:
            if command != command_history[-1]:
                command_history.append(command)
        except IndexError:
            command_history.append(command)

        command_history_index = None

        terminal_input.delete("0", "end")
        terminal.configure(state = "normal")
        terminal.insert("end", f"@> {command}\n")

        if command in imbeded_commands:
            if command in ["cls", "clr"]:
                terminal.delete("1.0", "end")
        else:
            if command.split(" ")[0] == "cd" and len(command.split(" ")) > 1:
                if (os.path.exists(work_dir + "\\" + command.split(" ")[1]) == True or os.path.exists(command.split(" ")[1]) == True) and command.split(" ")[1].capitalize() != "C:":
                    if "C:\\" in command.split(" ")[1].capitalize():
                        work_dir = command.split(" ")[1]
                    elif command.split(" ")[1][0:2].upper() == "..":
                        work_dir_list = work_dir.split("\\")
                        del work_dir_list[-1]
                        work_dir = "\\".join(work_dir_list)
                    else: 
                        if command.split(" ")[1] != ".":
                            work_dir = work_dir + "\\" + command.split(" ")[1]

                working_dir_label.configure(text = f"Working Directory: {work_dir.capitalize()}>")
                terminal.configure(state = "disabled")

            cmd_result = subprocess.run(command, shell = True, capture_output = True, text = True, cwd = work_dir)
            output = cmd_result.stdout
            error = cmd_result.stderr
            terminal.insert("end", f"{output}\n")

            if error:
                terminal.insert("end", f"{error}\n")

        terminal.configure(state = "disabled")

def command_history_navigation(event: Event) -> None:
    global command_history
    global command_history_index

    if event.keysym in {"Up", "Down"}:
        if event.keysym == "Up":
            if command_history_index:
                if (len(command_history) + (command_history_index - 1)) >= 0:
                    command_history_index -= 1
            else:
                command_history_index = -1

        elif event.keysym == "Down":
            if command_history_index:
                if (len(command_history) - (command_history_index + 1)) >= 0:
                    command_history_index += 1
            else:
                command_history_index = 0
        
        
        terminal_input.delete("0", "end")
        terminal_input.insert("end", command_history[command_history_index])

    else:
        return

def compilation() -> None:
    global active_file
    if active_file is not None:
        terminal.configure(state = "normal")
        terminal.insert("end", f"@> python {ROOT_DIR}\\vcc.py --file {active_file} --cpu 4x8_vn16")
        terminal.insert("end", f"\n{subprocess.run(["python", f"{ROOT_DIR}\\vcc.py", "--file", active_file, "--cpu", "4x8_vn16"], capture_output = True, text = True).stdout}")
        terminal.insert("end", f"\n{subprocess.run(["python", f"{ROOT_DIR}\\vcc.py", "--file", active_file, "--cpu", "4x8_vn16"], capture_output = True, text = True).stderr}")
        terminal.configure(state = "disabled")

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

def del_file() -> None:
    global active_file
    global editor

    if active_file is None:
        shutil.rmtree(get_selected_path())
    else:
        os.remove(active_file)
    refresh_tree()
    active_file = None
    editor.delete("1.0", "end")

def explorer(work_dir: list[str]) -> list[str]:
    # Rekurzívne načíta štruktúru priečinkov a súborov
    try:
        path = os.path.join(*work_dir) if work_dir else ROOT_DIR + "\\projects"
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

def get_selected_item_path() -> None | Path:
    selected_node = tree.focus()

    if not selected_node:
        return None

    path_parts = []
    current = selected_node
    while current:
        item_text = tree.item(current, "text").rstrip("\\")
        if item_text != "projects":
            path_parts.insert(0, item_text)
        current = tree.parent(current)

    return os.path.join(ROOT_DIR + "\\projects", *path_parts)

def get_selected_path() -> str:
    # Zistí cestu vybraného priečinka v strome
    selected_path = get_selected_item_path()

    if not selected_path:
        return ROOT_DIR + "\\projects"

    if os.path.isfile(selected_path):
        return os.path.dirname(selected_path)

    return selected_path if os.path.isdir(selected_path) else ROOT_DIR + "\\projects"

def insert_files(parent: str, path: str) -> None:
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            node = tree.insert(parent, "end", text = item, open = False)

            if os.path.isdir(full_path):
                tree.insert(node, "end")
    except PermissionError:
        pass

def load_active_file() -> None:
    global active_file
    global editor

    if active_file is None:
        pass
    else:
        with open(active_file, "r") as file:
            editor.delete("1.0", "end")
            editor.insert("end", file.read())

def open_node(event: Event) -> None:
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
        
        path = os.path.join(ROOT_DIR + "\\projects", *path_parts[1:])
        insert_files(node, path)

def refresh_tree() -> None:
    tree.delete(*tree.get_children())
    root_node = tree.insert("", "end", text = ROOT_DIR + "\\projects".capitalize() + "\\", open = True)
    insert_files(root_node, ROOT_DIR + "\\projects")

def save_active_file(event: Event = None) -> str:
    if active_file is None:
        return "break"

    with open(active_file, "w") as file:
        file.write(editor.get("1.0", "end-1c"))

    return "break"

def update_active_file(event: Event = None) -> None:
    global active_file

    selected_path = get_selected_item_path()
    if selected_path and os.path.isfile(selected_path):
        active_file = selected_path
    else:
        active_file = None

    load_active_file()
    
# Setup file explorere
tree = ttk.Treeview(file_explorer, style = "Treeview")
root_node = tree.insert("", "end", text = ROOT_DIR + "\\projects".capitalize() + "\\", open = True)

insert_files(root_node, ROOT_DIR + "\\projects")

tree.bind("<<TreeviewOpen>>", open_node)
tree.bind("<<TreeviewSelect>>", update_active_file)

# Key biding
root.bind_all("<Control-s>", save_active_file)
root.bind_all("<Control-S>", save_active_file)

terminal_input.bind("<Return>", lambda event: command_execution(terminal_input.get()))
terminal_input.bind("<Key>", lambda event: command_history_navigation(event))


# Root grid init
root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 4)

root.grid_rowconfigure(0, weight = 4)
root.grid_rowconfigure(1, weight = 1)


# File explorer
file_explorer.grid(row = 0, column = 0, rowspan = 2, sticky = "nsew", padx = 10, pady = 10)

file_explorer.grid_columnconfigure(0, weight = 1)
file_explorer.grid_rowconfigure(1, weight = 1)

# File explorer buttons
root_path_link.grid(row = 0, column = 0, sticky = "nw", padx = (5, 2.5), pady = (5, 5))

delete_file.grid(row = 0, column = 1, sticky = "nw", padx = 2.5, pady = (5, 5))
new_file.grid(row = 0, column = 2, sticky = "nw", padx = 2.5, pady = (5, 5))
new_folder.grid(row = 0, column = 3, sticky = "nw", padx = 2.5, pady = (5, 5))
refresh_file_explorer.grid( row = 0, column = 4, sticky = "nw", padx = (2.5, 5), pady = (5, 5))

tree.grid(row = 1, column = 0, columnspan = 6, sticky = "nsew", padx = 5, pady = (0, 5))


# Codeing workspace
work_space.grid(row = 0, column = 1, sticky = "nsew", padx =  10, pady = 10)

work_space.grid_columnconfigure(0, weight = 1)
work_space.grid_columnconfigure(1, weight = 0)
work_space.grid_rowconfigure(1, weight = 1)

hot_bar.grid(row = 0, column = 0, sticky = "ew", padx =  (10, 2.5), pady = (10, 5))
compile_button.grid(row = 0, column = 1, sticky = "e", padx = (2.5, 10), pady = (10, 5))
editor.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", padx = 10, pady = (5, 10))


# Terminal monitor
terminal_frame.grid(row = 1, column = 1, sticky = "nsew", padx =  10, pady = 10)

terminal_frame.grid_columnconfigure(0, weight = 1)
terminal_frame.grid_rowconfigure(1, weight = 1)

terminal_working_path.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = (10, 2.5))
working_dir_label.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = 5)
terminal.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 5)
terminal_input.grid(row = 2, column = 0, sticky = "ew", padx = 10, pady = (2.5, 10))

# End of main loop
root.mainloop()