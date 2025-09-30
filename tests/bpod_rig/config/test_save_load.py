import shutil
import tempfile
import unittest
from pathlib import Path

from bpod_rig.config.system_settings import SystemSettings, SystemPaths
from bpod_rig.config import utils

class TestSave(unittest.TestCase):
    def setUp(self):
        self.bpod_dir = Path(tempfile.mkdtemp())
        self.config_dir = self.bpod_dir.joinpath("Config")
        self.sp = SystemPaths(base_dir=self.bpod_dir)
        self.ss = SystemSettings(paths=self.sp)
        self.full_file_path = self.ss.paths.base_config_dir.joinpath("config.json")


    def test_save(self):
        self.config_dir.mkdir(exist_ok=True)
        save_path = utils.save_system_configuration(self.ss)

        self.assertEqual(save_path, self.full_file_path)
        self.assertTrue(self.full_file_path.exists())

        with open(self.full_file_path, 'r') as fs:
            self.assertEqual(fs.read(), self.ss.model_dump_json(indent=2))

        # On success, the save path is returned

    def test_save_path_override(self):
        self.config_dir.mkdir(exist_ok=True)
        save_path = utils.save_system_configuration(
            self.ss,
            save_dir_override=self.ss.paths.base_dir
        )

        self.assertEqual(save_path, self.full_file_path)
        self.assertTrue(self.full_file_path.exists())

        with open(self.full_file_path, 'r') as fs:
            self.assertEqual(fs.read(), self.ss.model_dump_json(indent=2))

    def test_invalid_default_path(self):
        save_path = utils.save_system_configuration(self.ss)
        self.assertIsNone(save_path)
        # If the default directory doesn't exist this should return None

    def test_invalid_override_path(self):
        invalid_dir = self.bpod_dir.joinpath("InvalidDir")
        save_path = utils.save_system_configuration(
            self.ss,
            save_dir_override=invalid_dir
        )

        self.assertIsNone(save_path)

    def tearDown(self):
        shutil.rmtree(self.bpod_dir, ignore_errors=True)


class TestLoad(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
