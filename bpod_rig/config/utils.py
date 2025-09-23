import datetime
import logging
from pathlib import Path

from bpod_rig.config.system_settings import SystemPaths, SystemSettings
from bpod_rig.IO import json_handler

logger = logging.getLogger(__name__)

def init_system_configuration(bpod_dir: Path) -> SystemSettings:
    system_paths = SystemPaths(
        base_dir=bpod_dir,
    )

    system_settings = SystemSettings(paths=system_paths)
    print(system_settings.model_dump_json(indent=2))
    return system_settings

def save_system_configuration(
    system_settings: SystemSettings,
    save_dir_override: Path = None
) -> Path | None:
    """
    Save system_configuration instance to disk as json-formatted text.
    Simultaneously will update the save_datetime field of the models to datetime.now()

    Parameters
    ----------
    system_settings : SystemSettings
        SystemSettings instance to serialize and write to disk
    save_dir_override : Path, optional
        Optional Path to override the default save directory. If not provided,
        system_settings.paths.base_config_dir will be used.

    Returns
    -------
        Path or None

        If the file successfully saves, the path to the saved file is returned
        If the file unsuccessfully saves, None is returned
    """
    logger.debug("Saving system configuration as JSON!")
    save_datetime = datetime.datetime.now()
    system_settings.set_save_time(save_datetime)

    save_dir = system_settings.paths.base_config_dir

    if save_dir_override is not None and save_dir_override.exists():
        save_dir = save_dir_override

    system_settings_json = system_settings.model_dump_json(indent=2)

    return json_handler.write_json(system_settings_json, save_dir, 'config')
