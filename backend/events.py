from datetime import datetime, timezone
from uuid import uuid4


def create_event(session_id, event_type, details):
    return {
        "event_id": str(uuid4()),
        "session_id": session_id,
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details
    }