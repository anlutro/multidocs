import os.path
from urllib.parse import urlsplit, urlunsplit


def transform_url(url, page, source=None):
    source = source or page.source
    urlparts = urlsplit(url)

    # don't do anything with absolute URLs
    if urlparts.netloc or urlparts.path.startswith("/"):
        return url

    # if URL has more .. than page.path has slashes, the relative URL goes
    # beyond the scope of the source root which means it's not part of the
    # generated HTML, so we need to fall back on the source URL
    if source and url.split("/").count("..") >= len(page.path.split("/")):
        urlparts = urlsplit(source.url + "/" + urlparts.path)
        new_path = os.path.normpath(urlparts.path)
        return urlunsplit((urlparts.scheme, urlparts.netloc, new_path, "", ""))

    # at this point we know we're dealing with a relative URL which is inside
    # the multidocs directory, so we can safely replace md with html
    if url.endswith(".md"):
        url = url[:-3] + ".html"

    return url
