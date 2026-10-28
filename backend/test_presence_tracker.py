from datetime import datetime, timedelta
from presence_tracker import PresenceTracker

T0 = datetime(2026, 10, 28, 10, 0, 0)

def t(sec):
    return T0 + timedelta(seconds=sec)

def run(samples):
    tracker, events = PresenceTracker("SESSION-T", 5), []
    for sec, state in samples:
        events += tracker.add_sample(state, t(sec), 0.9)
    return tracker, events

def test_short_absence_is_ignored():
    _, events = run([(0, "FACE_PRESENT"), (1, "FACE_ABSENT"), (2, "FACE_PRESENT"), (3, "FACE_PRESENT")])
    assert events == []

def test_long_absence_is_one_event_with_duration():
    _, events = run([(0, "FACE_PRESENT"), (1, "FACE_ABSENT"), (3, "FACE_ABSENT"),
                     (7, "FACE_ABSENT"), (9, "FACE_PRESENT")])
    absent = [e for e in events if e["event_type"] == "FACE_ABSENT"]
    assert len(absent) == 1 and absent[0]["duration_seconds"] == 8.0

def test_no_event_per_sample():
    tracker, events = run([(i, "FACE_PRESENT") for i in range(200)])
    events += tracker.finish(t(200))
    assert len(events) == 1

def test_camera_failure_is_not_absence():
    tracker = PresenceTracker("SESSION-T", 5)
    events = tracker.add_sample("FACE_PRESENT", t(0), 0.9)
    events += tracker.add_sample("DETECTION_UNAVAILABLE", t(2), None, "camera_unavailable")
    events += tracker.finish(t(6))
    kinds = [(e["event_type"], e["status"]) for e in events]
    assert ("DETECTION_UNAVAILABLE", "UNCERTAIN") in kinds
    