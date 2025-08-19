"""Module implementing the base BpodSettings object"""

from typing import Annotated, Optional, Union
from pydantic import BaseModel, ConfigDict, DirectoryPath, PastDate
from pydantic.types import StringConstraints, conbytes

class SettingsBase(BaseModel):
    save_date: PastDate
    author: str  # Username of settings creator

class BpodSettings(BaseModel, SettingsBase):
    nickname: Annotated[
        str,
        StringConstraints(
            min_length=1, max_length=32, strip_whitespace=True, to_lower=True
        ),
    ]
    serial: Annotated[
        str,
        StringConstraints(
            min_length=1, max_length=32, strip_whitespace=True, to_upper=True
        ),
    ]
    COM: int
    location: str

    behavior_ports: conbytes(max_length=1) # Can this be more than 8 bits?


class SystemPaths(BaseModel, SettingsBase):
    protocol_dir: DirectoryPath
    data_dir: DirectoryPath
    calibration_dir: DirectoryPath
    config_dir: DirectoryPath  # This might be redundant


class SystemSettings(BaseModel, SettingsBase):
    current_version: str
    last_update_check: Union[None, PastDate]

    phone_home_id: Optional[str]
    phone_home_opt_in: bool = False

    bpods: list[BpodSettings]
    paths: SystemPaths
    model_config = ConfigDict()
