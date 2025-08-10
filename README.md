# DSS-to-MP3 Converter

A lightweight **pure-Python** utility that batch-converts Olympus DSS (Digital Speech Standard) dictation files to 
 - high-quality MP3—no external `ffmpeg` 
 - or to any other format, but `ffmpeg` should be installed on your system.

## 📃 Requirements

🐍 Python 3.8 – 3.12

---
## 👨🏻‍🔧 Installation
```bash
git clone https://github.com/yaromenkoMykyta/dss_mp3_converter.git
cd dss-to-mp3

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```
If you would like to convert to formats other than MP3, you will also need to install `ffmpeg` on your system.
MacOS users can use [Homebrew](https://brew.sh/):
```bash
brew install ffmpeg
```
---
Linux users can install it via your package manager, e.g.:
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
sudo dnf install ffmpeg  # Fedora/RHEL
sudo pacman -S ffmpeg      # Arch Linux
```
Windows users can download the [FFmpeg binaries](https://ffmpeg.org/download.html) and
add the `bin` directory to your `PATH` environment variable.
```bash
setx PATH "%PATH%;C:\path\to\ffmpeg\bin"
```

## 🏁 Quick start
Use the `convert_dss_to_mp3.py` script to convert `.dss` files to `.mp3` format:
```bash
PYTHONPATH=. python3 scripts/convert_dss_to_mp3.py /path/to/dss_input /path/to/mp3_output
```

If you want to convert to a different format, use the `convert_dss_to_anything.py` script:
```bash
PYTHONPATH=. python3 scripts/convert_dss_to_anything.py /path/to/dss_input /path/to/mp3_output --format wav
```
The `--format` option can be any format supported by `ffmpeg`, such as `wav`, `ogg`, `flac`, etc.
This script will use `ffmpeg` to convert the files, so make sure it is installed on your system.

### Example output:
```pgsql
[2025-08-02 10:03:32,194] INFO: Found 17 files with .dss format in /Users/myk/dictation
[2025-08-02 10:03:33,761] INFO: Done. MP3s saved to /Users/myk/dictation_mp3
```
---
## ⛳️ Flags
| Positional | Description                                           |
| ---------- | ----------------------------------------------------- |
| `input`    | Folder containing `.dss` files (searched recursively) |
| `output`   | Destination folder for the `.mp3` results             |

---
## 👿 Troubleshooting
| Symptom                                | Cause / Fix                                                                                  |
| -------------------------------------- | -------------------------------------------------------------------------------------------- |
| **`Unrecognised container format`**    | Your DSS file might be encrypted or corrupted; PyAV/FFmpeg cannot decode it.                 |
| **`InputFolderNotExistException`**     | The first positional argument must be a *directory*, not a single file.                      |
| **`DssFilesNotFoundException`**        | No `.dss` files were found—check the extension or use the correct folder.                    |
| **Wheel install fails** on arm64 Linux | Ensure `manylinux_2_28` support or compile PyAV with `--enable-libdav` if using musl/alpine. |

---
## 🪪 License
MIT License – see LICENSE for details.

---
# Happy converting! ☕🎧
