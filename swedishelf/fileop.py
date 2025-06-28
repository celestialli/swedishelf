import os

import click
import requests

# Global application identifier variables
APP_NAME = "swedishelf"


def get_app_dir() -> str:
    """Get standard locations for application configuration

    Returns
    -------
    app_dir : str
        The path to the application data directory.
    """
    app_dir = click.get_app_dir(APP_NAME)
    return app_dir


def download_file(
    url: str, filename: str = None, category: str = None, overlay: bool = False
) -> str:
    """Download file to application data directory

    Parameters
    ----------
    url : str
        The URL of the file to be downloaded.
    filename : str, optional
        The filename of the downloaded file. If not specified, will use the
        filename from the URL.
    category : str, optional
        The category of the downloaded file. If specified, will download the
        file to the subdirectory with the same name.
    overlay : bool, optional
        Whether to overlay the downloaded file if it already exists. If False,
        will skip the download if the file already exists.

    Returns
    -------
    file_path : str
        The path to the downloaded file.
    """
    if filename is None:
        filename = os.path.basename(url)
    app_dir = get_app_dir()
    if category is not None and isinstance(category, str):
        os.makedirs(os.path.join(app_dir, category), exist_ok=True)
        file_path = os.path.join(app_dir, category, filename)
    else:
        file_path = os.path.join(app_dir, filename)
    if os.path.exists(file_path):
        if not overlay:
            return file_path

    response = requests.get(url)
    if response.status_code != 200:
        return
    if len(response.content) == 0:
        return
    with open(file_path, "wb") as f:
        f.write(response.content)

    return file_path
