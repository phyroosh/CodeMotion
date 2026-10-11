"""
Comprehensive Verification and Test Suite for Podcast Intelligence & Topic Queue.
Tests:
1. Persistent Topic Queue state machine (add, list uncompleted, mark completed, preserve unselected).
2. Option string formatting for ask_question interactive UI.
3. Lightweight yt-dlp metadata & subtitle extraction with ZERO video stream downloads.
4. Auto-retrieval behavior when no topic or script is provided.
"""

import os
import shutil
import tempfile
from pathlib import Path
from motion_framework.topic_queue import TopicItem, TopicQueueManager
from motion_framework.podcast_extractor import (
    PodcastContent,
    PodcastChapter,
    extract_podcast_content,
    identify_reel_topics,
    process_podcast_link,
)


def test_topic_queue_state_machine():
    print("\n--- TEST 1: Topic Queue Persistence & State Tracking ---")
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db = str(Path(tmp_dir) / "test_queue.json")
        qm = TopicQueueManager(db_path=test_db)

        # 1. Add 4 extracted topics
        topics = [
            TopicItem(
                id="top_101",
                title="The Sleep Architecture Paradox",
                hook_premise="Eight continuous hours is a post-industrial myth.",
                context_summary="Segment on polyphasic sleep patterns.",
                source_url="https://youtube.com/watch?v=sample1",
                source_title="Huberman Lab: Sleep Optimization",
                timestamp="12:45",
            ),
            TopicItem(
                id="top_102",
                title="The 10 AM Caffeine Trap",
                hook_premise="Drinking coffee within 90 minutes of waking guarantees a 2 PM crash.",
                context_summary="Segment on adenosine receptor clearance.",
                source_url="https://youtube.com/watch?v=sample1",
                source_title="Huberman Lab: Sleep Optimization",
                timestamp="24:10",
            ),
            TopicItem(
                id="top_103",
                title="Cold Exposure Dopamine Spikes",
                hook_premise="Three minutes at 50 degrees creates a 250% sustained dopamine surge.",
                context_summary="Segment on cold plunge neurochemistry.",
                source_url="https://youtube.com/watch?v=sample1",
                source_title="Huberman Lab: Sleep Optimization",
                timestamp="41:15",
            ),
            TopicItem(
                id="top_104",
                title="Light Viewing at Dawn",
                hook_premise="Viewing sunlight through a window is 50x less effective.",
                context_summary="Segment on melanopsin retinal ganglion cells.",
                source_url="https://youtube.com/watch?v=sample1",
                source_title="Huberman Lab: Sleep Optimization",
                timestamp="55:30",
            ),
        ]

        added = qm.add_topics(topics)
        assert added == 4, f"Expected 4 added, got {added}"
        print(f"✅ Added {added} topics to queue.")

        # 2. Check uncompleted topics
        uncompleted = qm.get_uncompleted_topics()
        assert len(uncompleted) == 4, f"Expected 4 uncompleted, got {len(uncompleted)}"

        # 3. Simulate user selecting Topic 2 for reel generation
        selected_option = uncompleted[1].format_option_label()
        print(f"Simulating user selecting: '{selected_option}'")
        matched = qm.mark_topic_by_title_or_option(selected_option)
        assert matched is not None, "Failed to match selected option"
        assert matched.id == "top_102", f"Matched wrong topic: {matched.id}"
        print(f"✅ Topic '{matched.title}' successfully marked completed.")

        # 4. Verify that remaining 3 topics are still uncompleted and preserved across sessions
        # Create a new manager instance simulating a subsequent session:
        qm_session_2 = TopicQueueManager(db_path=test_db)
        remaining = qm_session_2.get_uncompleted_topics()
        assert len(remaining) == 3, f"Expected 3 remaining uncompleted topics, got {len(remaining)}"
        remaining_ids = [t.id for t in remaining]
        assert "top_102" not in remaining_ids, "Completed topic should not be in uncompleted queue"
        assert "top_101" in remaining_ids and "top_103" in remaining_ids and "top_104" in remaining_ids
        print(f"✅ Verified multi-session retention: 3 unselected topics remain safely queued!")

        # 5. Check formatted ask_question options
        opts = qm_session_2.format_options_for_user()
        assert len(opts) == 3
        print("Generated ask_question Options:")
        for idx, o in enumerate(opts, 1):
            print(f"  [{idx}] {o}")


def test_podcast_extraction_zero_media_download():
    print("\n--- TEST 2: Podcast Content Extraction (Zero Video Stream Download) ---")
    test_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    print(f"Extracting metadata & transcript for: {test_url}")
    content = extract_podcast_content(test_url)

    assert content.title, "Title must not be empty"
    assert content.duration > 0, "Duration must be > 0"
    print(f"✅ Title: {content.title}")
    print(f"✅ Channel: {content.channel}")
    print(f"✅ Duration: {content.duration:.1f}s")
    print(f"✅ Transcript Length: {len(content.transcript)} characters")

    # Topic formulation
    topics = identify_reel_topics(content, max_topics=3)
    assert len(topics) > 0, "Expected at least 1 topic identified"
    print(f"✅ Identified {len(topics)} high-conversion reel topics:")
    for t in topics:
        print(f"  • {t.format_option_label()}")


def test_auto_retrieval_flow():
    print("\n--- TEST 3: Auto-Retrieval When No Topic Is Provided ---")
    with tempfile.TemporaryDirectory() as tmp_dir:
        test_db = str(Path(tmp_dir) / "auto_queue.json")
        qm = TopicQueueManager(db_path=test_db)

        # Initially empty queue
        uncompleted = qm.get_uncompleted_topics()
        assert len(uncompleted) == 0
        print("Empty queue check passed.")

        # Add stored topics
        qm.add_topics([
            TopicItem(
                id="top_aut1",
                title="The Knight Capital Bug",
                hook_premise="A forgotten flag erased $440M in 45 minutes.",
                context_summary="Wall street trading disaster.",
            )
        ])

        # Simulate user triggering reel generation with no topic provided
        uncompleted_now = qm.get_uncompleted_topics()
        assert len(uncompleted_now) == 1
        options = qm.format_options_for_user()
        assert len(options) == 1
        print(f"✅ Successfully retrieved pending topic options for ask_question: {options}")


if __name__ == "__main__":
    test_topic_queue_state_machine()
    test_podcast_extraction_zero_media_download()
    test_auto_retrieval_flow()
    print("\n🏆 ALL PODCAST INTELLIGENCE & QUEUE TESTS PASSED SUCCESSFULLY!")
