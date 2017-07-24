# BBC News Search Rest API

from   flask import Flask
from   flask_restful import Resource, Api
from   flask_pymongo import PyMongo
from   bson import json_util
import json

# Connecting to MongoDB containing the crawled BBC News Articles.
app    = Flask(__name__)
app.config['MONGO_DBNAME'] = 'bbc_news'
app.config['MONGO_URI']    = 'mongodb://user:password@ds119223.mlab.com:19223/bbc_news'
api                        = Api(app)
mongo                      = PyMongo(app)

def toJson(data):
    """Convert Mongo object(s) to JSON"""
    return json.dumps(data, default=json_util.default)

class NewsMeta(Resource):
    def get(self):
        '''
        DESCRIPTION:
        -----------
        Gets all the news articles in database.
        '''
        results = mongo.db.news_articles.find()
        json_results = []
        for result in results:
            json_results.append(result)
        return toJson(json_results)

class SearchNewsTextKeyword(Resource):
    def get(self, keyword):
        '''
        DESCRIPTION:
        ------------
        GET news articles, where keyword appears in news article text.

        PARAMETERS:
        ----------
        1. keyword: string to be searched in news text.
        '''
        results = mongo.db.news_articles.find({'newsText': {'$regex': '.*' + keyword + '.*'}})
        json_results = []
        for result in results:
            json_results.append(result)
        return toJson(json_results)

class SearchNewsHeadlineKeyword(Resource):
    def get(self, keyword):
        '''
        DESCRIPTION:
        ------------
        GET news articles, where keyword appears in news headline.

        PARAMETERS:
        ----------
        1. keyword: string to be searched in news headline.
        '''
        results = mongo.db.news_articles.find({'newsHeadline': {'$regex': '.*' + keyword + '.*'}})
        json_results = []
        for result in results:
            json_results.append(result)
        return toJson(json_results)

api.add_resource(SearchNewsHeadlineKeyword, '/newsHeadline/<string:keyword>')
api.add_resource(SearchNewsTextKeyword, '/newsText/<string:keyword>')
api.add_resource(NewsMeta, '/news')

if __name__ == '__main__':
    app.run()