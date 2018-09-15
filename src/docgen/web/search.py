import flask
from flask.blueprints import Blueprint

from .auth import requires_login


blueprint = Blueprint('search', __name__)


@blueprint.route('/search')
@requires_login
def search():
    query = flask.request.args.get('for')
    results = flask.current_app.search.search(query, num_results=15)
    return flask.render_template('search.html.j2', results=results)
