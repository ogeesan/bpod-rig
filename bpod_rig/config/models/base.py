"""Base classes for configuration classes"""

import datetime
from typing import Union
from pydantic import BaseModel, PastDate


class SettingsBase(BaseModel):
    creation_date: Union[datetime.date, PastDate] = datetime.date.today()
    save_date: Union[datetime.date, PastDate] = datetime.date(1970, 1, 1)
    author: str = None  # Username of settings creator


class ModuleBase(SettingsBase):
    name: str
    USB_port: str
