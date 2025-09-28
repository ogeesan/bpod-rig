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

    def test_save(self):
        self.config_dir.mkdir(exist_ok=True)
        save_path = utils.save_system_configuration(self.ss)
        full_file_path = self.ss.paths.base_config_dir.joinpath("config.json")

        self.assertEqual(save_path, full_file_path)
        self.assertTrue(full_file_path.exists())
        # On success, the save path is returned

    def test_save_path_override(self):
        self.config_dir.mkdir(exist_ok=True)
        save_path = utils.save_system_configuration(
            self.ss,
            save_dir_override=self.ss.paths.base_dir
        )
        full_file_path = self.ss.paths.base_dir.joinpath("config.json")

        self.assertEqual(save_path, full_file_path)
        self.assertTrue(full_file_path.exists())

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
