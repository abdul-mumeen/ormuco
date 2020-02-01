## Ormuco

This repository consist of three algorithmic challenges written in python3. A program that checks of two lines overlaps, a library for comparing to app versions to see which is greater, lesser or if they are equal and a data manager for handling geo distributed least recently used cache.

### Quick Testing

There are a handful of test cases created to confirm the functionality of the programs. These tests can be found under `tests/` directory. Follow the steps below to run them locally:

- Clone the repository. From a directory on the terminal. RUN `git clone https://github.com/abdul-mumeen/ormuco.git`
- CD into the project base directory. RUN `cd ormuco`
- Install dependencies. Ensure you have python3 installed then RUN `pip install -r requirements.txt`
- Run all tests. RUN `nose2`. All tests should pass.

### Implementation

This section describe the approaches taken to create the programs along with constrainst, consideration and assumptions made.

#### Overlapping Lines

This program accept two string inputs from the user and return a boolean value. The input is a two number string separated by a space representing the coordinate of each line on the x-axis and the output is boolean which will be `True` when the two lines overlaps and `False` if they don't.

For two lines to overlap, the max coordinate of one line must be greater than the min coordinate of the other line. So a method is created to get the interger format of the coordinate of each line, could be a positive or negative number and exit if the coordinates supply is not an integer or more than two coordinates are supplied. The main method then gets the maximum of the coordinate of first line and the minimum of second line then compare them to see if max is greater min.

To run the program, do:

- From base directory, RUN `python overlap/overlap.py`
- Enter the coordinate of first line then second line e.g `12 3`, `-2 0`

#### Versions Comparism

A version is greater than another if one of its dot separated version number is greater than the equivalent of the other version and lesser if it is the other way round. They aer equal if all dot separated integers are the same.
This library accept two dot separated number strings, extract the number by splitting the string and converting each number string to integer storing them in a list. It then compares each integer in list of the first version to the integer in the list of the second version starting with the first item in each list. If one integer is greater than the second, the version is considered to be greater and the loop is exited but if lesser, the version is said to be lesser and loop is also exited. If the integers are the same for the first item, it move to the next index until end of loop and the versions are said to be equal.

##### Considerations made

- Trailing and leading zeros are ignored.
- Alphanumeric versions are not allowed and considered as invalid. They raise a value error.
- A version with more valid dot separated numbers with the preceeding numbers equal to the other version is considered to be greater.
- Invalid error will be return if any of the versions is invalid.

#### Geo Distributed Least Recently Used Cache

This is a Geo distributed LRU cache system called DataManager. This manager maintain caches from different locations and a database for retrieval data. It retrieves data from LRU cache closest to the user's location (location supplied) if that cache has not expired else it gets it from the next closest. If it tries to get data from an expired cache then it activates it after since it shows that there are users closest to the cache. If the data is not available within the caches then it gets it from the database. When data is retrieved the caches are updated to move the newly retrieved data to the top of the cache.

##### Components

The implementation uses small simple schemas to build different parts of the system and they are highlight below:

**Entry**

This is a class representation of an entry within an LRU cache. It has a left, right, key and value attributes.

- Key: A unique indicator needed to point to the value of the entry in the LRU cache.
- Value: Data of the entry store in LRU cache.
- Right: Entry next to the current entry.
- Left: Entry preceeding the current entry in the cache.

**Location**

A location object that represent the location of a user or a cache. It has x and y attributes which are the coordinate of the location.

**LRUCache**

This class is the implementation of the least recently used cache. It stores data using a combination hashmap and linked list. The most recently accessed data is moved to the top of the list and saved in the hashmap. When new data needs to come in when the list is full, the least recently used data which is always at the bottom of the list is kicked out from the list and deleted from the hashmap. The cache can receive update from a cache object.

- most_recently_used: Property that stores the entry that is at the top of the link list.
- least_recently_used: Property that stores the entry that is at the bottom of the list.
- location: Property indicating the location of the cache.
- id: Used to identify the cache which mainly for the purpose of testing and invalidating cache.
- is_expired: Property to tell if the cache is active or expired.
- activate: Method that activate the cache by setting the is_expired to False.
- deactivate: Method that deactivate the cache by setting the is_expired to True.

**PriorityQueue**

This is an object used to get caches and return them in order of how close they are to the user's location.

**Heuristics/Euclidean Distance**

The is the method used to calculate the distance of each cache to the user's location. It calculates the sum of the absolute difference between the x-coordinate and y-coordinate.

##### Considerations and Missing piece

- Expiration of cache is not time based just simulated. Could be better with timer.
- Size of cache is set to 2 when no size is passed. The system also assumes that all caches in the system will have the same size.
- Getting data from cache return the location of the cache to for testing and confirmation purpose. It returns (-1, -1) for data from database.
- A full location based system using graph can be used.
