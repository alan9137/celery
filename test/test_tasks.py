from . import BaseTestCase
from tasks import add, name


class TestApp(BaseTestCase):
    def test_add(self):
        self.tasks = add.apply({"x": 1}, {"y": "2"})
        self.assertEqual(self.tasks.state, "SUCCESS")

    def test_name(self):
        self.tasks = name.apply({"name": "your name"})
        self.assertEqual(self.tasks.state, "SUCCESS")
