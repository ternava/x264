# x264

The branch from the e9a5903edf commit of x264, the previously analysed version of x264. 

Here is a useful Dockerfile to clone and compile x264 (to its e9a5903edf commit). 
Author: LL

__Dockerfile__
```
FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y ffmsindex nasm git gcc make
RUN git clone https://github.com/mirror/x264
RUN cd x264 \
    && git reset --hard e9a5903edf8ca59ef20e6f4894c196f135af735e \
    && ./configure --disable-avs --enable-pic --enable-shared \
    && make
```
It works well in Windows for encoding a **.mkv** and **.avs** file to **.mkv.** For example:

```
$ x264 -o "outputfile.avs" "video.mkv" --input-res 720x576
```
But, not for encoding to **.mp4** or from **.mp4**. For the first case, I receive a clear error:
```
$ x264 -o "outputfile.mp4" "video.mkv" --input-res 720x576
x264 [error]: not compiled with MP4 output support
```
Whereas, for the second case, the whole video is encoded in one frame.

```
.....
encoded 1 frames, 13.97 fps, 54384.80 kb/s
```
