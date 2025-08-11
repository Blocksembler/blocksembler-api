# Blocksembler REST API

This is the Blocksembler backend API powered by FastAPI, designed to handle and store logging events for the
Blocksembler platform.

## Setup

### Prerequisites

- Docker

### Installation

```shell
docker run --name blocksembler-api --port 80 blocksembler-api:latest
```

### Environment Variables

| Name                        | Default     | Description                                              |
|-----------------------------|-------------|----------------------------------------------------------|
| `DEBUG`                     | `True`      | Runs the API in debug mode, enabling detailed error logs |
| `BLOCKSEMBLER_API_DB_URL`   | `localhost` | Host address of the MongoDB instance (e.g., `localhost`) |
| `BLOCKSEMBLER_API_DB_PORT`  | `27017`     | Port number for connecting to the MongoDB instance       |
| `BLOCKSEMBLER_API_BASE_URL` | `/`         | Base URL path under which this API is served             |
| `BLOCKSEMBLER_ORIGINS`      | `*`         | Allowed Origins                                          |

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
  "source": "button1",
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
