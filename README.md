<p align="center">
  <img src="assets/ascii-art-transp.png" alt="ov3 banner" width="600">
</p>

# ov3

A simple, cross-platform command-line tool to download audio from YouTube videos and save it as MP3 (or other audio formats).

Built as a thin wrapper around `yt-dlp` and `FFmpeg`.

---

## Features

- Download best-quality audio from a YouTube URL
- Convert to MP3 (default) or other FFmpeg-supported audio formats
- Choose audio bitrate
- Clean, simple CLI
- Cross-platform (Windows, macOS, Linux)
- Installed globally via `pipx`

---

## Requirements

- **Python 3.8+**
- **FFmpeg** installed and available on `PATH`
- **pipx**

---

## Install FFmpeg

From the project root:

```bash
pipx install .

Or from GitHub:

```bash
pipx install git+https://github.com/your-username/ytmp3

---

### Usage

```bat
ytmp3 <youtube-url>

Options
Flag	Description	Default
--quality   Audio bitrate (128, 192, 256, 320)  [default: 192]
--format    Output audio format                 [default: mp3]
--output    Output filename template


Examples:

ytmp3 URL --quality 320
ytmp3 URL --format flac

Notes

FFmpeg must be installed and discoverable on PATH

Only download content you own or have permission to download