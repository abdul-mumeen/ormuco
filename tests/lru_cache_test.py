import unittest
from caching.lru_cache import LRUCache
from caching.data_manager import Location


class TestLRUCache(unittest.TestCase):
    def test_lru_cache(self):
        """Test LRU cache functionality"""
        location = Location(1, 3)
        lru_cache = LRUCache(location, 2)
        lru_cache.addEntry(1, 'This is the first entry')
        value = lru_cache.getEntry(1)
        self.assertEqual(value, 'This is the first entry')

        lru_cache.addEntry(1, 'Updating the first entry')
        value = lru_cache.getEntry(1)
        self.assertEqual(value, 'Updating the first entry')

        lru_cache.addEntry(5, 'Try a second entry')
        value = lru_cache.getEntry(5)
        self.assertEqual(value, 'Try a second entry')
        self.assertEqual(lru_cache.most_recently_used.value,
                         'Try a second entry')
        self.assertEqual(lru_cache.least_recently_used.value,
                         'Updating the first entry')

        lru_cache.addEntry(3, 'Three is a charm')
        value = lru_cache.getEntry(3)
        self.assertEqual(value, 'Three is a charm')

        value = lru_cache.getEntry(1)
        self.assertEqual(value, None)
