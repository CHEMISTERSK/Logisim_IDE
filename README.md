# Logisim_IDE

Logisim_IDE is a lightweight integrated development environment for creating, editing, and compiling assembly programs for custom virtual CPU architectures.

The project combines a simple graphical editor, a project explorer, an embedded terminal, and a compiler pipeline that translates assembly code into binary and hexadecimal output files.

## Features

- Graphical IDE for editing assembly source files
- Project browser for creating and organizing files and folders
- Built-in terminal for interacting with the workspace
- Support for multiple CPU architectures
- Compilation of assembly code into machine code
- Output generation in both .bin and .hex formats
- Custom instruction sets and hardware dependency definitions stored in JSON files

## Project Structure

- [gui.pyw](gui.pyw) - main graphical application
- [vcc.pyw](vcc.pyw) - compiler backend
- [add_arch_gui.py](add_arch_gui.py) - dialog for adding CPU architectures
- [rn_gui.py](rn_gui.py) - rename utility for project items
- [files/](files/) - configuration and library definitions
- [outputs/](outputs/) - generated binary and hexadecimal outputs
- [projects/](projects/) - example workspace folders
- [User Manuals/](User%20Manuals/) - documentation

## Requirements

- Python 3.x
- Windows environment (the project uses .pyw and Windows-specific file handling)
- Required Python packages:
  - customtkinter
  - pillow

## Installation

1. Clone or download this repository.

2. Run the IDE:

```bash
python gui.pyw
```

Or you can also launch it by double-clicking [logisim_ide.exe](logisim_ide.exe) for starting setup for packages.

## Usage

1. Open the IDE.
2. Create or open a project folder.
3. Create or edit assembly source files.
4. Select a CPU architecture.
5. Compile the source code using the compile button.
6. Review the generated output in [outputs/](outputs/).

## Compiler Notes

The compiler reads instruction definitions and hardware dependency information from the CPU library folders under [files/](files/). Each architecture contains JSON files describing:

- instruction set
- hardware dependencies
- memory layout and addressing details

Compiled output is written into the corresponding folders under [outputs/](outputs/).

## Notes

This project is intended as a lightweight educational or experimental IDE for virtual CPU programming and assembly compilation. It is not a full general-purpose development environment.

## License

This repository does not currently declare a license. If you plan to reuse or redistribute it publicly, consider adding an appropriate open-source license.
