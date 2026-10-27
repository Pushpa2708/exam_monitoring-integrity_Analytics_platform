from flask import request
from flask import Flask
from logging_config import logger
from events import create_event
from database import get_connection
import json
from datetime import datetime
from event_validation import validate_event
from kafka_client import send_event

app = Flask(__name__)

@app.route("/api/health", methods=["GET"])
def health():
    logger.info("Health check successful")
    return {"status": "ok", "message": "ExamGuard backend is running"}, 200


@app.route("/api/test-event")
def test_event():
    event = create_event(
        session_id="SESSION-101",
        event_type="TAB_SWITCH",
        details={"message": "Candidate switched browser tab"}
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
def save_event():
    session_id = "SESSION-101"
    event_type = "TAB_SWITCH"
    details = {"message": "Candidate switched browser tab"}

    valid, message = validate_event(session_id, event_type, details)

    if not valid:
        return {"error": message}, 400

    event = create_event(session_id, event_type, details)
    connection = get_connection()

    try:
        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO events
            (event_id, session_id, event_type, event_timestamp, details)
            VALUES (%s, %s, %s, %s, %s)""",
            (
                event["event_id"],
                event["session_id"],
                event["event_type"],
                datetime.fromisoformat(event["timestamp"]).replace(tzinfo=None),
                json.dumps(event["details"])
            )
        )
        connection.commit()
        try:
            send_event(event)
            logger.info("Event sent to Kafka: %s", event["event_id"])
        except Exception:
            logger.exception("Failed to send event to Kafka")
        logger.info("Event saved: %s", event["event_id"])
        return {"message": "Event saved successfully", "event": event}, 201

    finally:
        cursor.close()
        connection.close()

@app.route("/api/events")
def get_events():
    session_id = request.args.get("session_id")
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        if session_id:
            cursor.execute("""
                SELECT event_id, session_id, event_type,
                       event_timestamp, details
                FROM events
                WHERE session_id = %s
                ORDER BY event_timestamp DESC
            """, (session_id,))
        else:
            cursor.execute("""
                SELECT event_id, session_id, event_type,
                       event_timestamp, details
                FROM events
                ORDER BY event_timestamp DESC
            """)

        events = cursor.fetchall()

        for event in events:
            if event["event_timestamp"]:
                event["event_timestamp"] = event["event_timestamp"].isoformat()

        return {"events": events}, 200

    finally:
        cursor.close()
        connection.close()
        connection.close()

if __name__ == "__main__":
    app.run(debug=True)