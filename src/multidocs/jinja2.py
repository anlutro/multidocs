import datetime
import jinja2


def get_jinja2_env():
    j2 = jinja2.Environment(
        loader=jinja2.PackageLoader(__name__, "templates"),
        undefined=jinja2.StrictUndefined,
    )
    j2.globals["now"] = datetime.datetime.now()
    return j2
