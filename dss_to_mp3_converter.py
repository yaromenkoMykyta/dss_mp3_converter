from pathlib import Path
import av
import lameenc
import logging
import argparse

# logging level
_LOGGER_LEVER = logging.INFO

# extentions of dss files to read
_DSS_FILE_FORMATS = [".dss", ".DSS"]

# 0 -> best, 9 -> worst
_MP3_QUALITY = 4

# bit rate of mp3 file
_MP3_BITRATE = 192

logging.basicConfig(
    format="[%(asctime)s] %(levelname)s: %(message)s", level=_LOGGER_LEVER
)


class DssFilesNotFoundException(Exception):
    pass


class InputFolderNotExistException(Exception):
    pass


def _convert_dss_to_mp3_file(input_path: Path, output_path: Path) -> None:
    """
    converts a DSS (Digital Speech Standard) audio file to an MP3 file.

    uses the `av` library to decode the DSS audio stream, resamples it
    to 16-bit signed PCM format, and encodes the
    audio to MP3 format using `lameenc`. The resulting MP3 data is written to the
    specified output path.


    :param input_path: path to the `.dss` file to convert
    :param output_path: path to save `.mp3` file

    :return `None`
    """
    #  open DSS and prepare encoder
    container = av.open(str(input_path))
    astream = next(s for s in container.streams if s.type == "audio")

    # resample/format-convert to 16-bit signed PCM
    resampler = av.audio.resampler.AudioResampler(
        format="s16", rate=astream.rate, layout=astream.layout.name
    )

    enc = lameenc.Encoder()
    enc.set_bit_rate(_MP3_BITRATE)
    enc.set_in_sample_rate(astream.rate)
    enc.set_channels(astream.channels)

    enc.set_quality(_MP3_QUALITY)

    # decode, resample and encode
    with open(output_path, "wb") as out_f:
        for pkt in container.demux(astream):
            for frame in pkt.decode():
                for res in resampler.resample(frame):
                    # interleaved s16
                    pcm = res.to_ndarray().tobytes()
                    chunk = enc.encode(pcm)
                    if chunk:
                        out_f.write(chunk)

        # final MP3 tail
        out_f.write(enc.flush())
    container.close()


def convert_dss_folder(input_dir: str, output_dir: str) -> None:
    """
    transcode every `*.dss` file in input_dir to MP3 (CBR ≈192 kb/s) and
    write them to `output_dir` with the same basename.

    :param input_dir: input directory with `.dss` files
    :param output_dir: output directory to save `.mp3` files

    :return: `None`
    """
    in_dir = Path(input_dir).expanduser().resolve()

    if not in_dir.exists():
        raise InputFolderNotExistException(
            f"Input folder with absolute path {in_dir} doesn't exist"
        )

    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    dss_files = [f for f in in_dir.rglob("*") if f.suffix.lower() in _DSS_FILE_FORMATS]

    if not dss_files:
        raise DssFilesNotFoundException(f"No DSS files in {in_dir}")

    logging.info("Found %s files with .dss format in %s", len(dss_files), in_dir)

    for dss_file in dss_files:
        logging.debug("Converting of %s to mp3", dss_file)
        mp3_path = out_dir / (dss_file.stem + ".mp3")
        _convert_dss_to_mp3_file(dss_file, mp3_path)
        logging.debug("Converted file saved to %s", mp3_path)
    logging.info(f"Done. MP3s saved to {out_dir}")


if __name__ == "__main__":
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
