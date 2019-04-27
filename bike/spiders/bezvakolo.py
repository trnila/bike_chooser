# -*- coding: utf-8 -*-
import scrapy
import re
import bike.utils as utils


class BezvakoloSpider(scrapy.Spider):
    name = 'bezvakolo'
    base_url = 'https://www.bezvakolo.cz'


    def start_requests(self):
        page_url = '{base_url}/horska-kola/?f%5Bdyn_a1%5D%5B0%5D=5411&from={offset}'

        offset = 36
        for i in range(0, 9):
            url = page_url.format(offset=i*offset, base_url=self.base_url)
            yield scrapy.Request(url, callback=self.parse_list)

    def parse_list(self, res):
        for url in res.css('.shop_list_product a.link::attr(href)').extract():
            yield scrapy.Request(self.base_url + url, callback=self.parse_bike)

    def parse_bike(self, res):
        data = {}
        data['url'] = res.url
        data['price'] = res.css('.prices .primary::text').get().replace(' ', '').replace('Kč', '').strip() 
        data['name'] = res.css('h1::text').get().strip() 
        for pair in res.css('.params tr'):
            key = utils.normalize_attr(pair.css('th::text').get().replace(':', ''))
            val = re.sub(r'\s+', ' ', pair.css('td::text').get()).strip()
            data[key] = val
        yield data

