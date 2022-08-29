from . import BaseTestCase
from unittest.mock import patch


class TestApp(BaseTestCase):
    @patch("app.add.delay")
    def test_post_add(self, mock_add):
        response = self.client.post(
            "/post_add",
            json={
                "x": 1,
                "y": 2
            },
        )
        self.assertTrue(mock_add.called)
        self.assertEqual(response.status_code, 200)

    @patch("app.name.delay")
    def test_get_name(self, mock_name):
        response = self.client.get(
            "/get_name",
            query_string=({"name": "your name"})
        )
        self.assertTrue(mock_name.called)
        self.assertEqual(response.status_code, 200)

    @patch("app.AsyncResult")
    def test_get_id(self, mock_AsyncResult):
        response = self.client.get(
            "/get_id",
            query_string=({"id": "9bc07713-640d-4cbc-8074-74cbf765c635"})
        )
        self.assertTrue(mock_AsyncResult.called)
        self.assertEqual(response.status_code, 200)
