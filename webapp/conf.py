import os
import logging

DEBUG=False
AUTORELOAD=False
LOG_LEVEL=logging.INFO
REDIS_DB_URL = os.environ.get("REDIS_DB_URL", "redis://redis:6379/0")
SHORTENER_URL = os.environ.get('SHORTENER_URL', "localhost")
HASHIDS_SALT = os.environ.get('HASHIDS_SALT', "default_salt")

try:
    from . localconf import *
except:
    pass