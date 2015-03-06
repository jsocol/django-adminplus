INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.admin',
    'adminplus',
)

SECRET_KEY = 'adminplus'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    },
}

ROOT_URLCONF = 'test_urlconf'
MIDDLEWARE_CLASSES = ()
