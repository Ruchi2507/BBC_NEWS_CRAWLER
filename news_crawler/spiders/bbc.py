# This file defines Crawler for BBC News Website.

import scrapy
from   scrapy.spiders import CrawlSpider, Rule
from   scrapy.linkextractors import LinkExtractor
from   ..items import NewsItem
import json, os, logging

class BbcSpider(CrawlSpider):
    '''
    DESCRIPTION:
    ------------
    * This class inherits the 'CrawlSpider' class of Scrapy.
    * It defines crawler for BBC News Website.
    '''

    name  = 'bbc'   # Crawler Name
    rules = []      # Rule to be used for scraping the entire website.

    def generateCrawlingRule(self):
        '''
        DESCRIPTION:
        -----------
        This function generates the crawling rules using file
        specified 'bbcRules.json' by end user.
        '''
        for rule in self.ruleFile["rules"]:
            allow_r = ()
            if 'allow' in rule.keys():
                allow_r = [a for a in rule['allow']]

            deny_r = ()
            if 'deny' in rule.keys():
                deny_r = [d for d in rule['deny']]

            restrict_xpaths_r = ()
            if 'restrict_xpaths' in rule.keys():
                restrict_xpaths_r = [rx for rx in rule['restrict_xpaths']]

            BbcSpider.rules.append(Rule(
                LinkExtractor(
                    allow=allow_r,
                    deny=deny_r,
                    restrict_xpaths=restrict_xpaths_r,
                ),
                follow=rule['follow'],
                callback=rule['callback']
            ))

    def readVisitedURLS(self):
        '''
        DESCRIPTION:
        -----------
        * This function reads the URLs already scraped, from file
          'Output/visited_urls.txt'. And assign list of scraped URLS
          to 'self.visitedUrls'.
        * If no such file exists then, self.visitedUrls is set to
          empty list.
        * File 'Output/visited_urls.txt', is opened and file handler
          is assigned to 'self.urlFile', for updating the visiting urls
          as the new urls are scraped.
        * 'Output/visited_urls.txt', keeps track of news URLS already
          scraped, in order to avoid scraping of same URL multiple times.
        '''
        visitedUrlFile = 'Output/visited_urls.txt'
        try:
            fileUrls = open(visitedUrlFile, 'r')
        except IOError:
            self.visitedUrls = []
        else:
            self.visitedUrls  = [url.strip() for url in fileUrls.readlines()]
            fileUrls.close()
        finally:
            if not os.path.exists('Output/'):
                os.makedirs('Output/')
            self.urlFile = open(visitedUrlFile, 'a')

    def __init__(self):
        '''
        DESCRIPTION:
        ------------
        Constructor of BBC Spider.
        '''

        # File which defines rules for extracting desired
        # data from BBC News website.
        self.ruleFile = json.load(open('bbcRules.json'))

        # Web pages of allowed_domains will be scraped only.
        self.allowed_domains = self.ruleFile['allowed_domains']

        # URL to start web scraping.
        self.start_urls = self.ruleFile['start_urls']

        self.generateCrawlingRule()
        self.readVisitedURLS()
        super(BbcSpider, self).__init__()

    def getNewsAuthor(self,hxs):
        '''
        DESCRIPTION:
        -----------
        This function fetches the Author of news article being crawled.

        PARAMETERS:
        -----------
        1. hxs: Web page selector of news article being crawled.

        RETURNS:
        --------
        Author of news article being crawled or an empty string if no
        Author is fetched from web page (being crawled).
        '''
        author = hxs.xpath(self.ruleFile['paths']['author'][0]).extract()
        if not author:
            author = hxs.xpath(self.ruleFile['paths']['author'][1]).extract()

        if author:
            return author[0].encode('ascii', 'ignore')
        else:
            return ''

    def parseItems(self, response):
        '''
        DESCRIPTION:
        -----------
        * This function is called for parsing every URL encountered,
          starting from 'start_urls'.
        * In this function required information is fetched from
          the web page and stored in NewsItem object.

        PARAMETERS:
        ----------
        1. response object of Web page.
        '''
        if str(response.url) not in self.visitedUrls:
            try:
                logging.info('Parsing URL: ' + str(response.url))

                newsItem = NewsItem()

                # Selector for Web Page
                hxs    = scrapy.Selector(response)

                # Fetch News URL
                newsItem['newsUrl'] = response.url

                # Fetch News Headline
                title  = hxs.xpath(self.ruleFile['paths']['title'][0]).extract()[0]
                if title:
                    newsItem['newsHeadline'] = title.encode('ascii', 'ignore')

                # Fetch News Author
                newsItem['author'] = self.getNewsAuthor(hxs)

                # Write visited url tp self.urlFile
                self.urlFile.write(str(response.url) + '\n')

                yield newsItem

            except Exception:
                pass

    def close(spider, reason):
        spider.urlFile.close()