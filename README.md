# Zillow Scraper Installation Guide

## Retrieve code

* `$ https://github.com/realchief/zillow-scraping.git`

## Create Vritual Environment

* `$ sudo apt-get install python-virtualenv`
* `$ cd zillow_scraping`
* `$ virtualenv venv`
* `$ source venv/bin/activate`


## Install packages

* `$ pip install -r requirements.txt`


## Run spiders

* `$ cd zillow/spiders`
* `$ scrapy crawl scrapingdata -o result.csv`
* `$ scrapy crawl scrapingdata -o result.json`
