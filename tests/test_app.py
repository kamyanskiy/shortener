import json
from tornado.platform.asyncio import AsyncIOMainLoop
from tornado.testing import AsyncHTTPTestCase

from webapp import app

class TestHelloApp(AsyncHTTPTestCase):
    def get_app(self):
        return app.make_app()

    def tearDown(self):
        AsyncIOMainLoop.clear_instance()
        super().tearDown()

    def test_get_root_url(self):
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body.decode(), """
                    <form method="GET" action=".">
                        <input type="text" name="url" value="" placeholder="Enter url to get short url"></input>
                        <button type="submit">Submit</button>
                    </form>
                    """)

    def test_get_short_url(self):
        response = self.fetch('/?url=http://kamyanskiy.github.io', method="GET")
        self.assertEqual(response.code, 200)
        link_id = int(self._app.db.get('id'))
        encoded = self._app.hasher.encode(link_id)

        expected = f"http://{app.conf.SHORTENER_URL}/{encoded}"

        self.assertEqual(response.body.decode(),
                         f"<a href='{expected}'>{expected}</a>")

    def test_get_short_url_twice_returns_404(self):
        response = self.fetch('/?url=http://kamyanskiy.github.io', method="GET")
        self.assertEqual(response.code, 200)
        link_id = int(self._app.db.get('id'))
        encoded = self._app.hasher.encode(link_id)

        expected = f"http://{app.conf.SHORTENER_URL}/{encoded}"

        self.assertEqual(response.body.decode(),
                         f"<a href='{expected}'>{expected}</a>")

        result1 = self.fetch(f"/{encoded}")
        self.assertEqual(result1.effective_url,
                         'https://kamyanskiy.github.io/')

        result2 = self.fetch(f"/{encoded}")
        self.assertEqual(result2.body.decode(),
                         '{"code": 404, "message": "Url not found."}')
