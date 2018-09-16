import argparse
import os
import os.path
import logging


def serve_webapp(args):
    import docgen.web.app
    docgen.web.app.run_server()


def generate_html(args):
    import docgen.content
    docgen.content.generate_html()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config")
    parser.add_argument("command")
    args = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)

    if args.config:
        os.environ.setdefault("DOCGEN_CONFIG_FILE", os.path.abspath(args.config))
        os.chdir(os.path.dirname(os.environ["DOCGEN_CONFIG_FILE"]))

    if args.command == "serve":
        return serve_webapp(args)
    if args.command == "generate":
        return generate_html(args)
    raise ValueError("unknown command: %r" % args.command)
