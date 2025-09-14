"""Module implementing the Pydantic models for any system settings"""

from typing import Annotated, Optional
from pydantic import ConfigDict, DirectoryPath, PastDate, UUID4, Field
from bpod_rig.config.models.base import SettingsBase
from bpod_rig.config.models.bpod_settings import BpodPaths

DEFAULT_PROTOCOL_DIR_NAME = "Protocols"
DEFAULT_DATA_DIR_NAME = "Data"
DEFAULT_CONFIG_DIR_NAME = "Config"
DEFAULT_LOG_DIR_NAME = "Logs"

def system_path_factory(data: dict, addition: str):
    """
    Function to dynamically create SytemPath subpaths at validation time.
    Function creates a path in the below form:

    {base_dir}/[addition]

    Path components in {} are retrieved from the dictionary of pre-validated data.

    Parameters
    ----------
    data (dict): Dictionary containing all previously validated fields
    addition (str): Addition to join to the end of the path

    Returns
    -------
    (pathlib.Path): combined path in above form
    """
    if "base_dir" not in data:
        return None

    return data["base_dir"].joinpath(addition)

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
            title="Bpod Protocol Directory",
            description="Local directory where Bpod protocols are stored."
            " The Protocol explorer will list all valid protocols found"
            " in this directory.",
            default_factory=lambda data: system_path_factory(
                data,
                DEFAULT_PROTOCOL_DIR_NAME
            ),
            validate_default=True
        ),
    ] = None

    data_dir: Annotated[
        DirectoryPath,
        Field(
            title="Bpod Data Directory",
            description="Local directory where data from protocol runs are stored.",
            default_factory=lambda data: system_path_factory(
                data, DEFAULT_DATA_DIR_NAME
            ),
            validate_default=True,
        ),
    ] = None

    base_config_dir: Annotated[
        DirectoryPath,
        Field(
            title="Bpod Configuration Directory",
            description="Local directory where Bpod configuration files are stored.",
            default_factory=lambda data: system_path_factory(
                data, DEFAULT_CONFIG_DIR_NAME
            ),
            validate_default=True,
        ),
    ] = None

    log_dir: Annotated[
        Optional[DirectoryPath],
        Field(
            None,
            title="Bpod Log Directory",
            description="Local directory where Bpod logs are stored.",
            # default_factory=lambda data: system_path_factory(
            #     data,
            #     DEFAULT_LOG_DIR_NAME
            # ),
            # validate_default=True,
            # TODO: Add log folder to initial configuration; until then this is optional
        ),
    ] = None

    model_config = ConfigDict()


class SystemSettings(SettingsBase):
    current_version: Annotated[
        str,
        Field(
            title="Current bpod-rig version",
            description="Currently installed version of the bpod-rig repository",
        ),
    ] = "0.0.0"

    last_update_check: Annotated[
        Optional[PastDate],
        Field(
            title="Last update check date and time",
            description="Last date and time that system checked for any updates"
            " compared to the current version",
        ),
    ] = None

    phone_home_id: Annotated[
        Optional[UUID4],
        Field(
            title="System's Unique Phone-Home ID",
            description="UUID4 ID of the current system"
            " for the Bpod phone-home telemetry.",
        ),
    ] = None

    phone_home_opt_in: Annotated[
        bool,
        Field(
            title="Phone-Home Opt-In",
            description="Whether or not the user has opted"
            " in to the phone-home telemetry.",
        ),
    ] = False

    debug: Annotated[
        bool,
        Field(
            False,
            title="Debug Enabled",
            description="Set to True to enable debug information output.",
        ),
    ] = False

    paths: Annotated[
        SystemPaths,
        Field(
            title="System Paths Model",
            description="Model containing validated bpod system paths",
        ),
    ]

    bpod_dirs: Annotated[
        Optional[list[BpodPaths]],
        Field(
            title="All Bpod Paths",
            description="List containing BpodPaths objects that contain"
            " the folder structure for each unique Bpod",
        ),
    ] = None

    model_config = ConfigDict()
