import argparse
import sys
from pathlib import Path
from typing import Optional

from yt_dlp import YoutubeDL
from yt_dlp.utils import DownloadError, PostProcessingError

import shutil

QUALITIES = {"128", "192", "256", "320"}
AUDIO_FORMATS = {"mp3", "m4a", "opus", "flac", "wav", "aac"}
VIDEO_FORMATS = {"mp4"}
COMMON_FORMATS = AUDIO_FORMATS | VIDEO_FORMATS

def parse_time_value(value: str) -> int:
    parts = value.strip().split(":")
    if not parts or any(p == "" for p in parts):
        raise ValueError("empty time component")
    if not all(p.isdigit() for p in parts):
        raise ValueError("non-numeric time component")
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
    elif len(parts) == 2:
        hours = 0
        minutes, seconds = map(int, parts)
    elif len(parts) == 1:
        hours = 0
        minutes = 0
        seconds = int(parts[0])
    else:
        raise ValueError("too many time components")
    if minutes >= 60 or seconds >= 60:
        raise ValueError("minutes/seconds must be < 60")
    return hours * 3600 + minutes * 60 + seconds

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
        help="Output format/extension (default: mp3). For video use: mp4.",
    )
    parser.add_argument(
        "--start",
        help="Start time for a snippet (seconds, MM:SS, or HH:MM:SS).",
    )
    parser.add_argument(
        "--end",
        help="End time for a snippet (seconds, MM:SS, or HH:MM:SS).",
    )
    return parser.parse_args()

def build_opts(args: argparse.Namespace, start_seconds: Optional[int], end_seconds: Optional[int]) -> dict:
    # Validate output directory exists (create it if missing)
    out_path = Path(args.output)
    if out_path.parent and not out_path.parent.exists():
        out_path.parent.mkdir(parents=True, exist_ok=True)

    download_sections = None
    if start_seconds is not None or end_seconds is not None:
        start_str = "" if start_seconds is None else str(start_seconds)
        end_str = "" if end_seconds is None else str(end_seconds)
        download_sections = [f"*{start_str}-{end_str}"]

    if args.format in VIDEO_FORMATS:
        opts = {
            "format": "bv*+ba/b",
            "merge_output_format": args.format,
            "outtmpl": args.output,
            "postprocessors": [
                {"key": "FFmpegVideoRemuxer", "preferedformat": args.format}
            ],
            "noplaylist": True,
            "quiet": False,
            "no_warnings": True,
            "restrictfilenames": True,
        }
        if download_sections is not None:
            opts["download_sections"] = download_sections
            opts["force_keyframes_at_cuts"] = True
        return opts

    postprocessors = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": args.format,
        "preferredquality": args.quality,
    }]

    opts = {
        "format": "bestaudio/best",
        "outtmpl": args.output,
        "postprocessors": postprocessors,
        "noplaylist": True,
        "quiet": False,
        "no_warnings": True,
        "restrictfilenames": True,
    }
    if download_sections is not None:
        opts["download_sections"] = download_sections
        opts["force_keyframes_at_cuts"] = True
    return opts

def main() -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("FFmpeg not found. Install it and ensure it is on your PATH.")

    args = parse_args()
    args.format = args.format.lower()
    if not args.url.strip():
        sys.exit("Error: URL is empty.")

    if args.format not in COMMON_FORMATS:
        print(
            f"Warning: '{args.format}' may not be supported; ensure FFmpeg has it.",
            file=sys.stderr,
        )

    if args.format in VIDEO_FORMATS and args.quality != "192":
        print("Note: --quality is ignored for video (mp4) downloads.", file=sys.stderr)

    start_seconds = None
    end_seconds = None
    if args.start or args.end:
        try:
            if args.start:
                start_seconds = parse_time_value(args.start)
            if args.end:
                end_seconds = parse_time_value(args.end)
        except ValueError:
            sys.exit("Error: invalid time format. Use seconds, MM:SS, or HH:MM:SS.")
        if args.start is None and args.end is not None:
            start_seconds = 0
        if start_seconds is not None and end_seconds is not None and end_seconds <= start_seconds:
            sys.exit("Error: --end must be greater than --start.")

    opts = build_opts(args, start_seconds, end_seconds) 

    try:
        with YoutubeDL(opts) as ydl:
            print("Starting download…")
            ydl.download([args.url])
            print("Success: file saved (check the current directory or your --output path)")
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
