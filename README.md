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

| Name                        | Default              | Description                                              |
|-----------------------------|----------------------|----------------------------------------------------------|
| `DEBUG`                     | `True`               | Runs the API in debug mode, enabling detailed error logs |
| `BLOCKSEMBLER_API_URI`      | `sqlite:///:memory:` | Host address of the MongoDB instance (e.g., `localhost`) |
| `BLOCKSEMBLER_API_BASE_URL` | `/`                  | Base URL path under which this API is served             |
| `BLOCKSEMBLER_ORIGINS`      | `*`                  | Allowed Origins                                          |

## Contributing

Contributions are welcome! To get started:

- Fork the repository
- Create a new branch (git checkout -b feature/your-feature)
- Make your changes
- Open a pull request

## Contact

Florian Wörister | Universität Wien