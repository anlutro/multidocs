import logging
import os
import os.path
import shutil

import whoosh.index
import whoosh.fields
import whoosh.qparser

log = logging.getLogger(__name__)

schema = whoosh.fields.Schema(
    title=whoosh.fields.TEXT(stored=True),
    path=whoosh.fields.ID(stored=True),
    src_path=whoosh.fields.ID(stored=True),
    content=whoosh.fields.TEXT,
)


class Result:
    def __init__(self, path, src_path, title, highlight=None):
        self.path = path
        self.src_path = src_path
        self.title = title
        self.highlight = highlight


class Search:
    def __init__(self, path):
        self.idx_path = path
        if not os.path.exists(self.idx_path):
            self.indexer = self._create_index()
        try:
            self.indexer = whoosh.index.open_dir(path)
        except whoosh.index.EmptyIndexError:
            log.warning('error reading whoosh index, re-creating')
            self._create_index()

    def _create_index(self):
        if os.path.exists(self.idx_path):
            shutil.rmtree(self.idx_path)
        os.makedirs(self.idx_path)
        return whoosh.index.create_in(self.idx_path, schema)

    def add_contents(self, contents):
        if os.path.exists(self.idx_path):
            shutil.rmtree(self.idx_path)
        os.makedirs(self.idx_path)
        self.indexer = whoosh.index.create_in(self.idx_path, schema)
        Indexer(self.indexer.writer()).run(contents)

    def search(self, search_for, num_results=5):
        qp = whoosh.qparser.QueryParser('content', self.indexer.schema)
        query = qp.parse(search_for)
        ret = []
        with self.indexer.searcher() as searcher:
            for hit in searcher.search(query)[:num_results]:
                highlight = src_path = None
                if 'src_path' in hit:
                    src_path = hit['src_path']
                    with open(src_path) as fh:
                        contents = fh.read()
                    highlight = hit.highlights('content', text=contents)
                result = Result(
                    path=hit['path'],
                    title=hit['title'],
                    highlight=highlight,
                    src_path=src_path
                )
                ret.append(result)
        return ret


class Indexer:
    def __init__(self, writer):
        self.writer = writer

    def run(self, contents):
        for content in contents:
            self.add_index(content)
        log.info('committing search index')
        self.writer.commit()

    def add_index(self, content):
        if hasattr(content, 'content'):
            log.debug('adding content to search index: %r', content)
            self.writer.add_document(
                title=content.title,
                path=content.get_path(),
                src_path=getattr(content, '_source_path_abs', None),
                content=content.content,
            )

        for child in content.children:
            self.add_index(child)


def get_search():
    from docgen.globals import settings
    Search(settings.source_dir + '/_idx')
