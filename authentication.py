from werkzeug.wrappers import Response, Request
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
import jwt
import datetime

secret_key = key = "QWd-4ylNhsOnNK5-iSmFovx4zUCdk79ghGIl-wGfBCYR9lqBwYESHVMmQDtrEiS_OvBVg2HRsfHWu9VIJ0BfzHYijrim_23740CCLWnRyK6eWjQ79eVt3HLHyxtHfSV9urdGPGNToKLv81BBAZb_bNkLXSuuiI4H4omOgr2x0upkHSGjV4kR24r_hXf5XkCZDz3yeYXbauhiPomk1VdWwRX7aV_AyCoR-GMwrpGl3JVHFVhP549A0P6eUP7Saodxd6k4VcRlHhSIknsgzQ4gA5uKZbQtc6C0ITC2Jk7YdAyk2qIg_1hb8nRoSfQGRzzeO0sgy104YVf3RUiHe_CEVg"

class Authentication(object):

  def __init__(self):
     self.url_map = Map([
         Rule('/', endpoint='authenticate'),
         Rule('/secret', endpoint='secret')
     ])

  def dispatch_request(self, request):
      adapter = self.url_map.bind_to_environ(request.environ)
      try:
          endpoint, values = adapter.match()
          return getattr(self, 'on_' + endpoint)(request, **values)
      except HTTPException, e:
          return e
  
  def wsgi_app(self, environ, start_response):
      request = Request(environ)
      response = self.dispatch_request(request)
      return response(environ, start_response)

  def __call__(self, environ, start_response):
      return self.wsgi_app(environ, start_response)

  def on_authenticate(self, request):
      if request.method == 'POST':
          user = request.form['user']
          password = request.form['password']
          encoded = jwt.encode({'user': user, 'password': password, 'iat': datetime.datetime.utcnow(), 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, secret_key, algorithm='HS256')
          return Response(encoded)

  def on_secret(self, request):
      if request.method == 'GET':
          return Response(secret_key)

def create_app():
    app = Authentication()
    return app

if __name__ == '__main__':
    from werkzeug.serving import run_simple
    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)