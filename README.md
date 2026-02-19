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
Python Script

### Shared
MySQL database connection and schema via Python. Used by API and scraper to directly connect and manipulate DB.



## Project Roadmap
