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
    Number_of_Active_Listing = Field()
    Number_of_Bedrooms = Field()
    Info_of_Days_Vacant = Field()
    PhoneNumber = Field()
    ZipCode = Field()
    Email = Field()


class ZillowScraper (scrapy.Spider):
    name = "scrapingdata"
    allowed_domains = ['www.zillow.com']
    DOMAIN_URL = 'https://www.zillow.com'
    START_URL = 'https://www.zillow.com/'
    RENT_URL = 'https://www.zillow.com/homes/for_rent/'
    LOGIN_URL = 'https://www.zillow.com/user/account/services/Login.htm'
    GRAPH_QL_URL = 'https://www.zillow.com/graphql/'
    LOCATION = 'Philadelphia'
    ZIP_CODE_LIST = ['19153', '19145', '19148', '19142', '19143', '19146', '19147', '19106', '19107', '19103', '19102',
                     '19104', '19130', '19123', '19125', '19122', '19121', '19132', '19133', '19134', '19129', '19140']
    ZIP_CODE = '19122'
    EMAIL = 'todor.dev000@gmail.com'
    PASSWORD = "password12345"
    # settings.overrides['ROBOTSTXT_OBEY'] = False

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
                              'email': self.EMAIL,
                              'password': self.PASSWORD
                          },
                          meta=response.meta
                          )

    def check_login(self, response):

        is_authenticated = json.loads(response.body)['succeeded']
        if is_authenticated:
            yield Request(url=self.START_URL,
                          callback=self.parse_category,
                          headers=self.headers,
                          dont_filter=True,
                          meta=response.meta
                          )
        else:
            print ("login failed")

    def parse_category(self, response):

        for zip_code in self.ZIP_CODE_LIST:
            response.meta['zip_code'] = zip_code
            category_link = 'https://www.zillow.com/homes/{zip_code}_rb/13_zm/'.format(zip_code=zip_code)
            yield Request(url=category_link, callback=self.get_zpid, dont_filter=True, headers=self.headers,
                          meta=response.meta)

        # zip_code = self.ZIP_CODE
        # response.meta['zip_code'] = zip_code
        # category_link = 'https://www.zillow.com/homes/{zip_code}_rb/13_zm/'.format(zip_code=zip_code)
        # yield Request(url=category_link, callback=self.get_zpid, dont_filter=True, headers=self.headers,
        #               meta=response.meta)

    def get_zpid(self, response):

        headers_zpid = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'referer': response.url
        }

        request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111&pr=,' \
                      '&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0&parking=0' \
                      '&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                      '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0' \
                      '&pf=0&sch=100111&zoom=12&rect=-75314541,39827588,-75168114,39944028&p=1&sort=paymenta' \
                      '&search=map&rid=65820&rt=7&listright=true&isMapSearch=1&zoom=12'

        if '19153' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=12&rect=-75314541,39827588,-75168114,39944028&p=1&sort=paymenta' \
                          '&search=map&rid=65820&rt=7&listright=true&isMapSearch=1&zoom=12'
        if '19145' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75230427,39885734,-75157214,39943929&p=1&sort=paymenta&search=map' \
                          '&rid=65812&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19148' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75188542,39882770,-75115328,39940968&p=1&sort=paymenta' \
                          '&search=map&rid=65815&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19142' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000' \
                          '&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C' \
                          '&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0' \
                          '&furnished-apartments=0&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0' \
                          '&days=any&ds=all&pmf=0&pf=0&sch=100111&zoom=14&rect=-75249997,39909127,-75213390,39938221' \
                          '&p=1&sort=paymenta&search=map&rid=65809&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19143' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75264845,39911283,-75191632,39969457&p=1&sort=paymenta' \
                          '&search=map&rid=65810&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19146' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000' \
                          '&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C' \
                          '&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0' \
                          '&furnished-apartments=0&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0' \
                          '&days=any&ds=all&pmf=0&pf=0&sch=100111&zoom=13&rect=-75224505,39910822,-75151291,39968996' \
                          '&p=1&sort=paymenta&search=map&rid=65813&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19147' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0&' \
                          'sch=100111&zoom=13&rect=-75189915,39909374,-75116702,39967549&p=1&sort=paymenta' \
                          '&search=map&rid=65814&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19106' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000' \
                          '&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C' \
                          '&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0' \
                          '&furnished-apartments=0&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0' \
                          '&days=any&ds=all&pmf=0&pf=0&sch=100111&zoom=14&rect=-75163093,39934733,-75126486,39963816' \
                          '&p=1&sort=paymenta&search=map&rid=65774&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19107' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=14&rect=-75176955,39937069,-75140348,39966151&p=1&sort=paymenta' \
                          '&search=map&rid=65775&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19103' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000' \
                          '&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C' \
                          '&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0' \
                          '&furnished-apartments=0&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0' \
                          '&days=any&ds=all&pmf=0&pf=0&sch=100111&zoom=14&rect=-75194679,39941577,-75158072,39970657' \
                          '&p=1&sort=paymenta&search=map&rid=65771&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19102' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0' \
                          '&pf=0&sch=100111&zoom=14&rect=-75183993,39937958,-75147386,39967039&p=1&sort=paymenta' \
                          '&search=map&rid=65770&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19104' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000' \
                          '&ht=111111&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C' \
                          '&pho=0&pets=0&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0' \
                          '&furnished-apartments=0&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0' \
                          '&days=any&ds=all&pmf=0&pf=0&sch=100111&zoom=13&rect=-75233088,39931360,-75159874,39989517' \
                          '&p=1&sort=paymenta&search=map&rid=65772&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19130' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=14&rect=-75194893,39953487,-75158287,39982562&p=1&sort=paymenta' \
                          '&search=map&rid=65797&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19123' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0' \
                          '&pf=0&sch=100111&zoom=14&rect=-75164123,39948157,-75127516,39977235&p=1&sort=paymenta' \
                          '&search=map&rid=65790&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19125' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0' \
                          '&pf=0&sch=100111&zoom=13&rect=-75160218,39946496,-75087004,40004640&p=1&sort=paymenta' \
                          '&search=map&rid=65792&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19122' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0' \
                          '&pf=0&sch=100111&zoom=14&rect=-75164295,39963059,-75127688,39992130&p=1&sort=paymenta' \
                          '&search=map&rid=65789&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19121' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75216952,39954326,-75143738,40012463&p=1&sort=paymenta' \
                          '&search=map&rid=65788&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19132' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75209227,39967352,-75136014,40025478&p=1&sort=paymenta' \
                          '&search=map&rid=65799&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19133' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=14&rect=-75159960,39978090,-75123354,40007154&p=1&sort=paymenta' \
                          '&search=map&rid=65800&rt=7&listright=true&isMapSearch=1&zoom=14'
        if '19134' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75143309,39958931,-75070096,40017064&p=1&sort=paymenta' \
                          '&search=map&rid=65801&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19129' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75221243,39985439,-75148030,40043550&p=1&sort=paymenta' \
                          '&search=map&rid=65796&rt=7&listright=true&isMapSearch=1&zoom=13'
        if '19140' in response.url:
            request_url = 'https://www.zillow.com/search/GetResults.htm?spt=homes&status=000010&lt=000000&ht=111111' \
                          '&pr=,&mp=,&bd=0%2C&ba=0%2C&sf=,&lot=0%2C&yr=,&singlestory=0&hoa=0%2C&pho=0&pets=0' \
                          '&parking=0&laundry=0&income-restricted=0&fr-bldg=0&condo-bldg=0&furnished-apartments=0' \
                          '&cheap-apartments=0&studio-apartments=0&pnd=0&red=0&zso=0&days=any&ds=all&pmf=0&pf=0' \
                          '&sch=100111&zoom=13&rect=-75184165,39983401,-75110951,40041513&p=1&sort=paymenta' \
                          '&search=map&rid=65807&rt=7&listright=true&isMapSearch=1&zoom=13'

        response_content = requests.get(request_url, headers=headers_zpid).content
        json_content = json.loads(response_content)
        properties = json_content['map']['properties']

        for property in properties:
            zpid = property[0]
            zpid_data = {
                "operationName": "ForRentFullRenderQuery",
                "variables": {
                    "zpid": zpid,
                    "contactFormRenderParameter": {
                        "zpid": zpid,
                        "platform": "desktop",
                        "isDoubleScroll": "false"
                    }
                },
                "queryId": "ebd67590aabde8f7381e643bfefff0bb",
                "clientVersion": "home-details/5.41.1.0.0.hotfix-2019-03-08.d7df593"
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
                headers=zpid_headers,
                meta=response.meta
            )

    def parse_product(self, response):

        product = SiteProductItem()

        product['ZipCode'] = response.meta['zip_code']
        product['Email'] = self.EMAIL

        PhoneNumber = self._parse_phone_number(response)
        product['PhoneNumber'] = PhoneNumber

        ContactInfo = self._parse_contact_info(response)
        product['ContactInfo'] = ContactInfo

        daysVacant = self._parse_days_vacant(response)
        product['Info_of_Days_Vacant'] = daysVacant

        address = self._parse_address(response)
        product['Address'] = address

        rent = self._parse_rent(response)
        product['Rent'] = rent

        Number_of_Active_Listing = self._parse_number_of_active_listing(response)
        product['Number_of_Active_Listing'] = Number_of_Active_Listing

        json_content = json.loads(response.body)
        property_data = json_content['data']['property']
        bedrooms = property_data['bedrooms']
        product['Number_of_Bedrooms'] = bedrooms

        crawl_enable = False
        if rent and bedrooms:
            if (bedrooms == 1) and (int(rent) > 1200):
                crawl_enable = True
            if (bedrooms == 2) and (int(rent) > 1500):
                crawl_enable = True
            if (bedrooms == 3) and (int(rent) > 1800):
                crawl_enable = True
            if (bedrooms == 4) and (int(rent) > 2100):
                crawl_enable = True
            if (bedrooms == 5) and (int(rent) > 2400):
                crawl_enable = True
            if (bedrooms == 6) and (int(rent) > 2700):
                crawl_enable = True
            if (int(bedrooms) > 6) and (int(rent) > 3000):
                crawl_enable = True
            if bedrooms == 0:
                crawl_enable = True
            if bedrooms == '0':
                crawl_enable = True
        if not bedrooms:
            crawl_enable = True

        if crawl_enable:
            yield product

    @staticmethod
    def _parse_phone_number(response):

        json_content = json.loads(response.body)
        property_data = json_content['data']['property']
        phone_number = None
        if 'listingProvider' in property_data.keys():
            phone_number = property_data['listingProvider']['phoneNumber']

        return str(phone_number) if phone_number else None

    @staticmethod
    def _parse_days_vacant(response):

        try:
            json_content = json.loads(response.body)
            property_data = json_content['data']['property']
            daysVacant_info = None
            if 'homeFacts' in property_data.keys():
                daysVacant_info_list = property_data['homeFacts']['categoryDetails'][0]['categories'][0]['categoryFacts']
                for index in range(0, len(daysVacant_info_list)):
                    if 'ago' in daysVacant_info_list[index]['factValue']:
                        if ('hour' in daysVacant_info_list[index]['factValue']) or ('minute' in daysVacant_info_list[index]['factValue']):
                            daysVacant_info = '1 day ago'
                        else:
                            daysVacant_info = str(daysVacant_info_list[index]['factValue'])
                    else:
                        continue
            return daysVacant_info if daysVacant_info else None
        except:
            pass

    @staticmethod
    def _parse_contact_info(response):

        json_content = json.loads(response.body)
        property_data = json_content['data']['property']
        ContactInfo = None
        if 'listingProvider' in property_data.keys():
            phone_number = property_data['listingProvider']['phoneNumber']
            ContactInfo = str(phone_number)
            if not phone_number:
                ContactInfo = ''
            postingGroupName = property_data['listingProvider']['postingGroupName']
            if postingGroupName and ContactInfo:
                ContactInfo = str(postingGroupName) + '  ' + ContactInfo
        return ContactInfo if ContactInfo else None

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

    @staticmethod
    def _parse_number_of_active_listing(response):

        number_of_active_listing = '1'
        return number_of_active_listing
