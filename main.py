import os
import json

import bottle
import mistune
import jinja2
import yaml

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import html

import config


class HighlightRenderer(mistune.HTMLRenderer):
    def block_code(self, code, lang=None):
        if lang:
            lexer = get_lexer_by_name(lang, stripall=True)
            formatter = html.HtmlFormatter()
            return highlight(code, lexer, formatter)
        return '<pre><code>' + mistune.escape(code) + '</code></pre>'

markdown = mistune.create_markdown(renderer=HighlightRenderer())


loader = jinja2.FileSystemLoader('templates')
jinja_env = jinja2.Environment(loader=loader)

TEMPLATE = open('templates/post.html').read()

@dataclass
class PostMeta:
    layout: str
    title: str
    date: datetime.date
    tags: List[str]
    categories: List[str]
    enabled: bool


    @classmethod
    def from_dict(cls, input_dict):
        post = cls()
        post.layout = input_dict['layout']
        post.title = input_dict['title']
        post.date = input_dict['date']
        post.enabled = input_dict.get('enabled', False)

        if isinstance(input_dict, list):
            post.tags = input_dict['tags']
        else:
            post.tags = input_dict['tags'].split()

        if isinstance(input_dict['categories'], list):
            post.categories = input_dict['categories']
        else:
            post.categories = input_dict['categories'].split()



<!---
layout: post
title:  "Una forma alterna de generar XML"
date:   2015-10-22
tags: python xml ats
categories: programacion python
-->




@bottle.get('/<path:path>')
def get_file(path):
    print(path)
    return bottle.static_file(path, root='.')


def render_content(content):
    header_end = 0
    header = {
            'title':'',
            'subtitle':'',
            'post_time': '',
            }
    if content.startswith('<!--'):
        # get rid first line
        header_start = content.find('\n', 1) + 1
        header_end = content.find('-->')
        header_txt = content[header_start:header_end]
        header.update(yaml.load(header_txt))
        print(header)
    content_html = markdown(content[header_end + 3:])
    return header, content_html


def render_md_file(dirname, filename):
    source = os.path.join(dirname, filename)
    source_name, ext = os.path.splitext(filename)
    relpath = os.path.relpath(dirname, config.MD_DIR)
    dest = os.path.join(
            config.HTML_DIR, relpath, source_name + '.html')
    with open(source) as source_file:
        dest_header, dest_content = render_content(source_file.read())
    with open(dest, 'w') as dest_file:
        dest_file.write(jinja_env.get_template('post.html').render(
            title=dest_header['title'],
            post_time=dest_header.get('date'),
            banner=dest_header.get('banner'),
            content=dest_content
        ))
    dest_header['href'] = os.path.join(relpath, source_name + '.html')
    return dest_header


def render_all():
    posts = []
    for root, dirs, files in os.walk(config.MD_DIR):
        for f in files:
            print(f)
            header = render_md_file(root, f)
            header['summary'] = 'I am summary'
            posts.append(header)

    with open(os.path.join(config.HTML_DIR, 'index.html'), 'w') as f:
        f.write(jinja_env.get_template('index.html').render(posts=posts))




if __name__ == '__main__':
    render_all()
    bottle.run(host='0.0.0.0', port=8080)
