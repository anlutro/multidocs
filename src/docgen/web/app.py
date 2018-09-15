import flask
import docgen.globals
import docgen.search
import docgen.web.auth
import docgen.web.search
import docgen.web.static


def get_app():
    app = flask.Flask('docgen')
    app.secret_key = docgen.globals.settings.secret_key
    app.search = docgen.search.get_search()
    app.auth = docgen.web.auth.get_authenticator()

    app.register_blueprint(docgen.web.auth.blueprint)
    app.register_blueprint(docgen.web.search.blueprint)
    app.register_blueprint(docgen.web.static.blueprint)

    return app


def run_server(host='0.0.0.0', port=5000, debug=False):
	from werkzeug.serving import run_simple
	run_simple(host, port, get_app(), use_reloader=debug, use_debugger=debug)
