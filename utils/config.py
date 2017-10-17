from pymongo import MongoClient
from redis import StrictRedis

env = 'dev'
redis_setting = {
    'dev': {
        'host': 'localhost',
        'port': 6379,
        'max_connections': 200,
        'db': 1,
    }
}
mongo_setting = {
    'dev': 'mongodb://127.0.0.1:27017'
}
REDIS_CLIENT = StrictRedis(**redis_setting[env])
MONGO_CLIENT = MongoClient(mongo_setting[env])

DB_NAME = 'base'
