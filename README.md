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
Beer recipes are provided by an external API `Punk API` 
`https://punkapi.com/documentation/v2`

### Supported operations are:
- get average fermentation temperature by hop
- get average fermentation temperature for primary hops per beer
- get 10 most used hops in the recipes
- get the beers that use a particular hop

### Requests
Async requests to the external API were made using `httpx` library 
to get all 325 beer recipes in JSON format

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

### Documentation
Once the application is up and running, you can access FastAPI automatic docs 
at index page `/docs`

### Endpoints
| Method | Endpoint                            | Description                                                        |
|--------|-------------------------------------|--------------------------------------------------------------------|
| GET    | /avg_fermentation_temp_by_hop       | Get average (mean) fermentation temperature for each type of hops  |
| GET    | /avg_fermentation_temp_primary_hops | Get average fermentation temperature for the primary hops          |
| GET    | /get_10_most_used_hops              | Show the top 10 most used hops in the recipes                      |
| GET    | /get_beers_by_hop/{hop_name}        | Show the beers that use a particular hop                           |

## Examples
GET `/avg_fermentation_temp_by_hop`
```json
{
  "TBA": "TBA"
}
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
  "TBA": "TBA"
}
```
GET `/get_beers_by_hop/fuggles`
```json
{
  "TBA": "TBA"
}
```

