from pathlib import Path

import av
import lameenc

from core.converter.extentions import (
    DssFilesNotFoundException,
    InputFolderNotExistException,
)
from core.misc.get_list_of_dss_files import get_list_of_dss_files
from core.misc.logger import get_logger

# 0 -> best, 9 -> worst
_MP3_QUALITY = 4

# bit rate of mp3 file
_MP3_BITRATE = 192


logger = get_logger(__name__)


def convert_dss_to_mp3_file(input_path: Path, output_path: Path) -> None:
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
    input_dir_path = Path(input_dir).expanduser().resolve()

    if not input_dir_path.exists():
        raise InputFolderNotExistException(
            f"Input folder with absolute path {input_dir} doesn't exist"
        )

    out_dir = Path(output_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    dss_files = get_list_of_dss_files(input_dir_path)

    if not dss_files:
        raise DssFilesNotFoundException(f"No DSS files in {input_dir}")

    logger.info("Found %s files with .dss format in %s", len(dss_files), input_dir)

    for dss_file in dss_files:
        logger.debug("Converting of %s to mp3", dss_file)
        mp3_path = out_dir / (dss_file.stem + ".mp3")
        convert_dss_to_mp3_file(dss_file, mp3_path)
        logger.debug("Converted file saved to %s", mp3_path)
    logger.info(f"Done. MP3s saved to {out_dir}")
