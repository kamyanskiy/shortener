import asyncio
import hashids
import redis
import logging

from tornado.platform.asyncio import AsyncIOMainLoop
import tornado.web

from webapp.handlers import MainHandler
from . import conf


logging.basicConfig(level=conf.LOG_LEVEL)
logger = logging.getLogger(__name__)


class ShortenerApplication(tornado.web.Application):
    hasher = hashids.Hashids(salt=conf.HASHIDS_SALT, min_length=5)
    db = redis.from_url(conf.REDIS_DB_URL)


def make_app():
    return ShortenerApplication([
        (r"/", MainHandler),
        (r'/(?P<hash>[\w-]+)', MainHandler)
    ], debug=conf.DEBUG, autoreload=conf.AUTORELOAD)


def start_app():
    AsyncIOMainLoop().install()
    app = make_app()
    app.listen(8888)
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    try:
        logger.debug("Listen port: 8888")
        loop.run_forever()
    except KeyboardInterrupt:
        logger.debug("Exit webapp")
    finally:
        loop.stop()
        loop.close()