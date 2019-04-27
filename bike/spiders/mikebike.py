# -*- coding: utf-8 -*-
import scrapy
import bike.utils as utils


class MikebikeSpider(scrapy.Spider):
    name = 'mikebike'

    def start_requests(self):
        page_url = 'https://www.mikebike.cz/Jizdni-kola/Horska-kola/Horska-kola-29/Panska-horska-kola-29/?strana={}'
        for i in range(1, 9):
            yield scrapy.Request(page_url.format(i), callback=self.parse_list)

    def parse_list(self, response):
        for url in response.css('.product-list h3 a::attr(href)').extract():
            yield scrapy.Request("https://www.mikebike.cz" + url, callback=self.parse_bike)

    def parse_bike(self, res):
        data = {}
        data['url'] = res.url
        data['price'] = res.css('.koupit .price::text').get()
        data['name'] = res.css('h1::text').get().strip() 

        for pair in res.css('.parametry tr'):
            tds = pair.css('td *::text').extract()
            data[utils.normalize_attr(tds[0])] = tds[1].strip()
        yield data
 
