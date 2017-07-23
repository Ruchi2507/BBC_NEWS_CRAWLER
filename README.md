# BBC NEWS CRAWLER
BBC News Content Collect and Store

## Details
  * This Python Application crawls BBC online news website using the SCRAPY crawler framework (http://scrapy.org/).
  * This appliction cleans the news articles to obtain only information relevant to the news story,
    e.g. News URL, News Text, News Headline, Author and Countries mentioned in news article.
  * News articles crawled are stored in Mongo Database.
  * Provides a search REST API, that provides access to the content in the mongo database. 
    * Using the search REST API, end user can fetch:
      * All the news articles in data base.
      * News Articles with a given keyword in News Text.
      * News Articles with a given keyword in News Headline.
      
## Execution:
   * Change to BBC_NEWS_CRAWLER (i.e. Current directory) and execute below command:
      ```$ scrapy crawl bbc```
   * Above command will execute the crawler.
   
## Directory Structure:
  * Directory ``news_crawler``: 
    * Contains the Scrapy Spider for BBC News Website.
  * Directory ``Log``: 
    * This directory is created at runtime and contains log file of crawler.
  * Directory ``Output``: 
    * This directory is also created at runtime.
    * It contains the output json file including the data cawled from BBC News Website.
  * File ```bbcRules.json```:
    * In this file rules are defined for crawling BBC News Website.
    * End-User can edit this file as per requirement.
  * File ```newsSearchRestAPI.py```:
    * This script provides implementation of search REST API, for News Crawler.
    * Implemented search APIs gets the required data from Mongo Database and display to end user.
    * 3 search APIs are implemented, which are:
      1. For fetching all the news articles in Mongo Database.
         * (Example API Call: ```<ROOT URL>/news ```)
      2. For fetching news articles from Mongo Database, with a given keyword in News Text. 
         * (Example API Call: ```<ROOT URL>/newsText/<string:keyword>``` like: "http://127.0.0.1:5000/newsText/Tension") 
      3. For fetching news articles from Mongo Database, with a given keyword in News Headline. 
         * (Example API Call: ```<ROOT URL>/newsHeadline/<string:keyword>``` like: "http://127.0.0.1:5000/newsHeadline/BBC" 
           or "http://127.0.0.1:5000/newsHeadline/BBC News") 
