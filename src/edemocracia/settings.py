from decouple import config, Csv
import django.conf.global_settings as default
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# APPLICATION SETTINGS
DEBUG = config('DEBUG', cast=bool, default=True)
SECRET_KEY = config('SECRET_KEY', default='secret_key')

RECAPTCHA_SITE_KEY = config(
    'RECAPTCHA_SITE_KEY',
    default='6LeqwioUAAAAAJQwLBKGmmpuazIQM6hEYYoFSTYW'
)
RECAPTCHA_PRIVATE_KEY = config(
    'RECAPTCHA_PRIVATE_KEY',
    default='6LeqwioUAAAAAHs4i1Zq4D_9kc1I-OL0TmaUowq3'
)

SITE_ID = 1
ALLOWED_HOSTS = config('ALLOWED_HOSTS',
                       cast=Csv(lambda x: x.strip().strip(',').strip()),
                       default='*')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + config('DATABASE_ENGINE',
                                                 default='sqlite3'),
        'NAME': config('DATABASE_NAME',
                       default=os.path.join(BASE_DIR, 'db.sqlite3')),
        'USER': config('DATABASE_USER', default=''),
        'PASSWORD': config('DATABASE_PASSWORD', default=''),
        'HOST': config('DATABASE_HOST', default=''),
        'PORT': config('DATABASE_PORT', default=''),
    }
}

ROOT_URLCONF = 'edemocracia.urls'
WSGI_APPLICATION = 'edemocracia.wsgi.application'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.sites',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'constance',
    'constance.backends.database',
    'social_django',

    'apps.core',
    'apps.wikilegis',
    'apps.accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.core.middleware.CookieHandler',

]

# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# REGISTRATION
INCLUDE_REGISTER_URL = False
REGISTRATION_FORM = 'apps.accounts.forms.SignUpAjaxForm'
ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_AUTO_LOGIN = True

# AUTHENTICATION
AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'apps.accounts.backends.AuthenticationEmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# SOCIAL AUTH
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'social_core.pipeline.social_auth.associate_by_email',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',
                                       default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',
                                          default='')

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY', default='')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET', default='')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,first_name,last_name,email'
}

SOCIAL_AUTH_REDIRECT_IS_HTTPS = config('SOCIAL_AUTH_REDIRECT_IS_HTTPS',
                                       default=True, cast=bool)

# INTERNATIONALIZATION
LANGUAGE_CODE = config('LANGUAGE_CODE', default='pt-br')
TIME_ZONE = config('TIME_ZONE', default='America/Sao_Paulo')
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

LANGUAGES = (
    ('en', 'English'),
    ('pt-br', 'Brazilian Portuguese'),
)

# EMAIL SETTINGS
EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', cast=int, default=587)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool, default=True)
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='')

# STATICFILES SETTINGS
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public'))

STATICFILES_FINDERS = default.STATICFILES_FINDERS + [
    'npm.finders.NpmFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'constance.context_processors.config',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

# E-DEMOCRACIA PLUGINS
WIKILEGIS_ENABLED = config('WIKILEGIS_ENABLED', default=True, cast=bool)
WIKILEGIS_UPSTREAM = config('WIKILEGIS_UPSTREAM',
                            default='http://localhost:7000')
WIKILEGIS_API_URL = config('WIKILEGIS_API_URL', default='/api/v1/')
WIKILEGIS_API_KEY = config('WIKILEGIS_API_KEY', default='apikey')


# EDITABLE SETTINGS
CONSTANCE_CONFIG = {
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'
