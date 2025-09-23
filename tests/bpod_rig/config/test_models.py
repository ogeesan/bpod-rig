import datetime
import pathlib
import unittest

from pydantic import ValidationError

from bpod_rig.config.base import SettingsMetadata
from bpod_rig.config.system_settings import SystemPaths
from bpod_rig.config.bpod_settings import BpodPaths


class TestMetadataModel(unittest.TestCase):
    def test_default(self):  # NOQA N802
        bm = SettingsMetadata()
        self.assertEqual(bm.creation_date, datetime.date.today())
        self.assertIsNone(bm.save_datetime)
        self.assertEqual(bm.username, "BpodUser")

    def test_good_manual_vals(self):
        past_creation_date = datetime.date(2025, 1, 1)
        past_save_datetime = datetime.datetime(2025, 2, 1)
        new_user = "TestUser"

        bm = SettingsMetadata(
            creation_date=past_creation_date,
            save_datetime=past_save_datetime,
            username=new_user,
        )

        self.assertEqual(bm.creation_date, past_creation_date)
        self.assertEqual(bm.save_datetime, past_save_datetime)
        self.assertEqual(bm.username, new_user)

    def test_validator_failure(self):
        with self.assertRaises(ValidationError):
            future_creation_date = datetime.date(3000, 1, 1)
            SettingsMetadata(creation_date=future_creation_date)
        with self.assertRaises(ValidationError):
            future_save_datetime = datetime.datetime.now() + datetime.timedelta(hours=1)
            SettingsMetadata(save_datetime=future_save_datetime)
        with self.assertRaises(ValidationError):
            too_long_username = "a" * 200
            SettingsMetadata(username=too_long_username)
        with self.assertRaises(ValidationError):
            too_short_username = ""
            SettingsMetadata(username=too_short_username)


class TestSystemPathsModel(unittest.TestCase):
    def setUp(self):
        self.working_dir = pathlib.Path.home()
        self.bpod_dir = self.working_dir.joinpath("Bpod")
        self.config_dir = self.bpod_dir.joinpath("Config")
        self.protocol_dir = self.bpod_dir.joinpath("Protocols")
        self.data_dir = self.bpod_dir.joinpath("Data")
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

    def test_pass_username(self):
        self.bpod_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        self.protocol_dir.mkdir(exist_ok=True)
        self.config_dir.mkdir(exist_ok=True)

        sp = SystemPaths(base_dir=self.bpod_dir, username="valid_username")

        self.assertEqual(sp.metadata.username, "valid_username")

    def test_not_paths(self):
        with self.assertRaises(ValidationError):
            SystemPaths(base_dir=1234321)
        sp = SystemPaths(base_dir="/this/is/a/path")
        self.assertIsInstance(sp.base_dir, pathlib.Path)


class TestBpodPathsModel(unittest.TestCase):
    def setUp(self):
        self.working_dir = pathlib.Path.home()
        self.base_dir = self.working_dir.joinpath("Bpods")

        self.bpod_ID = "1234"
        self.bpod_dir = self.base_dir.joinpath(f"Machine-{self.bpod_ID}")
        self.config_dir = self.bpod_dir.joinpath("Settings")
        self.calibration_dir = self.bpod_dir.joinpath("Calibration")

    def test_ID_validation(self):
        with self.assertRaises(ValidationError):
            BpodPaths(parent_dir=self.bpod_dir)
            # No ID, fails validation
        with self.assertRaises(ValidationError):
            BpodPaths(bpod_id=1234, parent_dir=self.bpod_dir)
            # ID is wrong type
        with self.assertRaises(ValidationError):
            BpodPaths(bpod_id=self.bpod_ID)
            # No parent_dir

        bp = BpodPaths(bpod_id=self.bpod_ID, parent_dir=self.base_dir)
        self.assertEqual(bp.bpod_id, self.bpod_ID)

    def test_default_factory(self):
        bp = BpodPaths(bpod_id=self.bpod_ID, parent_dir=self.base_dir)
        self.assertEqual(bp.unique_bpod_dir, self.bpod_dir)
        self.assertEqual(bp.parent_dir, self.base_dir)
        self.assertEqual(bp.calibration_dir, self.calibration_dir)
        self.assertEqual(bp.settings_dir, self.config_dir)


if __name__ == "__main__":
    unittest.main()
