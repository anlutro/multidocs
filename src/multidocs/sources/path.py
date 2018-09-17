import os
import os.path

from multidocs.entities import SourceFile, SourceDirectory


def populate_children(parent, path, root_path):
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.name.startswith("."):
                continue

            relpath = os.path.relpath(entry.path, root_path)
            if entry.is_dir(follow_symlinks=False):
                sd = SourceDirectory(relpath, parent=parent)
                parent.children.add(sd)
                populate_children(sd, entry.path, path)
            else:
                sf = SourceFile(relpath, parent=parent)
                parent.children.add(sf)


def populate_source_from_path(source, path):
    source.root_path = path
    populate_children(source, path, path)
