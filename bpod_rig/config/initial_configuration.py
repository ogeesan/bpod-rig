import datetime
from pathlib import Path

from bpod_rig.config.models.bpod_settings import SystemPaths, SystemSettings


def init_system_configuration(bpod_dir: Path) -> SystemSettings:
    system_paths = SystemPaths(
        creation_date=datetime.date.today(),
        base_dir=bpod_dir,
        data_dir=bpod_dir.joinpath("Data"),
        config_dir=bpod_dir.joinpath("Settings"),
        protocol_dir=bpod_dir.joinpath("Protocols"),
        # log_dir=bpod_dir.joinpath("Logs")
    )

    system_settings = SystemSettings(paths=system_paths)

    return system_settings
