import scrapy
import random
import os
from bs4 import BeautifulSoup
import re

from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from webcrawler.items import PublicationWebpage

class Crawler(CrawlSpider):
    name = "crawler"
    publication = None
    domain = None

    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True
            ),
            follow=True,
            callback="parse_items"
        )
    ]

    custom_settings = {
        'DEPTH_PRIORITY': '1',
    }

    def start_requests(self):
        seed = getattr(self, 'seed', None)
        self.domain = getattr(self, 'domain', None)
        self.publication = getattr(self, 'name', None)

        if self.domain is not None and seed is not None:
            yield scrapy.Request(seed, callback=self.parse, dont_filter=True)

    def parse_items(self, response):
        # extract the title
        title = response.css('title::text').extract()
        print("Parsing: " + ', '.join(title))

        # extract the links to follow
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        items = []

        for link in links:
            if self.domain in link.url:
                item = PublicationWebpage()
                item['current_url'] = response.url
                item['destination_url'] = link.url
                items.append(item)

        # save the data
        self.publication = self.publication.lower()
        if not os.path.exists('data/%s' % self.publication):
            os.makedirs('data/%s' % self.publication)

        filename = 'data/%s/%s.txt' % (self.publication, title)
        with open(filename, 'wb') as f:
            soup = BeautifulSoup(response.body, 'html.parser')
            # In the future, could send this text processing task elsewhere that way it doesn't slow down crawling
            soup.title.decompose()
            for s in soup(['script', 'style']):
                s.decompose()
            body = soup.get_text(separator=' ').lower() # Replaces line breaks as seen on website through <br>, <div>, etc tags with space
            body = ''.join([i if ord(i) > 96 and ord(i) < 123 else ' ' for i in body]) # Replaces anything non alphabetical to a space (except for ".")
            body = body.replace('\n', ' ').replace(self.publication, ' ') # Replaces new lines with space and removes publication reference
            body = ' '.join(body.split()) # Takes one or more consecutive spaces and shrinks to a single space

            #TODO: Convert contractions to words (we're -> we are, shouldn't -> should not), or maybe remove them altogether.
            f.write(body)

        return items

#See current publication and remove common text
