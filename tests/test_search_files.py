import unittest
from unittest import mock
from gdrive_backup.search_files import SearchFiles
search = SearchFiles()


class MyTestCase(unittest.TestCase):

    @mock.patch.object(SearchFiles, "_SearchFiles__get_files")
    @mock.patch.object(SearchFiles, "_SearchFiles__get_file_stats")
    def test_search_files(self, mock_stats, mock_get):
        mock_get.return_value = 'Dummy Value'
        mock_stats.return_value = 'Dummy Value'
        result = search.search_files()
        self.assertEqual('Dummy Value', result)

    @mock.patch('os.walk')
    def test__get_files(self, mock_os):
        mock_os.return_value = [['Directory_Path', 'Folder_Name', 'File_Name'], ['Directory_Path', 'Folder_Name', 'File_Name']]
        result = search.search_files()
        self.assertEqual('Value', result)


if __name__ == '__main__':
    unittest.main()
