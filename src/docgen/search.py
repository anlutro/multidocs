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
    body=whoosh.fields.TEXT,
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
            self.index = self._create_index()
        try:
            self.index = whoosh.index.open_dir(path)
        except whoosh.index.EmptyIndexError:
            log.warning("error reading whoosh index, re-creating")
            self._create_index()

    def _create_index(self):
        if os.path.exists(self.idx_path):
            shutil.rmtree(self.idx_path)
        os.makedirs(self.idx_path)
        return whoosh.index.create_in(self.idx_path, schema)

    def index_contents(self, root):
        # re-create the index, wiping existing data
        self.index = self._create_index()
        writer = self.index.writer()

        def _index(content):
            if hasattr(content, "body"):
                log.debug("adding content to search index: %r", content)
                writer.add_document(
                    title=content.title,
                    path=content.path,
                    src_path=content.source.abspath,
                    body=content.body,
                )

            for child in content.children:
                _index(child)

        _index(root)

        log.info("committing search index")
        writer.commit()

    def search(self, search_for, num_results=5):
        qp = whoosh.qparser.QueryParser("body", self.index.schema)
        query = qp.parse(search_for)
        ret = []
        with self.index.searcher() as searcher:
            for hit in searcher.search(query)[:num_results]:
                highlight = src_path = None
                if "src_path" in hit:
                    src_path = hit["src_path"]
                    with open(src_path) as fh:
                        contents = fh.read()
                    highlight = hit.highlights("body", text=contents)
                result = Result(
                    path=hit["path"],
                    title=hit["title"],
                    highlight=highlight,
                    src_path=src_path,
                )
                ret.append(result)
        return ret


def get_search():
    from docgen.globals import settings

    return Search(settings.source_dir + "/_idx")
