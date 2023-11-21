import unittest
import os

from importlib import import_module
from src.utils.IscFileSearch import IscFileSearch
class TestIscFileSearch(unittest.TestCase):
    def setUp(self):
        """
        Method that runs before each test method to set up the test environment
        """
        self.test_dir = "test_dir"
        os.mkdir(self.test_dir)
        self.file1_path = os.path.join(self.test_dir, "file1.txt")
        with open(self.file1_path, "w") as f:
            f.write("This is file 1.")
        self.file2_path = os.path.join(self.test_dir, "file2.txt")
        with open(self.file2_path, "w") as f:
            f.write("This is file 2.")
    
    def tearDown(self):
        """
        Method that runs after each test method to clean up the test environment
        """
        os.remove(self.file1_path)
        os.remove(self.file2_path)
        os.rmdir(self.test_dir)
    
    def test_traverse_directory(self):
        """
        A test method to test the traverse_directory method of the IscFileSearch class
        """
        file_search = IscFileSearch(self.test_dir)
        files = file_search.traverse_directory()
        self.assertEqual(len(files), 2)
        self.assertIn(self.file1_path, files)
        self.assertIn(self.file2_path, files)
    
    def test_get_file(self):
        """
        A test method to test the get_file method of the IscFileSearch class
        """
        file_search = IscFileSearch(self.test_dir)
        file_path = file_search.get_file()
        self.assertIn(file_path, [self.file1_path, self.file2_path])
    
    def test_delete_file(self):
        """
        A test method to test the delete_file method of the IscFileSearch class
        """
        file_search = IscFileSearch(self.test_dir)
        file_search.delete_file(self.file1_path)
        self.assertFalse(os.path.exists(self.file1_path))
    
    def test_rename_file(self):
        """
        A test method to test the rename_file method of the IscFileSearch class
        """
        file_search = IscFileSearch(self.test_dir)
        new_name = "new_file1.txt"
        file_search.rename_file("file1.txt", new_name)
        self.assertFalse(os.path.exists(self.file1_path))
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, new_name)))
    
    def test_get_file_properties(self):
        """
        A test method to test the get_file_properties method of the IscFileSearch class
        """
        file_search = IscFileSearch(self.test_dir)
        file_props = file_search.get_file_properties(self.file1_path)
        self.assertEqual(file_props["file_name"], "file1.txt")
        self.assertEqual(file_props["file_size"], os.stat(self.file1_path).st_size)


if __name__ == '__main__':
    unittest.main()