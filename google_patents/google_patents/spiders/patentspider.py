import scrapy


class PatentspiderSpider(scrapy.Spider):
    name = "patentspider"
    allowed_domains = ["patents.google.com"]
    start_urls = ["https://patents.google.com"]

    def parse(self, response):
        pass
