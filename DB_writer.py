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


def insert_opener(opener):
    collection.insert_one(opener)

'''
url = 'mongodb+srv://scraper-writer:{0}@news-hgakq.mongodb.net/<dbname>?retryWrites=true&w=majority'
client = pymongo.MongoClient("mongodb+srv://scraper-writer:<password>@news-hgakq.mongodb.net/<dbname>?retryWrites=true&w=majority")
db = client.test
'''
