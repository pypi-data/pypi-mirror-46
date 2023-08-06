RunSpiders
==========

|Python3|

A python library contains some predefined web crawlers.
Attention: this package probably can't work properly because of the correlated webs updates.
If this situation happens, just fix it on your own.

**Installation**

.. code:: bash

    pip install RunSpiders


**Examples**

.. code:: python

    from RunSpiders import NovelSpider

    spider = NovelSpider()
    spider.download_books(['***', 'xxx'])
    # spider.download_books(['***', 'xxx'], style="recipe_first")

.. |Python3| image:: https://img.shields.io/badge/python-3-red.svg

