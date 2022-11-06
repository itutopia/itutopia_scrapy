# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
from itemadapter import ItemAdapter
import re

# pipline 可以将文档存到本地.也可以存入数据库,如mongodb.
class DaomunovelPipeline:

    def process_item(self, item, spider):

        # 写入mongodb
        host = spider.settings['MONGODB_HOST']
        port = spider.settings['MONGODB_PORT']
        db_name = spider.settings['MONGODB_DB_NAME']
        client = pymongo.MongoClient(host=host, port=port)
        db = client[db_name]
        collection = db[spider.settings['MONGODB_COLLECTION_NAME']]
        collection.insert_one(dict(item))

        # filename = './novel/{}/{}.txt'.format(
        #     re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['book_title']),
        #     re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['chapter_name']),
        # )

        # 沙海小说
        filename = './shahai/{}/{}.txt'.format(
            re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['book_title']),
            re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['chapter_name']),
        )

        # 写入本项目指定路径
        # 藏海花
        # filename = './zanghaihua/{}/{}.txt'.format(
        #     re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['book_title']),
        #     re.sub(r'[\\\/\:\*\?\"\<\>\|]', '_', item['chapter_name']),
        # )

        print('正在写入')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(item['content_text'])

        return item
