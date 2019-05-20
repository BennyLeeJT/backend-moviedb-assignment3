.. image:: https://travis-ci.org/alberanid/imdbpy.svg?branch=master
    :target: https://travis-ci.org/alberanid/imdbpy

**IMDbPY** is a Python package for retrieving and managing the data
of the `IMDb`_ movie database about movies, people and companies.

:Homepage: https://imdbpy.sourceforge.io/
:PyPI: https://pypi.org/project/IMDbPY/
:Repository: https://github.com/alberanid/imdbpy
:Documentation: https://imdbpy.readthedocs.io/
:Support: https://imdbpy.sourceforge.io/support.html

.. admonition:: Revamp notice
   :class: note

   Starting on November 2017, many things were improved and simplified:

   - moved the package to Python 3 (compatible with Python 2.7)
   - removed dependencies: SQLObject, C compiler, BeautifulSoup
   - removed the "mobile" and "httpThin" parsers
   - introduced a test suite (`please help with it!`_)


Main features
-------------

- written in Python 3 (compatible with Python 2.7)

- platform-independent

- can retrieve data from both the IMDb's web server, or a local copy
  of the database

- simple and complete API

- released under the terms of the GPL 2 license

IMDbPY powers many other software and has been used in various research papers.
`Curious about that`_?


Installation
------------

Whenever possible, please use the latest version from the repository::

   pip install git+https://github.com/alberanid/imdbpy


But if you want, you can also install the latest release from PyPI::

   pip install imdbpy


Example
-------

Here's an example that demonstrates how to use IMDbPY:

.. code-block:: python

   from imdb import IMDb

   # create an instance of the IMDb class
   ia = IMDb()

   # get a movie
   movie = ia.get_movie('0133093')

   # print the names of the directors of the movie
   print('Directors:')
   for director in movie['directors']:
       print(director['name'])

   # print the genres of the movie
   print('Genres:')
   for genre in movie['genres']:
       print(genre)

   # search for a person name
   people = ia.search_person('Mel Gibson')
   for person in people:
      print(person.personID, person['name'])


.. _IMDb: https://www.imdb.com/
.. _please help with it!: http://imdbpy.readthedocs.io/en/latest/devel/test.html
.. _Curious about that: https://imdbpy.sourceforge.io/ecosystem.html
