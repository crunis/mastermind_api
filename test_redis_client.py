import unittest
import redis_client

# This needs a Redis Server running
# with Docker, you can do:
#   docker run -d -p 6379:6379 redis
#   REDIS_HOST=127.0.0.1 python test_redis_client.py

class TestRedisClient(unittest.TestCase):
    def test_set_get(self):
        redis_client.set('my_key', 'my_value')
        self.assertEqual(redis_client.get('my_key'), 'my_value')

if __name__ == '__main__':
    unittest.main()