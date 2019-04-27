# -*- coding: utf-8 -*-
import scrapy
import bike.utils as utils


class MojekoloSpider(scrapy.Spider):
    name = 'mojekolo'

    def start_requests(self):
        page_url = 'http://www.mojekolo.cz/jizdni-kola/horska-kola/horska-kola-29/{}'
        for i in range(1, 35):
            yield scrapy.Request(page_url.format(i), callback=self.parse_list)

    def parse_list(self, response):
        for url in response.css('.list-items__item__in > a::attr(href)').extract():
            yield scrapy.Request(url, callback=self.parse_bike)

    def parse_bike(self, response):
        data = {}
        data['url'] = response.url
        data['price'] = response.css('.box-detail-add__prices__item--main dt::text').get()
        data['name'] = response.css('h1::text').get()

        for pair in response.css('.table-params tr'):
            key = utils.normalize_attr(pair.css('th::text').get())
            val = pair.css('td::text').get()
            data[key] = val
        yield data
 
