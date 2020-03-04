# web-scraper

## Table of Contents
* [Routing](#routing)
* [Setup and Run](#setup-and-run)
* [Contact](#contact)

## Routing
### Scrape text
To scrape text from a website send POST request on:
```url
/text-scraper/
```
with JSON raw data:
```JSON
{
  "website-url": "http://sample.com"
}
```

### Scrape images
To scrape images from a website send POST request on:
```url
/image-scraper/
```
with JSON raw data:
```JSON
{
  "website-url": "http://sample.com"
}
```

### Download scraped data
To download scraped data send GET request on:
```url
/download-scraped-data/<int:id>/
```
where id is scraping index returned in scrap response.

## Setup and Run
You need to have installed [Docker](https://www.docker.com/).

Clone or download the repo. Open your terminal pointing to the project root directory. To run the aplication type:

```bash
# start the server in the background
docker-compose up -d 

# apply migrations
docker-compose exec web python /code/manage.py migrate --noinput
```

You can also create admin user by typing:
```bash
# create superuser
docker-compose exec web python /code/manage.py createsuperuser
```

To run tests type:
```bash
docker-compose exec web python /code/manage.py test
```

## Contact
Created by [@patrykwiener](https://github.com/patrykwiener). 

Feel free to contact me on [My LinkedIn](https://www.linkedin.com/in/patryk-wiener-439074182/)!
