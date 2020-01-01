import os
import shutil
from zipfile import ZipFile
import send2trash as safe_delete
from functools import update_wrapper, partial


class Security:
    class Check:
        """Decorator Method to Check for Security"""
        def __init__(self, decorated_func):
            """Basic Decorator Options"""
            update_wrapper(self, decorated_func)
            self.decorated_func = decorated_func

        def __get__(self, obj, obj_type):
            return partial(self.__call__, obj)

        def __call__(self, obj, *args, **kwargs):
            """Wrapping the Function to Check for Security and if the Security is Passed, Allowing
            the actual decorator function to execute"""
            if self.__check_security(*args, **kwargs):
                return self.decorated_func(obj, *args, **kwargs)
            else:
                return 'User Denied'

        @staticmethod
        def __check_security(user_id, operation):
            """Basic Security Checks By the Given User ID and Operation Type"""
            # ToDO --> The User Checks can be called from an API
            admin_users = {
                'ADMIN': True,
                'TEST': True
            }
            normal_users = {
                'ADMIN': True,
                'TEST': True,
                'USER': True
            }
            if operation == 'D':
                return admin_users.get(user_id, False)
            elif operation in ['C', 'M', 'Z']:
                return normal_users.get(user_id, False)
            else:
                return False

        def __str__(self):
            info = 'Class Description: Makes the Security Check with the Given User ID and Operation Type'
            return info


class FileOperation:

    def __init__(self, files: dict, destination: str, g_drive: str, zip_file: str, user_id: str):
        self.destination = destination
        self.files = files
        self.g_drive = g_drive
        self.zip_file = zip_file
        self.user_id = user_id
        self.file_names = list()

    @Security.Check
    def operate_copy_files(self, *args):
        """Captures the Eligible File Names"""
        self.file_names = list(map(self.__copy_files, self.files.items()))

    @Security.Check
    def operate_zip_files(self, *args):
        """Zips the File Name"""
        self.__zip_files()

    @Security.Check
    def operate_delete_files(self, *args):
        """Delete's the Files"""
        list(map(self.__delete_files, self.file_names))

    @Security.Check
    def operate_move_files(self, *args):
        """Move the Zip file from one location to another location"""
        self.__move_files(self.zip_file)

    def __copy_files(self, unpacked_args: dict) -> str:
        """Copy the Eligible Files from Source to Backup_ToDO or Backup_Done Directory."""
        name = unpacked_args[0]
        stats = unpacked_args[1]
        source_loc = os.path.join(stats.get('file_path'), name)
        shutil.copy(source_loc, self.destination)
        return name

    def __zip_files(self):
        """Zip all the files available in the Backup_ToDO Directory"""
        with ZipFile(self.zip_file, 'w') as Zip:
            for file in self.file_names:
                Zip.write(os.path.join(self.destination, file))

    def __delete_files(self, file):
        """Delete all the files except the Zip File in the Backup_ToDO Directory"""
        safe_delete.send2trash(os.path.join(self.destination, file))

    def __move_files(self, name):
        """Move all the Files from Backup_ToDO to Backup_Done Directory"""
        source_loc = self.destination
        destiny = self.g_drive
        self.__run_log__(os.path.join(source_loc, name), destiny)
        shutil.move(os.path.join(source_loc, name), destiny)

    @staticmethod
    def __run_log__(source, destiny):
        info = f'Backing up the file {source} to {destiny}'
        print(info)

    def __str__(self):
        info = 'Class Description: File Operation class for Move, Copy, Zipping and Deleting Files'
        return info
