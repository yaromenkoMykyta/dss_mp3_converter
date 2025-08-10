import argparse
from core.converter import convert_dss_folder_to_anything
from core.misc.logger import get_logger

if __name__ == "__main__":
    logger = get_logger(__name__)

    args_parser = argparse.ArgumentParser(
        description="Convert each file in --input folder with the .dss format to another audio format"
        " and save it to --output folder",
    )
    args_parser.add_argument(
        "input", type=str, help="folder where are located .dss files to convert"
    )
    args_parser.add_argument(
        "output", type=str, help="folder to save converted audio files"
    )
    args_parser.add_argument(
        "--format",
        type=str,
        default="wav",
        help="desired output audio format (e.g., 'mp3', 'wav')",
    )

    args = args_parser.parse_args()

    convert_dss_folder_to_anything(args.input, args.output, args.format)
