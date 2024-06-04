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
    # start_urls = ["https://www.pisos.com/viviendas/barcelona"]
    base_url = "https://www.pisos.com"


    def start_requests(self):


        # startURLs = ["https://www.pisos.com/locales/barcelona", "https://www.pisos.com/naves/barcelona",
        #               "https://www.pisos.com/garajes/barcelona", "https://www.pisos.com/terrenos/barcelona"]


        startURLs = ["https://www.pisos.com/viviendas/barcelona"]


        for startURL in startURLs:
            yield scrapy.Request(startURL, self.parse, meta={'fullRegionName':'barcelona'})

    #rules = (Rule(LinkExtractor(restrict_xpaths="//a[@class='ad-preview__title']"), callback="parse_item", follow=True),)

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
                # Uncomment to go subregions all listings
                yield response.follow(subregionLink, callback=self.parse, meta = {'fullRegionName' : fullRegionName})




    def parseListings(self, response):
        ## For following the listing fully
        # num_listings = response.css('div.grid__title span::text').getall()[1]
        # listings = response.css('div.ad-preview__section a::attr(href)')


        # For getting the data from the page immediately
        pattern = re.compile(r'\b([^\s/]+)\-\b([^\s/]+)\/')
        listingsURL = response.url

        typeOfListing = pattern.search(listingsURL)[1]
        location      = pattern.search(listingsURL)[2]

        infoBoxes   = response.css('div.ad-preview__info')
        diggitsPattern = re.compile(r'\d+')
        for infoBox in infoBoxes:

            # listing name
            listingName = infoBox.css('div.ad-preview__section a::attr(href)').get()
            listingName = urljoin(self.base_url, listingName)

            try:
                price = int(diggitsPattern.search(infoBox.css('span.ad-preview__price::text').get().strip().replace('.', ''))[0])
            except:
                logging.log(logging.INFO, "Price could not be found")
                price = None




            descriptions = infoBox.css('div.ad-preview__inline p::text').getall()
            pattern = re.compile(r'(\d+)\s(\w+)|(\d+)ª\s(\w+)')
            size = None; bathrooms = None; rooms = None; floor = None
            for d in descriptions:
                m = pattern.search(d)
                try:
                    if(m[2] == 'm²'):
                        size = int(m[1])
                    elif(m[2] == 'baño'):
                        bathrooms = int(m[1])
                    elif(m[2] == 'habs'):
                        rooms = int(m[1])
                    elif(m[4] == 'planta' or m[4] == 'atico' or m[4] == 'bajo'):
                        floor = m[3]
                except:
                    logging.log(logging.INFO, "Could not parse deccription")


            yield{
                    'listingName' : listingName,
                    'location' : response.meta['fullRegionName'],
                    'price' : price,
                    'rooms' : rooms,
                    'bathrooms' : bathrooms,
                    'size'  : size,
                    'floor' : floor,
                    'type'  : typeOfListing
                }


        # PAGINATION
        nextPage = response.css('div.pagination__next a::attr(href)').get()
        if nextPage is not None: # or just if next_button?
            nextPage = urljoin(self.base_url, nextPage)
            yield response.follow(nextPage, callback=self.parseListings, meta={'fullRegionName' : response.meta['fullRegionName']})


        # Get price
        # response.css('div.ad-preview__bottom div.ad-preview__info div.ad-preview__section div.ad-preview__inline span::text').getall()
        # response.css('div.ad-preview__bottom div.ad-preview__inline span::text').get()





    # For individual listing
    def parseSingleListing(self,response):
        pass
