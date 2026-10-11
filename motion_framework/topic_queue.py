"""
Persistent Topic Queue Management for CodeMotion.
Stores and tracks extracted reel topics across sessions in data/topics_queue.json.
Maintains state between 'uncompleted' and 'completed' topics, ensuring unselected
topics are never lost.
"""

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any


DEFAULT_QUEUE_PATH = "data/topics_queue.json"


@dataclass
class TopicItem:
    """
    A single reel candidate topic extracted from a podcast or brainstormed.
    """
    id: str
    title: str
    hook_premise: str
    context_summary: str
    source_url: str = ""
    source_title: str = ""
    timestamp: str = ""
    status: str = "uncompleted"  # "uncompleted" | "completed"
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    completed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TopicItem":
        return cls(
            id=data.get("id", str(uuid.uuid4())[:8]),
            title=data.get("title", ""),
            hook_premise=data.get("hook_premise", ""),
            context_summary=data.get("context_summary", ""),
            source_url=data.get("source_url", ""),
            source_title=data.get("source_title", ""),
            timestamp=data.get("timestamp", ""),
            status=data.get("status", "uncompleted"),
            created_at=data.get("created_at", datetime.now(timezone.utc).isoformat()),
            completed_at=data.get("completed_at"),
        )

    def format_option_label(self) -> str:
        """
        Formats a clean, punchy option label suitable for the ask_question UI.
        """
        ts_part = f" [{self.timestamp}]" if self.timestamp else ""
        return f"{self.title}{ts_part}: {self.hook_premise}"


class TopicQueueManager:
    """
    Manages local persistent storage and state tracking of topics.
    """

    def __init__(self, db_path: str = DEFAULT_QUEUE_PATH):
        self.db_path = Path(db_path)
        self._ensure_db_exists()

    def _ensure_db_exists(self) -> None:
        if not self.db_path.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)
            self._write_raw([])

    def _read_raw(self) -> List[Dict[str, Any]]:
        try:
            with open(self.db_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def _write_raw(self, items: List[Dict[str, Any]]) -> None:
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.db_path, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=2, ensure_ascii=False)

    def load_all_topics(self) -> List[TopicItem]:
        raw_items = self._read_raw()
        return [TopicItem.from_dict(item) for item in raw_items]

    def add_topics(self, new_topics: List[TopicItem]) -> int:
        """
        Adds new topics to the queue, avoiding duplicates by title & source_url.
        Returns the count of newly added topics.
        """
        existing = self.load_all_topics()
        existing_signatures = {(t.title.strip().lower(), t.source_url.strip().lower()) for t in existing}

        added_count = 0
        for topic in new_topics:
            sig = (topic.title.strip().lower(), topic.source_url.strip().lower())
            if sig not in existing_signatures:
                existing.append(topic)
                existing_signatures.add(sig)
                added_count += 1

        self._write_raw([t.to_dict() for t in existing])
        return added_count

    def get_uncompleted_topics(self) -> List[TopicItem]:
        """
        Retrieves all topics that have not yet been turned into reels.
        """
        all_topics = self.load_all_topics()
        return [t for t in all_topics if t.status == "uncompleted"]

    def get_completed_topics(self) -> List[TopicItem]:
        """
        Retrieves all topics marked as completed.
        """
        all_topics = self.load_all_topics()
        return [t for t in all_topics if t.status == "completed"]

    def get_topic_by_id(self, topic_id: str) -> Optional[TopicItem]:
        for topic in self.load_all_topics():
            if topic.id == topic_id:
                return topic
        return None

    def mark_topic_completed(self, topic_id: str) -> bool:
        """
        Marks a topic as completed and stamps the completion time.
        Preserves all other topics intact.
        """
        all_topics = self.load_all_topics()
        found = False
        for t in all_topics:
            if t.id == topic_id:
                t.status = "completed"
                t.completed_at = datetime.now(timezone.utc).isoformat()
                found = True
                break

        if found:
            self._write_raw([t.to_dict() for t in all_topics])
        return found

    def mark_topic_by_title_or_option(self, option_text: str) -> Optional[TopicItem]:
        """
        Matches an option text (as selected in ask_question) back to the TopicItem,
        and marks it as completed.
        """
        uncompleted = self.get_uncompleted_topics()
        clean_text = option_text.strip().lower()

        for t in uncompleted:
            # Exact option match or title match
            if t.format_option_label().lower() in clean_text or clean_text in t.format_option_label().lower():
                self.mark_topic_completed(t.id)
                return t
            if t.title.lower() in clean_text or clean_text in t.title.lower():
                self.mark_topic_completed(t.id)
                return t

        return None

    def delete_topic(self, topic_id: str) -> bool:
        all_topics = self.load_all_topics()
        initial_len = len(all_topics)
        filtered = [t for t in all_topics if t.id != topic_id]
        if len(filtered) < initial_len:
            self._write_raw([t.to_dict() for t in filtered])
            return True
        return False

    def clear_queue(self) -> None:
        self._write_raw([])

    def format_options_for_user(self, limit: int = 6) -> List[str]:
        """
        Formats uncompleted topics into a list of strings ready for ask_question options.
        """
        uncompleted = self.get_uncompleted_topics()
        return [t.format_option_label() for t in uncompleted[:limit]]
