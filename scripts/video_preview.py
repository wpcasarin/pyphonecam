import tkinter as tk
import subprocess as sp
import imageio
import sys
from PIL import Image, ImageTk


def device_index(index):
    video_name = (f"<video{index}>")
    video = imageio.get_reader(video_name)
    return video

# generate frames from a cam input


def frame_generator(video):

    for frame, image in enumerate(video.iter_data()):

        # turn video array into an image and reduce the size
        image = Image.fromarray(image)
        image.thumbnail((750, 750), Image.ANTIALIAS)

        # make image in a tk Image and put in the label
        image = ImageTk.PhotoImage(image)

        yield frame, image


def preview_video(video, pid):

    root = tk.Tk()
    root.title("pyPhoneCam")

    label = tk.Label(root)
    label.pack()

    vid_frame = frame_generator(video)

    while True:
        frame_number, frame = next(vid_frame)
        label.config(image=frame)

        root.update()
        
        # kill the ffmpeg process if the preview window is closed
        try:
            sp.check_output(f"xprop -name 'pyPhoneCam'", stderr=sp.DEVNULL, shell=True)
        except sp.CalledProcessError:
            sp.Popen(f"kill {pid}", shell=True)
            sys.exit("pyPhoneCam finished!")
        
    root.mainloop()
