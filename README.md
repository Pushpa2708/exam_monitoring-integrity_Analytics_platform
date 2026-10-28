# ExamGuard — Online Exam Monitoring & Integrity Analytics Platform

## Overview

ExamGuard is an online exam monitoring platform designed to record monitoring events, maintain evidence, and support examination integrity analysis.

This repository contains the backend work for **Team 3 — Events & Evidence** as part of the Infosys Springboard internship project.git status

## Team Responsibilities

Team 3 focuses on processing monitoring events, validating event data, recording timestamps, and preparing evidence for storage and analysis.

## Technology Stack

- **Python** — Backend development
- **Flask** — REST API
- **MySQL** — Event storage
- **Apache Kafka** — Planned event streaming and integration
- **Python Logging** — Application logs

## Implemented Features

- [x] Flask backend setup
- [x] MySQL database connection
- [x] Event creation with unique event IDs
- [x] Event timestamps
- [x] Basic event validation
- [x] Application logging
- [x] Save events to MySQL
- [x] Retrieve stored events
- [x] Filter events using session ID
- [x] Basic event-validation tests

## Planned Features

- [ ] Apache Kafka producer and consumer integration
- [ ] Integration with webcam-based monitoring events
- [ ] Record monitoring event start time and end time
- [ ] Calculate event duration
- [ ] Record detector confidence when available
- [ ] Distinguish confirmed observations from uncertain detections
- [ ] Prevent excessive duplicate events
- [ ] Integrate with other project teams

## Project Structure

```text
backend/
├── app.py
├── database.py
├── events.py
├── event_validation.py
├── logging_config.py
├── test_events.py
├── test_db.py
├── requirements.txt
├── .env.example
└── README.md
```

*Note: The file list may vary depending on the current implementation.*

## Database

The project uses MySQL with a database named `examguard`.

The `events` table stores:

| Field | Description |
|---|---|
| `event_id` | Unique identifier for an event |
| `session_id` | Exam session associated with the event |
| `event_type` | Type of monitoring event |
| `event_timestamp` | Date and time when the event occurred |
| `details` | Additional event information stored as JSON |

## Setup Instructions

### 1. Create a Python virtual environment

```bash
python -m venv venv
```

### 2. Activate the environment on Windows
git status
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure the following variables with your local MySQL settings:

# ExamGuard — Online Exam Monitoring & Integrity Analytics Platform

## 1. Project Overview

ExamGuard is an online examination monitoring project designed to record monitoring events, track face-detection states, and maintain evidence for later analysis.

 **Team 3 — Events & Evidence**.

The main tasks are:
- Normalize and validate monitoring events.
- Track face-presence states over time.
- Filter short face-absence intervals.
- Record event timestamps, durations, and confidence when available.
- Distinguish face absence from camera or detection failures.
- Store event records in MySQL.
- Support event streaming through Kafka when enabled.

## 2. Architecture

```text
             Team 2
      Computer Vision Module
       (Expected sample source)
                 |
                 v
       Monitoring State Samples
   FACE_PRESENT / FACE_ABSENT /
       DETECTION_UNAVAILABLE
                 |
                 v
             Team 3
        PresenceTracker
    - State tracking
    - Short-absence filtering
    - Interval calculation
    - Confidence and status
                 |
                 v
           Flask REST API
                 |
                 v
          Event Processing
                 |
          +------+------+
          |             |
          v             v
        MySQL          Kafka
     Event Store    Event Stream
          |             |
          +------+------+
                 |
                 v
       Future Dashboard /
          Event Timeline
```

**Note:** This represents the intended architecture. Live webcam integration, Kafka publishing of tracker-generated events, and automatic dashboard integration still require end-to-end verification.

## 3. Project Structure

