from pathlib import Path

DSS_FILE_EXTENSION = '.dss'


def get_list_of_dss_files(directory: Path) -> list:
    """
    Get a list of all DSS files in the specified directory.

    :param directory: Path to the directory to search for DSS files.
    :return: List of paths to DSS files.
    """
    if not directory.is_dir():
        raise NotADirectoryError(f"The path {directory} is not a directory.")

    dss_files: list[Path] = []

    for file in directory.iterdir():
        if file.suffix.lower() == DSS_FILE_EXTENSION:
            dss_files.append(file)

    return dss_files
