# # # This source code is subject to the license referenced at
# # # https://github.com/NRLMMD-GEOIPS.

"""Module for setting paths used throughout GeoIPS.

This module sets various directory paths required for GeoIPS.
Setting these variables here keeps geoips code and outputs consolidated.
Eventually, we aim to supplant this method of setting variables with a config file.
`GEOIPS_OUTDIRS` serves as the base reference for all other variables and defaults
to the current directory.

The module defaults to the values set in environment variables for all other variables.
It also provides a function for creating directories.

Functions
---------
- get_env_var: Retrieve an environment variable or a provided default value.
- initialize_paths: Returns a dictionary with GeoIPS directories and variables.
- make_dirs: Create directories if they don't already exist.

Attributes
----------
- PATHS: Dictionary with initialized paths for various GeoIPS directories and URLs.

Environment Variables:
- GEOIPS_OUTDIRS (required): Base output directory for GeoIPS.
"""

import logging
import os
import socket

LOG = logging.getLogger(__name__)


def get_env_var(var_name, default, rstrip_path=True):
    """Retrieve environment variable or provided default, optionally rstrip a '/'.

    Parameters
    ----------
    var_name : str
        The name of the environment variable.
    default : str
        The default value to return if the environment variable is not set.
    rstrip_path : bool, optional
        If True, strip trailing slashes from the returned path (default is True).

    Returns
    -------
    str
        The value of the environment variable or the default value if not set.
    """
    env_value = os.getenv(var_name)
    if env_value:
        if rstrip_path:
            return env_value.rstrip("/")
        else:
            return env_value
    else:
        return default


