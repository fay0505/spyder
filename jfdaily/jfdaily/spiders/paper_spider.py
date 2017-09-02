# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from jfdaily.items import JfdailyItem
import re

class PaperSpider(Spider):
    name = "PaperSpider"
    allowed_domains = ["jfdaily.com"]
    start_url = 'http://www.jfdaily.com'
    epaper_url = ''
    next_url = ''

    def start_requests(self):
        yield Request(self.start_url, self.parse_epaper)

    def parse_epaper(self, response):            #获取解放日报的电子版链接
        r = response.xpath('//ul[@class="epaper-ul"]/li')[0]
        href = r.xpath('./a/@href').extract()[0]
        tmp = href.split('/')[-1]
        self.next_url = self.start_url + href.replace(tmp,'')
        self.epaper_url = self.start_url + href
        yield Request(self.epaper_url, self.parse_layout)

    def parse_layout(self,response):
        r = response.xpath('//div[@class="WH100 Left_bg01 iframeScroll"]/ul/li')
        num_of_layout = len(r)      #计算今日新闻的版面数
        for i in range(1, num_of_layout):
            if(i < 10):
                new_url = self.next_url + 'page_' + '0' + str(i) + '.htm'
            else:
                new_url = self.next_url + 'page_' + str(i) + '.htm'
           # print("new:",new_url)
            yield Request(new_url, self.parse_news)

    def parse_news(self,response):   #进入到每个版面，抓取新闻的链接
        r = response.xpath('//div[@class="list"]/a')
        for node in r:
            href = node.xpath('./@href').extract()[0]
            url = self.next_url + href
            yield Request(url, self.parse_new)

    def parse_new(self, response):     #进入每个新闻页面，抓起新闻内容
            item = JfdailyItem()
            r = response.xpath('//div[@class="title"]')    #抓取新闻标题
            h3 = r.xpath('./h3/text()').extract()
            if(len(h3) == 2):
                item['subtitle1'] = h3[0]      #有两个副标题
                item['subtitle2'] = h3[1]
            elif(len(h3) == 1):
                item['subtitle1'] = h3[0]
                item['subtitle2'] = ''
            else:
                item['subtitle1'] = item['subtitle2'] = ''
            item['main_title'] = r.xpath('./h1/text()').extract()[0]

            r1 = response.xpath('//div[@class="content"]/text()').extract()
            content = ''
            for i in range(len(r1)):
                t = r1[i].split()
                for j in range(len(t)):
                    content += t[j]
            item['content']  = content

            yield  item

