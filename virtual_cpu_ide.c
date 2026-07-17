#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <shellapi.h>

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
    char x;

    get_path(path);

    sprintf(bat_cmd, "cmd /c \"%s\\setup.bat\"", path);
    sprintf(py_cmd, "%s\\gui.pyw", path);

    printf("Starting Setup...\n");
    int return_code = system(bat_cmd);
    printf("Setup Done!\n");

    printf("Init Startup...");
    if (return_code == 0){
        ShellExecute(
            NULL,
            "open",
            py_cmd,
            NULL,
            NULL,
            SW_SHOWNORMAL
        );
    }
    
    else {
        MessageBoxA(
        NULL,
        "An error occurred!\nPython is not installed or \"customtkinter\" could't be installed.",
        "Fatal Error",
        MB_OK | MB_ICONERROR
        );

        printf("Startup Faild!");
        scanf("%c", &x);
    }

    return 0;
}