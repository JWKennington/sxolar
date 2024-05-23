.. sXolar documentation master file

Scholar's tools for arXiv
=========================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


.. image:: sxolar.png
    :align: center
    :width: 200px
    :alt: sXolar logo


The sXolar package is a collection of tools for working with arXiv data.
It includes low-level and high-level interfaces for querying arXiv metadata,
summarizing query results into digest formats, based on a configuration file.

The tools are written in Python and are designed to be used in any python application. The tools are designed to be
used in place of the [Arxiv API](https://arxiv.org/help/api/index), with a simpler interface and more features, including

* Searching and downloading papers
* Creating personalized search indices for easy repeated searches
* Exploring the network of citations between papers

Ultimately, the goal of this project is to provide a set of tools that can be used to build a personalized search engine
for academic papers, with the ability to search, download, and explore the network of citations between papers.


Getting Started
---------------


Installation
~~~~~~~~~~~~

To install sXolar, run the command:

.. code-block:: bash

    pip install sxolar

This will install the sXolar package and all of its dependencies.


Simple Usage
~~~~~~~~~~~~

The high-level api provides a simple object-oriented interface for constructing
and executing queries. Here is an example of how to use the high-level api:

.. code-block:: python

    from sxolar import Author

    query = Author('John Doe') | Author('Jane Doe')
    query.search()


Note that some builtin python operations have been overloaded to provide a more
intuitive interface for constructing queries. For example, the `|` operator is
overloaded to represent a logical OR operation between two query objects. For more
information on the high-level api, see the :ref:`api/index`.


Quick Examples
~~~~~~~~~~~~~~

Here are some quick examples of how to use the sXolar package.

Search for papers by a specific author:

.. code-block:: python

    from sxolar import Author

    query = Author('John Doe')
    query.search()

Search for papers by multiple authors (logical OR):

.. code-block:: python

    from sxolar import Author

    query = Author('John Doe') | Author('Jane Doe')
    query.search()


Search for papers by a specific title:

.. code-block:: python

    from sxolar import Title

    query = Title('Quantum Mechanics')
    query.search()


Search for papers with a specific title, but not by a specific author:

.. code-block:: python

    from sxolar import Title, Author

    query = Title('Quantum Mechanics') - Author('John Doe')
    query.search()


Search for papers with a specific title, but not by a specific set of authors:

.. code-block:: python

    from sxolar import Title, Author

    query = Title('Quantum Mechanics') - (Author('John Doe') | Author('Jane Doe')).wrap()
    query.search()


sXolar API
----------

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index




Indices and tables
------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


Acknowledgements
----------------

Thank you to arXiv for use of its open access interoperability.
