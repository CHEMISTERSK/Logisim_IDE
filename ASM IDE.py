import json
from customtkinter import *
from pathlib import Path
from PIL import Image

from virtual_cpu_compiler import compiler

root  =  CTk()
root.geometry("1920x1080")
root.title("Virtual CPU IDE")
root.after(25, lambda: root.state("zoomed"))


def scale(root):
    dpi_scale  =  root.winfo_fpixels('1i') / 72

    set_window_scaling(dpi_scale)
    set_widget_scaling(dpi_scale)

def create_file() -> None:
    with open(f"{os.path.dirname(os.path.abspath(__file__))}\\projects\\newfile.txt", "w"):
            pass

compile_icon_path = Path(__file__).with_name("icons") / "compile_icon.png"
folder_icon_path = Path(__file__).with_name("icons") / "folder.png"
new_file_icon_path = Path(__file__).with_name("icons") / "new_file.png"

compile_icon = CTkImage(light_image = Image.open(compile_icon_path),
                dark_image = Image.open(compile_icon_path),
                size = (25, 25))
folder_icon = CTkImage(light_image = Image.open(folder_icon_path),
                       dark_image = Image.open(folder_icon_path),
                       size = (25, 25))
new_file_icon = CTkImage(light_image = Image.open(new_file_icon_path),
                       dark_image = Image.open(new_file_icon_path),
                       size = (25, 25))


terminal_frame = CTkFrame(root,
                    width = 1135,
                    height = 230,
                    border_width = 2.5,
                    border_color = "white"
                    )

terminal_cards = CTkFrame(terminal_frame,
                          width = 1120,
                          height = 30
                          )

terminal = CTkTextbox(terminal_frame,
                      width = 1120,
                      height = 150,
                      state = "disabled",
                      font = ("Consolas", 12)
                      )

terminal_input = CTkEntry(terminal_frame,
                          width = 1120,
                          height = 30
                          )


def compilation():
    terminal.configure(state = "normal")
    terminal.insert("end", f"\n{compiler("pro", "4x8_vn16")}")
    terminal.configure(state = "disabled")


work_space = CTkFrame(root,
                      width = 1135,
                      height = 550,
                      border_width = 2.5,
                      border_color = "white"
                      )

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
                    height = 495
                    )


file_explorer = CTkFrame(root,
                         width = 384,
                         height = 785,
                         border_width  =  2.5,
                         border_color  =  "white" 
                         )

path_link = CTkButton(file_explorer,
                      text = "Open Projects Folder ",
                      font = ("arial", 15, "bold"),
                      width = 120,
                      height = 30,
                      image = folder_icon,
                      command = lambda: os.startfile(f"{os.path.dirname(os.path.abspath(__file__))}\\projects")
                      )

new_file = CTkButton(file_explorer,
                     text = "",
                     width = 30,
                     height = 30,
                     image = new_file_icon,
                     command = lambda: create_file()
                     )


root.grid_columnconfigure(0, weight = 1)
root.grid_columnconfigure(1, weight = 4)

root.grid_rowconfigure(0, weight = 4)
root.grid_rowconfigure(1, weight = 1)


file_explorer.grid(row = 0, column = 0, rowspan = 2, sticky = "nsew", padx = 10, pady = 10)

path_link.grid(row = 0, column = 0, sticky = "nw", padx = (10, 5), pady = 10)
new_file.grid(row = 0, column = 1, sticky = "nw", padx = 5, pady = 10)


work_space.grid(row = 0, column = 1, sticky = "nsew", padx =  10, pady = 10)

work_space.grid_columnconfigure(0, weight = 1)
work_space.grid_columnconfigure(1, weight = 0)
work_space.grid_rowconfigure(1, weight = 1)

hot_bar.grid(row = 0, column = 0, sticky = "ew", padx =  (10, 2.5), pady = (10, 5))
compile_button.grid(row = 0, column = 1, sticky = "e", padx = (2.5, 10), pady = (10, 5))
editor.grid(row = 1, column = 0, columnspan = 2, sticky = "nsew", padx = 10, pady = (5, 10))


terminal_frame.grid(row = 1, column = 1, sticky = "nsew", padx =  10, pady = 10)

terminal_frame.grid_columnconfigure(0, weight = 1)
terminal_frame.grid_rowconfigure(1, weight = 1)

terminal_cards.grid(row = 0, column = 0, sticky = "ew", padx = 10, pady = (10, 2.5))
terminal.grid(row = 1, column = 0, sticky = "nsew", padx = 10, pady = 5)
terminal_input.grid(row = 2, column = 0, sticky = "ew", padx = 10, pady = (2.5, 10))

root.mainloop()