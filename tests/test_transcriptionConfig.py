import unittest
import os
import xml.etree.ElementTree as ET
from src.config_file.TranscriptionConfig import TranscriptionConfig


class TestTranscriptionConfig(unittest.TestCase):

    def setUp(self):
        self.file_path = "test_config.xml"
        # Create a test XML configuration file
        with open(self.file_path, "w") as f:
            f.write("<config>\n<key1>value1</key1>\n<key2>value2</key2>\n</config>")
        self.config = TranscriptionConfig(self.file_path)

    def test_get_existing_key(self):
        self.assertEqual(self.config.get("key1"), "value1")

    def test_get_nonexistent_key(self):
        self.assertIsNone(self.config.get("nonexistent_key"))

    def test_set_existing_key(self):
        self.assertTrue(self.config.set("key1", "new_value"))
        self.assertEqual(self.config.get("key1"), "new_value")

    def test_set_new_key(self):
        self.assertTrue(self.config.set("new_key", "new_value"))
        self.assertEqual(self.config.get("new_key"), "new_value")

    def test_set_nonexistent_key(self):
        self.assertFalse(self.config.set("nonexistent_key", "new_value"))

    def test_get_all(self):
        expected = {"key1": "value1", "key2": "value2"}
        self.assertDictEqual(self.config.get_all(), expected)

    def test_delete_existing_key(self):
        self.assertTrue(self.config.delete_key("key1"))
        self.assertIsNone(self.config.get("key1"))

    def test_delete_nonexistent_key(self):
        self.assertFalse(self.config.delete_key("nonexistent_key"))

    def test_create_key(self):
        self.assertTrue(self.config.create_key("new_key", "new_value"))
        self.assertEqual(self.config.get("new_key"), "new_value")

    def tearDown(self):
        # Delete the test XML configuration file
        os.remove(self.file_path)


if __name__ == '__main__':
    unittest.main()
