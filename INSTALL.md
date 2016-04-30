WCIVF requires Python 3.

To install:

    sudo apt-get install python3-dev libpq-dev libjpeg-dev
    sudo gem install --no-ri --no-rdoc sass -v 3.4.21`
    pip install -r requirements/local.txt
    python manage.py migrate
    python manage.py import_elections
    manage.py import_posts
    manage.py import_parties
    manage.py import_people

If you don't want to install Redis for some reason (like e.g. laziness) you can override
the cache backend with a file at `./wcivf/settings/local.py` with the following:

    CACHES = {
           'default': {
                   'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
                      }
             }
