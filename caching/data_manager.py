import heapq


class Location:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y


class PriorityQueue:
    def __init__(self):
        self.caches = []

    def empty(self):
        return len(self.caches) == 0

    def put(self, cache, priority, counter):
        heapq.heappush(self.caches, (priority, counter, cache))

    def get(self):
        return heapq.heappop(self.caches)[2]


class DataManager:
    def __init__(self, array_caches, database):
        self._caches_dict = {cache.id: cache for cache in array_caches}
        self._database = database

    @property
    def caches(self):
        return self._caches_dict

    def _replicate_update(self, cache):
        for i, cache_item in self._caches_dict.items():
            if not cache_item.is_expired and cache_item.id != cache.id:
                self._caches_dict[i].update_cache_from(cache)

    def _activate_cache(self, cache_id):
        self._caches_dict[cache_id].activate()

    def _get_data_from_database(self, key):
        return self._database.get(key)

    def _heuristic_distance(self, user_location, cache_location):
        return abs(user_location.x - cache_location.x) + abs(user_location.y -
                                                             cache_location.y)

    def _get_closest_caches(self, user_location):
        closest_caches = PriorityQueue()
        counter = 0
        for cache in self._caches_dict.values():
            distance = self._heuristic_distance(user_location, cache.location)
            closest_caches.put(cache, distance, counter)
            counter += 1
        return closest_caches

    def getData(self, key, user_location):
        closest_caches = self._get_closest_caches(user_location)
        while not closest_caches.empty():
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
