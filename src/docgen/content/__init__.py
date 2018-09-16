import os
import os.path
import re

import bleach.linkifier

from docgen.globals import config, settings, j2
from docgen.sources import download_source
from docgen import entities
from .markdown import page_to_html, extract_title


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


def generate_html():
    sources = {}
    for source_cfg in config["sources"]:
        source = download_source(**source_cfg)
        sources[source] = entities.ContentSource(source)

    root = entities.ContentRoot(sources.values())
    contents = {None: root}

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

                with open(os.path.join(source.root_path, path.path)) as fh:
                    file_contents = fh.read()
                kwargs["body"] = file_contents

                if path.path.endswith(".md"):
                    kwargs["title"], kwargs["body"] = extract_title(kwargs["body"])

            if not kwargs.get("title"):
                kwargs["title"] = guess_file_title(path.basename)

            content = cls(**kwargs)
            contents[path] = content

    sources = list(sources.values())

    for content in contents.values():
        content_path = os.path.join(settings.target_dir, content.path)

        if content.is_dir:
            html = j2.get_template("directory.html.j2").render(
                directory=content, root=root
            )
            content_dir = content_path
            content_path = os.path.join(content_path, "index.html")
        else:
            page_html = page_to_html(content)
            page_html = linker.linkify(page_html)
            html = j2.get_template("page.html.j2").render(
                page=content, page_html=page_html, root=root
            )
            content_dir = os.path.dirname(content_path)

        if not os.path.exists(content_dir):
            os.makedirs(content_dir)

        with open(content_path, "w+") as fh:
            fh.write(html)