```text
exam_monitoring-integrity_Analytics_platform/
│
├── backend/
│   ├── logs/
│   ├── .venv/
│   ├── .env
│   ├── .env.example
│   ├── app.py
│   ├── check_db.py
│   ├── database.py
│   ├── event_validation.py
│   ├── events.py
│   ├── kafka_client.py
│   ├── logging_config.py
│   ├── presence_tracker.py
│   ├── requirements.txt
│   ├── test_events.py
│   └── test_presence_tracker.py
│
├── frontend/
├── .gitignore
├── LICENSE
└── README.md
```

### Backend file responsibilities

| File | Purpose |
|---|---|
| `app.py` | Main Flask application and API endpoints |
| `presence_tracker.py` | Tracks monitoring states and groups samples into intervals |
| `event_validation.py` | Normalizes and validates standard event types |
| `events.py` | Creates events with unique IDs and timestamps |
| `database.py` | Connects Python to MySQL |
| `kafka_client.py` | Creates the Kafka producer and publishes standard events |
| `logging_config.py` | Configures application logging |
| `check_db.py` | Helps test database connectivity |
| `test_events.py` | Tests standard event functionality |
| `test_presence_tracker.py` | Tests presence-tracking behavior |
| `.env` | Local database and Kafka configuration |
| `.env.example` | Example configuration template |
| `requirements.txt` | Python package dependencies |
| `logs/` | Application log files |
| `.venv/` | Isolated Python environment |

## 4. Technologies Used

- Python
- Flask REST API
- MySQL
- Apache Kafka
- `kafka-python`
- Pytest
- Python logging

## 5. How the System Works

1. The monitoring component supplies a state sample for an examination session.
2. Flask receives the sample through the monitoring API.
3. `PresenceTracker` tracks the current state and its duration.
4. Repeated samples are grouped into intervals rather than creating an event for every sample.
5. Short face-absence gaps can be ignored using a configurable threshold.
6. Detection failures are recorded separately from confirmed face absence.
7. Completed intervals are saved to MySQL.
8. Kafka can be used to stream events to other services when enabled and available.

## 6. How to Run the Backend

### Prerequisites

Install or configure:

- Python
- MySQL Server
- Project Python dependencies
- Apache Kafka only if you want to demonstrate Kafka publishing

### Step 1: Open the backend folder

Open the project in VS Code.

Open the terminal and navigate to the backend directory:

```powershell
cd backend
```

### Step 2: Activate the virtual environment

If `.venv` already exists, run:

```powershell
.\.venv\Scripts\Activate
```

If PowerShell activates it successfully, the terminal should show `(.venv)`.

If the virtual environment does not exist, create it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

### Step 3: Install dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Ensure `backend/.env` contains the correct values for your local setup.

Example:
>>>>>>> 032a59c (Update ExamGuard backend)

```text
DB_HOST=localhost
DB_PORT=3306

DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=examguard
```

**Important:** Never commit `.env` or expose database passwords in a public repository.

### 5. Run the Flask application

```bash
python app.py
```

## Testing

Run the event-validation tests:

```bash
python test_events.py
```

The database connection can be checked separately using:

```bash
python test_db.py
```

## Current Status

The basic Flask backend and MySQL event-storage functionality have been implemented and tested.

Kafka integration and the remaining Sprint 3 event-processing requirements are still in progress.

## Future Integration

The planned workflow is:

**Webcam Monitoring → Event Validation and Normalization → Kafka → Event Storage → Dashboard and Analytics**

The final workflow will be coordinated with the other teams during integration.
DB_USER=your_mysql_user
DB_PASSWORD=your_mysql_password
DB_NAME=examguard

KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=exam-events
USE_KAFKA=false

