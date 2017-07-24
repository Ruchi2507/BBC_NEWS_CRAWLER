# Pipelines used in News Crawler are defined here.
#
# Pipelines defined here are added to ITEM_PIPELINES setting

from   scrapy.exceptions import DropItem
from   scrapy import signals
from   pydispatch import dispatcher
from   scrapy.exporters import JsonItemExporter
from   readability import Document
from   scrapy.conf import settings
from   datetime import datetime
from   lxml import etree
import geograpy
import requests, html2text
import pymongo, logging

class NewsCrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class NewsTextPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This pipeline is used for extracting news article text.
    '''

    def process_item(self, item, spider):
        '''
        DESCRIPTION:
        ------------
        For each news item, corresponding news text is extracted
        using python library 'readability'.

        RETURNS:
        --------
        News item with 'newsText' field updated is returned.
        '''
        try:
            response = requests.get(item['newsUrl'])
            doc      = Document(response.text)
            content  = Document(doc.content()).summary()
            h = html2text.HTML2Text()
            h.ignore_links = True
            articleText    =  h.handle(content)
            articleText    =  articleText.replace('\r', ' ').replace('\n', ' ').strip()
            item['newsText'] = articleText
        except Exception:
            raise DropItem("Failed to extract article text from: " + item['newsUrl'])

        return item

class NewsCountriesMentionPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This pipeline is used for extracting list of countries,
    specified in news article.
    '''
    def process_item(self, item, spider):
        '''
        DESCRIPTION:
        -----------
        For each news item, list of countries specified in news text,
        is fetched by using 'geograpy'.

        RETURNS:
        --------
        News item with 'countriesMentioned' field updated is returned.
        '''
        try:
            places = geograpy.get_place_context(url=item['newsUrl'])
            countryList = []
            for country in places.country_mentions:
                countryList.append(country[0].encode('ascii', 'ignore'))
            item['countriesMentioned'] = countryList
        except etree.XMLSyntaxError as e:
            logging.info('XML Syntax Error' + e)
        except etree.DocumentInvalid as e:
            logging.info('XML Document Invalid Error'+ e)
        except Exception:
            raise DropItem("Failed to extract country mentions from: " + item['newsUrl'])

        return item

class DropIfEmptyPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This function drops news item if either of following
    mandatory fields are empty:
    1. newsHeadline
    2. newsUrl
    3. newsText
    4. author
    '''
    def process_item(self, item, spider):
        if ((not item['newsHeadline']) or (not item['newsUrl'])
             or (not item['newsText']) or (not item['author'])):
            raise DropItem()
        else:
            return item

class DuplicatesPipeline(object):
    '''
    DESCRIPTION:
    ------------
    This pipeline is used to remove the duplicate news items.
    '''
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['newsUrl'] in self.ids_seen:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.ids_seen.add(item['newsUrl'])
            return item

class MongoDBPipeline(object):
    '''
    DESCRIPTION:
    ------------
    * This pipeline is used to insert data in to MongoDB.
    * MongoDB setting are provided in settings.py
    '''
    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_URI']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if ((data == 'newsUrl' or data == 'newsHeadline' or data == 'newsText'
                 or data == 'author') and not data):
                valid = False
                raise DropItem('News Item dropped, missing ' + data)
        if valid:
            self.collection.insert(dict(item))
            logging.info('News Article inserted to MongoDB database!')
        return item

class JsonExportPipeline(object):
    '''
    DESCRIPTION:
    -----------
    * This pipeline is used for exporting the crawling output
      to a JSON file.
    * JSON file is generated in output directory.
    '''
    def __init__(self):
        dispatcher.connect(self.spider_opened, signals.spider_opened)
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.fjsons = {}

    def spider_opened(self, spider):
        fjson = open('Output/bbc_'+ datetime.now().strftime("%Y%m%d%H%M%S") + '.json', 'wb')
        self.fjsons[spider] = fjson
        self.exporter = JsonItemExporter(fjson)
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        fjson = self.fjsons.pop(spider)
        fjson.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item