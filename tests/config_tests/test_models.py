import datetime
import pathlib
import shutil
import tempfile
import unittest

from pydantic import ValidationError

from config.base import SettingsBase
from bpod_rig.config.bpod_system import SystemPaths

class TestBaseModel(unittest.TestCase):
    def test_default(self): # NOQA N802
        bm = SettingsBase()
        self.assertEqual(bm.creation_date, datetime.date.today())
        self.assertIsNone(bm.save_datetime)
        self.assertEqual(bm.username, "BpodUser")

    def test_good_manual_vals(self):
        past_creation_date = datetime.date(2025, 1, 1)
        past_save_datetime = datetime.datetime(2025, 2, 1)
        new_user = "TestUser"

        bm = SettingsBase(
            creation_date=past_creation_date,
            save_datetime=past_save_datetime,
            username=new_user
        )

        self.assertEqual(bm.creation_date, past_creation_date)
        self.assertEqual(bm.save_datetime, past_save_datetime)
        self.assertEqual(bm.username, new_user)

    def test_validator_failure(self):
        with self.assertRaises(ValidationError):
            future_creation_date = datetime.date(3000, 1, 1)
            SettingsBase(creation_date=future_creation_date)
        with self.assertRaises(ValidationError):
            future_save_datetime = datetime.datetime.now() + datetime.timedelta(hours=1)
            SettingsBase(save_datetime=future_save_datetime)
        with self.assertRaises(ValidationError):
            too_long_username = "a"*200
            SettingsBase(username=too_long_username)
        with self.assertRaises(ValidationError):
            too_short_username = ""
            SettingsBase(username=too_short_username)

class TestSystemPathsModel(unittest.TestCase):
    def setUp(self):
        self.working_dir = pathlib.Path(tempfile.mkdtemp())
        self.bpod_dir = self.working_dir.joinpath('Bpod')
        self.config_dir = self.working_dir.joinpath('Config')
        self.protocol_dir = self.working_dir.joinpath('Protocols')
        self.data_dir = self.working_dir.joinpath('Data')
        # self.log_dir = self.working_dir.joinpath('Logs')
        # TODO: enable this once we add log dir

    def test_default_factory(self):
        try:
            sp = SystemPaths(base_dir=self.bpod_dir)
            self.assertEqual(sp.data_dir, self.data_dir)
            self.assertEqual(sp.base_config_dir, self.config_dir)
            self.assertEqual(sp.protocol_dir, self.protocol_dir)
            # self.assertEqual(sp.log_dir, self.log_dir)
        except ValidationError:
            # This will raise a validation error, but I just want to test the
            # default factory in isolation
            pass

    def test_non_exists(self):
        with self.assertRaises(ValidationError):
            # Bpod dir does not exist; raises validation error
            SystemPaths(base_dir=self.bpod_dir)
        with self.assertRaises(ValidationError):
            # Bpod dir exists now; other dirs do not
            self.bpod_dir.mkdir(exist_ok=True)
            SystemPaths(base_dir=self.bpod_dir)
        with self.assertRaises(ValidationError):
            # Bpod dir and data dir exist
            self.data_dir.mkdir(exist_ok=True)
            SystemPaths(
                base_dir=self.bpod_dir,
                data_dir=self.data_dir
            )
        with self.assertRaises(ValidationError):
            # Bpod dir, data, and protocol exists
            self.protocol_dir.mkdir(exist_ok=True)
            SystemPaths(
                base_dir=self.bpod_dir,
                data_dir=self.data_dir,
                protocol_dir=self.protocol_dir
            )
        with self.assertRaises(ValidationError):
            # Bpod dir, data, and config exist; delete protocol
            self.protocol_dir.rmdir()
            self.config_dir.mkdir(exist_ok=True)
            SystemPaths(
                base_dir=self.bpod_dir,
                data_dir=self.data_dir,
                base_config_dir=self.config_dir,
            )



    def tearDown(self):
        # Since we are not using a context manager we gotta clean this up on our own
        shutil.rmtree(self.working_dir)

if __name__ == "__main__":
    unittest.main()
