===========
Tweet Model
===========


.. image:: https://img.shields.io/pypi/v/tweet_model_serpucga.svg
        :target: https://pypi.python.org/pypi/tweet_model_serpucga

.. image:: https://readthedocs.org/projects/tweet-model/badge/?version=latest
        :target: https://tweet-model.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status




A modelization of a tweet object with convenient features and functionalities.
This project was thought for integration and usage as a package by the Twitter
Dashboard project.


* Free software: MIT license
* Documentation: https://tweet-model.readthedocs.io.


Features
--------

* A modelization of a tweet in the form of class Tweet. This class contains a
  constructor that initializes all the possible tweet attributes to None
  except those indicated otherwise.
* The inner objects of a tweet ("user", "entities", "places", etc.) are stored
  internally as nested dictionaries.
* The __getitem__() method for Tweet is overriden to allow a dictionary-like
  access to the tweet contents. For example, if "tweet1" is an instance of
  Tweet, one could do tweet1["id"] to get the id of that tweet, or
  tweet1["user"]["name"] to get the name of the person that published the
  tweet.

Credits
-------
Creator: Sergio

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
