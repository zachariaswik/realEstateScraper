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
    start_urls = ["https://www.pisos.com/viviendas/barcelona"]
    base_url = "https://www.pisos.com"




    #rules = (Rule(LinkExtractor(restrict_xpaths="//a[@class='ad-preview__title']"), callback="parse_item", follow=True),)

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        subregions = response.css('div.zoneList a.item:not(.item-subitem)')
        listingsPattern = re.compile(r'venta')

        for subregion in subregions:
            subregionLink = urljoin(self.base_url, subregion.css('a::attr(href)').get())
            numListing = int(subregion.css('a span.total::text').get().strip('()').replace('.',''))
            isListings = listingsPattern.search(subregionLink)

            if isListings:
                yield response.follow(subregionLink, callback=self.parseListings)

            else:
                continue
                # Uncomment to go subregions all listings
                # yield response.follow(subregionLink, callback=self.parse)




    def parseListings(self, response):
        ## For following the listing fully
        # num_listings = response.css('div.grid__title span::text').getall()[1]
        # listings = response.css('div.ad-preview__section a::attr(href)')


        # for listing in listings:
        #     listing_url = urljoin(self.base_url, listings.get())

        #     yield {
        #         'listing_url' : listing_url
        #     }

        # For getting the data from the page immediately
        infoBoxes   = response.css('div.ad-preview__info')
        diggitsPattern = re.compile(r'\d+')
        for infoBox in infoBoxes:



            ## These might fail!
            try:
                price     = int(diggitsPattern.search(infoBox.css('div.ad-preview__inline span::text').get().strip().replace('.', ''))[0])
            except:
                logging.log(logging.INFO, "Price could not be found")
                price = None

            try:
                rooms     = int(diggitsPattern.search(infoBox.css("div.ad-preview__inline p::text")[0].get())[0])
            except:
                logging.log(logging.INFO, "Rooms number could not be found")
                rooms = None
            try:
                bathrooms = int(diggitsPattern.search(infoBox.css("div.ad-preview__inline p::text")[1].get())[0])
            except:
                logging.log(logging.INFO, "Bathrooms number could not be found")
                bathrooms = None
            try:
                size      = int(diggitsPattern.search(infoBox.css("div.ad-preview__inline p::text")[2].get())[0])
            except:
                logging.log(logging.INFO, "Size could not be found")
                size = None

            yield{
                    'price' : price,
                    'rooms' : rooms,
                    'bathrooms' : bathrooms,
                    'size'  : size
                }


        # PAGINATION
        nextPage = response.css('div.pagination__next a::attr(href)').get()
        if nextPage is not None: # or just if next_button?
            nextPage = urljoin(self.base_url, nextPage)
            yield response.follow(nextPage, callback=self.parseListings)


        # Get price
        # response.css('div.ad-preview__bottom div.ad-preview__info div.ad-preview__section div.ad-preview__inline span::text').getall()
        # response.css('div.ad-preview__bottom div.ad-preview__inline span::text').get()





    # For individual listing
    def parseSingleListing(self,response):
        pass
