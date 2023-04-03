## Beer API

### Overview
This a Beer Recipe API

### Main features:
- FastAPI framework
- async HTTP requests using `httpx` library
- data stored in database with `postgresql`
- SQL queries and table models with ORM provided by `SQLalchemy`
- data validation and data modelling with `pydantic`

### Beer recipes
Beer recipes are provided by an external API `Punk API` at 
`https://punkapi.com/documentation/v2`

### Supported operations are:
- get average fermentation temperature by hop
- get average fermentation temperature for primary hops per beer
- get 10 most used hops in the recipes
- get the beers that use a particular hop

### Requests
Async requests to the external API were made using `httpx` library 
to get all 325 beer recipes in JSON format.

### Database
JSON response has a nested structure and many missing data therefore only 
required data was extracted and saved to a database. 2 tables were created 
"beers" and "hops" with required relationships. Database created with `postgres` 
and `SQLAlchemy`

### Dependencies
Dependency management is handled using `requirements.txt` file

### Docker setup
1. Create docker container `docker compose up -d`
2. See the status `docker compose status`
3. Delete docker container `docker compose down -v`

### Local setup
1. Install dependencies from `requirements.txt`
2. Run the app: `uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload`

### How to run application
Make sure to hit `/data` endpoint first. It will fetch data from Punk API and save it to database.
Only then you can hit other endpoints.

### Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at index page `/docs`

### Endpoints
| Method | Endpoint                            | Description                                                       |
|--------|-------------------------------------|-------------------------------------------------------------------|
| GET    | /data                               | Making a request to beer API, storing data in DB                  |
| GET    | /avg_fermentation_temp_by_hop       | Get average (mean) fermentation temperature for each type of hops |
| GET    | /avg_fermentation_temp_primary_hops | Get average fermentation temperature for the primary hops         |
| GET    | /get_10_most_used_hops              | Show the top 10 most used hops in the recipes                     |
| GET    | /get_beers_by_hop/{hop_name}        | Show the beers that use a particular hop                          |

## Examples
GET `/data`
```json
{
  "message": "Data requested from Punk API and stored in database"
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
  {
    "name": "American Oak Chips Heavy Toast soaked in Speyside Whisky",
    "avg_beer_fermentation_temp": 19
  },
  ...
]
```
GET `/avg_fermentation_temp_primary_hops`
```json
{
  "TBA": "TBA"
}
```
GET `/get_10_most_used_hops`
```json
{
  "Simcoe": 6861.01,
  "Centennial": 5605.6900000000005,
  "Amarillo": 5591.6900000000005,
  "Citra": 5172.25,
  "Chinook": 4625.66,
  "Honey": 4410,
  "Raspberry Juice": 3800,
  "Columbus": 3142.0800000000004,
  "Cascade": 2710.45,
  "Mosaic": 2168
}
}
```
GET `/get_beers_by_hop/Fuggles`
```json
[
  {
    "beer_id": 1
  },
  {
    "beer_id": 1
  },
  {
    "beer_id": 11
  },
  {
    "beer_id": 11
  },
  {
    "beer_id": 27
  },
  ...
]
```

