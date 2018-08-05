import redis
import os
import logging
import json

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
    rc().set(key, json.dumps(value), EXPIRES)


def get(key):
    v = rc().get(key)
    if v:
        v = json.loads(v)

    return v