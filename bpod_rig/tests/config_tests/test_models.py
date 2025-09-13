import datetime
import unittest

from pydantic import ValidationError

from bpod_rig.config.models.base import SettingsBase

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



if __name__ == "__main__":
    unittest.main()
