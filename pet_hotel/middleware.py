from werkzeug.wrappers import Request, Response


class Middleware:
    def __init__(self, app):
        self.app = app
        self.API_token = 'token'

    def __call__(self, environ, start_response):
        request = Request(environ)
        token = request.headers.get('api_token')
        if token == self.API_token:
            environ['user'] = 'Some token user'
            return self.app(environ, start_response)

        res = Response('Wrong api_token', mimetype='text/plain', status=401)
        return res(environ, start_response)
