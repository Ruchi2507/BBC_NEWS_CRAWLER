# This file defines the models for scraped news items

import scrapy

class NewsItem(scrapy.Item):
    '''
    DESCRIPTION:
    -----------
    This class defines contents of Crawled news feed.
    '''
    newsHeadline = scrapy.Field()  # News Headline
    newsUrl      = scrapy.Field()  # News URL
    newsText     = scrapy.Field()  # News Article
    author       = scrapy.Field()  # News Author
    countriesMentioned = scrapy.Field()  # Name of Country mostly Specified in news article
