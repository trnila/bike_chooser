# -*- coding: utf-8 -*-
import scrapy
import bike.utils as utils


class HupnakoloSpider(scrapy.Spider):
    name = 'hupnakolo'
    allowed_domains = ['hupnakolo.cz']
    start_urls = ['']

    def start_requests(self):
        base = 'https://www.hupnakolo.cz/jizdni-kola/horska-kola/horska-kola-29'

        for i in range(1, 9):
            yield scrapy.Request("{}/{}".format(base, i), callback=self.parse_page)



    def parse_page(self, response):
        for path in response.css('.categoryItem h2 a::attr(href)').extract():
            yield scrapy.Request("https://www.hupnakolo.cz" + path, callback=self.parse_detail)

    def parse_detail(self, response):
        data = {}
        data['name'] = response.css('h1::text').extract()[0].strip()
        data['url'] = response.url
        data['price'] = response.css('.price-value::text').extract()[0].replace(u"\xa0", '').replace('Kč', '').strip()
        for param in response.css('.itemparam .row-parametr'):
            key = utils.normalize_attr(param.css('.col-sm-5::text').extract()[0].strip(':'))
            value = param.css('.col-sm-7::text').extract()[0].strip()
            data[key] = value
        yield data




