"""Module implementing the Pydantic models for any Bpod-specific settings"""


from typing import Annotated, Optional
from pydantic import DirectoryPath, Field, FilePath
from bpod_rig.config.models.base import SettingsBase


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

    calibration_files: Annotated[
        Optional[dict[str, FilePath]],
        Field(
            {},
            title="Bpod calibration files",
            description="Dictionary of calibration files found in the calibration "
                        "directory for this Bpod."
        )
    ]

