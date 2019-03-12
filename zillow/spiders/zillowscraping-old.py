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
    name = "scrapingdata-old"
    allowed_domains = ['www.zillow.com']
    DOMAIN_URL = 'https://www.zillow.com'
    START_URL = 'https://www.zillow.com/'
    RENT_URL = 'https://www.zillow.com/homes/for_rent/'
    LOGIN_URL = 'https://www.zillow.com/user/account/services/Login.htm'
    GRAPH_QL_URL = 'https://www.zillow.com/graphql/'
    LOCATION = 'Philadelphia'
    ZIP_CODE_LIST = ['19153', '19145', '19148', '19142', '19143', '19146', '19147', '19106', '19107', '19103', '19102',
                     '19104', '19130', '19123', '19125', '19122', '19121', '19132', '19133', '19134', '19132', '19129'
                     '19140']
    ZIP_CODE = '19140'
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

        for zip_code in self.ZIP_CODE_LIST:
            category_link = 'https://www.zillow.com/homes/{zip_code}_rb/13_zm/'.format(zip_code=zip_code)
            yield Request(url=category_link, callback=self.get_zpid, dont_filter=True, headers=self.headers)

    def get_zpid(self, response):

        headers_zpid = {
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'referer': response.url
        }

        spt = re.search('"spt":"(.*?)",', response.body)
        if spt:
            spt = spt.group(1)

        status = re.search('"status":"(.*?)",', response.body)
        if status:
            status = status.group(1)

        lt = re.search('"lt":"(.*?)",', response.body)
        if lt:
            lt = lt.group(1)

        ht = re.search('"ht":"(.*?)",', response.body)
        if ht:
            ht = ht.group(1)

        pr = re.search('"pr":"(.*?)",', response.body)
        if pr:
            pr = pr.group(1)

        mp = re.search('"mp":"(.*?)",', response.body)
        if mp:
            mp = mp.group(1)

        bd = re.search('"bd":"(.*?)",', response.body)
        if bd:
            bd = bd.group(1)

        ba = re.search('"ba":"(.*?)",', response.body)
        if ba:
            ba = ba.group(1)

        sf = re.search('"sf":"(.*?)",', response.body)
        if sf:
            sf = sf.group(1)

        lot = re.search('"lot":"(.*?)",', response.body)
        if lot:
            lot = lot.group(1)

        yr = re.search('"yr":"(.*?)",', response.body)
        if yr:
            yr = yr.group(1)

        singlestory = re.search('"singlestory":"(.*?)",', response.body)
        if singlestory:
            singlestory = singlestory.group(1)

        hoa = re.search('"hoa":"(.*?)",', response.body)
        if hoa:
            hoa = hoa.group(1)

        pho = re.search('"pho":"(.*?)",', response.body)
        if pho:
            pho = pho.group(1)

        pets = re.search('"pets":"(.*?)",', response.body)
        if pets:
            pets = pets.group(1)

        parking = re.search('"parking":"(.*?)",', response.body)
        if parking:
            parking = parking.group(1)

        laundry = re.search('"laundry":"(.*?)",', response.body)
        if laundry:
            laundry = laundry.group(1)

        income_restricted = re.search('"restricted":"(.*?)",', response.body)
        if income_restricted:
            income_restricted = income_restricted.group(1)

        fr_bldg = re.search('fr\\\-bldg":"(.*?)",', response.body)
        if fr_bldg:
            fr_bldg = fr_bldg.group(1)

        condo_bldg = re.search('condo\\\-bldg":"(.*?)",', response.body)
        if condo_bldg:
            condo_bldg = condo_bldg.group(1)

        furnished_apartments = re.search('furnished\\\-apartments":"(.*?)",', response.body)
        if furnished_apartments:
            furnished_apartments = furnished_apartments.group(1)

        cheap_apartments = re.search('cheap\\\-apartments":"(.*?)",', response.body)
        if cheap_apartments:
            cheap_apartments = cheap_apartments.group(1)

        studio_apartments = re.search('studio\\\-apartments":"(.*?)",', response.body)
        if studio_apartments:
            studio_apartments = studio_apartments.group(1)

        pnd = re.search('"pnd":"(.*?)",', response.body)
        if pnd:
            pnd = pnd.group(1)

        red = re.search('"red":"(.*?)",', response.body)
        if red:
            red = red.group(1)

        zso = re.search('"zso":"(.*?)",', response.body)
        if zso:
            zso = zso.group(1)

        days = re.search('"days":"(.*?)",', response.body)
        if days:
            days = days.group(1)

        ds = re.search('"ds":"(.*?)",', response.body)
        if ds:
            ds = ds.group(1)

        pmf = re.search('"pmf":"(.*?)",', response.body)
        if pmf:
            pmf = pmf.group(1)

        pf = re.search('"pf":"(.*?)",', response.body)
        if pf:
            pf = pf.group(1)

        sch = '100111'
        p = '1'

        sw_lat = re.search('"sw": { "lat": (.*?),', response.body)
        if sw_lat:
            sw_lat = sw_lat.group(1).replace('\\', '').replace('.', '').replace(' ', '')

        sw_lon = re.search('"lon": (.*?)},', response.body)
        if sw_lon:
            sw_lon = sw_lon.group(1).replace('\\', '').replace('.', '').replace(' ', '')

        ne_lat = re.search('"ne": { "lat": (.*?),', response.body)
        if ne_lat:
            ne_lat = ne_lat.group(1).replace('\\', '').replace('.', '').replace(' ', '')

        ne_lon = re.search('"lon": (.*?)},', response.body)
        if ne_lon:
            ne_lon = ne_lon.group(1).replace('\\', '').replace('.', '').replace(' ', '')

        rect = sw_lon + ',' + sw_lat + ',' + ne_lon + ',' + ne_lat

        sort = re.search('"sort":"(.*?)",', response.body)
        if sort:
            sort = sort.group(1)

        search = 'map'

        rid = re.search('"regionId" : (.*?),', response.body)
        if rid:
            rid = rid.group(1)

        rt = '7'
        listright = 'true'
        isMapSearch = '1'
        zoom = '13'

        request_url = 'https://www.zillow.com/search/GetResults.htm?spt={spt}&status={status}&lt={lt}&ht={ht}' \
                      '&pr={pr}&mp={mp}&bd={bd}%2C&ba={ba}%2C&sf={sf}&lot={lot}%2C&yr={yr}' \
                      '&singlestory={singlestory}&hoa={hoa}%2C&pho={pho}&pets={pets}&parking={parking}' \
                      '&laundry={laundry}&income-restricted={income_restricted}&fr-bldg={fr_bldg}' \
                      '&condo-bldg={condo_bldg}' \
                      '&furnished-apartments={furnished_apartments}&cheap-apartments={cheap_apartments}' \
                      '&studio-apartments={studio_apartments}&pnd={pnd}&red={red}&zso={zso}&days={days}&ds={ds}' \
                      '&pmf={pmf}&pf={pf}&sch={sch}&zoom={zoom}' \
                      '&rect={rect}&p={p}&sort={sort}&search={search}&rid={rid}' \
                      '&rt={rt}&listright={listright}&isMapSearch={isMapSearch}&zoom={zoom}'\
            .format(spt=spt, status=status, lt=lt, ht=ht, pr=pr, mp=mp, bd=bd, ba=ba, sf=sf, lot=lot, yr=yr,
                    singlestory=singlestory, hoa=hoa, pho=pho, pets=pets, parking=parking, laundry=laundry,
                    income_restricted=income_restricted, fr_bldg=fr_bldg, furnished_apartments=furnished_apartments,
                    studio_apartments=studio_apartments, pnd=pnd, red=red, zso=zso, days=days, ds=ds, pmf=pmf, pf=pf,
                    sch=sch, p=p, rect=rect, sort=sort, search=search, condo_bldg=condo_bldg,
                    cheap_apartments=cheap_apartments, rid=rid, rt=rt, listright=listright, isMapSearch=isMapSearch,
                    zoom=zoom)

        response_content = requests.get(request_url, headers=headers_zpid).content
        json_content = json.loads(response_content)
        properties = json_content['map']['properties']

        for property in properties:
            zpid = property[0]
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
        property_data = json_content['data']['property']
        ContactInfo = None
        if property_data:
            ContactInfo = property_data['listingProvider']['phoneNumber']

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
