"""Utilities for summarizing the results of arXiv queries.
"""

import enum
from dataclasses import dataclass
from typing import List

from sxolar.api.arxiv import Entry


class Format(str, enum.Enum):
    """An enumeration of formatting options for summaries"""

    Plain = "plain_text"
    Html = "html"


@dataclass
class Summary:
    """A summary of the results of an arXiv query, with optional
    formatting behavior for plain text or html. A summary of results
    is essentially a list of entries with optional formatting options.

    Args:
        name:
            str, the name of the summary
        results:
            List[Entry], the list of entries to summarize
        max_authors:
            int, default 3, the maximum number of authors to include in the summary.
            Set to None to include all authors.
        include_abstract:
            bool, default False, whether to include the abstract in the summary
    """

    name: str
    results: List[Entry]
    max_authors: int = 3
    include_abstract: bool = False

    def _format_entry(self, entry: Entry, format: Format) -> str:
        """Format an entry as a string"""
        authors = (
            entry.author
            if self.max_authors is None
            else entry.author[: self.max_authors]
        )
        authors = ", ".join(str(a) for a in authors)
        title = entry.title
        abstract = entry.summary if self.include_abstract else ""

        if format == Format.Plain:
            return f"{title} [{entry.id}]\n" f"{authors}\n" f"{abstract}\n"

        if format == Format.Html:
            return (
                f"<p>"
                f'<h3><a href="{entry.id.link()}">{title} [{entry.id}]</a></h3><br>'
                f"{authors}<br>"
                f"{abstract}<br>"
                f"</p>"
            )

        raise ValueError(f"Invalid format: {format}, options are {Format}")

    def to_text(self) -> str:
        """Returns the summary as plain text"""
        return f"{self.name}:\n" + "\n".join(
            self._format_entry(entry, Format.Plain) for entry in self.results
        )

    def to_html(self) -> str:
        """Returns the summary as html"""
        return f"<h2>{self.name}</h2>\n" + "\n".join(
            self._format_entry(entry, Format.Html) for entry in self.results
        )
