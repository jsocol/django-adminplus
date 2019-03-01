import django

INSTALLED_APPS = [
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.auth',
    'django.contrib.staticfiles',
]

if django.VERSION >= (2, 1):
    INSTALLED_APPS += [
        'adminplus.apps.AdminPlusConfig',
    ]
else:
    INSTALLED_APPS += [
        'django.contrib.admin',
        'adminplus',
    ]

INSTALLED_APPS += [
    'test_app',
]

DEBUG = True
SECRET_KEY = 'adminplus'

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

STATIC_URL = '/static/'

if django.VERSION < (2, 0):
    ROOT_URLCONF = 'test_urlconf'
else:
    ROOT_URLCONF = 'test_urlconf2'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
