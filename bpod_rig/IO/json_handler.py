import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)


def write_json(json_content: str, save_path: Path, file_name: str) -> Path:
    """Write json-formatted data to disk.

    Data should be provided in a pre-formatted dictionary with indentations/spaces
    included.

    Parameters
    ----------
    json_content: str
        Json-formatted data in a dictionary to write to disk.
    save_path: pathlib.Path
        Directory to write file to.
    file_name: str
        Name of file to save

    Returns
    -------
    pathlib.Path
        The final save path with filename and extension.
    """
    save_dir = save_path

    if not save_dir.exists():
        raise FileNotFoundError(f"Save directory [{save_dir}] does not exist!")

    full_save_path = save_dir.joinpath(file_name).with_suffix(".json")

    full_save_path.write_text(json_content)

    return full_save_path


def read_json(file_path: Path) -> str | None:
    """Read json-formatted data from disk.

    Parameters
    ----------
    file_path: pathlib.Path
        Path with filename and extension of file to read

    Returns
    -------
    str
        Json-formatted data read from provided file path
    """
    if not file_path.exists():
        logger.error("File [%s] does not exist!", file_path)
        return None

    try:
        with open(file_path, "r") as json_stream:
            logger.debug("Reading JSON from %s", str(file_path))
            return json_stream.read()
    except (IOError, OSError) as e:
        logger.error("Error opening and reading file!", exc_info=e)
        return None
