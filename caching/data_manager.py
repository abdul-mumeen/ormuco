import heapq


class Location:
    """This is class for representing the location of both user and cache"""
    def __init__(self, x, y):
        """
        This is a constructor for Location class

        Parameters:
            x (int): The x coordinate of the location
            y (int): The y coordinate of the location
        """
        self._x = x
        self._y = y

    @property
    def x(self):
        """Get x coordinate"""
        return self._x

    @property
    def y(self):
        """Get y coordinate"""
        return self._y


class PriorityQueue:
    """This class is for sorting caches based on how close they are to the user's location"""
    def __init__(self):
        """This is the constructor for PriorityQueue class"""
        self.caches = []

    @property
    def empty(self):
        """Get emptiness of PriorityQueue"""
        return len(self.caches) == 0

    def put(self, cache, priority, counter):
        """
        The function to add cache to the PriorityQueue

        Parameters:
            cache (LRUCache): An instance of the LRUCache
            priority (int): Distance of the cache to the user's location
            counter (int): Index to be a tie breaker when two cache has the same distance
        """
        heapq.heappush(self.caches, (priority, counter, cache))

    def get(self):
        """
        This function finds the data with the highest priority in the queue

        Returns:
            cache (LRUCache): An instance of the LRUCache
        """
        return heapq.heappop(self.caches)[2]


class DataManager:
    """
    This is a class to manage caching and data retrieval from cache and database

    Attributes:
        caches_list (list): A list of LRUCaches
        database (dict): A dictionary with int key and string value
    """
    def __init__(self, caches_list, database):
        """
        The constructor for DataManager class

        Parameters:
            caches_list (list): A list of LRUCaches
            database (dict): A dictionary with int key and string value
        """
        self._caches_dict = {cache.id: cache for cache in caches_list}
        self._database = database

    @property
    def caches(self):
        """Get all the caches from the manager"""
        return self._caches_dict

    def _replicate_update(self, cache):
        """
        This function updates all caches with latest available update.

        Parameters:
            cache (LRUCache): A cache with the latest update
        """
        for i, cache_item in self._caches_dict.items():
            if not cache_item.is_expired and cache_item.id != cache.id:
                self._caches_dict[i].update_cache_from(cache)

    def _activate_cache(self, cache_id):
        """
        This function reactivates expired cache

        Parameters:
            cache_id (UUID): The ID of the cache to be re-activated
        """
        self._caches_dict[cache_id].activate()

    def _get_data_from_database(self, key):
        """
        This gets data from the database

        Parameters:
            key (int): The key for the data to be retrieved

        Returns:
            data (string): A string value from the database
        """
        return self._database.get(key)

    def _heuristic_distance(self, user_location, cache_location):
        """
        This function uses Euclidean distance to get distance between two locations

        Parameters:
            user_location (Location): A user location object
            cache_location (Location): The location object for a cache

        Returns:
            distance (int): Euclidean distance between the two locations
        """
        return abs(user_location.x - cache_location.x) + abs(user_location.y -
                                                             cache_location.y)

    def _get_closest_caches(self, user_location):
        """
        This function gets available caches in order of closeness to user's location

        Parameters:
            user_location (Location): A user location object

        Returns:
            closest_caches (PriorityQueue): A queue of caches in order of priority (closness to user)
        """
        closest_caches = PriorityQueue()
        counter = 0
        for cache in self._caches_dict.values():
            distance = self._heuristic_distance(user_location, cache.location)
            closest_caches.put(cache, distance, counter)
            counter += 1
        return closest_caches

    def getData(self, key, user_location):
        """
        This function gets data and location from cache or database

        Parameters:
            key (int): The key to the data to retrieve
            user_location (Location): A user location object

        Returns:
            tuple:
                data (string): The data retrieved
                location (Location): The location where the data is retrieved
        """
        closest_caches = self._get_closest_caches(user_location)
        while not closest_caches.empty:
            cache = closest_caches.get()
            if not cache.is_expired:
                data = cache.getEntry(key)
                if data:
                    self._replicate_update(cache)
                    return data, cache.location

                # if data is not in first cache
                # can't be found in others, so get from data base
                data = self._get_data_from_database(key)
                location = Location(-1, -1)
                cache.addEntry(key, data)
                self._replicate_update(cache)
                return data, location

            # activate expired cache if closer to user's location
            self._activate_cache(cache.id)
