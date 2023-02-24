#!/usr/bin/env python3

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import os
from os import path
import re
import time
import shutil
import subprocess
from typing import List

from markdown import markdown, Markdown
from markdown.extensions.codehilite import CodeHiliteExtension
import chevron
import pygments
import pygments.formatters


def title_case(snake: str) -> str:
    def title_repl(match):
        return re.sub('_', ' ', match.group(1)) \
        + match.group(2).upper() + match.group(3)
    return re.sub(r'(_|)([a-z])([a-z]*)', title_repl, snake)


def snake_case(title: str) -> str:
    def title_repl(match):
        return re.sub(' ', '_', match.group(1)) \
        + match.group(2).lower() + match.group(3)
    return re.sub(r'( |)([A-Z])([a-z]*)', title_repl, title)


def file_date(filename: str) -> datetime:
    date = subprocess.check_output([
        'git', 'log', '--follow',
        '--format=%ad', '--date=default',
        filename,
    ]).decode('utf-8').split('\n')[0]
    return parsedate_to_datetime(date)


def check_dir(dirname: str):
    if not path.exists(dirname):
        os.mkdir(dirname)


def pygments_css(style: str, arg='.codehilite') -> str:
    fmt = pygments.formatters.html.HtmlFormatter(style=style)
    return fmt.get_style_defs(arg=arg)


class PostDate:
    dt: datetime

    def __init__(self, dt: datetime):
        self.dt = dt

    def __str__(self) -> str:
        return self.dt.strftime('%d %b %Y at %I:%M %p')


class Post:
    title:   str
    url:     str
    date:    PostDate
    content: str

    def __init__(self, filename: str):
        self.url     = re.sub('.md', '.html', filename)
        self.title   = title_case(re.sub('.md', '', filename))
        self.date    = PostDate(file_date(path.join('src', filename)))
        with open(path.join('src', filename), 'r') as f:
            self.content = f.read()

    def compile(self):
        md = Markdown(extensions=[
            'fenced_code', 'codehilite', 'sane_lists', 'meta'
        ])
        self.content = md.convert(self.content)
        if 'title' in md.Meta:
            self.title = ' '.join(md.Meta['title'])


    def write(self):
        with open('template/post.html', 'r') as f:
            rendered = chevron.render(f, self.__dict__)

        filename = path.join('build', self.url)
        with open(filename, 'w', encoding='utf-8', errors='xmlcharrefreplace') as f:
            f.write(rendered)


def main():
    check_dir('build')

    posts = []
    for filename in os.listdir('src'):
        p = Post(filename)
        p.compile()
        p.write()
        posts.append(p)

    posts.sort(reverse=True, key=lambda p: p.date.dt)

    map(lambda p: p.__dict__, posts)

    with open('template/index.html', 'r') as f:
        rendered = chevron.render(f, {'posts': posts})
    with open('build/index.html', 'w') as f:
        f.write(rendered)

    shutil.copytree('style', 'build/style', dirs_exist_ok=True)
    with open('build/style/codehilite.css', 'w') as f:
        f.write(pygments_css(style='gruvbox-dark'))


if __name__ == '__main__':
    main()
