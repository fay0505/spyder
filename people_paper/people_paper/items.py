# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PeoplePaperItem(scrapy.Item):

    layout_n = scrapy.Field()    #新闻所属版面
    theme = scrapy.Field()   #新闻版面的主题
    shoulder_title = scrapy.Field() #新闻的肩题<h3>
    main_title = scrapy.Field()    #新闻标题<h1>
    subtitle = scrapy.Field()  #副标题<h2>
    author = scrapy.Field()  #作者<h4>
    content = scrapy.Field() #新闻内容
