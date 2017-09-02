# -*- coding: utf-8 -*-

from scrapy import Spider, Request
from people_paper.items import PeoplePaperItem
import re


class PaperSpider(Spider):
    name = "PaperSpider"
    allowed_domains = ["paper.people.com.cn"]
    start_url = 'http://paper.people.com.cn'
    date_url = ''


    def start_requests(self):     #第一次访问返回当前日期的报纸地址
        yield Request(self.start_url, self.parse_layout)



    def parse_layout(self, response):  #抓取每日新闻的版面信息

        r_url = response.url
        exp0 = '\d{4}.\d{2}.\d{2}'  # 构造正则表达式，抓取url中的日期
        date = re.findall(exp0, r_url)[0]
        self.date_url = self.start_url + '/rmrb/html/' + date

        t = response.xpath('//div[@class="right_title-name"]')  # 定位到版面划分的节点
        for node in t:
            newurl = self.date_url + '/' + node.xpath('./a/@href').extract()[0]
            print('layout_url: ', newurl)
            yield Request(newurl, self.parse_news)


    def parse_news(self, response):               #抓取版面新闻的个数以及链接

        r = response.xpath('//div[@class="l_c"]/div/ul/li')  # 定位到该版面新闻标题li元素处
        for node in r:
            news_url = self.date_url + '/' + node.xpath('./a/@href').extract()[0]
            yield Request(news_url, self.parse_new)


    def parse_new(self, response):         #对每一条新闻进行抓取

        r = response.xpath('//div[@class="ban_t"]/div/ul/li/text()').extract()[0]   # 抓取版面的主题
        exp = '\d+[\u4e00-\u9fa5].[\u4e00-\u9fa5]+'
        tmp = re.findall(exp, r)[0]
        layout_n = tmp.split(':')[0]  # 获取版号和主题
        theme = tmp.split(':')[1]

        Item  = PeoplePaperItem()
        Item['layout_n'] = layout_n
        Item['theme'] = theme
        Item['main_title'] =  response.xpath('//div[@class="text_c"]/h1/text()').extract()
        Item['subtitle'] = response.xpath('//div[@class="text_c"]/h2/text()').extract()
        Item['shoulder_title'] = response.xpath('//div[@class="text_c"]/h3/text()').extract()
        Item['author'] = response.xpath('//div[@class="text_c"]/h4/text()').extract()

        r1 = response.xpath('//div[@id="ozoom"]/p')      #提取新闻的内容
        content = ''
        for node in r1:
            t = node.xpath('./text()').extract()[0]
            t = t.split('\u3000')[2]     #去除抓取到内容中的分隔符
            t = t.split('\xa0')[0]
            content += t
        Item['content'] = content

        yield Item