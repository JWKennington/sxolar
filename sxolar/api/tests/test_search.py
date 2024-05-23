"""Tests for search api
"""

from sxolar.api.search import Author, Title


class TestSearchAPI:
    """Test the search API"""

    def test_query(self):
        """Test the query function"""
        res = Author('del maestro').search()
        assert len(res) == 10

    def test_query_andnot(self):
        """Test the query function"""
        res = (Author('del maestro') - (Title('checkerboard') | Title('Pyrochlore'))).search()
        assert len(res) == 10


