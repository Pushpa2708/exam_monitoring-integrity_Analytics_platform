def validate_event(session_id, event_type, details):
    if not session_id:
        return False, "Session ID is required"

    if not event_type:
        return False, "Event type is required"

    if not isinstance(details, dict):
        return False, "Details must be a dictionary"

    return True, "Event is valid"