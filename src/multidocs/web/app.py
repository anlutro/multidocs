import os.path

import flask
import multidocs.globals
import multidocs.search
import multidocs.web.auth
import multidocs.web.search
import multidocs.web.static


def get_app():
    static_folder = os.path.join(os.path.dirname(__file__), "static")
    app = flask.Flask("multidocs", static_folder=static_folder)
    app.secret_key = multidocs.globals.settings.secret_key
    app.search = multidocs.search.get_search()
    app.auth = multidocs.web.auth.get_authenticator(app)

    app.register_blueprint(multidocs.web.auth.blueprint)
    app.register_blueprint(multidocs.web.search.blueprint)
    app.register_blueprint(multidocs.web.static.blueprint)

    return app


def run_server(host="0.0.0.0", port=5000, debug=False):
    from werkzeug.serving import run_simple

    run_simple(host, port, get_app(), use_reloader=debug, use_debugger=debug)
