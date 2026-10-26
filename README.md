
# ExamGuard — Online Exam Monitoring & Integrity Analytics Platform

## Overview

ExamGuard is an online exam monitoring platform designed to record monitoring events, maintain evidence, and support examination integrity analysis.

This repository contains the backend work for **Team 3 — Events & Evidence** as part of the Infosys Springboard internship project.

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

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file using `.env.example` as a reference.

Configure the following variables with your local MySQL settings:

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

