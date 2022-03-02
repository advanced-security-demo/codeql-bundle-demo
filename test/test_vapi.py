import json
import unittest

from test import BaseTestCase


class TestvAPI(BaseTestCase):
    def test_tokens_1(self):
        headers = {"Content-type": "application/json"}
        r = self.client.open(
            "/tokens",
            method="POST",
            data=json.dumps({"username": "blah1'", "password": "blah"}),
            headers=headers,
        )
        print(r.status_code, r.data)
        self.assertEqual(r.status_code, 500)

    def test_tokens_2(self):
        headers = {"Content-type": "application/json"}
        r = self.client.open(
            "/tokens",
            method="POST",
            data=json.dumps({"username": "blah1'", "password": "blah"}),
            headers=headers,
        )
        print(r.status_code, r.data)
        self.assertEqual(r.status_code, 500)

    def test_tokens_3(self):
        headers = {"Content-type": "application/json"}
        r = self.client.open(
            "/tokens",
            method="POST",
            data=json.dumps({"username": "blah1'", "password": "blah"}),
            headers=headers,
        )
        print(r.status_code, r.data)
        self.assertEqual(r.status_code, 500)

    def test_tokens_4(self):
        headers = {"Content-type": "application/json"}
        r = self.client.post(
            "/tokens",
            data=json.dumps({"username": "blah1'", "password": "blah"}),
            headers=headers,
        )
        print(r.status_code, r.data)
        self.assertEqual(r.status_code, 500)

    def test_widget_1(self):
        headers = {
            "Content-type": "application/json",
            "X-Auth-Token": "4d94fc705cd9b2b36b2280dd543d9004",
        }
        r = self.client.post(
            "/widget", data=json.dumps({"name": "blah1"}), headers=headers
        )
        # print(r.status_code, r.data)
        self.assertEqual(r.status_code, 200)

    def test_widget_2(self):
        headers = {
            "Content-type": "application/json",
            "X-Auth-Token": "4d94fc705cd9b2b36b2280dd543d9004",
        }
        r = self.client.post(
            "/widget", data=json.dumps({"name": "blah"}), headers=headers
        )
        self.assertEqual(r.status_code, 403)

    def test_widget_3(self):
        headers = {
            "Content-type": "application/json",
            "X-Auth-Token": "tokenwithsinglequote'",
        }
        r = self.client.post(
            "/widget", data=json.dumps({"name": "blah1"}), headers=headers
        )
        self.assertEqual(r.status_code, 500)

    def test_widget_4(self):
        headers = {"Content-type": "application/json", "X-Auth-Token": "unknowntoken"}
        r = self.client.post(
            "/widget", data=json.dumps({"name": "blah1"}), headers=headers
        )
        self.assertEqual(r.status_code, 401)


if __name__ == "__main__":
    unittest.main()
