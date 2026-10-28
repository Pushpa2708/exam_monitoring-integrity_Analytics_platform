import json
import logging
import os

from dotenv import load_dotenv
from kafka import KafkaProducer
from kafka.errors import KafkaError

load_dotenv()
log = logging.getLogger("examguard")

BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
TOPIC = os.getenv("KAFKA_TOPIC", "exam-events")
_producer = None


def _get_producer():
    global _producer
    if _producer is None:               # created only when first needed
        _producer = KafkaProducer(
            bootstrap_servers=BOOTSTRAP,
            key_serializer=lambda k: str(k).encode("utf-8"),
            value_serializer=lambda v: json.dumps(v, default=str).encode("utf-8"),
        )
    return _producer


def send_event(event):
    """Return True if Kafka accepted the event, otherwise False."""
    try:
        _get_producer().send(TOPIC, key=event["session_id"], value=event).get(timeout=10)
        return True
    except KafkaError as error:
        log.error("Kafka send failed for %s: %s", event.get("event_id"), error)
        return False