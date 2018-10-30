import requests
import unittest
import schema
from psycopg2 import connect
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class TestPuppiesApi(unittest.TestCase):

    def test_create_a_user(self):
        url = "http://localhost:5000/users"

        payload = "{\n\t\"email\" : \"janet.adrianna.carr@gmail.com\",\n\t\"password\" : \"password\",\n\t\"first_name\" : \"Janet\",\n\t\"last_name\" : \"Carr\"\n}"
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers)
        self.assertEqual(201, response.status_code)


    def test_create_post(self):
        url = "http://localhost:5000/posts"

        payload = "------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"file\"; filename=\"doge.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW\r\nContent-Disposition: form-data; name=\"description\"\r\n\r\nCheck out my new post!\r\n------WebKitFormBoundary7MA4YWxkTrZu0gW--"
        headers = {
            'Content-Type': "multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW",
            'Authorization': "Basic amFuZXQuYWRyaWFubmEuY2FyckBnbWFpbC5jb206cGFzc3dvcmQ=",
            'Cache-Control': "no-cache"
        }
        response = requests.request("POST", url, data=payload, headers=headers)

        self.assertEqual(201, response.status_code)


    def test_get_post(self):
        url = "http://localhost:5000/posts"

        querystring = {"post_id": "1"}

        headers = {
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
            'Authorization': "Basic amFuZXQuYWRyaWFubmEuY2FyckBnbWFpbC5jb206cGFzc3dvcmQ="
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        self.assertEqual(200, response.status_code)


    def test_like_a_post(self):
        url = "http://localhost:5000/likes"

        querystring = {"post_id": "1"}

        payload = ""
        headers = {
            'Authorization': "Basic amFuZXQuYWRyaWFubmEuY2FyckBnbWFpbC5jb206cGFzc3dvcmQ=",
            'Cache-Control': "no-cache"
        }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

        self.assertEqual(201, response.status_code)


    def test_get_feed(self):
        # Get all posts (user feed)
        url = "http://localhost:5000/posts"

        headers = {
            'Authorization': "Basic amFuZXQuYWRyaWFubmEuY2FyckBnbWFpbC5jb206cGFzc3dvcmQ=",
            'Cache-Control': "no-cache"
        }

        response = requests.request("GET", url, headers=headers)

        self.assertEqual(200, response.status_code)


if __name__ == '__main__':
    unittest.main()