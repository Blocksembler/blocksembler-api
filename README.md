# Blocksembler REST API

A FastAPI-based REST API for managing TAN codes and storing logging events in MongoDB.

## Setup

### Prerequisites

- Python 3.11+
- MongoDB running on localhost:27017

### Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Start the API server:
   ```
   uvicorn src.main:app --reload
   ```

## API Endpoints

### TAN Code Management

- `GET /tan/{tan_code}` - Get a specific TAN code
- `POST /tan/` - Create new TAN codes

### Logging Events

#### Store Logging Events

```
POST /logging/{tan_code}
```

Stores multiple logging events for a specific TAN code in MongoDB.

**Path Parameters:**
- `tan_code` (string): The TAN code to associate with the logging events

**Request Body:**
- Array of LoggingEvent objects with the following properties:
  - `ts` (datetime, optional): Timestamp of the event (defaults to current time)
  - `type` (string): Type of the logging event
  - `source` (string): Source of the log
  - `payload` (object, optional): Additional data for the log (defaults to empty object)

**Response:**
- Returns the number of events successfully stored

**Example Request:**

```
POST /logging/ABC123
```

Request body:
```json
[
  {
    "type": "info",
    "source": "sensor_1",
    "payload": {
      "temperature": 22.5,
      "humidity": 45
    }
  },
  {
    "type": "warning",
    "source": "sensor_2",
    "payload": {
      "battery": "low"
    }
  }
]
```

#### Get Logging Events by Date Range

```
GET /logging/{tan_code}?start={start_datetime}&end={end_datetime}
```

Retrieves logging events for a specific TAN code within a date range.

**Path Parameters:**
- `tan_code` (string): The TAN code to retrieve events for

**Query Parameters:**
- `start` (datetime): Start date/time for the range
- `end` (datetime, optional): End date/time for the range

**Response:**
- Returns an array of LoggingEvent objects sorted by timestamp (newest first)

#### Get Latest Logging Event

```
GET /logging/{tan_code}/latest
```

Retrieves the most recent logging event for a specific TAN code.

**Path Parameters:**
- `tan_code` (string): The TAN code to retrieve the latest event for

**Response:**
- Returns a single LoggingEvent object

## Data Models

### LoggingEvent

```json
{
  "ts": "2025-07-28T13:15:00",
  "type": "info",
  "source": "sensor_1",
  "payload": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

### TanCode

```json
{
  "code": "ABC123",
  "valid_from": "2025-07-28T00:00:00",
  "valid_to": "2025-08-28T00:00:00"
}
```

## MongoDB Collections

The API uses the following MongoDB collections:

- `tans`: Stores TAN code information
- `logging_events`: Stores logging events with references to TAN codes
