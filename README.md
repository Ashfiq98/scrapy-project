## Scrapy Project for Trip.com Data Scraping

This project is designed to dynamically scrape property data from Trip.com and store it efficiently in a PostgreSQL database, leveraging Docker for seamless setup and deployment. The project includes automated table creation, local storage of property images, and references to these images in the database. Additionally, testing and verification of the scraper functionality are incorporated to ensure high-quality data collection.

---
## Key Features

- **Dynamic Scraping**: Scrape property details such as titles, ratings, location, latitude/longitude, room types, prices, and images.
- **PostgreSQL Integration**: Use SQLAlchemy for database interactions, with automatic table creation and seamless data insertion.
- **Docker Support**: Simplifies setup using Docker Compose for managing the Scrapy project and PostgreSQL database.
- **Image Management**: Save images locally, with their file paths referenced in the database.
- **Automated Testing**: Test the scraping process and generate code coverage insights to ensure robust functionality.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Started](#getting-started)
3. [Running the Scraper](#running-the-scraper)
4. [Accessing Scraped Data](#accessing-scraped-data)
5. [Testing the Scraper](#testing-the-scraper)

---

## Prerequisites

Ensure you have the following installed:
- Docker
- Python 3.8+
- Git

---

## Getting Started

# Step 1: Clone the Repository
```bash
git clone https://github.com/Ashfiq98/scrapy-project.git
```
```bash
cd scrapy-project
```
```bash
code . # for entering into vs code
```
# Step 2: Build and Start the Docker Containers
```bash
docker-compose build
docker-compose up
docker-compose build --no-cache #use this if there is any problem in building
```
 * This will:

  * Start the PostgreSQL database.
  * Run the scraper (trip_com_spider.py) to scrape data from Trip.com.
  * Store the scraped data into the database and save it in JSON files for confirmation.
  * Running the Scraper
  * The scraper collects the following details from Trip.com:

     - Property Title
     - Rating
     - Location
     - Latitude & Longitude
     - Room Type
     - Price
     - Images
 * JSON Confirmation : 
     - After scraping, the data is also saved in JSON format. You can check the JSON files to confirm the scraped results.

# Accessing Scraped Data in the Database
 
 * To view the scraped data stored in the PostgreSQL database:
  - Enter the database container bash:
```bash
docker exec -it scrapy-project-db-1 bash
```
  - Log in to PostgreSQL:

```bash
psql -U user -d mydb
```
  - user: The PostgreSQL username.
  - mydb: The database name.
 
 * View the database tables:

```bash
\dt
```
 * Query the data from the hotels table:

```bash
SELECT * FROM hotels;
```
* You can see database inside pgAdmin go to :
  - http://localhost:5050/
    - username : admin@admin.com  (from docker-compose.yml)
    - password : admin (from docker-compose.yml)
   - go to
  - Servers 
    - Register 
      - server
        - (general tab)
        - name : mydb 
         - (Connection tab)  
         - Host name/address: db
         - Port: 5432 
         - Maintenance database: mydb (as defined in POSTGRES_DB)
         - username : user (as defined in POSTGRES_USER)
         - password : password (as defined in POSTGRES_USER)
- inside 'mydb' open query tool and run this command :
```bash
 SELECT * FROM hotels;
```   
### Testing the Scraper
 # Step 1: Set Up a Virtual Environment
   - Create and activate a virtual environment for testing.

* On Linux/macOS:
```bash
python3 -m venv my_env #if python3 isn't working , use python instead of python3
```
```bash
source my_env/bin/activate
```
* On Windows:
```bash
python -m venv my_env
```
```bash
my_env\Scripts\activate
```
 # Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```
 # Step 3: Run Tests
  * Run the tests for the spider:
```bash
pytest tests/
```
 # Step 4: Test Coverage
  * Check test coverage:
```bash
pytest tests/ --cov=trip_scraper.spiders.trip_com_spider
```
