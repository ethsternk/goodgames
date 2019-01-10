from django.test import TestCase
from goodgames.views import igdb_request


class TestViewHelpers(TestCase):
    def test_igdb_request(self):
        self.assertTrue(igdb_request(1))