def initialize_paths():
    """
    Initialize and return a dictionary of paths used throughout GeoIPS.

    Returns
    -------
    dict
        A dictionary containing various paths used by GeoIPS.

    Raises
    ------
    KeyError
        If the required environment variable GEOIPS_OUTDIRS is not set.
    """
    paths = {}

    # Base and Documentation Paths
    paths["BASE_PATH"] = os.path.abspath(
        os.path.join(os.path.dirname(__file__), os.pardir)
    )

    # Output Directories
    try:
        paths["GEOIPS_OUTDIRS"] = os.environ["GEOIPS_OUTDIRS"].rstrip("/")
    except KeyError:
        LOG.warning(
            "GEOIPS_OUTDIRS is not set in your environment. "
            "Defaulting to $HOME/GEOIPS_OUTDIRS as output dir. "
            "Please set GEOIPS_OUTDIRS if you want to write to a "
            "different directory by default."
        )
        try:
            home_dir = os.environ["HOME"]
        except KeyError:
            LOG.error(
                "Could not resolve enviorment variable " "'$HOME', using '/' as default"
            )
            home_dir = "/"
        paths["GEOIPS_OUTDIRS"] = os.path.join(home_dir, "GEOIPS_OUTDIRS")
    paths["GEOIPS_PACKAGES_DIR"] = os.path.abspath(
        os.path.join(paths["BASE_PATH"], os.pardir, os.pardir)
    )
    paths["GEOIPS_BASEDIR"] = get_env_var(
        "GEOIPS_BASEDIR",
        os.path.abspath(os.path.join(paths["GEOIPS_PACKAGES_DIR"], os.pardir)),
    )
    paths["GEOIPS_REBUILD_REGISTRIES"] = get_env_var(
        "GEOIPS_REBUILD_REGISTRIES",
        True,
    )
    # Convert the string to a bool
    if paths["GEOIPS_REBUILD_REGISTRIES"] == "0":
        paths["GEOIPS_REBUILD_REGISTRIES"] = False

    # Identify defaults for global GeoIPS variables.  The actual values for
    # these variables will be set using get_env_var below.
    geoips_global_variable_defaults = {
        # GeoIPS Documentation URL
        "GEOIPS_DOCS_URL": r"https://nrlmmd-geoips.github.io/geoips/",
        # Version
        "GEOIPS_VERS": "0.0.0",
        # Operational User
        "GEOIPS_OPERATIONAL_USER": False,
        # Copyright Information
        "GEOIPS_COPYRIGHT": "NRL-Monterey",
        "GEOIPS_COPYRIGHT_ABBREVIATED": "NRLMRY",
        # Configuration and Queue
        "GEOIPS_RCFILE": "",
        "DEFAULT_QUEUE": None,
        # Computer Identifier
        "BOXNAME": socket.gethostname(),
        # Threshold for image-based output checks.  This will be cast to float below.
        "OUTPUT_CHECKER_THRESHOLD_IMAGE": 0.05,
        # Minimal default
        # "GEOIPS_LOG_FMT_STRING": "%(asctime)s: %(message)s"
        # "GEOIPS_LOG_DATEFMT_STRING": "%d_%H%M%S"
        # More informative default
        "GEOIPS_LOGGING_FMT_STRING": "%(asctime)s %(module)12s.py:%(lineno)-4d "
        "%(levelname)7s: %(message)s",
        "GEOIPS_LOGGING_DATEFMT_STRING": "%d_%H%M%S",
        "GEOIPS_LOGGING_LEVEL": "interactive",
    }

    # Identify the defaults for relative path-based environment variables,
    # these paths default to locations under base paths set above.
    # The actual variables will be set using get_env_var below.
    default_derivative_directory_path_defaults = {
        paths["GEOIPS_BASEDIR"]: {
            "GEOIPS_TESTDATA_DIR": "test_data",
            "GEOIPS_DEPENDENCIES_DIR": "geoips_dependencies",
        },
        paths["GEOIPS_OUTDIRS"]: {
            # Data Output Paths
            "PRESECTORED_DATA_PATH": "preprocessed/sectored",
            "PREREAD_DATA_PATH": "preprocessed/unsectored",
            "PREREGISTERED_DATA_PATH": "preprocessed/registered",
            "PRECALCULATED_DATA_PATH": "preprocessed/algorithms",
            "CLEAN_IMAGERY_PATH": "preprocessed/clean_imagery",
            "ANNOTATED_IMAGERY_PATH": "preprocessed/annotated_imagery",
            "GEOTIFF_IMAGERY_PATH": "preprocessed/geotiff_imagery",
            "FINAL_DATA_PATH": "preprocessed/final",
            "PREGENERATED_GEOLOCATION_PATH": "preprocessed/geolocation",
            # Scratch Directories
            "SCRATCH": "scratch",
            "LOCALSCRATCH": "scratch",
            "SHAREDSCRATCH": "scratch",
            # Log and Data Directories
            "LOGDIR": "logs",
            "GEOIPSDATA": "geoipsdata",
            # Ancillary Data Directories
            "GEOIPS_ANCILDAT_AUTOGEN": "ancildat_autogen",
            "GEOIPS_ANCILDAT": "ancildat",
            # WWW Paths
            "TCWWW": "preprocessed/tcwww",
            "PUBLICWWW": "preprocessed/publicwww",
            "PRIVATEWWW": "preprocessed/privatewww",
            # Tropical Cyclone Paths
            "TC_DECKS_DB": "longterm_files/tc/tc_decks.db",
            "TC_DECKS_DIR": "longterm_files/tc/decks",
        },
        paths["BASE_PATH"]: {
            "TC_TEMPLATE": "plugins/yaml/sectors/dynamic/tc_web_template.yaml",
        },
        paths["GEOIPS_REBUILD_REGISTRIES"]: {
            "GEOIPS_REBUILD_REGISTRIES_TRUE": True,
            "GEOIPS_REBUILD_REGISTRIES_FALSE": False,
        },
    }

    # looping through all the directory-based paths and global variables set above
    # using "get_env_var" function to set the variables to the environment variable
    # specified option (when defined via the first argument)
    # else defaulting to the passed-in default (second argument)
    for key, value in geoips_global_variable_defaults.items():
        paths[key] = get_env_var(key, value)

    for (
        top_directory,
        sub_directories,
    ) in default_derivative_directory_path_defaults.items():
        for key, sub_path in sub_directories.items():
            if "GEOIPS_REBUILD_REGISTRIES" in key:
                paths[key] = get_env_var(key, sub_path, rstrip_path=False)
            else:
                paths[key] = get_env_var(key, os.path.join(top_directory, sub_path))

    # Handling special cases now: home for linux/windows
    if not os.getenv("HOME"):
        # need home drive default for windows
        paths["HOME"] = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH")
    else:
        paths["HOME"] = os.getenv("HOME").rstrip("/")

    # Setting links for WWW Paths
    www_paths = ["TCWWW", "PUBLICWWW", "PRIVATEWWW"]
    for path in www_paths:
        paths[f"{path}_URL"] = get_env_var(f"{path}_URL", paths[path])

    # This needs to be a float
    paths["OUTPUT_CHECKER_THRESHOLD_IMAGE"] = float(
        paths["OUTPUT_CHECKER_THRESHOLD_IMAGE"]
    )

    return paths


def make_dirs(path):
    """Make directories, catching exceptions if directory already exists.

    Parameters
    ----------
    path : str
        Path to directory to create

    Returns
    -------
    str
        Path if successfully created
    """
    LOG.info("Creating directory %s if it doesn't already exist.", path)
    os.makedirs(path, mode=0o755, exist_ok=True)
    return path


# Initialize the PATHS dictionary
PATHS = initialize_paths()
