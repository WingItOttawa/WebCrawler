# -*- coding: utf-8 -*-

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
        #print("Parsing: " + ', '.join(title))

        # extract the links to follow
        links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)
        item = {}

        for link in links:
            if self.domain in link.url:
                item['current_url'] = response.url
                item['destination_url'] = link.url

        item['publication'] = self.publication.lower()
        #print "type(item['publication']) is", type(item['publication']), "and is", item['publication']

        item['content'] = response.body

        return item
