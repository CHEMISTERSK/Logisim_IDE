#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <shellapi.h>
#include <unistd.h>

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

void directory_check(char *path, char directories[][16]) {
    char full_path[256];

    for (int i = 0; i < 5; i++) {
        sprintf(full_path, "%s\\%s", path, directories[i]);
        if (access(full_path, F_OK) == 0) {
            continue;
        }
        else mkdir(full_path);
    }
}

int files_check(char *path, char files[][30], char *missing_files, int size) {
    char full_path[256];
    int return_code = 0;

    for (int i = 0; i < size; i++) {
        sprintf(full_path, "%s\\%s", path, files[i]);
        if (access(full_path, F_OK) == 0) {
            continue;
        }
        
        else {
            sprintf(missing_files, "%s\t%s\n", missing_files, files[i]);
            return_code = 1;
        }
    }
    return return_code;
}

int main() {
    char path[MAX_PATH];
    char bat_cmd[256];
    char py_cmd[256];
    char missing_files[1024];

    char icons[8][30] = {"icons\\compile_icon.png", "icons\\delete_file.png", "icons\\folder.png", "icons\\icon.ico", "icons\\new_file.png", "icons\\new_folder.png", "icons\\refresh.png", "icons\\rename_file.png"};
    char files[4][30] = {"gui.pyw", "rn_gui.py", "setup.bat", "vcc.pyw"};
    char directories[5][16] = {"files\\ide", "icons", "projects", "outputs\\bin", "outputs\\hex"};

    char x;

    get_path(path);

    printf("Checking files...\n");
    directory_check(path, directories);
    int files_result = files_check(path, files, missing_files, 4);
    int icons_result = files_check(path, icons, missing_files, 8);

    if (files_result == 1 || icons_result == 1) {
        printf("Faild!\nMissingFilesError:\n%s\n", missing_files);
        scanf("%c", &x);
        return 0;
    }
    
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