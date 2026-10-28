import uuid
from datetime import datetime

PRESENT, ABSENT, UNAVAILABLE = "FACE_PRESENT", "FACE_ABSENT", "DETECTION_UNAVAILABLE"
STATES = (PRESENT, ABSENT, UNAVAILABLE)


class PresenceTracker:
    def __init__(self, session_id, absence_threshold_s=5.0, min_confidence=0.6):
        self.session_id = session_id
        self.threshold = absence_threshold_s
        self.min_confidence = min_confidence
        self.state = None
        self.start = None
        self.confs = []
        self.reason = None
        self.pending_since = None     
        self.pending_confs = []

    def add_sample(self, state, ts, confidence=None, reason=None):
        """Feed one sample. Returns finished events (usually an empty list)."""
        if state not in STATES:
            raise ValueError(f"Unknown state: {state}")

        if state == ABSENT and self.state == PRESENT:
            if self.pending_since is None:
                self.pending_since, self.pending_confs = ts, []
            if confidence is not None:
                self.pending_confs.append(float(confidence))
            if (ts - self.pending_since).total_seconds() < self.threshold:
                return []                              # short absence: wait
            began, confs = self.pending_since, list(self.pending_confs)
            self.pending_since, self.pending_confs = None, []
            events = self._collect(self._close(began))
            self.state, self.start, self.confs, self.reason = ABSENT, began, confs, reason
            return events

        self.pending_since, self.pending_confs = None, []   # face came back in time
        events = []
        if state != self.state:
            if self.state is not None:
                events = self._collect(self._close(ts))
            self.state, self.start, self.confs, self.reason = state, ts, [], None
        if confidence is not None:
            self.confs.append(float(confidence))
        if reason and not self.reason:
            self.reason = reason
        return events

    def finish(self, end):
        """Close the open interval when monitoring stops or is interrupted."""
        events = self._collect(self._close(end)) if self.state else []
        self.state, self.start, self.confs, self.reason = None, None, [], None
        self.pending_since, self.pending_confs = None, []
        return events

    @staticmethod
    def _collect(event):
        return [event] if event else []

    def _close(self, end):
        duration = (end - self.start).total_seconds()
        if duration <= 0 or (self.state == ABSENT and duration < self.threshold):
            return None
        confidence = sum(self.confs) / len(self.confs) if self.confs else None
        uncertain = (self.state == UNAVAILABLE
                     or (confidence is not None and confidence < self.min_confidence))
        return {
            "event_id": "evt_" + uuid.uuid4().hex[:12],
            "session_id": self.session_id,
            "event_type": self.state,
            "start_time": self.start,
            "end_time": end,
            "duration_seconds": round(duration, 1),
            "confidence": round(confidence, 2) if confidence is not None else None,
            "status": "UNCERTAIN" if uncertain else "CONFIRMED",
            "reason": self.reason,
        }