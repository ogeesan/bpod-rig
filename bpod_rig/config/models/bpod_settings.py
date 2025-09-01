"""Module implementing the base BpodSettings object"""

from typing import Annotated, Optional
from pydantic import ConfigDict, DirectoryPath, PastDate, UUID4
from pydantic.types import StringConstraints, conbytes

from config.models.base import SettingsBase


class SystemPaths(SettingsBase):
    base_dir: DirectoryPath
    protocol_dir: DirectoryPath = '.'
    data_dir: DirectoryPath = '.'
    calibration_dir: DirectoryPath = '.'
    config_dir: DirectoryPath  = '.'  # This might be redundant
    log_dir: DirectoryPath = '.'


class SystemSettings(SettingsBase):
    current_version: str = '0.0.0'
    last_update_check: PastDate = None

    phone_home_id: Optional[UUID4] = None
    phone_home_opt_in: bool = False

    debug: bool = False

    paths: SystemPaths = SystemPaths()
    model_config = ConfigDict()
