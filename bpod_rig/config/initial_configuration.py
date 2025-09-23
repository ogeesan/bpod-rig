from pathlib import Path

from config.system_settings import SystemPaths, SystemSettings


def init_system_configuration(bpod_dir: Path) -> SystemSettings:
    system_paths = SystemPaths(
        username="Austin-PC",
        base_dir=bpod_dir,
    )

    system_settings = SystemSettings(username="Austin-PC", paths=system_paths)
    print(system_settings.model_dump_json(indent=2))
    return system_settings
