#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/balon/")

from balon import app as application
application.secret_key = 'Add your secret key'

bind = '127.0.0.1:9090'
workers = 1
worker_class = 'eventlet'
user = 'www-data'
group = 'www-data'
errorlog = '/var/log/balon/prod/gunicorn-error.log'
accesslog = '/var/log/balon/prod/gunicorn-access.log'
