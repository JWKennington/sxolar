"""Utilities for summarizing the results of arXiv queries.
"""

import datetime
import enum
from dataclasses import dataclass
from typing import List, Optional

from sxolar.api.arxiv import Entry
from sxolar.api.search import Query


class Format(str, enum.Enum):
    """An enumeration of formatting options for summaries"""

    Plain = "plain_text"
    Html = "html"


@dataclass
class Section:
    """A section of the results of an arXiv query, with optional
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
        max_results:
            int, default 50, the maximum number of results to include in the summary
        trailing:
            Optional[int], the number of days to include in the summary. If None,
            include all results.
        trailing_unit:
            str, default "days", the unit of time for the trailing period, must be a
            valid argument for datetime.timedelta
    """

    name: str
    query: Query
    results: List[Entry] = None
    max_authors: int = 3
    include_abstract: bool = False
    max_results: int = 50
    trailing: Optional[int] = None
    trailing_unit: str = "days"

    def _format_entry(
        self,
        entry: Entry,
        format: Format,
        starting_header: int = 3,
    ) -> str:
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
                f'<h{starting_header}><a href="{entry.id.link()}">{title} '
                f"[{entry.id}]</a></h{starting_header}><br>"
                f"{authors}<br>"
                f"{abstract}<br>"
                f"</p>"
            )

        raise ValueError(f"Invalid format: {format}, options are {Format}")

    def refresh(self):
        """Refresh the results of the query"""
        kwargs = {
            "start": 0,
            "max_results": self.max_results,
        }

        # Add time filters if specified
        if self.trailing is not None:
            # Format timedelta
            td = datetime.timedelta(**{self.trailing_unit: self.trailing})
            # Get the current date
            now = datetime.datetime.now(datetime.UTC)
            # Subtract the timedelta
            start_date = now - td
            kwargs["min_date"] = start_date
            kwargs["max_date"] = now

        # run the search
        self.results = self.query.search(**kwargs)

    def to_text(self) -> str:
        """Returns the summary as plain text"""
        return f"{self.name}:\n" + "\n".join(
            self._format_entry(entry, Format.Plain) for entry in self.results
        )

    def to_html(self, starting_header: int = 2) -> str:
        """Returns the summary as html"""
        return f"<h{starting_header}>{self.name}</h{starting_header}>\n" + "\n".join(
            self._format_entry(entry, Format.Html, starting_header=starting_header + 1)
            for entry in self.results
        )

    @staticmethod
    def from_combo(
        name: str,
        authors: List[str] = None,
        alls: List[str] = None,
        max_authors: int = 3,
        include_abstract: bool = False,
        max_results: int = 50,
        trailing: Optional[int] = None,
        trailing_unit: str = "days",
    ) -> "Section":
        """Create a section from a combination of arguments

        Args:

        """
        if authors is None and alls is None:
            raise ValueError("At least one of authors or alls must be specified")

        query = Query.from_combo(
            authors=authors,
            alls=alls,
        )

        return Section(
            name=name,
            query=query,
            max_authors=max_authors,
            include_abstract=include_abstract,
            max_results=max_results,
            trailing=trailing,
            trailing_unit=trailing_unit,
        )


@dataclass
class Summary:
    """A summary is a named collection of sections, with formatting metadata

    Args:
        name:
            str, the name of the summary
        sections:
            List[Section], a list of sections to include in the summary
    """

    name: str
    sections: List[Section]

    def refresh(self):
        """Refresh the results of the query"""
        for section in self.sections:
            section.refresh()

    def to_text(self) -> str:
        """Returns the summary as plain text"""
        return "\n\n".join(section.to_text() for section in self.sections)

    def to_html(self) -> str:
        """Returns the summary as html"""
        return "<br><br>".join(section.to_html() for section in self.sections)