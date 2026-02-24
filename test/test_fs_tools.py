import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pathlib import Path
from src.service.fs_tools import read_file, list_files, write_file, search_in_file

class TestFSTools(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_output")
        self.test_dir.mkdir(exist_ok=True)
        self.test_file = self.test_dir / "test.txt"
        with open(self.test_file, "w", encoding="utf-8") as f:
            f.write("This is a test file for Python search.")

    def tearDown(self):
        import shutil
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)

    def test_read_file(self):
        result = read_file(str(self.test_file))
        self.assertIn("content", result)
        self.assertEqual(result["content"], "This is a test file for Python search.")
        self.assertIn("metadata", result)

    def test_list_files(self):
        # Create another file
        (self.test_dir / "test2.txt").touch()
        files = list_files(str(self.test_dir))
        self.assertEqual(len(files), 2)
        names = [f["name"] for f in files]
        self.assertIn("test.txt", names)

        # Test extension filter
        files_txt = list_files(str(self.test_dir), extension=".txt")
        self.assertEqual(len(files_txt), 2)

        files_pdf = list_files(str(self.test_dir), extension=".pdf")
        self.assertEqual(len(files_pdf), 0)

    def test_write_file(self):
        filepath = str(self.test_dir / "subdir" / "new.txt")
        result = write_file(filepath, "New content")
        self.assertEqual(result["status"], "success")
        self.assertTrue(Path(filepath).exists())
        with open(filepath, "r") as f:
            self.assertEqual(f.read(), "New content")

    def test_search_in_file(self):
        result = search_in_file(str(self.test_file), "Python")
        self.assertEqual(result["matches_count"], 1)
        self.assertEqual(result["matches"][0]["match"], "Python")

        result_fail = search_in_file(str(self.test_file), "Java")
        self.assertEqual(result_fail["matches_count"], 0)

if __name__ == '__main__':
    unittest.main()


