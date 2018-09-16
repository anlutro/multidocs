import os
import os.path
import re

import bleach.linkifier

from docgen.globals import config, settings, j2
from docgen.search import get_search
from docgen.sources import download_source
from docgen import entities
from . import markdown


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


linker = bleach.linkifier.Linker(callbacks=[_linkify_callback])


def guess_file_title(file_name):
    parts = re.split(r"[_.-]+", file_name.split(".")[0])
    return " ".join(parts).capitalize()


def iter_path(node):
    yield from node.children
    for child in node.children:
        yield from iter_path(child)


def get_title_and_body(path):
    title = None
    with open(path) as fh:
        body = fh.read()
    if path.endswith(".md"):
        title, body = markdown.extract_title(body)
    return title, body


def page_to_html(page, source=None):
    source = source or page.source
    if source.path.endswith(".md"):
        html = markdown.page_to_html(page)
    else:
        raise ValueError("unknown page source type: %r" % source)
    html = linker.linkify(html)
    return html


def generate_html():
    sources = {}
    for source_cfg in config["sources"]:
        source = download_source(**source_cfg)
        sources[source] = entities.ContentSource(source)

    root = entities.ContentRoot(sources.values())
    contents = {None: root}

    # convert source objects to content objects
    for source, content_source in sources.items():
        contents[source] = content_source

        for path in iter_path(source):
            kwargs = dict(
                parent=contents.get(path.parent),
                path=content_source.path + "/" + path.path,
                slug=path.basename,
                source=path,
            )

            if isinstance(path, entities.SourceDirectory):
                cls = entities.Directory
            else:
                cls = entities.Page
                kwargs["path"] = os.path.splitext(kwargs["path"])[0] + ".html"
                kwargs["title"], kwargs["body"] = get_title_and_body(
                    os.path.join(source.root_path, path.path)
                )

            if not kwargs.get("title"):
                kwargs["title"] = guess_file_title(path.basename)

            content = cls(**kwargs)
            contents[path] = content

    sources = list(sources.values())

    # write HTML from content objects
    for content in contents.values():
        content_path = os.path.join(settings.target_dir, content.path)

        if content.is_dir:
            content_dir = content_path
            content_path = os.path.join(content_path, "index.html")
        else:
            content.html = page_to_html(content)
            content_dir = os.path.dirname(content_path)

        html = j2.get_template("content.html.j2").render(content=content, root=root)

        if not os.path.exists(content_dir):
            os.makedirs(content_dir)

        with open(content_path, "w+") as fh:
            fh.write(html)

    # store content in the search index
    get_search().index_contents(root)

    # store the sidebar HTML separately so it can be used in dynamic pages
    sidebar_path = os.path.join(settings.target_dir, "_sidebar.html")
    html = j2.get_template("sidebar.html.j2").render(root=root)
    with open(sidebar_path, "w+") as fh:
        fh.write(html)


def get_sidebar_html():
    sidebar_path = os.path.join(settings.target_dir, "_sidebar.html")
    if os.path.exists(sidebar_path):
        with open(sidebar_path) as fh:
            return fh.read()
