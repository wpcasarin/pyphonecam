import subprocess
import argparse
import time
import sys

sys.path.insert(0, "./scripts")

from scripts import inputs
from scripts import validators

# aguments recived
parser = argparse.ArgumentParser(
    description="syntax -> pyphonecam --ip 198.168.0.1 --port 8080")
parser.add_argument("--ip", help="ip adresss (e.g 198.168.0.1)",
                    type=str, required=True, metavar="'cam IP'")
parser.add_argument("--port", help="port number (e.g. 8080)",
                    type=str, required=True, metavar="'cam port'")
args = parser.parse_args()

# check if the url is valid
url = validators.url_validator(validators.ip_validator(args.ip), args.port)

# setup the v4l2loopback and recive the device index
v_index = str(inputs.inputs())

# ffmpeg cmd line arguments
ff_cmd = (f"ffmpeg -re -i {url}/video -f v4l2 -pix_fmt yuv420p /dev/video{v_index}")

# make the virtual device recive the video data
subprocess.Popen(ff_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

# get the ffmpeg process pid id
pid = (''.join(filter(lambda i: i.isdigit(), str(subprocess.check_output(["pidof", "ffmpeg"])))))


window_name = ("'pyPhoneCam'")

time.sleep(2)

# create a preview window
subprocess.Popen(f"ffplay -fflags nobuffer -an -sn -window_title {window_name} /dev/video{v_index}", shell=True)

time.sleep(1)

# kill the ffmpeg process if the preview window is closed
while True:
    try:
        subprocess.check_output(f"xprop -name {window_name}", stderr=subprocess.DEVNULL, shell=True)
    except subprocess.CalledProcessError:
        subprocess.Popen(f"killall ffmpeg", shell=True)
        break

sys.exit()
