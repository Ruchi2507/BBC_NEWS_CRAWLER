# Scrapy settings for news_crawler project
#
from datetime import datetime
import os

BOT_NAME = 'news_crawler'

SPIDER_MODULES = ['news_crawler.spiders']
NEWSPIDER_MODULE = 'news_crawler.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Log File Settings
if not os.path.exists('Log/'):
    os.makedirs('Log/')
LOG_FILE = 'Log/BBC_crawer_log_' + datetime.now().strftime("%Y%m%d%H%M%S") + ".log"

# Configure item pipelines
ITEM_PIPELINES = {
    'news_crawler.pipelines.NewsCrawlerPipeline':100,
    'news_crawler.pipelines.NewsTextPipeline':200,
    'news_crawler.pipelines.NewsCountriesMentionPipeline':300,
    'news_crawler.pipelines.DropIfEmptyPipeline': 400,
    'news_crawler.pipelines.DuplicatesPipeline': 500,
    'news_crawler.pipelines.MongoDBPipeline': 600,
    'news_crawler.pipelines.JsonExportPipeline':800,
}

#MongoDB settings
MONGODB_URI        = 'mongodb://user:password@ds119223.mlab.com:19223/bbc_news'
MONGODB_DB         = 'bbc_news'
MONGODB_COLLECTION = 'news_articles'
