import logging
from pathlib import Path
from typing import Union

from bpod_rig.config.models.system_settings import SystemSettings

DEFAULT_CONFIG_FILE_NAME = "config.json"

logger = logging.getLogger(__name__)

def save_config_to_disk(
    system_config: SystemSettings,
    override_path: Path = None,
    override_name: str = None
    ) -> Union[Path, None]:
    """
    Serialize and save the Bpod configuration model to disk in json format.

    By default, the configuration file will be saved in
    [BPOD_DIR]/Config/Machine-<machine_id>/Settings/

    By default, the configuration file name is config.json

    Parameters
    ----------
    system_config: bpod_settings.SystemSettings
        Initialized instance of SystemSettings containing configuration values for the
        Bpod system.
    override_path: pathlib.Path, optional
        A path to override the default save directory.
    override_name: str, optional
        A string to override the name of the saved json file

    Returns
    -------
    pathlib.Path
        The final save path with filename and extension.
    """
    filename = DEFAULT_CONFIG_FILE_NAME

    if override_name:
        filename = override_name + ".json"""

    save_dir = system_config.paths.config_dir

    if override_path:
        if not override_path.exists():
            logger.error("%s does not exist!", override_path)
            return None

        save_dir = override_path

    config_save_path = save_dir.joinpath(filename)

    try:
        with open(config_save_path, "w") as json_stream:
                logger.info("Saving configuration to %s", str(config_save_path))
                model_as_json = system_config.model_dump_json(indent=4)
                json_stream.write(model_as_json)
    except (IOError, OSError) as e:
        logger.error("Error opening or writing config file to disk!", e)

    return config_save_path







