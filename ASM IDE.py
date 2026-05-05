from customtkinter import *
from pathlib import Path
from PIL import Image

from virtual_cpu_compiler import compiler

root = CTk()
root.geometry("1920x1080")
root.title("Virtual CPU IDE")
root.after(25, lambda: root.state("zoomed"))

icon_path = Path(__file__).with_name("icons") / "compile_icon.png"

icon = CTkImage(light_image = Image.open(icon_path),
                dark_image = Image.open(icon_path),
                size = (25, 25),
                )


terminal_frame = CTkFrame(root,
                    width = 1135,
                    height = 230,
                    border_width = 2.5,
                    border_color = "white"
                    )

terminal_cards = CTkFrame(terminal_frame,
                          width = 1120,
                          height = 25
                          )

terminal = CTkTextbox(terminal_frame,
                      width = 1120,
                      height = 150,
                      state = "disabled"
                      )

terminal_input = CTkEntry(terminal_frame,
                          width = 1120,
                          height = 30)


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
                           image = icon,
                           text = "",
                           width = 25,
                           height = 25,
                           command = lambda: compilation())

editor = CTkTextbox(work_space,
                    width = 1120,
                    height = 500
                    )


file_explorer = CTkFrame(root,
                         width = 384,
                         height = 785,
                         border_width = 2.5,
                         border_color = "white" 
                         )






work_space.place(x = 395, y = 5)
work_space.grid_propagate(False)

hot_bar.place(x = 7, y = 7)
compile_button.place(x = 1085, y = 5)
editor.place(x = 7, y = 40)


file_explorer.place(x = 5, y = 5)
file_explorer.grid_propagate(False)


terminal_frame.place(x = 395, y = 560)
terminal_frame.grid_propagate(False)

terminal_cards.place(x = 7, y = 7)
terminal.place(x = 7, y = 35)
terminal_input.place(x = 7, y = 190)


root.mainloop()