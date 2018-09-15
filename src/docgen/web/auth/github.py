import fnmatch

import flask
from flask_oauthlib.client import OAuth

from . import Authenticator
from docgen.globals import settings


def _matches_conf(items, configs):
    if not isinstance(configs, (list, tuple, set)):
        configs = (configs,)
    return any(
        (any((fnmatch.fnmatch(item, conf) for item in items)) for conf in configs)
    )


class GithubAuthenticator(Authenticator):
    is_oauth = True
    session_key = "github_token"

    def __init__(self, app):
        self.gh = OAuth(app).remote_app(
            "github",
            consumer_key=settings.auth_github_key,
            consumer_secret=settings.auth_github_secret,
            access_token_method="POST",
            access_token_url="https://github.com/login/oauth/access_token",
            authorize_url="https://github.com/login/oauth/authorize",
            base_url="https://api.github.com/",
            request_token_params={"scope": "read:org"},
            request_token_url=None,
        )
        self.gh.tokengetter(self.get_github_oauth_token)

    def get_github_oauth_token(self):
        return flask.session.get(self.session_key)

    def is_logged_in(self):
        return bool(flask.session.get(self.session_key))

    def is_allowed(self):
        if settings.auth_github_orgs not in ("all", "*"):
            org_names = {o["login"] for o in self.gh.get("user/orgs").data}
            if not _matches_conf(org_names, settings.auth_github_orgs):
                return False

        if settings.auth_github_teams not in ("all", "*"):
            team_names = {o["name"] for o in self.gh.get("user/teams").data}
            if not _matches_conf(team_names, settings.auth_github_teams):
                return False

        return True

    def login(self):
        return self.gh.authorize(callback=flask.url_for("authorized", _external=True))

    def oauth_authorize(self):
        resp = self.gh.authorized_response()

        if not resp or not resp.get("access_token"):
            flask.abort(
                403,
                "<br>".join(
                    (
                        "Access denied! Reason: %s" % flask.request.args["error"],
                        "Description: %s" % flask.request.args["error_description"],
                        flask.request.args["error_uri"],
                    )
                ),
            )

        flask.session[self.session_key] = (resp["access_token"], "")

    def logout(self):
        flask.session.pop(self.session_key, None)


def get_authenticator(app=flask.current_app):
    return GithubAuthenticator(app)
