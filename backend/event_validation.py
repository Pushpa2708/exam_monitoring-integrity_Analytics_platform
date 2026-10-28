ALLOWED_EVENT_TYPES = {
    "TAB_SWITCH", "MONITORING_STARTED", "MONITORING_STOPPED",
    "FACE_PRESENT", "FACE_ABSENT", "DETECTION_UNAVAILABLE",
}


def normalize_event_type(event_type):
    return str(event_type).strip().upper()


def validate_event(session_id, event_type, details):
    if not session_id or len(str(session_id)) > 64:
        return False, "Session ID is required (max 64 characters)"

    if not event_type:
        return False, "Event type is required"

    if normalize_event_type(event_type) not in ALLOWED_EVENT_TYPES:
        return False, "Unsupported event type"

    if not isinstance(details, dict):
        return False, "Details must be a dictionary"

    return True, "Event is valid"