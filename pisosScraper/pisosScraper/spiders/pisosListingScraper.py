import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class PisoslistingscraperSpider(CrawlSpider):
    name = "pisosListingScraper"
    allowed_domains = ["www.pisos.com"]
    start_urls = ["https://www.pisos.com/venta/pisos-barcelona/"]
    
    rules = (Rule(LinkExtractor(restrict_xpaths="//div[contains(@class,'ad-preview__bottom')]"), callback="parse_item", follow=True),)

    def parse_item(self, response):
        item = response.html
        print(item)
        # item = {}
        # #item["domain_id"] = response.xpath('//input[@id="sid"]/@value').get()
        # #item["name"] = response.xpath('//div[@id="name"]').get()
        # #item["description"] = response.xpath('//div[@id="description"]').get()
        return item
