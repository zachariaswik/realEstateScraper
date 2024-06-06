This code demonstrates how to web scrape pisos.com using Scrapy and store the data in a SQLite database.

# Steps to Run the Scraper

1. Navigate to the Project Directory:
```cd pisosScraper```
3. Create the SQLite Database: 
```python create_db.py```
3. Run the Scraper:
```scrapy crawl PisosListingScraper```

# Database Structure

The first command creates a SQLite database with the following columns:


| Columns         | Description |
| -------- | ------- |
| listingName   | webpage URL used as primary key |
| location      | example "Barcelona_Barcelonès_Badalona_Centre" |
| price         | price |
| bathrooms     | number of bathrooms |
| sizeConstr    | size of construction, in square meters |
| sizeUtil      | size of usable area, in square meters | 
| sizeSolar     | size of outside area, in square meters |
| floor         | floor number | 
| type          | type of listing |
| exterior      | has external facade | 
| interior      | has internal facade |
| age           | age, in years |
| state         | condition  |
| reference     | reference number | 
| communityCost | monthly commmunity cost |
| description   | description |
| Erating       | energy electrical rating |
| CO2rating     | energy carbon rating |
| Econsumption  | electrical consumption |
| CO2emission   | carbon emission |
| last_update   | last update of listing | 

# Scraping Process

The second command initiates the web scraping using PisosListingScraper, described below.

PisosListingScraper starts at this URL, https://www.pisos.com/en/viviendas/barcelona/,  which provides a hierarchical location search. It begins from Barcelona and drills down into smaller regions. The initial region is shown below:

__Initial region__

<img width="296" alt="Screenshot 2024-06-06 at 12 08 25" src="https://github.com/zachariaswik/realEstateScraper/assets/45999030/6704d62a-c6b3-40e1-bb0f-eae9eedb95b3">


The search continues until there are no more subregions, leading to the listings page:

__Listings page__

<img width="629" alt="Screenshot 2024-06-06 at 12 10 24" src="https://github.com/zachariaswik/realEstateScraper/assets/45999030/191ff319-d799-4a15-b46c-96c930498cd2">

From the listings page, the crawler visits every page and listing to collect available data:

<img width="236" alt="Screenshot 2024-06-06 at 12 24 45" src="https://github.com/zachariaswik/realEstateScraper/assets/45999030/d98e14ed-b100-4d71-8ff4-84af4e757d90">

<img width="228" alt="Screenshot 2024-06-06 at 12 24 55" src="https://github.com/zachariaswik/realEstateScraper/assets/45999030/bfc1d52c-8e56-4b7c-9733-756ed4126bba">

<img width="229" alt="Screenshot 2024-06-06 at 12 25 07" src="https://github.com/zachariaswik/realEstateScraper/assets/45999030/91926884-76da-4c26-b35b-2c35a586d916">


Finally, the data is extracted according to the definitions in pipeline.py and stored in pisos_listings.db.




