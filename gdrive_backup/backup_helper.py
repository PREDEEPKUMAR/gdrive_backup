import os
import shutil
from zipfile import ZipFile
import time
import send2trash as safe_delete

LAP_DESTINATION = r'E:\BB\GDrive_Backup\BackUp_Folder\ToDO'
PC_DESTINATION = r'D:\Predi_BackUp\ToDo'
LAP_Zip_FILE = rf'E:\BB\GDrive_Backup\BackUp_Folder\ToDO\lap_backup_{int(time.time())}.zip'
PC_Zip_FILE = rf'D:\Predi_BackUp\ToDo\pc_backup_{int(time.time())}.zip'


class FileOperation:

    def __init__(self, files: dict, destination: str, zip_file: str, user_id: str):
        self.destination = destination
        self.files = files
        self.zip_file = zip_file
        self.user_id = user_id
        self.file_names = list()

    def operate_move_files(self):
        if self.__check_security(self.user_id, 'M'):
            self.__move_files()
        else:
            return 'User Denied!'

    def operate_zip_files(self):
        if self.__check_security(self.user_id, 'Z'):
            self.__zip_files()
        else:
            return 'User Denied!'

    def operate_delete_files(self):
        if self.__check_security(self.user_id, 'D'):
            self.__delete_files()
        else:
            return 'User Denied!'

    @staticmethod
    def __check_security(user_id, operation):
        """Basic Security Checks"""
        if operation == 'D' and user_id == 'ADMIN':
            return True
        elif (operation == 'M' or 'Z') and (user_id == 'USER' or 'ADMIN'):
            return True
        else:
            return False

    def __move_files(self):
        """Copy the Eligible Files from Source to Backup_ToDO Directory.
        Also it captures the eligible file names"""
        for name, stats in self.files.items():
            self.file_names.append(name)
            source_loc = os.path.join(stats['file_path'], name)
            shutil.copy(source_loc, self.destination)

    def __zip_files(self):
        """Zip all the files available in the Backup_ToDO Directory"""
        with ZipFile(self.zip_file, 'w') as Zip:
            for file in self.file_names:
                Zip.write(os.path.join(self.destination, file))

    def __delete_files(self):
        """Delete all the files except the Zip File in the Backup_ToDO Directory"""
        for file in self.file_names:
            safe_delete.send2trash(os.path.join(self.destination, file))

    def __str__(self):
        info = 'Class Description: File Operation class for Move, Zipping and Deleting Files'
        return info


from gdrive_backup import search_files as search, identify_files as idf
SearchTest = search.SearchFiles(search.PC_BACKUP_FOLDER, search.FILE_TYPES)
files = SearchTest.search_files()
IDFTest = idf.IdentifyFiles(files, 5)
Idffiles = IDFTest.identify_files()
FileTest = FileOperation(Idffiles, PC_DESTINATION, PC_Zip_FILE, 'USER')
FileTest.operate_move_files()
FileTest.operate_zip_files()
FileTest.operate_delete_files()
