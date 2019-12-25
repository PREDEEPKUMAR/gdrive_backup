import os
BACKUP_FOLDER = r'D:\\Backup'


class SearchFiles:

    def __init__(self, folder_path: str):
        """Search Folder Path is initiated here"""
        self.folder_path = folder_path

    def search_files(self) -> dict:
        """Operates the Search Functionality on the Defined Directory"""
        dir_file_info = self._SearchFiles__get_files()
        result = self._SearchFiles__get_file_stats(dir_file_info)
        return result

    def __get_files(self) -> dict:
        """Scans for all the files in the given Directory and creates directory-file info on a Dictionary.
        Sample_Dict_Format = {
            dir_path1 : {file1, file2, file3,...},
            dir_path2 : {file1, file2, file3,...},
            .............
        }
        """
        dir_info = dict()
        for dir_path, directory, filename in os.walk(self.folder_path):
            if dir_path in dir_info.keys():
                dir_info.update(filename)
            else:
                dir_info[dir_path] = filename

        return dir_info

    @staticmethod
    def __get_file_stats(dir_file_info: dict) -> dict:
        """Stats for all the scanned files are created using a dictionary
        Sample_Dict_Format = {
            file_name : {file_path: path, file_size: size, file_cTime: created_time, file_mTime: mod_time},
            file_name1 : {file_path: path, file_size: size, file_cTime: created_time, file_mTime: mod_time},
            .............
        }
        The Stats includes File Path, File Size, File Created Time, File Modified Time
        """
        file_stats = dict()
        for file_path, file_names in dir_file_info.items():
            for name in file_names:
                stats = os.stat(file_path + '\\' + name)
                file_stats[name] = {
                'file_path':file_path,
                 'file_size':stats.st_size, 
                 'file_cTime':stats.st_ctime, 
                 'file_mTime':stats.st_mtime
                }

        return file_stats

    def __str__(self):
        info = f"Class Description: Code to scans all the files/folders/sub-folders on the given directory " \
            f"{self.folder_path}"
        return info