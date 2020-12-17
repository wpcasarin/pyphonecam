
import subprocess
import argparse
import time
import sys

sys.path.insert(0, "./scripts")
from scripts import validators
from scripts import inputs


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
ff_cmd = (f"ffmpeg -i {url}/video -f v4l2 -pix_fmt yuv420p /dev/video{v_index}")

if __name__ == '__main__':

    try:    
        subprocess.Popen(ff_cmd, shell=True)
        pid = (''.join(filter(lambda i: i.isdigit(), str(subprocess.check_output(["pidof", "ffmpeg"])))))
    except KeyboardInterrupt:
        subprocess.Popen("killall ffmpeg")
    finally:
        sys.exit()
    