ABSENCE_THRESHOLD_S=5
```

Replace the database username and password with your actual credentials.

Keep `USE_KAFKA=false` if Kafka is not running. Set it to `true` only when the local broker is running and you intend to test publishing.

**Security:** Never commit your real `.env` file or database password to GitHub.

### Step 5: Start MySQL

Start your local MySQL server.

Confirm that the database and `events` table have been created using your project's existing database setup.

### Step 6: Start the Flask application

From the `backend` directory, run:

```powershell
python app.py
```

Wait until Flask displays a message similar to:

```text
* Running on http://127.0.0.1:5000
```

Keep this terminal open.

## 7. How to Test the APIs

Open a **second PowerShell terminal**. Keep the Flask terminal running.

### Test 1: Health check

Run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/health" -Method GET
```

Expected response:

```text
status message
------ -------
ok     ExamGuard backend is running
```

### Test 2: Submit a face-presence sample

Run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/monitoring/samples" -Method POST -ContentType "application/json" -Body '{"session_id":"SESSION-DEMO-1","state":"FACE_PRESENT","confidence":0.95}'
```

Expected result:

```text
events_created current_state
-------------- -------------
0              FACE_PRESENT
```

The response may be displayed differently in PowerShell.

An `events_created` value of zero is normal when the interval is still open.

### Test 3: Submit a face-absence sample

Wait approximately two seconds and run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/monitoring/samples" -Method POST -ContentType "application/json" -Body '{"session_id":"SESSION-DEMO-1","state":"FACE_ABSENT","confidence":0.90}'
```

Wait at least six seconds and submit another absence sample:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/monitoring/samples" -Method POST -ContentType "application/json" -Body '{"session_id":"SESSION-DEMO-1","state":"FACE_ABSENT","confidence":0.90}'
```

The tracker waits for the absence threshold before treating the prolonged absence as an interval.

### Test 4: Stop monitoring

Run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/monitoring/stop" -Method POST -ContentType "application/json" -Body '{"session_id":"SESSION-DEMO-1"}'
```

Expected response format:

```text
message           events_closed
-------           -------------
Monitoring stopped 1
```

The number of closed events can vary depending on the tracker state and duration.

### Test 5: Retrieve events

Run:

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/api/events?session_id=SESSION-DEMO-1" -Method GET
```

This retrieves events stored for the specified session.

### Test 6: Run automated tracker tests

Open a terminal in the `backend` directory, with the virtual environment activated.

Run:

```powershell
python -m pytest test_presence_tracker.py -v
```

The four tests currently cover:

1. Ignoring short face-absence gaps.
2. Recording a prolonged absence with its duration.
3. Avoiding one event per repeated sample.
4. Distinguishing detection failures from confirmed face absence.

**Previously verified result:** All four tests passed.

To run the standard event tests too:

```powershell
python -m pytest test_events.py -v
```

## 8. Database Storage

Completed monitoring intervals are stored in MySQL.

The event table contains fields such as:

- `event_id`
- `session_id`
- `event_type`
- `event_timestamp`
- `details`

The `details` JSON field stores interval metadata, including start time, end time, duration, confidence, status, and reason.

To inspect a session's events in MySQL:

```sql
USE examguard;

SELECT
    event_id,
    session_id,
    event_type,
    event_timestamp,
    details
FROM events
WHERE session_id = 'SESSION-DEMO-1'
ORDER BY event_timestamp;
```

Use the actual database name configured in your `.env` if it differs from `examguard`.

## 9. Current Implementation Status

### Implemented and tested

- Flask API and standard event processing.
- Event creation, validation, and normalization.
- MySQL integration for event storage and retrieval.
- Local Kafka setup and producer code configured previously.
- Presence-tracking interval logic.
- Filtering short absences.
- Grouping repeated samples into intervals.
- Separate handling of detection-unavailable states.
- Monitoring sample and stop endpoints tested locally.
- Four automated presence-tracker tests passed.

### Remaining work

- Verify integration with live webcam/OpenCV detection.
- Verify Kafka publishing of tracker-generated intervals.
- Integrate the event stream or stored events with the dashboard.
- Improve persistence of tracker state across server restarts.

The current tracker registry is in memory, so active intervals can be lost if the Flask process restarts.


