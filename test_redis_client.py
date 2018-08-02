import unittest
import redis_client

class TestRedis(unittest.TestCase):
    def test_set_get(self):
        redis_client.set('my_key', 'my_value')
        self.assertEqual(redis_client.get('my_key'), 'my_value')

if __name__ == '__main__':
    unittest.main()