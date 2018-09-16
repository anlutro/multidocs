import flask
from flask.blueprints import Blueprint

from docgen.content import get_sidebar_html
from .auth import requires_login


blueprint = Blueprint("search", __name__)


@blueprint.route("/search")
@requires_login
def search():
    query = flask.request.args.get("for")
    results = flask.current_app.search.search(query, num_results=15)
    sidebar_html = get_sidebar_html()
    return flask.render_template(
        "search.html.j2", query=query, results=results, sidebar_html=sidebar_html
    )
