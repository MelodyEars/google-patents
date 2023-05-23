import scrapy


class PatentspiderSpider(scrapy.Spider):
    name = "patentspider"
    allowed_domains = ["patents.google.com"]
    start_urls = ["https://patents.google.com/?country=US"]

    def parse(self, response):
        our_response = response.css("span.search-result-item")
