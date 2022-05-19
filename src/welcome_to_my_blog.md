# Introduction
This is my blog, which I made using a Python script.
The source code for the blog is available on [my GitHub repository](https://github.com/ancientstraits/ancientstraits.github.io).

# A Trick In Python
I have automated the process of running `ssg.py` on GitHub pages,
meaning that I can write the blog post on the GitHub website, commit it, and it will
build it for me.
My blog script, `ssg.py` (stands for Static Site Generator),
uses the modules `markdown` and `chevron`.
However, I want to install them without having to type the commands into the
GitHub configuration file.

There is a trick that can be done to automatically install any module if it doesn't exist:
```py
import os

try:
    import <module>
except ImportError:
    os.system('pip3 install <module>')
    import <module>
```
Some may say it's cursed, I say it's a great feature.

# How it Works
In the `src` folder, my blog posts reside in Markdown format.
Their filename are in snake_case and are converted to Title Case by the script.
For example, this article is called `welcome_to_my_blog.md`,
so the title you see is "Welcome To My Blog".
This means that the filename is the title, so I don't need to write it in my Markdown file.

## The `PostDate` class
I made a new `PostDate` class in order to format the dates like how they would be
in a blog (not like the ISO format):
```py
class PostDate:
    dt: datetime

    def __init__(self, dt: datetime):
        self.dt = dt

    def __str__(self) -> str:
        return self.dt.strftime('%w %b %Y at %I:%M %p')
```
This means that a template file can just say `{{date}}` for a `PostDate` object `date`,
and my script will format the date correctly.


## Classes in Python are Nice
I defined a class in Python to hold my post:
```py
class Post:
    title:   str
    url:     str
    date:    PostDate
    content: str
```
The best part of putting all the attributes in a class in this case is that
the templating engine `chevron` can easily use these variables:
```py
with open('template/post.html', 'r') as f:
    rendered = chevron.render(f, self.__dict__)
```
`chevron` takes in a `dict` for variables, but luckily in scripting languages like Python,
it is easy to convert between an object and `dict`. In Ruby, you use the `.attributes` method
to convert an object to a hash, and in Javascript, the object is already a hash.
I wonder how difficult it would be to do the same thing in C.

# Sorting by Date
The landing page of this blog has a list of blogs sorted by date. I easily did that with this
function:
```py
def add_and_sort(posts: List[Post], post: Post):
    index = 0
    for i in range(len(posts) - 1):
        if posts[i].date.dt >= post.date.dt >= posts[i + 1].date.dt:
            index = i
            break
    posts.insert(index, post)
```
Focus on the line starting with `if`. in C, that statement would be more like:
```c
if (date_cmp(posts[i].date.dt, post.date.dt) >= 0
    && date_cmp(post, posts[i + 1].date.dt) >= 0)
```

# The Highlighting Process
As you can see in the code blocks, this code is highlighted. How does this work?
I used the "Fenced Code Blocks" python-markdown extension while processing the
markdown in my script:
```py
def compile(self):
    self.content = markdown(self.content, extensions=['fenced_code'])
```
Whenever this extension detects a markdown code block that has a name after the
opening three backticks, it adds it to a class based on the name.
For example, for the upper code block:
```html
<pre><code class="language-py">
def compile(self):
    self.content = markdown(self.content, extensions=['fenced_code'])
</code></pre>
```

The script `highlight.js` recognizes this, and highlights the code. It is the only
client-side code in my site (besides the obligatory method call to it), so my blog is
very minimal and fast. Although `highlight.js` highlights on the client-side, it
just doesn't feel like it, because it runs extremely quickly.

# Rewrite in C?
I am comparing everything to C because I regularly use C to write applications.
However, I realized that C might not be a great idea for an application like this.

Still, I love the C programming language for its simplicity and speed, which is why
I write so many programs in C. I will eventually rewrite this program in C, and I
will write a blog post about that new program.

# Frontend Design
The last thing I want to talk about is designing the frontend. As a systems developer,
this at first seems easy, but gets very difficult. I have to keep looking things up
about CSS, and I have to make sure everything looks just right.
Eventually, though, I got to my current style, and I think it looks very beautiful.
The borders on the code blocks were actually unintentional, as they were a side efect
of this CSS:
```css
pre {
    background-color: #333;
    padding: 10px;
}
```
Although there is no actual border, the padding of the `pre` element combined with its
dark color against my `highlight.js` theme's light background color creates the border. I actually find it very nice, and I think it goes well with my website.
