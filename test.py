import os
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("600x400")

tree = ttk.Treeview(app)
tree.pack(fill="both", expand=True, padx=10, pady=10)

# pridanie root priečinka
root_path = f"{os.path.dirname(os.path.abspath(__file__))}\\projects"

root_node = tree.insert("", "end", text = "projects\\", open = True)

def insert_files(parent, path):
    try:
        for item in os.listdir(path):
            full_path = os.path.join(path, item)

            node = tree.insert(parent, "end", text=item, open=False)

            # ak je to priečinok, pridáme dummy child
            if os.path.isdir(full_path):
                tree.insert(node, "end")
    except PermissionError:
        pass

insert_files(root_node, root_path)

def open_node(event):
    node = tree.focus()

    # odstránenie dummy childov
    children = tree.get_children(node)

    if len(children) == 1 and tree.item(children[0], "text") == "":
        tree.delete(children[0])

        path_parts = []

        current = node
        while current:
            path_parts.insert(0, tree.item(current, "text"))
            current = tree.parent(current)

        path = os.path.join(*path_parts)

        insert_files(node, path)

tree.bind("<<TreeviewOpen>>", open_node)

app.mainloop()