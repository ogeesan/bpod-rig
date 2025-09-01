"""Module implementing the base BpodSettings object"""

from typing import Annotated, Optional
from pydantic import ConfigDict, DirectoryPath, PastDate, UUID4, Field
from config.models.base import SettingsBase


class SystemPaths(SettingsBase):
    base_dir: Annotated[
        DirectoryPath,
        Field(...,
            title="Local Bpod Directory",
            description="Local Bpod base directory where other folders are stored."
                         " There is not any data directly stored in this directory",
            examples = [r"C:\Users\BpodUser\Documents\Bpod",
                        "/home/BpodUser/Documents/Bpod"]
        )
    ]

    protocol_dir: Annotated[
        DirectoryPath,
        Field(
            '.',
            title="Bpod Protocol Directory",
            description="Local directory where Bpod protocols are stored."
                        " The Protocol explorer will list all valid protocols found"
                        " in this directory."
        )
    ]

    data_dir: Annotated[
        DirectoryPath,
        Field(
            '.',
            title="Bpod Data Directory",
            description="Local directory where data from protocol runs are stored."
        )
    ]
    calibration_dir: Annotated[
        DirectoryPath,
        Field(
            '.',
            title="Bpod Calibration File Directory",
            description="Local directory where Bpod water valve calibrations are stored."
        )
    ]
    config_dir: Annotated[
        DirectoryPath,
        Field(
            '.',
            title="Bpod Configuration Directory",
            description="Local directory where Bpod configuration files are stored."
        )
    ]
    log_dir: Annotated[
        DirectoryPath,
        Field(
            '.',
            title="Bpod Log Directory",
            description="Local directory where Bpod logs are stored."
        )
    ]


class SystemSettings(SettingsBase):
    current_version: str = '0.0.0'
    last_update_check: PastDate = None

    phone_home_id: Optional[UUID4] = None
    phone_home_opt_in: bool = False

    debug: bool = False

    paths: SystemPaths = SystemPaths()
    model_config = ConfigDict()
