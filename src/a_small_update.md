I have updated the [blogging system](https://github.io/ancientstraits/ancientstraits.github.io) in two new ways:

1. Replaced `highlight.js` (client-side) with `pygments` (server-side) for syntax highlighting
2. Added `meta` OpenGraph tags to make links look better in embeds

# Pygments and CodeHilite
Initially, my blogging script, [ssg.py](https://github.com/ancientstraits/ancientstraits.github.io/blob/master/ssg.py),
has worked by solely using the `fenced_code_blocks` extension for `python-markdown`, which puts code into a `pre` element without adding syntax highlighting.
The blog post used to load `highlight.js` into the browser to highlight the code blocks after the page was loaded.
This is clearly inefficient, because it adds JavaScript(TM) to my blog pages, and forces the browser to parse each block of code whenever it is loaded.
Now, the page uses `python-markdown`'s CodeHilite extension instead, which separates each lexical block into a `span` element, each of which is highlighted with a CSS class.
These CSS classes can be styled by using `pygments` to export a CSS file to implement the color of each class:
```py

def pygments_css(style: str, arg='.codehilite') -> str:
    fmt = pygments.formatters.html.HtmlFormatter(style=style)
    return fmt.get_style_defs(arg=arg)

Which is the Python equivalent of `pygmentize -S [style] -f html -a .codehilite` in Bash.
As of writing, I have chosen this style to be `gruvbox-dark`.
Unfortunately, I cannot change the whole style of the codeblocks simply by changing the `style` argument,
since I also have to change the foreground and background colors manually in `style/style.css`.

# OpenGraph
OpenGraph tags are used when someone posts your program's link to a social media site, such as Twitter.
They are used to retrieve more information, so that a box of info about the website appears under the message where the link was posted.
I have added `title` and `url` tags to my post template:
```html
<meta name=og:title content={{title}}>
<meta name=og:url content=ancientstraits.github.io>
```
This will perhaps make my posts gain more popularity when shared.

