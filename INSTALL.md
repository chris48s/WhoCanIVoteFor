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


## Creating inline CSS

The CSS for this project is inlined in the base template for performance reasons.

This is created using [`critical`](https://github.com/addyosmani/critical), and can be re-created by running

```
curl localhost:8000 | critical --base wcivf -m > wcivf/templates/_compressed_css.html
```

