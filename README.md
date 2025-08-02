# DSS-to-MP3 Converter

A lightweight **pure-Python** utility that batch-converts Olympus DSS (Digital Speech Standard) dictation files to high-quality MP3—no external `ffmpeg` or shell calls required.

The script wraps two self-contained binary wheels:

| Library | Purpose | Notes |
|---------|---------|-------|
| **[PyAV](https://github.com/PyAV-Org/PyAV)** | Decodes DSS through the FFmpeg libraries bundled inside the wheel | No system FFmpeg needed |
| **[lameenc](https://github.com/etienne-lms/lameenc)** | Encodes raw PCM to MP3 via an embedded LAME build | Works on Windows / macOS / Linux |

---

## 📃 Requirements

🐍 Python 3.8 – 3.12
* 🪈 Pip-installable wheels:
  ```bash
  pip install av lameenc numpy
  ```
---
## 👨🏻‍🔧 Installation
```bash
git clone https://github.com/yaromenkoMykyta/dss_mp3_converter.git
cd dss-to-mp3

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```
---
## 🏁 Quick start
```bash
python dss_to_mp3_converter.py /path/to/dss_input /path/to/mp3_output
```

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
