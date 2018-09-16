import os.path

from CommonMarkExtensions.tables import ParserWithTables, RendererWithTables


parser = ParserWithTables()
renderer = RendererWithTables()


def extract_title(markdown):
    """ Given markdown text, return the title and body. """
    body = None
    title = None
    prev_line = None
    for line in markdown.splitlines():
        # prevent comments in code blocks from becoming titles
        if line.startswith("```"):
            break
        if line.startswith("# "):
            title = line[2:].strip()
        elif prev_line and line.count("=") >= len(prev_line) / 2:
            title = prev_line
        if title:
            idx = markdown.index(title) + len(title)
            body = markdown[idx:].strip()
        prev_line = line.strip()

    if not body:
        body = markdown
    return title, body.strip()


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
    return renderer.render(ast)
