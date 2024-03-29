## Beer API

### Overview
This a Beer Recipe API

### Main features:
- FastAPI framework
- async HTTP requests using `httpx` library
- data stored in database with `sqlite`
- SQL queries and table models with ORM provided by `SQLalchemy`
- data validation and data modelling with `pydantic`
- environment variable management with `pydantic-settings`
- authentication via API key in headers
- dependency management with `poetry` and `pyproject.toml`
- `pre-commit` tool with `black` and `ruff` as formatters and linters

### Beer recipes
Beer recipes are provided by an external API `Punk API` at 
`https://punkapi.com/documentation/v2`

### Supported operations are:
- `MANDATORY FIRST REQUEST` Making a request to Punk API, storing data in DB
- Get average fermentation temperature for each type of hops
- Get average fermentation temperature for the primary hops
- Show the top 10 most used hops in the recipes
- Get all beers that have a fermentation temperature greater than X
- Get all hops that have an amount greater than or equal to X
- Get all beers that have a hop with the name X

### Requests
Async requests to the external API were made using `httpx` library 
to get all 325 beer recipes in JSON format.

### Database
JSON response has a nested structure and many missing data therefore only 
required data was extracted and saved to a database. 
2 tables were created "beers" and "hops" with required relationships. 
Database created with `sqlite`and `SQLAlchemy`

### Authentication
To authenticate incoming requests, we check the `x-api-key` header.
Create the `.env` file (use the `.env.dist` for reference) 
and add `API_KEY` to environment variables.

### Dependencies
Dependency management is handled with `poetry` and `pyproject.toml`

### Docker setup
1. Start the application by running the following command `docker-compose up --build -d`
2. You can access the application at `http://localhost:9080` on linux/windows or `http://0.0.0.0:9080` on mac.
3. SwaggerUI is accessible at `/docs` endpoint.

### How to run application
Make sure to hit mandatory `/data` endpoint first. It will fetch data 
from Punk API and save it to database. It will take 20-30 seconds to fetch all data. 
You can hit other endpoints after successfully executing `/data` endpoint.

### Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at index page `/docs`

### Status codes
| Status code | Description       |
|-------------|-------------------|
| 200         | success           |
| 400         | Bad request       |
| 404         | Not found         |
| 424         | Failed dependency |

### Health Endpoint
| Method | Endpoint | Description  |
|--------|----------|--------------|
| GET    | /ping    | Health check |

### Data Endpoints
| Method | Endpoint | Description                                                                |
|--------|----------|----------------------------------------------------------------------------|
| GET    | /data    | `MANDATORY FIRST REQUEST` Making a request to beer API, storing data in DB |

### Beer Endpoints
| Method | Endpoint                            | Description                                                       |
|--------|-------------------------------------|-------------------------------------------------------------------|
| GET    | /avg_fermentation_temp_by_hop       | Get average fermentation temperature for each type of hops        |
| GET    | /avg_fermentation_temp_primary_hops | Get average fermentation temperature for the primary hops         |
| GET    | /get_10_most_used_hops              | Show the top 10 most used hops in the recipes                     |
| GET    | /beers_by_temp                      | Get all beers that have a fermentation temperature greater than X |
| GET    | /hops_by_amount                     | Get all hops that have an amount greater than or equal to X       |
| GET    | /beers_by_hop                       | Get all beers that have a hop with the name X                     |

## Examples
GET `/data`
```json
{
  "message": "Data successfully requested from Punk API and stored in database. You can can query data now."
}
```
GET `/avg_fermentation_temp_by_hop`
```json
[
  {
    "name": "1 lemon drop chilli",
    "avg_beer_fermentation_temp": 21
  },
  {
    "name": "Ahtanum",
    "avg_beer_fermentation_temp": 18.7
  },
  {
    "name": "Amarillo",
    "avg_beer_fermentation_temp": 19.3
  },
  {
    "name": "American Oak Chips Heavy Toast Soaked in Bourbon",
    "avg_beer_fermentation_temp": 19
  },
]
```
GET `/avg_fermentation_temp_primary_hops`
```json
[
  {
    "id": 1,
    "name": "Buzz",
    "primary_hop_name": "Cascade",
    "max_amount": 37.5,
    "avg_beer_fermentation_temp": 18.8
  },
  {
    "id": 1,
    "name": "Buzz",
    "primary_hop_name": "First Gold",
    "max_amount": 37.5,
    "avg_beer_fermentation_temp": 19.4
  },
  {
    "id": 1,
    "name": "Buzz",
    "primary_hop_name": "Fuggles",
    "max_amount": 37.5,
    "avg_beer_fermentation_temp": 18.9
  },
]
```
GET `/most_used_hops`
```json
{
  "Simcoe": 6531,
  "Centennial": 5605.7,
  "Amarillo": 5576.7,
  "Citra": 5157.3,
  "Chinook": 4625.7,
  "Honey": 4410,
  "Raspberry Juice": 3800,
  "Columbus": 3142.1,
  "Cascade": 2710.5,
  "Mosaic": 2168
}
```
GET `/beers_by_temp?temp=20`
```json
[
  {
    "id": 76,
    "fermentation_temp": 21,
    "name": "#Mashtag 2013"
  },
  {
    "id": 136,
    "fermentation_temp": 21,
    "name": "#Mashtag 2014"
  },
  {
    "id": 90,
    "fermentation_temp": 21,
    "name": "#Mashtag 2015"
  },
]
```
GET `/hops_by_amount?amount=1000`
```json
[
  {
    "id": 1476,
    "add": "Flame out",
    "beer_id": 271,
    "name": "Raspberry Juice",
    "amount": 3000,
    "attribute": "Flavour"
  },
  {
    "id": 1564,
    "add": "Flame Out",
    "beer_id": 286,
    "name": "Fresh Strawberries",
    "amount": 2000,
    "attribute": "Flavour"
  },
]
```
GET `/beers_by_hop?hop_name=Raspberry%20Juice`
```json
[
  {
    "name": "Small Batch: Cranachan Cream Ale",
    "id": 271,
    "fermentation_temp": 19
  },
  {
    "name": "Raspberry Popsicle Parade",
    "id": 299,
    "fermentation_temp": 21
  },
]
```
