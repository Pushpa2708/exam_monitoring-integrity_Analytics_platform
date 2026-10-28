from event_validation import validate_event

assert validate_event("", "TAB_SWITCH", {})[0] is False
assert validate_event("SESSION-101", "", {})[0] is False
assert validate_event("SESSION-101", "TAB_SWITCH", "invalid")[0] is False
assert validate_event("SESSION-101", "TAB_SWITCH", {})[0] is True

print("All validation tests passed!")