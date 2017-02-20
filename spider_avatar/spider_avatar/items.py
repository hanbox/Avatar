# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SpiderAvatarItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # pass
    title = scrapy.Field()
    data = scrapy.Field()
    src_url = scrapy.Field()
    image_paths = scrapy.Field()
    data_type = scrapy.Field()
