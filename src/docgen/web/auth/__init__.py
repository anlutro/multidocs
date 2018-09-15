import functools

import flask
from flask import current_app
from flask.blueprints import Blueprint

from docgen.globals import settings


class Authenticator:
    is_oauth = False

    def is_logged_in(self):
        raise NotImplementedError()

    def is_allowed(self):
        raise NotImplementedError()

    def login(self):
        raise NotImplementedError()


def requires_login(func):
    """ Route decorator that enforces login. """
    if not settings.auth_required:
        return func

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        auth = flask.current_app.auth
        if not auth.is_logged_in():
            return login()
        if not auth.user_is_authorized():
            logout()
            return "You do not have access to this resource.", 403
        return func(*args, **kwargs)

    return wrapper


blueprint = Blueprint("auth", __name__)


@blueprint.route("/login")
def login():
    if settings.auth_required:
        return current_app.auth.login()
    return flask.redirect(flask.url_for("index"))


@blueprint.route("/login/authorized")
def authorized():
    if settings.auth_required:
        if not current_app.auth.is_oauth:
            raise RuntimeError(
                "attempting oauth authorized callback without"
                "an oauth-enabled Authenticator!"
            )
        current_app.auth.oauth_authorize()
    return flask.redirect(flask.url_for("index"))


@blueprint.route("/logout")
def logout():
    current_app.auth.logout()
    return "You have been logged out."


def get_authenticator(app=flask.current_app):
    import importlib

    mod = importlib.import_module(__name__ + "." + settings.auth_type)
    return mod.get_authenticator(app)
