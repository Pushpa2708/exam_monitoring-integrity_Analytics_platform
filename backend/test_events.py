from event_validation import normalize_event_type, validate_event


def test_valid_event():
    assert validate_event("SESSION-101", "TAB_SWITCH", {})[0] is True


def test_missing_session_id():
    assert validate_event("", "TAB_SWITCH", {})[0] is False


def test_missing_event_type():
    assert validate_event("SESSION-101", "", {})[0] is False


def test_unsupported_event_type():
    assert validate_event("SESSION-101", "HELLO", {})[0] is False


def test_details_must_be_dict():
    assert validate_event("SESSION-101", "TAB_SWITCH", "invalid")[0] is False


def test_event_type_is_normalized():
    assert normalize_event_type(" tab_switch ") == "TAB_SWITCH"