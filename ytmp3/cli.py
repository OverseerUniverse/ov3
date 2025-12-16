import argparse
import sys
from pathlib import Path

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, PostProcessingError

import shutil

QUALITIES = {"128", "192", "256", "320"}
COMMON_FORMATS = {"mp3", "m4a", "opus", "flac", "wav", "aac"}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Download YouTube audio and save as MP3 (or other audio formats)."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--quality",
        choices=sorted(QUALITIES),
        default="192",
        help="Audio bitrate in kbps (default: 192)",
    )
    parser.add_argument(
        "--output",
        default="%(title)s.%(ext)s",
        help="Output filename template (yt-dlp style, default: %%(title)s.%%(ext)s)",
    )
    parser.add_argument(
        "--format",
        default="mp3",
        help="Audio format/extension (default: mp3). Must be supported by FFmpeg.",
    )
    return parser.parse_args()

def build_opts(args: argparse.Namespace) -> dict:
    # Validate output directory exists (create it if missing)
    out_path = Path(args.output)
    if out_path.parent and not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    postprocessors = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": args.format,
        "preferredquality": args.quality,
    }]

    return {
        "format": "bestaudio/best",
        "outtmpl": args.output,
        "postprocessors": postprocessors,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": True,
        "restrictfilenames": True,
    }

def main() -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("FFmpeg not found. Install it and ensure it is on your PATH.")

    args = parse_args()
    if not args.url.strip():
        sys.exit("Error: URL is empty.")

    if args.format not in COMMON_FORMATS:
        print(
            f"Warning: '{args.format}' may not be supported; ensure FFmpeg has it.",
            file=sys.stderr,
        )

    opts = build_opts(args) 

    try:
        with YoutubeDL(opts) as ydl:
            print("Starting download…")
            ydl.download([args.url])
            print("Success: audio saved (check the current directory or your --output path)")
    except DownloadError as e:
        sys.exit(f"Download failed: {e}")
    except PostProcessingError as e:
        sys.exit(f"Post-processing failed (is FFmpeg installed?): {e}")
    except KeyboardInterrupt:
        sys.exit("\nDownload cancelled by user.")
    except Exception as e:
        sys.exit(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
