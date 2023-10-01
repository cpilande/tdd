"""
Test Cases for Counter Web Service

Create a service that can keep a track of multiple counters
- API must be RESTful - see the status.py file. Following these guidelines, you can make assumptions about
how to call the web service and assert what it should return.
- The endpoint should be called /counters
- When creating a counter, you must specify the name in the path.
- Duplicate names must return a conflict error code.
- The service must be able to update a counter by name.
- The service must be able to read the counter
"""
from unittest import TestCase
import json 

# we need to import the unit under test - counter
from src.counter import app 

# we need to import the file that contains the status codes
from src import status 

class CounterTest(TestCase):
    """Counter tests"""
    def setUp(self):
        self.client = app.test_client()

    def test_create_a_counter(self):
        """It should create a counter"""
        client = app.test_client()
        result = client.post('/counters/foo')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_duplicate_a_counter(self):
        """It should return an error for duplicates"""
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        result = self.client.post('/counters/bar')
        self.assertEqual(result.status_code, status.HTTP_409_CONFLICT)

    def test_update_a_counter(self):
        """It should update a counter"""
        client = app.test_client()
        result = client.post('/counters/new')

        check = json.loads(result.data)
        check["new"] = check["new"] + 1 # updates the dictionary value by 1

        if result.status_code == status.HTTP_201_CREATED:
            result2 = self.client.put('/counters/new') #calls update function 

            self.assertEqual(result2.status_code, status.HTTP_200_OK)

            actual = json.loads(result2.data)

            self.assertEqual(actual, check)
    
    def test_read_counter(self):
        """It should read a counter"""
        client = app.test_client()
        result = client.post('/counters/new2')
        result = client.get('/counters/new2')

        self.assertEqual(result.status_code, status.HTTP_200_OK)

        result2 = client.get('/counters/doesnotexist')
        self.assertEqual(result2.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_counter(self):
        """It should delete a counter"""
        client = app.test_client()

        result = client.post('/counters/toDelete')
        result = client.delete('/counters/toDelete')

        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)

        result = client.delete('/counters/toDelete')

        self.assertEqual(result.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)