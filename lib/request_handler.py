from tornado.web import RequestHandler

class ApiHandler(RequestHandler):
    def api_response(self, data, code=200, reason=None):
        self.set_header('Content-Type', 'application/json')
        self.set_status(code, reason=reason)
        self.write(data)
        self.finish()
