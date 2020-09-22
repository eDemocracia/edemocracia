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

SITE_URL = config('SITE_URL', default='http://localhost:8000')

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
    'rest_framework',
    'macros',
    'compressor',
    'compressor_toolkit',
    'widget_tweaks',
    'corsheaders',

    'apps.core',
    'apps.wikilegis',
    'apps.accounts',
    'apps.pautas',
    'apps.audiencias',
    'apps.discourse',
    'apps.about',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'corsheaders.middleware.CorsMiddleware',
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
    'apps.accounts.backends.CamaraOAuth2',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'apps.accounts.backends.AuthenticationEmailBackend',
    'django.contrib.auth.backends.ModelBackend',
)

LOGIN_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

# SOCIAL AUTH
SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'apps.accounts.pipeline.save_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY',
                                       default='')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET',
                                          default='')

SOCIAL_AUTH_FACEBOOK_KEY = config('SOCIAL_AUTH_FACEBOOK_KEY', default='')
SOCIAL_AUTH_FACEBOOK_SECRET = config('SOCIAL_AUTH_FACEBOOK_SECRET', default='')
SOCIAL_AUTH_FACEBOOK_SCOPE = config('SOCIAL_AUTH_FACEBOOK_SCOPE',
                                    cast=Csv(lambda x: x.strip().strip(',').strip()), # noqa
                                    default='email, user_birthday, user_location')    # noqa
SOCIAL_AUTH_FACEBOOK_API_VERSION = config('SOCIAL_AUTH_FACEBOOK_API_VERSION',
                                          default='3.2')
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email,gender,picture,birthday,location'
}

SOCIAL_AUTH_CAMARA_DEPUTADOS_KEY = config('SOCIAL_AUTH_CD_KEY', default='')
SOCIAL_AUTH_CAMARA_DEPUTADOS_SECRET = config('SOCIAL_AUTH_CD_SECRET',
                                             default='')
SOCIAL_AUTH_CAMARA_DEPUTADOS_VERIFY_SSL = config('SOCIAL_AUTH_CD_VERIFY_SSL',
                                                 default=True, cast=bool)
CAMARA_DEPUTADOS_AUTHORIZATION_URL = config('CD_AUTHORIZATION_URL', default='')
CAMARA_DEPUTADOS_ACCESS_TOKEN_URL = config('CD_ACCESS_TOKEN_URL', default='')
CAMARA_DEPUTADOS_METADATA_URL = config('CD_METADATA_URL', default='')

SOCIAL_AUTH_REDIRECT_IS_HTTPS = config('SOCIAL_AUTH_REDIRECT_IS_HTTPS',
                                       default=True, cast=bool)

CAMARA_LOGIN = config('CAMARA_LOGIN', default=False, cast=bool)

# API
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}

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
EMAIL_BACKEND = config('EMAIL_BACKEND',
                       default='django.core.mail.backends.console.EmailBackend')

# STATICFILES SETTINGS
STATIC_URL = config('STATIC_URL', default='/static/')
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'static'))

STATICFILES_FINDERS = default.STATICFILES_FINDERS + [
    'npm.finders.NpmFinder',
    'compressor.finders.CompressorFinder',
]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/edem-navigation/static'),
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'apps/about/static'),
]

NPM_ROOT_PATH = os.path.dirname(BASE_DIR)

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
                'apps.core.processors.settings_variables',
            ],
        },
    },
]

MEDIA_URL = config('MEDIA_URL', default='/media/')
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'public', 'media'))

COMPRESS_PRECOMPILERS = [
    ('text/x-scss', 'compressor_toolkit.precompilers.SCSSCompiler'),
]

NODE_MODULES = os.path.join(os.path.dirname(BASE_DIR), 'node_modules')
COMPRESS_NODE_MODULES = NODE_MODULES
COMPRESS_NODE_SASS_BIN = os.path.join(NODE_MODULES, '.bin/node-sass')
COMPRESS_POSTCSS_BIN = os.path.join(NODE_MODULES, '.bin/postcss')
COMPRESS_OFFLINE = config('COMPRESS_OFFLINE', cast=bool, default=False)

if not DEBUG:
    COMPRESS_SCSS_COMPILER_CMD = '{node_sass_bin}' \
                                 ' --source-map true' \
                                 ' --source-map-embed true' \
                                 ' --source-map-contents true' \
                                 ' --output-style expanded' \
                                 ' {paths} "{infile}" "{outfile}"' \
                                 ' &&' \
                                 ' {postcss_bin}' \
                                 ' --use "{node_modules}/autoprefixer"' \
                                 ' --autoprefixer.browsers' \
                                 ' "{autoprefixer_browsers}"' \
                                 ' -r "{outfile}"'

