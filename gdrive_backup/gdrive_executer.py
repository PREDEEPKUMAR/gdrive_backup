from gdrive_backup import search_files as search, \
    identify_files as idf, \
    backup_helper as helper
import os
import time


class BackUpExec:

    def __init__(self, user_type: str, exec_mode: str, backup_scope: int):
        self.user_type = user_type
        self.exec_mode = exec_mode
        self.backup_scope = backup_scope

    def operate_execution(self):
        """Actual Execution Method to prevent security attacks"""
        self.__backup_exec()

    def __folder_selection(self, folder: str) -> str:
        """Based on the Execution Mode (PC or LAP), the Folder is being Selected"""

        if self.exec_mode == 'PC':
            file_name = rf'pc_backup_{folder[:3].lower()}_{str(time.time()).replace(".", "_")}.zip'
            pc_zip_file = os.path.join(TODO_DIR, file_name)
            return pc_zip_file

        elif self.exec_mode == 'LAP':
            file_name = rf'lap_backup_{folder[:3].lower()}_{str(time.time()).replace(".", "_")}.zip'
            lap_zip_file = os.path.join(TODO_DIR, file_name)
            return lap_zip_file

        else:
            return ''

    def __backup_exec(self):
        """Executable Code
        Steps:
        1. Scans for the files on the scoped folder for the specific file extension -> returns files
        2. Identify the Eligible file for Backup from the scanned files
        3. Based on the Execution Mode the Backup Folder is selected
        4. Eligible Files are Copied from Source Loc to backup_todo location
        5. All the files are Zipped in the backup_todo location
        6. Delete all the files except the Zip file in the backup_todo location
        7. Moves the Zip file to BackUp Ready(Done) Location
        8. Backup Starts by GDrive Plugin App
        """
        for folder in BACKUP_FOLDER:
            search_exe = search.SearchFiles(os.path.join(HOME_DIR, folder), FILE_TYPES)
            files = search_exe.search_files()  # Step 1
            idf_exe = idf.IdentifyFiles(files, self.backup_scope)
            idf_files, eligible_count = idf_exe.identify_files()  # Step 2
            if eligible_count:
                zip_file = self.__folder_selection(folder)  # Step 3
                opr_exe = helper.FileOperation(idf_files, TODO_DIR, G_DRIVE_DIR, zip_file, self.user_type)
                opr_exe.operate_copy_files(self.user_type, 'C')  # Step 4
                opr_exe.operate_zip_files(self.user_type, 'Z')  # Step 5
                opr_exe.operate_delete_files(self.user_type, 'D')  # Step 6
                opr_exe.operate_move_files(self.user_type, 'M')  # Step 7


if __name__ == '__main__':

    BACKUP_FOLDER = ['Desktop', 'Downloads', 'Documents', 'Pictures']
    HOME_DIR = os.path.join(os.environ.get('HOMEDRIVE'), (os.environ.get('HOMEPATH')))
    TODO_DIR = os.environ.get('GDrive_TODO')
    G_DRIVE_DIR = os.environ.get('GDrive')
    FILE_TYPES = [
        'xls', 'xlsx', 'pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png', 'txt', 'ppt', 'pptx', 'zip', 'gz', 'rar',
        'xlsm ', 'xltx', 'xltm', 'xlt'
    ]

    if G_DRIVE_DIR and TODO_DIR:
        execute = BackUpExec(user_type='ADMIN', exec_mode='PC', backup_scope=5)
        execute.operate_execution()
    else:
        print('Setup the G-Drive in the Environment First')
