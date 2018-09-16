import os
import os.path
import re

from docgen.globals import config, settings, j2
from docgen.sources import download_source
from docgen import entities

from .markdown import page_to_html


def find_markdown_title(markdown):
    prev_line = None
    for line in markdown.splitlines():
        # prevent comments in code blocks from becoming titles
        if line.startswith("```"):
            return
        if line.startswith("# "):
            return line[2:].strip()
        if prev_line and line.count("=") >= len(prev_line) / 2:
            return prev_line
        prev_line = line.strip()


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

    for source, content_source in sources.items():
        contents = {source: content_source}

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
                    kwargs["title"] = find_markdown_title(kwargs["body"])

            if not kwargs.get("title"):
                kwargs["title"] = guess_file_title(path.basename)

            content = cls(**kwargs)
            contents[path] = content

    for content in contents.values():
        content_path = os.path.join(settings.target_dir, content.path)

        if content.is_dir:
            html = j2.get_template("directory.html.j2").render(
                directory=content, sources=sources.values()
            )
            content_dir = content_path
            content_path = os.path.join(content_path, "index.html")
        else:
            page_html = page_to_html(content)
            html = j2.get_template("page.html.j2").render(
                page=content, page_html=page_html, sources=sources.values()
            )
            content_dir = os.path.dirname(content_path)

        if not os.path.exists(content_dir):
            os.makedirs(content_dir)

        with open(content_path, "w+") as fh:
            fh.write(html)