# E-DEMOCRACIA PLUGINS
WIKILEGIS_ENABLED = config('WIKILEGIS_ENABLED', default=False, cast=bool)
WIKILEGIS_UPSTREAM = config('WIKILEGIS_UPSTREAM',
                            default='http://localhost:7000')
WIKILEGIS_API_URL = config('WIKILEGIS_API_URL', default='/api/v1/')
WIKILEGIS_API_KEY = config('WIKILEGIS_API_KEY', default='apikey')

PAUTAS_ENABLED = config('PAUTAS_ENABLED', default=False, cast=bool)
PAUTAS_UPSTREAM = config('PAUTAS_UPSTREAM', default='http://localhost:9000')
PAUTAS_API_URL = config('PAUTAS_API_URL', default='/api/v1/')
PAUTAS_API_KEY = config('PAUTAS_API_KEY', default='api_key')

AUDIENCIAS_ENABLED = config('AUDIENCIAS_ENABLED', default=False, cast=bool)
AUDIENCIAS_UPSTREAM = config('AUDIENCIAS_UPSTREAM',
                             default='http://localhost:6000/audiencias')
AUDIENCIAS_API_URL = config('AUDIENCIAS_API_URL', default='/api/')
AUDIENCIAS_API_KEY = config('AUDIENCIAS_API_KEY', default='secret_key')

DISCOURSE_ENABLED = config('DISCOURSE_ENABLED', default=False, cast=bool)
DISCOURSE_UPSTREAM = config('DISCOURSE_UPSTREAM',
                            default='http://localhost:3000/expressao')
DISCOURSE_SSO_SECRET = config('DISCOURSE_SSO_SECRET', default='sso_secret')


# EDITABLE SETTINGS
CONSTANCE_ADDITIONAL_FIELDS = {
    'image_field': ['django.forms.ImageField', {}]
}

CONSTANCE_CONFIG = {
    'SITE_LOGO': ('logo-camara-color.svg', 'Logo do topo', 'image_field'),
    'SITE_NAME': ('Câmara dos Deputados', 'Nome do site', str),
    'DESCRIPTION': ('Este Portal foi criado para ampliar a participação '
                    'social no processo legislativo e aproximar cidadãos e '
                    'seus representantes por meio da interação digital.',
                    'Descrição da barra superior e rodapé de site', str),
    'TOS_DESCRIPTION': ('Condições gerais aplicáveis à utilização do site e '
                        'de suas ferramentas associadas', 'Descrição dos '
                        'Termos de Serviço', str),
    'AUDIENCIAS_TITLE': ('FAÇA SUA PERGUNTA', 'Título da seção do Audiências '
                         'Interativas', str),
    'AUDIENCIAS_DESCRIPTION': ('Acompanhe audiências ao vivo e participe '
                               'enviando perguntas.', 'Descrição da seção do '
                               'Audiências Interativas', str),
    'WIKILEGIS_TITLE': ('CONTRIBUA EM PROJETOS DE LEI', 'Título da seção do'
                        'Wikilegis', str),
    'WIKILEGIS_DESCRIPTION': ('Edite e aprimore projetos de lei artigo por '
                              'artigo.', 'Descrição da seção do Wikilegis',
                              str),
    'EXPRESSAO_TITLE': ('PARTICIPE EM DISCUSSÕES', 'Título da seção do '
                        'Expressão', str),
    'EXPRESSAO_DESCRIPTION': ('Dê sua opinião sobre os assuntos que afetam '
                              'a sua vida, discutindo soluções com outros '
                              'cidadãos e os deputados.', 'Descrição da seção '
                              'do Expressão', str),
    'PAUTAS_TITLE': ('COLOQUE PROJETOS NA PAUTA', 'Título da seção do Pauta '
                     'Participativa', str),
    'PAUTAS_DESCRIPTION': ('Vote nos assustos a serem abordados em plenário.',
                           'Título da seção do Pauta Participativa', str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'General Options': ('SITE_NAME', 'SITE_LOGO', 'DESCRIPTION',
                        'TOS_DESCRIPTION'),
    'Audiências Options': ('AUDIENCIAS_TITLE', 'AUDIENCIAS_DESCRIPTION'),
    'Wikilegis Options': ('WIKILEGIS_TITLE', 'WIKILEGIS_DESCRIPTION'),
    'Expressão Options': ('EXPRESSAO_TITLE', 'EXPRESSAO_DESCRIPTION'),
    'Pauta Participativa Options': ('PAUTAS_TITLE', 'PAUTAS_DESCRIPTION'),
}

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

# THIRD PARTY LIBRARIES
GOOGLE_ANALYTICS_ID = config('GOOGLE_ANALYTICS_ID', default=None)
OLARK_ID = config('OLARK_ID', default=None)

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_URLS_REGEX = r'^/api/.*$'