from CommonMarkExtensions.tables import ParserWithTables, RendererWithTables

from .utils import transform_url


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
            idx = markdown.index(line) + len(line)
            body = markdown[idx:].strip()
            break
        prev_line = line.strip()

    if not body:
        body = markdown
    return title, body.strip()


def page_to_html(page):
    ast = parser.parse(page.body)
    for node, entering in ast.walker():
        if entering and node.t == "link":
            node.destination = transform_url(node.destination, page)
    return renderer.render(ast)
