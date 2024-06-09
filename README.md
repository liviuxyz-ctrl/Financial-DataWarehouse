# Financial DataWarehouse Project

<details open> 
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#introduction">Introduction</a></li>
    <li><a href="#system-architecture">System Architecture</a></li>
    <li><a href="#getting-started">Getting Started</a></li>
    <li><a href="#project-structure">Project Structure</a></li>
    <li><a href="#docker-architecture">Docker Architecture</a></li>
    <li><a href="#api-documentation">API Documentation</a></li>
    <li><a href="#license">License</a></li>
  </ol>
</details>

## Introduction

<details open>
  <summary>Details</summary>
  This Data Warehouse project is engineered to facilitate extensive data handling capabilities for financial and commodities data. It employs advanced Python data engineering techniques, leveraging ORM for efficient data interactions and providing a RESTful API for data access.
</details>

## System Architecture

<details open>
  <summary>Details</summary>
  The architecture is built around Python and Cassandra, with Docker ensuring container management. The integration of Python ORM simplifies database interactions, converting complex SQL into manageable Python code, enhancing maintainability and scalability.
</details>

## Getting Started

<details open>
  <summary>Details</summary>

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

</details>

## Project Structure

<details>
  <summary>Details</summary>
  <ul>
    <li><code>src/</code>: Contains all source files.
      <ul>
        <li><code>clients/</code>: API clients for data sources.
          <ul>
            <li><code>commodities_api_client.py</code>: Retrieves commodities data.</li>
            <li><code>nasdaq_api_client.py</code>: Fetches NASDAQ data.</li>
          </ul>
        </li>
        <li><code>config/</code>: Application configurations.
          <ul>
            <li><code>settings.py</code>: Central config file.</li>
          </ul>
        </li>
        <li><code>data/</code>: Handles database operations.
          <ul>
            <li><code>database.py</code>: Manages database connections.</li>
            <li><code>models.py</code>: Defines ORM models.</li>
          </ul>
        </li>
        <li><code>ingestion/</code>: Manages data loading and processing.
          <ul>
            <li><code>load.py</code>: Ingests data into the database.</li>
            <li><code>transform.py</code>: Transforms data as needed.</li>
          </ul>
        </li>
        <li><code>init_scripts/</code>: Database initialization scripts.
          <ul>
            <li><code>populate_commodities_data.py</code>: Seeds commodities data.</li>
            <li><code>populate_sp500_data.py</code>: Seeds S&P 500 data.</li>
          </ul>
        </li>
        <li><code>utils/</code>: Utility scripts.
          <ul>
            <li><code>log_helper.py</code>: Provides logging functions.</li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>
</details>


## Docker Architecture

<details>
  <summary>Details</summary>
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

  2. **Portainer**:
     - The **Portainer** service provides a web-based interface for managing Docker containers.
     - It is configured to use the same `dc1ring` network and has access to the Docker socket for control.
</details>

## API Documentation

<details open>
  <summary>Details</summary>
  The API is structured around resources representing financial data and commodities. It supports operations for retrieving data based on asset identifiers and includes pagination capabilities.

  For easier use, a **Postman collection** is provided. You can download it [here](https://github.com/liviuxyz-ctrl/DataWarehouse/blob/master/Financial%20Data%20API.postman_collection.json).

  ### Endpoint Details

  #### Financial Data Endpoints

  - **GET /api/v1/data/{asset_id}**
    - Retrieves financial data for a specified asset.
    - Parameters:
      - `asset_id`: UUID of the asset.
      - `limit`: Number of records to return.
      - `offset`: Pagination offset.
    - Example: `http://127.0.0.1:8000/api/v1/data/AAPL?limit=20&offset=0`

  #### Commodity Data Endpoints

  - **GET /api/v1/commodities/{commodity_id}**
    - Fetches commodity data.
    - Parameters:
      - `commodity_id`: Identifier for the commodity.
      - `limit`: Controls the size of the returned data set.
      - `offset`: Specifies the pagination offset.
    - Example: `http://127.0.0.1:8000/api/v1/commodities/brent?limit=20&offset=0`

  #### Asset Endpoints

  - **GET /api/v1/assets**
    - Retrieves a list of asset names.
    - Parameters:
      - `offset`: The number of records to skip from the beginning.
      - `limit`: The number of records to return.
    - Example: `http://127.0.0.1:8000/api/v1/assets?offset=0&limit=20`

  #### Data Source Endpoints

  - **GET /api/v1/data_sources**
    - Retrieves a list of all data sources.
    - Example: `http://127.0.0.1:8000/api/v1/data_sources`

  - **GET /api/v1/data_sources/{source_id}**
    - Retrieves details of a specific data source.
    - Parameters:
      - `source_id`: UUID of the data source.
    - Example: `http://127.0.0.1:8000/api/v1/data_sources/{source_id}`

  ### Examples

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
</details>

## Photos

<details open>
  <summary>Details</summary>
  
  ![image](https://github.com/liviuxyz-ctrl/DataWarehouse/assets/70070368/30ad1780-90cc-49cb-be44-45df3acffbeb)
  
  ![image](https://github.com/liviuxyz-ctrl/DataWarehouse/assets/70070368/d81a715e-cfc0-4b3e-b62c-87fb8dbeb35d)

  ![image](https://github.com/liviuxyz-ctrl/Financial-DataWarehouse/assets/70070368/64c7257a-5ed7-4c5f-b835-c27c40fcc05c)

</details>

## License

<details>
  <summary>Details</summary>
  Licensed under the MIT License. See [LICENSE.md](LICENSE) for more details.
</details>

