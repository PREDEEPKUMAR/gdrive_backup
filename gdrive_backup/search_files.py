import os


class SearchFiles:

    def __init__(self, folder_path: str, file_types: list):
        """Search Folder Path is initiated here"""
        self.folder_path = folder_path
        self.file_types = file_types

    def search_files(self) -> dict:
        """Operates the Search Functionality on the Defined Directory"""
        dir_file_info = self.__get_files()
        result = self.__get_file_stats(dir_file_info)
        return result

    def __get_files(self) -> dict:
        """Scans for all the files in the given Directory and creates directory-file info on a Dictionary.
        Sample_Dict_Format = {
            dir_path1 : {file1, file2, file3,...},
            dir_path2 : {file1, file2, file3,...},
            .............
        }
        Unpacking the path using os.walk Command -- Generator which gives out
        item 0 - Dir Path, item 1 - Directory, item 2 - FileName
        """
        dir_info = dict()
        self.__run_log__()
        gen_folder = list(os.walk(self.folder_path))
        list(filter(lambda i: dir_info.update(i[2]) if i[0] in dir_info else dir_info.setdefault(i[0], i[2]),
                    gen_folder))

        return dir_info

    def __get_file_stats(self, dir_file_info: dict) -> dict:
        """Stats for the given file type extension is only checked.
        Stats for all the files are created using a dictionary
        Sample_Dict_Format = {
            file_name : {file_path: path, file_size: size, file_cTime: created_time, file_mTime: mod_time},
            file_name1 : {file_path: path, file_size: size, file_cTime: created_time, file_mTime: mod_time},
            .............
        }
        The Stats includes File Path, File Size, File Created Time, File Modified Time
        """
        # ToDO -- Check for the best approach to replace the nested for Loop
        file_stats = dict()
        for file_path, file_names in dir_file_info.items():
            for name in file_names:
                for extension in self.file_types:
                    if name.lower().endswith(extension):
                        file = os.path.join(file_path, name)
                        stats = os.stat(file)
                        file_stats[name] = {
                             'file_path': file_path,
                             'file_size': stats.st_size,
                             'file_cTime': stats.st_ctime,
                             'file_mTime': stats.st_mtime
                        }
                    else:
                        pass

        return file_stats

    def __str__(self):
        info = f"Class Description: Code to scans files/folders/sub-folders for given file types {self.file_types}" \
               f" on the given directory {self.folder_path}"
        return info

    def __run_log__(self):
        info = f'_______________________________________________________\n' \
               f'Scanning for Files {self.file_types} on the folder {self.folder_path}'
        print(info)
