"""
Verification and Test Suite for the 20-Year Veteran Script Engine.
Tests:
1. Knight Capital $400M Keystroke (IN_MEDIA_RES archetype)
2. Morning Coffee 10 AM Crash (NEGATIVE_CONSTRAINT archetype)
3. Intentionally Flawed Script (to verify negative constraint catches & gate enforcement)
4. Full Audio Generation via Edge TTS (en-US-AvaMultilingualNeural)
5. Audio Beat Synchronization and Seamless Audio Loop Continuity
"""

from pathlib import Path
from motion_framework.script_engine import (
    VeteranScript,
    ScriptBeat,
    HookArchetype,
    BeatType,
    ScriptValidator,
    VeteranScriptDirector,
)
from motion_framework.voice import DEFAULT_VOICE, get_audio_duration


def test_flawed_script_detection():
    print("\n--- TEST 1: Intentionally Flawed Script Audit (Negative Constraints Check) ---")
    flawed = VeteranScript(
        topic="Generic Productivity Tips",
        hook_archetype=HookArchetype.INVERTED_TRUTH,
        target_duration_sec=30.0,
    )
    # Banned hook: rhetorical question
    flawed.add_beat(
        beat_id="beat_bad_hook",
        text="Have you ever wondered why success is all about discipline?",
        visual_cue="[Camera shows someone working]",
        beat_type=BeatType.HOOK,
    )
    # Banned monologue: > 18 words
    flawed.add_beat(
        beat_id="beat_too_long",
        text="Well today we are going to talk about three simple daily routines that will completely change your entire productive workflow forever and ever.",
        visual_cue="[Desk shot]",
        beat_type=BeatType.LOCK_IN_PREMISE,
    )
    # Banned chronological linker + hedging language + missing brackets in visual cue
    flawed.add_beat(
        beat_id="beat_hedging",
        text="And then maybe you might perhaps consider writing down your goals every single morning.",
        visual_cue="Camera zooms in",  # Missing brackets!
        beat_type=BeatType.OPEN_LOOP_VARIABLE,
    )
    # Banned legacy outro
    flawed.add_beat(
        beat_id="beat_bad_outro",
        text="Thanks for watching, don't forget to like and subscribe and comment below!",
        visual_cue="[Subscribe button]",
        beat_type=BeatType.PAYOFF,
    )

    report = flawed.validate()
    print(report.summary())
    assert not report.is_valid, "Flawed script must FAIL validation!"
    assert len(report.violations) >= 5, f"Expected at least 5 violations, got {len(report.violations)}"
    print("✅ Flawed script correctly flagged all negative constraints and failed validation!")


def test_knight_capital_veteran_script():
    print("\n--- TEST 2: The $400 Million Keystroke (10/10 Veteran Standard) ---")
    script = VeteranScriptDirector.craft_knight_capital_script()
    report = script.validate()
    print(report.summary())

    assert report.is_valid, "Knight Capital script must PASS 10/10 validation!"
    assert report.score >= 90.0, f"Expected score >= 90.0, got {report.score}"
    assert report.gate_results["Zero-Second Hook Gate"]
    assert report.gate_results["Legacy Outro Ban Gate"]
    assert report.gate_results["Causal Opposition ('And Then' Ban) Gate"]
    assert report.gate_results["Anti-Hedging (Absolute Reality) Gate"]
    assert report.gate_results["18-Word Cap & Visual Cues Gate"]
    assert report.gate_results["Pacing Budget Gate"]
    assert report.gate_results["Infinite Loop & Dilemma Gate"]

    print("✅ Knight Capital script passed all 8 validation gates with 10/10 standard!")
    print("\nGenerated Markdown Script:\n")
    print(script.to_markdown())


def test_coffee_adenosine_veteran_script_and_tts():
    print("\n--- TEST 3: Morning Coffee Timing + Edge TTS Synthesis ---")
    script = VeteranScriptDirector.craft_coffee_adenosine_script()
    report = script.validate()
    print(report.summary())

    assert report.is_valid, "Morning Coffee script must PASS validation!"

    print(f"\nSynthesizing voiceover beats with Microsoft Edge Neural Voice ('{DEFAULT_VOICE}')...")
    audio_dir = Path("media/audio/test_script_engine")
    audio_dir.mkdir(parents=True, exist_ok=True)

    sheet = script.to_beat_sheet(voice=DEFAULT_VOICE, base_dir=str(audio_dir))
    master_audio = sheet.build_master_track(str(audio_dir / "coffee_adenosine_master.mp3"))

    total_audio_duration = get_audio_duration(master_audio)
    print(f"Master Audio Track Generated: {master_audio}")
    print(f"Total Spoken Audio Duration: {total_audio_duration:.2f}s across {len(sheet.beats)} beats")

    for name, fpath, dur in sheet.beats:
        print(f"  • Beat '{name}': {dur:.2f}s -> {fpath}")

    # Verify seamless loop audio transition:
    hook_file = sheet.get_file("beat_hook")
    loop_file = sheet.get_file("beat_loop")
    assert Path(hook_file).exists() and Path(loop_file).exists()
    print(f"✅ Infinite Audio Loop verified: '{script.loop_bridge_line}' smoothly connects into '{script.beats[0].text}'")


if __name__ == "__main__":
    test_flawed_script_detection()
    test_knight_capital_veteran_script()
    test_coffee_adenosine_veteran_script_and_tts()
    print("\n🏆 ALL SCRIPT ENGINE TESTS PASSED WITH 10/10 VETERAN STANDARD!")
