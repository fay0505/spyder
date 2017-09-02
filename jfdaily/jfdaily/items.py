# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JfdailyItem(scrapy.Item):

    main_title = scrapy.Field()
    subtitle1 = scrapy.Field()
    subtitle2  = scrapy.Field()
    content = scrapy.Field()


