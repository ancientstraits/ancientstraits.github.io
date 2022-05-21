#!/usr/bin/env python3

from datetime import datetime, timezone
import os
from os import path
import re
import time
import shutil
from typing import List

# just so I don't have to run these commands
try:
    from markdown import markdown
except ImportError:
    os.system('pip3 install markdown')
    from markdown import markdown
try:
    import chevron
except ImportError:
    os.system('pip3 install chevron')
    import chevron


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
    mtime = os.stat(filename).st_mtime
    return datetime.fromtimestamp(mtime, tz=timezone.utc)


def check_dir(dirname: str):
    if not path.exists(dirname):
        os.mkdir(dirname)


class PostDate:
    dt: datetime

    def __init__(self, dt: datetime):
        self.dt = dt

    def __str__(self) -> str:
        return self.dt.strftime('%w %b %Y at %I:%M %p')


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
        self.content = markdown(self.content, extensions=['fenced_code'])

    def write(self):
        filename = path.join('build', snake_case(self.title)) + '.html'
        with open('template/post.html', 'r') as f:
            rendered = chevron.render(f, self.__dict__)
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


if __name__ == '__main__':
    main()
