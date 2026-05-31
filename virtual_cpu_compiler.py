import json, os, argparse

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

def load(project_name: str = None) -> list[str]:
    try:
        with open(f"{os.path.dirname(os.path.abspath(__file__))}\\projects\\{project_name}.txt", "r") as project_file:
            return project_file.readlines()
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

# Loading Instruction Set and Hardware Dependencies
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
    used_mem = {"bytes": 0, "addr": []}
    current_addr = 0
    functions: dict = {}
    asm_lines = load(file_name)
    values = []
    bin_compiled_code, hex_compiled_code = [], []
    TAB = "    "

# start of compiling cycle
    for line in asm_lines:
        line = (line.strip()).replace(TAB, "")

    # cheking if the line is commentary
        if line[0:2] == '//' or line == "":
            continue

    # checking if line is label (function)
        if line[-1] == ":":
            functions[line[:-1].upper()] = current_addr + 1
            continue

    # compiling assembly code to machine code
        if line[-1] == ";":
            line = line[:-1].strip()

            try:
                operation, operand = line.split(" ")
            except ValueError:
                operation = line
                operand = None

        # cheking if operand is in address range
            if operand != None:
                if int(operand) >= 2**hw_dep["address_bits"] and operation.upper() != "VAL":
                    raise OperandOutOfRangeError(f"\nOperandOutOfRangeError: {operation} {operand}; <- Value must be in range 0-{2**hw_dep['address_bits'] - 1}\nReturn code 1\n")

            # saveing Store (STR) adresses for check if it owerwrites instructions
                if operation.upper() == "STR" and operand not in used_mem["addr"]:
                        used_mem["addr"].append(operand)
            
            # ignoring VAL operations
                if operation.upper() != "VAL":
                    bin_compiled_code.append(f"{ins[operation.upper()]}{format(int(operand), f"0{hw_dep['address_bits']}b")}\n")

        # compileing instructions and labels (functions)
            else:
                try:
                    bin_compiled_code.append(f"{ins[operation.upper()]}{"0" * hw_dep['address_bits']}\n")
                except KeyError:
                    try:
                        bin_compiled_code.append(f"{ins["JMP"]}{format(functions[operation.upper()], f"0{hw_dep['address_bits']}b")}\n")
                    except KeyError:
                        raise SyntaxError(f"\nCode name: \"{operation}\" is not defined!\nReturn code 1\n")
    # syntax check 
        else:
            raise SyntaxError(f"\n{line.replace("\n", "")} <- missing \';\' between instructions\nReturn code 1\n")
        
        if operation.upper() == "VAL":
            break
        
        code_length -= 1
        current_addr += 1

    # checking for memory overflow
        if code_length < 0:
            raise MemoryOverflowError(f"\nMemoryOverflowError:\n\tInsufficient memory to write code\n\tMaximum instructions {len(asm_lines)}/{2**hw_dep['address_bits']}\n\tReturn code 1")
    
# filling rest of memory with 0's
    for _ in range(2**hw_dep['address_bits'] - current_addr):
        bin_compiled_code.append("00000000\n")


    for line in asm_lines:
        line = line.strip()

    # Ingnoring Commentars
        if line[:2] == "//":
            continue

        if line.upper() in ins["non-op"] or line == "":
            continue
        else:
            try:
                operation, operand = line.split(" ")
            except ValueError:
                try:
                    functions[line[:-1].upper()]
                    continue
                except KeyError:
                    try:
                        ins[line[:-1].upper()]
                        continue
                    except KeyError:
                        raise SyntaxError(f"\n{line.replace("\n", " ")} <- missing \';\' between instructions\nReturn code 1\n")
    
    # evaluating VAL expressions
        if operation.upper() == "VAL":
                if int(operand[:-1]) < 2**hw_dep["data_bits"]:
                    values.append(int(operand[:-1]))
                else:
                    raise MemoryOverflowError(f"\nMemoryOverflowError:\n\tMaximum value exceeded! \"{operation} {operand[:-1]};\"\n\tVAL operand must be in range 0-{2**hw_dep['data_bits'] - 1}\n\tReturn code 1\n")
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

# writeing VAL expressions into the memory !
    for i in range(len(values)):
        bin_compiled_code[2**hw_dep["address_bits"] - len(values) + i] = str(format(values[i], f"0{hw_dep['data_bits']}b")) + "\n"

    hex_compiled_code = [format(int(x, 2), f"0{int(hw_dep['data_bits'] / 4)}x") + "\n" for x in bin_compiled_code]

    save(bin_compiled_code, hex_compiled_code, cpu, file_name)
        
    print(f"{warning}\nCode Successfully Compiled!\n\tSize: {len(hex_compiled_code) - hex_compiled_code.count("0" * int(hw_dep["data_bits"] / 4) + "\n")} bytes - Memory Usage {int(((len(hex_compiled_code) - hex_compiled_code.count("0" * int(hw_dep["data_bits"] / 4) + "\n")) / hw_dep["ram_registers"] * 100))}%\n\tReturn code 0\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--file")
    parser.add_argument("--cpu")

    args = parser.parse_args()

    compiler(args.file, args.cpu)