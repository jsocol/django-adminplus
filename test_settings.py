import django

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.admin',
    'adminplus',
)

SECRET_KEY = 'adminplus'

if django.VERSION >= (1, 10):
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': (),
            'OPTIONS': {
                'autoescape': False,
                'loaders': (
                    'django.template.loaders.filesystem.Loader',
                    'django.template.loaders.app_directories.Loader',
                ),
                'context_processors': (
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.request',
                    'django.template.context_processors.static',
                    'django.contrib.auth.context_processors.auth',
                ),
            },
        },
    ]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test.db',
    },
}

ROOT_URLCONF = 'test_urlconf'
MIDDLEWARE_CLASSES = ()
