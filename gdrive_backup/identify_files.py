import datetime as dt


class IdentifyFiles:

    def __init__(self, files: dict, backup_scope: int):
        self.files = files
        self.current_date = dt.date.today()
        self.backup_scope = backup_scope
        self.scoped_date = self.current_date - dt.timedelta(days=self.backup_scope)

    @staticmethod
    def __convert_time(c_time: float):
        """Converts the unix time to Standard Date"""
        return dt.date.fromtimestamp(c_time)

    def __eligible_check(self) -> dict:
        """Checks if a file is eligible for backup by comparing last modified date of file with current date
        Eligibility Flag is added to the existing Dictionary
        Sample_Dict_Format = {
            file_name : {file_path: path, file_size: size, file_cTime: created_time, file_mTime: mod_time, Eligible: v},
            .............
        }
        """
        for name, stats in self.files.items():
            file_date = self.__convert_time(stats.get('file_mTime'))
            if file_date > self.scoped_date:
                stats.setdefault('Eligible', True)
            else:
                stats.setdefault('Eligible', False)

        return self.files

    def identify_files(self) -> tuple:
        """Operates the Identify Functionality on the Scanned Files"""
        result = self.__eligible_check()
        print(f"{len(result)} files have been scanned")
        identified_files = {k: v for k, v in result.items() if v.get('Eligible')}
        print(f"{len(identified_files)} files are eligible for backup")
        return identified_files, len(identified_files)

    def __str__(self):
        info = f"Class Description: Code to check & return the files which are eligible for Backup" \
            f"\nCurrent Date: {self.current_date}" \
            f"\nBackUp Scope Date: {self.scoped_date}\n"
        return info
