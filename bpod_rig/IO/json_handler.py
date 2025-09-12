import logging
from pathlib import Path
from typing import Union

logger = logging.getLogger(__name__)

def write_json(
    json_content: str,
    save_path: Path = None,
    file_name: str = None
    ) -> Union[Path, None]:
    """
    Write json-formatted data to disk. Data should be provided in a pre-formatted
    dictionary with indentations/spaces included

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

    filename_w_ext = file_name + ".json"
    save_dir = save_path

    if not save_dir.exists():
        logger.error("Save directory [%s] does not exist!", save_dir)
        return None

    full_save_path = save_dir.joinpath(filename_w_ext)

    try:
        with open(full_save_path, "w") as json_stream:
                logger.debug("Saving JSON to %s", str(full_save_path))
                json_stream.write(json_content)
    except (IOError, OSError) as e:
        logger.error("Error opening or writing file to disk!", exc_info=e)

    return full_save_path







