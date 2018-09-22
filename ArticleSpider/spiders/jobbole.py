# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114364/']

    def parse(self, response):
        title = response.xpath("//div[@class='entry-header']/h1/text()").extract()[0].strip()

        create_date=response.xpath("//div[@class='entry-meta']/p[@class='entry-meta-hide-on-mobile']/text()").extract()[
            0].strip().replace("·", "").strip()

        dianzan_num = int(response.xpath("//div[@class='post-adds']/span[contains(@class,'vote-post-up')]/h10/text()").extract()[0])

        print("title"+title+",create_date:"+create_date+",dianzan_num:"+dianzan_num)
