# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import datetime
from scrapy.loader import ItemLoader
from  scrapy.loader.processors  import MapCompose,TakeFirst,Join


def date_convert(value):
    try:
        date = datetime.datetime.strptime(value,"%Y/%m/%d").date()
    except Exception as e:
        date =  datetime.datetime.now().date()
    return date


def get_nums(value):
    match_re = re.match(".*?(\d+).*",value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0
    return nums


def remove_comment_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def return_value(value):
    return value

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class JobBoleArticleItemOld(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field()
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                   insert into article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
               """
        if "front_image_path" in self:
            xxx = self["front_image_path"]
        else:
            xxx = ""
        params = (self["title"], self["create_date"], self["url"], self["url_object_id"],
                                         self["front_image_url"],xxx, self["comment_nums"],
                                         self["fav_nums"],
                                         self["praise_nums"], self["tags"], self["content"])
        return insert_sql, params




class JobBoleArticleItem(scrapy.Item):
    title=scrapy.Field()
    create_date=scrapy.Field(
        input_processor=MapCompose(date_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=MapCompose(return_value)
    )
    front_image_path = scrapy.Field()
    praise_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    tags = scrapy.Field(
        input_processor=MapCompose(remove_comment_tags),
        output_processor=Join(",")
    )
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                   insert into article(title,create_date,url,url_object_id,front_image_url,front_image_path,comment_nums,fav_nums,praise_nums,tags,content)
                   values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
               """
        if "front_image_path" in self:
            xxx = self["front_image_path"]
        else:
            xxx = ""
        params = (self["title"], self["create_date"], self["url"], self["url_object_id"],
                                         self["front_image_url"],  xxx, self["comment_nums"],
                                         self["fav_nums"],
                                         self["praise_nums"], self["tags"], self["content"])
        return insert_sql, params



