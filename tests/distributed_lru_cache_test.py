import unittest
from caching.lru_cache import LRUCache
from caching.data_manager import Location
from caching.data_manager import DataManager


class TestGeoDistributedLRUCache(unittest.TestCase):
    """Test the implementation of geo distributed least recently used cache"""
    def setUp(self):
        """Runs before each test"""
        CACHE_SIZE = 3
        self.loc_one = Location(1, 3)
        self.loc_two = Location(2, 4)
        self.loc_three = Location(3, 5)
        self.loc_four = Location(4, 6)
        self.cache_one = LRUCache(self.loc_one, CACHE_SIZE)
        self.cache_two = LRUCache(self.loc_two, CACHE_SIZE)
        self.cache_three = LRUCache(self.loc_three, CACHE_SIZE)
        self.cache_four = LRUCache(self.loc_four, CACHE_SIZE)
        database = {
            1: 'first data',
            2: 'second data',
            3: 'third data',
            4: 'fourth data',
            5: 'fifth data',
        }
        caches = [
            self.cache_one, self.cache_two, self.cache_three, self.cache_four
        ]
        self.data_manager = DataManager(caches, database)
        self.database_location = Location(-1, -1)

    def test_get_data_from_database_when_cache_is_empty(self):
        """Test ability to get data from the database when no data in the cache"""
        user_location = Location(1, 4)
        data, location = self.data_manager.getData(1, user_location)
        self.assertEqual(data, 'first data')
        self.assertEqual(location.x, self.database_location.x)
        self.assertEqual(location.y, self.database_location.y)

        for cache in self.data_manager.caches.values():
            self.assertEqual(cache.most_recently_used.value, 'first data')

    def test_get_data_from_database_when_cache_is_full_but_no_required_data(
        self):
        """Test getting data from databse when cache is not empty but does not have required data"""
        user_location = Location(1, 1)
        self.data_manager.getData(1, user_location)
        self.data_manager.getData(3, user_location)
        self.data_manager.getData(5, user_location)

        new_user_location = Location(2, 4)
        data, location = self.data_manager.getData(3, new_user_location)
        self.assertEqual(data, 'third data')
        self.assertEqual(location.x, self.loc_two.x)
        self.assertEqual(location.y, self.loc_two.y)

        data, location = self.data_manager.getData(2, new_user_location)
        self.assertEqual(data, 'second data')
        self.assertEqual(location.x, self.database_location.x)
        self.assertEqual(location.y, self.database_location.y)

        for cache in self.data_manager.caches.values():
            self.assertEqual(cache.most_recently_used.value, 'second data')

    def test_evicting_least_used_data_in_LRU_cache(self):
        """Test removal of least recently used data when cache is full"""
        user_location = Location(1, 1)
        self.data_manager.getData(1, user_location)
        self.data_manager.getData(3, user_location)
        self.data_manager.getData(5, user_location)

        for cache in self.data_manager.caches.values():
            self.assertEqual(cache.most_recently_used.value, 'fifth data')
            self.assertEqual(cache.least_recently_used.value, 'first data')

        new_user_location = Location(2, 4)
        self.data_manager.getData(2, new_user_location)

        for cache in self.data_manager.caches.values():
            self.assertEqual(cache.most_recently_used.value, 'second data')
            self.assertEqual(cache.least_recently_used.value, 'third data')

    def test_move_most_recently_used_data_up(self):
        """Test placing of most recently used data at the top of the cache"""
        user_location = Location(1, 4)
        self.data_manager.getData(1, user_location)
        data, location = self.data_manager.getData(5, user_location)
        self.assertEqual(data, 'fifth data')
        self.assertEqual(location.x, self.database_location.x)
        self.assertEqual(location.y, self.database_location.y)

        for cache in self.data_manager.caches.values():
            self.assertEqual(cache.most_recently_used.value, 'fifth data')
            self.assertEqual(cache.most_recently_used.right.value,
                             'first data')
            self.assertEqual(cache.most_recently_used.left, None)

    def test_get_data_from_closest_cache_to_user_location(self):
        """Test getting data from cache closest to user and not expired"""
        # caches are empty
        user_location = Location(1, 4)
        self.data_manager.getData(1, user_location)

        #caches no longer empty
        new_user_location = Location(1, 1)
        data, location = self.data_manager.getData(1, new_user_location)
        self.assertEqual(data, 'first data')
        self.assertEqual(location.x, self.loc_one.x)
        self.assertEqual(location.y, self.loc_one.y)

        new_user_location = Location(3, 5)
        data, location = self.data_manager.getData(1, new_user_location)
        self.assertEqual(data, 'first data')
        self.assertEqual(location.x, self.loc_three.x)
        self.assertEqual(location.y, self.loc_three.y)

    def test_get_data_from_next_closest_when_closest_cache_has_expired(self):
        """Test getting data from alternate cache when the closest has expired and reactivating it"""
        # caches are empty
        user_location = Location(1, 4)
        self.data_manager.getData(1, user_location)

        #caches no longer empty
        new_user_location = Location(1, 1)
        # disable location_one cache
        self.assertFalse(
            self.data_manager.caches[self.cache_one.id].is_expired)
        self.data_manager.caches[self.cache_one.id].deactivate()
        self.assertTrue(self.data_manager.caches[self.cache_one.id].is_expired)

        data, location = self.data_manager.getData(1, new_user_location)
        self.assertEqual(data, 'first data')
        self.assertEqual(location.x, self.loc_two.x)
        self.assertEqual(location.y, self.loc_two.y)

        # cache is reactivated after a close user tries to get data
        self.assertFalse(
            self.data_manager.caches[self.cache_one.id].is_expired)
        self.assertEqual(
            self.data_manager.caches[
                self.cache_one.id].most_recently_used.value, 'first data')
