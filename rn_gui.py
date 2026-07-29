from customtkinter import *
import os

def rename_(path: str = None) -> tuple[str, str]:
    # Init
    root = CTkToplevel()
    root.geometry("430x200")
    root.title(f"Rename File: {path}")
    root.iconbitmap(f"{os.path.dirname(os.path.abspath(__file__))}\\icons\\icon.ico")
    root.grab_set()

    new_file_path = None
    new_dir_path = None

    # Wegits definition
    rename_frame = CTkFrame(root)

    old_name_label = CTkLabel(rename_frame,
                              font = ("arial", 14, "bold"),
                              text = "From:")
    
    new_name_label = CTkLabel(rename_frame,
                              font = ("arial", 14, "bold"),
                              text = "To:")

    old_name_entry = CTkEntry(rename_frame,
                              width = 360,
                              height = 28,
                              font = ("arial", 14, "bold"))

    new_name_entry = CTkEntry(rename_frame,
                              width = 360,
                              height = 28,
                              font = ("arial", 14, "bold"))
    
    button_frame = CTkFrame(root)

    rename_button = CTkButton(button_frame,
                              font = ("arial", 16, "bold"),
                              text = "Rename",
                              width = 120,
                              height = 30,
                              command = lambda: rename(path, new_name_entry.get()))

    cancel_button = CTkButton(button_frame,
                              font = ("arial", 16, "bold"),
                              text = "Cancel",
                              fg_color = "#ff0000",
                              hover_color = "#8a0101",
                              width = 120,
                              height = 30,
                              command = lambda: root.destroy())

    # Functions
    def is_file(path: str = None) -> tuple[str, bool] | None:
        if path is not None:
            if os.path.isfile(path):
                return (path.split('\\')[-1], True)
            else:
                return (path.split('\\')[-1], False)
        else:
            return ("Err", "Err")

    def fill_entry(path: str = None) -> None:
        new_name_entry.insert("end", is_file(path)[0])
        old_name_entry.insert("end", is_file(path)[0])

        old_name_entry.configure(state = "disabled")

    def rename(path: str = None, new_name: str = None) -> None:
        nonlocal new_file_path, new_dir_path

        if is_file(path)[1] == True:
            new_file_path = path.split('\\')
            new_file_path[-1] = new_name
            new_file_path = '\\'.join(new_file_path)

            with open(path, "r") as file:
                file_content = file.read()

            with open(new_file_path, "w") as file:
                file.write(file_content)

            os.remove(path)
            
        else:
            new_dir_path = path.split('\\')
            new_dir_path[-1] = new_name if '.' not in new_name else new_name.split('.')[0]
            new_dir_path = '\\'.join(new_dir_path)

            os.rename(path, new_dir_path)

        root.destroy()

    if path is None:
        root.destroy()

    # Init functions calls
    fill_entry(path)

    # Key binds
    root.bind_all("<Return>", lambda event: rename(path, new_name_entry.get()))
    root.bind_all("<Escape>", lambda event: root.destroy())

    # Root grid init
    root.grid_columnconfigure(0, weight = 1)
    root.grid_columnconfigure(1, weight = 2)

    root.grid_rowconfigure(0, weight = 2)
    root.grid_rowconfigure(1, weight = 1)

    rename_frame.grid_columnconfigure(0, weight = 1)
    rename_frame.grid_rowconfigure(0, weight = 1)

    rename_frame.grid(row = 0, column = 0, padx = 5, pady = 5)

    # Old name entryes
    old_name_label.grid(row = 0, column = 0, padx = 5, pady = 5)
    old_name_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

    # New name entryes
    new_name_label.grid(row = 1, column = 0, padx = 5, pady = 5)
    new_name_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

    # Buttons
    button_frame.grid_columnconfigure(0, weight = 1)
    button_frame.grid(row = 1, column = 0, padx = 5, pady = 5)

    rename_button.grid(row = 0, column = 0, padx = 5, pady = 5)
    cancel_button.grid(row = 0, column = 1, padx = 5, pady = 5)

    root.wait_window()
    return (path, new_file_path if new_dir_path == None else new_dir_path)