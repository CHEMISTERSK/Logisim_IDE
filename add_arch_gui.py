from customtkinter import *
from tkinter import messagebox
import os, json

# Classes
class config_entry(CTkFrame):
    def __init__(self, parent, name: str, lenght: int = None):
        super().__init__(parent, fg_color = "#2b2b2b", corner_radius = 5, width = 160, height = 36)

        self.name = name
        self.lenght = lenght

        self.label = CTkLabel(self,
                            font = ("Consolas", 14, "bold"),
                            text = f"{name} :")

        self.entry = CTkEntry(self,
                            height = 30,
                            width = lenght,
                            font = ("Consolas", 13, "bold"))

        self.label.pack(side = "left", padx = 2.5, pady = 5)
        self.entry.pack(side = "left", padx = 2.5, pady = 5)

    def _get(self) -> str:
        return self.entry.get()

class ins_entry(CTkFrame):
    def __init__(self, parent, id: int = None):
        super().__init__(parent, fg_color = "#2b2b2b", corner_radius = 5, width = 160, height = 36)

        self.id = id

        self.id_label = CTkLabel(self,
                                    text = f"{f"{self.id}." if isinstance(self.id, int) == True else ""}",
                                    font = ("Consolas", 13, "bold"))

        self.name_entry = CTkEntry(self,
                            height = 30,
                            width = 180,
                            font = ("Consolas", 13, "bold"))

        self.value_entry = CTkEntry(self,
                            height = 30,
                            width = 180,
                            font = ("Consolas", 13, "bold"))

        self.op_checkbox = CTkCheckBox(self,
                                    text = "No Operand?")

        self.id_label.pack(side = "left", padx = 5, pady = 5)
        self.name_entry.pack(side = "left", padx = 5, pady = 5)
        self.value_entry.pack(side = "left", padx = 5, pady = 5)
        self.op_checkbox.pack(side = "left", padx = 5, pady = 5)

    def _get(self) -> tuple[str, str, int]:
        return self.name_entry.get(), self.value_entry.get().replace(" ", ""), self.op_checkbox.get()

# Variables (A -> Z)
address_bits: int = 0
data_bits: int = 0
flag_bits: int = 0
op_codes_bits: int = 0
ram_registers: int = 0

cpu_hw_arch: str = ""
spec_id: str = ""

configs: list[config_entry] = []
config_names: list[str] = ["Address Bits", "Data Bits", "OP Code Bits", "Flag Bits", "Specific ID"]

ins_form: list[ins_entry] = []

