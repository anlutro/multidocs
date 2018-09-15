import os.path

import flask
from flask.blueprints import Blueprint

from docgen.globals import settings
from .auth import requires_login


blueprint = Blueprint('static', __name__)


@blueprint.route('/<path:path>')
@requires_login
def static_file(path):
    full_path = os.path.join(settings.target_dir, path)
    if os.path.isdir(full_path):
        path += '/index.html'

    return flask.send_from_directory(
        settings.target_dir,
        path,
        cache_timeout=-1,
    )


@blueprint.route('/')
def index():
    return static_file('index.html')
