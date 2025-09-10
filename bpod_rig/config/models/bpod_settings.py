"""Module implementing the base BpodSettings object"""

from typing import Annotated, Optional, Any
from pydantic import ConfigDict, DirectoryPath, PastDate, UUID4, Field, field_validator
from config.models.base import SettingsBase


def bpod_path_factory(data: dict, addition: str):
    """
    Function to dynamically create BpodPaths subpaths at validation time.
    Function creates a path in the below form:

    {Parent_Dir}/Machine-{Bpod_ID}/[addition]

    Path components in {} are retrieved from the dictionary of pre-validated data.

    Parameters
    ----------
    data (dict): Dictionary containing all previously validated fields
    addition (str): Addition to join to the end of the path

    Returns
    -------
    (pathlib.Path): combined path in above form
    """
    return data["parent_dir"].joinpath(f"Machine-{data['bpod_id']}", addition)


class BpodPaths(SettingsBase):
    bpod_id: Annotated[
        str,
        Field(
            ...,
            title="Bpod ID",
            description="Unique identifier for each Bpod connected to the system;"
            " doubles as the name for the configuration sub directory name"
            " for this Bpod",
        ),
    ]

    parent_dir: Annotated[
        DirectoryPath,
        Field(
            ...,
            title="Bpod directory parent directory",
            description="This is the parent directory to this unique Bpod's directory",
        ),
    ]

    config_dir: Annotated[
        Optional[DirectoryPath],
        Field(
            title="Bpod Configuration Subdirectory",
            description="Sub directory where Bpod configuration files are "
            "stored for this unique Bpod",
            default_factory=lambda data: bpod_path_factory(data, "Config"),
        ),
    ]

    calibration_dir: Annotated[
        Optional[DirectoryPath],
        Field(
            default_factory=lambda data: bpod_path_factory(data, "Calibration"),
            title="Bpod Configuration Directory",
            description="Local directory where Bpod configuration files are stored.",
        ),
    ]


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

    base_config_dir: Annotated[
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
            None,
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
            None,
            title="Last update check date and time",
            description="Last date and time that system checked for any updates"
            " compared to the current version",
        ),
    ]

    phone_home_id: Annotated[
        Optional[UUID4],
        Field(
            None,
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
