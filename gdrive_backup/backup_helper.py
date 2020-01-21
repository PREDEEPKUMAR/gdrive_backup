import os
import shutil
from zipfile import ZipFile
import send2trash as safe_delete


class FileOperation:

    def __init__(self, files: dict, destination: str, g_drive: str, zip_file: str, user_id: str):
        self.destination = destination
        self.files = files
        self.g_drive = g_drive
        self.zip_file = zip_file
        self.user_id = user_id
        # self.file_names = list()
        # additon of few other lines

    def operate_copy_files(self):
        if self.__check_security(self.user_id, 'M'):
            self.__copy_files()
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

    def operate_move_files(self):
        self.__move_files()

    @staticmethod
    def __check_security(user_id, operation):
        """Basic Security Checks"""
        if operation == 'D' and user_id == 'ADMIN':
            return True
        elif (operation in ['M', 'Z']) and (user_id in ['USER', 'ADMIN']):
            return True
        elif user_id == 'TEST':
            return True
        else:
            return False

    def __copy_files(self):
        """Copy the Eligible Files from Source to Backup_ToDO or Backup_Done Directory.
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

    def __move_files(self):
        """Move all the Files from Backup_ToDO to Backup_Done Directory"""
        source_loc = self.destination
        zipped_files = os.listdir(source_loc)
        destiny = self.g_drive
        for name in zipped_files:
            self.__run_log__(os.path.join(source_loc, name), destiny)
            shutil.move(os.path.join(source_loc, name), destiny)

    def __str__(self):
        info = 'Class Description: File Operation class for Move, Copy, Zipping and Deleting Files'
        return info

    @staticmethod
    def __run_log__(source, destiny):
        info = f'Backing up the file {source} to {destiny}'
        print(info)
