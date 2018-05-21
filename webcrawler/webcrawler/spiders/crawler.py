import scrapy
import random
import os

class Crawler(scrapy.Spider):
    name = "crawler"
    publication = None
    domain = None
    
    def start_requests(self):
        seed = getattr(self, 'seed', None)
        self.domain = getattr(self, 'domain', None)
        self.publication = getattr(self, 'name', None)

        if self.domain is not None and seed is not None:
            yield scrapy.Request(seed, self.parse)

    def parse(self, response):
        if not os.path.exists('data/%s' % self.publication):
            os.makedirs('data/%s' % self.publication)

        filename = 'data/%s/%s.html' % (self.publication, response.css('title::text').extract())
        with open(filename, 'wb') as f:
            f.write(response.body)