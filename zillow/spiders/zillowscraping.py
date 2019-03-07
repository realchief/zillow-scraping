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
    LOGIN_URL = 'https://www.zillow.com/user/account/services/Login.htm'
    LOCATION = 'Philadelphia'
    ZIP_CODE = '19019'
    USER_NAME = 'todor.dev000@gmail.com'
    PASSWORD = "password12345"
    settings.overrides['ROBOTSTXT_OBEY'] = False

    def __init__(self, **kwargs):
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
                                      " Chrome/70.0.3538.102 Safari/537.36"}

    def start_requests(self):
        yield Request(url=self.START_URL,
                      callback=self.login,
                      headers=self.headers,
                      dont_filter=True
                      )

    def login(self, response):

        yield FormRequest(url=self.LOGIN_URL,
                          callback=self.check_login,
                          headers=self.headers,
                          dont_filter=True,
                          method="POST",
                          formdata={
                              'ap': 'undefined',
                              'authToken': '',
                              'email': self.USER_NAME,
                              'password': self.PASSWORD
                          }
                          )

    def check_login(self, response):

        is_authenticated = json.loads(response.body)['succeeded']
        if is_authenticated:
            yield Request(url=self.START_URL,
                          callback=self.parse_category,
                          headers=self.headers,
                          dont_filter=True
                          )
        else:
            print ("login failed")

    def parse_category(self, response):

        category_link = self.START_URL + 'homes/for_sale/{zip_code}_rb/'.format(zip_code = self.ZIP_CODE)
        yield Request(url=category_link, callback=self.parse_page, dont_filter=True, headers=self.headers)

    def parse_page(self, response):
        total_product_urls = response.xpath('//a[contains(@class,"zsg-photo-card-overlay-link")]/@href').extract()
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
