import os

import bottle
import mistune

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

import config

BASE = '.'


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'

markdown = mistune.create_markdown(renderer=HighlightRenderer())

TEMPLATE = """
<html>
<head><title>{title}</title></head>
<body>
{body}
</body>
</html>
"""

TEMPLATE = open('static/post.html').read()


@bottle.get('/<path:path>')
def get_file(path):
    print(path)
    path = os.path.join('.', path)
    with open(path) as f:
        return f.read()


def render_all():
    for root, dirs, files in os.walk(config.MD_DIR):
        for f in files:
            source = os.path.join(root, f)
            source_name, ext = os.path.splitext(f)
            relpath = os.path.relpath(root, config.MD_DIR)
            dest = os.path.join(
                    config.HTML_DIR, relpath, source_name + '.html')
            with open(source) as source_file:
                dest_content = markdown(source_file.read())
            with open(dest, 'w') as dest_file:
                dest_file.write(TEMPLATE.format(
                    post_content=dest_content
                ))


if __name__ == '__main__':
    render_all()
    bottle.run(host='0.0.0.0', port=8080)
