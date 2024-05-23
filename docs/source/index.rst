.. sXolar documentation master file

sXolar, Scholar's tools for working with arXiv
==============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:


The sXolar package is a collection of tools for working with arXiv data.
It includes low-level and high-level interfaces for querying arXiv metadata,
summarizing query results into digest formats, based on a configuration file.


Getting Started
===============


Installation
------------

To install sXolar, run the command:

.. code-block:: bash

    pip install sxolar

This will install the sXolar package and all of its dependencies.


Simple Usage
------------

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


sXolar API
==========

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
