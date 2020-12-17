import subprocess
import argparse
import time
import sys

sys.path.insert(0, "./scripts")
from scripts import validators as vali
from scripts import video_preview as vp
from scripts import inputs

# arguments recived
parser = argparse.ArgumentParser(
    description="syntax -> pyphonecam --ip 198.168.0.1 --port 8080")
parser.add_argument("--ip", help="ip adresss (e.g 198.168.0.1)",
                    type=str, required=True, metavar="'cam IP'")
parser.add_argument("--port", help="port number (e.g. 8080)",
                    type=str, required=True, metavar="'cam port'")
args = parser.parse_args()

# check if the url is valid
url = vali.url_validator(vali.ip_validator(args.ip), args.port)

# setup the v4l2loopback and recive the device index
v_index = str(inputs.inputs())


# ffmpeg cmd line arguments
ff_cmd = (
    f"ffmpeg -i {url}/video -f v4l2 -pix_fmt yuv420p /dev/video{v_index}")

if __name__ == '__main__':
    # start ffmpeg process
    subprocess.Popen(ff_cmd, shell=True)
    # get the process id
    pid = (''.join(filter(lambda i: i.isdigit(), str(
        subprocess.check_output(["pidof", "ffmpeg"])))))
    time.sleep(1)
    #start the preview window
    vp.preview_video(vp.device_index(v_index), pid)

        

 


sys.exit()
