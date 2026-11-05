"""Core module for extracting audio and converting YouTube videos to MP3."""

import os
import re
import glob
from typing import Dict, Any, Optional
import yt_dlp

VALID_BITRATES = ["128", "192", "256", "320"]
DEFAULT_BITRATE = "192"


def sanitize_filename(name: str) -> str:
    """Sanitize filename to prevent invalid characters and path traversal."""
    cleaned = re.sub(r'[\\/*?:"<>|]', "", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "audio"


def get_video_info(url: str) -> Dict[str, Any]:
    """Extract metadata for a YouTube URL without downloading media."""
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "extract_flat": False,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        if not info:
            raise ValueError("No se pudo obtener información del video.")

        duration = info.get("duration", 0)
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        if hours > 0:
            duration_formatted = f"{hours}:{minutes:02d}:{seconds:02d}"
        else:
            duration_formatted = f"{minutes}:{seconds:02d}"

        return {
            "id": info.get("id"),
            "title": info.get("title", "Desconocido"),
            "uploader": info.get("uploader", "Desconocido"),
            "duration": duration,
            "duration_formatted": duration_formatted,
            "thumbnail": info.get("thumbnail"),
            "webpage_url": info.get("webpage_url", url),
        }


def download_audio_as_mp3(
    url: str,
    output_dir: str,
    bitrate: str = DEFAULT_BITRATE,
    custom_filename: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Downloads audio from YouTube video and converts it to MP3 format.

    Args:
        url: The YouTube video URL.
        output_dir: Directory where the converted MP3 should be stored.
        bitrate: Audio bitrate (e.g. '128', '192', '320').
        custom_filename: Optional custom base name without extension.

    Returns:
        dict with filepath, filename, title, duration, filesize.
    """
    os.makedirs(output_dir, exist_ok=True)

    if bitrate not in VALID_BITRATES:
        bitrate = DEFAULT_BITRATE

    template = os.path.join(
        output_dir,
        f"{custom_filename or '%(title)s'}.%(ext)s"
    )

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": bitrate,
            },
            {
                "key": "FFmpegMetadata",
                "add_metadata": True,
            },
        ],
        "quiet": True,
        "no_warnings": True,
        "windowsfilenames": True,
        "restrictfilenames": False,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        title = info.get("title", "audio")
        video_id = info.get("id", "audio")

        # Find the generated mp3 file
        expected_name = custom_filename or sanitize_filename(title)
        direct_path = os.path.join(output_dir, f"{expected_name}.mp3")

        final_path = None
        if os.path.exists(direct_path):
            final_path = direct_path
        else:
            # Look for recently created mp3 in output_dir
            mp3_files = glob.glob(os.path.join(output_dir, "*.mp3"))
            if mp3_files:
                # pick the most recently modified file
                final_path = max(mp3_files, key=os.path.getmtime)

        if not final_path or not os.path.exists(final_path):
            raise FileNotFoundError("El archivo MP3 no pudo ser generado.")

        filename = os.path.basename(final_path)
        filesize = os.path.getsize(final_path)

        return {
            "filepath": final_path,
            "filename": filename,
            "title": title,
            "id": video_id,
            "duration": info.get("duration", 0),
            "bitrate": bitrate,
            "filesize": filesize,
        }
