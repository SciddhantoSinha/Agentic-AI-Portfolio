import time

import pytest

from src.telemetry import TelemetryTracker


def test_tracker_starts_with_no_events():
    tracker = TelemetryTracker()

    assert tracker.events == []
    assert tracker.elapsed_ms() == 0.0


def test_record_adds_event():
    tracker = TelemetryTracker()

    tracker.record(
        event="retrieval",
        metadata={
            "source": "internal"
        },
    )

    assert len(tracker.events) == 1
    assert tracker.events[0]["event"] == "retrieval"
    assert tracker.events[0]["metadata"]["source"] == "internal"
    assert "timestamp" in tracker.events[0]


def test_empty_event_raises_error():
    tracker = TelemetryTracker()

    with pytest.raises(ValueError):
        tracker.record("")


def test_elapsed_time_is_measured():
    tracker = TelemetryTracker()

    tracker.start()

    time.sleep(0.01)

    elapsed = tracker.elapsed_ms()

    assert elapsed > 0


def test_finish_returns_telemetry_summary():
    tracker = TelemetryTracker()

    tracker.start()

    tracker.record(
        event="routing",
        metadata={
            "route": "INTERNAL"
        },
    )

    summary = tracker.finish()

    assert "duration_ms" in summary
    assert "events" in summary
    assert summary["duration_ms"] >= 0
    assert summary["events"][-1]["event"] == (
        "pipeline_complete"
    )


def test_clear_removes_events_and_timer():
    tracker = TelemetryTracker()

    tracker.start()

    tracker.record(
        event="retrieval"
    )

    tracker.clear()

    assert tracker.events == []
    assert tracker.elapsed_ms() == 0.0
