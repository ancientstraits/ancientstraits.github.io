The reader (that is you) must have learnt about declarative programming.
In my quest to write a programming video generator named Codim,
I have thought about declarative programming and how it could change my library's API.

# What is Declarative Programming?
Declarative programming is when you tell the computer to perform an action,
instead of telling it to perform the steps in that action.
This means that functions can be a type of declarative structure.
For example, in Codim:
```c
static AVFrame* create_video_frame(AVCodecContext* vcc) {
    AVFrame* ret = av_frame_alloc();

    ret->format = vcc->pix_fmt;
    ret->width  = vcc->width;
    ret->height = vcc->height;
    av_frame_get_buffer(ret, 0);

    return ret;
}

void output_context_open(OutputContext* oc) {
    // ...
    oc->vf = create_video_frame(oc->vcc);
    // ...
}
```
The line starting with `oc->vf` could be called "declarative programming" because it just
tells a computer to let `oc->vf` be a video frame based on `oc->vcc`'s settings.

# "Markup-style" declarative programming
Although my example could be considered declarative, the reader (you again) probably thinks
that it's still primarily imperative, because it's using an imperative library in an
imperative programming language. The reader's first thought when hearing the word
"declarative programming" might be a React component:
```js
const MyComponent = ({time}) => (
    <div style={{color: 'blue'}}>
        <h1>The Time</h1>
        <p>The time is {time}.</p>
    </div>
)
```
In this case, `MyComponent` is declarative because it is returning the UI,
instead of telling some context to change each property.
The result is something a lot like markup, but in a programming language.
The opposite of this is the JavaScript canvas API:
```js
ctx.fillStyle = '#123456'
ctx.fillRect(12, 34, 56, 78)
```
The UI is not being returned all at once, and is being applied to a context.

# The Significance of Declarative Programming in Animation
Although it wouldn't hurt to write the canvas code above instead of using a React component,
it gets much worse when trying to draw something animated:
```js
let x = 0;
const loop = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    ctx.fillRect(x, 100, 20, 20)
    x++
    requestAnimationFrame(loop)
}
```
Definitely not something you can return. This could also not use iteration/recursion if the API stored the current time. Then it could all be declarative.
```js
const Rect = () => {
    const frame = useCurrentFrame()
    return (<svg>
        <rect x={frame} y="100" width="20" height="20">
    </svg>)
}
```
The above example is easy to understand because it just makes a vector of a rect with its
x value assigned to the frame number. No looping, which is done internally by the framework.
Speaking of the framework, the above code is actually valid syntax for Remotion, an animation
generator that uses React to render videos. I am not using it and instead wasting 8 months writing Codim because Remotion takes up an extreme amount of space for a single project, unlike 3Blue1Brown's Manim, which is just a binary that takes a single Python file as input.
Why am I not using Manim either? Because it's written mainly for math animations, not my niche.

# Declarative Programming in Codim
Codim will use LuaJIT for scripting, because Lua is very light and LuaJIT is faster than Node.
It it easy to maintain a declarative syntax in a scripting language like Lua.
One idea I have for the API is this:
```lua
local cm = require('codim')

function rect()
    return cm.rect {
        x = cm.frame,
        y = 100,
        width  = 20,
        height = 20,
    }
end

function main()
    return cm.frame <= 5 and cm.output{
        width  = 1920,
        height = 1080,
        fps    = 24,
        rect{},
    } or nil
end
```
The above code sample takes advantage of many things in Lua:

- Lua's `and / or` functions like a ternary statement, so we can use it to set the length of a video. In this case, the video is 5 seconds long. The video will end once `nil` is returned.
- In Lua, whenever a function is called with one string or one table, the parentheses in the function call are optional. This means that `fn('abc')` and `fn 'abc'` are the same, as well as `fn({a = 1})` and `fn{a = 1}`. This can save clutter when writing components.
- Lua's tables (`{}`) are the only non-scalar data structure, so they are both objects and arrays. Whenever the key isn't specified in an array, like `rect{}` in `main`, it will get assigned to an integer index, starting from 1. This means that the key of `rect{}` implicitly is 1. By assuming that a component's properties are string indices and a component's children are at integer indices, we can easily specify both the properties and children in one table.

# Declarative Is Not Always Better
While the above example of declarative programming might seem nice, it might be bad when we want to render multiple things in succession. One would have to do some magic to make sure everything comes one after another in time. In this case, imperative animation succeeds.
Take an example from Manim, which uses a more imperative API:
```py
class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set color and transparency

        square = Square()  # create a square
        square.rotate(PI / 4)  # rotate a certain amount

        self.play(Create(square))  # animate the creation of the square
        self.play(Transform(square, circle))  # interpolate the square into the circle
        self.play(FadeOut(square))  # fade out animation
```
Although React users would call this imperative, I really think it is more declarative than React. In this code sample, it is very easy to understand what will happen. A square rotated 45 degrees counterclockwise will be created, then will be animated into a pink, transparent circle, which will fade out. Notice that there are no dimensions or time measurement here - the only numbers are `PI / 4` and `0.5`. The programmer is telling the computer to perform an action instead of telling it how to, then trusting it to generate something suitable. This is the definition of declarative I defined at the start of this post. The programmer does not have to write any complicated components that vary dependent on time, that programmer just has to trust Manim that it will make a good video.

# The Quality of the Videos
The Python sample above creates [the video here](https://docs.manim.community/en/stable/tutorials/SquareToCircle2-1.mp4). Notice how much has been defined by the library itself - and for the better. The most beautiful generated videos are made declaratively, where the polish can be added in the library implementation. Once it is added, it becomes the reason that 3Blue1Brown's YouTube videos look so spectacular. It not only creates something good, but the code also looks good. This has to be the best fit for Codim - to let most things be as declarative as possible, so that there is as much potential to make beautiful videos as possible.
