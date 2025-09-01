"""Module implementing the base BpodSettings object"""

from typing import Annotated, Optional
from pydantic import ConfigDict, DirectoryPath, PastDate, UUID4, Field
from config.models.base import SettingsBase


class SystemPaths(SettingsBase):
    base_dir: Annotated[
        DirectoryPath,
        Field(
            ...,
            title="Local Bpod Directory",
            description="Local Bpod base directory where other folders are stored."
            " There is not any data directly stored in this directory",
            examples=[
                r"C:\Users\BpodUser\Documents\Bpod",
                "/home/BpodUser/Documents/Bpod",
            ],
        ),
    ]

    protocol_dir: Annotated[
        DirectoryPath,
        Field(
            ...,
            title="Bpod Protocol Directory",
            description="Local directory where Bpod protocols are stored."
            " The Protocol explorer will list all valid protocols found"
            " in this directory.",
        ),
    ]

    data_dir: Annotated[
        DirectoryPath,
        Field(
            ...,
            title="Bpod Data Directory",
            description="Local directory where data from protocol runs are stored.",
        ),
    ]
    calibration_dir: Annotated[
        DirectoryPath,
        Field(
            ...,
            title="Bpod Calibration File Directory",
            description="Local directory where Bpod water"
            " valve calibrations are stored.",
        ),
    ]
    config_dir: Annotated[
        DirectoryPath,
        Field(
            ...,
            title="Bpod Configuration Directory",
            description="Local directory where Bpod configuration files are stored.",
        ),
    ]
    log_dir: Annotated[
        Optional[DirectoryPath],
        Field(
            ...,
            title="Bpod Log Directory",
            description="Local directory where Bpod logs are stored.",
        ),
    ]

    model_config = ConfigDict()



class SystemSettings(SettingsBase):
    current_version: Annotated[
        str,
        Field(
            "0.0.0",
            title="Current bpod-rig version",
            description="Currently installed version of the bpod-rig repository",
        ),
    ]

    last_update_check: Annotated[
        Optional[PastDate],
        Field(
            title="Last update check date and time",
            description="Last date and time that system checked for any updates"
            " compared to the current version",
        ),
    ]

    phone_home_id: Annotated[
        Optional[UUID4],
        Field(
            title="System's Unique Phone-Home ID",
            description="UUID4 ID of the current system"
            " for the Bpod phone-home telemetry.",
        ),
    ]

    phone_home_opt_in: Annotated[
        bool,
        Field(
            False,
            title="Phone-Home Opt-In",
            description="Whether or not the user has opted"
            " in to the phone-home telemetry.",
        ),
    ]

    debug: Annotated[
        bool,
        Field(
            False,
            title="Debug Enabled",
            description="Set to True to enable debug information output.",
        ),
    ]

    paths: Annotated[
        SystemPaths,
        Field(
            title="System Paths Model",
            description="Model containing validated bpod system paths",
        ),
    ]
    model_config = ConfigDict()
