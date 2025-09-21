"""Module implementing the Pydantic models for any Bpod-specific settings"""

from pathlib import Path
from typing import Annotated, Optional
from pydantic import Field
from bpod_rig.config.base import ModelWithMetadata


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

    if "bpod_id" not in data:
        return None

    return data["parent_dir"].joinpath(f"Machine-{data['bpod_id']}", addition)


class BpodPaths(ModelWithMetadata):
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
        Path,
        Field(
            ...,
            title="Bpod directory parent directory",
            description="This is the parent directory to this unique Bpod's directory",
        ),
    ]

    config_dir: Annotated[
        Optional[Path],
        Field(
            title="Bpod Configuration Subdirectory",
            description="Sub directory where Bpod configuration files are "
            "stored for this unique Bpod",
            default_factory=lambda data: bpod_path_factory(data, "Config"),
        ),
    ] = None

    calibration_dir: Annotated[
        Optional[Path],
        Field(
            default_factory=lambda data: bpod_path_factory(data, "Calibration"),
            title="Bpod Configuration Directory",
            description="Local directory where Bpod configuration files are stored.",
        ),
    ] = None

    calibration_files: Annotated[
        Optional[dict[str, Path]],
        Field(
            {},
            title="Bpod calibration files",
            description="Dictionary of calibration files found in the calibration "
                        "directory for this Bpod."
        )
    ] = None

