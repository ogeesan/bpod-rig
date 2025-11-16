import datetime
import logging
from pathlib import Path

from pydantic import ValidationError
from pydantic_core import from_json

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
    system_settings: SystemSettings, save_dir_override: Path | None = None
) -> Path:
    """
    Save system_configuration instance to disk as json-formatted text.

    Simultaneously will update the modified_datetime field of the models to datetime.now()

    Parameters
    ----------
    system_settings : SystemSettings
        SystemSettings instance to serialize and write to disk
    save_dir_override : Path, optional
        Optional Path to override the default save directory. If not provided,
        system_settings.paths.base_config_dir will be used.

    Returns
    -------
        Path
        Path to the saved file is returned
    """
    logger.debug("Saving system configuration as JSON!")
    modified_datetime = datetime.datetime.now()
    system_settings.set_modification_time(modified_datetime)

    if save_dir_override is None:
        if system_settings.paths.base_config_dir is None:
            raise ValueError("system_settings.paths.base_config_dir is None.")
        save_dir = system_settings.paths.base_config_dir
    else:
        save_dir = save_dir_override

    system_settings_json = system_settings.model_dump_json(indent=2)

    return json_handler.write_json(system_settings_json, save_dir, "config")


def load_system_configuration(config_file_path: Path) -> SystemSettings | None:
    """
    Load valid JSON from disk and validate it against the SystemSettings schema.

    If valid JSON is read from disk, parsed, and validated, an initialized
    SystemSettings object is returned.

    Otherwise, any errors are logged and None is returned

    Parameters
    ----------
    config_file_path : pathlib.Path
        Path to the JSON file to load and validate

    Returns
    -------
    SystemSettings or None
        If there are no errors, an instance of the SystemSettings model created from
        the provided configuration file is returned
        Otherwise, if there are any errors reading, parsing, or validating the JSON file

    """
    logger.debug("Attempting to read, parse, and validate: %s", config_file_path)

    file_content_json = json_handler.read_json(config_file_path)

    if file_content_json is not None:
        try:
            return SystemSettings.model_validate(
                from_json(file_content_json, allow_partial=False)
            )
            # If from_json fails to parse the content of the file as JSON, a ValueError
            # is raised. e.g. JSON structure errors
            # If the JSON fails to validate against the SystemSettings schema a
            # ValidationError is raised
        except ValidationError as ve:
            logger.error(
                "JSON loaded from disk is not a valid SystemSettings schema!",
                exc_info=ve,
            )
        except ValueError as ve:
            logger.error("Error parsing JSON loaded from disk!", exc_info=ve)
    else:
        logger.error("No JSON loaded from disk, unable to load system configuration.")

    return None
