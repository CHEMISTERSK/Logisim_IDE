import json, os

class OperandOutOfRangeError(ValueError):
    pass
class MemoryOverflowError(ValueError):
    pass
class InstructionSetArchitectureMismatchError(ValueError):
    pass
class InstructionOverwriteError(ValueError):
    pass
class CPUModuleNotFoundError(FileNotFoundError):
    pass

def load(project_name: str = None) -> str:
    try:
        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\projects\\{project_name}.txt", "r") as project_file:
            return project_file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"\nFileNotFoundError:\n\tFile named '{project_name}' doesn't exist!\n\tReturn code 1\n")

def load_json(location: str, file_name: str) -> dict[str, str | int]:
    try:
        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\files\\{location}\\{file_name}.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        raise CPUModuleNotFoundError(f"\nCPUModuleNotFoundError:\n\tCPU compileing modul '{location}' doesn't exist or corrupted\n\tReturn code 1\n")

def save(bin_code: list[str], hex_code: list[str], location: str, name: str) -> None:
    os.makedirs(f"{os.path.dirname(os.path.abspath(__file__))}\\outputs\\bin\\{location}", exist_ok = True)
    os.makedirs(f"{os.path.dirname(os.path.abspath(__file__))}\\outputs\\hex\\{location}", exist_ok = True)

    with open(f"{os.path.dirname(os.path.abspath(__file__))}\\outputs\\bin\\{location}\\{name}.bin", "w") as bin_file:
        bin_file.writelines(bin_code)

    with open(f"{os.path.dirname(os.path.abspath(__file__))}\\outputs\\hex\\{location}\\{name}.hex", "w") as hex_file:
        hex_file.writelines(hex_code)

def compiler(file_name: str, cpu: str) -> str:

# Loading Instruction set and Hardware Dependencies
    hw_dep = load_json(cpu, "hardware_dependencies")
    ins = load_json(cpu, "instructions")

# Compatibility Checks
    if (hw_dep["arch"] == ins["arch"]) and (hw_dep["cpu"] == ins["cpu"]):
        pass
    else:
        if (hw_dep["arch"] != ins["arch"]):
            err = [f"Architecture: {ins["arch"]}", f"Architecture: {hw_dep["arch"]}"]
        if (hw_dep["cpu"] != ins["cpu"]):
            err = [f"CPU Type: {ins["cpu"]}", f"CPU Type: {hw_dep["cpu"]}"]
        raise InstructionSetArchitectureMismatchError(f"\nInstructionSetArchitectureMismatchError:\n\tinstructions target '{err[0]}', but hardware dependencies define '{err[1]}'\n\tReturn code 1\n")

# init compiling variables
    code_length = 2**hw_dep["address_bits"]
    used_mem = {"bytes": 0, "add": []}
    asm_code = load(file_name)
    values = []
    bin_compiled_code, hex_compiled_code = [], []
    code_lines = asm_code.split(";")

    def compile_to_machine(code_line: str) -> str:
        operand = ""
        operation = ""

        if code_line.strip().upper() in ins["non-op"]:
            operation = code_line.strip()
        
        else:
            if code_line != "":
                try:
                    operation, operand = code_line.split(" ")
                    if operation.upper() == "STR" and operand not in used_mem["add"]:
                        used_mem["add"].append(operand)
                except ValueError:
                    raise SyntaxError(f"\nSyntaxError:\n\tInvalid instruction syntax: {code_line!r}\n\tReturn code 1\n")
        
        if operation.upper() in ins["non-op"] or operand == "":
            operand = "0"

        if (int(operand) > (2 ** hw_dep["address_bits"]) - 1):
            raise OperandOutOfRangeError(f"\nOperandOutOfRangeError: {operation} {operand}; <- Value must be in range 0-{2**hw_dep['address_bits'] - 1}!\nReturn code 1\n")

        return f"{ins[operation.upper()]}{format(int(operand), f"0{hw_dep['address_bits']}b")}"

    try:
        for line in code_lines:
            line = line.strip()

        # Ingnoreing Commentars
            if line[:2] == "//":
                try:
                    comment, line = line.split("\n")
                except ValueError:
                    raise SyntaxError(f"\n{line.replace("\n", " ")}; <- missing \';\' between instructions\nReturn code 1\n")

        # Syntax Check
            if line.count(" ") > 1:
                raise SyntaxError(f"\n{line.replace("\n", " ")}; <- missing \';\' between instructions\nReturn code 1\n")
            
        # Code Compileing
            if (line != "") and (line[:3].upper() != "VAL"):
                bin_compiled_code.append(compile_to_machine(line) + "\n")
                hex_compiled_code.append(f"{format(int(compile_to_machine(line), 2), f"0{int(hw_dep['data_bits'] / 4)}x")}\n")
                
                if line[:3].upper() == "STR":
                    used_mem["bytes"] += 1

                code_length -= 1

            # code length check
                if code_length < 0:
                    raise MemoryOverflowError(f"\nMemoryOverflowError:\n\tInsufficient memory to write code\n\tMaximum instructions {2**hw_dep['address_bits']}\n\tReturn code 1")
                
    except TypeError:
        raise SyntaxError(f"\n{line.replace("\n", " ")}; <- missing \';\' between instructions\nReturn code 1\n")

    for _ in range(code_length):
        bin_compiled_code.append("0" * hw_dep["data_bits"] + "\n")
        hex_compiled_code.append("0" * int(hw_dep["data_bits"] / 4) + "\n")

