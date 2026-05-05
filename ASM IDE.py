from customtkinter import *

root = CTk()
root.geometry("1920x1080")
root.title("Virtual CPU IDE")
root.after(25, lambda: root.state("zoomed"))

work_space = CTkFrame(root,
                      width = 1135,
                      height = 550,
                      border_width = 2.5,
                      border_color = "white" 
                      )

file_explorer = CTkFrame(root,
                         width = 384,
                         height = 785,
                         border_width = 2.5,
                         border_color = "white" 
                         )

terminal_frame = CTkFrame(root,
                    width = 1135,
                    height = 230,
                    border_width = 2.5,
                    border_color = "white"
                    )

terminal_cards = CTkFrame(terminal_frame,
                          width = 1120,
                          height = 25)

terminal = CTkTextbox(terminal_frame,
                      width = 1120,
                      height = 185)



work_space.place(x = 395, y = 5)
work_space.grid_propagate(False)


file_explorer.place(x = 5, y = 5)
file_explorer.grid_propagate(False)


terminal_frame.place(x = 395, y = 560)
terminal_frame.grid_propagate(False)

terminal_cards.place(x = 7, y = 7)
terminal.place(x = 7, y = 35)



root.mainloop()