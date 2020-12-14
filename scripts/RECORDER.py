#THIS CODE IS A MESS 
#


import gi
import cv2 as cv
import numpy as np
import subprocess
import png
from PIL import Image

gi.require_version('Gtk', '3.0')
from gi.repository import GdkX11
from gi.repository import Gdk
from gi.repository import GdkPixbuf as Pixbuf


win_name = "VLC media player"

def get_xid(win_name):
    
    xid = int(subprocess.check_output(f"xdotool search --name '{win_name}'", shell=True))
    return xid

def get_window_from_xid(xid):
    display = GdkX11.X11Display.get_default()
    return GdkX11.X11Window.foreign_new_for_display(display, xid)


def capture_window(window):
    sz = window.get_geometry()[2:4]
    pb = Gdk.pixbuf_get_from_window(window, 0, 0, sz[0], sz[1])
    return pb


def pixbuf_to_array(pb):
    w, h, c, r = (pb.get_width(), pb.get_height(),
                  pb.get_n_channels(), pb.get_rowstride())
    assert pb.get_colorspace() == Pixbuf.Colorspace.RGB
    assert pb.get_bits_per_sample() == 8
    if pb.get_has_alpha():
        assert c == 4
    else:
        assert c == 3
    assert r >= w * c
    a = np.frombuffer(pb.get_pixels(), dtype=np.uint8)
    if a.shape[0] == w*c*h:
        return a.reshape((h, w, c))
    else:
        b = np.zeros((h, w*c), 'uint8')
        for j in range(h):
            b[j, :] = a[r*j:r*j+w*c]
        return b.reshape((h, w, c))

xid = get_xid(win_name)

from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

cmd_out = ['ffmpeg','-re','-framerate','30','-y','-i','pipe:0', '-vcodec', 'rawvideo','-pix_fmt', 'yuv420p','-f', 'v4l2', '/dev/video0']

pipe = subprocess.Popen(cmd_out, stdin=subprocess.PIPE)

try:
    while True:

        window = get_window_from_xid(xid)
        pb = capture_window(window)
        frame = pixbuf_to_array(pb)
        #frame = cv.cvtColor(frame, cv.COLOR_RGB2BGR)
        #cv.imshow("TEST", frame)

        img = Image.fromarray(frame, 'RGB')
        
        img.save(pipe.stdin, 'jpeg', quality=100)
        
        # if cv.waitKey(1) == ord("q"):
        #     break
except KeyboardInterrupt:
    pass


print("DONE")

