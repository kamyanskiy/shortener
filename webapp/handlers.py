import logging
import traceback
import tornado.web

from . import conf


logging.basicConfig(level=conf.LOG_LEVEL)
logger = logging.getLogger(__name__)


class MainHandler(tornado.web.RequestHandler):

    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        self.set_header('Content-Type', 'application/json')
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            self.finish({"code": status_code,
                         "message": self._reason,
                        })

    async def get(self, *args, **kwargs):
        return await self.handler(*args, **kwargs)

    async def post(self, *args, **kwargs):
        return await self.handler(*args, **kwargs)

    async def handler(self, *args, **kwargs):
        url = None
        if "hash" in kwargs:
            try:
                decoded_id = self.application.hasher.decode(kwargs['hash'])
                url = self.application.db.get(decoded_id[0])
                url = url.decode()
            except:
                return self.send_error(404, reason="Url not found.")
            self.application.db.delete(decoded_id[0])
            if not url.startswith("http"):
                url = "https://" + url
            return self.redirect(url)

        try:
            url = self.get_argument('url')
        except tornado.web.MissingArgumentError as e:
            logger.info("Missing url argument.")
            return await self.show_form()

        if not url:
            self.redirect("/")

        key = self.application.db.incr("id")
        encoded = self.application.hasher.encode(key)
        self.application.db.set(key, url)
        logger.debug(f"{args} {kwargs} {encoded} id: {key}")
        decoded = self.application.hasher.decode(encoded)
        logger.debug(f"Decoded: {decoded}")
        self.write(f"<a href='https://{conf.SHORTENER_URL}/{encoded}'>https://{conf.SHORTENER_URL}/{encoded}</a>")

    async def show_form(self):
        return self.write("""
                    <form method="GET" action=".">
                        <input type="text" name="url" value="" placeholder="Enter url to get short url"></input>
                        <button type="submit">Submit</button>
                    </form>
                    """)
