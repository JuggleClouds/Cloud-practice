# -*- coding: utf8 -*-
import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

OPENID_PROVIDERS = [
    #{'name': 'Wargaming', 'url': 'https://ru.wargaming.net/id'},
    # {'name': 'Google', 'url': 'https://accounts.google.com/o/oauth2/v2/auth'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'}
    # {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}
    ]

if os.environ.get('DATABASE_URL') is None:
    # DB Vars
    db_user = 'postgres'
    db_pass = 'postgres'
    db_host = 'localhost'
    db_name = 'blog'
    db_port = '5432'
    # DB Settings
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'.format(
    db_user=db_user,
    db_pass=db_pass,
    db_host=db_host,
    db_name=db_name,
    db_port=db_port
    )
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_RECORD_QUERIES = True
WHOOSH_BASE = os.path.join(basedir, 'search.db')

# Whoosh does not work on Heroku
WHOOSH_ENABLED = os.environ.get('HEROKU') is None

# slow database query threshold (in seconds)
DATABASE_QUERY_TIMEOUT = 0.5

# email server
MAIL_SERVER = 'your.mailserver.com'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']

# available languages
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# microsoft translation service
MS_TRANSLATOR_CLIENT_ID = ''  # enter your MS translator app id here
MS_TRANSLATOR_CLIENT_SECRET = ''  # enter your MS translator app secret here

# administrator list
ADMINS = ['a_pankratyev@wargaming.net']

# pagination
POSTS_PER_PAGE = 50
MAX_SEARCH_RESULTS = 50
