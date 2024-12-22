"""Tests for the summary module
"""

import datetime

import pytest

from sxolar.api.arxiv import Author, Category, Entry, Identifier
from sxolar.summary import Format, Summary


class TestSummary:
    """Test the summary module"""

    @pytest.fixture(autouse=True, scope="class")
    def results(self):
        """Return a list of results"""
        return [
            Entry.from_dict(
                {
                    "author": [
                        Author(name="Adrian Del Maestro", affiliation=None),
                        Author(name="Ian Affleck", affiliation=None),
                    ],
                    "category": [
                        Category(
                            term="cond-mat.stat-mech",
                            scheme="http://arxiv.org/schemas/atom",
                        )
                    ],
                    "id": Identifier(number="1005.5383", version="1", is_new=True),
                    "published": datetime.datetime(
                        2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
                    ),
                    "summary": "  Harmonically trapped ultra-cold atoms and helium-4 in nanopores provide new\nexperimental realizations of bosons in one dim...eement is obtained after\nincluding the leading irrelevant interactions in the Hamiltonian which are\ndetermined explicitly.\n",
                    "title": "Interacting bosons in one dimension and Luttinger liquid theory",
                    "updated": datetime.datetime(
                        2010, 5, 28, 20, 0, 5, tzinfo=datetime.timezone.utc
                    ),
                }
            ),
            Entry.from_dict(
                {
                    "author": [
                        Author(name="C. M. Herdman", affiliation=None),
                        Author(name="A. Rommal", affiliation=None),
                        Author(name="A. Del Maestro", affiliation=None),
                    ],
                    "category": [
                        Category(
                            term="cond-mat.stat-mech",
                            scheme="http://arxiv.org/schemas/atom",
                        ),
                        Category(
                            term="cond-mat.other",
                            scheme="http://arxiv.org/schemas/atom",
                        ),
                    ],
                    "id": Identifier(number="1312.6177", version="1", is_new=True),
                    "published": datetime.datetime(
                        2013, 12, 20, 23, 48, 25, tzinfo=datetime.timezone.utc
                    ),
                    "summary": "  A path integral Monte Carlo method based on the worm algorithm has been\ndeveloped to compute the chemical potential of int...re. We speculate on future applications of the proposed\ntechnique, including its use in studies of confined quantum fluids.\n",
                    "title": "Quantum Monte Carlo measurement of the chemical potential of helium-4",
                    "updated": datetime.datetime(
                        2013, 12, 20, 23, 48, 25, tzinfo=datetime.timezone.utc
                    ),
                }
            ),
        ]

    def test_init(self):
        """Test the summary class"""
        smy = Summary("Test", [])
        assert isinstance(smy, Summary)
        assert smy.name == "Test"
        assert smy.results == []
        assert smy.max_authors == 3
        assert smy.include_abstract is False

    def test_format_entry_plain(self, results):
        """Test the format_entry method"""
        smy = Summary("TestPlain", results)
        entry = smy.results[0]
        entry_str = smy._format_entry(entry, Format.Plain)
        assert isinstance(entry_str, str)
        assert entry_str == (
            "Interacting bosons in one dimension and Luttinger liquid theory "
            "[1005.5383v1]\n"
            "Adrian Del Maestro, Ian Affleck\n"
            "\n"
        )

    def test_format_entry_html(self, results):
        """Test the format_entry method"""
        smy = Summary("TestPlain", results)
        entry = smy.results[0]
        entry_str = smy._format_entry(entry, Format.Html)
        assert isinstance(entry_str, str)
        assert entry_str == (
            '<p><h3><a href="http://arxiv.org/abs/1005.5383v1">Interacting bosons in one '
            "dimension and Luttinger liquid theory [1005.5383v1]</a></h3><br>Adrian Del "
            "Maestro, Ian Affleck<br><br></p>"
        )

    def test_to_text(self, results):
        """Test the to_text method"""
        smy = Summary("TestPlain", results)
        text = smy.to_text()
        assert isinstance(text, str)
        assert text == (
            "TestPlain:\n"
            "Interacting bosons in one dimension and Luttinger liquid theory "
            "[1005.5383v1]\n"
            "Adrian Del Maestro, Ian Affleck\n"
            "\n"
            "\n"
            "Quantum Monte Carlo measurement of the chemical potential of helium-4 "
            "[1312.6177v1]\n"
            "C. M. Herdman, A. Rommal, A. Del Maestro\n"
            "\n"
        )

    def test_to_html(self, results):
        """Test the to_html method"""
        smy = Summary("TestHtml", results)
        html = smy.to_html()
        assert isinstance(html, str)
        assert html == (
            "<h2>TestHtml</h2>\n"
            '<p><h3><a href="http://arxiv.org/abs/1005.5383v1">Interacting bosons in one '
            "dimension and Luttinger liquid theory [1005.5383v1]</a></h3><br>Adrian Del "
            "Maestro, Ian Affleck<br><br></p>\n"
            '<p><h3><a href="http://arxiv.org/abs/1312.6177v1">Quantum Monte Carlo '
            "measurement of the chemical potential of helium-4 "
            "[1312.6177v1]</a></h3><br>C. M. Herdman, A. Rommal, A. Del "
            "Maestro<br><br></p>"
        )
