"""main entry point for bpod-rig"""

import logging

from bpod_rig.config import initial_configuration
from bpod_rig.IO import default_setup, json_handler

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def main():
    logger.info("Initializing bpod-rig!")
    # Setup folders. "EMU" is the USB serial port argument for the emulator.
    # create_default_directories() is called later to add folders for each FSM on the PC
    bpod_directory = default_setup.create_default_directories("EMU")

    # Populate this machine's folders with the default config and calibration files.
    default_setup.copy_default_files(bpod_directory, "EMU")

    inital_system_config = initial_configuration.init_system_configuration(
        bpod_directory
    )

if __name__ == "__main__":
    main()
