"""
Microsoft Edge Neural Voice Over integration and audio-video synchronization.
Default voice: en-US-AvaMultilingualNeural (Expressive, Warm, Engaging).
"""

import asyncio
import os
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import edge_tts
from mutagen.mp3 import MP3

DEFAULT_VOICE = "en-US-AvaMultilingualNeural"


async def _async_generate_voiceover(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    pitch: str = "+0Hz",
) -> None:
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)


def generate_voiceover(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = "+0%",
    pitch: str = "+0Hz",
) -> float:
    """
    Synthesizes speech using Microsoft Edge Neural Voice and returns audio duration in seconds.
    """
    asyncio.run(_async_generate_voiceover(text, output_path, voice, rate, pitch))
    return get_audio_duration(output_path)


def get_audio_duration(file_path: str) -> float:
    """
    Extracts the exact duration of an audio file in seconds with millisecond precision.
    """
    try:
        audio = MP3(file_path)
        return float(audio.info.length)
    except Exception:
        # Fallback to ffprobe
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            file_path,
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())


def mux_video_audio(video_path: str, audio_path: str, output_path: str) -> str:
    """
    Combines video and audio into a final production MP4 using ffmpeg.
    Guarantees frame-accurate synchronization.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        video_path,
        "-i",
        audio_path,
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        output_path,
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def concatenate_audio_files(audio_files: List[str], output_path: str) -> str:
    """
    Concatenates multiple audio files into a single master audio track using ffmpeg.
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    inputs = []
    filter_complex = []
    for i, f in enumerate(audio_files):
        inputs.extend(["-i", f])
        filter_complex.append(f"[{i}:0]")
    filter_complex_str = "".join(filter_complex) + f"concat=n={len(audio_files)}:v=0:a=1[out]"

    cmd = ["ffmpeg", "-y", *inputs, "-filter_complex", filter_complex_str, "-map", "[out]", output_path]
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


class VoiceoverBeatSheet:
    """
    Helper to script narration beats, synthesize voiceover files,
    and return exact durations for Manim timeline synchronization.
    """

    def __init__(self, voice: str = DEFAULT_VOICE, base_dir: str = "media/audio"):
        self.voice = voice
        self.base_dir = Path(base_dir)
        self.beats: List[Tuple[str, str, float]] = []  # (beat_name, text, duration)

    def add_beat(self, beat_name: str, text: str, rate: str = "+0%") -> float:
        output_file = str(self.base_dir / f"{beat_name}.mp3")
        duration = generate_voiceover(text, output_file, voice=self.voice, rate=rate)
        self.beats.append((beat_name, output_file, duration))
        return duration

    def get_duration(self, beat_name: str) -> float:
        for name, _, duration in self.beats:
            if name == beat_name:
                return duration
        raise KeyError(f"Beat {beat_name} not found")

    def get_file(self, beat_name: str) -> str:
        for name, file_path, _ in self.beats:
            if name == beat_name:
                return file_path
        raise KeyError(f"Beat {beat_name} not found")

    def build_master_track(self, output_path: str = "media/audio/master_voice.mp3") -> str:
        files = [f for _, f, _ in self.beats]
        return concatenate_audio_files(files, output_path)
