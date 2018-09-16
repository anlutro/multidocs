import os.path
import subprocess

from docgen.globals import settings
from docgen.entities import GitSource

from .path import populate_source_from_path


def github_cb(path, source):
    path_type = "tree" if path.is_dir else "blob"
    path.url = f"{source.url}/{path_type}/{source.branch}/{source.root_dir}/{path.path}"


def populate_urls(node, source, url_cb):
    for child in node.children:
        url_cb(child, source)
        populate_urls(child, source, url_cb)


def populate_source_urls(source):
    source_url = source.url.replace("ssh://", "").replace(
        "git@github.com", "https://github.com"
    )

    if source_url.startswith("https://github.com"):
        populate_urls(source, source, github_cb)


def download_source(url, **kwargs):
    env = {}
    ssh_key = kwargs.pop("ssh_key", None) or settings.git_ssh_key
    if ssh_key:
        env["GIT_SSH_COMMAND"] = "ssh -i %s" % ssh_key

    source = GitSource(url, **kwargs)
    git_path = os.path.join(settings.source_dir, source.slug)
    if os.path.exists(os.path.join(git_path, ".git")):
        res = subprocess.run(
            ["git", "-C", git_path, "remote", "-v"],
            env=env,
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        # todo: this needs to be improved
        if url not in res.stdout:
            print(res.stdout)
            raise RuntimeError("url not in git remote")
        subprocess.run(["git", "-C", git_path, "pull", "-q"], env=env, check=True)
    else:
        subprocess.run(["git", "clone", "-q", url, git_path], env=env, check=True)

    if not source.branch:
        res = subprocess.run(
            ["git", "-C", git_path, "rev-parse", "--abbrev-ref", "HEAD"],
            env=env,
            capture_output=True,
            encoding="utf-8",
            check=True,
        )
        source.branch = res.stdout.strip()

    populate_source_from_path(source, os.path.join(git_path, source.root_dir))
    populate_source_urls(source)

    return source
