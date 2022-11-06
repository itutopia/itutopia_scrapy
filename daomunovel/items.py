# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DaomunovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 书名
    book_title = scrapy.Field()
    # 章节名称
    chapter_name = scrapy.Field()
    # 文本内容
    content_text = scrapy.Field()

    pass
