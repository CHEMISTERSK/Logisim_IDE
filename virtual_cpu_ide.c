#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int get_path(char path[]) {

    GetModuleFileNameA(NULL, path, MAX_PATH);

    for (int i = strlen(path); i >= 0; i--) {
        if (path[i] == '\\') {
            path[i] = '\0';
            break;
        }
    }

    return 0;
}

int main() {
    char path[MAX_PATH];
    char bat_cmd[256];
    char py_cmd[256];

    get_path(path);
    sprintf(bat_cmd, "cmd /c \"%s\\setup.bat\"", path);
    sprintf(py_cmd, "cmd /c start pythonw \"%s\\gui.pyw\"", path);

    int return_code = system(bat_cmd);

    if (return_code == 0) system(py_cmd);
    else {
        MessageBoxA(
        NULL,
        "An error occurred!\nPython is not installed or \"customtkinter\" could't be installed.",
        "Fatal Error",
        MB_OK | MB_ICONERROR
        );
    }

    return 0;
}