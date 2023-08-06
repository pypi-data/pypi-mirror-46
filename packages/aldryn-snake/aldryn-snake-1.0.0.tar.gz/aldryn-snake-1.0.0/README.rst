============
Aldryn Snake
============

|pypi| |build| |coverage|

**Aldryn Snake** adds tail and head context processors for addons similar to
`django-sekizai <https://github.com/divio/django-sekizai>`_.

This addon still uses the legacy "Aldryn" naming. You can read more about this in our
`support section <https://support.divio.com/general/faq/essential-knowledge-what-is-aldryn>`_.


Contributing
============

This is a an open-source project. We'll be delighted to receive your
feedback in the form of issues and pull requests. Before submitting your
pull request, please review our `contribution guidelines
<http://docs.django-cms.org/en/latest/contributing/index.html>`_.

We're grateful to all contributors who have helped create and maintain this package.
Contributors are listed at the `contributors <https://github.com/divio/aldryn-snake/graphs/contributors>`_
section.


Documentation
=============

See ``REQUIREMENTS`` in the `setup.py <https://github.com/divio/aldryn-snake/blob/master/setup.py>`_
file for additional dependencies:

|python| |django|


Installation
------------

* add ``aldryn_snake.template_api.template_processor`` to your TEMPLATE_CONTEXT_PROCESSORS settings
* somewhere in your app (that will be imported on startup (models, admin etc) add something to the api::

    # -*- coding: utf-8 -*-
    from aldryn_snake.template_api import registry
    from django.conf import settings

    OPTIMIZELY_SCRIPT = """<script src="//cdn.optimizely.com/js/%(account_number)s.js"></script>"""


    def get_crazyegg_script():
      optimizely_number = getattr(settings, 'OPTIMIZELY_ACCOUNT_NUMBER', None)
      if optimizely_number:
          return OPTIMIZELY_SCRIPT % {'account_number': optimizely_number}
       else:
          return ''

    registry.add_to_tail(get_crazyegg_script())


If ``add_to_tail`` or ``add_to_head`` receive a callable, it will be called with the ``request``
keyword argument.


* add the following in your base template to the HEAD::

    {{ ALDRYN_SNAKE.render_head }}

* add the following in your base template right above </BODY>::

    {{ ALDRYN_SNAKE.render_tail }}


Running Tests
-------------

You can run tests by executing::

    virtualenv env
    source env/bin/activate
    pip install -r tests/requirements.txt
    python setup.py test


.. |pypi| image:: https://badge.fury.io/py/aldryn-snake.svg
    :target: http://badge.fury.io/py/aldryn-snake
.. |build| image:: https://travis-ci.org/divio/aldryn-snake.svg?branch=master
    :target: https://travis-ci.org/divio/aldryn-snake
.. |coverage| image:: https://codecov.io/gh/divio/aldryn-snake/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/divio/aldryn-snake

.. |python| image:: https://img.shields.io/badge/python-2.7%20%7C%203.4+-blue.svg
    :target: https://pypi.org/project/aldryn-snake/
.. |django| image:: https://img.shields.io/badge/django-1.11%20%7C%202.1%20%7C%202.2-blue.svg
    :target: https://www.djangoproject.com/
