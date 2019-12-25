import os
import shutil
from zipfile import ZipFile

DESTINATION = r'E:\BB\GDrive_Backup\BackUp_Folder\ToDO'
Zip_FILE = r'E:\BB\GDrive_Backup\BackUp_Folder\ToDO\Test1.zip'

class FileOperation:

    def __init__(self, files, destination):
        self.destination = destination
        self.files = files

    def move_files(self):
        for name, stats in self.files.items():
            source_loc = stats['file_path'] + '\\' + name
            shutil.copy(source_loc, self.destination)

    def zip_files(self):
        with ZipFile(Zip_FILE, 'w') as Zip:
            for file in os.listdir(DESTINATION):
                Zip.write(DESTINATION+'\\'+file)


from gdrive_backup import search_files as search, identify_files as idf
SearchTest = search.SearchFiles(search.BACKUP_FOLDER)
files = SearchTest.search_files()
IDFTest = idf.IdentifyFiles(files, idf.BACKUP_SCOPE)
Idffiles = IDFTest.identify_files()
FileTest = FileOperation(Idffiles, DESTINATION)
FileTest.move_files()
FileTest.zip_files()