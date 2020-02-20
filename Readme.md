# Scrapy教程

## 网站

http://quotes.toscrape.com

## 目的

爬quotes和人物的名字，并且自动识别下一页继续爬

## 相关的步骤看自己的有道云笔记

举个例子

``` xml
<?xml version="1.0" encoding="UTF-8"?>
 
<bookstore>
 
<book>
  <title lang="eng">Harry Potter</title>
  <price>29.99</price>
</book>
 
<book>
  <title lang="eng">Learning XML</title>
  <price>39.95</price>
</book>
 
</bookstore>
```

举个网页的例子

http://quotes.toscrape.com/

提取出需要的两个text

可以用一下的xapth语句

``` python
response.xpath('//div[@class="quote"][1]/span[@class="text"]/text()').extract()
response.xpath('//div[@class="quote"][1]/span/small/text()').extract()
```

匹配tag里面的内容

``` python
response.xpath('//div[@class="quote"][1]/div/a/text()').extract()  
```

按阶段来匹配，注意是在quote里面相对的坐标用./

``` python
quote=response.xpath('//div[@class="quote"][1]/div/a') 
quote.xpath('./text()').extract()
```

spider里面应该怎么写

``` python
# -*- coding: utf-8 -*-

import scrapy

class QuotesSpider(scrapy. Spider):

    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').get(),
                'author': quote.xpath('./span/small/text()').extract(),
                'tags': quote.xpath('./div/a[@class="tag"]/text()').extract(),
            }
```

运行的时候用

``` sh
scrapy crawl -o output.jl
```

获取下一页的href标签，继续yield调用scrapy. Request方法，用parse函数处理response，应该是把这个response放到调度器里面排队。

``` python
# -*- coding: utf-8 -*-

import scrapy

class QuotesSpider(scrapy. Spider):

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
        if next_page:
            yield scrapy. Request('http://quotes.toscrape.com/'+next_page, 
                                 callback=self.parse)
```

