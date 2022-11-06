import scrapy
from daomunovel.items import DaomunovelItem
from copy import deepcopy
import os
import re

class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    # def parse(self, response):
    #     pass

    def parse(self, response):

        # 开始解析网页第一层，拿到书的名称
        # 盗墓笔记全集
        res = response.xpath('//ul[@class="sub-menu"]/li')

        for i in res:
            item = DaomunovelItem()
            # 书的名称
            item['book_title'] = i.xpath('.//a/text()').get()
            # 拿到书连接，可以进入拿到书的章节
            url_one = i.xpath('.//a/@href').get()

            # 存放路径
            book_path = re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['book_title'])

            dirpath = './novel/{}'.format(book_path)

            # 创建
            if not os.path.exists(dirpath):
                os.makedirs(dirpath)

            yield scrapy.Request(url_one, callback=self.parse_two, meta={'item':deepcopy(item)})

    def parse_two(self, response):
        # 开始解析网页第二层，拿到书的章节
        # 把刚刚传参的参数取下来
        item = response.meta.get('item')

        res_two = response.xpath('//div[@class="excerpts"]/article')
        for i in res_two:
            # 书的章节
            item['chapter_name'] = i.xpath('.//a/text()').get()
            # 拿到章节连接，可以进入拿到文本内容
            url_two = i.xpath('.//a/@href').get()

            yield scrapy.Request(url_two, callback=self.parse_three, meta={'item':
                                                                               deepcopy(item)})

    def parse_three(self, response):
        # 开始解析网页第三层，拿到文本内容
        # 把刚刚传参的参数取下来
        item = response.meta.get('item')

        res_three = response.xpath('//article[@class="article-content"]/p/text()').getall()

        item['content_text'] = '\n'.join(res_three)

        yield item

