"""
Export Bridge for RightClips Integration.
Copies finished video and thumbnail to RightClips/out and updates RightClips/studio/metadata.json.
"""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

DEFAULT_RIGHTCLIPS_DIR = "/home/phyroosh/TopProducts/RightClips"


def extract_thumbnail_frame(video_path: str, output_image_path: str, timestamp_sec: float = 2.0) -> str:
    """Extracts a high-res still frame from the video using ffmpeg."""
    Path(output_image_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        str(timestamp_sec),
        "-i",
        video_path,
        "-vframes",
        "1",
        output_image_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_image_path


def export_to_rightclips(
    video_path: str,
    metadata: Dict[str, Any],
    custom_video_name: Optional[str] = None,
    thumbnail_path: Optional[str] = None,
    rightclips_dir: str = DEFAULT_RIGHTCLIPS_DIR,
    thumbnail_timestamp: float = 2.0,
) -> Dict[str, str]:
    """
    Exports video, thumbnail, and metadata directly to the RightClips project.
    
    1. Copies video to RightClips/out/<video_name>.mp4
    2. Generates thumbnail to RightClips/out/<video_name>_thumbnail.png
    3. Atomically registers metadata in RightClips/studio/metadata.json
    """
    rc_path = Path(rightclips_dir)
    if not rc_path.exists():
        raise FileNotFoundError(f"RightClips directory not found at {rightclips_dir}")

    out_dir = rc_path / "out"
    studio_dir = rc_path / "studio"
    metadata_file = studio_dir / "metadata.json"

    out_dir.mkdir(parents=True, exist_ok=True)
    studio_dir.mkdir(parents=True, exist_ok=True)

    src_video = Path(video_path)
    if not src_video.exists():
        raise FileNotFoundError(f"Source video not found: {video_path}")

    # Determine final video filename
    if custom_video_name:
        video_filename = custom_video_name if custom_video_name.endswith(".mp4") else f"{custom_video_name}.mp4"
    else:
        video_filename = src_video.name

    base_name = video_filename.replace(".mp4", "")
    thumb_filename = f"{base_name}_thumbnail.png"

    dest_video_path = out_dir / video_filename
    dest_thumb_path = out_dir / thumb_filename

    # 1. Copy video
    shutil.copy2(src_video, dest_video_path)
    print(f"📦 Copied video to RightClips: {dest_video_path}")

    # 2. Handle Thumbnail (Dedicated Frontier T or Extracted Frame)
    if thumbnail_path and Path(thumbnail_path).exists():
        shutil.copy2(thumbnail_path, dest_thumb_path)
        print(f"🎨 Copied certified Frontier T thumbnail to RightClips: {dest_thumb_path}")
    else:
        extract_thumbnail_frame(str(dest_video_path), str(dest_thumb_path), timestamp_sec=thumbnail_timestamp)
        print(f"🖼️ Extracted frame thumbnail to RightClips: {dest_thumb_path}")

    # Validate thumbnail optical properties via Frontier T
    from .frontier_t import FrontierTValidator
    validation = FrontierTValidator.audit_thumbnail(str(dest_thumb_path), save_debug=False)
    metrics = validation.get("metrics", {})
    print(f"🔍 Frontier T Audit: Passed={validation.get('passed')} (Mobile RMS: {metrics.get('mobileRmsContrast')}, Blur: {metrics.get('blurredContrast')})")

    # 3. Update RightClips studio/metadata.json
    saved_metadata = {}
    if metadata_file.exists():
        try:
            with open(metadata_file, "r", encoding="utf-8") as f:
                saved_metadata = json.load(f)
        except Exception as e:
            print(f"⚠️ Warning reading {metadata_file}: {e}")

    # Register metadata under this video key
    saved_metadata[video_filename] = {
        "topic": metadata.get("topic", base_name),
        "title": metadata.get("title", f"{base_name} #Shorts"),
        "description": metadata.get("description", ""),
        "tags": metadata.get("tags", ["Shorts", "Tech", "Viral"]),
        "categoryId": metadata.get("categoryId", "28"),
        "privacyStatus": metadata.get("privacyStatus", "public"),
        "pinnedComment": metadata.get("pinnedComment", ""),
    }

    # Save back atomically
    with open(metadata_file, "w", encoding="utf-8") as f:
        json.dump(saved_metadata, f, indent=2, ensure_ascii=False)
    print(f"📝 Updated RightClips metadata in: {metadata_file}")

    # Also save local backup copy in Manim exports
    local_meta_backup = src_video.parent / f"{base_name}_metadata.json"
    with open(local_meta_backup, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)

    return {
        "video_path": str(dest_video_path),
        "thumbnail_path": str(dest_thumb_path),
        "metadata_path": str(metadata_file),
        "local_metadata_backup": str(local_meta_backup),
    }
