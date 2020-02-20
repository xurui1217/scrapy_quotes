# -*- coding: utf-8 -*-
import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').get(),
                'author': quote.xpath('./span/small/text()').extract(),
                'tags': quote.xpath('./div/a[@class="tag"]/text()').extract(),
            }
        next_page = response.xpath('//li/a/@href').extract()[0]
        if next_page and len(next_page) > 0:
            # 获取下一页的链接
            new_link = response.urljoin(next_page)
            yield scrapy.Request(new_link,
                                 callback=self.parse)
