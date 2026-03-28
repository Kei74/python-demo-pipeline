# Demo Pipeline
**mock-server** reads and serves data from a file
**pipeline-service** ingests data from mock-server and saves it to Postgres. Endpoints are available to fetch ingested data.
## Instructions:
0. Prerequisites: 
    - Git
    - Docker 
1. Clone the repo via running `https://github.com/Kei74/python-demo-pipeline.git`
2. Start the containers via running `docker compose up`
3. Test the endpoints for mock-server at http://localhost:5000 and pipeline-service at http://localhost:8000


## Mock-Server
Mock API data source, reading and serving data from the `mock-server/data/customers.json` file.

### Endpoints:
1. `GET /api/health`
    - Simple health check
2. `GET /api/customers?page=1&limit=5`
    - Returns all customers paginated as per query params
    - Response format: 
    ```json
    {
        "data": [], // Array of Customers
        "limit": 5, // Limit Customers per page
        "page": 1,  // Page Number
        "total": 2  // Total number of Customers in all pages
    }
    ```
3. `GET /api/customers/{customer_id}`
    - Return customer by id
    - Returns 404 if customer is not found

### Limitations:
Currently the contents of the `/data/customers.json` file are loaded into memory on service start. This is memory inefficient for large datasets, and edits to the dataset would not be reflected until the service is restarted.

## Pipeline-service
Data ingestion pipeline service.
Dependencies;
- FastAPI for API endpoints
- SQLAlchemy as ORM for querying Postgres
- dtl for data ingestion from mock-server

### Endpoints:

1. `GET /api/health`
    - Simple health check
2. `POST /api/ingest`
    - Ingests customers from mock-server
    - Returns number of records ingested
2. `GET /api/customers?page=1&limit=5`
    - Returns all customers paginated as per query params
3. `GET /api/customers/{customer_id}`
    - Return customer by id
    - Returns 404 if customer is not found