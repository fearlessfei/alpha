# *-* coding: utf-8 *-*

import unittest
from tornado.testing import AsyncHTTPTestCase

from cgi import Server


class TestMain(AsyncHTTPTestCase):
    def get_app(self):
        server = Server()
        app = server.app
        return app

    def test_sync(self):
        response = self.fetch('/sync')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'0 users1 so far!')

    def test_gen(self):
        response = self.fetch('/gen-coroutines')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'0 users2 so far!')

    def test_coroutines(self):
        response = self.fetch('/native-coroutines')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'0 users3 so far!')


if __name__ == '__main__':
    unittest.main()
