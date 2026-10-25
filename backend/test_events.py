from events import create_event

event = create_event(
    "SESSION-101",
    "TAB_SWITCH",
    {"message": "Candidate switched browser tab"}
)

assert event["event_id"]
assert event["session_id"] == "SESSION-101"
assert event["event_type"] == "TAB_SWITCH"
assert event["timestamp"]
assert isinstance(event["details"], dict)

print("All event tests passed!")