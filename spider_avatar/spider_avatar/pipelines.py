# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy.pipelines.files import FilesPipeline
from scrapy.http import Request
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class myImagesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):  
        image_guid = request.url.split('/')[-1]  
        return 'spider_funpic/file/full/%s' % (image_guid)  

    def get_media_requests(self, item, info):   
        if item['data_type'] == 'funpics':
            for image_url in item['image_paths']:
                yield Request(image_url)

    def item_completed(self, results, item, info):
        if item['data_type'] == 'jokes':
            return item   
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths[0]
        return item

class SpiderAvatarPipeline_JSON(object):
    def __init__(self):
        self.ids_seen = set()

    def open_spider(self, spider):
        self.file = codecs.open('jokes.json', mode='wb', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['title'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'])
            line = json.dumps(dict(item)) + "\n"
            self.file.write(line.decode("unicode_escape"))
            return item

import MySQLdb
class SpiderAvatarPipeline_MYSQL(object):

    def __init__(self):
        self.ids_seen = set()

        self.conn = MySQLdb.connect(user=settings['MYSQL_USER'], passwd=settings['MYSQL_PWD'], db=settings['MYSQL_DB'], host=settings['MYSQL_HOST'], charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()

        #清空表：
        # self.cursor.execute("truncate table " + settings['SQL_DB_JOKES'])
        # self.conn.commit()
        # self.cursor.execute("truncate table " + settings['SQL_DB_FUNPICS'])
        # self.conn.commit()

    def process_item(self, item, spider):
        #使用set去重
        if item['title'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['title'])

            # 存储至mydsql
            try:
                if spider.name == 'jokes':
                    self.cursor.execute("""INSERT INTO Jokes_jokes_jokes (title, data, src_url, dateTime)  
                          VALUES (%s, %s, %s, NOW())""", 
                          (
                            item.get('title'), 
                            item.get('data'),
                            item.get('src_url'),
                          )
                    )
                else:
                    self.cursor.execute("""INSERT INTO Jokes_jokes_funpics (title, image_paths, src_url, dateTime)  
                          VALUES (%s, %s, %s, NOW())""", 
                          (
                            item.get('title'), 
                            item.get('image_paths'),
                            item.get('src_url'),
                          )
                    )
                self.conn.commit()
            except MySQLdb.Error, e:
                print "********   Error %d: %s  ******" % (e.args[0], e.args[1])

        return item

    def spider_closed(self, spider):
        self.file.close()
