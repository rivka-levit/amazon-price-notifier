# Amazon Price Notifier

## Send an email when the price changes

The app allows a user to pass the url of a product from amazon.com, 
and receive an email when the price changes.

#### Core Features:

- Flask application
- Selenium for scraping price from Amazon
- OOP using pattern 'Observer'
- Dockerized
- Unit tests

Command to run the app in container:

```commandline
docker compose up
```

Command to run tests:

```commandline
docker compose run --rm web sh -c "python -m unittest -v"
```