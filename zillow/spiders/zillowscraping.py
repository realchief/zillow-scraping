from scrapy.conf import settings
from urllib import urlencode
from scrapy import Request
from lxml import html
import re
import scrapy
import json
from scrapy.item import Item, Field
from scrapy import FormRequest
import requests
from scrapy import Selector
from urllib import urlencode


class SiteProductItem(Item):
    Url = Field()
    ContactInfo = Field()
    Address = Field()
    Rent = Field()
    Number_of_Active_Listing = Field()


class ZillowScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.zillow.com']
    START_URL = 'https://www.zillow.com/'
    ZIP_CODE = '19019'

    def __init__(self, **kwargs):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) "
                                "AppleWebKit/537.36 (KHTML, like Gecko) "
                                "Chrome/57.0.2987.133 Safari/537.36"}

    def start_requests(self):
        yield Request(url=self.START_URL,
                      callback=self.parse_category,
                      headers=self.headers,
                      dont_filter=True
                      )

    def parse_category(self, response):

        if response.meta.has_key('url'):
            yield Request(url=response.meta['url'], callback=self.parse_product, dont_filter=True, headers=self.headers)
        else:
            assert_category_links = response.xpath('//div[@class="thirdNav"]//ul[@class="unlisted"]/li/a/@href').extract()
            for assert_category_link in assert_category_links:
                category_link = self.START_URL + assert_category_link
                yield Request(url=category_link, callback=self.parse_page, dont_filter=True, headers=self.headers, meta=response.meta)

    def parse_page(self, response):

        for prod_url in total_product_urls:
            yield Request(url=prod_url, callback=self.parse_product, dont_filter=True, headers=self.headers, meta=response.meta)

    def parse_product(self, response):

        product = SiteProductItem()
        product['Url'] = response.url

        ContactInfo = self._parse_ContactInfo(response)
        product['ContactInfo'] = ContactInfo

        yield product

    @staticmethod
    def _parse_ContactInfo(response):

        path_words = response.xpath('//div[@class="container-fluid"]//ul[@class="unlisted inline"]//a/text()').extract()
        ContactInfo = ''
        for path_word in path_words:
            ContactInfo = ContactInfo + '>' + path_word

        return ContactInfo
