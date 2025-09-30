import shutil
import tempfile
import unittest
from pathlib import Path
from bpod_rig.IO import json_handler

JSON_STRING = '{"first_key":{"second_key": "1234"}}'


class TestJSONHandler(unittest.TestCase):
    def setUp(self):
        self.tempdir = Path(tempfile.mkdtemp())

    def test_save(self):
        full_path = self.tempdir.joinpath("temp.json")

        returned_path = json_handler.write_json(
            JSON_STRING,
            self.tempdir,
            "temp"
        )

        self.assertEqual(returned_path, full_path)
        self.assertTrue(full_path.exists())

        with open(full_path, 'r') as fs:
            file_content = fs.read()

        self.assertEqual(file_content, JSON_STRING)

    def test_save_bad_path(self):
        bad_dir = self.tempdir.joinpath("bad_dir")

        returned_path = json_handler.write_json(
            JSON_STRING,
            bad_dir,
            "temp"
        )

        self.assertIsNone(returned_path)

    def test_load(self):
        test_file = self.tempdir.joinpath("config.json")
        with open(test_file, 'w') as tf:
            tf.write(JSON_STRING)

        returned_data = json_handler.read_json(test_file)
        self.assertEqual(returned_data, JSON_STRING)

    def test_load_bad_path(self):
        bad_file = self.tempdir.joinpath("dne.json")

        returned_data = json_handler.read_json(bad_file)
        self.assertIsNone(returned_data)

    def tearDown(self):
        shutil.rmtree(self.tempdir, ignore_errors=True)

if __name__ == "__main__":
    unittest.main()