# self-modifying check
    for address in used_mem["add"]:
        if bin_compiled_code[int(address)] != ("0" * hw_dep["data_bits"] + "\n"):
            raise InstructionOverwriteError(f"\nInstructionOverwriteError:"
                                            f"\n\tAttempt to write to address {address}, which contains an instruction"
                                            f"\n\tRuntime write would overwrite program code"
                                            f"\n\tReturn code 1\n")

# Compiling Values (VAL)
    for line in code_lines:
        line = line.strip()

    # Ingnoreing Commentars
        if len(line) >= 2 and line[:2] == "//":
            comment, line = line.split("\n")
            line = line.strip()

        if line.upper() in ins["non-op"] or line == "":
            continue
        else:
            try:
                operation, operand = line.split(" ")
            except ValueError:
                raise SyntaxError(f"\n{line.replace("\n", " ")}; <- missing \';\' between instructions\nReturn code 1\n")
    
    # evaluating VAL expressions
        if operation.upper() == "VAL":
                if int(operand) < 2**hw_dep["data_bits"]:
                    values.append(int(operand))
                else:
                    raise MemoryOverflowError(f"\nMemoryOverflowError:\n\tMaximum value exceeded! \"{operation} {operand};\"\n\tVAL operand must be in range 0-{2**hw_dep['data_bits'] - 1}\n\tReturn code 1\n")
# memory checks
    if 0 == code_length - (len(values)):
        warning = f"\nMemoryUsageWarning:"\
                  f"\n\tUsed {len(values)}/{code_length} value slots"\
                  f"\n\tNo spare value slots left - runtime writes will overwrite VAL data\n"

    elif 0 > code_length - (len(values)):
        raise MemoryOverflowError(f"\nMemoryOverflowError:"
                                  f"\n\tUsed {len(values) + len(hex_compiled_code) - hex_compiled_code.count("0" * int(hw_dep["data_bits"] / 4) + "\n")}/{2**hw_dep["address_bits"]} bytes"
                                  f"\n\tToo many VAL instructions - memory exceeded!"
                                  f"\n\tReturn code 1\n")

    else:
        warning = ""

# writeing VAL expressions into the memory
    for i in range(len(values)):
        bin_compiled_code[-(i + 1)] = str(format(values[i], f"0{hw_dep['data_bits']}b")) + "\n"
        hex_compiled_code[-(i + 1)] = str(format(values[i], f"0{int(hw_dep['data_bits'] / 4)}x")) + "\n"
    
    save(bin_compiled_code, hex_compiled_code, cpu, file_name)

    return f"{warning}\nCode Successfully Compiled!\n\tSize: {len(hex_compiled_code) - hex_compiled_code.count("0" * int(hw_dep["data_bits"] / 4) + "\n")} bytes - Memory Usage {int(((len(hex_compiled_code) - hex_compiled_code.count("0" * int(hw_dep["data_bits"] / 4) + "\n")) / hw_dep["ram_registers"] * 100))}%\n\tReturn code 0\n"

if __name__ == "__main__":
    try:
        return_message = compiler("pro", "4x8_vn16")
        print(return_message)
    except Exception as e:
        print(e)