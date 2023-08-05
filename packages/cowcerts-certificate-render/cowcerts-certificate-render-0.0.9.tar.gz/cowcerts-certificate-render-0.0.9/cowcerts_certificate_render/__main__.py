"""Cowcerts certificate render entry point."""
import pkgutil
import json
import os
import sys

from flask import Flask
from jinja2 import Template
from bs4 import BeautifulSoup
import htmlmin
from inlinestyler.utils import inline_css
from livereload import Server

CURRENT_MODULE = "cowcerts_certificate_render"

DATA_DIR = "data"

TEMPLATES_DIR = os.path.join(
    DATA_DIR,
    "templates"
)

CERTIFICATES_DIR = os.path.join(
    DATA_DIR,
    "certificates"
)

DEFAULT_TEMPLATE_FILE = os.path.join(
    TEMPLATES_DIR,
    "cowcerts-for-education.html"
)

DEFAULT_EDS_TEMPLATE_FILE = os.path.join(
    TEMPLATES_DIR,
    "cowcerts-eds.html"
)

DEFAULT_CERTIFICATE_FILE = os.path.join(
    CERTIFICATES_DIR,
    "cowcerts-edu-20190422.json"
)

SERVER_HOST = "localhost"

SERVER_PORT = 8081


def main():
    # Template selection
    template = DEFAULT_TEMPLATE_FILE
    if "-e" in sys.argv or "--eds" in sys.argv:
        template = DEFAULT_EDS_TEMPLATE_FILE

    html = read_html_template(template)
    certificate = read_certificate()

    # Serve
    if len(sys.argv) > 1 and sys.argv[1] in ("-s", "--serve"):
        app = Flask(__name__)
        app.debug = True
        @app.route('/')
        def main_route():
            return beautify_html(render_html(
                read_html_template(template), certificate))
        server = Server(app.wsgi_app)
        print("Serving certificate at http://%s:%d" % (SERVER_HOST, SERVER_PORT))
        server.watch("cowcerts_certificate_render/data/templates/*.html")
        server.serve(SERVER_PORT, None, SERVER_HOST)
    # Embed
    else:
        # No EDS
        if "-e" in sys.argv or "--eds" in sys.argv:
            print("EDS embedding not implemented yet")
            return
        html = minify_html(
            extract_html_body(
                inline_css_styles(
                    render_html(html, certificate))))
        certificate["displayHtml"] = html
        print(json.dumps(certificate))


def read_html_template(template_file=DEFAULT_TEMPLATE_FILE):
    return load_file(template_file)


def load_file(filename):
    return pkgutil.get_data(CURRENT_MODULE, filename).decode("utf-8")


def read_certificate(certificate_file=DEFAULT_CERTIFICATE_FILE):
    return json.loads(load_file(certificate_file))


def render_html(html, context):
    return Template(html).render(context)


def beautify_html(html):
    return BeautifulSoup(
        html,
        features="html.parser"
    ).prettify()


def inline_css_styles(html):
    return inline_css(html)


def extract_html_body(html):
    return ''.join(
        '%s' % l for l in BeautifulSoup(
            html,
            features="lxml"
        ).body.contents)


def minify_html(html):
    return htmlmin.minify(html, remove_empty_space=True)


if __name__ == "__main__":
    main()
