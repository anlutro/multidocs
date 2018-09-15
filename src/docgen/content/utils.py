import re


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


def find_content(path, parent=None, root_path=None):
    items = []

    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isdir(file_path):
            LOG.debug("found folder (dir) at %r", file_path)
            folder = Folder(guess_file_title(file_name), parent=parent)
            # this will add child content as children to the folder. it will
            # also recurse to create children of children etc.
            get_content(file_path, parent=folder, root_path=root_path)
            items.append(folder)
        elif os.path.isfile(file_path) and file_path.endswith((".md", ".markdown")):
            LOG.debug("found page (file) at %r", file_path)
            with open(file_path, "r") as file_handle:
                content = file_handle.read()
            title = find_markdown_title(content) or guess_file_title(file_name)
            LOG.debug("guessed title=%r from file_path=%r", title, file_path)
            page = Page(title, content, parent=parent)
            page._source_path = file_path
            page._source_path_abs = os.path.abspath(file_path)
            if root_path:
                page._source_path = os.path.relpath(file_path, root_path)
            items.append(page)

    return items
