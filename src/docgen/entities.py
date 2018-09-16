import os.path

import slugify


class Source:
    def __init__(self, url, root_dir, title=None, slug=None):
        self.url = url
        self.root_dir = root_dir
        self.title = title or os.path.basename(url)
        self.slug = slug or slugify.slugify(self.title)
        self.path = self.slug
        self.children = set()

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.url)


class GitSource(Source):
    def __init__(self, *args, branch=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.branch = branch


class Path:
    def __init__(self, path, parent=None):
        self.path = path
        self.basename = os.path.basename(path)
        self.dirname = os.path.dirname(path)
        self.children = set()
        self.parent = parent
        if parent:
            parent.children.add(self)

    def __repr__(self):
        return "<%s %r>" % (self.__class__.__name__, self.path)

    def __gt__(self, other):
        return self.path > other.path


class SourcePath(Path):
    def __init__(self, path, parent=None, source=None):
        super().__init__(path, parent=parent)
        if source is None:
            source = self.parent
            while not isinstance(source, Source):
                source = source.parent
        self.source = source


class SourceFile(SourcePath):
    is_dir = False


class SourceDirectory(SourcePath):
    is_dir = True


class Content(Path):
    def __init__(self, path, source, title=None, parent=None, slug=None):
        super().__init__(path, parent=parent)
        self.source = source
        self.title = title or os.path.basename(path)
        self.slug = slug or slugify.slugify(self.title)


class Directory(Content):
    is_dir = True


class ContentSource(Directory):
    def __init__(self, source):
        super().__init__(
            source.slug, source, title=source.title, parent=None, slug=source.slug
        )


class Page(Content):
    is_dir = False

    def __init__(self, path, source, body, title=None, parent=None, slug=None):
        super().__init__(path, source, title=title, parent=parent, slug=slug)
        self.body = body
