========
Usage
========

To use profile-middleware in a project::

    pip install profile-middleware

now add it to INSTALLED_APPS

    INSTALLED_APPS += ('profiler',)

Add the middleware class

    MIDDLEWARE_CLASSES += ('profiler.middleware.ProfileMiddleware',)

To see profiling results, just visit a url of your django app and add

    <url>?prof=time

this will show you a view with profiling details
