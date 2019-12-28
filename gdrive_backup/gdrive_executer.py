from gdrive_backup import search_files as search, \
    identify_files as idf, \
    backup_helper as helper
import os
import time

BACKUP_FOLDER = ['Desktop', 'Downloads', 'Documents', 'Pictures']
HOME_DIR = os.path.join(os.environ['HOMEDRIVE'], (os.environ['HOMEPATH']))


class BackUpExec:

    def __init__(self, user_type: str, home_dir: str, backup_folder: list, exec_mode: str, backup_scope: int):
        self.user_type = user_type
        self.home_dir = home_dir
        self.backup_folder = backup_folder
        self.exec_mode = exec_mode
        self.backup_scope = backup_scope

    def operate_execution(self):
        """Actual Execution Method to prevent security attacks"""
        self.__backup_exec()

    def __folder_selection(self, folder: str) -> tuple:
        """Based on the Execution Mode (PC or LAP), the Folder is being Selected"""
        if self.exec_mode == 'PC':
            pc_zip_file = \
                rf'D:\Predi_BackUp\ToDo\pc_backup_{folder[:3].lower()}_{str(time.time()).replace(".", "_")}.zip'
            pc_destination = r'D:\Predi_BackUp\ToDo'
            return pc_zip_file, pc_destination
        elif self.exec_mode == 'LAP':
            lap_zip_file = \
                rf'E:\BB\GDrive_Backup\BackUp_Folder\ToDO\lap_backup' \
                rf'_{folder[:3].lower()}_{str(time.time()).replace(".", "_")}.zip'
            lap_destination = r'E:\BB\GDrive_Backup\BackUp_Folder\ToDO'
            return lap_zip_file, lap_destination
        else:
            return '', ''

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
        for folder in self.backup_folder:
            search_exe = search.SearchFiles(os.path.join(self.home_dir, folder), search.FILE_TYPES)
            files = search_exe.search_files()  # Step 1
            idf_exe = idf.IdentifyFiles(files, self.backup_scope)
            idf_files, eligible_count = idf_exe.identify_files()  # Step 2
            if eligible_count:
                zip_file, destination = self.__folder_selection(folder)  # Step 3
                opr_exe = helper.FileOperation(idf_files, destination, zip_file, self.user_type)
                opr_exe.operate_copy_files()  # Step 4
                opr_exe.operate_zip_files()  # Step 5
                opr_exe.operate_delete_files()  # Step 6
                opr_exe.operate_move_files()  # Step 7


if __name__ == '__main__':

    execute = BackUpExec(user_type='ADMIN',
                         home_dir=HOME_DIR,
                         backup_folder=BACKUP_FOLDER,
                         exec_mode='PC',
                         backup_scope=5)
    execute.operate_execution()
