import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
from urllib.parse import urljoin
import logging
# Configure logging



class PisoslistingscraperSpider(scrapy.Spider):
    name = "pisosListingScraper"
    allowed_domains = ["www.pisos.com"]
    base_url = "https://www.pisos.com"


    def start_requests(self):
        # startURLs = ["https://www.pisos.com/locales/barcelona", "https://www.pisos.com/naves/barcelona",
        #               "https://www.pisos.com/garajes/barcelona", "https://www.pisos.com/terrenos/barcelona"]

        startURLs = ["https://www.pisos.com/viviendas/barcelona"]
        for startURL in startURLs:
            yield scrapy.Request(startURL, self.parse, meta={'fullRegionName':'barcelona'})


    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        subregions = response.css('div.zoneList a.item:not(.item-subitem)')
        listingsPattern = re.compile(r'venta')
        prevRegionName = response.meta['fullRegionName']

        for subregion in subregions:
            fullRegionName = f"{prevRegionName}_{subregion.css('span::text').get()}"
            subregionLink = urljoin(self.base_url, subregion.css('a::attr(href)').get())
            numListing = int(subregion.css('a span.total::text').get().strip('()').replace('.',''))
            isListings = listingsPattern.search(subregionLink)

            if isListings:
                yield response.follow(subregionLink, callback=self.parseListings, meta = {'fullRegionName' : fullRegionName})

            else:
                yield response.follow(subregionLink, callback=self.parse, meta = {'fullRegionName' : fullRegionName})




    def parseListings(self, response):

        # For getting the data from the page immediately
        pattern = re.compile(r'\b([^\s/]+)\-\b([^\s/]+)\/')
        typeOfListing = pattern.search(response.url)[1]

        infoBoxes   = response.css('div.ad-preview__info')
        for infoBox in infoBoxes:

            # listing name
            listingName = infoBox.css('div.ad-preview__section a::attr(href)').get()
            listingName = urljoin(self.base_url, listingName)

            # Enter every listing to get full data
            yield response.follow(listingName, callback=self.parseSingleListing,
                                  meta={'fullRegionName' : response.meta['fullRegionName'],
                                        'type'           : typeOfListing
                                       }
                                    )

        # PAGINATION
        nextPage = response.css('div.pagination__next a::attr(href)').get()
        if nextPage is not None: # or just if next_button?
            nextPage = urljoin(self.base_url, nextPage)
            yield response.follow(nextPage, callback=self.parseListings, meta={'fullRegionName' : response.meta['fullRegionName']})



    # For individual listing
    def parseSingleListing(self,response):

        features = response.css('div.features__content')
        numPattern = re.compile(r'\d+')

        description = response.css('div.description__content::text').getall()
        try:
            description = ' '.join(description).strip().replace('\r', '')
        except:
            logging.log(logging.INFO, "description not found")


        price = response.css('div.jsPriceValue::text').get()
        try:
            price = int(numPattern.search(price.replace('.', ''))[0])
        except:
            logging.log(logging.INFO, "price not included")


        # Get superficie construida
        sizeConstr = features.css('span.icon-superficiecontruida + div span.features__value::text').get()
        try:
            sizeConstr = int(numPattern.search(sizeConstr.replace('.', ''))[0])
        except:
            logging.log(logging.INFO, "superficie construida not included")


        # Get superficie util
        sizeUtil = features.css('span.icon-superficieutil + div span.features__value::text').get()
        try:
            sizeUtil = int(numPattern.search(sizeUtil.replace('.', ''))[0])
        except:
            logging.log(logging.INFO, "superficie util not included")


        # Get superficie solar
        sizeSolar = features.css('span.icon-superficiesolar + div span.features__value::text').get()
        try:
            sizeSolar = int(numPattern.search(sizeSolar.replace('.', ''))[0])
        except:
            logging.log(logging.INFO, "superficie solar not included")


        # Get habitaciones
        rooms = features.css('span.icon-numhabitaciones + div span.features__value::text').get()
        try:
            rooms = int(numPattern.search(rooms)[0])
        except:
            logging.log(logging.INFO, "rooms not included")

        # Get banos
        bathrooms = features.css('span.icon-numbanos + div span.features__value::text').get()
        try:
            bathrooms = int(numPattern.search(bathrooms)[0])
        except:
            logging.log(logging.INFO, "bathrooms not included")

        # get planta
        floor = features.css('span.icon-planta + div span.features__value::text').get()
        try:
            floor = int(numPattern.search(floor)[0])
        except:
            logging.log(logging.INFO, "floor not included")




        # Get energy data
        energyInfo = response.css('div.energy-certificate__data')
        Econsumption = CO2emission = Erating = CO2rating = None

        # Get electrict consumption
        try:
            Erating      = energyInfo.css('span.energy-certificate__tag::text')[0].get()
            Econsumption = energyInfo.css('span span::text')[0].get()
        except:
            logging.log(logging.INFO, "electricity consumption not included")

        # Get CO2 emission
        try:
            CO2rating   = energyInfo.css('span.energy-certificate__tag::text')[1].get()
            CO2emission = energyInfo.css('span span::text')[1].get()
        except:
            logging.log(logging.INFO, "CO2 emission not included")

        exterior      = features.css('span.icon-exterior + div span.features__value::text').get()
        interior      = features.css('span.icon-interior + div span.features__value::text').get()
        age           = features.css('span.icon-antiguedad + div span.features__value::text').get()
        state         = features.css('span.icon-estadoconservacion + div span.features__value::text').get()
        reference     = features.css('span.icon-reference + div span.features__value::text').get()
        communityCost = features.css('span.icon-gastosdecomunidad + div span.features__value::text').get()
        last_update   = response.css('p.last-update__date::text').get()

        yield{
           'listingName'   : response.url,
           'location'      : response.meta['fullRegionName'],
           'sizeConstr'    : sizeConstr,
           'sizeUtil'      : sizeUtil,
           'price'         : price,
           'type'          : response.meta['type'],
           'bathrooms'     : bathrooms,
           'rooms'         : rooms,
           'floor'         : floor,
           'sizeSolar'     : sizeSolar,
           'exterior'      : exterior,
           'interior'      : interior,
           'age'           : age,
           'state'         : state,
           'reference'     : reference,
           'communityCost' : communityCost,
           'description'   : description,
           'Erating'       : Erating,
           'CO2rating'     : CO2rating,
           'Econsumption'  : Econsumption,
           'CO2emission'   : CO2emission,
           'last_update'   : last_update
        }
