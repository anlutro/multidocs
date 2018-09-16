import os.path

from CommonMarkExtensions.tables import ParserWithTables, RendererWithTables
import bleach.linkifier


def _linkify_callback(attrs, new=False):
    if not new:
        return attrs

    # try to filter out things that might look like URLs but aren't
    if (
        not attrs["_text"].startswith(("http:", "https:", "www."))
        and "/" not in attrs["_text"]
    ):
        return None

    return attrs


parser = ParserWithTables()
renderer = RendererWithTables()
linker = bleach.linkifier.Linker(callbacks=[_linkify_callback])


def transform_url(url, page):
    # don't do anything with absolute URLs
    if url.startswith(("http:", "https:", "//")):
        return url

    # rewrite non-absolute markdown URLs to HTML
    if url.endswith(".md"):
        url = url[:-3] + ".html"

    # from this point on we only need to tweak URLs that
    # could point to parent directories
    if not url.startswith(("./", "../")):
        return url

    # if URL has more .. than page.path has slashes, the relative URL goes
    # beyond the scope of the page's source and there's nothing we can do
    if page.source and url.count("..") < len(page.path.split("/")):
        return url

    new_url = page.url
    if "/" in page.path:
        new_url += "/" + os.path.dirname(page.path)
    new_url += "/" + url
    return new_url


def page_to_html(page):
    ast = parser.parse(page.body)
    for node, entering in ast.walker():
        if entering and node.t == "link":
            node.destination = transform_url(node.destination, page)
    html = renderer.render(ast)
    html_linkified = linker.linkify(html)
    return html_linkified
