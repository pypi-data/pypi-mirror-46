from werkzeug.serving import make_server
import threading


class ServerThread(threading.Thread):
    """
    https://stackoverflow.com/questions/15562446/how-to-stop-flask-application-without-using-ctrl-c/45017691#45017691
    """

    _server = None
    _context = None

    def __init__(self, app, port, host="0.0.0.0"):
        threading.Thread.__init__(self, name="{} ({}:{})".format(__class__.__name__, host, port))
        self._server = make_server(app=app, port=port, host=host)
        self._context = app.app_context()
        self._context.push()

    def run(self):
        self._server.serve_forever()

    def stop(self):
        self._server.shutdown()
