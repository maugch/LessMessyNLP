import os

import redis
from rq import Worker, Connection

redis_url = 'redis://'

queue_name = 'nlptasks'
conn = redis.from_url(redis_url)
redis_available = False

try:
    conn.ping()
    redis_available = True
except:
    print("Redis not found!")
    redis_available = False
    exit

if __name__ == '__main__':
    with Connection(conn):
        worker = Worker([queue_name])
        worker.work()