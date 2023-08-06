Transifex Python Library
========================

This library is a wrapper around the Transifex API, built to provide a
simpler interface to users of the API.

At this moment, it supports only a subset of the endpoints of the API.
In particular, it allows certain operations on Projects, Resources and
Translations.

Usage
-----

Initialization
~~~~~~~~~~~~~~

Before making any requests, you need to setup the HTTP handler, which
will be used for all subsequent requests.

Authentication works both with username/password or with an API token.

.. code:: python

    from txlib_too.http.auth import BasicAuth
    from txlib_too.http.http_requests import HttpRequest
    from txlib_too.registry import registry

    credentials = BasicAuth(username='api', password='')

    host = 'https:/www.transifex.com/'
    conn = HttpRequest(host, auth=credentials)
    registry.setup({'http_handler': conn})


Projects
~~~~~~~~

TODO

Resources
~~~~~~~~~

Get resource
^^^^^^^^^^^^

.. code:: python

    from txlib_too.api.resources import Resource
    from txlib_too.http.exceptions import NotFoundError, ServerError

    try:
        r = Resource.get(project_slug='project_slug', slug='resource_slug')
        print(r.slug) # 'resource_slug'
    except NotFoundError:
        print('Resource not found')
    except ServerError as e:
        print('Exception while retrieving resource: {}'.format(e))


Create/update resource
^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from txlib_too.api.resources import Resource
    from txlib_too.http.exceptions import NotFoundError, ServerError

    try:
        r = Resource.get(project_slug='project_slug', slug='resource_slug')
        # Resource exists, update it
        # Not all fields are allowed here. For example, if i18n_type
        # is provided, the request will fail with a 400 error
        try:
            r.save(content='{"key1": "text1"}')
        except ServerError as e:
            print('Exception while updating resource: {}'.format(e))

    except NotFoundError:
        # Resource does not exist, create one now
        try:
            r = Resource(project_slug='project_slug', slug='resource_slug')
            r.save(name='R1', i18n_type='KEYVALUEJSON', content='{"key1": "text1"}')
        except ServerError as e:
            print('Exception while creating resource: {}'.format(e))

    except ServerError as e:
        print('Exception while retrieving resource: {}'.format(e))

Alternatively, instead of passing all parameters to :code:`save()`, you can
do the following:

.. code:: python

    r = Resource.get(...)
    r.name = '...'
    r.i18n_type = '...'
    r.content = '...'
    r.save()


Translations
~~~~~~~~~~~~

Get translation
^^^^^^^^^^^^^^^
.. code:: python

    from txlib_too.api.translations import Translation
    from txlib_too.http.exceptions import NotFoundError, ServerError

    try:
        t = Translation.get(project_slug='project_slug', slug='resource_slug', lang='translation_language')
        print(t.lang) # 'translation_language'
    except NotFoundError:
        print('Translation not found')
    except ServerError as e:
        print('Exception while retrieving translation: {}'.format(e))


Create/update translation
^^^^^^^^^^^^^^^^^^^^^^^^^
.. code:: python

    from txlib_too.api.translations import Translation
    from txlib_too.http.exceptions import NotFoundError, ServerError

    try:
        t = Translation(
            project_slug=project_slug, slug=resource_slug, lang=language_code
        )
        t.save(content=content)
    except ServerError as e:
        print('Exception while retrieving translation: {}'.format(e))