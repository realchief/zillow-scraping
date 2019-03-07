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

    ContactInfo = Field()
    Address = Field()
    Rent = Field()
    # Number_of_Active_Listing = Field()


class ZillowScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.zillow.com']
    DOMAIN_URL = 'https://www.zillow.com'
    START_URL = 'https://www.zillow.com/'
    LOGIN_URL = 'https://www.zillow.com/user/account/services/Login.htm'
    GRAPH_QL_URL = 'https://www.zillow.com/graphql/'
    LOCATION = 'Philadelphia'
    ZIP_CODE = '19019'
    USER_NAME = 'todor.dev000@gmail.com'
    PASSWORD = "password12345"
    settings.overrides['ROBOTSTXT_OBEY'] = False
    REQUEST_URL = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=110001&lt=111101&ht=111111&pr=,&mp=,' \
                  '&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0&parking=0&laundry=0&' \
                  'income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0&cheap-apartments=0&' \
                  'studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=1&pf=1&sch=100111&zoom=12&' \
                  'rect=-75083142,40061979,-74936715,40178020&p=1&sort=days&search=maplist&rid=65700&rt=7&' \
                  'listright=true&isMapSearch=true&zoom=12'

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
        yield Request(url=category_link, callback=self.get_zpid, dont_filter=True, headers=self.headers)

    def get_zpid(self, response):

        headers_zpid = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'referer': response.url
        }
        response_content = requests.get(self.REQUEST_URL, headers=headers_zpid).content
        json_content = json.loads(response_content)
        list_html = json_content['list']['listHTML']
        zpid_list = re.findall('data-zpid="(.*?)"', list_html)
        for zpid in zpid_list:
            zpid_data = {
                "operationName": "NewConstructionFullRenderQuery",
                "variables": {
                    "zpid": zpid,
                    "contactFormRenderParameter": {
                        "zpid": zpid,
                        "platform": "desktop",
                        "isDoubleScroll": "false"
                    }
                },
                "queryId": "a9442e54042cd22a054e6a2f973fe7b2",
                "clientVersion": "home-details/5.41.0.0.0.hotfix-2019-03-01.29df601"
            }

            zpid_headers = {

                'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
                'content-type': 'text/plain'
            }
            yield FormRequest(
                url=self.GRAPH_QL_URL,
                method='POST',
                body=json.dumps(zpid_data),
                callback=self.parse_product,
                dont_filter=True,
                headers=zpid_headers
            )

    def parse_product(self, response):

        product = SiteProductItem()

        ContactInfo = self._parse_ContactInfo(response)
        product['ContactInfo'] = ContactInfo

        address = self._parse_address(response)
        product['Address'] = address

        rent = self._parse_rent(response)
        product['Rent'] = rent

        yield product

    @staticmethod
    def _parse_ContactInfo(response):

        json_content = json.loads(response.body)
        nc_community_data = json_content['data']['ncCommunity']
        ContactInfo = None
        if nc_community_data:
            ContactInfo = nc_community_data['contactData']['phoneNumber']

        return str(ContactInfo) if ContactInfo else None

    @staticmethod
    def _parse_address(response):

        json_content = json.loads(response.body)
        property_data = json_content['data']['property']
        address = None
        if property_data:
            address_info = property_data['address']
            city = address_info['city']
            state = address_info['state']
            streetAddress = address_info['streetAddress']
            zipcode = address_info['zipcode']
            address = str(streetAddress) + ", " + str(city) + ", " + str(state) + ", " + str(zipcode)
        return address if address else None

    @staticmethod
    def _parse_rent(response):

        json_content = json.loads(response.body)
        property_data = json_content['data']['property']
        price = None
        if property_data:
            adTargets = property_data['adTargets']
            price = adTargets['price']
        return str(price) if price else None
