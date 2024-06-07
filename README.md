# Data Warehouse Project

## Table of Contents

1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Docker Architecture](#docker-architecture)
6. [API Documentation](#api-documentation)
8. [License](#license)


## Introduction

This Data Warehouse project is engineered to facilitate extensive data handling capabilities for financial and
commodities data. It employs advanced Python data engineering techniques, leveraging ORM for efficient data interactions
and providing a RESTful API for data access.

## System Architecture

The architecture is built around Python and Cassandra, with Docker ensuring container management. The integration of
Python ORM simplifies database interactions, converting complex SQL into manageable Python code, enhancing
maintainability and scalability.

## Getting Started

### Prerequisites

- Python 3.10 or later
- Docker and Docker Compose
- Cassandra
- Virtualenv or any environment management tool

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://yourrepository.com/data-warehouse.git
   cd data-warehouse
   ```

2. **Set up the virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch Docker containers:**
   ```bash
   docker-compose up -d
   ```

5. **Database Initialization:**
   Execute scripts to configure the database schema and seed it with initial data.

## Project Structure

- `src/`: Contains all source files.
    - `clients/`: API clients for data sources.
        - `commodities_api_client.py`: Retrieves commodities data.
        - `nasdaq_api_client.py`: Fetches NASDAQ data.
    - `config/`: Application configurations.
        - `settings.py`: Central config file.
    - `data/`: Handles database operations.
        - `database.py`: Manages database connections.
        - `models.py`: Defines ORM models.
    - `ingestion/`: Manages data loading and processing.
        - `load.py`: Ingests data into the database.
        - `transform.py`: Transforms data as needed.
    - `init_scripts/`: Database initialization scripts.
        - `populate_commodities_data.py`: Seeds commodities data.
        - `populate_sp500_data.py`: Seeds S&P 500 data.
    - `utils/`: Utility scripts.
        - `log_helper.py`: Provides logging functions.



## Docker Architecture

This project uses Docker to containerize and manage the Cassandra database cluster, ensuring consistency and scalability in the development and deployment environments. The Docker setup is defined in the `docker-compose.yml` file, which specifies the configuration for a multi-node Cassandra cluster along with Portainer for container management.

### Docker Compose File

The `docker-compose.yml` file defines the services and their configurations as follows:

```yaml
version: '3'

services:
  # Node 1 Configuration
  DC1N1:
    image: cassandra:3.10
    command: bash -c 'if [ -z "$$(ls -A /var/lib/cassandra/)" ] ; then sleep 0; fi && /docker-entrypoint.sh cassandra -f'
    networks:
      - dc1ring
    volumes:
      - ./n1data:/var/lib/cassandra
    environment:
      - CASSANDRA_CLUSTER_NAME=dev_cluster
      - CASSANDRA_SEEDS=DC1N1
    expose:
      - 7000  # Cluster communication
      - 7001  # SSL Cluster communication
      - 7199  # JMX
      - 9042  # CQL
      - 9160  # Thrift service
    ports:
      - "9042:9042"
    ulimits:
      memlock: -1
      nproc: 32768
      nofile: 100000

  # Node 2 Configuration
  DC1N2:
    image: cassandra:3.10
    command: bash -c 'if [ -z "$$(ls -A /var/lib/cassandra/)" ] ; then sleep 60; fi && /docker-entrypoint.sh cassandra -f'
    networks:
      - dc1ring
    volumes:
      - ./n2data:/var/lib/cassandra
    environment:
      - CASSANDRA_CLUSTER_NAME=dev_cluster
      - CASSANDRA_SEEDS=DC1N1
    depends_on:
      - DC1N1
    expose:
      - 7000
      - 7001
      - 7199
      - 9042
      - 9160
    ports:
      - "9043:9042"
    ulimits:
      memlock: -1
      nproc: 32768
      nofile: 100000

  # Node 3 Configuration
  DC1N3:
    image: cassandra:3.10
    command: bash -c 'if [ -z "$$(ls -A /var/lib/cassandra/)" ] ; then sleep 120; fi && /docker-entrypoint.sh cassandra -f'
    networks:
      - dc1ring
    volumes:
      - ./n3data:/var/lib/cassandra
    environment:
      - CASSANDRA_CLUSTER_NAME=dev_cluster
      - CASSANDRA_SEEDS=DC1N1
    depends_on:
      - DC1N1
    expose:
      - 7000
      - 7001
      - 7199
      - 9042
      - 9160
    ports:
      - "9044:9042"
    ulimits:
      memlock: -1
      nproc: 32768
      nofile: 100000

  # Portainer Configuration
  portainer:
    image: portainer/portainer
    networks:
      - dc1ring
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
      - ./portainer-data:/data
    ports:
      - "9000:9000"

networks:
  dc1ring: { }
```

### Explanation

1. **Cassandra Nodes**:
   - **DC1N1, DC1N2, DC1N3**:
     - Each service represents a Cassandra node in the cluster.
     - The `image` specifies the Docker image used.
     - The `command` ensures that the node waits if the data directory is empty, then starts Cassandra.
     - `networks` configures the internal network (`dc1ring`) for the cluster.
     - `volumes` maps the host directory to the container directory for persistent storage.
     - `environment` variables set cluster configurations such as `CASSANDRA_CLUSTER_NAME` and `CASSANDRA_SEEDS`.
     - `ports` exposes necessary ports for communication and management.
     - `ulimits` sets resource limits for the container.



## API Documentation

The API is structured around resources representing financial data and commodities. It supports operations for retrieving data based on asset identifiers and includes pagination capabilities.

## Endpoint Details

### Financial Data Endpoints

- **GET /api/v1/data/{asset_id}**
  - Retrieves financial data for a specified asset.
  - Parameters:
    - `asset_id`: UUID of the asset.
    - `limit`: Number of records to return.
    - `offset`: Pagination offset.
  - Example: `http://127.0.0.1:8000/api/v1/data/AAPL?limit=20&offset=0`

### Commodity Data Endpoints

- **GET /api/v1/commodities/{commodity_id}**
  - Fetches commodity data.
  - Parameters:
    - `commodity_id`: Identifier for the commodity.
    - `limit`: Controls the size of the returned data set.
    - `offset`: Specifies the pagination offset.
  - Example: `http://127.0.0.1:8000/api/v1/commodities/brent?limit=20&offset=0`

### Asset Endpoints

- **GET /api/v1/assets**
  - Retrieves a list of asset names.
  - Parameters:
    - `offset`: The number of records to skip from the beginning.
    - `limit`: The number of records to return.
  - Example: `http://127.0.0.1:8000/api/v1/assets?offset=0&limit=20`

### Data Source Endpoints

- **GET /api/v1/data_sources**
  - Retrieves a list of all data sources.
  - Example: `http://127.0.0.1:8000/api/v1/data_sources`

- **GET /api/v1/data_sources/{source_id}**
  - Retrieves details of a specific data source.
  - Parameters:
    - `source_id`: UUID of the data source.
  - Example: `http://127.0.0.1:8000/api/v1/data_sources/{source_id}`

## Examples

```bash
# Fetch financial data for a specific asset
curl -X GET "http://localhost:8000/api/v1/data/AAPL?limit=10&offset=0"

# Retrieve commodity data
curl -X GET "http://localhost:8000/api/v1/commodities/brent?limit=5&offset=0"

# Get a list of assets
curl -X GET "http://localhost:8000/api/v1/assets?offset=0&limit=20"

# Get a list of data sources
curl -X GET "http://localhost:8000/api/v1/data_sources"

# Get details of a specific data source
curl -X GET "http://localhost:8000/api/v1/data_sources/{source_id}"
```
## Photos

![image](https://github.com/liviuxyz-ctrl/DataWarehouse/assets/70070368/30ad1780-90cc-49cb-be44-45df3acffbeb)

![image](https://github.com/liviuxyz-ctrl/DataWarehouse/assets/70070368/d81a715e-cfc0-4b3e-b62c-87fb8dbeb35d)


## License

Licensed under the MIT License. See [LICENSE.md](LICENSE) for more details.
