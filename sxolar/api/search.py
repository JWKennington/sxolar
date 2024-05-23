"""Higher-level api for searching for papers, uses an object interface
with overridden magic methods for syntactic sugar
"""

from sxolar.api import arxiv
from sxolar.api.arxiv import LogicalOperator, SearchField


class Query:
    """Represents a query clause for the arxiv API

    Attributes:
        value (str): The value to search for
        operator (str): The operator to use
    """

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value

    def __and__(self, other):
        return self.and_(other)

    def __or__(self, other):
        return self.or_(other)

    def __sub__(self, other):
        return self.and_not(other)

    def and_(self, other):
        return Query(f'{self}{LogicalOperator.AND}{other}')

    def and_not(self, other):
        return Query(f'{self}{LogicalOperator.AND_NOT}{other}')

    def or_(self, other):
        return Query(f'{self}{LogicalOperator.OR}{other}')

    def wrap(self):
        return Query(f'({self})')

    def search(self, start: int = 0, max_results: int = 10):
        """Searches the arxiv API with the query

        Args:
            start (int, optional): The starting index of the results
            max_results (int, optional): The maximum number of results to return

        Returns:
            list: A list of dictionaries representing the search results
        """
        return arxiv._query(self.value, id_list=None, start=start, max_results=max_results)


class Author(Query):
    """Represents an author query for the arxiv API
    """

    def __init__(self, name: str):
        if not name.startswith(SearchField.AUTHOR):
            name = f'{SearchField.AUTHOR}:{name}'
        super().__init__(name)


class Title(Query):
    """Represents a title query for the arxiv API
    """

    def __init__(self, title: str):
        if not title.startswith(SearchField.TITLE):
            title = f'{SearchField.TITLE}:{title}'
        super().__init__(title)


class Abstract(Query):
    """Represents an abstract query for the arxiv API
    """

    def __init__(self, abstract: str):
        if not abstract.startswith(SearchField.ABSTRACT):
            abstract = f'{SearchField.ABSTRACT}:{abstract}'
        super().__init__(abstract)


class All(Query):
    """Represents an all query for the arxiv API
    """

    def __init__(self, all: str):
        if not all.startswith(SearchField.ALL):
            all = f'{SearchField.ALL}:{all}'
        super().__init__(all)


class JournalRef(Query):
    """Represents a journal reference query for the arxiv API
    """

    def __init__(self, journal_ref: str):
        if not journal_ref.startswith(SearchField.JOURNAL_REFERENCE):
            journal_ref = f'{SearchField.JOURNAL_REFERENCE}:{journal_ref}'
        super().__init__(journal_ref)


class Category(Query):
    """Represents a category query for the arxiv API
    """

    def __init__(self, category: str):
        if not category.startswith(SearchField.CATEGORY):
            category = f'{SearchField.CATEGORY}:{category}'
        super().__init__(category)
