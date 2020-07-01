import config
import pymongo
from pprint import pprint

user = config.mongo_db_credentials['user']
password = config.mongo_db_credentials['password']
mongodb_url = "mongodb+srv://scraper-writer:{0}@news-hgakq.mongodb.net/news?retryWrites=true&w=majority"\
    .format(password)

client = pymongo.MongoClient(mongodb_url)
db = client['news']
collection = db['openers']
error_collection = db['errors']
trend_collection = db['trends']

def insert_opener(opener):
    collection.insert_one(opener)

def insert_error(error_message):
    error_collection.insert_one(error_message)

def insert_trends(trend):
    trend_collection.insert_one(trend)

'''
url = 'mongodb+srv://scraper-writer:{0}@news-hgakq.mongodb.net/<dbname>?retryWrites=true&w=majority'
client = pymongo.MongoClient("mongodb+srv://scraper-writer:<password>@news-hgakq.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
'''
