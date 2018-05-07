import pymongo
from pymongo import MongoClient

client = MongoClient('localhost:27017')

db = client['test_database']
coll = db.test_collection

#db.posts.remove({})


posts = db.posts



print(posts.count())
