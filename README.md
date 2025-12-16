<p align="center">
  <img src="ytmp3/assets/ascii-art-transp.png" alt="ov3 banner" width="254">
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

## Installation

Install via pipx (local project)

```bash
pipx install .
```

Install from GitHub
```bash
pipx install git+https://github.com/OverseerUniverse/ov3
```

# Usage
```bash
ytmp3 <"youtube-url">
```

### Options

| Flag        | Description                             | Default |
|-------------|-----------------------------------------|---------|
| --quality   | Audio bitrate (128, 192, 256, 320)      | 192     |
| --format    | Output audio format                     | mp3     |
| --output    | Output filename template (yt-dlp style) |         |

### Examples
```bash
ytmp3 <URL> --quality 320
```

```bash
ytmp3 <URL> --format flac
```

### Notes

FFmpeg must be installed and discoverable on your PATH

Only download content you own or have permission to download