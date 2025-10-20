## <img src="img/logo.png" alt="drawing" width="200"/>

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC_BY--NC--ND_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-nd/4.0/)

# Blocksembler REST API

This is the Blocksembler Backend API powered by FastAPI, designed to handle and store logging events, exercises and
automatic grading of exercise submissions.

## Getting Started

### Run from Source

To get started with the Assembler Programming Learning Environment, follow these steps:

1. **Clone the Repository**: Clone this repository to your local machine using

   ```bash
    git clone https://github.com/Blocksembler/blocksembler-api.git
   ```

2. **Create and activate a new Virtual Environment**: Navigate to the project directory and execute following command
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. **Install requirements**: Install all python packages required for this application
   ```bash
   pip install -r requirements
   ```

4. **Run the Application**: Start the application by running following command:
   ```bash
   fastapi run app/main.py --port 8081 --host=0.0.0.0
   ```

   This will launch the backend locally. In case the DEBUG environment variable is set to `true` the swagger ui can be
   accessed on [http://localhost:8081/docs](http://localhost:8081/docs).

### Run from Docker Image

Blocksembler is also available on [Docker Hub](https://hub.docker.com/r/blocksembler/blocksembler-frontend/tags). To get
started, follow these steps:

1. **Pull Docker Image**: Pull the blocksembler/blocksembler-frontend image
   `docker pull blocksembler/blocksembler-api:latest`

2. **Run the Container**: Start up a new container instance that runs the blocksembler application
   `docker run blocksembler/blocksembler-api:latest -p 8081:8081 -d`. This will launch the application locally. In case
   the DEBUG environment variable is set to `true` the swagger ui can be accessed
   on [http://localhost:8081/docs](http://localhost:8081/docs).

### Environment Variables

#### Genearl Settings

| Name                        | Default | Description                                              |
|-----------------------------|---------|----------------------------------------------------------|
| `DEBUG`                     | `True`  | Runs the API in debug mode, enabling detailed error logs |
| `BLOCKSEMBLER_ORIGINS`      | `*`     | Allowed Origins                                          |
| `BLOCKSEMBLER_API_BASE_URL` | `/`     | Base URL path under which this API is served             |

#### Database Settings

| Name                  | Default                                                              | Description                                                 |
|-----------------------|----------------------------------------------------------------------|-------------------------------------------------------------|
| `BLOCKSEMBLER_DB_URI` | `postgresql+asyncpg://postgres:postgres@localhost:5432/blocksembler` | Host address of the *postgres* instance (e.g., `localhost`) |

#### Message Queue Settings

| Name                                      | Default                         | Description                                                     |
|-------------------------------------------|---------------------------------|-----------------------------------------------------------------|
| `BLOCKSEMBLER_MQ_URL`                     | `localhost`                     | Hostname or URL of the RabbitMQ broker.                         |
| `BLOCKSEMBLER_MQ_PORT`                    | `5672`                          | Port on which the RabbitMQ broker is listening.                 |
| `BLOCKSEMBLER_MQ_USER`                    | `blocksembler`                  | Username for authenticating with the RabbitMQ broker.           |
| `BLOCKSEMBLER_MQ_PWD`                     | `blocksembler`                  | Password for authenticating with the RabbitMQ broker.           |
| `BLOCKSEMBLER_MQ_EXCHANGE_NAME`           | `blocksembler-grading-exchange` | Name of the RabbitMQ exchange used for publishing grading jobs. |
| `BLOCKSEMBLER_MQ_GRADING_JOB_QUEUE`       | `grading-jobs`                  | Name of the RabbitMQ queue that receives grading jobs.          |
| `BLOCKSEMBLER_MQ_GRADING_JOB_ROUTING_KEY` | `grading.job.created`           | Routing key used to bind the grading job queue to the exchange. |
|

## Contributing

Contributions to this project are welcome! If you have ideas for new features, improvements, or bug fixes, feel free to
open an issue or submit a pull request.

## Contact

Florian Wörister | Universität Wien