=============================
django-trojsten-news
=============================

.. image:: https://badge.fury.io/py/django-trojsten-news.png
    :target: https://badge.fury.io/py/django-trojsten-news

.. image:: https://travis-ci.org/trojsten/news.png?branch=master
    :target: https://travis-ci.org/trojsten/news

.. image:: https://codecov.io/gh/trojsten/news/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/trojsten/news

News for django used in Trojsten seminary web apps

Quickstart
----------

Install trojsten_django_news::

    pip install django-trojsten-news

Then use it in a project::

    import news

Features
--------

* News
* Markdown
* RSS feed

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_dev.txt
    (myenv) $ python example/manage.py test

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
