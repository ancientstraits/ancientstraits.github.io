On the outside, `ffmpeg` seems like a very nice piece of software.
The `ffmpeg` command lets you convert videos into different formats and even pipe raw data very easily.
However, this CLI is simply an interface on top of a much larger (and scarier) set of libraries, including
`libavcodec` to encode and decode video,
`libavformat` to "open" and "close" video containers,
`libavfilter` to apply various filters to videos,
and several other libraries offering various utilities.

My application [codim](https://github.com/ancientstraits/codim) relies on FFmpeg to export an mp4 file.
A couple months ago, I had to go through the grueling process of writing code that interfaced with the libraries I listed.
The APIs can truly be unintuitive at times, and any subtle mistake can cause a frightening `segmentation fault (core dumped)`.
Yet I was able to finish the video-exporting code, and did not have to worry about it ever since.

Until I ran `make -B`.
Then, I saw the warnings:

```
src/output.c:100:47: warning: 'channels' is deprecated [-Wdeprecated-declarations]
        av_opt_set_int(ret, "in_channel_count", acc->channels, 0);
...
src/output.c:85:27: warning: 'channel_layout' is deprecated [-Wdeprecated-declarations]
        f->channel_layout = acc->channel_layout;
...
src/output.c:58:26: warning: 'av_get_channel_layout_nb_channels' is deprecated [-Wdeprecated-declarations]
                oc->acc->channels = av_get_channel_layout_nb_channels(oc->acc->channel_layout);
```

It seemed that `ffmpeg` had made some changes to its `channel` API.
I support breaking changes to projects in order to make them better, and there are only a few changes to make.
So it is time to do it.

# The New Channel API

Instead of `AVCodecContext->channel_layout`, I was meant to use `ch_layout`:
```c
/**
 * Audio channel layout.
 * - encoding: set by user.
 * - decoding: set by user, may be overwritten by libavcodec.
 * @deprecated use ch_layout
 */
attribute_deprecated
uint64_t channel_layout;
```
And instead of `AVCodecContext->channels`, I was meant to use `ch_layout.nb_channels`:
```c
/**
 * number of audio channels
 * @deprecated use ch_layout.nb_channels
 */
attribute_deprecated
int channels;
```

This is the declaration for AVChannelLayout:
```c
/**
 * Audio channel layout.
 * - encoding: must be set by the caller, to one of AVCodec.ch_layouts.
 * - decoding: may be set by the caller if known e.g. from the container.
 *             The decoder can then override during decoding as needed.
 */
AVChannelLayout ch_layout;
```

Look at what the comment asks for encoding. More stuff I have to do. At least it seems straighforward.
I do not understand what a channel layout is, I did not back then, I do not now.
My only objective is to meet the new API standards.

And here is the declaration of `AVCodec->ch_layouts`:
```c
/**
 * Audio channel layout.
 * - encoding: must be set by the caller, to one of AVCodec.ch_layouts.
 * - decoding: may be set by the caller if known e.g. from the container.
 *             The decoder can then override during decoding as needed.
 */
AVChannelLayout ch_layout;
```

# Reimplementation

I will have to replace this code that `ffmpeg` deems as deprecated:
```c
oc->acc->channels = av_get_channel_layout_nb_channels(oc->acc->channel_layout);
oc->acc->channel_layout = AV_CH_LAYOUT_STEREO;
```

I found this comment in the `AVChannelLayout` (type of `ch_layout`)'s documentation:
```c
/*
 * AVChannelLayout can be initialized as follows:
 * - default initialization with {0}, followed by setting all used fields
 *   correctly;
 * - by assigning one of the predefined AV_CHANNEL_LAYOUT_* initializers; <===!!!
 * - with a constructor function, such as av_channel_layout_default(),
 *   av_channel_layout_from_mask() or av_channel_layout_from_string().
 */
```
I also found, in the header, a `AV_CHANNEL_LAYOUT_STEREO`.
This will help me greatly.

I replaced my code with:
```c
oc->acc->ch_layout = AV_CHANNEL_LAYOUT_STEREO;
```
So it was swapping `ch` with `channel`. Pretty funny in my opinion.

...except its NOT THAT SIMPLE! GCC hits me with a vague `expected expression` error!
(this was probably because `AV_CHANNEL_LAYOUT_STEREO` expands into a struct literal,
and it seems that you cannot assign an already-declared variable to a struct literal in C.)

I finally found out from FFmpeg's wonderful `muxing.c` example file, the solution:
```c
av_channel_layout_copy(&c->ch_layout, &(AVChannelLayout)AV_CHANNEL_LAYOUT_STEREO);
```
A dedicated function to copy a few fields over. I love C so much.

After changing it to:
```c
av_channel_layout_copy(&oc->acc->ch_layout, &(AVChannelLayout)AV_CHANNEL_LAYOUT_STEREO);
```
to suit my needs, I replaced some usages of `acc->channels` with `acc->ch_layout.nb_channels`,
and now my program works perfectly! Very nice!

[Relevant Commit](https://github.com/ancientstraits/codim/commit/c3d6475437219f35f786aa7db0fcc129a9234ebb)


