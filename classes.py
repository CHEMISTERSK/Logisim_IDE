import customtkinter as ctk

class FileTab(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        name: str,
        path: str,
        content: str,
        on_select = None,
        on_close = None
    ):
        super().__init__(parent, fg_color = "#2b2b2b", corner_radius = 5, width = 160, height = 36)

        self.name = name
        self.path = path
        self.content = content

        self.on_select = on_select
        self.on_close = on_close

        self.file_button = ctk.CTkButton(
            self,
            text = self.name,
            width = 120,
            corner_radius = 5,
            command = self.select_tab
        )
        self.file_button.pack(side = "left")

        self.close_button = ctk.CTkButton(
            self,
            text = "×",
            width = 30,
            corner_radius = 5,
            command = self.close_tab
        )
        self.close_button.pack(side = "left")

    def select_tab(self):
        if self.on_select:
            self.on_select(self)
            active_file = self.path

    def close_tab(self):
        if self.on_close:
            self.on_close(self)

        self.destroy()