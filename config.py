import os

WTF_CSRF_ENABLED = True
SECRET_KEY = "The peperonizzi always try photogreph me in compromisin position. Unlucky for them" \
             "my head will be soon unstuck from this sodacan. Any minut"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
SQLALCHEMY_COMMIT_ON_TEARDOWN = True

