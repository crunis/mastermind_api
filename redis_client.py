import redis
import os
import logging

EXPIRES = 3600 * 24 * 7 # Automatically purge games in a week
client = None

def rc():
    global client
    if client:
        logging.info("Reusing existing Redis client")
        return client
    logging.info("Creating new Redis client")
    redis_host = os.getenv('REDIS_HOST', 'redis')
    redis_port = int(os.getenv('REDIS_PORT', '6379'))
    client =  redis.StrictRedis(host=redis_host, port=redis_port, db=0)
    return client

def set(key, value):
    rc().set(key, value, EXPIRES)

def get(key):
    return rc().get(key)