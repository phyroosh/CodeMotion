"""
Podcast Content Extractor and Reel Topic Identifier.
Extracts podcast metadata, chapters, and full transcript with ZERO video/audio stream downloads
using yt-dlp --skip-download. Formulates high-conversion reel topics adhering to the
20-Year Veteran Hook standards.
"""

import re
import os
import json
import uuid
import tempfile
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any

from motion_framework.topic_queue import TopicItem, TopicQueueManager
from motion_framework.script_engine import HookArchetype


@dataclass
class PodcastChapter:
    title: str
    start_time: float
    end_time: Optional[float] = None

    @property
    def timestamp_str(self) -> str:
        minutes = int(self.start_time // 60)
        seconds = int(self.start_time % 60)
        hours = int(minutes // 60)
        if hours > 0:
            return f"{hours:02d}:{minutes % 60:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"


@dataclass
class PodcastContent:
    url: str
    title: str
    channel: str
    duration: float
    description: str
    chapters: List[PodcastChapter] = field(default_factory=list)
    transcript: str = ""

    def get_summary_text(self, max_chars: int = 3000) -> str:
        """
        Returns a condensed overview combining title, chapters, and leading transcript.
        """
        lines = [
            f"Title: {self.title}",
            f"Channel: {self.channel}",
            f"Duration: {int(self.duration // 60)} minutes",
            f"Chapters Count: {len(self.chapters)}",
        ]
        if self.chapters:
            lines.append("Key Chapters:")
            for ch in self.chapters[:8]:
                lines.append(f"  - [{ch.timestamp_str}] {ch.title}")

        if self.transcript:
            lines.append("\nTranscript Excerpt:")
            lines.append(self.transcript[:max_chars])

        return "\n".join(lines)


def _clean_vtt_content(vtt_text: str) -> str:
    """
    Strips VTT headers, cue tags, and rolling auto-sub line duplicates.
    """
    lines = vtt_text.splitlines()
    cleaned_tokens: List[str] = []
    seen_recent: List[str] = []

    for line in lines:
        line = line.strip()
        if not line or line.startswith("WEBVTT") or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        # Strip timestamps e.g. 00:00:01.000 --> 00:00:04.000
        if "-->" in line:
            continue
        # Strip inline cue tags like <c> </c> or <00:01:02.000>
        line = re.sub(r"<[^>]+>", "", line).strip()
        if not line:
            continue

        # De-duplicate identical repeated lines caused by YouTube's rolling auto-captions
        if line in seen_recent[-3:]:
            continue

        seen_recent.append(line)
        cleaned_tokens.append(line)

    return " ".join(cleaned_tokens)


def extract_podcast_content(url: str) -> PodcastContent:
    """
    Extracts podcast metadata, chapters, and subtitles directly via yt-dlp.
    Strictly enforces --skip-download to guarantee ZERO media bytes downloaded.
    """
    # 1. Fetch JSON metadata
    cmd_meta = [
        "yt-dlp",
        "--skip-download",
        "--dump-json",
        "--no-warnings",
        url,
    ]
    res = subprocess.run(cmd_meta, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Failed to extract metadata from {url}: {res.stderr[:300]}")

    meta = json.loads(res.stdout)
    title = meta.get("title", "Untitled Podcast")
    channel = meta.get("uploader", meta.get("channel", "Unknown Channel"))
    duration = float(meta.get("duration", 0))
    description = meta.get("description", "")

    # Parse chapters
    chapters: List[PodcastChapter] = []
    raw_chapters = meta.get("chapters") or []
    for rc in raw_chapters:
        chapters.append(PodcastChapter(
            title=rc.get("title", ""),
            start_time=float(rc.get("start_time", 0)),
            end_time=float(rc.get("end_time", 0)) if "end_time" in rc else None,
        ))

    # 2. Extract Subtitles/Captions without downloading video stream
    transcript = ""
    with tempfile.TemporaryDirectory() as temp_dir:
        sub_template = str(Path(temp_dir) / "sub.%(ext)s")
        cmd_sub = [
            "yt-dlp",
            "--skip-download",
            "--write-auto-sub",
            "--write-sub",
            "--sub-lang", "en",
            "--convert-subs", "vtt",
            "--output", sub_template,
            url,
        ]
        sub_res = subprocess.run(cmd_sub, capture_output=True, text=True)
        # Check generated sub files
        sub_files = list(Path(temp_dir).glob("sub*"))
        if sub_files:
            try:
                with open(sub_files[0], "r", encoding="utf-8", errors="ignore") as sf:
                    raw_vtt = sf.read()
                    transcript = _clean_vtt_content(raw_vtt)
            except Exception as e:
                transcript = f"(Subtitles extracted but failed to parse: {e})"

    return PodcastContent(
        url=url,
        title=title,
        channel=channel,
        duration=duration,
        description=description,
        chapters=chapters,
        transcript=transcript,
    )


def identify_reel_topics(content: PodcastContent, max_topics: int = 5) -> List[TopicItem]:
    """
    Identifies high-conversion short-form reel topics from podcast content.
    Prioritizes chapter demarcations and cognitive friction moments,
    formulating them into 20-Year Veteran Hook angles.
    """
    topics: List[TopicItem] = []

    # Heuristic A: If structured chapters exist, leverage chapter hooks
    if content.chapters and len(content.chapters) >= 2:
        for ch in content.chapters:
            title_clean = ch.title.strip()
            # Skip generic intro/outro chapters
            if any(k in title_clean.lower() for k in ["intro", "outro", "sponsor", "welcome", "subscribe"]):
                continue

            hook_premise = _transform_title_to_veteran_hook(title_clean)
            topic_id = f"top_{uuid.uuid4().hex[:6]}"
            topic = TopicItem(
                id=topic_id,
                title=title_clean,
                hook_premise=hook_premise,
                context_summary=f"Segment from '{content.title}' discussing {title_clean}.",
                source_url=content.url,
                source_title=content.title,
                timestamp=ch.timestamp_str,
                status="uncompleted",
            )
            topics.append(topic)
            if len(topics) >= max_topics:
                break

    # Heuristic B: If chapters are sparse or empty, extract from transcript & description
    if len(topics) < max_topics:
        # Scan transcript for high-friction keywords
        text_source = content.transcript if len(content.transcript) > 200 else content.description
        extracted_moments = _extract_friction_moments(text_source, needed=max_topics - len(topics))
        for item in extracted_moments:
            topic_id = f"top_{uuid.uuid4().hex[:6]}"
            topic = TopicItem(
                id=topic_id,
                title=item["title"],
                hook_premise=item["hook"],
                context_summary=item["summary"],
                source_url=content.url,
                source_title=content.title,
                timestamp=item.get("timestamp", ""),
                status="uncompleted",
            )
            topics.append(topic)

    # Heuristic C: Fallback to core podcast premise if everything else is minimal
    if not topics:
        topic_id = f"top_{uuid.uuid4().hex[:6]}"
        topics.append(TopicItem(
            id=topic_id,
            title=content.title,
            hook_premise=_transform_title_to_veteran_hook(content.title),
            context_summary=f"Core takeaway from '{content.title}' ({content.channel}).",
            source_url=content.url,
            source_title=content.title,
            timestamp="00:00",
            status="uncompleted",
        ))

    return topics[:max_topics]


def _transform_title_to_veteran_hook(topic_title: str) -> str:
    """
    Transforms a standard topic title into a high-tension veteran hook statement.
    """
    title_lower = topic_title.lower()
    if "why" in title_lower:
        return f"The real reason {re.sub(r'^why ', '', topic_title, flags=re.I)} isn't what you've been told."
    if "how to" in title_lower:
        return f"Most people fail at {re.sub(r'^how to ', '', topic_title, flags=re.I)} because of one overlooked constraint."
    if "mistake" in title_lower or "failure" in title_lower:
        return f"This single mistake destroys {topic_title} before you even notice."
    if "secret" in title_lower or "truth" in title_lower:
        return f"The uncomfortable truth about {topic_title} that industry veterans rarely say out loud."
    return f"The counter-intuitive reality of {topic_title} that changes how you approach it."


def _extract_friction_moments(text: str, needed: int = 3) -> List[Dict[str, str]]:
    """
    Extracts cognitive friction sentences and transforms them into reel candidate items.
    """
    results: List[Dict[str, str]] = []
    # Key markers of high-friction storytelling
    patterns = [
        (r"(the biggest mistake [^.?!]+[.?!])", "The Fatal Mistake"),
        (r"(nobody talks about [^.?!]+[.?!])", "The Hidden Constraint"),
        (r"(the truth is [^.?!]+[.?!])", "The Inverted Truth"),
        (r"(what actually happens is [^.?!]+[.?!])", "The Underlying Physics"),
        (r"(if you don't [^.?!]+[.?!])", "The Negative Warning"),
    ]

    for pat, label in patterns:
        match = re.search(pat, text, re.IGNORECASE)
        if match:
            sentence = match.group(1).strip()
            if len(sentence) > 15:
                results.append({
                    "title": f"{label}: {sentence[:35]}...",
                    "hook": sentence,
                    "summary": f"Discussion focused on: {sentence}",
                })
        if len(results) >= needed:
            break

    # If pattern search yields fewer, generate based on text sentences
    if len(results) < needed and text:
        sentences = [s.strip() for s in re.split(r"[.?!]", text) if len(s.strip().split()) >= 6]
        for s in sentences[:needed - len(results)]:
            results.append({
                "title": f"Insight: {s[:30]}...",
                "hook": f"Here is why {s.lower()}.",
                "summary": s,
            })

    return results


def process_podcast_link(url: str, queue_db_path: str = "data/topics_queue.json") -> Dict[str, Any]:
    """
    End-to-end pipeline:
    1. Extracts podcast content (zero video download).
    2. Identifies high-conversion reel topics.
    3. Saves them to the local topic queue (persisted across sessions).
    4. Returns summary and formatted options for ask_question.
    """
    content = extract_podcast_content(url)
    topics = identify_reel_topics(content)
    manager = TopicQueueManager(db_path=queue_db_path)
    added_count = manager.add_topics(topics)
    options = manager.format_options_for_user()

    return {
        "podcast_title": content.title,
        "channel": content.channel,
        "duration_sec": content.duration,
        "chapters_found": len(content.chapters),
        "transcript_available": bool(content.transcript and len(content.transcript) > 50),
        "topics_extracted": len(topics),
        "newly_added_to_queue": added_count,
        "total_uncompleted_in_queue": len(manager.get_uncompleted_topics()),
        "options": options,
        "topics": topics,
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Extract podcast content and queue reel topics.")
    parser.add_argument("--url", type=str, required=True, help="YouTube podcast URL")
    args = parser.parse_args()

    result = process_podcast_link(args.url)
    print(f"\n✅ Podcast Processed: '{result['podcast_title']}' ({result['channel']})")
    print(f"Extracted {result['topics_extracted']} topics ({result['newly_added_to_queue']} new added to queue).")
    print(f"Total uncompleted topics in queue: {result['total_uncompleted_in_queue']}")
    print("\nSelectable Options for User:")
    for idx, opt in enumerate(result['options'], 1):
        print(f"  {idx}. {opt}")
