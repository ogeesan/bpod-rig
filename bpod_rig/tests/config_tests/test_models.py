import datetime
import unittest

from bpod_rig.config.models.base import SettingsBase
from bpod_rig.config.models.bpod_settings import BpodPaths
from bpod_rig.config.models.system_settings import SystemPaths, SystemSettings

class TestBaseModel(unittest.TestCase):
    def test_default_BaseModel(self): # NOQA N802
        bm = SettingsBase()
        self.assertEqual(bm.creation_date, datetime.date.today())
        self.assertIsNone(bm.save_date)
        self.assertEqual(bm.username, "BpodUser")



if __name__ == "__main__":
    unittest.main()
