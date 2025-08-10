import argparse
from core.converter import convert_dss_folder
from core.misc.logger import get_logger


if __name__ == "__main__":
    logger = get_logger(__name__)

    args_parser = argparse.ArgumentParser(
        description="Convert each file in --input folder with the .dss format to .mp3"
        " format and save it to --output folder",
    )
    args_parser.add_argument(
        "input", type=str, help="folder wheare are located .dss files to convert"
    )
    args_parser.add_argument(
        "output", type=str, help="folder to save converted .mp3 files"
    )

    args = args_parser.parse_args()

    convert_dss_folder(args.input, args.output)
