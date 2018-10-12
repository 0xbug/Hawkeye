from pymongo import MongoClient, DESCENDING
from redis import Redis
import os

if os.environ.get('MONGODB_URI'):
    MONGODB_URI = os.environ.get('MONGODB_URI')
else:
    MONGODB_URI = 'mongodb://localhost:27017'

client = MongoClient(MONGODB_URI, connect=False)
db = client.get_database('hawkeye')

if os.environ.get('MONGODB_USER'):
    MONGODB_USER = os.environ.get('MONGODB_USER')
    MONGODB_PASSWORD = os.environ.get('MONGODB_PASSWORD')
    db.authenticate(MONGODB_USER, MONGODB_PASSWORD)

result_col = db.get_collection('result')
query_col = db.get_collection('query')
blacklist_col = db.get_collection('blacklist')
task_col = db.get_collection('task')
notice_col = db.get_collection('notice')
github_col = db.get_collection('github')
setting_col = db.get_collection('setting')

if os.environ.get('REDIS_HOST'):
    REDIS_HOST = os.environ.get('REDIS_HOST')
else:
    REDIS_HOST = 'localhost'
if os.environ.get('REDIS_PORT'):
    REDIS_PORT = int(os.environ.get('REDIS_PORT'))
else:
    REDIS_PORT = 6379
result_cache = Redis(host=REDIS_HOST, port=REDIS_PORT,
                     db=1, decode_responses=True)
