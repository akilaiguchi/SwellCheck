# Swellcheck
Automated bouy reading bot that sends selected NDBC buoy information to users via
telegram messages.

## Author Information
- Akila Iguchi
- akilamauihi@gmail.com

## Implementation Details


### Docker
Docker was used as the development environment. Custom configured Dockerfiles and docker-compose
file was used to create application container

### API
FastAPI 

### Bot
Telegram bot API

### init_db
Initialize native MySQL database

### Scraper
Celery worker to 


Scrape NDBC spectral wave data. Data dictionary is as follows:
- YYYY MM DD hh mm: Year month day hour minute
- WVHT: Significant wave height (meters) is calculated as the average of the highest one-third of all of the wave heights during the 20-minute sampling period
- SwH: This is the estimated average height of the highest one-third of the swells (meters)
- SwP: This is the peak period in seconds of the swells (sec)
- WWH: This is the average height of the highest one-third of the wind-waves (meters)
- WWP: This is the peak period in seconds of the wind-waves (sec)
- SwD: This is the direction that the swells are coming from (NESW)
- WWD: This is the direction that the wind-waves are coming from (NESW)
- STEEPNESS: For a given wave height, steep waves represent a more serious threat to capsizing vessels or damaging marine structures than broad swell. ("VERY STEEP", "STEEP", "AVERAGE", or "SWELL")
- APD: Average wave period (seconds) of all waves during the 20-minute period
- MWD: The direction from which the waves at the dominant period (DPD) are coming (deg)


### Shared
MySQL database connection and schema via Python. Used by API and scraper to directly connect and manipulate DB.



## Project Roadmap
