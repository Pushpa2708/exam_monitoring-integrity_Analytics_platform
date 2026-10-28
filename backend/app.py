import json
import os
from datetime import datetime , timezone
from presence_tracker import PresenceTracker, STATES
from flask import Flask, request

from database import get_connection
from event_validation import normalize_event_type, validate_event
from events import create_event
from kafka_client import send_event
from logging_config import logger

app = Flask(__name__)
ABSENCE_THRESHOLD_S = float(os.getenv("ABSENCE_THRESHOLD_S", "5"))
TRACKERS = {}
USE_KAFKA = os.getenv("USE_KAFKA", "false").lower() == "true"

INSERT_SQL = """INSERT INTO events
    (event_id, session_id, event_type, event_timestamp, details)
    VALUES (%s, %s, %s, %s, %s)"""


def store_event(event):
    """Save one event in MySQL."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(INSERT_SQL, (
            event["event_id"],
            event["session_id"],
            event["event_type"],
            datetime.fromisoformat(event["timestamp"]).replace(tzinfo=None),
            json.dumps(event["details"]),
        ))
        connection.commit()
    finally:
        cursor.close()
        connection.close()


def process_event(session_id, event_type, details):
    """Validate, save, and (if turned on) send to Kafka."""
    if event_type:
        event_type = normalize_event_type(event_type)

    valid, message = validate_event(session_id, event_type, details)
    if not valid:
        logger.warning("Event rejected: %s", message)
        return {"error": message}, 400

    event = create_event(session_id, event_type, details)
    store_event(event)
    logger.info("Event saved: %s", event["event_id"])

    if USE_KAFKA:
        if send_event(event):
            logger.info("Event sent to Kafka: %s", event["event_id"])
        else:
            logger.warning("Kafka send failed: %s", event["event_id"])

    return {"message": "Event saved successfully", "event": event}, 201


@app.route("/api/health", methods=["GET"])
def health():
    logger.info("Health check successful")
    return {"status": "ok", "message": "ExamGuard backend is running"}, 200


@app.route("/api/test-event")
def test_event():
    event = create_event(
        session_id="SESSION-101",
        event_type="TAB_SWITCH",
        details={"message": "Candidate switched browser tab"},
    )
    logger.info("Event created: %s", event["event_id"])
    return event, 200


@app.route("/api/test-logs")
def test_logs():
    logger.debug("Debug message")
    logger.info("Application running normally")
    logger.warning("Unusual examination activity detected")
    logger.error("Example error message")
    return {"message": "Check terminal and logs/examguard.log"}, 200


@app.route("/api/save-event")
def save_test_event():
    return process_event(
        "SESSION-101", "TAB_SWITCH",
        {"message": "Candidate switched browser tab"},
    )


@app.route("/api/events", methods=["POST"])
def add_event():
    data = request.get_json(silent=True) or {}
    return process_event(
        data.get("session_id"), data.get("event_type"), data.get("details", {})
    )


@app.route("/api/events", methods=["GET"])
def get_events():
    session_id = request.args.get("session_id")
    query = ("SELECT event_id, session_id, event_type, event_timestamp, details "
             "FROM events")
    params = ()
    if session_id:
        query += " WHERE session_id = %s"
        params = (session_id,)
    query += " ORDER BY event_timestamp ASC"

    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(query, params)
        events = cursor.fetchall()
    finally:
        cursor.close()
        connection.close()

    for e in events:
        if e["event_timestamp"]:
            e["event_timestamp"] = e["event_timestamp"].isoformat()
        if isinstance(e["details"], str):
            e["details"] = json.loads(e["details"])

    return {"events": events}, 200


def parse_ts(value):
    """Text -> naive UTC datetime. Text without a timezone is treated as UTC."""
    if not value:
        return datetime.now(timezone.utc).replace(tzinfo=None)
    dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).replace(tzinfo=None) if dt.tzinfo else dt


def save_tracker_event(ev):
    store_event({
        "event_id": ev["event_id"],
        "session_id": ev["session_id"],
        "event_type": ev["event_type"],
        "timestamp": ev["start_time"].isoformat(),
        "details": {
            "start_time": ev["start_time"].isoformat(),
            "end_time": ev["end_time"].isoformat(),
            "duration_seconds": ev["duration_seconds"],
            "confidence": ev["confidence"],
            "status": ev["status"],
            "reason": ev["reason"],
        },
    })
    logger.info("Event %s %s %.1fs %s", ev["event_id"], ev["event_type"],
                ev["duration_seconds"], ev["status"])


@app.route("/api/monitoring/samples", methods=["POST"])
def add_sample():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")
    state = str(data.get("state", "")).upper()
    if not session_id or state not in STATES:
        return {"error": "session_id and a valid state are required"}, 400
    try:
        ts = parse_ts(data.get("timestamp"))
    except ValueError:
        return {"error": "Invalid timestamp"}, 400

    tracker = TRACKERS.setdefault(session_id, PresenceTracker(session_id, ABSENCE_THRESHOLD_S))
    events = tracker.add_sample(state, ts, data.get("confidence"), data.get("reason"))
    for ev in events:
        save_tracker_event(ev)
    return {"events_created": len(events), "current_state": tracker.state}, 200

@app.route("/api/monitoring/stop", methods=["POST"])
def stop_monitoring():
    data = request.get_json(silent=True) or {}
    session_id = data.get("session_id")

    if not session_id:
        return {"error": "session_id is required"}, 400

    try:
        end_time = parse_ts(data.get("timestamp"))
    except ValueError:
        return {"error": "Invalid timestamp"}, 400

    tracker = TRACKERS.pop(session_id, None)
    events = tracker.finish(end_time) if tracker else []

    for ev in events:
        save_tracker_event(ev)

    result, status_code = process_event(
        session_id, "MONITORING_STOPPED", {}
    )

    if status_code >= 400:
        return result, status_code

    return {
        "message": "Monitoring stopped",
        "events_closed": len(events)
    }, 200

if __name__ == "__main__":
    app.run(debug=True)