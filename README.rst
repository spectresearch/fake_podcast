
Fake Podcast
===============

It's a python script to simulate a podcast. It takes a directory with audio or
video files (file formats accepted by Itunes) and creates a temporal podcast in
a desired local network interface. Then it can be added in Itunes as a normal
podcast, you can download audio/video files and synchronize with your iPod.

The project objective is to add audio/video files of courses, conferences and
so on, and these don't be mixed with the music.

Supported format files by Itunes are: m4a, .mp3, .mov, .mp4, .m4v, and .pdf.
As it's a normal podcast, I think it should be read successfully by any
program, but it's not tested yet.

Requirements
*************

No requirements.


Installation
*************

You can get fake_podcast from github with: ::
    
    git clone git://github.com/spectresearch/fake_podcast.git

Then you run it: ::

    cd fake_podcast/src/
    python fake_podcast.py 


Usage
******

**fake_podcast.py** needs two arguments:

1) A directory where there are audio/videos files that will be the content of
the podcast.

2) The ip:port of a network interface where start the webserver .  It's an
optional argument, it is 127.0.0.1:8000 by default.

Then, you can run fake_podcast.py without problems: ::

    $ python fake_podcast.py /media/conf
    Setting up web server on 127.0.0.1:8000 ..
    Your fake podcast url is: http://127.0.0.1:8000/conf/fake_podcast.rss

You must add the provided fake podcast url in Itunes, and you can enjoy it as a
normal podcast.
If you want to update your podcast, use the same directory and ip:port again.
