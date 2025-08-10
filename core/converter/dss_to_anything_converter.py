import os
from core.misc import get_logger, get_list_of_dss_files
from core.converter.extentions import (
    InputFolderNotExistException,
    DssFilesNotFoundException,
)
from pathlib import Path
from pydub import AudioSegment

logger = get_logger(__name__)


def convert_dss_file_to_anything(
    input_path: Path, output_path: Path, _format: str
) -> None:
    """
    Converts a DSS (Digital Speech Standard) audio file to another audio format.

    :param input_path: Path to the `.dss` file to convert.
    :param output_path: Path to save the converted audio file.
    :param _format: Desired output audio format (e.g., 'mp3', 'wav').
    :return: None
    """

    logger.info(f"Converting {input_path} to {output_path} in {_format} format.")
    audio = AudioSegment.from_file(input_path, format="dss")
    try:
        audio.export(output_path, format=_format)
    except Exception as e:
        raise RuntimeError(f"Failed to convert {input_path} to {output_path}: {e}")
    logger.info(f"Converted {input_path} to {output_path} in {_format} format.")


def convert_dss_folder_to_anything(
    input_folder: str, output_folder: str, _format: str
) -> None:
    """
    Converts all DSS files in the specified input folder to another audio format
    and saves them in the output folder.

    :param input_folder: Path to the folder containing `.dss` files.
    :param output_folder: Path to the folder to save converted audio files.
    :param _format: Desired output audio format (e.g., 'mp3', 'wav').
    :return: None
    """

    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        raise InputFolderNotExistException(
            f"The input folder {input_folder} does not exist or is not a directory."
        )

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_folder_path = Path(output_folder)

    input_folder_path = Path(input_folder)

    dss_files = get_list_of_dss_files(input_folder_path)

    if not dss_files:
        raise DssFilesNotFoundException(f"No DSS files found in {input_folder}.")

    for dss_file in dss_files:
        output_file = output_folder_path / (dss_file.stem + f".{_format}")
        convert_dss_file_to_anything(dss_file, output_file, _format)