# Main Function
def new_cpu_arch() -> None:

    # Init of CTk
    root = CTkToplevel()
    root.geometry("1250x500")
    root.title(f"Add New Architecture")
    root.iconbitmap(f"{os.path.dirname(os.path.abspath(__file__))}\\icons\\icon.ico")
    root.grab_set()

    global address_bits, data_bits, flag_bits, op_codes_bits, ram_registers, cpu_hw_arch, configs, config_names, ins_form, spec_id

    button_frame = CTkFrame(root)

    create_button = CTkButton(button_frame,
                              text = "Create",
                              font = ("Consolas", 14, "bold"),
                              command = lambda: create_arch_files(ins_form, spec_id))

    cancel_button = CTkButton(button_frame,
                              text = "Cancel",
                              font = ("Consolas", 14, "bold"),
                              fg_color = "#ff0000",
                              hover_color = "#8a0101",
                              command = lambda: root.destroy())

    config_frame = CTkFrame(root)

    confirm_button = CTkButton(config_frame,
                            text = "Confirm",
                            font = ("Consolas", 15, "bold"),
                            command = lambda: calculate_parameters(configs))

    main_frame = CTkScrollableFrame(root,
                                    width = 550,
                                    height = 1600)

    label_farme = CTkFrame(main_frame)

    ins_mark_label = CTkLabel(label_farme,
                            width = 180,
                            text = "3 Letter Name\nof Instruction",
                            font = ("Consolas", 13, "bold"))

    ins_rep_label = CTkLabel(label_farme,
                            width = 180,
                            text = "Binary Representation\nof Instruction",
                            font = ("Consolas", 13, "bold"))

    # Functions
    def create_config(entries: list[str]) -> None:
        global configs

        for name in entries:
            configs.append(config_entry(config_frame, name, lenght = 40))

        configs.append(CTkOptionMenu(config_frame, font = ("Consolas", 12, "bold"), values = ["Von Neummann", "Harward"]))

        for item in configs:
            item.pack(side = "left", padx = 2.5, pady = 5)

    def calculate_parameters(configs: list[config_entry | CTkOptionMenu]) -> None:
        global address_bits, data_bits, flag_bits, op_codes_bits, ram_registers, cpu_hw_arch, spec_id

        for item in configs:
            if isinstance(item, config_entry) == True:
                if item._get().isdigit() == True:
                    if item.name == "Address Bits":
                        address_bits = int(item._get())
                    elif item.name == "Data Bits":
                        data_bits = int(item._get())
                    elif item.name == "Flag Bits":
                        flag_bits = int(item._get())
                    elif item.name == "OP Code Bits":
                        op_codes_bits = int(item._get())
                    else:
                        pass
                else:
                    spec_id = item._get().strip()
            else:
                cpu_hw_arch = item.get() if item.get() != None else "Von Neummann"
                    
        ram_registers = 2**address_bits
        create_ins_form(2**op_codes_bits)

    def create_ins_form(size: int = 0) -> None:
        global ins_form

        if len(ins_form) != 0:
            for item in ins_form:
                item.destroy()
            ins_form = []
        else:
            pass

        for i in range(size):
            ins_form.append(ins_entry(main_frame, i + 1))

        label_farme.pack(padx = 5, pady = (10, 5))
        ins_mark_label.pack(side = "left", padx = 15)
        ins_rep_label.pack(side = "left", padx = (0, 130))
        main_frame.pack(pady = 10)

        for item in ins_form:
            item.pack()

    def error_widow(err: str, line: int) -> None:
            messagebox.showerror(title = err,
                                 message = f"Error at line {line}.\n\n"\
                                 "The instruction name must contain 3 letters,\n"\
                                 "allows only binary values\n"\
                                 "and value lenght can't exeed number of OP code bits.")

    def create_arch_files(ins_form: list[ins_entry], spec_id: str = None) -> None:
        global address_bits, data_bits, cpu_hw_arch, op_codes_bits

        ins_table: dict = {}
        no_op_ins: list = []

        for line in ins_form:
            name, value, no_op = line._get()

            if name != "" and value != "":
                try:
                    int(value, 2)
                except ValueError:
                    error_widow("InvalidValueError:", line.id)
                    return None

                if len(value) > op_codes_bits:
                    error_widow("InvalidValueLenghtError:", line.id)
                    return None
                
                if len(name) < 4:
                    ins_table[name.upper()] = value
                else:
                    error_widow("InvalidNameLenghtError:", line.id)
                    return None
                
            if no_op == 1:
                no_op_ins.append(name)

        arch = "vn" if cpu_hw_arch == "Von Neummann" else "h"
        cpu_name = f"{arch}_{address_bits}x{data_bits}" + f" - {spec_id}" if spec_id != "" else ""
        hw_dep = {"arch": f"{address_bits}x{data_bits}", "cpu": arch, "address_bits": address_bits, "data_bits": data_bits, "ram_registers": 2**address_bits, "id": spec_id if spec_id != None else "NA"}

        ins_table["non-op"] = no_op_ins
        ins_table["arch"] = f"{address_bits}x{data_bits}"
        ins_table["cpu"] = arch
        ins_table["id"] = spec_id if spec_id != "" else "NA"

        try:
            os.mkdir(f"{os.path.dirname(os.path.abspath(__file__))}\\files\\{cpu_name}")
        except FileExistsError:
            if spec_id == "":
                messagebox.showerror(title = "FileExistsError:", message = "CPU already exist! For adding new one add 'Specific ID'.")
            return None

        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\files\\{cpu_name}\\instructuins.json", "w") as file:
            json.dump(ins_table, file, indent = 4)

        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\files\\{cpu_name}\\hardware_dependencies.json", "w") as file:
            json.dump(hw_dep, file, indent = 4)

        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\files\\ide\\libraries.json", "r+") as file:
            content: list = json.load(file)
            if cpu_name not in content:
                content.append(cpu_name)
                file.seek(0)
                json.dump(content, file, indent = 4)
            else:
                file.close()


    create_config(config_names)

    root.bind_all("<Return>", lambda event: calculate_parameters(configs) if len(ins_form) == 0 else exec("pass"))

    config_frame.pack()
    confirm_button.pack(side = "left", padx = 5, pady = 5)

    button_frame.pack(padx = 5, pady = (15, 5))
    create_button.pack(side = "left", padx = 5, pady = 5)
    cancel_button.pack(side = "left", padx = 5, pady = 5)

    root.wait_window()